#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MARKETPLACE_ROOT="$PROJECT_ROOT/mcp-server/codex-marketplace"
MARKETPLACE_JSON="$MARKETPLACE_ROOT/.agents/plugins/marketplace.json"
PLUGIN_ROOT="$MARKETPLACE_ROOT/plugins/skill-library"
PLUGIN_JSON="$PLUGIN_ROOT/.codex-plugin/plugin.json"
MCP_JSON="$PLUGIN_ROOT/.mcp.json"
GATEWAY_SKILL="$PLUGIN_ROOT/skills/skill-library-gateway/SKILL.md"

CHECK_ONLY=false
if [[ "${1:-}" == "--check" ]]; then
  CHECK_ONLY=true
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--check]" >&2
  exit 2
fi

python3 - "$MARKETPLACE_JSON" "$PLUGIN_JSON" "$MCP_JSON" "$GATEWAY_SKILL" <<'PY'
import json
import re
import sys
from pathlib import Path

marketplace_path, plugin_path, mcp_path, skill_path = map(Path, sys.argv[1:])
for path in (marketplace_path, plugin_path, mcp_path, skill_path):
    if not path.is_file():
        raise SystemExit(f"missing required file: {path}")

marketplace = json.loads(marketplace_path.read_text())
plugin = json.loads(plugin_path.read_text())
mcp = json.loads(mcp_path.read_text())
skill = skill_path.read_text()

if marketplace.get("name") != "skill-building-local":
    raise SystemExit("marketplace name must be skill-building-local")
entries = marketplace.get("plugins", [])
if not any(entry.get("name") == "skill-library" for entry in entries):
    raise SystemExit("marketplace is missing skill-library")
if plugin.get("name") != "skill-library":
    raise SystemExit("plugin name must be skill-library")
semver = re.compile(
    r"\d+\.\d+\.\d+"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
if not semver.fullmatch(plugin.get("version", "")):
    raise SystemExit("plugin version is not valid semver")

server = mcp.get("mcpServers", {}).get("skill-library", {})
expected_tools = {
    "list_skills",
    "search_skills",
    "get_skill",
    "get_skill_details",
    "get_system_overview",
}
if set(server.get("enabled_tools", [])) != expected_tools:
    raise SystemExit("skill-library MCP enabled_tools does not match the read surface")
if server.get("default_tools_approval_mode") != "approve":
    raise SystemExit("skill-library MCP approval mode must be approve")
if "name: skill-library-gateway" not in skill or "[TODO:" in skill:
    raise SystemExit("gateway skill is incomplete")

print("Codex skill-library configuration is valid.")
PY

if [[ "$CHECK_ONLY" == true ]]; then
  exit 0
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI is required to reinstall the plugin" >&2
  exit 1
fi

MANIFEST_BACKUP="$(mktemp "${TMPDIR:-/tmp}/skill-library-plugin.XXXXXX")"
cp "$PLUGIN_JSON" "$MANIFEST_BACKUP"
HAD_CURRENT_INSTALL=false
INSTALL_ATTEMPTED=false
UPDATE_COMMITTED=false

rollback_update() {
  status=$?
  trap - EXIT
  if [[ "$UPDATE_COMMITTED" != true ]]; then
    cp "$MANIFEST_BACKUP" "$PLUGIN_JSON"
    if [[ "$INSTALL_ATTEMPTED" == true ]]; then
      if ! codex plugin remove skill-library@skill-building-local --json >/dev/null 2>&1; then
        echo "warning: failed to remove unverified plugin installation" >&2
      fi
      if [[ "$HAD_CURRENT_INSTALL" == true ]]; then
        if ! codex plugin add skill-library@skill-building-local --json >/dev/null 2>&1; then
          echo "warning: failed to restore previous plugin installation" >&2
        fi
      fi
    fi
  fi
  rm -f "$MANIFEST_BACKUP"
  exit "$status"
}
trap rollback_update EXIT

PLUGIN_LIST="$(codex plugin list)"
if grep -Eq '^skill-library@skill-building-local[[:space:]]+installed,' <<<"$PLUGIN_LIST"; then
  HAD_CURRENT_INSTALL=true
fi

python3 - "$PLUGIN_JSON" <<'PY'
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(sys.argv[1])
plugin = json.loads(path.read_text())
old_version = plugin["version"]
base_version = old_version.split("+", 1)[0]
cachebuster = os.environ.get("CODEX_PLUGIN_CACHEBUSTER")
if cachebuster is None:
    cachebuster = "local-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
if not re.fullmatch(r"[0-9A-Za-z.-]+", cachebuster):
    raise SystemExit("CODEX_PLUGIN_CACHEBUSTER contains unsupported characters")
plugin["version"] = f"{base_version}+codex.{cachebuster}"
path.write_text(json.dumps(plugin, indent=2) + "\n")
print(f"Updated plugin version: {old_version} -> {plugin['version']}")
PY

codex plugin marketplace add "$MARKETPLACE_ROOT" --json
INSTALL_ATTEMPTED=true
INSTALL_JSON="$(codex plugin add skill-library@skill-building-local --json)"
echo "$INSTALL_JSON"

INSTALLED_PATH="$(python3 -c '
import json, sys
data = json.load(sys.stdin)
if data.get("pluginId") != "skill-library@skill-building-local":
    raise SystemExit("unexpected plugin id in installer response")
path = data.get("installedPath")
if not path:
    raise SystemExit("installer response is missing installedPath")
print(path)
' <<<"$INSTALL_JSON")"

if ! diff -qr "$PLUGIN_ROOT" "$INSTALLED_PATH" >/dev/null; then
  echo "installed plugin cache does not match the validated source" >&2
  exit 1
fi

# Remove the legacy identity only after the replacement is installed and its
# cached contents have been verified. The command is safe when already absent.
codex plugin remove skill-library@personal --json >/dev/null 2>&1
echo "Cleared legacy plugin entry (safe if absent): skill-library@personal"

UPDATE_COMMITTED=true
echo "Start a new Codex task to load the updated plugin."
