#!/bin/bash
# analyze-skill.sh — Compute metrics for a single SKILL.md file
# Usage: bash analyze-skill.sh /path/to/SKILL.md
# Output: JSON object with computed metrics

set -euo pipefail

SKILL_PATH="${1:?Usage: analyze-skill.sh /path/to/SKILL.md}"
SKILL_DIR=$(dirname "$SKILL_PATH")

if [ ! -f "$SKILL_PATH" ]; then
  echo "{\"error\": \"File not found: $SKILL_PATH\"}" >&2
  exit 1
fi

# Total word count
TOTAL_WORDS=$(wc -w < "$SKILL_PATH" | tr -d ' ')

# Extract frontmatter using awk (portable across macOS/Linux)
FRONTMATTER=$(awk '
  /^---$/ { count++; next }
  count == 1 { print }
  count >= 2 { exit }
' "$SKILL_PATH")
FRONTMATTER_WORDS=$(echo "$FRONTMATTER" | wc -w | tr -d ' ')

# Body words (total minus frontmatter minus the two --- lines)
BODY_WORDS=$((TOTAL_WORDS - FRONTMATTER_WORDS - 2))
if [ "$BODY_WORDS" -lt 0 ]; then BODY_WORDS=0; fi

# Section count (## headings, excluding those inside fenced code blocks)
SECTION_COUNT=$(awk '
  /^```/ { in_code = (in_code == 0) ? 1 : 0; next }
  in_code == 0 && /^## / { count++ }
  END { print count+0 }
' "$SKILL_PATH")

# Extract description from frontmatter (handles multi-line YAML descriptions)
DESC_WORDS=$(echo "$FRONTMATTER" | awk '
  /^description:/ {
    sub(/^description:[[:space:]]*[>|]?[[:space:]]*/, "")
    if (length($0) > 0) print
    in_desc = 1
    next
  }
  in_desc && /^[a-zA-Z_-]+:/ { exit }
  in_desc { print }
' | wc -w | tr -d ' ')

# Count files in subdirectories.
# Mirrors sync-registry.py: count only git-tracked files so local untracked
# files don't inflate metrics and drift against CI's clean checkout.
count_files() {
  local dir="$1"
  if [ ! -d "$dir" ]; then
    echo 0
    return
  fi
  if git -C "$dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git -C "$dir" ls-files -- . 2>/dev/null \
      | grep -Ev '(^|/)\.gitkeep$' \
      | wc -l | tr -d ' '
  else
    # Not in a git repo (e.g., tarball extract) — fall back to raw count.
    find "$dir" -type f ! -name '.gitkeep' | wc -l | tr -d ' '
  fi
}

REF_COUNT=$(count_files "$SKILL_DIR/references")
EXAMPLE_COUNT=$(count_files "$SKILL_DIR/examples")
SCRIPT_COUNT=$(count_files "$SKILL_DIR/scripts")
TEMPLATE_COUNT=$(count_files "$SKILL_DIR/templates")

# Token estimation (~4 chars per token) — body only, excluding frontmatter
BODY_CHARS=$(awk '
  /^---$/ { count++; next }
  count >= 2 { print }
' "$SKILL_PATH" | wc -c | tr -d ' ')
EST_TOKENS_BODY=$((BODY_CHARS / 4))

# Metadata tokens: description is always loaded (~1.3 tokens per word for natural language)
META_TOKENS=$(( (DESC_WORDS * 13 + 9) / 10 ))

# Total estimated tokens
EST_TOKENS_TOTAL=$((META_TOKENS + EST_TOKENS_BODY))

# Extract name from frontmatter
SKILL_NAME=$(echo "$FRONTMATTER" | awk -F': *' '/^name:/ { gsub(/["\047]/, "", $2); print $2; exit }')
if [ -z "$SKILL_NAME" ]; then
  SKILL_NAME=$(basename "$SKILL_DIR")
fi

# Escape strings for safe JSON output (handle ", \, and control chars)
json_escape() {
  printf '%s' "$1" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()), end='')" 2>/dev/null \
    || printf '"%s"' "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"
}

# Output JSON
ESCAPED_NAME=$(json_escape "$SKILL_NAME")
ESCAPED_PATH=$(json_escape "$SKILL_PATH")

cat <<EOF
{
  "name": $ESCAPED_NAME,
  "path": $ESCAPED_PATH,
  "word_count": $TOTAL_WORDS,
  "body_words": $BODY_WORDS,
  "description_words": $DESC_WORDS,
  "section_count": $SECTION_COUNT,
  "reference_files": $REF_COUNT,
  "example_files": $EXAMPLE_COUNT,
  "script_files": $SCRIPT_COUNT,
  "template_files": $TEMPLATE_COUNT,
  "estimated_tokens_metadata": $META_TOKENS,
  "estimated_tokens_body": $EST_TOKENS_BODY,
  "estimated_tokens_total": $EST_TOKENS_TOTAL
}
EOF
