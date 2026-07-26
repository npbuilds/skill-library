#!/usr/bin/env python3
"""
test_usage_rollup.py — Tests for the dashboard usage rollup.

Covers the properties the rollup exists to guarantee:
  - counts match recalibrate_scores.py's usage_counts (same skill-load filter)
  - source (mcp|plugin) attribution, including legacy rows with no `source`
  - idempotence: the doc is a pure function of its input (no wall clock)
  - the watermark is echoed verbatim — it is the dashboard's exact live-tail
    boundary, so a wrong value means double-counted or missing events
  - sync_registry writes meta/usage_rollup BEFORE meta/registry, preserving
    meta/registry as the failure-honest commit marker

Run: python3 scripts/test_usage_rollup.py
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mcp-server"))

from usage_rollup import (  # noqa: E402
    build_skill_domain_map,
    build_usage_rollup,
    normalize_source,
    read_watermark,
)


def rows():
    """A usage log mixing sources, a search event, and an undomained skill."""
    return [
        {"skill": "alpha", "type": "action", "timestamp": "2026-07-01T10:00:00+00:00"},
        {"skill": "alpha", "type": "action", "source": "mcp",
         "timestamp": "2026-07-02T10:00:00+00:00"},
        {"skill": "beta", "type": "knowledge", "source": "plugin",
         "timestamp": "2026-07-03T10:00:00+00:00"},
        {"skill": "alpha", "type": "action", "source": "plugin",
         "timestamp": "2026-07-03T11:00:00+00:00"},
        # search event: no skill field — must not be counted
        {"type": "search", "query": "x", "result_count": 0,
         "timestamp": "2026-07-03T12:00:00+00:00"},
        # skill with no domain in the registry — counted in totals, skipped in
        # the domain×day heatmap (matches the dashboard's old `if (!d) continue`)
        {"skill": "orphan", "type": "action",
         "timestamp": "2026-07-03T13:00:00+00:00"},
    ]


DOMAINS = {"alpha": "meta", "beta": "meta", "gamma": "investing"}


def test_counts_match_recalibrate_filter():
    """Totals must equal Counter(e['skill'] for e in iter_skill_uses(...)) —
    the exact expression recalibrate_scores.py uses. If these diverge the
    dashboard shows scores its usage panel cannot explain, which is the whole
    defect this rollup closes."""
    from shared import iter_skill_uses

    expected = Counter(e["skill"] for e in iter_skill_uses(rows()))
    roll = build_usage_rollup(rows(), DOMAINS)
    assert roll["totals"] == dict(expected), (roll["totals"], expected)
    assert roll["event_count"] == sum(expected.values()) == 5, roll["event_count"]


def test_search_events_excluded():
    roll = build_usage_rollup(rows(), DOMAINS)
    assert "" not in roll["totals"]
    assert None not in roll["totals"]
    assert sum(roll["by_source"].values()) == roll["event_count"]


def test_source_attribution_and_legacy_default():
    """Rows predating the `source` field came from the MCP server."""
    roll = build_usage_rollup(rows(), DOMAINS)
    # alpha: 1 legacy + 1 explicit mcp + 1 plugin;  beta: 1 plugin; orphan: 1 legacy
    assert roll["by_source"] == {"mcp": 3, "plugin": 2}, roll["by_source"]
    assert roll["totals_by_source"]["mcp"] == {"alpha": 2, "orphan": 1}
    assert roll["totals_by_source"]["plugin"] == {"alpha": 1, "beta": 1}
    # Per-skill splits must sum back to the per-skill total.
    for skill, total in roll["totals"].items():
        by_src = sum(c.get(skill, 0) for c in roll["totals_by_source"].values())
        assert by_src == total, (skill, by_src, total)


def test_normalize_source_agrees_with_shared_event_source():
    """usage_rollup.normalize_source duplicates shared.event_source because it
    must run without the mcp-server package installed (sync-firestore.yml only
    installs google-cloud-firestore). Pin them together so the dashboard's
    buckets can never drift from the MCP server's and the CLI's."""
    from shared import event_source

    for row in [{}, {"source": "mcp"}, {"source": "plugin"}, {"source": "cli"},
                {"skill": "a"}, {"source": None}, {"source": ""}]:
        assert normalize_source(row) == event_source(row), row


def test_skill_raw_rows_are_never_counted():
    """The plugin hook writes unresolved invocation names as `skill_raw`, never
    `skill`, so a foreign plugin name cannot become recalibrate's max_usage
    denominator. The rollup must honour that same boundary, or the dashboard
    would show usage the scores don't have."""
    log = [
        {"skill": "alpha", "source": "plugin", "timestamp": "2026-07-01T00:00:00+00:00"},
        {"skill_raw": "codex:review", "type": "unresolved", "source": "plugin",
         "timestamp": "2026-07-01T01:00:00+00:00"},
        {"skill_raw": "anthropic-skills:docx", "type": "unresolved", "source": "plugin",
         "timestamp": "2026-07-01T02:00:00+00:00"},
    ]
    roll = build_usage_rollup(log, DOMAINS)
    assert roll["event_count"] == 1
    assert roll["totals"] == {"alpha": 1}
    assert roll["by_source"] == {"plugin": 1}
    assert "codex:review" not in roll["totals"]
    assert [r["skill"] for r in roll["recent"]] == ["alpha"]


