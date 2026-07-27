#!/bin/bash
# pre-commit-stray-check.sh — Reject commits with unexpected files at project root
# Allowlisted: repository metadata, config files, dotfiles, Dockerfile
set -euo pipefail

# Files allowed at root (exact match)
ALLOWED_ROOT_FILES=(
  "CLAUDE\.md"
  "AGENTS\.md"
  "README\.md"
  "LICENSE"
  "Dockerfile"
  "\.dockerignore"
  "\.gitignore"
  "\.DS_Store"
)

# Build grep pattern from allowlist (dots already escaped above)
ALLOW_PATTERN=$(printf "|%s" "${ALLOWED_ROOT_FILES[@]}")
ALLOW_PATTERN="${ALLOW_PATTERN:1}"  # strip leading pipe

# Get staged files that are at the root level (no / in path)
STRAY_FILES=$(git diff --cached --name-only --diff-filter=ACR | grep -v '/' | grep -Ev "^(${ALLOW_PATTERN})$" || true)

if [ -n "$STRAY_FILES" ]; then
  echo "ERROR: Stray files detected at project root:"
  echo ""
  while IFS= read -r f; do echo "  - $f"; done <<< "$STRAY_FILES"
  echo ""
  echo "Move these into the correct directory. See CLAUDE.md for file placement rules."
  echo "To bypass (rare): git commit --no-verify"
  exit 1
fi

# Machinery-only leak guard (private term list; see hooks/leak-guard.sh).
top="$(git rev-parse --show-toplevel)"
if [ -x "$top/hooks/leak-guard.sh" ]; then
  "$top/hooks/leak-guard.sh" staged || exit 1
else
  echo "leak-guard: hooks/leak-guard.sh missing in this checkout — pull main. CI is the backstop." >&2
fi
