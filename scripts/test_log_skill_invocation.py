#!/usr/bin/env python3
"""
test_log_skill_invocation.py — Tests for plugin-native usage capture.

Pins the guards that keep hook-written telemetry from corrupting scores:
foreign plugin names never get a `skill` field (they would become the
max_usage denominator in recalibrate_scores.py), aliases only resolve to real
registry entries, the emitted schema is what iter_skill_uses/migrate expect,
and the per-(session, day) cap bounds a runaway loop.

Run: python3 scripts/test_log_skill_invocation.py
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mcp-server"))

from log_skill_invocation import (  # noqa: E402
    build_event, resolve_skill, over_session_cap, append_event, report_unresolved,
)
from shared import iter_skill_uses, event_source, SOURCE_MCP  # noqa: E402

SKILLS = {
    "six-eyes": {"type": "orchestrator", "plugin": "skill-binding-vow"},
    "asclepius": {"type": "orchestrator", "plugin": "skill-biotech-venture"},
    "statement-grader": {"type": "action", "plugin": "skill-binding-vow"},
}
ALIASES = {"diligence": "asclepius", "grade": "statement-grader", "ghost": "not-a-skill"}


def payload(skill, session="s1"):
    return {
        "session_id": session,
        "tool_name": "Skill",
        "tool_input": {"skill": skill, "args": "..."},
    }


def test_exact_registry_name_resolves():
    assert resolve_skill("six-eyes", SKILLS, ALIASES) == "six-eyes"


def test_alias_resolves_to_registry_name():
    assert resolve_skill("diligence", SKILLS, ALIASES) == "asclepius"


def test_alias_to_missing_skill_is_rejected():
    # A stale alias must not invent a skill name that scoring can't look up.
    assert resolve_skill("ghost", SKILLS, ALIASES) is None


def test_own_plugin_prefix_is_stripped():
    assert resolve_skill("skill-binding-vow:six-eyes", SKILLS, ALIASES) == "six-eyes"


def test_foreign_plugin_prefix_is_not_stripped():
    # codex:review has 31 invocations; if it resolved, max_usage would be 31
    # and every real skill's usage score would be divided down by it.
    assert resolve_skill("codex:review", SKILLS, ALIASES) is None
    assert resolve_skill("anthropic-skills:docx", SKILLS, ALIASES) is None


def test_resolved_event_schema_is_scoreable():
    event = build_event(payload("diligence"), SKILLS, ALIASES)
    assert event["skill"] == "asclepius"
    assert event["type"] == "orchestrator"
    assert event["source"] == "plugin"
    assert event["invoked_as"] == "diligence", "raw name kept for auditing"
    assert event["session_id"] == "s1"
    assert event["timestamp"].endswith("+00:00"), "ISO UTC, lexicographically ordered"
    assert list(iter_skill_uses([event])) == [event], "must count as a skill use"


def test_unresolved_event_is_quarantined():
    event = build_event(payload("codex:review"), SKILLS, ALIASES)
    assert "skill" not in event, "no `skill` key — scoring and Firestore both skip it"
    assert event["skill_raw"] == "codex:review"
    assert list(iter_skill_uses([event])) == [], "must not count as a skill use"


def test_non_skill_tool_is_ignored():
    assert build_event({"tool_name": "Bash", "tool_input": {"command": "ls"}}, SKILLS, ALIASES) is None
    assert build_event(payload(""), SKILLS, ALIASES) is None


def test_failed_skill_call_is_not_logged():
    ok = dict(payload("six-eyes"), tool_response="Launching skill: six-eyes")
    assert build_event(ok, SKILLS, ALIASES) is not None
    for bad in ("Error: skill not found", {"is_error": True}, {"error": "nope"}):
        p = dict(payload("six-eyes"), tool_response=bad)
        assert build_event(p, SKILLS, ALIASES) is None, f"logged a failed call: {bad}"


def test_legacy_rows_read_as_mcp():
    assert event_source({"skill": "six-eyes", "type": "action"}) == SOURCE_MCP
    assert event_source({"skill": "six-eyes", "source": "plugin"}) == "plugin"


def test_session_daily_cap_bounds_runaway_loops():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "usage.jsonl"
        for i in range(50):
            append_event(
                {"session_id": "s1", "skill": "six-eyes", "source": "plugin",
                 "timestamp": f"2026-07-26T00:00:{i:02d}+00:00"},
                path,
            )
        capped = {"session_id": "s1", "timestamp": "2026-07-26T01:00:00+00:00"}
        assert over_session_cap(capped, path) is True
        next_day = {"session_id": "s1", "timestamp": "2026-07-27T00:00:00+00:00"}
        assert over_session_cap(next_day, path) is False, "cap resets daily"
        other = {"session_id": "s2", "timestamp": "2026-07-26T01:00:00+00:00"}
        assert over_session_cap(other, path) is False, "cap is per session"


def test_cap_ignores_mcp_events():
    # The MCP server has its own path; its volume must not starve the hook.
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "usage.jsonl"
        for i in range(60):
            append_event(
                {"session_id": "s1", "skill": "six-eyes", "source": "mcp",
                 "timestamp": f"2026-07-26T00:00:{i:02d}+00:00"},
                path,
            )
        assert over_session_cap(
            {"session_id": "s1", "timestamp": "2026-07-26T01:00:00+00:00"}, path
        ) is False


def test_append_writes_one_valid_json_line():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "usage.jsonl"
        event = build_event(payload("six-eyes"), SKILLS, ALIASES)
        append_event(event, path)
        rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        assert len(rows) == 1 and rows[0]["skill"] == "six-eyes"


def test_report_separates_attributed_from_unresolved():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "usage.jsonl"
        append_event(build_event(payload("diligence"), SKILLS, ALIASES), path)
        append_event(build_event(payload("kol"), SKILLS, ALIASES), path)
        append_event({"skill": "six-eyes", "source": "mcp", "timestamp": "2026-07-26T00:00:00+00:00"}, path)
        out = report_unresolved(path)
        assert "asclepius" in out and "kol" in out
        assert "1 attributed" in out and "1 unresolved" in out, out


def run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
