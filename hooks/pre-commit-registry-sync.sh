#!/bin/bash
# pre-commit-registry-sync.sh — Block commits that would leave data/registry.json
# out of sync with on-disk SKILL.md metrics, so drift is caught locally before CI.
#
# Fires only when staged changes could affect the registry: registry.json itself,
# any SKILL.md, or files under skills/**/{references,examples,scripts,templates}.
set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

STAGED=$(git diff --cached --name-only --diff-filter=ACMR)

# Only run the (relatively expensive) sync if staged files could affect metrics.
if ! echo "$STAGED" | grep -Eq \
  '^(data/registry\.json|skills/.*/SKILL\.md|skills/.*/(references|examples|scripts|templates)/)'; then
  exit 0
fi

output=$(python3 "$REPO_ROOT/scripts/sync-registry.py" 2>&1) || true

if echo "$output" | grep -q "Registry is in sync"; then
  exit 0
fi

echo "ERROR: data/registry.json is out of sync with on-disk SKILL.md files."
echo ""
echo "--- sync-registry.py dry-run tail ---"
echo "$output" | tail -20
echo "-------------------------------------"
echo ""
echo "Fix: python3 scripts/sync-registry.py --apply && git add data/registry.json"
echo "To bypass (rare): git commit --no-verify"
exit 1
