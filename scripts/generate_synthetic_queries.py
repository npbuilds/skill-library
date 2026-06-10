#!/usr/bin/env python3
"""Generate synthetic user queries per skill for retrieval indexing.

Re-Invoke pattern (Wang et al., EMNLP 2024 Findings): indexing each skill
with LLM-generated queries that real users would type — rather than only the
author's description — closes the query/description vocabulary gap and lifts
retrieval recall. Generated queries feed the search index (BM25 + embeddings)
as extra "documents" pointing at their skill.

Output: data/synthetic_queries.json
  {
    "version": 1,
    "generated_with": "<model>",
    "skills": {
      "<skill>": {
        "content_hash": "<sha256(desc + body)>",
        "index_queries": [7 queries],   # used to build the index
        "eval_queries":  [3 queries]    # held out for eval (never indexed)
      }, ...
    }
  }

The index/eval split is fixed at generation time so the retrieval eval can
never test on a query that was also indexed (contamination guard lives in
eval_retrieval.py too).

Usage:
  python3 scripts/generate_synthetic_queries.py                 # all stale/new
  python3 scripts/generate_synthetic_queries.py --only-stale    # alias of default
  python3 scripts/generate_synthetic_queries.py --force         # regenerate all
  python3 scripts/generate_synthetic_queries.py --skills a,b    # just these
  python3 scripts/generate_synthetic_queries.py --limit 8       # first N (testing)
  python3 scripts/generate_synthetic_queries.py --dry-run       # show one prompt
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic_queries.json"

# Use the index's canonical content hash so the generator's stored hashes and
# the index's staleness check can never drift apart.
sys.path.insert(0, str(PROJECT_ROOT / "mcp-server"))
from search_index import synthetic_content_hash, SYNTHETIC_BODY_EXCERPT_CHARS  # noqa: E402

BATCH_SIZE = 8
QUERIES_PER_SKILL = 10
INDEX_SPLIT = 7  # nominal index/eval split; _filter_and_split adapts it
# Cap shared with the canonical hash so the prompt excerpt and the hashed body
# stay aligned.
BODY_EXCERPT_CHARS = SYNTHETIC_BODY_EXCERPT_CHARS
DEFAULT_MODEL = "haiku"

_STRIP_FM_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def _read_skill_md(location: str) -> str:
    """Read a skill's raw SKILL.md text (with frontmatter)."""
    try:
        return (PROJECT_ROOT / location).read_text(errors="replace")
    except OSError:
        return ""


def _body_excerpt(raw_md: str) -> str:
    """Frontmatter-stripped, capped body for the generation prompt."""
    return _STRIP_FM_RE.sub("", raw_md, count=1).strip()[:BODY_EXCERPT_CHARS]


def _echoes_name(query: str, name: str) -> bool:
    """True if a query trivially echoes the skill's NAME.

    Only filters queries that contain the full slug as a phrase (hyphenated
    or space-separated), not individual topic words. Filtering single common
    tokens (e.g. "color" for color-theory) wrongly drops good on-topic queries
    and was the cause of ~123 skills failing to produce a valid split.
    """
    q = query.lower()
    slug = name.lower()
    return slug in q or slug.replace("-", " ") in q


def _build_prompt(batch: list[dict]) -> str:
    """Prompt for a batch of skills → JSON {skill: [queries]}."""
    lines = [
        f"You are generating realistic search queries for a skill library. "
        f"For EACH skill below, write exactly {QUERIES_PER_SKILL} distinct queries "
        f"a real user would type when they need that skill's help.",
        "",
        "Rules:",
        "- Vary phrasing: questions, commands, problem statements, keyword fragments.",
        "- Write what a user wants to DO, not the skill's name. Do NOT include the "
        "skill's slug or its hyphenated words verbatim.",
        "- Keep each query under 15 words. No numbering, no explanations.",
        "",
        "Skills:",
    ]
    for s in batch:
        lines.append(f"\n### {s['name']}")
        lines.append(f"Description: {s['description']}")
        if s["body"]:
            lines.append(f"Excerpt: {s['body'][:400]}")
    lines.append(
        f"\nOutput ONLY a JSON object mapping each skill name to an array of "
        f"{QUERIES_PER_SKILL} query strings. No prose, no markdown fences."
    )
    return "\n".join(lines)


