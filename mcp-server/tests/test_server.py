"""Tests for the Skill Library MCP server."""

import json
import os
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import server


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_REGISTRY = {
    "skills": {
        "color-theory": {
            "name": "color-theory",
            "description": "Understand color relationships and palettes.",
            "location": "skills/design/color-theory/SKILL.md",
            "type": "knowledge",
            "status": "active",
            "health_status": "healthy",
            "composite_score": 85,
            "tags": ["domain:design", "subdomain:visual-communication"],
            "parent": "design-director",
            "depends_on": [],
            "referenced_by": [],
            "metrics": {"word_count": 500},
            "last_modified": "2026-03-01",
        },
        "design-director": {
            "name": "design-director",
            "description": "Routes design queries to the right skill.",
            "location": "skills/design/design-director/SKILL.md",
            "type": "director",
            "status": "active",
            "health_status": "healthy",
            "composite_score": 90,
            "tags": ["domain:design", "subdomain:visual-communication"],
            "parent": None,
            "depends_on": [],
            "referenced_by": ["color-theory"],
            "metrics": {},
            "last_modified": "2026-03-01",
        },
        "data-wrangling": {
            "name": "data-wrangling",
            "description": "Clean, reshape, and transform messy datasets.",
            "location": "skills/data-science/data-wrangling/SKILL.md",
            "type": "knowledge",
            "status": "active",
            "health_status": "unhealthy",
            "composite_score": 40,
            "tags": ["domain:data-science"],
            "parent": None,
            "depends_on": ["missing-skill"],
            "referenced_by": [],
            "metrics": {},
            "last_modified": "2026-03-10",
        },
    },
    "network": {
        "domains": {
            "design": ["color-theory", "design-director"],
            "data-science": ["data-wrangling"],
        }
    },
}


@pytest.fixture
def tmp_project(tmp_path):
    """Set up a temporary project directory with a registry and skill files."""
    # Create data dir with registry
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "registry.json").write_text(json.dumps(MINIMAL_REGISTRY))

    # Create skill dirs with SKILL.md files
    for skill_name, entry in MINIMAL_REGISTRY["skills"].items():
        location = entry["location"]
        skill_file = tmp_path / location
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(f"# {skill_name}\n\nThis is the {skill_name} skill.\n")

    # Create a reference file for color-theory
    refs_dir = tmp_path / "skills/design/color-theory/references"
    refs_dir.mkdir()
    (refs_dir / "color-wheel.md").write_text("# Color Wheel\n\nReference content.\n")

    # Patch module-level paths to use tmp_path.
    # Note: `shared` module globals must also be patched because functions like
    # `atomic_write_registry` live in shared.py and read shared.REGISTRY_PATH
    # (not server.REGISTRY_PATH). Without this, writes escape the test sandbox.
    import shared
    with (
        patch.object(server, "PROJECT_ROOT", tmp_path),
        patch.object(server, "REGISTRY_PATH", data_dir / "registry.json"),
        patch.object(server, "SKILLS_DIR", tmp_path / "skills"),
        patch.object(server, "DATA_DIR", data_dir),
        patch.object(server, "USAGE_LOG", data_dir / "usage.jsonl"),
        patch.object(server, "GAPS_LOG", data_dir / "gaps.jsonl"),
        patch.object(server, "FEEDBACK_LOG", data_dir / "feedback.jsonl"),
        patch.object(shared, "PROJECT_ROOT", tmp_path),
        patch.object(shared, "REGISTRY_PATH", data_dir / "registry.json"),
        patch.object(shared, "DATA_DIR", data_dir),
    ):
        yield tmp_path


# ---------------------------------------------------------------------------
# load_registry
# ---------------------------------------------------------------------------


