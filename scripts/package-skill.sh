#!/usr/bin/env bash
# Existing entry point retained for callers; metadata and file handling use Python.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/package_skill.py" "$@"