def test_unknown_source_is_not_relabelled_mcp():
    """A future writer must surface as its own bucket, not be swallowed."""
    assert normalize_source({"source": "cli"}) == "cli"
    assert normalize_source({"source": "  "}) == "mcp"
    assert normalize_source({}) == "mcp"
    roll = build_usage_rollup(
        [{"skill": "a", "source": "cli", "timestamp": "2026-07-01T00:00:00+00:00"}],
        DOMAINS,
    )
    assert roll["by_source"] == {"cli": 1}


def test_domain_day_skips_undomained_and_keys_correctly():
    roll = build_usage_rollup(rows(), DOMAINS)
    assert roll["domain_day"] == {
        "meta|2026-07-01": 1,
        "meta|2026-07-02": 1,
        "meta|2026-07-03": 2,
    }, roll["domain_day"]
    # 'orphan' has no domain, so 2026-07-03 counts 2 (beta + alpha), not 3.
    assert roll["days"] == ["2026-07-01", "2026-07-02", "2026-07-03"]


def test_domain_day_bounded_on_active_days_not_calendar_days():
    """The bound must count days that HAVE events, not calendar days.

    Usage here is sparse and bursty — a calendar window would silently drop
    active days the heatmap (last 7 active days) used to display, even though
    the map stayed well within any size limit.
    """
    # Six years apart, but only two active days: both must survive a bound of 2.
    old = {"skill": "alpha", "timestamp": "2020-01-01T00:00:00+00:00"}
    new = {"skill": "alpha", "timestamp": "2026-07-03T00:00:00+00:00"}
    roll = build_usage_rollup([old, new], DOMAINS, active_days=2)
    assert roll["domain_day"] == {"meta|2020-01-01": 1, "meta|2026-07-03": 1}
    assert roll["days"] == ["2020-01-01", "2026-07-03"]

    # Tightening the bound to 1 keeps only the newest active day...
    tight = build_usage_rollup([old, new], DOMAINS, active_days=1)
    assert tight["domain_day"] == {"meta|2026-07-03": 1}, tight["domain_day"]
    # ...while the all-time totals stay complete regardless of the bound.
    assert tight["totals"] == roll["totals"] == {"alpha": 2}


def test_domain_day_bound_is_wall_clock_independent():
    """No `now()` anywhere: the doc is a pure function of the log, so CI can
    diff it and the score-idempotency gate stays deterministic."""
    log = [{"skill": "alpha", "timestamp": "2020-01-01T00:00:00+00:00"}]
    roll = build_usage_rollup(log, DOMAINS)
    # A years-old sole event is still charted; nothing is aged out by "today".
    assert roll["domain_day"] == {"meta|2020-01-01": 1}
    assert roll["days"] == ["2020-01-01"]


def test_recent_is_newest_first_and_capped():
    roll = build_usage_rollup(rows(), DOMAINS, recent_limit=2)
    assert [r["timestamp"] for r in roll["recent"]] == [
        "2026-07-03T13:00:00+00:00", "2026-07-03T11:00:00+00:00"]
    assert roll["recent_truncated"] is True
    assert roll["recent"][0]["source"] == "mcp"
    assert roll["recent"][1]["source"] == "plugin"
    # `type` is carried for the infra page's activity feed.
    assert roll["recent"][1]["type"] == "action"
    full = build_usage_rollup(rows(), DOMAINS)
    assert full["recent_truncated"] is False
    assert len(full["recent"]) == 5


