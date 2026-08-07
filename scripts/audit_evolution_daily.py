#!/usr/bin/env python3
"""Audit and optionally repair aggregate evolution while raw history exists.

By default this performs a semantic comparison: legacy raw rows are deduplicated
to the newest row per skill/date and compared with ``evolution_daily``. ``--push``
repairs only raw-backed dates and writes a local backup first. It never deletes
new aggregate-only dates. After the raw collection is retired, use
``--schema-only`` for the ongoing lightweight audit.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from check_firestore_divergence import git, strict_sync_error
from evolution_daily import build_historical_aggregates, validate_daily_document
from migrate_to_firestore import get_db


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DEFAULT_BACKUP_DIR = ROOT / "output" / "infra-backups"
RAW_EVOLUTION_SAFETY_FLOOR = 1_000
BATCH_LIMIT = 400


def read_collection(db, name: str) -> dict[str, dict]:
    return {
        snapshot.id: snapshot.to_dict()
        for snapshot in db.collection(name).stream()
    }


def audit_documents(documents: dict[str, dict]) -> list[str]:
    if not documents:
        return ["evolution_daily: collection is empty"]
    errors: list[str] = []
    for doc_id, document in sorted(documents.items()):
        errors.extend(validate_daily_document(doc_id, document))
    return errors


def plan_repairs(
    computed_documents: list[dict], existing_documents: dict[str, dict]
) -> list[dict]:
    """Return missing/changed raw-backed dates; preserve newer aggregate-only dates."""
    repairs: list[dict] = []
    for document in computed_documents:
        doc_id = document["date"]
        current = existing_documents.get(doc_id)
        comparable = None if current is None else {
            "date": current.get("date"),
            "count": current.get("count"),
            "domains": current.get("domains", {}),
        }
        if comparable != document:
            repairs.append(document)
    return repairs


def write_backup(
    backup_dir: Path,
    project: str,
    raw_count: int,
    repairs: list[dict],
    existing_documents: dict[str, dict],
) -> Path:
    """Back up the exact pre-write state of every daily document to be repaired."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = backup_dir / f"evolution-daily-{project}-{timestamp}.json"
    repair_ids = [document["date"] for document in repairs]
    payload = {
        "project": project,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "raw_evolution_count": raw_count,
        "repair_ids": repair_ids,
        "before": {doc_id: existing_documents.get(doc_id) for doc_id in repair_ids},
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def apply_repairs(db, repairs: list[dict]) -> None:
    for offset in range(0, len(repairs), BATCH_LIMIT):
        batch = db.batch()
        for document in repairs[offset:offset + BATCH_LIMIT]:
            ref = db.collection("evolution_daily").document(document["date"])
            batch.set(ref, document)
        batch.commit()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit/repair Firestore evolution_daily from deduplicated raw history"
    )
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Validate stored document shapes without reading retired raw history",
    )
    parser.add_argument("--push", action="store_true", help="Apply semantic repairs")
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=DEFAULT_BACKUP_DIR,
        help="Directory for the pre-write daily-document backup",
    )
    args = parser.parse_args()
    if args.schema_only and args.push:
        parser.error("--schema-only conflicts with --push")

    db = get_db(args.project)
    documents = read_collection(db, "evolution_daily")
    errors = audit_documents(documents)
    if errors:
        print(f"✗ evolution_daily: {len(errors)} validation error(s)")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    dates = sorted(documents)
    samples = sum(document.get("count", 0) for document in documents.values())
    span = f"{dates[0]} → {dates[-1]}" if dates else "empty"
    print(f"✓ schema: {len(documents)} valid daily aggregates ({span})")
    print(f"  aggregate skill samples represented: {samples}")
    if args.schema_only:
        return

    if args.push:
        head = git("rev-parse", "HEAD")
        registry_snapshot = db.collection("meta").document("registry").get()
        synced_sha = (
            (registry_snapshot.to_dict() or {}).get("synced_sha")
            if registry_snapshot.exists
            else None
        )
        sync_error = strict_sync_error(head, synced_sha)
        if sync_error:
            print(f"✗ refusing repair from an unsynced checkout: {sync_error}")
            raise SystemExit(1)

    print("▸ Reading raw evolution for pre-deletion semantic audit...")
    raw_documents = read_collection(db, "evolution")
    if len(raw_documents) < RAW_EVOLUTION_SAFETY_FLOOR:
        print(
            f"✗ refusing semantic audit: only {len(raw_documents)} raw documents "
            f"(safety floor {RAW_EVOLUTION_SAFETY_FLOOR}); use --schema-only after deletion"
        )
        raise SystemExit(1)

    registry = json.loads((DATA / "registry.json").read_text())
    computed = build_historical_aggregates(list(raw_documents.values()), registry)
    repairs = plan_repairs(computed, documents)
    unique_samples = sum(document["count"] for document in computed)
    print(f"  raw documents: {len(raw_documents)}")
    print(f"  unique skill/date samples: {unique_samples}")
    print(f"  raw-backed daily aggregates: {len(computed)}")
    print(f"  repairs required: {len(repairs)}")
    for document in repairs:
        old_count = (documents.get(document["date"]) or {}).get("count", "missing")
        print(f"    {document['date']}: count {old_count} → {document['count']}")

    if not repairs:
        print("✓ semantic audit: every raw-backed date matches one-sample-per-skill history")
        return
    if not args.push:
        print("✗ semantic audit failed; dry run only — re-run with --push after review")
        raise SystemExit(1)

    backup = write_backup(
        args.backup_dir, args.project, len(raw_documents), repairs, documents
    )
    print(f"  backup: {backup}")
    apply_repairs(db, repairs)

    verified = read_collection(db, "evolution_daily")
    remaining = plan_repairs(computed, verified)
    if remaining:
        print(f"✗ verification failed: {len(remaining)} repair(s) still required")
        raise SystemExit(1)
    print(f"✓ repaired and verified {len(repairs)} historical daily aggregates")


if __name__ == "__main__":
    main()
