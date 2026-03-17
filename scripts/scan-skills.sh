#!/bin/bash
# scan-skills.sh — Find all SKILL.md files across Claude Code directories
# Usage: bash scan-skills.sh [additional_dirs...]
# Output: Newline-delimited list of absolute paths to SKILL.md files

set -euo pipefail

# Default scan locations
SCAN_DIRS=(
  "$HOME/.claude/plugins/cache"
  "$HOME/.claude/plugins/marketplaces"
  "$HOME/.claude/skills"
)

# Add any additional directories passed as arguments
for dir in "$@"; do
  SCAN_DIRS+=("$dir")
done

# Find all SKILL.md files, output absolute paths
for dir in "${SCAN_DIRS[@]}"; do
  if [ -d "$dir" ]; then
    find "$dir" -name "SKILL.md" -type f 2>/dev/null
  fi
done | sort -u
