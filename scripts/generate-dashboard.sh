#!/usr/bin/env bash
# Open the skill-infra dashboard in the default browser.
# The dashboard.html file fetches registry.json dynamically,
# so it always shows current data when served via HTTP.
#
# For local file:// access, run a quick server:
#   cd <plugin-dir> && python3 -m http.server 8765
#   open http://localhost:8765/dashboard.html
#
# Usage: generate-dashboard.sh [--serve]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ "${1:-}" = "--serve" ]; then
  echo "Serving dashboard at http://localhost:8765/dashboard.html"
  cd "$PLUGIN_DIR" && python3 -m http.server 8765
else
  echo "Dashboard: $PLUGIN_DIR/dashboard.html"
  echo "Note: Must be served via HTTP (fetch requires it)."
  echo "Run with --serve to start a local server, or:"
  echo "  cd \"$PLUGIN_DIR\" && python3 -m http.server 8765"
  echo "  open http://localhost:8765/dashboard.html"
fi
