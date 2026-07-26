#!/usr/bin/env python3
"""
usage_rollup.py — Build the committed-usage aggregate the dashboard reads.

The problem this closes
-----------------------
The Firestore `usage` collection is populated by exactly one writer: the Cloud
Run MCP server's mirror (mcp-server/firestore_telemetry.py). CI syncs Firestore
with `migrate_to_firestore.py --registry-only`, which never pushes
data/usage.jsonl. So two whole classes of skill load were invisible in the
dashboard's usage view:

  - local stdio MCP loads (`python3 mcp-server/server.py`)
  - plugin-native loads (source="plugin")

Both nonetheless feed `auto_score` via recalibrate_scores.py, which reads the
committed jsonl. Net effect: the dashboard showed scores its own usage panel
could not explain.

Why an aggregate rather than pushing raw rows
---------------------------------------------
Pushing data/usage.jsonl into the `usage` collection is an APPEND, and appends
need four invariants to hold at once to avoid double-counting (deterministic
doc IDs, a push watermark, skipping rows that carry `_fs_id` because they
originated in Firestore, and a pull-side guard so pushed rows are not re-pulled
by pull_telemetry_from_firestore.py). Any one of those failing silently
inflates both dashboard counts and scores.

This rollup is instead a FULL-SNAPSHOT OVERWRITE of a single doc — the same
idempotent pattern `meta/registry` and `evolution_daily` already use. Re-running
is a no-op by construction: no watermark to regress, no dedupe key to mismatch,
and nothing is ever written to the `usage` collection, so the pull loop's
`_fs_id` dedupe stays untouched and cannot see a duplicate.

It also makes the dashboard and the scores agree by construction: counts here
use the same "truthy skill field" filter as `iter_skill_uses`, over the same
committed file that recalibrate_scores.py reads.

The live tail (why `firestore_watermark` is in the doc)
------------------------------------------------------
Cloud events only reach git via the nightly pull → bot PR → merge, so a
git-derived rollup alone would lag cloud usage by up to ~24h. The rollup
therefore stamps data/.telemetry_watermark. The pull loop guarantees every
Firestore usage doc with timestamp <= watermark is already in the committed
jsonl, so the dashboard can read:

    rollup(committed history)  +  usage WHERE timestamp > watermark

That boundary is exact — no double count, no gap — and it replaces an unbounded
full-collection read with a bounded tail. When the watermark is absent (pull
loop never bootstrapped) the doc carries null and the dashboard skips the tail:
undercounting transiently is acceptable, double-counting is not.

Determinism
-----------
No wall-clock reads. The domain×day window is anchored on the newest event's
date, not "today", so the same input file always produces the same doc — CI can
diff it and the score-idempotency gate stays deterministic.

This module is import-only (no __main__): migrate_to_firestore.py calls
build_usage_rollup() during sync_registry().
"""

from collections import Counter
from pathlib import Path

# Newest-first cap on the per-event tail carried in the doc. Drives the 2D/3D
# "recently used" pulse (needs 15) and the learning trail (walks the whole
# list). 300 keeps the doc small while leaving the trail far longer than the
# ~136 events the library has accumulated to date; beyond that a trail through
# every event ever is visual noise anyway.
RECENT_LIMIT = 300

# Domain×day counts are kept for the newest N days that actually have events.
# Bounded on ACTIVE days, not calendar days: usage is sparse and bursty (the
# library has ~134 events spread over a handful of days), so a 60-day calendar
# window would silently drop active days the heatmap used to show. The
# dashboard renders the last 7 active days; 30 leaves headroom while keeping
# the map's cardinality bounded no matter how the log grows.
DOMAIN_DAY_ACTIVE_DAYS = 30

# Sources are open-ended on purpose: "mcp" (MCP server, cloud or local stdio)
# and "plugin" (plugin-native hook) are what exist today, but a future writer
# stamping source="cli" should surface as its own bucket rather than being
# silently relabelled "mcp".
DEFAULT_SOURCE = "mcp"


def normalize_source(row: dict) -> str:
    """Bucket one usage row by writer.

    Rows written before the `source` field existed came from the MCP server
    (the only writer at the time), so an absent/empty source means "mcp".
    Any other non-empty value passes through as its own bucket.

    Same contract as mcp-server/shared.py `event_source()`, reimplemented here
    (plus whitespace/non-string coercion) rather than imported on purpose: this
    module runs in sync-firestore.yml, which installs only
    google-cloud-firestore, so importing from mcp-server would break the sync.
    Keep the two in step — test_usage_rollup pins them against each other.
    """
    source = row.get("source")
    if isinstance(source, str) and source.strip():
        return source.strip()
    return DEFAULT_SOURCE


def _day(row: dict) -> str:
    """UTC date prefix of an ISO-8601 timestamp, or "" if unusable.

    Timestamps are stamped by server._log_event as ISO-8601 with a fixed +00:00
    offset, so the first 10 chars are the UTC date and lexicographic ordering
    is chronological.
    """
    ts = row.get("timestamp")
    return ts[:10] if isinstance(ts, str) and len(ts) >= 10 else ""


