"""Static and executable checks for the repo-local Codex marketplace."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE_ROOT = PROJECT_ROOT / "mcp-server" / "codex-marketplace"
MARKETPLACE_JSON = MARKETPLACE_ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_ROOT = MARKETPLACE_ROOT / "plugins" / "skill-library"


def test_marketplace_uses_repo_specific_identity():
    marketplace = json.loads(MARKETPLACE_JSON.read_text())
    assert marketplace["name"] == "skill-building-local"
    assert marketplace["interface"]["displayName"] == "Skill Building Local"


def test_plugin_limits_autoapproval_to_gateway_read_surface():
    config = json.loads((PLUGIN_ROOT / ".mcp.json").read_text())
    server = config["mcpServers"]["skill-library"]
    assert set(server["enabled_tools"]) == {
        "list_skills",
        "search_skills",
        "get_skill",
        "get_skill_details",
        "get_system_overview",
    }
    assert server["default_tools_approval_mode"] == "approve"


def test_gateway_requires_sanitized_search_queries():
    skill = (
        PLUGIN_ROOT / "skills" / "skill-library-gateway" / "SKILL.md"
    ).read_text()
    assert "2-6 generic domain and" in skill
    assert "Never include personal names" in skill
    assert "rather than blindly" in skill


def test_project_updater_check_mode():
    updater = PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh"
    result = subprocess.run(
        ["bash", str(updater), "--check"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "configuration is valid" in result.stdout


def test_project_updater_removes_legacy_installation():
    updater = (
        PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh"
    ).read_text()
    install = "codex plugin add skill-library@skill-building-local --json"
    remove = "codex plugin remove skill-library@personal --json"
    assert install in updater
    assert remove in updater
    assert updater.index(install) < updater.index(remove)


def test_project_updater_uses_collision_safe_cachebuster():
    updater = (
        PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh"
    ).read_text()
    assert "%Y%m%d-%H%M%S-%f" in updater


def test_project_updater_preserves_legacy_plugin_when_install_fails(tmp_path):
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    shutil.copy2(
        PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh",
        project / "scripts" / "update-codex-skill-library.sh",
    )
    shutil.copytree(
        MARKETPLACE_ROOT,
        project / "mcp-server" / "codex-marketplace",
    )
    copied_manifest = (
        project
        / "mcp-server"
        / "codex-marketplace"
        / "plugins"
        / "skill-library"
        / ".codex-plugin"
        / "plugin.json"
    )
    original_manifest = copied_manifest.read_text()

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    call_log = tmp_path / "codex-calls.txt"
    fake_codex = fake_bin / "codex"
    fake_codex.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' \"$*\" >> \"$CODEX_TEST_LOG\"\n"
        "if [ \"$1\" = plugin ] && [ \"$2\" = add ]; then exit 42; fi\n"
        "printf '{}\\n'\n"
    )
    fake_codex.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = str(fake_bin) + os.pathsep + env["PATH"]
    env["CODEX_TEST_LOG"] = str(call_log)
    result = subprocess.run(
        ["bash", str(project / "scripts" / "update-codex-skill-library.sh")],
        cwd=project,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 42
    calls = call_log.read_text()
    assert "plugin add skill-library@skill-building-local --json" in calls
    assert "plugin remove skill-library@skill-building-local --json" in calls
    assert "plugin remove skill-library@personal --json" not in calls
    assert copied_manifest.read_text() == original_manifest


def test_project_updater_rolls_back_unverified_installation(tmp_path):
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    shutil.copy2(
        PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh",
        project / "scripts" / "update-codex-skill-library.sh",
    )
    shutil.copytree(
        MARKETPLACE_ROOT,
        project / "mcp-server" / "codex-marketplace",
    )
    copied_manifest = (
        project
        / "mcp-server"
        / "codex-marketplace"
        / "plugins"
        / "skill-library"
        / ".codex-plugin"
        / "plugin.json"
    )
    original_manifest = copied_manifest.read_text()

    bad_cache = tmp_path / "bad-cache"
    bad_cache.mkdir()
    (bad_cache / "unexpected.txt").write_text("not the plugin")

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    call_log = tmp_path / "codex-calls.txt"
    fake_codex = fake_bin / "codex"
    fake_codex.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' \"$*\" >> \"$CODEX_TEST_LOG\"\n"
        "if [ \"$1\" = plugin ] && [ \"$2\" = add ]; then\n"
        "  printf '{\"pluginId\":\"skill-library@skill-building-local\","
        "\"installedPath\":\"%s\"}\\n' \"$FAKE_INSTALLED_PATH\"\n"
        "else\n"
        "  printf '{}\\n'\n"
        "fi\n"
    )
    fake_codex.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = str(fake_bin) + os.pathsep + env["PATH"]
    env["CODEX_TEST_LOG"] = str(call_log)
    env["FAKE_INSTALLED_PATH"] = str(bad_cache)
    result = subprocess.run(
        ["bash", str(project / "scripts" / "update-codex-skill-library.sh")],
        cwd=project,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    calls = call_log.read_text()
    assert "plugin remove skill-library@skill-building-local --json" in calls
    assert "plugin remove skill-library@personal --json" not in calls
    assert copied_manifest.read_text() == original_manifest


def test_project_updater_accepts_prerelease_with_build_metadata(tmp_path):
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    shutil.copy2(
        PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh",
        project / "scripts" / "update-codex-skill-library.sh",
    )
    shutil.copytree(
        MARKETPLACE_ROOT,
        project / "mcp-server" / "codex-marketplace",
    )
    manifest_path = (
        project
        / "mcp-server"
        / "codex-marketplace"
        / "plugins"
        / "skill-library"
        / ".codex-plugin"
        / "plugin.json"
    )
    manifest = json.loads(manifest_path.read_text())
    manifest["version"] = "1.2.3-beta.1+codex.local-1"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    result = subprocess.run(
        ["bash", str(project / "scripts" / "update-codex-skill-library.sh"), "--check"],
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("version", ["1.2", "1.2.3+", "1.2.3-beta..1"])
def test_project_updater_rejects_invalid_semver(tmp_path, version):
    project = tmp_path / "project"
    (project / "scripts").mkdir(parents=True)
    shutil.copy2(
        PROJECT_ROOT / "scripts" / "update-codex-skill-library.sh",
        project / "scripts" / "update-codex-skill-library.sh",
    )
    shutil.copytree(
        MARKETPLACE_ROOT,
        project / "mcp-server" / "codex-marketplace",
    )
    manifest_path = (
        project
        / "mcp-server"
        / "codex-marketplace"
        / "plugins"
        / "skill-library"
        / ".codex-plugin"
        / "plugin.json"
    )
    manifest = json.loads(manifest_path.read_text())
    manifest["version"] = version
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    result = subprocess.run(
        ["bash", str(project / "scripts" / "update-codex-skill-library.sh"), "--check"],
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0


def test_dashboard_labels_redacted_gap_events():
    dashboard = (PROJECT_ROOT / "app" / "infra.html").read_text()
    assert "Redacted search gap" in dashboard
    assert "e.result_count ?? 0" in dashboard
