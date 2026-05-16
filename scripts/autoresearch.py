#!/usr/bin/env python3
from __future__ import annotations
"""
autoresearch.py — Autonomous skill improvement loop.

Mirrors Karpathy's autoresearch pattern:
  Propose → Apply → Score → Keep/Revert → Log → Repeat

Improvement levers (ordered by expected ROI):
  1. ADD_REF_FILE   — extract tables/code from SKILL.md → references/quick-reference.md
  2. FIX_DESC       — fix descriptions outside the ideal 20-60 word range
  3. CLEAN_DEPS     — remove depends_on entries pointing to non-existent skills

Metrics tracked per experiment:
  - composite_score delta
  - per-dimension breakdown (structure, depth, connectivity, freshness, usage, feedback)

Usage:
    python3 scripts/autoresearch.py                    # dry-run, all skills
    python3 scripts/autoresearch.py --apply            # run and commit changes
    python3 scripts/autoresearch.py --apply --n 20     # top 20 lowest-scoring skills
    python3 scripts/autoresearch.py --apply --domain sommelier
    python3 scripts/autoresearch.py --report           # show experiment history
"""

import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
USAGE_LOG     = PROJECT_ROOT / "data" / "usage.jsonl"
FEEDBACK_LOG  = PROJECT_ROOT / "data" / "feedback.jsonl"
AR_LOG        = PROJECT_ROOT / "data" / "autoresearch_log.jsonl"


# ── Scoring (inlined from recalibrate_scores.py) ─────────────────────────────

def score_structure(metrics: dict) -> int:
    section_count = metrics.get("section_count", 0)
    desc_words    = metrics.get("description_words", 0)
    body_words    = metrics.get("body_words", metrics.get("word_count", 0))
    score = 50
    # Density-adjusted section score (mirrors recalibrate_scores.py)
    length_factor = max(1.0, body_words / 500)
    adj_sc = section_count / length_factor
    if 1.0 <= adj_sc <= 5.0:    score += 25
    elif 0.5 <= adj_sc <= 10.0: score += 15
    if 20 <= desc_words <= 60:    score += 25
    elif 15 <= desc_words <= 100: score += 15
    else:                          score += 5
    return score

def score_depth(metrics: dict) -> int:
    body_words = metrics.get("body_words", metrics.get("word_count", 0))
    ref_files  = metrics.get("reference_files", 0)
    if 300 <= body_words <= 5000:    score = 75
    elif body_words < 300:           score = max(10, int(body_words / 300 * 75))
    else:                            score = max(40, 75 - int((body_words - 5000) / 500))
    score += min(30, ref_files * 10)
    return min(100, score)

def score_connectivity(entry: dict) -> int:
    total = len(entry.get("depends_on", [])) + len(entry.get("referenced_by", []))
    if total == 0:   return 20
    elif total <= 2: return 40
    elif total <= 5: return 65
    elif total <= 10: return 85
    else:            return 100

def score_freshness(entry: dict, now: datetime) -> int:
    last_mod = entry.get("last_modified", "2020-01-01")
    try:
        mod_date = datetime.fromisoformat(last_mod).replace(tzinfo=timezone.utc)
        days_old = (now - mod_date).days
    except (ValueError, TypeError):
        days_old = 90
    if days_old <= 7:   return 100
    elif days_old <= 30: return 80
    elif days_old <= 60: return 60
    elif days_old <= 90: return 40
    else: return max(20, 40 - int((days_old - 90) / 30) * 5)

def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists(): return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try: events.append(json.loads(line))
            except json.JSONDecodeError: pass
    return events

def compute_composite(entry: dict, now: datetime,
                      usage_counts: Counter, max_usage: int,
                      feedback_ratings: dict) -> tuple[int, dict]:
    metrics = entry.get("metrics", {})
    name    = entry["name"]
    s_struct = score_structure(metrics)
    s_depth  = score_depth(metrics)
    s_conn   = score_connectivity(entry)
    s_fresh  = score_freshness(entry, now)
    uses     = usage_counts.get(name, 0)
    s_usage  = min(100, int((uses / max_usage) * 80) + 20) if max_usage > 0 and uses > 0 else 0
    ratings  = feedback_ratings.get(name, [])
    s_fb     = int(sum(ratings) / len(ratings) * 20) if ratings else 50
    composite = round(
        s_struct * 0.20 + s_depth * 0.25 + s_conn * 0.20 +
        s_fresh  * 0.15 + s_usage * 0.10 + s_fb * 0.10
    )
    breakdown = dict(structure=s_struct, depth=s_depth, connectivity=s_conn,
                     freshness=s_fresh, usage=s_usage, feedback=s_fb)
    return composite, breakdown


