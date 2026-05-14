#!/bin/bash
# spelunker-trigger.sh — UserPromptSubmit hook that detects research-flavored prompts
# and surfaces a system note suggesting /spelunker.
#
# Triggered by Claude Code UserPromptSubmit hook. Reads JSON from stdin with
# {"prompt": "<user text>"} and emits {"hookSpecificOutput": {...}} if matched.
#
# Trigger phrases mirror the auto-trigger contract in CLAUDE.md.
# Guards:
#   - Skips slash commands (already explicit user intent)
#   - Skips very short prompts (< 12 chars — too thin to be a research question)
#   - Skips prompts with negative signals ("just", "quick", "simple") that suggest
#     the user wants a one-shot answer, not deep research

set -euo pipefail

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""' 2>/dev/null || echo "")

# Guard 1: skip empty
[[ -z "$PROMPT" ]] && exit 0

# Guard 2: skip slash commands
[[ "$PROMPT" =~ ^/ ]] && exit 0

# Guard 3: skip very short prompts
[[ ${#PROMPT} -lt 12 ]] && exit 0

# Lowercase once for matching
LC=$(echo "$PROMPT" | tr '[:upper:]' '[:lower:]')

# Guard 4: skip if user signals they want quick/cheap answer
if echo "$LC" | grep -qE '\b(just|quick|simple|simply|tldr|tl;dr|in short|briefly)\b'; then
  exit 0
fi

# Match trigger phrases (mirrors CLAUDE.md Auto-Trigger Skills section)
MATCHED=""
if echo "$LC" | grep -qE '\b(research|investigate|verify|fact-check|fact check|look into|dig into|deep dive|deep-dive)\b'; then
  MATCHED="explicit"
elif echo "$LC" | grep -qE '(what does the evidence say|help me understand|is .* true|what caused|why does|why did|how come)'; then
  MATCHED="inquiry"
elif echo "$LC" | grep -qE "(what'?s the best|how should we (design|build|approach)|what are the options for|comprehensive analysis)"; then
  MATCHED="generative"
elif echo "$LC" | grep -qE '(i need to be sure|this is for a decision|critical decision|must be right|must be correct)'; then
  MATCHED="depth-cue"
fi

[[ -z "$MATCHED" ]] && exit 0

# Emit advisory system note. Non-blocking — Claude can still ignore.
jq -n --arg msg "Spelunker auto-trigger matched ($MATCHED). Consider invoking \`/spelunker\` for this question — see CLAUDE.md Auto-Trigger Skills section. If a single web search is enough, ignore this hint." '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: $msg
  }
}'
