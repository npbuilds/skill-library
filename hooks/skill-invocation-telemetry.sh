#!/bin/bash
# skill-invocation-telemetry.sh — PostToolUse hook: record native Skill loads.
#
# Claude Code's Skill tool and slash commands bypass the skill-library MCP
# server, so those loads never reached data/usage.jsonl. This hook closes that
# gap by piping the PostToolUse payload into scripts/log_skill_invocation.py.
#
# Register it in ~/.claude/settings.json, NOT in this repo's .claude/settings.json:
# plugin skills are invoked from other projects (the biopharma-vault /diligence
# runs, Hermes strategist loads), and a project-scoped hook only fires inside
# this repo. Registering it in both places would double-count.
#
#   "PostToolUse": [{
#     "matcher": "Skill",
#     "hooks": [{"type": "command",
#                "command": "bash '<repo>/hooks/skill-invocation-telemetry.sh'"}]
#   }]
#
# Contract: consumes hook JSON on stdin, ALWAYS exits 0. A telemetry write must
# never fail the user's tool call, and a hook that exits non-zero surfaces a
# warning in every session it fires.
#
# Resolves the repo from its own location, so a moved/renamed checkout keeps
# working and a stale registration (path no longer exists) is a silent no-op.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 0
SCRIPT="$REPO_ROOT/scripts/log_skill_invocation.py"

[[ -f "$SCRIPT" ]] || exit 0

SKILL_LIBRARY_ROOT="$REPO_ROOT" python3 "$SCRIPT" >/dev/null 2>&1

exit 0