class TestLoadRegistry:
    def test_loads_valid_registry(self, tmp_project):
        reg = server.load_registry()
        assert "skills" in reg
        assert "color-theory" in reg["skills"]

    def test_raises_on_missing_file(self, tmp_path):
        with patch.object(server, "REGISTRY_PATH", tmp_path / "nope.json"):
            with pytest.raises(RuntimeError, match="Registry not found"):
                server.load_registry()

    def test_raises_on_invalid_json(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{not valid json")
        with patch.object(server, "REGISTRY_PATH", bad_file):
            with pytest.raises(RuntimeError, match="invalid JSON"):
                server.load_registry()


# ---------------------------------------------------------------------------
# list_skills
# ---------------------------------------------------------------------------


class TestListSkills:
    def test_lists_all_skills(self, tmp_project):
        result = server.list_skills()
        assert "Found 3 skill(s)" in result
        assert "color-theory" in result
        assert "data-wrangling" in result

    def test_filters_by_domain(self, tmp_project):
        result = server.list_skills(domain="design")
        assert "color-theory" in result
        assert "data-wrangling" not in result

    def test_filters_by_type(self, tmp_project):
        result = server.list_skills(skill_type="director")
        assert "design-director" in result
        assert "color-theory" not in result

    def test_filters_by_subdomain_excludes_directors(self, tmp_project):
        result = server.list_skills(subdomain="visual-communication")
        assert "color-theory" in result
        # Directors that own the subdomain are excluded as entries
        assert "[director] design-director" not in result

    def test_no_matches_returns_message(self, tmp_project):
        result = server.list_skills(domain="nonexistent")
        assert "No skills found" in result


class TestListSkillsPagination:
    def test_limit_slices_results(self, tmp_project):
        result = server.list_skills(limit=2)
        assert "Found 3 skill(s), showing 1–2" in result
        assert "call again with offset=2" in result
        # Sorted by (domain, name): "data-science" < "design", so the page is
        # data-wrangling, color-theory. design-director (page 2) appears only
        # as color-theory's parent annotation, not as an entry.
        assert "data-wrangling" in result
        assert "[director] design-director" not in result

    def test_offset_returns_next_page(self, tmp_project):
        page1 = server.list_skills(limit=2)
        page2 = server.list_skills(limit=2, offset=2)
        assert "showing 3–3" in page2
        assert "design-director" in page2
        assert "data-wrangling" not in page2
        # No overlap between pages
        assert "color-theory" in page1 and "color-theory" not in page2

    def test_offset_past_end(self, tmp_project):
        result = server.list_skills(offset=99)
        assert "past the end" in result
        assert "offset < 3" in result

    def test_domains_footer_first_page_only(self, tmp_project):
        page1 = server.list_skills(limit=2)
        page2 = server.list_skills(limit=2, offset=2)
        assert "Available domains:" in page1
        assert "Available domains:" not in page2

    def test_limit_zero_returns_all(self, tmp_project):
        result = server.list_skills(limit=0)
        assert "showing 1–3" in result
        assert "call again with offset" not in result

    def test_deterministic_order_across_calls(self, tmp_project):
        assert server.list_skills() == server.list_skills()


class TestIndexFreshnessKey:
    def test_key_changes_when_synthetic_queries_change(self, tmp_project):
        """The search index ingests synthetic_queries.json, so the freshness
        key must change when that file changes — otherwise a running server
        serves a stale index after query regeneration without a registry edit."""
        import json as _json
        import os as _os

        syn = server.DATA_DIR / "synthetic_queries.json"
        key1 = server._index_freshness_key()
        assert key1 is not None and key1[1] == 0.0  # absent → 0.0

        syn.write_text(_json.dumps({"version": 1, "skills": {}}))
        # Force a later mtime so the change is observable regardless of clock
        # granularity.
        future = _os.path.getmtime(server.REGISTRY_PATH) + 100
        _os.utime(syn, (future, future))
        key2 = server._index_freshness_key()
        assert key2 != key1 and key2[1] != 0.0

    def test_key_none_when_registry_missing(self, tmp_path):
        with patch.object(server, "REGISTRY_PATH", tmp_path / "nope.json"):
            assert server._index_freshness_key() is None


# ---------------------------------------------------------------------------
# search_skills
# ---------------------------------------------------------------------------


class TestSearchSkills:
    def test_finds_by_name(self, tmp_project):
        result = server.search_skills("color")
        assert "color-theory" in result

    def test_finds_by_description(self, tmp_project):
        result = server.search_skills("palette")
        assert "color-theory" in result

    def test_finds_by_tag(self, tmp_project):
        result = server.search_skills("data-science")
        assert "data-wrangling" in result

    def test_case_insensitive(self, tmp_project):
        result = server.search_skills("COLOR")
        assert "color-theory" in result

    def test_no_match_logs_gap(self, tmp_project):
        result = server.search_skills("quantum-physics")
        assert "No skills found" in result
        # Check that a gap was logged
        gaps = server._load_log(server.GAPS_LOG)
        assert len(gaps) == 1
        assert gaps[0]["query"] == "quantum-physics"
        assert gaps[0]["result_count"] == 0

    def test_low_result_logs_gap(self, tmp_project):
        # "wrangling" matches only data-wrangling (1 result)
        server.search_skills("wrangling")
        gaps = server._load_log(server.GAPS_LOG)
        assert len(gaps) == 1
        assert gaps[0]["result_count"] == 1


# ---------------------------------------------------------------------------
# get_skill
# ---------------------------------------------------------------------------


class TestGetSkill:
    def test_returns_skill_content(self, tmp_project):
        result = server.get_skill("color-theory")
        assert "=== SKILL: color-theory ===" in result
        assert "This is the color-theory skill" in result

    def test_includes_references(self, tmp_project):
        result = server.get_skill("color-theory", include_references=True)
        assert "REFERENCE DOCUMENTS" in result
        assert "color-wheel.md" in result

    def test_excludes_references_when_disabled(self, tmp_project):
        result = server.get_skill("color-theory", include_references=False)
        assert "REFERENCE DOCUMENTS" not in result

    def test_logs_usage(self, tmp_project):
        server.get_skill("color-theory")
        usage = server._load_log(server.USAGE_LOG)
        assert len(usage) == 1
        assert usage[0]["skill"] == "color-theory"

    def test_not_found(self, tmp_project):
        result = server.get_skill("nonexistent")
        assert "not found" in result


# ---------------------------------------------------------------------------
# get_skill_details
# ---------------------------------------------------------------------------


class TestGetSkillDetails:
    def test_returns_json(self, tmp_project):
        result = server.get_skill_details("color-theory")
        details = json.loads(result)
        assert details["name"] == "color-theory"
        assert details["type"] == "knowledge"
        assert details["score"] == 85

    def test_not_found(self, tmp_project):
        result = server.get_skill_details("nope")
        assert "not found" in result


# ---------------------------------------------------------------------------
# record_skill_feedback
# ---------------------------------------------------------------------------


class TestRecordFeedback:
    def test_records_valid_feedback(self, tmp_project):
        result = server.record_skill_feedback("color-theory", 4, "great detail")
        assert "Recorded" in result
        assert "4/5" in result
        fb = server._load_log(server.FEEDBACK_LOG)
        assert len(fb) == 1
        assert fb[0]["rating"] == 4
        assert fb[0]["note"] == "great detail"

    def test_rejects_invalid_rating(self, tmp_project):
        result = server.record_skill_feedback("color-theory", 6)
        assert "between 1 and 5" in result

    def test_rejects_unknown_skill(self, tmp_project):
        result = server.record_skill_feedback("nonexistent", 3)
        assert "not found" in result


# ---------------------------------------------------------------------------
# get_skill_stats
# ---------------------------------------------------------------------------


class TestGetSkillStats:
    def test_empty_stats(self, tmp_project):
        result = server.get_skill_stats()
        assert "No analytics data" in result

    def test_single_skill_stats(self, tmp_project):
        # Generate some usage
        server.get_skill("color-theory")
        server.get_skill("color-theory")
        server.record_skill_feedback("color-theory", 5, "perfect")

        result = server.get_skill_stats("color-theory")
        assert "Total uses: 2" in result
        assert "5.0/5" in result
        assert "perfect" in result

    def test_summary_stats(self, tmp_project):
        server.get_skill("color-theory")
        server.get_skill("data-wrangling")
        server.get_skill("color-theory")
        server.search_skills("quantum")  # gap

        result = server.get_skill_stats()
        assert "Total skill loads: 3" in result
        assert "color-theory: 2" in result
        assert "quantum" in result

    def test_summary_labels_redacted_remote_gaps(self, tmp_project):
        with (
            patch.object(server, "REMOTE_MODE", True),
            patch.dict(os.environ, {}, clear=False),
        ):
            os.environ.pop("TELEMETRY_SEARCH_QUERIES", None)
            server.search_skills("private-unmatched-query")

        result = server.get_skill_stats()
        assert "[redacted remote queries]" in result
        assert "1 search(es), 1 with no results" in result
        assert '"?"' not in result

    def test_shows_unused_skills(self, tmp_project):
        server.get_skill("color-theory")
        result = server.get_skill_stats()
        assert "Never used" in result
        assert "data-wrangling" in result

    def test_no_analytics_when_only_search_events(self, tmp_project):
        # Search-only history (no skill loads, no feedback, no gaps) should
        # report "No analytics" — search events alone are not skill activity.
        # Inject directly so we control the log shape without depending on
        # tmp_project's registry contents to dictate gap thresholds.
        server.USAGE_LOG.write_text(
            json.dumps({
                "session_id": "test-session",
                "type": "search",
                "query": "anything",
                "result_count": 5,
                "timestamp": "2026-05-16T00:00:00Z",
            }) + "\n"
        )
        result = server.get_skill_stats()
        assert "No analytics data" in result


# ---------------------------------------------------------------------------
# get_system_overview
# ---------------------------------------------------------------------------


class TestSystemOverview:
    def test_returns_overview(self, tmp_project):
        result = server.get_system_overview()
        assert "SKILL LIBRARY OVERVIEW" in result
        assert "design" in result
        assert "data-science" in result

    def test_detects_broken_dependencies(self, tmp_project):
        result = server.get_system_overview()
        # data-wrangling depends on "missing-skill"
        assert "missing-skill" in result

    def test_detects_unhealthy_skills(self, tmp_project):
        result = server.get_system_overview()
        assert "data-wrangling" in result


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


class TestLogEvent:
    def test_writes_jsonl(self, tmp_project):
        log_path = server.DATA_DIR / "test.jsonl"
        server._log_event(log_path, {"action": "test"})
        events = server._load_log(log_path)
        assert len(events) == 1
        assert events[0]["action"] == "test"
        assert "timestamp" in events[0]

    def test_does_not_mutate_input(self, tmp_project):
        log_path = server.DATA_DIR / "test.jsonl"
        event = {"action": "test"}
        server._log_event(log_path, event)
        assert "timestamp" not in event

    def test_handles_write_errors(self, tmp_path):
        # Path to a directory that doesn't exist
        bad_path = tmp_path / "no" / "such" / "dir" / "log.jsonl"
        # Should not raise
        server._log_event(bad_path, {"action": "test"})

    def test_write_errors_reported_to_stderr(self, tmp_path, capsys):
        """Failed log writes must not raise, but must not vanish either —
        they go to stderr where Cloud Logging picks them up."""
        bad_path = tmp_path / "no" / "such" / "dir" / "log.jsonl"
        server._log_event(bad_path, {"action": "test"})
        captured = capsys.readouterr()
        assert "failed to write log" in captured.err
        assert "log.jsonl" in captured.err


class TestLoadLog:
    def test_handles_missing_file(self, tmp_path):
        result = server._load_log(tmp_path / "nope.jsonl")
        assert result == []

    def test_skips_corrupt_lines(self, tmp_path):
        log = tmp_path / "mixed.jsonl"
        log.write_text('{"good": true}\nnot json\n{"also": "good"}\n')
        result = server._load_log(log)
        assert len(result) == 2


class TestResolveSkillPath:
    def test_resolves_relative_location(self, tmp_project):
        entry = MINIMAL_REGISTRY["skills"]["color-theory"]
        path = server.resolve_skill_path(entry, "color-theory")
        assert path.endswith("SKILL.md")
        assert Path(path).exists()

    def test_falls_back_to_search(self, tmp_project):
        entry = {"location": "nonexistent/path/SKILL.md"}
        path = server.resolve_skill_path(entry, "color-theory")
        # Should find it by rglob
        assert "color-theory" in path
        assert path.endswith("SKILL.md")

    def test_returns_none_for_missing_skill(self, tmp_project):
        entry = {"location": "nonexistent/path/SKILL.md"}
        path = server.resolve_skill_path(entry, "totally-fake")
        assert path is None


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestDeletedSkillFile:
    """Skill is registered in the registry but its SKILL.md has been deleted."""

    def test_get_skill_returns_friendly_error(self, tmp_project):
        # Delete the skill file on disk while leaving the registry entry intact
        skill_file = tmp_project / "skills/design/color-theory/SKILL.md"
        skill_file.unlink()

        result = server.get_skill("color-theory")
        # Should not raise; should return a message explaining the file is missing
        assert "could not read file" in result or "not found" in result.lower()

    def test_get_skill_still_logs_usage(self, tmp_project):
        # Usage should still be logged even if the file is missing
        skill_file = tmp_project / "skills/design/color-theory/SKILL.md"
        skill_file.unlink()

        server.get_skill("color-theory")
        usage = server._load_log(server.USAGE_LOG)
        assert any(e.get("skill") == "color-theory" for e in usage)

    def test_system_overview_does_not_crash(self, tmp_project):
        # Overview reads registry only, not files — should not be affected
        skill_file = tmp_project / "skills/design/color-theory/SKILL.md"
        skill_file.unlink()
        result = server.get_system_overview()
        assert "SKILL LIBRARY OVERVIEW" in result


class TestCircularDependencies:
    """Skills that form a dependency cycle: A depends_on B, B depends_on A."""

    def test_system_overview_reports_broken_reference(self, tmp_project):
        # Inject a cycle into the registry: color-theory depends on design-director,
        # design-director already has color-theory in referenced_by.
        # We make design-director depend on color-theory to close the loop.
        reg_path = tmp_project / "data/registry.json"
        reg = json.loads(reg_path.read_text())
        reg["skills"]["design-director"]["depends_on"] = ["color-theory"]
        reg["skills"]["color-theory"]["depends_on"] = ["design-director"]
        reg_path.write_text(json.dumps(reg))

        # get_system_overview detects broken/circular references via depends_on check
        result = server.get_system_overview()
        # Both skills exist so no "missing" reference — but the overview should complete
        assert "SKILL LIBRARY OVERVIEW" in result

    def test_get_skill_does_not_loop(self, tmp_project):
        # get_skill reads files, not the dependency graph — should complete fine
        result = server.get_skill("color-theory")
        assert "color-theory" in result


class TestConcurrentLogging:
    """Multiple threads writing to the same log file simultaneously."""

    def test_all_events_are_written(self, tmp_project):
        log_path = server.DATA_DIR / "concurrent.jsonl"
        errors = []

        def write_event(i):
            try:
                server._log_event(log_path, {"index": i})
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=write_event, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Exceptions during concurrent write: {errors}"
        events = server._load_log(log_path)
        assert len(events) == 20

    def test_no_partial_json_lines(self, tmp_project):
        log_path = server.DATA_DIR / "concurrent2.jsonl"
        threads = [
            threading.Thread(target=server._log_event, args=(log_path, {"n": i}))
            for i in range(30)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Every line must be valid JSON — no partial writes
        raw_lines = [l for l in log_path.read_text().splitlines() if l.strip()]
        for line in raw_lines:
            json.loads(line)  # raises if malformed


# ---------------------------------------------------------------------------
# update_skill_metadata — referenced_by maintenance
# ---------------------------------------------------------------------------
# Regression tests for the drift bug: changing `parent` via
# update_skill_metadata must keep the denormalized referenced_by index in sync
# on both the old and new parents.


class TestUpdateMetadataReferencedBy:
    def test_reparent_moves_entry_between_referenced_by_lists(self, tmp_project):
        """parent: A → B must remove child from A.referenced_by and append to B.referenced_by."""
        # Seed: add a second director so we have two possible parents
        reg = json.loads((server.REGISTRY_PATH).read_text())
        reg["skills"]["other-director"] = {
            "name": "other-director", "type": "director", "status": "active",
            "description": "Another director for reparenting tests.",
            "location": "skills/design/other-director/SKILL.md",
            "tags": ["domain:design"], "parent": None, "depends_on": [],
            "referenced_by": [], "metrics": {}, "last_modified": "2026-03-01",
            "health_status": "healthy",
        }
        server.REGISTRY_PATH.write_text(json.dumps(reg))

        # color-theory starts with parent=design-director
        result = server.update_skill_metadata("color-theory", parent="other-director")
        assert "parent=other-director" in result

        reg2 = json.loads((server.REGISTRY_PATH).read_text())
        assert reg2["skills"]["color-theory"]["parent"] == "other-director"
        # Old parent loses the back-reference
        assert "color-theory" not in reg2["skills"]["design-director"]["referenced_by"]
        # New parent gains it
        assert "color-theory" in reg2["skills"]["other-director"]["referenced_by"]

    def test_clearing_parent_removes_from_old_referenced_by(self, tmp_project):
        """parent: X → "" must remove child from X.referenced_by."""
        result = server.update_skill_metadata("color-theory", parent="")
        assert "cleared" in result

        reg = json.loads((server.REGISTRY_PATH).read_text())
        assert reg["skills"]["color-theory"]["parent"] is None
        assert "color-theory" not in reg["skills"]["design-director"]["referenced_by"]

    def test_setting_parent_on_orphan_appends_to_new_referenced_by(self, tmp_project):
        """parent: None → X must add child to X.referenced_by."""
        # data-wrangling starts with parent=None
        # Seed a director in data-science to adopt it
        reg = json.loads((server.REGISTRY_PATH).read_text())
        reg["skills"]["ds-director"] = {
            "name": "ds-director", "type": "director", "status": "active",
            "description": "Data science director.",
            "location": "skills/data-science/ds-director/SKILL.md",
            "tags": ["domain:data-science"], "parent": None, "depends_on": [],
            "referenced_by": [], "metrics": {}, "last_modified": "2026-03-01",
            "health_status": "healthy",
        }
        server.REGISTRY_PATH.write_text(json.dumps(reg))

        server.update_skill_metadata("data-wrangling", parent="ds-director")

        reg2 = json.loads((server.REGISTRY_PATH).read_text())
        assert reg2["skills"]["data-wrangling"]["parent"] == "ds-director"
        assert "data-wrangling" in reg2["skills"]["ds-director"]["referenced_by"]

    def test_same_parent_noop_does_not_duplicate(self, tmp_project):
        """Setting parent to its existing value must not duplicate in referenced_by."""
        # color-theory already has parent=design-director, and design-director
        # already has ["color-theory"] in its referenced_by
        server.update_skill_metadata("color-theory", parent="design-director")

        reg = json.loads((server.REGISTRY_PATH).read_text())
        refs = reg["skills"]["design-director"]["referenced_by"]
        assert refs.count("color-theory") == 1, f"duplicated: {refs}"

    def test_unrelated_metadata_update_does_not_touch_referenced_by(self, tmp_project):
        """Changing only health_status/manual_rating/etc must leave referenced_by alone."""
        before = json.loads((server.REGISTRY_PATH).read_text())
        before_refs = dict((n, list(e.get("referenced_by", [])))
                           for n, e in before["skills"].items())

        server.update_skill_metadata("color-theory", health_status="warning")

        after = json.loads((server.REGISTRY_PATH).read_text())
        after_refs = dict((n, list(e.get("referenced_by", [])))
                          for n, e in after["skills"].items())
        assert before_refs == after_refs, "referenced_by drifted on unrelated update"


# ---------------------------------------------------------------------------
# update_skill_metadata — manual health override (preserved across recalibrate)
# ---------------------------------------------------------------------------
# A manual health_status must be recorded as an override (manual_health) so the
# aggressive auto-classifier in recalibrate_scores.py cannot silently undo it.


def _load_recalibrate():
    """Import scripts/recalibrate_scores.py by path (it has no import side effects)."""
    import importlib.util
    import pathlib
    p = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "recalibrate_scores.py"
    spec = importlib.util.spec_from_file_location("recalibrate_scores_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestManualHealthOverride:
    def test_manual_health_records_override_marker(self, tmp_project):
        """Setting health_status writes both health_status and the manual_health marker."""
        result = server.update_skill_metadata("color-theory", health_status="warning")
        assert "manual override" in result
        e = json.loads((server.REGISTRY_PATH).read_text())["skills"]["color-theory"]
        assert e["health_status"] == "warning"
        assert e["manual_health"] == "warning"

    def test_auto_clears_override(self, tmp_project):
        """health_status='auto' clears the manual_health marker."""
        server.update_skill_metadata("color-theory", health_status="critical")
        result = server.update_skill_metadata("color-theory", health_status="auto")
        assert "cleared" in result
        e = json.loads((server.REGISTRY_PATH).read_text())["skills"]["color-theory"]
        assert e["manual_health"] is None

    def test_invalid_health_value_lists_auto(self, tmp_project):
        result = server.update_skill_metadata("color-theory", health_status="bogus")
        assert "must be one of" in result and "auto" in result

    def test_classify_health_preserves_manual_override(self):
        """recalibrate's classifier returns the manual value, ignoring a failing score."""
        rc = _load_recalibrate()
        from datetime import datetime, timezone
        now = datetime(2026, 6, 3, tzinfo=timezone.utc)
        entry = {"manual_health": "healthy", "depends_on": [], "parent": None,
                 "last_modified": "2020-01-01"}
        # composite 10 + never-loaded + stale would normally be "critical"
        assert rc.classify_health("x", entry, 10, {"x": entry}, {}, now) == "healthy"

    def test_classify_health_auto_without_marker(self):
        """Without a manual_health marker, classification is purely automatic."""
        rc = _load_recalibrate()
        from datetime import datetime, timezone
        now = datetime(2026, 6, 3, tzinfo=timezone.utc)
        entry = {"depends_on": [], "parent": None, "last_modified": "2020-01-01"}
        assert rc.classify_health("x", entry, 10, {"x": entry}, {}, now) == "critical"


# ---------------------------------------------------------------------------
# session_id + search-event instrumentation (PR #1)
# ---------------------------------------------------------------------------


class TestSessionInstrumentation:
    def test_session_id_on_usage_event(self, tmp_project):
        server.get_skill("color-theory")
        usage = server._load_log(server.USAGE_LOG)
        # Find the get_skill event (search events also live in usage.jsonl)
        skill_event = next(e for e in usage if e.get("skill") == "color-theory")
        assert skill_event["session_id"] == server._SERVER_SESSION_ID

    def test_session_id_on_gap_event(self, tmp_project):
        server.search_skills("quantum-physics")
        gaps = server._load_log(server.GAPS_LOG)
        assert gaps[0]["session_id"] == server._SERVER_SESSION_ID

    def test_session_id_consistent_across_events(self, tmp_project):
        server.search_skills("quantum-physics")
        server.get_skill("color-theory")
        usage = server._load_log(server.USAGE_LOG)
        gaps = server._load_log(server.GAPS_LOG)
        # All events from one process must share the same session_id
        assert {e["session_id"] for e in usage} == {server._SERVER_SESSION_ID}
        assert {e["session_id"] for e in gaps} == {server._SERVER_SESSION_ID}

    def test_search_logs_to_usage_with_query(self, tmp_project):
        server.search_skills("color")
        usage = server._load_log(server.USAGE_LOG)
        search_events = [e for e in usage if e.get("type") == "search"]
        assert len(search_events) == 1
        assert search_events[0]["query"] == "color"
        assert "result_count" in search_events[0]
        assert search_events[0]["session_id"] == server._SERVER_SESSION_ID

    def test_no_match_search_logs_to_usage(self, tmp_project):
        # No-match path is a separate code branch from keyword-match; verify
        # it also writes a usage event with result_count=0.
        server.search_skills("quantum-physics")
        usage = server._load_log(server.USAGE_LOG)
        search_events = [e for e in usage if e.get("type") == "search"]
        assert len(search_events) == 1
        assert search_events[0]["query"] == "quantum-physics"
        assert search_events[0]["result_count"] == 0

    def test_remote_search_omits_query_text_by_default(self, tmp_project):
        with (
            patch.object(server, "REMOTE_MODE", True),
            patch.dict(os.environ, {}, clear=False),
        ):
            os.environ.pop("TELEMETRY_SEARCH_QUERIES", None)
            server.search_skills("confidential-client-project")

        usage = server._load_log(server.USAGE_LOG)
        gaps = server._load_log(server.GAPS_LOG)
        assert usage[0]["type"] == "search"
        assert usage[0]["result_count"] == 0
        assert "query" not in usage[0]
        assert usage[0]["query_redacted"] is True
        assert gaps[0]["type"] == "search"
        assert "query" not in gaps[0]
        assert gaps[0]["query_redacted"] is True

    def test_remote_search_query_text_can_be_opted_in(self, tmp_project):
        with (
            patch.object(server, "REMOTE_MODE", True),
            patch.dict(os.environ, {"TELEMETRY_SEARCH_QUERIES": "1"}),
        ):
            server.search_skills("explicit-opt-in-query")

        usage = server._load_log(server.USAGE_LOG)
        gaps = server._load_log(server.GAPS_LOG)
        assert usage[0]["query"] == "explicit-opt-in-query"
        assert gaps[0]["query"] == "explicit-opt-in-query"
        assert "query_redacted" not in usage[0]

    def test_cli_remote_mode_uses_privacy_default(self, tmp_project):
        with (
            patch.object(server, "REMOTE_MODE", False),
            patch.dict(os.environ, {}, clear=False),
        ):
            os.environ.pop("TELEMETRY_SEARCH_QUERIES", None)
            server.REMOTE_MODE = True
            server.search_skills("late-cli-remote-mode")

        usage = server._load_log(server.USAGE_LOG)
        assert usage[0]["result_count"] == 0
        assert "query" not in usage[0]

    def test_cli_remote_mode_enables_firestore_mirroring(self):
        with (
            patch.object(server, "REMOTE_MODE", False),
            patch.dict(os.environ, {"TELEMETRY_FIRESTORE": "1"}),
        ):
            assert server._mirror_telemetry_enabled() is False
            server.REMOTE_MODE = True
            assert server._mirror_telemetry_enabled() is True


class TestRuntimeMode:
    @pytest.mark.parametrize("transport", ["sse", "streamable-http"])
    def test_http_transport_forces_remote_mode(self, transport):
        with patch.object(server, "REMOTE_MODE", False):
            assert server._remote_mode_requested(False, transport) is True

    def test_stdio_transport_stays_local_without_remote_flag(self):
        with patch.object(server, "REMOTE_MODE", False):
            assert server._remote_mode_requested(False, "stdio") is False

    def test_remote_flag_restricts_stdio_too(self):
        with patch.object(server, "REMOTE_MODE", False):
            assert server._remote_mode_requested(True, "stdio") is True

    def test_remote_setup_fails_closed_on_removal_error(self):
        fake_mcp = MagicMock()
        fake_mcp.remove_tool.side_effect = RuntimeError("removal failed")
        with (
            patch.object(server, "mcp", fake_mcp),
            patch.object(server, "REMOTE_MODE", False),
            patch.object(server, "_REMOTE_MODE_CONFIGURED", False),
        ):
            with pytest.raises(RuntimeError, match="removal failed"):
                server._enable_remote_mode()
            assert server.REMOTE_MODE is False
            assert server._REMOTE_MODE_CONFIGURED is False

    def test_remote_setup_fails_if_write_tool_survives(self):
        fake_mcp = MagicMock()
        fake_mcp._tool_manager._tools = {"update_skill_content": object()}
        with (
            patch.object(server, "mcp", fake_mcp),
            patch.object(server, "REMOTE_MODE", False),
            patch.object(server, "_REMOTE_MODE_CONFIGURED", False),
        ):
            with pytest.raises(RuntimeError, match="update_skill_content"):
                server._enable_remote_mode()
            assert server.REMOTE_MODE is False

    def test_remote_setup_is_idempotent_after_success(self):
        fake_mcp = MagicMock()
        with (
            patch.object(server, "mcp", fake_mcp),
            patch.object(server, "REMOTE_MODE", False),
            patch.object(server, "_REMOTE_MODE_CONFIGURED", True),
        ):
            server._enable_remote_mode()
            assert server.REMOTE_MODE is True
            fake_mcp.remove_tool.assert_not_called()

    def test_iter_skill_uses_excludes_search_events(self, tmp_project):
        server.search_skills("color")
        server.get_skill("color-theory")
        usage = server._load_log(server.USAGE_LOG)
        # Pre-filter: both events present (verifies search logging is actually
        # happening, not silently broken).
        assert len(usage) == 2
        assert any(e.get("type") == "search" for e in usage)
        import shared
        skill_uses = list(shared.iter_skill_uses(usage))
        # Post-filter: only the get_skill event remains
        assert len(skill_uses) == 1
        assert skill_uses[0]["skill"] == "color-theory"