def _call_claude(prompt: str, model: str) -> str:
    """Run `claude -p` and return the model's text result."""
    proc = subprocess.run(
        ["claude", "-p", "--output-format", "json", "--model", model],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI failed ({proc.returncode}): {proc.stderr[:300]}")
    outer = json.loads(proc.stdout)
    return outer.get("result", "")


def _parse_batch(text: str, batch: list[dict]) -> dict[str, list[str]]:
    """Parse the model's JSON object; tolerate markdown fences."""
    cleaned = _FENCE_RE.sub("", text).strip()
    data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object mapping skill → queries")
    out: dict[str, list[str]] = {}
    names = {s["name"] for s in batch}
    for name, queries in data.items():
        if name in names and isinstance(queries, list):
            out[name] = [str(q).strip() for q in queries if str(q).strip()]
    return out


def _filter_and_split(name: str, queries: list[str]) -> dict | None:
    """Drop name-echoing queries, then split into index/eval sets.

    Reserves the last ~30% (min 1) of surviving queries for eval and indexes
    the rest, so the split adapts when filtering leaves fewer than 10 queries
    — rather than failing whenever <8 survive.
    """
    kept = [q for q in queries if not _echoes_name(q, name)]
    if len(kept) < 2:
        return None  # need at least one index + one eval query
    kept = kept[:QUERIES_PER_SKILL]
    # Reserve ~30% for eval (at least 1, at most 3), index the remainder.
    n_eval = max(1, min(3, len(kept) // 3))
    split = len(kept) - n_eval
    index_q, eval_q = kept[:split], kept[split:]
    if not index_q or not eval_q:
        return None
    return {"index_queries": index_q, "eval_queries": eval_q}


def _atomic_write_json(path: Path, data) -> None:
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".json.tmp", delete=False
        ) as f:
            tmp = f.name
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError):
        if tmp and os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--skills", help="comma-separated skill names to (re)generate")
    ap.add_argument("--limit", type=int, help="cap number of skills (testing)")
    ap.add_argument("--force", action="store_true", help="regenerate even if hash matches")
    ap.add_argument("--only-stale", action="store_true",
                    help="default behavior; only generate new/changed skills")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the first batch prompt and exit without calling the model")
    args = ap.parse_args()

    registry = json.loads(REGISTRY_PATH.read_text())["skills"]
    existing = {}
    if OUTPUT_PATH.exists():
        try:
            existing = json.loads(OUTPUT_PATH.read_text()).get("skills", {})
        except (json.JSONDecodeError, OSError):
            existing = {}

    only = set(args.skills.split(",")) if args.skills else None

    # Assemble the work list, computing content hashes for staleness.
    work: list[dict] = []
    fresh_kept = {}
    for name, entry in sorted(registry.items()):
        if entry.get("status") != "active":
            continue
        if only is not None and name not in only:
            continue
        desc = entry.get("description", "")
        raw_md = _read_skill_md(entry.get("location", ""))
        body = _body_excerpt(raw_md)
        chash = synthetic_content_hash(desc, raw_md)
        prev = existing.get(name)
        is_stale = (prev is None) or (prev.get("content_hash") != chash)
        if not args.force and not is_stale:
            fresh_kept[name] = prev  # unchanged — carry forward
            continue
        work.append({"name": name, "description": desc, "body": body, "content_hash": chash})

    if args.limit:
        # Carry forward any beyond the limit so we don't drop existing entries.
        for s in work[args.limit:]:
            if s["name"] in existing:
                fresh_kept[s["name"]] = existing[s["name"]]
        work = work[:args.limit]

    print(f"{len(work)} skill(s) to generate, {len(fresh_kept)} unchanged "
          f"(carried forward), model={args.model}")

    if not work:
        print("Nothing to generate.")
        return 0

    if args.dry_run:
        print("\n--- DRY RUN: first batch prompt ---\n")
        print(_build_prompt(work[:BATCH_SIZE]))
        return 0

    # Start from everything already on disk (carried-forward unchanged skills
    # plus any prior run's results) so a kill mid-run never loses progress and
    # re-running with --only-stale resumes from where it stopped.
    result_skills = dict(existing)
    result_skills.update(fresh_kept)

    def _checkpoint():
        _atomic_write_json(OUTPUT_PATH, {
            "version": 1,
            "generated_with": args.model,
            "skills": result_skills,
        })

    failed: list[str] = []
    n_batches = (len(work) + BATCH_SIZE - 1) // BATCH_SIZE
    for i in range(0, len(work), BATCH_SIZE):
        batch = work[i:i + BATCH_SIZE]
        names = [s["name"] for s in batch]
        print(f"  batch {i // BATCH_SIZE + 1}/{n_batches}: {', '.join(names)}",
              flush=True)
        parsed = None
        for attempt in (1, 2):  # retry once
            try:
                text = _call_claude(_build_prompt(batch), args.model)
                parsed = _parse_batch(text, batch)
                break
            except (RuntimeError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
                print(f"    attempt {attempt} failed: {e}", file=sys.stderr, flush=True)
        if parsed is None:
            failed.extend(names)
            continue
        hash_by_name = {s["name"]: s["content_hash"] for s in batch}
        for name in names:
            split = _filter_and_split(name, parsed.get(name, []))
            if split is None:
                failed.append(name)
                continue
            result_skills[name] = {"content_hash": hash_by_name[name], **split}
        # Persist after every batch — checkpoint so a kill is never total loss.
        _checkpoint()

    _checkpoint()
    total_idx = sum(len(s.get("index_queries", [])) for s in result_skills.values())
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}: "
          f"{len(result_skills)} skills, {total_idx} index queries.")
    if failed:
        print(f"  {len(failed)} skill(s) failed: {', '.join(failed[:10])}"
              f"{'...' if len(failed) > 10 else ''}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
