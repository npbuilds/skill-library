#!/bin/bash
# lint-structure.sh — Audit project for misplaced files
# Usage: bash scripts/lint-structure.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

ISSUES=0

# Count non-empty lines (immune to trailing-newline overcounting)
count_lines() { echo "$1" | grep -c . 2>/dev/null || echo 0; }

# Check 1: Unexpected files at root (skip gitignored files, explicit dotfile allowlist)
echo "=== Root-level file check ==="
STRAYS=""
while IFS= read -r f; do
  base=$(basename "$f")
  rel="${f#"$PROJECT_ROOT"/}"
  # Explicit allowlist (no catch-all for dotfiles — .env etc. should be caught)
  case "$base" in
    AGENTS.md|CLAUDE.md|README.md|Dockerfile|.git|.gitignore|.dockerignore|.DS_Store) continue ;;
  esac
  # Skip gitignored files (use relative path for reliability)
  if git -C "$PROJECT_ROOT" check-ignore -q "$rel" 2>/dev/null; then
    continue
  fi
  STRAYS="${STRAYS}${base}"$'\n'
done < <(find "$PROJECT_ROOT" -maxdepth 1 -type f)
STRAYS=$(echo "$STRAYS" | sed '/^$/d')

if [ -n "$STRAYS" ]; then
  echo "WARN: Stray files at project root:"
  while IFS= read -r f; do echo "  - $f"; done <<< "$STRAYS"
  ISSUES=$((ISSUES + $(count_lines "$STRAYS")))
else
  echo "  OK — no stray files at root"
fi

# Check 2: HTML files outside output/ or archon-briefings/
echo ""
echo "=== HTML file location check ==="
BAD_HTML=$(find "$PROJECT_ROOT" -maxdepth 1 -name '*.html' -type f || true)
if [ -n "$BAD_HTML" ]; then
  echo "WARN: HTML files at root (should be in output/visualizations/ or archon-briefings/):"
  while IFS= read -r f; do echo "  - $(basename "$f")"; done <<< "$BAD_HTML"
  ISSUES=$((ISSUES + $(count_lines "$BAD_HTML")))
else
  echo "  OK — no stray HTML files"
fi

# Check 3: Log files anywhere in tracked files
echo ""
echo "=== Log file check ==="
TRACKED_LOGS=$(cd "$PROJECT_ROOT" && git ls-files -- '*.log' 2>/dev/null || true)
if [ -n "$TRACKED_LOGS" ]; then
  echo "WARN: Log files tracked in git (should be gitignored):"
  while IFS= read -r f; do echo "  - $f"; done <<< "$TRACKED_LOGS"
  ISSUES=$((ISSUES + $(count_lines "$TRACKED_LOGS")))
else
  echo "  OK — no log files tracked"
fi

# Check 4: Data files at root
echo ""
echo "=== Data file check ==="
ROOT_DATA=$(find "$PROJECT_ROOT" -maxdepth 1 \( -name '*.json' -o -name '*.jsonl' -o -name '*.csv' \) -type f || true)
if [ -n "$ROOT_DATA" ]; then
  echo "WARN: Data files at root (should be in data/):"
  while IFS= read -r f; do echo "  - $(basename "$f")"; done <<< "$ROOT_DATA"
  ISSUES=$((ISSUES + $(count_lines "$ROOT_DATA")))
else
  echo "  OK — no stray data files"
fi

echo ""
if [ "$ISSUES" -gt 0 ]; then
  echo "Found $ISSUES issue(s). See CLAUDE.md for file placement rules."
  exit 1
else
  echo "All clear — no structural issues found."
fi