# ── Reference file extraction ─────────────────────────────────────────────────

_TABLE_RE = re.compile(
    r'(?:^#{2,4}[ \t]+([^\n]+)\n+)?'          # optional heading
    r'((?:\|[^\n]+\|\n)+\|[-|: ]+\|\n'         # header + separator
    r'(?:\|[^\n]+\|\n){1,30})',                 # 1-30 data rows
    re.MULTILINE,
)
_CODE_RE = re.compile(
    r'(?:^#{2,4}[ \t]+([^\n]+)\n+)?'           # optional heading
    r'```[^\n]*\n(.*?)```',
    re.MULTILINE | re.DOTALL,
)


def _title(s: str) -> str:
    return s.replace("-", " ").title()


def build_quick_reference(skill_name: str, skill_md_path: Path) -> Optional[str]:
    """Extract tables and compact code blocks from SKILL.md into a reference file."""
    content = skill_md_path.read_text(errors="replace")
    sections: list[tuple[str, str]] = []  # (heading, body)

    # Extract tables (must have ≥3 rows to be useful)
    for m in _TABLE_RE.finditer(content):
        heading = (m.group(1) or "Quick Reference").strip()
        table   = m.group(2).strip()
        if len(table.splitlines()) >= 3:
            sections.append((heading, table))

    # Extract code blocks that are compact enough to be useful as references
    for m in _CODE_RE.finditer(content):
        heading = (m.group(1) or "Formula / Pseudocode").strip()
        code    = m.group(2).strip()
        if 10 < len(code) < 700 and "\n" in code:  # multi-line, not a wall of text
            fence = "```\n" + code + "\n```"
            sections.append((heading, fence))

    if not sections:
        return None

    # Deduplicate (keep first occurrence), cap at 8 sections
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for h, b in sections:
        key = b[:80]
        if key not in seen:
            seen.add(key)
            unique.append((h, b))
        if len(unique) >= 8:
            break

    lines = [f"# {_title(skill_name)} — Quick Reference\n"]
    for h, b in unique:
        lines.append(f"## {h}\n\n{b}")
    return "\n\n".join(lines) + "\n"


# ── Description fixer ─────────────────────────────────────────────────────────

_YAML_DESC_RE = re.compile(
    r"^description:\s*[>|]\s*\n((?:[ \t]+.+\n)+)", re.MULTILINE
)
_INLINE_DESC_RE = re.compile(r"^description:\s+(.+)$", re.MULTILINE)


def fix_description(entry: dict, skill_path: Path) -> Optional[str]:
    """Return a corrected description string, or None if no fix is needed/possible."""
    content = skill_path.read_text(errors="replace")
    dw = entry.get("metrics", {}).get("description_words", 0)

    m = _YAML_DESC_RE.search(content)
    if m:
        raw = " ".join(line.strip() for line in m.group(1).strip().splitlines())
    else:
        m2 = _INLINE_DESC_RE.search(content)
        raw = m2.group(1).strip() if m2 else ""

    words = raw.split()
    if 20 <= len(words) <= 60:
        return None  # already fine

    if len(words) > 60:
        # Truncate to 55 words, end cleanly at a period if possible
        truncated = " ".join(words[:55])
        last_period = truncated.rfind(".")
        if last_period > 30:
            truncated = truncated[: last_period + 1]
        return truncated

    # Too short — try to pull a better description from the first paragraph after the H1
    h1_match = re.search(r"^# .+\n+((?:[^\n].+\n)+)", content, re.MULTILINE)
    if h1_match:
        para = h1_match.group(1).strip().replace("\n", " ")
        para_words = para.split()
        if 20 <= len(para_words) <= 80:
            return " ".join(para_words[:60])

    return None  # can't improve automatically


# ── Experiment runner ─────────────────────────────────────────────────────────

def _reload_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def _save_registry(reg: dict) -> None:
    with open(REGISTRY_PATH, "w") as f:
        json.dump(reg, f, indent=2)
        f.write("\n")

