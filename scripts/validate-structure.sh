#!/bin/bash
# validate-structure.sh — Structural validation of a skill directory
# Usage: bash validate-structure.sh /path/to/skill-directory/
# Output: JSON with validation results (pass/fail + issues list)

set -euo pipefail

SKILL_DIR="${1:?Usage: validate-structure.sh /path/to/skill-directory/}"
SKILL_DIR="${SKILL_DIR%/}"  # strip trailing slash

SKILL_MD="$SKILL_DIR/SKILL.md"
ISSUES=""
ISSUE_COUNT=0
HAS_CRITICAL="false"

add_issue() {
  local severity="$1"
  local message="$2"
  if [ -n "$ISSUES" ]; then
    ISSUES="$ISSUES, "
  fi
  # Escape the message for JSON
  local escaped_msg
  escaped_msg=$(printf '%s' "$message" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()), end='')" 2>/dev/null || printf '"%s"' "$(printf '%s' "$message" | sed 's/\\/\\\\/g; s/"/\\"/g')")
  ISSUES="$ISSUES{\"severity\": \"$severity\", \"message\": $escaped_msg}"
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
  if [ "$severity" = "critical" ]; then
    HAS_CRITICAL="true"
  fi
}

# Check 1: SKILL.md exists
if [ ! -f "$SKILL_MD" ]; then
  add_issue "critical" "SKILL.md not found in $SKILL_DIR"
  # Can't continue without the file — escape path for JSON output
  ESCAPED_DIR=$(printf '%s' "$SKILL_DIR" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()), end='')" 2>/dev/null || printf '"%s"' "$(printf '%s' "$SKILL_DIR" | sed 's/\\/\\\\/g; s/"/\\"/g')")
  cat <<EOF
{
  "valid": false,
  "skill_directory": $ESCAPED_DIR,
  "issue_count": $ISSUE_COUNT,
  "issues": [$ISSUES]
}
EOF
  exit 1
fi

# Check 2: Frontmatter delimiters
DELIMITER_COUNT=$(awk '/^---$/ { count++ } END { print count+0 }' "$SKILL_MD")
if [ "$DELIMITER_COUNT" -lt 2 ]; then
  add_issue "critical" "Missing YAML frontmatter delimiters (found $DELIMITER_COUNT, need 2)"
fi

# Extract frontmatter for further checks
FRONTMATTER=$(awk '
  /^---$/ { count++; next }
  count == 1 { print }
  count >= 2 { exit }
' "$SKILL_MD")

# Check 3: name field exists
HAS_NAME=$(echo "$FRONTMATTER" | awk '/^name:/ { found=1 } END { print found+0 }')
if [ "$HAS_NAME" -eq 0 ]; then
  add_issue "critical" "Missing 'name' field in frontmatter"
else
  # Check name matches directory name
  SKILL_NAME=$(echo "$FRONTMATTER" | awk -F': *' '/^name:/ { gsub(/["\047]/, "", $2); print $2; exit }')
  DIR_NAME=$(basename "$SKILL_DIR")
  if [ "$SKILL_NAME" != "$DIR_NAME" ]; then
    add_issue "warning" "Skill name '$SKILL_NAME' does not match directory name '$DIR_NAME'"
  fi
fi

# Check 4: description field exists and has content
DESC_TEXT=$(echo "$FRONTMATTER" | awk '
  /^description:/ {
    sub(/^description:[[:space:]]*[>|]?[[:space:]]*/, "")
    if (length($0) > 0) print
    in_desc = 1
    next
  }
  in_desc && /^[a-zA-Z_-]+:/ { exit }
  in_desc { print }
')

DESC_WORDS=$(echo "$DESC_TEXT" | wc -w | tr -d ' ')
if [ "$DESC_WORDS" -eq 0 ]; then
  add_issue "critical" "Missing or empty 'description' field in frontmatter"
elif [ "$DESC_WORDS" -lt 15 ]; then
  add_issue "warning" "Description too short ($DESC_WORDS words, minimum 15)"
elif [ "$DESC_WORDS" -gt 100 ]; then
  add_issue "warning" "Description too long ($DESC_WORDS words, maximum 100)"
fi

# Check 5: description has action verbs
if [ "$DESC_WORDS" -gt 0 ]; then
  HAS_VERB=$(echo "$DESC_TEXT" | tr '[:upper:]' '[:lower:]' | awk '
    /(^|[^a-z])(use|create|build|add|update|fix|analyze|check|run|generate|scaffold|fork|test|export|browse|search|manage|audit|review|optimize)([^a-z]|$)/ { found=1 }
    END { print found+0 }
  ')
  if [ "$HAS_VERB" -eq 0 ]; then
    add_issue "warning" "Description lacks action verbs (use, create, build, analyze, etc.)"
  fi
fi

# Check 6: section count
SECTION_COUNT=$(awk '
  /^```/ { in_code = (in_code == 0) ? 1 : 0; next }
  in_code == 0 && /^## / { count++ }
  END { print count+0 }
' "$SKILL_MD")

if [ "$SECTION_COUNT" -lt 2 ]; then
  add_issue "warning" "Too few sections ($SECTION_COUNT, minimum 2)"
elif [ "$SECTION_COUNT" -gt 8 ]; then
  add_issue "warning" "Too many sections ($SECTION_COUNT, maximum 8)"
fi

# Check 7: body word count
TOTAL_WORDS=$(wc -w < "$SKILL_MD" | tr -d ' ')
FRONTMATTER_WORDS=$(echo "$FRONTMATTER" | wc -w | tr -d ' ')
BODY_WORDS=$((TOTAL_WORDS - FRONTMATTER_WORDS - 2))
if [ "$BODY_WORDS" -lt 0 ]; then BODY_WORDS=0; fi

if [ "$BODY_WORDS" -gt 5000 ]; then
  add_issue "critical" "Body far too large ($BODY_WORDS words, maximum 5000)"
elif [ "$BODY_WORDS" -gt 2000 ]; then
  add_issue "warning" "Body exceeds recommended size ($BODY_WORDS words, recommended under 2000)"
fi

# Check 8: progressive disclosure (large body without references/)
if [ "$BODY_WORDS" -gt 1500 ]; then
  if [ ! -d "$SKILL_DIR/references" ] || [ -z "$(find "$SKILL_DIR/references" -type f ! -name '.gitkeep' 2>/dev/null)" ]; then
    add_issue "warning" "Body is $BODY_WORDS words but no reference files found — consider progressive disclosure"
  fi
fi

# Check 9: # title heading exists
HAS_TITLE=$(awk '
  /^---$/ { count++; next }
  count >= 2 && /^# / { found=1; exit }
  END { print found+0 }
' "$SKILL_MD")

if [ "$HAS_TITLE" -eq 0 ]; then
  add_issue "info" "No # title heading found after frontmatter"
fi

# Determine overall validity (tracked via HAS_CRITICAL boolean in add_issue)
VALID="true"
if [ "$HAS_CRITICAL" = "true" ]; then
  VALID="false"
fi

# Escape directory for JSON
ESCAPED_DIR=$(printf '%s' "$SKILL_DIR" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read()), end='')" 2>/dev/null || printf '"%s"' "$(printf '%s' "$SKILL_DIR" | sed 's/\\/\\\\/g; s/"/\\"/g')")

cat <<EOF
{
  "valid": $VALID,
  "skill_directory": $ESCAPED_DIR,
  "body_words": $BODY_WORDS,
  "section_count": $SECTION_COUNT,
  "description_words": $DESC_WORDS,
  "issue_count": $ISSUE_COUNT,
  "issues": [$ISSUES]
}
EOF
