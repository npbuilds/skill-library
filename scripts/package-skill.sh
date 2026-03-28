#!/usr/bin/env bash
# Package a skill directory into a portable export bundle.
# Usage: package-skill.sh <skill-dir> [output-dir]
# Output: Creates <output-dir>/<skill-name>-export/ with SKILL.md, references/, manifest.json, README.md

set -euo pipefail

SKILL_DIR="${1:?Usage: package-skill.sh <skill-dir> [output-dir]}"
OUTPUT_DIR="${2:-./exports}"

# Validate input
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "ERROR: $SKILL_DIR/SKILL.md not found" >&2
  exit 1
fi

SKILL_NAME=$(basename "$SKILL_DIR")
EXPORT_DIR="$OUTPUT_DIR/${SKILL_NAME}-export"

# Resolve paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGIN_VERSION="unknown"
if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
  PLUGIN_VERSION=$(python3 -c "import json, sys; print(json.load(open(sys.argv[1]))['version'])" "$PLUGIN_DIR/.claude-plugin/plugin.json" 2>/dev/null || echo "unknown")
fi

# Get metrics
METRICS_JSON=$("$SCRIPT_DIR/analyze-skill.sh" "$SKILL_DIR/SKILL.md" 2>/dev/null)
if [ -z "$METRICS_JSON" ]; then
  echo "ERROR: Failed to analyze $SKILL_DIR/SKILL.md" >&2
  exit 1
fi

# Clean and create export directory (rm first to avoid cp -r nesting on re-runs)
rm -rf "$EXPORT_DIR"
mkdir -p "$EXPORT_DIR"

# Copy SKILL.md
cp "$SKILL_DIR/SKILL.md" "$EXPORT_DIR/SKILL.md"

# Copy references/ if it exists
if [ -d "$SKILL_DIR/references" ]; then
  cp -r "$SKILL_DIR/references" "$EXPORT_DIR/references"
fi

# Copy templates/ if it exists
if [ -d "$SKILL_DIR/templates" ]; then
  cp -r "$SKILL_DIR/templates" "$EXPORT_DIR/templates"
fi

# Copy examples/ if it exists
if [ -d "$SKILL_DIR/examples" ]; then
  cp -r "$SKILL_DIR/examples" "$EXPORT_DIR/examples"
fi

# Extract metadata for manifest
DESCRIPTION=$(awk '
  BEGIN { in_fm=0; in_desc=0; desc="" }
  /^---$/ { in_fm = (in_fm == 0) ? 1 : 0; if (in_fm == 0) exit; next }
  in_fm && /^description:/ {
    in_desc=1
    sub(/^description:[[:space:]]*[>|]?[[:space:]]*/, "")
    if (length($0) > 0) desc = desc " " $0
    next
  }
  in_fm && in_desc && /^[[:space:]]/ {
    sub(/^[[:space:]]+/, "")
    desc = desc " " $0
    next
  }
  in_fm && in_desc && !/^[[:space:]]/ { in_desc=0 }
  END { sub(/^ /, "", desc); print desc }
' "$SKILL_DIR/SKILL.md")

BODY_WORDS=$(echo "$METRICS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['body_words'])" 2>/dev/null)
if [ -z "$BODY_WORDS" ]; then
  echo "ERROR: Failed to parse body_words from metrics" >&2
  exit 1
fi
EST_TOKENS=$(echo "$METRICS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['estimated_tokens_total'])" 2>/dev/null)
if [ -z "$EST_TOKENS" ]; then
  echo "ERROR: Failed to parse estimated_tokens_total from metrics" >&2
  exit 1
fi

# Generate manifest.json
EXPORT_DATE=$(date +%Y-%m-%d)
python3 -c "
import json, sys

manifest = {
    'format_version': 1,
    'skill': {
        'name': sys.argv[1],
        'version': '1.0.0',
        'description': sys.argv[2],
        'type': 'action',
        'source': 'custom'
    },
    'metrics': {
        'body_words': int(sys.argv[3]),
        'estimated_tokens_total': int(sys.argv[4]),
        'auto_score': 0
    },
    'dependencies': {
        'depends_on': [],
        'required_scripts': [],
        'required_data': []
    },
    'exported_from': {
        'plugin': 'skill-infra',
        'plugin_version': sys.argv[5],
        'export_date': sys.argv[6]
    }
}
print(json.dumps(manifest, indent=2))
" "$SKILL_NAME" "$DESCRIPTION" "$BODY_WORDS" "$EST_TOKENS" "$PLUGIN_VERSION" "$EXPORT_DATE" > "$EXPORT_DIR/manifest.json"

# Generate README.md
cat > "$EXPORT_DIR/README.md" << READMEEOF
# $SKILL_NAME

$DESCRIPTION

## Installation

Copy this directory to your \`skills/\` folder:

\`\`\`bash
cp -r ${SKILL_NAME}-export/ ~/.claude/skills/$SKILL_NAME/
\`\`\`

## Metrics

- Body words: $BODY_WORDS
- Estimated tokens: $EST_TOKENS

## Exported

- From: skill-infra v$PLUGIN_VERSION
- Date: $(date +%Y-%m-%d)
READMEEOF

# Count files
FILE_COUNT=$(find "$EXPORT_DIR" -type f | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh "$EXPORT_DIR" 2>/dev/null | cut -f1 | tr -d ' ')

python3 -c "
import json, sys
print(json.dumps({
    'skill': sys.argv[1],
    'export_dir': sys.argv[2],
    'files': int(sys.argv[3]),
    'size': sys.argv[4]
}))
" "$SKILL_NAME" "$EXPORT_DIR" "$FILE_COUNT" "$TOTAL_SIZE"
