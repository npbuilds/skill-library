#!/usr/bin/env python3
"""Append a point-in-time snapshot of every skill's scores to evolution.jsonl.

Usage:
    python3 scripts/snapshot_evolution.py [--event recalibrate|manual|hook]

Each run appends one JSON line per skill with current scores, health,
word count, and connection count. This creates a time-series that the
Neural Observatory dashboard uses to visualize skill maturation over time.

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


def main():
    event = "manual"
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
    count = 0

    with open(EVOLUTION_LOG, "a") as f:
        for name, entry in sorted(skills.items()):
            metrics = entry.get("metrics", {})
            record = {
                "skill": name,
                "date": now,
                "auto_score": entry.get("auto_score", 0),
                "composite_score": entry.get("composite_score", 0),
                "health": entry.get("health_status", "unknown"),
                "word_count": metrics.get("body_words", 0),
                "connections": len(entry.get("depends_on", []))
                + len(entry.get("referenced_by", [])),
                "reference_files": metrics.get("reference_files", 0),
                "event": event,
            }
            f.write(json.dumps(record) + "\n")
            count += 1

    print(f"Snapshot: {count} skills recorded to evolution.jsonl ({event})")


if __name__ == "__main__":
    main()
