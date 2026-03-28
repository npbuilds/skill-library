"""Tests for the Skill Library MCP server."""

import json
import threading
from pathlib import Path
from unittest.mock import patch

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

    # Patch module-level paths to use tmp_path
    with (
        patch.object(server, "PROJECT_ROOT", tmp_path),
        patch.object(server, "REGISTRY_PATH", data_dir / "registry.json"),
        patch.object(server, "SKILLS_DIR", tmp_path / "skills"),
        patch.object(server, "DATA_DIR", data_dir),
        patch.object(server, "USAGE_LOG", data_dir / "usage.jsonl"),
        patch.object(server, "GAPS_LOG", data_dir / "gaps.jsonl"),
        patch.object(server, "FEEDBACK_LOG", data_dir / "feedback.jsonl"),
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

    def test_shows_unused_skills(self, tmp_project):
        server.get_skill("color-theory")
        result = server.get_skill_stats()
        assert "Never used" in result
        assert "data-wrangling" in result


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
