#!/usr/bin/env bash
# refresh-registry.sh — Update registry timestamps and recompute metrics for changed skills
# Usage: bash scripts/refresh-registry.sh [skill-name ...]
#   No args: update last_scan timestamp only
#   With args: also recompute metrics for named skills
#
# Designed to run as a post-write hook or in CI to keep registry fresh.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY="$PROJECT_ROOT/data/registry.json"

if [ ! -f "$REGISTRY" ]; then
  echo "ERROR: Registry not found at $REGISTRY" >&2
  exit 1
fi

# Always update last_scan timestamp
NOW=$(python3 -c "from datetime import datetime, timezone; print(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))")

python3 -c "
import json, sys, os

registry_path = sys.argv[1]
project_root = sys.argv[2]
timestamp = sys.argv[3]
skill_names = sys.argv[4:]

with open(registry_path, 'r') as f:
    reg = json.load(f)

reg['last_scan'] = timestamp

# Recompute metrics for specific skills if provided
if skill_names:
    import subprocess
    for name in skill_names:
        entry = reg.get('skills', {}).get(name)
        if not entry:
            print(f'  SKIP {name} — not in registry', file=sys.stderr)
            continue

        location = entry.get('location', '')
        skill_path = os.path.join(project_root, location)

        if not os.path.exists(skill_path):
            print(f'  SKIP {name} — file not found: {skill_path}', file=sys.stderr)
            continue

        # Run analyze-skill.sh to get fresh metrics
        analyze_script = os.path.join(project_root, 'scripts', 'analyze-skill.sh')
        try:
            result = subprocess.run(
                ['bash', analyze_script, skill_path],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                try:
                    metrics = json.loads(result.stdout)
                except json.JSONDecodeError as je:
                    print(f'  WARN {name} — analyze returned non-JSON: {je}', file=sys.stderr)
                    continue
                entry['metrics'] = metrics
                entry['last_modified'] = timestamp[:10]
                print(f'  OK {name} — metrics refreshed')
            else:
                print(f'  WARN {name} — analyze failed: {result.stderr.strip()}', file=sys.stderr)
        except Exception as e:
            print(f'  WARN {name} — {e}', file=sys.stderr)

with open(registry_path, 'w') as f:
    json.dump(reg, f, indent=2)
    f.write('\n')

print(f'Registry updated: last_scan={timestamp}')
if skill_names:
    print(f'Refreshed {len(skill_names)} skill(s)')
" "$REGISTRY" "$PROJECT_ROOT" "$NOW" "$@"