def _log_experiment(record: dict) -> None:
    AR_LOG.parent.mkdir(exist_ok=True)
    record["timestamp"] = datetime.now(timezone.utc).isoformat()
    with open(AR_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")


def run_experiment(
    skill_name: str,
    lever: str,
    apply_fn,       # () -> bool   — makes the change, returns True if applied
    revert_fn,      # () -> None   — undoes the change
    now: datetime,
    usage_counts: Counter,
    max_usage: int,
    feedback_ratings: dict,
    dry_run: bool,
) -> dict:
    """
    Generic experiment harness.
    Returns a record dict with the outcome.
    """
    reg = _reload_registry()
    entry = reg["skills"][skill_name]
    before_score, before_bd = compute_composite(
        entry, now, usage_counts, max_usage, feedback_ratings
    )

    if dry_run:
        return dict(skill=skill_name, lever=lever, status="dry_run",
                    before=before_score, after=None, delta=None,
                    breakdown_before=before_bd)

    applied = apply_fn()
    if not applied:
        return dict(skill=skill_name, lever=lever, status="skipped",
                    before=before_score, after=None, delta=None)

    # Reload registry after change
    reg = _reload_registry()
    entry = reg["skills"][skill_name]
    after_score, after_bd = compute_composite(
        entry, now, usage_counts, max_usage, feedback_ratings
    )
    delta = after_score - before_score

    if delta < 0:
        revert_fn()
        status = "reverted"
    elif delta > 0:
        # Persist composite score only when there's an actual improvement
        reg["skills"][skill_name]["composite_score"] = after_score
        reg["skills"][skill_name]["auto_score"]      = after_score
        reg["skills"][skill_name]["last_modified"]   = now.strftime("%Y-%m-%d")
        _save_registry(reg)
        status = "kept"
    else:
        # Neutral — no score change, don't write registry (avoids inflating freshness)
        status = "neutral"

    return dict(skill=skill_name, lever=lever, status=status,
                before=before_score, after=after_score, delta=delta,
                breakdown_before=before_bd, breakdown_after=after_bd)


# ── Per-lever experiment factories ────────────────────────────────────────────

def experiment_add_ref_file(
    skill_name: str, entry: dict, now, usage_counts, max_usage, feedback_ratings, dry_run
) -> Optional[dict]:
    """Extract tables/code from SKILL.md → references/quick-reference.md."""
    loc = PROJECT_ROOT / entry.get("location", "")
    if not loc.exists():
        return None
    refs_dir = loc.parent / "references"
    ref_file = refs_dir / "quick-reference.md"
    if ref_file.exists():
        return None  # already has one from this extractor
    content = build_quick_reference(skill_name, loc)
    if not content:
        return None  # nothing extractable

    def apply():
        refs_dir.mkdir(exist_ok=True)
        ref_file.write_text(content)
        # Update registry metric
        reg = _reload_registry()
        reg["skills"][skill_name]["metrics"]["reference_files"] = len(
            list(refs_dir.glob("*.md"))
        )
        _save_registry(reg)
        return True

    # Capture pre-existing reference file count for safe revert
    pre_ref_count = entry.get("metrics", {}).get("reference_files", 0)

    def revert():
        if ref_file.exists():
            ref_file.unlink()
        if refs_dir.exists() and not any(refs_dir.iterdir()):
            refs_dir.rmdir()
        reg = _reload_registry()
        reg["skills"][skill_name]["metrics"]["reference_files"] = pre_ref_count
        _save_registry(reg)

    return run_experiment(
        skill_name, "ADD_REF_FILE", apply, revert,
        now, usage_counts, max_usage, feedback_ratings, dry_run
    )


def experiment_fix_desc(
    skill_name: str, entry: dict, now, usage_counts, max_usage, feedback_ratings, dry_run
) -> Optional[dict]:
    """Fix description word count to hit the 20-60 word sweet spot."""
    loc = PROJECT_ROOT / entry.get("location", "")
    if not loc.exists():
        return None
    new_desc = fix_description(entry, loc)
    if new_desc is None:
        return None

    old_desc_words = entry.get("metrics", {}).get("description_words", 0)
    new_desc_words = len(new_desc.split())
    if new_desc_words == old_desc_words:
        return None

    def apply():
        reg = _reload_registry()
        reg["skills"][skill_name]["description"]                   = new_desc
        reg["skills"][skill_name]["metrics"]["description_words"]  = new_desc_words
        _save_registry(reg)
        return True

    def revert():
        reg = _reload_registry()
        reg["skills"][skill_name]["description"]                   = entry.get("description", "")
        reg["skills"][skill_name]["metrics"]["description_words"]  = old_desc_words
        _save_registry(reg)

    return run_experiment(
        skill_name, "FIX_DESC", apply, revert,
        now, usage_counts, max_usage, feedback_ratings, dry_run
    )


def experiment_clean_deps(
    skill_name: str, entry: dict, all_skill_names: set,
    now, usage_counts, max_usage, feedback_ratings, dry_run
) -> Optional[dict]:
    """Remove depends_on entries that point to non-existent skills."""
    old_deps   = entry.get("depends_on", [])
    clean_deps = [d for d in old_deps if d in all_skill_names]
    if clean_deps == old_deps:
        return None  # nothing broken

    def apply():
        reg = _reload_registry()
        reg["skills"][skill_name]["depends_on"] = clean_deps
        _save_registry(reg)
        return True

    def revert():
        reg = _reload_registry()
        reg["skills"][skill_name]["depends_on"] = old_deps
        _save_registry(reg)

    return run_experiment(
        skill_name, "CLEAN_DEPS", apply, revert,
        now, usage_counts, max_usage, feedback_ratings, dry_run
    )


# ── Report ────────────────────────────────────────────────────────────────────

def show_report(last_n: int = 50) -> None:
    events = _load_jsonl(AR_LOG)
    if not events:
        print("No autoresearch experiments logged yet.")
        return
    recent = events[-last_n:]
    by_status: Counter = Counter(e["status"] for e in recent)
    print(f"Last {len(recent)} experiments:")
    for s, n in by_status.most_common():
        print(f"  {s:10s}: {n}")
    print()
    kept  = [e for e in recent if e["status"] == "kept"]
    gains = sorted(kept, key=lambda e: e.get("delta", 0), reverse=True)
    if gains:
        print("Best kept experiments:")
        for e in gains[:10]:
            print(f"  +{e['delta']:2d}  {e['lever']:15s}  {e['skill']}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args      = sys.argv[1:]
    dry_run   = "--apply" not in args
    report    = "--report" in args
    n_target  = None
    domain    = None

    if report:
        show_report()
        return

    for i, a in enumerate(args):
        if a == "--n" and i + 1 < len(args):
            n_target = int(args[i + 1])
        if a == "--domain" and i + 1 < len(args):
            domain = args[i + 1]

    # Load registry and analytics
    reg   = _reload_registry()
    skills = reg["skills"]
    all_names = set(skills)

    # Skill loads only; search events (no `skill` field) are excluded.
    usage_counts: Counter = Counter(
        e["skill"] for e in _load_jsonl(USAGE_LOG) if e.get("skill")
    )
    feedback_ratings: dict = {}
    for e in _load_jsonl(FEEDBACK_LOG):
        s, r = e.get("skill", ""), e.get("rating")
        if s and r is not None:
            feedback_ratings.setdefault(s, []).append(r)
    max_usage = max(usage_counts.values()) if usage_counts else 1
    now = datetime.now(timezone.utc)

    # Build candidate list — lowest scoring first, filtered by domain
    candidates = []
    for name, entry in skills.items():
        if domain:
            tags = entry.get("tags", [])
            if not any(t == f"domain:{domain}" for t in tags):
                continue
        candidates.append((entry.get("composite_score", 0), name, entry))
    candidates.sort(key=lambda x: x[0])
    if n_target:
        candidates = candidates[:n_target]

    print(f"{'DRY RUN — ' if dry_run else ''}autoresearch loop")
    print(f"  Candidates: {len(candidates)}{f' (domain: {domain})' if domain else ''}")
    print(f"  Levers: ADD_REF_FILE, FIX_DESC, CLEAN_DEPS")
    print()

    results: list[dict] = []

    for _, skill_name, entry in candidates:
        # Refresh entry each iteration (previous experiments may have changed it)
        entry = _reload_registry()["skills"][skill_name]

        for lever_fn in [
            lambda sn=skill_name, e=entry: experiment_add_ref_file(
                sn, e, now, usage_counts, max_usage, feedback_ratings, dry_run),
            lambda sn=skill_name, e=entry: experiment_fix_desc(
                sn, e, now, usage_counts, max_usage, feedback_ratings, dry_run),
            lambda sn=skill_name, e=entry: experiment_clean_deps(
                sn, e, all_names, now, usage_counts, max_usage, feedback_ratings, dry_run),
        ]:
            result = lever_fn()
            if result is None:
                continue
            results.append(result)
            if not dry_run:
                _log_experiment(result)
            status_icon = {"kept": "✓", "reverted": "✗", "neutral": "~",
                           "dry_run": "?", "skipped": "-"}.get(result["status"], "?")
            delta_str = f"+{result['delta']}" if result.get("delta", 0) and result["delta"] > 0 \
                else (str(result.get("delta", "")) if result.get("delta") is not None else "")
            print(f"  {status_icon} {result['lever']:15s}  {delta_str:>4s}  {skill_name}")

    # Summary
    print()
    by_status: Counter = Counter(r["status"] for r in results)
    total_gain = sum(r.get("delta", 0) or 0 for r in results if r["status"] == "kept")
    print(f"Results: {len(results)} experiments")
    for s, n in by_status.most_common():
        print(f"  {s:10s}: {n}")
    if total_gain:
        print(f"  Total score gain: +{total_gain} pts across kept experiments")
    if dry_run:
        print("\nRun with --apply to commit changes.")


if __name__ == "__main__":
    main()