def build_skill_domain_map(registry: dict) -> dict[str, str]:
    """skill name → domain, from registry.network.domains."""
    mapping = {}
    for domain, names in registry.get("network", {}).get("domains", {}).items():
        for name in names:
            mapping[name] = domain
    return mapping


def read_watermark(path: Path) -> str | None:
    """data/.telemetry_watermark, or None if it has never been bootstrapped."""
    if not path.exists():
        return None
    return path.read_text().strip() or None


def build_usage_rollup(
    usage_rows: list[dict],
    skill_domain: dict[str, str],
    watermark: str | None = None,
    recent_limit: int = RECENT_LIMIT,
    active_days: int = DOMAIN_DAY_ACTIVE_DAYS,
) -> dict:
    """Aggregate committed usage rows into the single doc the dashboard reads.

    Only skill-load events count: rows with a truthy `skill` are kept and
    search events (type="search", no skill) are dropped. This is deliberately
    the same filter as shared.iter_skill_uses, which recalibrate_scores.py uses
    to build the usage_counts behind auto_score — so the dashboard's usage panel
    and the scores it displays are derived from one identical input.

    Returned shape (all maps keyed by name so the client needs no joins):
      event_count          total skill-load events counted
      by_source            {source: count} across all events
      totals               {skill: count} all-time, exact
      totals_by_source     {source: {skill: count}} all-time, exact
      domain_day           {"<domain>|<YYYY-MM-DD>": count} over the newest
                           `active_days` days that have events
      days                 sorted active days present in domain_day
      recent               [{skill, timestamp, source, type}] newest-first, capped
      latest_timestamp     newest event timestamp, or None
      firestore_watermark  echoed watermark; the exact live-tail boundary
      recent_limit / domain_day_active_days / recent_truncated
                           so the client can tell a capped tail from a whole one
    """
    # Must stay equivalent to shared.iter_skill_uses — pinned by
    # test_rollup_filter_is_identical_to_shared_iter_skill_uses.
    # The str guard keeps a corrupt row from aborting the whole Firestore sync:
    # a non-str skill survives Counter but raises in sorted() below, and this
    # runs before the meta/registry commit marker. The dict guard is
    # belt-and-braces — parse_jsonl already drops non-dict rows — so this stays
    # safe when handed a list built some other way.
    events = [
        r for r in usage_rows
        if isinstance(r, dict) and isinstance(r.get("skill"), str) and r["skill"]
    ]

    totals: Counter = Counter()
    by_source: Counter = Counter()
    totals_by_source: dict[str, Counter] = {}

    for row in events:
        skill = row["skill"]
        source = normalize_source(row)
        totals[skill] += 1
        by_source[source] += 1
        totals_by_source.setdefault(source, Counter())[skill] += 1

    # Newest-first ordering, matching the dashboard's old
    # `orderBy('timestamp','desc')`. Rows with no usable timestamp sort last.
    ordered = sorted(events, key=lambda r: r.get("timestamp") or "", reverse=True)
    latest_timestamp = ordered[0].get("timestamp") if ordered else None

    # `type` is carried because the infra page's activity feed renders it
    # ("Used via <type>"); session_id is deliberately NOT carried — the rollup
    # is public dashboard data and per-event session IDs add nothing to it.
    recent = [
        {
            "skill": r["skill"],
            "timestamp": r.get("timestamp"),
            "source": normalize_source(r),
            "type": r.get("type"),
        }
        for r in ordered[:recent_limit]
    ]

    # Domain×day over the newest `active_days` days that have events. Derived
    # from the data itself rather than from "today", so the doc stays a pure
    # function of its input. Events whose skill has no domain are skipped —
    # same as the dashboard's old `if (!d) continue`.
    kept_days = sorted({d for d in (_day(r) for r in events) if d})[-active_days:]
    kept = set(kept_days)
    domain_day: Counter = Counter()
    for row in events:
        day = _day(row)
        if day not in kept:
            continue
        domain = skill_domain.get(row["skill"])
        if not domain:
            continue
        domain_day[f"{domain}|{day}"] += 1

    return {
        "event_count": len(events),
        "by_source": dict(sorted(by_source.items())),
        "totals": dict(sorted(totals.items())),
        "totals_by_source": {
            source: dict(sorted(counts.items()))
            for source, counts in sorted(totals_by_source.items())
        },
        "domain_day": dict(sorted(domain_day.items())),
        "days": sorted({key.split("|", 1)[1] for key in domain_day}),
        "recent": recent,
        "recent_limit": recent_limit,
        "recent_truncated": len(ordered) > recent_limit,
        "domain_day_active_days": active_days,
        "latest_timestamp": latest_timestamp,
        "firestore_watermark": watermark,
        "source_file": "data/usage.jsonl",
    }
