#!/bin/bash
# ariadne-session-nudge.sh — SessionStart hook: one-line stale-thread nudge.
#
# When a session opens inside a vault configured in ~/.config/ariadne/config.json
# (override: $ARIADNE_CONFIG), this emits a single line of additional context —
# "N stale threads, oldest Xd" — pointing at the ariadne skill for triage.
# The nudge is pull-not-push: it never triages, never blocks, never asks.
#
# Register it in ~/.claude/settings.json, NOT in this repo's .claude/settings.json:
# the vaults are other projects, and a project-scoped hook would never fire there.
#
#   "SessionStart": [{
#     "hooks": [{"type": "command",
#                "command": "[ -f '<repo>/hooks/ariadne-session-nudge.sh' ] && bash '<repo>/hooks/ariadne-session-nudge.sh' || true",
#                "statusMessage": "Checking idea threads..."}]
#   }]
#
# Contract: consumes hook JSON on stdin, ALWAYS exits 0. Silent no-op when the
# config is missing, the cwd is not a configured vault, dependencies are absent,
# or nothing is stale. A nudge must never fail or noise up a session.
#
# Resolves the repo from its own location, so a moved/renamed checkout keeps
# working and a stale registration (path no longer exists) is a silent no-op.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || exit 0
SCANNER="$REPO_ROOT/scripts/ariadne_scan.py"

command -v python3 >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0
[[ -f "$SCANNER" ]] || exit 0
CONFIG="${ARIADNE_CONFIG:-$HOME/.config/ariadne/config.json}"
[[ -f "$CONFIG" ]] || exit 0

INPUT="$(cat 2>/dev/null)"
CWD="$(jq -r '.cwd // empty' <<<"$INPUT" 2>/dev/null)"
[[ -n "$CWD" ]] || CWD="$PWD"

SCAN="$(python3 "$SCANNER" --json --cwd "$CWD" 2>/dev/null)" || exit 0
STALE="$(jq -r '.stale_total // 0' <<<"$SCAN" 2>/dev/null)" || exit 0
[[ "$STALE" =~ ^[0-9]+$ ]] || exit 0
[[ "$STALE" -gt 0 ]] || exit 0
OLDEST="$(jq -r '.oldest_days // 0' <<<"$SCAN" 2>/dev/null)"

jq -n --arg msg "Ariadne: $STALE stale idea thread(s) in this vault (oldest ${OLDEST}d). Load the 'ariadne' skill (skill-library get_skill) or run /ariadne to triage." \
  '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $msg}}' 2>/dev/null

exit 0
