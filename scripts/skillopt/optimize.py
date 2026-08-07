#!/usr/bin/env python3
"""optimize.py — validation-gated, text-space skill optimizer (SkillOpt pilot).

Mirrors scripts/autoresearch.py's propose -> apply -> score -> keep/revert -> log
loop, but the score is a *rollout-based held-out task_score* (the val split)
instead of the heuristic composite_score.

Loop per step:
  1. propose ONE bounded edit informed by the lowest-scoring train rollouts
     (and the persisted rejected-edit buffer, so we don't repeat mistakes)
  2. apply within the textual learning-rate budget
  3. re-run the frozen val split
  4. accept only if val task_score STRICTLY improves; else revert + buffer it
Accepted edits bump metadata.version and add a registry changelog entry. A final
slow/meta pass consolidates the document.

Usage:
    python3 scripts/skillopt/optimize.py                 # run (mock LLM by default)
    python3 scripts/skillopt/optimize.py --epochs 2
    python3 scripts/skillopt/optimize.py --dry-run       # don't write SKILL.md/registry
    python3 scripts/skillopt/optimize.py --reset         # restore baseline, clear logs
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
from common import (  # noqa: E402
    SKILL_NAME, SKILL_PATH, BASELINE_SNAPSHOT, OPTIMIZED_SNAPSHOT,
    LOG_PATH, REJECTED_PATH,
    read_skill_body, write_skill_body, append_jsonl, load_jsonl,
    load_registry, save_registry, ensure_dirs, now_iso, today,
)
from edits import apply_edit, within_budget, edit_size, get_proposer, Edit  # noqa: E402
from llm import get_solver_client  # noqa: E402
from runner import score_skill, score_by_type  # noqa: E402
from tasks import tasks_for_split  # noqa: E402

# Safety cap so an LLM proposer that keeps inventing novel edit ids can't loop
# unbounded when the val score is already at ceiling.
MAX_PROPOSALS_PER_EPOCH = 12


# ── Provenance helpers ─────────────────────────────────────────────────────────

def _bump_semver(v: str) -> str:
    parts = re.findall(r"\d+", v)
    while len(parts) < 3:
        parts.append("0")
    major, minor, patch = (int(parts[0]), int(parts[1]), int(parts[2]))
    return f"{major}.{minor}.{patch + 1}"


def bump_version_and_changelog(note: str, val_after: float) -> str | None:
    """Bump the registry version + changelog and mirror version into SKILL.md.

    Registry is the source of truth (CLAUDE.md). Returns the new version.
    """
    reg = load_registry()
    entry = reg["skills"].get(SKILL_NAME)
    if entry is None:
        return None
    new_version = _bump_semver(entry.get("version", "1.0.0"))
    entry["version"] = new_version
    entry["last_modified"] = today()
    entry.setdefault("changelog", []).append({
        "date": today(),
        "action": "skillopt",
        "note": note,
        "val_task_score": val_after,
    })
    save_registry(reg)
    _mirror_frontmatter_version(new_version)
    return new_version


def _mirror_frontmatter_version(version: str) -> None:
    text = SKILL_PATH.read_text()
    fm, body = common.split_frontmatter(text)
    if not fm:
        return
    new_fm, n = re.subn(r'(version:\s*)"[^"]*"', rf'\g<1>"{version}"', fm, count=1)
    if n:
        SKILL_PATH.write_text(new_fm + body)


# ── Reset ──────────────────────────────────────────────────────────────────────

def reset() -> None:
    if BASELINE_SNAPSHOT.exists():
        write_skill_body(BASELINE_SNAPSHOT.read_text())
        # restore frontmatter version too
        _mirror_frontmatter_version("1.0")
        print(f"Restored SKILL.md body from {BASELINE_SNAPSHOT}")
    for p in (LOG_PATH, REJECTED_PATH, OPTIMIZED_SNAPSHOT):
        if p.exists():
            p.unlink()
            print(f"Removed {p}")
    print("Note: registry version/changelog edits are not auto-reverted; review with git if needed.")


# ── Meta / consolidation pass ───────────────────────────────────────────────────

def consolidate(body: str) -> str:
    """Slow pass: dedupe identical added recipe blocks and tidy whitespace."""
    # Collapse 3+ blank lines into 2.
    out = re.sub(r"\n{3,}", "\n\n", body)
    # Dedupe identical '#### Recipe — ...' blocks (keep first).
    seen: set[str] = set()
    blocks = re.split(r"(?=#### Recipe — )", out)
    kept = []
    for b in blocks:
        key = b.strip()[:60]
        if key.startswith("#### Recipe —") and key in seen:
            continue
        if key.startswith("#### Recipe —"):
            seen.add(key)
        kept.append(b)
    return "".join(kept)


# ── Main optimization loop ───────────────────────────────────────────────────────

def worst_type_order(train_results: list[dict]) -> list[str]:
    by_type = score_by_type(train_results)
    # ascending pass-rate (worst first); break ties by name for determinism
    return [t for t, _ in sorted(by_type.items(), key=lambda kv: (kv[1][0] / kv[1][1], kv[0]))]


def optimize(epochs: int = 2, dry_run: bool = False) -> None:
    ensure_dirs()
    client = get_solver_client()
    proposer = get_proposer(client)
    print(f"Rollout backend: {client.name} | proposer: {proposer.name} | dry_run={dry_run}\n")

    # Snapshot the true original body once, so baselines stay meaningful across reruns.
    if not BASELINE_SNAPSHOT.exists() and not dry_run:
        BASELINE_SNAPSHOT.write_text(read_skill_body())
        print(f"Saved baseline snapshot -> {BASELINE_SNAPSHOT}")

    train_tasks = tasks_for_split("train")
    val_tasks = tasks_for_split("val")

    working_body = read_skill_body()
    best_val, _ = score_skill(working_body, val_tasks, client)
    start_val = best_val
    print(f"Starting val task_score: {best_val:.2f}\n")

    rejected_ids = {r["edit"]["id"] for r in load_jsonl(REJECTED_PATH) if r.get("edit")}
    applied_ids: set[str] = set()
    accepted, rejected = 0, 0

    for epoch in range(1, epochs + 1):
        print(f"── Epoch {epoch}/{epochs} ──")
        made_progress = False
        proposals_this_epoch = 0
        while True:
            if proposals_this_epoch >= MAX_PROPOSALS_PER_EPOCH:
                print(f"  (reached proposal cap {MAX_PROPOSALS_PER_EPOCH} for this epoch)")
                break
            train_score, train_results = score_skill(working_body, train_tasks, client)
            order = worst_type_order(train_results)
            edit = proposer.propose(working_body, order, rejected_ids, applied_ids)
            if edit is None:
                break
            proposals_this_epoch += 1

            # Learning-rate budget gate.
            if not within_budget(edit):
                chars, lines = edit_size(edit)
                rejected_ids.add(edit.id)
                rec = {"timestamp": now_iso(), "edit": edit.summary(),
                       "reason": f"over budget ({chars} chars / {lines} lines)"}
                if not dry_run:
                    append_jsonl(REJECTED_PATH, rec)
                _log({"status": "rejected_budget", "edit": edit.summary(),
                      "val_before": best_val, "val_after": best_val, "delta": 0.0,
                      "epoch": epoch}, dry_run)
                print(f"  ✗ budget   {edit.id}")
                rejected += 1
                continue

            candidate = apply_edit(working_body, edit)
            if candidate is None:
                rejected_ids.add(edit.id)
                print(f"  - skip     {edit.id} (anchor not found)")
                continue

            new_val, _ = score_skill(candidate, val_tasks, client)
            delta = round(new_val - best_val, 4)

            if delta > 0:  # strict improvement required
                working_body = candidate
                best_val = new_val
                applied_ids.add(edit.id)
                accepted += 1
                made_progress = True
                version = None
                if not dry_run:
                    write_skill_body(working_body)
                    version = bump_version_and_changelog(
                        note=f"Added '{edit.id}' ({edit.target}); val {start_val:.1f}->{new_val:.1f}",
                        val_after=new_val,
                    )
                _log({"status": "accepted", "edit": edit.summary(), "version": version,
                      "val_before": round(best_val - delta, 2), "val_after": new_val,
                      "delta": delta, "train_score": train_score, "epoch": epoch}, dry_run)
                print(f"  ✓ accept   {edit.id:28s} val {best_val - delta:.1f} -> {new_val:.1f}  (+{delta})")
            else:
                rejected_ids.add(edit.id)
                rejected += 1
                rec = {"timestamp": now_iso(), "edit": edit.summary(),
                       "reason": "no strict val improvement", "delta": delta}
                if not dry_run:
                    append_jsonl(REJECTED_PATH, rec)
                _log({"status": "rejected", "edit": edit.summary(),
                      "val_before": best_val, "val_after": new_val, "delta": delta,
                      "epoch": epoch}, dry_run)
                print(f"  ✗ reject   {edit.id:28s} val {best_val:.1f} -> {new_val:.1f}  ({delta})")
        if not made_progress:
            print("  (no further accepted edits this epoch)")
        print()

    # Slow / meta consolidation pass — must not reduce val.
    consolidated = consolidate(working_body)
    if consolidated != working_body:
        meta_val, _ = score_skill(consolidated, val_tasks, client)
        meta_delta = round(meta_val - best_val, 4)
        if meta_val >= best_val:
            working_body = consolidated
            best_val = meta_val
            if not dry_run:
                write_skill_body(working_body)
            _log({"status": "meta_consolidation", "val_after": meta_val,
                  "delta": meta_delta}, dry_run)
            print(f"Meta consolidation pass kept (val={meta_val:.2f}).\n")
        else:
            print(f"Meta consolidation pass rejected (val would drop to {meta_val:.2f}).\n")

    if not dry_run:
        OPTIMIZED_SNAPSHOT.write_text(working_body)

    print(f"Done. accepted={accepted} rejected={rejected}")
    print(f"val task_score: {start_val:.2f} -> {best_val:.2f}  (+{best_val - start_val:.2f})")
    if dry_run:
        print("\n(dry-run: SKILL.md / registry / logs were not written)")


def _log(record: dict, dry_run: bool) -> None:
    record = {"timestamp": now_iso(), "skill": SKILL_NAME, **record}
    if not dry_run:
        append_jsonl(LOG_PATH, record)


def main() -> None:
    args = sys.argv[1:]
    if "--reset" in args:
        reset()
        return
    epochs = 2
    if "--epochs" in args:
        epochs = int(args[args.index("--epochs") + 1])
    optimize(epochs=epochs, dry_run="--dry-run" in args)


if __name__ == "__main__":
    main()
