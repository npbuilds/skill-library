#!/bin/bash
# skill-file-watcher.sh — Auto health check + registry notification on SKILL.md changes
# Triggered by Claude Code PostToolUse hook when a SKILL.md file is written
# Usage: bash hooks/skill-file-watcher.sh /path/to/SKILL.md
#
# This hook:
# 1. Validates the skill's structure
# 2. Computes fresh metrics via analyze-skill.sh
# 3. Outputs a summary notification for the user
#
# Registry updates are handled by the skill-registry skill itself (not this hook)
# to keep the hook fast and avoid complex JSON manipulation in bash.

set -euo pipefail

SKILL_PATH="${1:?Usage: skill-file-watcher.sh /path/to/SKILL.md}"

# Resolve the plugin root (this script lives in hooks/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_DIR=$(dirname "$SKILL_PATH")
SKILL_NAME=$(basename "$SKILL_DIR")

# Step 1: Structural validation
VALIDATION=$(bash "$PLUGIN_ROOT/scripts/validate-structure.sh" "$SKILL_DIR" 2>/dev/null) || true

VALID=$(echo "$VALIDATION" | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    print('true' if data.get('valid', False) else 'false')
except:
    print('false')
" 2>/dev/null || echo "false")

ISSUE_COUNT=$(echo "$VALIDATION" | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    print(data.get('issue_count', 0))
except:
    print(0)
" 2>/dev/null || echo "0")

# Step 2: Compute metrics
METRICS=$(bash "$PLUGIN_ROOT/scripts/analyze-skill.sh" "$SKILL_PATH" 2>/dev/null) || true

BODY_WORDS=$(echo "$METRICS" | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    print(data.get('body_words', '?'))
except:
    print('?')
" 2>/dev/null || echo "?")

EST_TOKENS=$(echo "$METRICS" | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    print(data.get('estimated_tokens_total', '?'))
except:
    print('?')
" 2>/dev/null || echo "?")

# Step 3: Determine health status from metrics
HEALTH="healthy"
if [ "$BODY_WORDS" != "?" ]; then
  if [ "$BODY_WORDS" -gt 8000 ]; then
    HEALTH="critical"
  elif [ "$BODY_WORDS" -gt 5000 ]; then
    HEALTH="warning"
  fi
fi

if [ "$VALID" = "false" ]; then
  HEALTH="critical"
fi

# Step 4: Output notification
case "$HEALTH" in
  healthy)
    echo "✓ $SKILL_NAME — healthy ($BODY_WORDS words, ~$EST_TOKENS tokens)"
    ;;
  warning)
    echo "⚠ $SKILL_NAME — warning ($BODY_WORDS words, ~$EST_TOKENS tokens, $ISSUE_COUNT issues)"
    ;;
  critical)
    echo "✗ $SKILL_NAME — CRITICAL ($BODY_WORDS words, ~$EST_TOKENS tokens, $ISSUE_COUNT issues)"
    echo "  Run: bash scripts/validate-structure.sh \"$SKILL_DIR\" for details"
    ;;
esac

# Remind about registry sync if this is an existing skill
if [ -f "$PLUGIN_ROOT/data/registry.json" ]; then
  HAS_ENTRY=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    reg = json.load(f)
print('true' if sys.argv[2] in reg.get('skills', {}) else 'false')
" "$PLUGIN_ROOT/data/registry.json" "$SKILL_NAME" 2>/dev/null || echo "false")

  if [ "$HAS_ENTRY" = "true" ]; then
    # Auto-refresh registry metrics for this skill
    bash "$PLUGIN_ROOT/scripts/refresh-registry.sh" "$SKILL_NAME" && \
      echo "  Registry metrics refreshed for $SKILL_NAME" || \
      echo "  Registry refresh failed for $SKILL_NAME — run: bash scripts/refresh-registry.sh $SKILL_NAME"
  else
    # Auto-register new skills to prevent registry drift
    python3 "$PLUGIN_ROOT/scripts/sync-registry.py" --apply 2>/dev/null && \
      echo "  Auto-registered $SKILL_NAME in registry" || \
      echo "  Auto-register failed — run: python3 scripts/sync-registry.py --apply"
  fi
fi
