#!/usr/bin/env python3
"""Append a point-in-time snapshot of every skill's scores to evolution.jsonl.

Usage:
    python3 scripts/snapshot_evolution.py [--event recalibrate|manual|hook] [--dry-run]

Each run appends one JSON line per skill with current scores, health,
word count, and connection count. This creates a time-series that the
Neural Observatory dashboard uses to visualize skill maturation over time.

SkillOpt task_score fields (task_score_test / task_score_verdict) are carried
null-safely: skills without a `task_score` object emit null for these, and
existing evolution rows that predate the fields keep working unchanged.

Safe to run repeatedly — each snapshot is timestamped and append-only.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_here = Path(__file__).resolve().parent
PROJECT_ROOT = _here.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
EVOLUTION_LOG = PROJECT_ROOT / "data" / "evolution.jsonl"


def build_record(name: str, entry: dict, now: str, event: str) -> dict:
    """One evolution row for a skill. task_score fields are null-safe."""
    metrics = entry.get("metrics", {})
    # entry.get("task_score") may be absent (most skills) -> emit nulls.
    ts = entry.get("task_score") or {}
    return {
        "skill": name,
        "date": now,
        "auto_score": entry.get("auto_score", 0),
        "composite_score": entry.get("composite_score", 0),
        "health": entry.get("health_status", "unknown"),
        "word_count": metrics.get("body_words", 0),
        "connections": len(entry.get("depends_on", []))
        + len(entry.get("referenced_by", [])),
        "reference_files": metrics.get("reference_files", 0),
        "task_score_test": ts.get("test"),        # None if no task_score
        "task_score_verdict": ts.get("verdict"),  # None if no task_score
        "event": event,
    }


def main():
    event = "manual"
    dry_run = "--dry-run" in sys.argv
    for arg in sys.argv[1:]:
        if arg.startswith("--event"):
            if "=" in arg:
                event = arg.split("=", 1)[1]
        elif not arg.startswith("-"):
            event = arg

    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    skills = reg.get("skills", {})
    now = datetime.now(timezone.utc).isoformat()
    records = [build_record(n, e, now, event) for n, e in sorted(skills.items())]

    if dry_run:
        with_ts = [r for r in records if r["task_score_verdict"] is not None]
        print(f"DRY RUN: {len(records)} records built; "
              f"{len(with_ts)} carry task_score, {len(records) - len(with_ts)} null-safe.")
        for r in with_ts:
            print(f"  {r['skill']:14s} verdict={r['task_score_verdict']} "
                  f"test={r['task_score_test']}")
        sample = next((r for r in records if r["task_score_verdict"] is None), None)
        if sample:
            print(f"  example null-safe row: {json.dumps(sample)}")
        return

    with open(EVOLUTION_LOG, "a") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    print(f"Snapshot: {len(records)} skills recorded to evolution.jsonl ({event})")


if __name__ == "__main__":
    main()
