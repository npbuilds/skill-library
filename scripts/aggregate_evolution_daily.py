#!/usr/bin/env python3
"""Audit and repair Firestore's evolution_daily rollup from raw evolution docs.

Git no longer stores data/evolution.jsonl. The raw Firestore `evolution`
collection is therefore the recovery source of truth. By default this command
only prints an exact repair plan. Writes require --push; stale rollup deletion
additionally requires --prune. A JSON backup of every touched document is
created before any production write.

Usage:
  python3 scripts/aggregate_evolution_daily.py
  python3 scripts/aggregate_evolution_daily.py --project skill-library-prod
  python3 scripts/aggregate_evolution_daily.py --push --prune
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from migrate_to_firestore import build_evolution_daily, get_db


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DEFAULT_BACKUP_DIR = ROOT / "output" / "infra-backups"
RAW_EVOLUTION_SAFETY_FLOOR = 1_000
BATCH_LIMIT = 400


def read_collection(db, name: str) -> dict[str, dict]:
    """Read a Firestore collection into {document_id: document_data}."""
    result = {}
    for snapshot in db.collection(name).stream():
        result[snapshot.id] = snapshot.to_dict()
    return result


def plan_repair(
    computed_docs: list[dict], existing_docs: dict[str, dict]
) -> tuple[list[dict], list[str]]:
    """Return changed/missing upserts and stale document IDs."""
    target = {doc["date"]: doc for doc in computed_docs}
    upserts = []
    for doc_id, doc in sorted(target.items()):
        current = existing_docs.get(doc_id)
        comparable = None if current is None else {
            "date": current.get("date"),
            "count": current.get("count"),
            "domains": current.get("domains", {}),
        }
        if comparable != doc:
            upserts.append(doc)
    stale = sorted(set(existing_docs) - set(target))
    return upserts, stale


def write_backup(
    backup_dir: Path,
    project: str,
    raw_count: int,
    upserts: list[dict],
    stale: list[str],
    existing: dict[str, dict],
) -> Path:
    """Persist the exact pre-write state for every touched rollup document."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = backup_dir / f"evolution-daily-{project}-{timestamp}.json"
    touched = sorted({doc["date"] for doc in upserts} | set(stale))
    payload = {
        "project": project,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "raw_evolution_count": raw_count,
        "upsert_ids": [doc["date"] for doc in upserts],
        "delete_ids": stale,
        "before": {doc_id: existing.get(doc_id) for doc_id in touched},
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def apply_repair(db, upserts: list[dict], stale: list[str]) -> None:
    """Apply an exact repair in bounded Firestore batches."""
    operations = [
        ("set", doc["date"], doc) for doc in upserts
    ] + [
        ("delete", doc_id, None) for doc_id in stale
    ]
    for offset in range(0, len(operations), BATCH_LIMIT):
        batch = db.batch()
        for operation, doc_id, doc in operations[offset:offset + BATCH_LIMIT]:
            ref = db.collection("evolution_daily").document(doc_id)
            if operation == "set":
                batch.set(ref, doc)
            else:
                batch.delete(ref)
        batch.commit()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit/repair evolution_daily from Firestore evolution"
    )
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--push", action="store_true", help="Apply the repair plan")
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Allow deletion of stale evolution_daily docs (requires --push)",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=DEFAULT_BACKUP_DIR,
        help="Directory for the pre-write JSON backup",
    )
    args = parser.parse_args()
    if args.prune and not args.push:
        parser.error("--prune requires --push")

    registry = json.loads((DATA / "registry.json").read_text())
    db = get_db(args.project)
    print("▸ Reading Firestore evolution source of truth...")
    raw_by_id = read_collection(db, "evolution")
    existing = read_collection(db, "evolution_daily")
    raw = list(raw_by_id.values())

    if len(raw) < RAW_EVOLUTION_SAFETY_FLOOR:
        print(
            f"  ✗ REFUSING repair: only {len(raw)} raw evolution docs "
            f"(safety floor {RAW_EVOLUTION_SAFETY_FLOOR})",
            file=sys.stderr,
        )
        raise SystemExit(1)

    computed = build_evolution_daily(raw, registry)
    upserts, stale = plan_repair(computed, existing)
    raw_total = len(raw_by_id)
    rollup_total = sum(doc["count"] for doc in computed)

    print(f"  raw evolution docs: {raw_total}")
    print(f"  computed daily docs: {len(computed)} (count sum: {rollup_total})")
    print(f"  existing daily docs: {len(existing)}")
    print(f"  upserts required: {len(upserts)}")
    for doc in upserts:
        previous = existing.get(doc["date"])
        old_count = previous.get("count") if previous else "missing"
        print(f"    {doc['date']}: {old_count} → {doc['count']}")
    print(f"  stale docs: {len(stale)}")
    for doc_id in stale:
        print(f"    {doc_id}: delete")

    if raw_total != rollup_total:
        print(
            f"  ✗ REFUSING repair: raw count {raw_total} != rollup sum {rollup_total}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if not upserts and not stale:
        print("  ✓ evolution_daily already matches raw evolution")
        return
    if not args.push:
        print("\n  DRY RUN — no writes. Re-run with --push --prune after review.")
        return
    if stale and not args.prune:
        print(
            "\n  ✗ REFUSING partial repair: stale docs exist; review the plan and "
            "re-run with --push --prune.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    backup = write_backup(
        args.backup_dir, args.project, raw_total, upserts, stale, existing
    )
    print(f"\n  backup: {backup}")
    apply_repair(db, upserts, stale)

    verified = read_collection(db, "evolution_daily")
    verify_upserts, verify_stale = plan_repair(computed, verified)
    if verify_upserts or verify_stale:
        print(
            f"  ✗ verification failed: {len(verify_upserts)} mismatches, "
            f"{len(verify_stale)} stale docs",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(
        f"  ✓ repaired and verified: {len(verified)} daily docs, "
        f"count sum {sum(doc.get('count', 0) for doc in verified.values())}"
    )


if __name__ == "__main__":
    main()
