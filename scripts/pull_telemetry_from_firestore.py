#!/usr/bin/env python3
"""
pull_telemetry_from_firestore.py — Export cloud telemetry into git jsonl.

Phase 3 of the split-brain fix. The Cloud Run MCP server mirrors usage/gap/
feedback events to Firestore (firestore_telemetry.py — local jsonl there is
ephemeral). This script pulls those events back into the committed jsonl files
that recalibrate_scores.py reads, closing the loop:

    cloud usage → Firestore → (this script, daily bot PR) → git jsonl
    → recalibrate_scores.py → skills scores → deploy + firestore sync

recalibrate deliberately does NOT read Firestore directly: CI's idempotency
gate re-runs it --dry-run with no GCP auth (including fork PRs) and must stay
deterministic on committed files.

Dedupe strategy — watermark, NOT content hashing:
  Records round-tripped through Firestore don't come back byte-identical
  (datetime coercion, float formatting, field order), so hashing "canonical
  JSON" would silently mismatch and duplicate every event nightly. Instead:
  - data/.telemetry_watermark (committed) holds the last-pulled ISO timestamp;
    only events with timestamp > watermark are considered. First run
    bootstraps the watermark to "now" and pulls nothing (grandfathers all
    pre-existing docs — legacy auto-ID docs originated from local jsonl and
    are already there).
  - Each pulled row is appended with "_fs_id" (the Firestore doc ID,
    "{session_id}_{timestamp}_{seq}") as a secondary guard: a row whose _fs_id
    is already in the local file is never appended twice, even if the
    watermark regresses (e.g. a reverted commit).
  Timestamps are ISO-8601 UTC strings with a fixed +00:00 offset (stamped by
  server._log_event), so lexicographic comparison is chronological.

Score-pollution guard:
  The Cloud Run endpoint is public/unauthenticated; bot traffic writing usage
  events would inflate skill scores once pulled. Usage events are capped per
  (session_id, UTC day) — default 50 — and everything dropped is logged.
  Proper endpoint auth is the future hardening; this bounds the damage.

Git-bloat escape hatch: telemetry volume is trivial today (~150 lines total).
If it ever grows, rotate pulled history monthly into data/archive/ — the
watermark makes rotation safe.

Usage:
  python3 scripts/pull_telemetry_from_firestore.py [--project skill-library-prod]
      [--dry-run] [--session-daily-cap 50]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_to_firestore import get_db, parse_jsonl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WATERMARK_PATH = DATA / ".telemetry_watermark"

COLLECTIONS = {
    "usage": DATA / "usage.jsonl",
    "gaps": DATA / "gaps.jsonl",
    "feedback": DATA / "feedback.jsonl",
}


def read_watermark() -> str | None:
    if WATERMARK_PATH.exists():
        return WATERMARK_PATH.read_text().strip() or None
    return None


def write_watermark(value: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  (dry-run) watermark → {value}")
        return
    WATERMARK_PATH.write_text(value + "\n")
    print(f"  watermark → {value}")


def fetch_new_events(db, collection: str, watermark: str) -> list[tuple[str, dict]]:
    """Return [(doc_id, record)] with record timestamp > watermark, ascending."""
    query = (
        db.collection(collection)
        .where("timestamp", ">", watermark)
        .order_by("timestamp")
    )
    return [(snap.id, snap.to_dict()) for snap in query.stream()]


def cap_usage_events(
    events: list[tuple[str, dict]], cap: int
) -> tuple[list[tuple[str, dict]], int]:
    """Cap usage events per (session_id, UTC day). Returns (kept, dropped_count)."""
    counts: dict[tuple, int] = {}
    kept, dropped = [], 0
    for doc_id, record in events:
        key = (record.get("session_id", "?"), str(record.get("timestamp", ""))[:10])
        counts[key] = counts.get(key, 0) + 1
        if counts[key] > cap:
            dropped += 1
        else:
            kept.append((doc_id, record))
    return kept, dropped


def append_events(path: Path, events: list[tuple[str, dict]], dry_run: bool) -> int:
    """Append events not already present (by _fs_id). Returns appended count."""
    existing_ids = {
        row["_fs_id"] for row in parse_jsonl(path) if row.get("_fs_id")
    }
    fresh = [(i, r) for i, r in events if i not in existing_ids]
    if dry_run or not fresh:
        return len(fresh)
    with open(path, "a") as f:
        for doc_id, record in fresh:
            f.write(json.dumps({**record, "_fs_id": doc_id}, sort_keys=True) + "\n")
    return len(fresh)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull cloud telemetry from Firestore into git jsonl")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    parser.add_argument("--dry-run", action="store_true", help="Report without writing")
    parser.add_argument("--session-daily-cap", type=int, default=50,
                        help="Max usage events kept per session_id per UTC day")
    args = parser.parse_args()

    db = get_db(args.project)
    watermark = read_watermark()

    if watermark is None:
        # Bootstrap: grandfather everything currently in Firestore. Pre-Phase-2
        # docs are auto-ID pushes FROM local jsonl (already in git); starting
        # the watermark at the newest existing event pulls nothing today and
        # everything new tomorrow.
        newest = ""
        for collection in COLLECTIONS:
            docs = list(
                db.collection(collection)
                .order_by("timestamp", direction="DESCENDING")
                .limit(1)
                .stream()
            )
            if docs:
                ts = str((docs[0].to_dict() or {}).get("timestamp", ""))
                newest = max(newest, ts)
        if not newest:
            print("  No telemetry in Firestore yet; nothing to bootstrap.")
            return
        print(f"  Bootstrapping watermark (grandfathering all existing docs).")
        write_watermark(newest, args.dry_run)
        return

    print(f"  watermark: {watermark}")
    newest_seen = watermark
    total_appended = 0

    for collection, path in COLLECTIONS.items():
        events = fetch_new_events(db, collection, watermark)
        if events:
            newest_seen = max(newest_seen, max(str(r.get("timestamp", "")) for _, r in events))
        if collection == "usage":
            events, dropped = cap_usage_events(events, args.session_daily_cap)
            if dropped:
                print(f"  ⚠ usage: dropped {dropped} events over the "
                      f"{args.session_daily_cap}/session/day cap (bot-traffic guard)")
        appended = append_events(path, events, args.dry_run)
        total_appended += appended
        print(f"  {collection}: {len(events)} new since watermark, "
              f"{appended} appended{' (dry-run)' if args.dry_run else ''}")

    if newest_seen > watermark:
        write_watermark(newest_seen, args.dry_run)

    print(f"\n  {'Would append' if args.dry_run else 'Appended'} {total_appended} events total.")


if __name__ == "__main__":
    main()
