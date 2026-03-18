#!/bin/bash
# compute-tokens.sh — Detailed token breakdown for a skill directory
# Usage: bash compute-tokens.sh /path/to/skill-directory/
# Output: JSON with per-file and aggregate token estimates

set -euo pipefail

SKILL_DIR="${1:?Usage: compute-tokens.sh /path/to/skill-directory/}"
SKILL_DIR="${SKILL_DIR%/}"  # strip trailing slash

SKILL_MD="$SKILL_DIR/SKILL.md"
if [ ! -f "$SKILL_MD" ]; then
  echo "{\"error\": \"SKILL.md not found in $SKILL_DIR\"}" >&2
  exit 1
fi

# Estimate tokens for a single file (~4 chars per token)
estimate_tokens() {
  local file="$1"
  local chars
  chars=$(wc -c < "$file" | tr -d ' ')
  echo $((chars / 4))
}

# Extract description tokens (always-loaded metadata cost)
FRONTMATTER=$(awk '
  /^---$/ { count++; next }
  count == 1 { print }
  count >= 2 { exit }
' "$SKILL_MD")

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

META_TOKENS=$(( (DESC_WORDS * 13 + 9) / 10 ))

# Body tokens: count only the body (after frontmatter), not the full file
BODY_CHARS=$(awk '
  /^---$/ { count++; next }
  count >= 2 { print }
' "$SKILL_MD" | wc -c | tr -d ' ')
BODY_TOKENS=$((BODY_CHARS / 4))

# Compute tokens for each subdirectory
compute_dir_tokens() {
  local dir="$1"
  local total=0
  local file_details=""

  if [ ! -d "$dir" ]; then
    echo "0|"
    return
  fi

  while IFS= read -r -d '' file; do
    local tokens
    tokens=$(estimate_tokens "$file")
    local rel_path="${file#"$SKILL_DIR/"}"
    total=$((total + tokens))
    if [ -n "$file_details" ]; then
      file_details="$file_details, "
    fi
    # Escape the filename for JSON
    local escaped_name
    escaped_name=$(printf '%s' "$rel_path" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()), end='')" 2>/dev/null || printf '"%s"' "$rel_path")
    file_details="$file_details{\"file\": $escaped_name, \"tokens\": $tokens}"
  done < <(find "$dir" -type f ! -name '.gitkeep' -print0 2>/dev/null)

  echo "$total|$file_details"
}

REF_RESULT=$(compute_dir_tokens "$SKILL_DIR/references")
REF_TOKENS="${REF_RESULT%%|*}"
REF_FILES="${REF_RESULT#*|}"

EXAMPLE_RESULT=$(compute_dir_tokens "$SKILL_DIR/examples")
EXAMPLE_TOKENS="${EXAMPLE_RESULT%%|*}"
EXAMPLE_FILES="${EXAMPLE_RESULT#*|}"

SCRIPT_RESULT=$(compute_dir_tokens "$SKILL_DIR/scripts")
SCRIPT_TOKENS="${SCRIPT_RESULT%%|*}"
SCRIPT_FILES="${SCRIPT_RESULT#*|}"

TEMPLATE_RESULT=$(compute_dir_tokens "$SKILL_DIR/templates")
TEMPLATE_TOKENS="${TEMPLATE_RESULT%%|*}"
TEMPLATE_FILES="${TEMPLATE_RESULT#*|}"

TOTAL_ALL=$((META_TOKENS + BODY_TOKENS + REF_TOKENS + EXAMPLE_TOKENS + SCRIPT_TOKENS + TEMPLATE_TOKENS))

# Escape skill dir for JSON
ESCAPED_DIR=$(printf '%s' "$SKILL_DIR" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()), end='')" 2>/dev/null || printf '"%s"' "$SKILL_DIR")

cat <<EOF
{
  "skill_directory": $ESCAPED_DIR,
  "summary": {
    "metadata_tokens": $META_TOKENS,
    "body_tokens": $BODY_TOKENS,
    "reference_tokens": $REF_TOKENS,
    "example_tokens": $EXAMPLE_TOKENS,
    "script_tokens": $SCRIPT_TOKENS,
    "template_tokens": $TEMPLATE_TOKENS,
    "total_tokens": $TOTAL_ALL
  },
  "progressive_disclosure": {
    "always_loaded": $META_TOKENS,
    "on_trigger": $((META_TOKENS + BODY_TOKENS)),
    "full_load": $TOTAL_ALL
  },
  "files": {
    "references": [$REF_FILES],
    "examples": [$EXAMPLE_FILES],
    "scripts": [$SCRIPT_FILES],
    "templates": [$TEMPLATE_FILES]
  }
}
EOF
