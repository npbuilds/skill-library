#!/usr/bin/env python3
"""
test_pull_telemetry.py — Tests for the Firestore→git telemetry pull.

Pins the two loss/duplication guards: the per-(session, day) usage cap
(score-pollution bound for a public endpoint) and _fs_id-based append dedupe
(no event lands twice even if the watermark regresses).

Run: python3 scripts/test_pull_telemetry.py
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pull_telemetry_from_firestore import append_events, cap_usage_events


def test_cap_bounds_per_session_per_day():
    events = []
    # 60 events from one session on one day, 3 from another session same day,
    # 2 from the first session on the NEXT day.
    for i in range(60):
        events.append((f"a_t{i}", {"session_id": "bot", "timestamp": f"2026-07-11T00:00:{i:02d}+00:00"}))
    for i in range(3):
        events.append((f"b_t{i}", {"session_id": "human", "timestamp": f"2026-07-11T01:00:{i:02d}+00:00"}))
    for i in range(2):
        events.append((f"c_t{i}", {"session_id": "bot", "timestamp": f"2026-07-12T00:00:{i:02d}+00:00"}))

    kept, dropped = cap_usage_events(events, cap=50)
    assert dropped == 10, f"expected 10 dropped, got {dropped}"
    bot_day1 = [e for _, e in kept if e["session_id"] == "bot" and e["timestamp"].startswith("2026-07-11")]
    assert len(bot_day1) == 50, "cap must bind per session per day"
    assert len([e for _, e in kept if e["session_id"] == "human"]) == 3, "other sessions unaffected"
    assert len([e for _, e in kept if e["timestamp"].startswith("2026-07-12")]) == 2, "next day resets the cap"


def test_append_dedupes_on_fs_id():
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "usage.jsonl"
        # A legacy row without _fs_id and a previously-pulled row with one.
        path.write_text(
            json.dumps({"session_id": "old", "timestamp": "t0"}) + "\n"
            + json.dumps({"session_id": "s", "timestamp": "t1", "_fs_id": "s_t1_0"}) + "\n"
        )
        events = [
            ("s_t1_0", {"session_id": "s", "timestamp": "t1"}),  # already pulled
            ("s_t2_1", {"session_id": "s", "timestamp": "t2"}),  # fresh
        ]
        appended = append_events(path, events, dry_run=False)
        assert appended == 1, f"expected 1 appended, got {appended}"
        rows = [json.loads(l) for l in path.read_text().strip().split("\n")]
        assert len(rows) == 3
        assert rows[-1]["_fs_id"] == "s_t2_1"
        # Idempotent: same call again appends nothing.
        assert append_events(path, events, dry_run=False) == 0


def test_dry_run_writes_nothing():
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "usage.jsonl"
        path.write_text("")
        would = append_events(path, [("x_1_0", {"session_id": "x", "timestamp": "1"})], dry_run=True)
        assert would == 1
        assert path.read_text() == "", "dry-run must not write"


def test_append_survives_a_non_dict_row_in_the_local_log():
    """The dedupe reads `row.get("_fs_id")` over the whole local file, so one
    non-dict row used to raise AttributeError inside the nightly bot-PR job —
    the same job whose push this work repaired. parse_jsonl now drops such rows
    at the parse boundary; this pins that the dedupe still sees the real ids."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "usage.jsonl"
        path.write_text(
            '{"skill": "a", "_fs_id": "s_1"}\n'
            '"a bare string"\n'
            '[1,2]\n'
            '{"skill": "b", "_fs_id": "s_2"}\n'
        )
        # s_2 is already present, s_3 is new — the known id must still dedupe.
        appended = append_events(
            path, [("s_2", {"skill": "b"}), ("s_3", {"skill": "c"})], dry_run=False
        )
        assert appended == 1, appended
        rows = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        assert [r.get("_fs_id") for r in rows if isinstance(r, dict)][-1] == "s_3"


def main():
    tests = [
        test_cap_bounds_per_session_per_day,
        test_append_dedupes_on_fs_id,
        test_dry_run_writes_nothing,
        test_append_survives_a_non_dict_row_in_the_local_log,
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