def test_latest_timestamp_and_watermark_echoed():
    """The watermark is the dashboard's live-tail boundary — it must round-trip
    verbatim, and its absence must be explicit (None, not '')."""
    roll = build_usage_rollup(rows(), DOMAINS, watermark="2026-07-02T00:00:00+00:00")
    assert roll["firestore_watermark"] == "2026-07-02T00:00:00+00:00"
    assert roll["latest_timestamp"] == "2026-07-03T13:00:00+00:00"
    assert build_usage_rollup(rows(), DOMAINS)["firestore_watermark"] is None


def test_idempotent_for_same_input():
    a = build_usage_rollup(rows(), DOMAINS, watermark="w")
    b = build_usage_rollup(list(reversed(rows())), DOMAINS, watermark="w")
    assert a == b, "rollup must not depend on input order or the wall clock"


def test_empty_log_is_safe():
    roll = build_usage_rollup([], DOMAINS)
    assert roll["event_count"] == 0
    assert roll["totals"] == {} and roll["by_source"] == {}
    assert roll["domain_day"] == {} and roll["days"] == []
    assert roll["recent"] == [] and roll["latest_timestamp"] is None
    assert roll["recent_truncated"] is False


def test_malformed_timestamps_do_not_crash():
    bad = [
        {"skill": "alpha", "timestamp": None},
        {"skill": "alpha", "timestamp": "short"},
        {"skill": "alpha"},
        {"skill": "beta", "timestamp": "2026-07-03T10:00:00+00:00"},
    ]
    roll = build_usage_rollup(bad, DOMAINS)
    assert roll["totals"] == {"alpha": 3, "beta": 1}
    # Only the well-formed row can land in the day grid.
    assert roll["domain_day"] == {"meta|2026-07-03": 1}


def test_build_skill_domain_map():
    registry = {"network": {"domains": {"meta": ["a", "b"], "investing": ["c"]}}}
    assert build_skill_domain_map(registry) == {
        "a": "meta", "b": "meta", "c": "investing"}
    assert build_skill_domain_map({}) == {}


def test_read_watermark(tmp=None):
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / ".telemetry_watermark"
        assert read_watermark(path) is None, "missing file → None"
        path.write_text("")
        assert read_watermark(path) is None, "empty file → None, not ''"
        path.write_text("2026-07-11T22:04:39.154814+00:00\n")
        assert read_watermark(path) == "2026-07-11T22:04:39.154814+00:00"


def test_rollup_written_before_meta_registry():
    """meta/registry must stay the LAST write (the failure-honest commit
    marker documented in migrate_to_firestore). A mid-run failure after the
    rollup must leave meta/registry describing the previous snapshot."""
    import argparse

    import migrate_to_firestore as mig
    from test_migrate_to_firestore import FakeDB

    db = FakeDB()
    registry = {
        "schema_version": 2,
        "skills": {f"s{i}": {"composite_score": 50} for i in range(3)},
        "network": {"domains": {"meta": ["s0", "s1", "s2"]}},
    }
    args = argparse.Namespace(dry_run=False, prune=False, sha=None)
    mig.sync_registry(db, registry, args)

    meta_writes = [e for e in db.events if e[1] == "meta"]
    assert [e[2] for e in meta_writes] == ["usage_rollup", "registry"], meta_writes
    assert db.events[-1] == ("set", "meta", "registry"), db.events[-1]
    # And the doc it wrote is the real aggregate of the repo's committed log.
    doc = db.store["meta"]["usage_rollup"]
    assert doc["source_file"] == "data/usage.jsonl"
    assert sum(doc["by_source"].values()) == doc["event_count"]


def main():
    tests = [
        test_counts_match_recalibrate_filter,
        test_search_events_excluded,
        test_source_attribution_and_legacy_default,
        test_normalize_source_agrees_with_shared_event_source,
        test_skill_raw_rows_are_never_counted,
        test_unknown_source_is_not_relabelled_mcp,
        test_domain_day_skips_undomained_and_keys_correctly,
        test_domain_day_bounded_on_active_days_not_calendar_days,
        test_domain_day_bound_is_wall_clock_independent,
        test_recent_is_newest_first_and_capped,
        test_latest_timestamp_and_watermark_echoed,
        test_idempotent_for_same_input,
        test_empty_log_is_safe,
        test_malformed_timestamps_do_not_crash,
        test_build_skill_domain_map,
        test_read_watermark,
        test_rollup_written_before_meta_registry,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
