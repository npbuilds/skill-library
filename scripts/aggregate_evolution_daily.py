#!/usr/bin/env python3
"""
aggregate_evolution_daily.py — Build the per-date evolution rollup.

The dashboards read one summary doc per active day instead of the full
`evolution` collection (~27k docs and growing), cutting a page load from ~27k
Firestore reads to ~90. `migrate_to_firestore.py` writes this collection as part
of a full migration; this script lets you (re)build just the rollup — useful for
a one-off backfill without re-pushing every other collection.

Usage:
  python3 scripts/aggregate_evolution_daily.py            # write data/evolution_daily.json
  python3 scripts/aggregate_evolution_daily.py --push     # also push to Firestore
  python3 scripts/aggregate_evolution_daily.py --push --dry-run

The aggregation logic lives in migrate_to_firestore.build_evolution_daily so the
standalone backfill and the full migration can never diverge.
"""

import argparse
import json
import sys
from pathlib import Path

from migrate_to_firestore import (
    build_evolution_daily,
    parse_jsonl,
    batch_write,
    get_db,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def main():
    parser = argparse.ArgumentParser(description="Build the evolution_daily rollup")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--push", action="store_true", help="Push to Firestore (default: local file only)")
    parser.add_argument("--dry-run", action="store_true", help="With --push, validate without writing")
    args = parser.parse_args()

    registry = json.loads((DATA / "registry.json").read_text())
    evolution = parse_jsonl(DATA / "evolution.jsonl")
    daily = build_evolution_daily(evolution, registry)

    out = DATA / "evolution_daily.json"
    out.write_text(json.dumps(daily, indent=2) + "\n")
    print(f"▸ {len(evolution)} raw rows → {len(daily)} daily docs → {out.name}")
    if daily:
        print(f"  date range: {daily[0]['date']} → {daily[-1]['date']}")

    if args.push:
        print(f"\n▸ Pushing evolution_daily to Firestore (project {args.project})...")
        db = get_db(args.project)
        batch_write(db, "evolution_daily", daily,
                    id_fn=lambda d: d["date"], dry_run=args.dry_run)
        print("  ✓ done" + (" (dry-run)" if args.dry_run else ""))
    else:
        print("\n  (local only — pass --push to write to Firestore)")


if __name__ == "__main__":
    main()
