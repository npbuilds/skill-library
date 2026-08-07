#!/usr/bin/env python3
"""
snapshot_to_firestore.py — Write one daily evolution aggregate to Firestore.

The dashboard only consumes domain-level score history, so this job derives one
`evolution_daily/{YYYY-MM-DD}` document directly from the registry. It does not
write per-skill rows or read the retired raw `evolution` collection.

Intended runner: a scheduled GitHub Action authenticated to GCP via Workload
Identity Federation (see .github/workflows/daily-firestore.yml) — NOT the public Cloud
Run service, so its runtime service account stays least-privilege.

Usage:
  python3 scripts/snapshot_to_firestore.py [--project P] [--dry-run]
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from evolution_daily import build_daily_aggregate
from migrate_to_firestore import get_db

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def main():
    parser = argparse.ArgumentParser(description="Write a daily evolution aggregate to Firestore")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--dry-run", action="store_true", help="Build and print, without writing")
    args = parser.parse_args()

    registry = json.loads((DATA / "registry.json").read_text())
    day = datetime.now(timezone.utc).date().isoformat()
    daily = build_daily_aggregate(registry, day)
    print(f"▸ Built aggregate for {day}: {daily['count']} skills, "
          f"{len(daily['domains'])} domains")

    if args.dry_run:
        print(f"  DRY RUN — would overwrite `evolution_daily/{day}` with:")
        print(f"  {json.dumps(daily, sort_keys=True)}")
        return

    db = get_db(args.project)
    db.collection("evolution_daily").document(day).set(daily)
    print(f"  ✓ evolution_daily/{day}: count={daily['count']}, "
          f"{len(daily['domains'])} domains")


if __name__ == "__main__":
    main()
