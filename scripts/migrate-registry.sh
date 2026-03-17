#!/bin/bash
# migrate-registry.sh — Run pending registry schema migrations
# Usage: bash migrate-registry.sh /path/to/data/
# Reads schema_version from registry.json and applies any newer migrations

set -euo pipefail

DATA_DIR="${1:?Usage: migrate-registry.sh /path/to/data/}"
DATA_DIR="${DATA_DIR%/}"  # strip trailing slash
REGISTRY="$DATA_DIR/registry.json"
MIGRATIONS_DIR="$DATA_DIR/migrations"

if [ ! -f "$REGISTRY" ]; then
  echo "Error: Registry not found at $REGISTRY" >&2
  exit 1
fi

if [ ! -d "$MIGRATIONS_DIR" ]; then
  echo "No migrations directory found. Nothing to do."
  exit 0
fi

# Read current schema version (pass path via argument to avoid injection)
CURRENT_VERSION=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
print(data.get('schema_version', 1))
" "$REGISTRY" 2>/dev/null || echo 1)

echo "Current registry schema version: $CURRENT_VERSION"

# Find and run pending migrations
# Loop until no more migrations match, to handle chained migrations correctly
APPLIED=0
FOUND_MIGRATION=true

while $FOUND_MIGRATION; do
  FOUND_MIGRATION=false

  # Look for a migration matching the current version
  # Quote the directory but leave the glob unquoted so shell expands it
  for migration in "$MIGRATIONS_DIR"/v"${CURRENT_VERSION}"_to_v*.sh; do
    [ -f "$migration" ] || continue

    BASENAME=$(basename "$migration")
    TO_VER=$(echo "$BASENAME" | sed 's/v[0-9]*_to_v\([0-9]*\)\.sh/\1/')

    echo "Applying migration: $BASENAME (v$CURRENT_VERSION → v$TO_VER)"
    bash "$migration" "$REGISTRY"
    CURRENT_VERSION=$TO_VER
    APPLIED=$((APPLIED + 1))
    FOUND_MIGRATION=true
    break  # restart the while loop to find next migration
  done
done

if [ "$APPLIED" -eq 0 ]; then
  echo "Registry is up to date (schema v$CURRENT_VERSION). No migrations needed."
else
  echo "Applied $APPLIED migration(s). Registry now at schema v$CURRENT_VERSION."
fi
