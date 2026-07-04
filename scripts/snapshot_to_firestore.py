#!/usr/bin/env python3
"""
snapshot_to_firestore.py — Write a daily evolution snapshot straight to Firestore.

Phase 1 of the git-bloat remediation: evolution's read path is already Firestore
(`evolution` + `evolution_daily`), so committing `data/evolution.jsonl` to git on
every snapshot was redundant persistence — and the dominant driver of repo bloat.
This job replaces the append-to-jsonl-and-commit flow: it builds today's per-skill
rows from the registry and writes them directly to Firestore, then refreshes
today's `evolution_daily` rollup.

Intended runner: a scheduled GitHub Action authenticated to GCP via Workload
Identity Federation (see .github/workflows/snapshot.yml) — NOT the public Cloud
Run service, so its runtime service account stays least-privilege.

Usage:
  python3 scripts/snapshot_to_firestore.py [--event scheduled] [--project P] [--dry-run]

Reuses the exact row builder (snapshot_evolution.build_record), doc-ID scheme
(migrate_to_firestore.evo_id), and rollup logic (build_evolution_daily) so the
Firestore contents are identical to what the old jsonl→migrate path produced.
"""

import argparse
import json
from datetime import datetime, timezone, date, timedelta
from pathlib import Path

from snapshot_evolution import build_record
from migrate_to_firestore import (
    evo_id,
    build_evolution_daily,
    batch_write,
    get_db,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def _todays_daily_doc(db, registry: dict, day: str) -> dict | None:
    """Recompute one `evolution_daily` doc for `day` (YYYY-MM-DD) from all of that
    day's rows currently in Firestore — idempotent and correct even if more than
    one event wrote today. `date` is a full ISO timestamp, so a lexical
    [day, day+1) range selects exactly today's rows (a single-field index)."""
    nxt = (date.fromisoformat(day) + timedelta(days=1)).isoformat()
    q = (
        db.collection("evolution")
        .where("date", ">=", day)
        .where("date", "<", nxt)
    )
    rows = [d.to_dict() for d in q.stream()]
    dailies = build_evolution_daily(rows, registry)
    # build_evolution_daily groups by date[:10]; for a single day it returns 0 or 1 doc.
    return next((d for d in dailies if d["date"] == day), None)


def main():
    parser = argparse.ArgumentParser(description="Write a daily evolution snapshot to Firestore")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--event", default="scheduled", help="Event label for the snapshot rows")
    parser.add_argument("--dry-run", action="store_true", help="Build rows and print, without writing")
    args = parser.parse_args()

    registry = json.loads((DATA / "registry.json").read_text())
    skills = registry.get("skills", {})
    now = datetime.now(timezone.utc).isoformat()
    day = now[:10]
    rows = [build_record(n, e, now, args.event) for n, e in sorted(skills.items())]
    print(f"▸ Built {len(rows)} snapshot rows for {day} (event={args.event})")

    if args.dry_run:
        print(f"  DRY RUN — would write {len(rows)} rows to `evolution` and refresh "
              f"`evolution_daily/{day}`. Sample: {json.dumps(rows[0])}")
        return

    db = get_db(args.project)
    batch_write(db, "evolution", rows, id_fn=evo_id)

    daily = _todays_daily_doc(db, registry, day)
    if daily:
        batch_write(db, "evolution_daily", [daily], id_fn=lambda d: d["date"])
        print(f"  ✓ evolution_daily/{day}: count={daily['count']}, "
              f"{len(daily['domains'])} domains")
    else:
        print(f"  ⚠ no rows found for {day} when recomputing the daily rollup")


if __name__ == "__main__":
    main()
