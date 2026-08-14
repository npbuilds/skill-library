#!/usr/bin/env bash
# land_usage_backlog.sh — Sweep locally-appended data/usage.jsonl rows to main.
#
# The daily CI maint workflow cannot see the local working tree, so rows
# appended by the local writers (Claude Desktop stdio server, launchd remote
# server, the plugin telemetry hook) accumulate as uncommitted backlog that
# exists nowhere else. This script lands them via the normal flow:
#
#   validate (append-only, JSON, no dups vs origin/main)
#     -> branch -> recalibrate_scores.py -> commit -> push -> PR
#     -> wait for CI green -> squash-merge -> return checkout to a clean main
#
# Run it from the PRIMARY checkout (the one the writers append to), manually
# or from a local scheduler (launchd / Claude Code scheduled task). It is
# idempotent: with no backlog it exits 0 without side effects.
#
# Usage: bash scripts/land_usage_backlog.sh [--dry-run] [--no-merge]
#   --dry-run   validate and report the backlog, change nothing
#   --no-merge  push the branch and open the PR, but leave merging to a human
#
# Rows appended by a writer WHILE the sweep runs are never lost: they are
# rescued back into the working tree after the branch switch and become the
# next sweep's backlog.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
USAGE_REL="data/usage.jsonl"
USAGE_FILE="$PROJECT_ROOT/$USAGE_REL"

DRY_RUN=0
NO_MERGE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --no-merge) NO_MERGE=1 ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

cd "$PROJECT_ROOT"

# The writers append to the primary checkout; a linked worktree has its own
# working tree and would sweep nothing (or the wrong thing).
if [ ! -d .git ]; then
  echo "ERROR: not the primary checkout (.git is not a directory) — run this from the main checkout, not a worktree." >&2
  exit 1
fi

BRANCH="$(git branch --show-current)"
if [ "$BRANCH" != "main" ]; then
  echo "ERROR: checkout is on '$BRANCH', expected 'main'. Resolve whatever is in flight, return to main, and re-run." >&2
  exit 1
fi

git fetch origin main -q

# Extract the locally-appended rows (working tree lines not in the given ref's
# copy of usage.jsonl), preserving order. Also validates JSON + append-only.
extract_new_rows() { # $1 = ref to compare against, output: one JSON row per line
  python3 - "$1" <<'PYEOF'
import json, subprocess, sys
ref = sys.argv[1]
base = subprocess.run(["git", "show", f"{ref}:data/usage.jsonl"],
                      capture_output=True, text=True, check=True).stdout
keys = set()
for line in base.splitlines():
    if line.strip():
        r = json.loads(line)
        keys.add((r.get("session_id"), r.get("timestamp")))
seen_lines = set(l for l in base.splitlines() if l.strip())
new = []
with open("data/usage.jsonl") as f:
    for n, line in enumerate(f, 1):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"ERROR: data/usage.jsonl line {n} is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)
        if line in seen_lines:
            continue
        k = (r.get("session_id"), r.get("timestamp"))
        if k in keys:
            # Same event already committed (e.g. landed upstream by a bot PR
            # while it also sat in the local tree) — drop it, do not re-land.
            print(f"note: dropping already-committed row {k}", file=sys.stderr)
            continue
        keys.add(k)
        new.append(line)
for line in new:
    print(line)
PYEOF
}

# Refuse anything that isn't a pure append — a deletion or edit of committed
# rows means something unexpected touched the log and needs human eyes.
assert_append_only() { # $1 = ref
  local dels
  dels="$(git diff --numstat "$1" -- "$USAGE_REL" | awk '{print $2}')"
  if [ -n "$dels" ] && [ "$dels" != "0" ]; then
    echo "ERROR: $USAGE_REL diff vs $1 removes/edits $dels committed line(s) — not a pure append. Inspect manually:" >&2
    echo "  git diff $1 -- $USAGE_REL" >&2
    exit 1
  fi
}

# --- Reconcile with origin/main -------------------------------------------
# If local main is behind (a bot telemetry PR landed since the last pull),
# branching from local HEAD would open an unmergeable append-conflict PR.
# Rebuild instead: save the local rows, fast-forward, re-append (deduped).
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
  if ! git merge-base --is-ancestor HEAD origin/main; then
    echo "ERROR: local main has diverged from origin/main (not fast-forwardable). Reconcile manually first." >&2
    exit 1
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "Local main is behind origin/main — a real run will fast-forward and reconcile. Backlog vs origin/main:"
    assert_append_only HEAD
    extract_new_rows origin/main | sed 's/^/  /'
    echo "Dry run — nothing changed."
    exit 0
  fi
  echo "Local main is behind origin/main — reconciling backlog across the fast-forward."
  assert_append_only HEAD
  SAVED="$(mktemp)"
  extract_new_rows HEAD > "$SAVED"
  git restore "$USAGE_REL"
  git pull --ff-only -q origin main
  if [ -s "$SAVED" ]; then
    # Re-append, dropping rows the pulled commits already contain.
    python3 - "$SAVED" <<'PYEOF'
import json, sys
saved = sys.argv[1]
keys = set()
with open("data/usage.jsonl") as f:
    for line in f:
        if line.strip():
            r = json.loads(line)
            keys.add((r.get("session_id"), r.get("timestamp")))
kept = dropped = 0
with open(saved) as f, open("data/usage.jsonl", "a") as out:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        r = json.loads(line)
        if (r.get("session_id"), r.get("timestamp")) in keys:
            dropped += 1
            continue
        out.write(line + "\n")
        kept += 1
print(f"Reconciled: kept {kept} local row(s), dropped {dropped} already landed upstream.")
PYEOF
  fi
  rm -f "$SAVED"
fi

# --- Detect + validate the backlog ----------------------------------------
if git diff --quiet HEAD -- "$USAGE_REL"; then
  echo "No usage backlog — $USAGE_REL matches origin/main. Nothing to sweep."
  exit 0
fi
assert_append_only HEAD

ROWS_FILE="$(mktemp)"
extract_new_rows HEAD > "$ROWS_FILE"
N_ROWS="$(grep -c . "$ROWS_FILE" || true)"
if [ "$N_ROWS" -eq 0 ]; then
  # Every "new" line was a duplicate of a committed row; reset the file so the
  # phantom diff stops reappearing.
  echo "All locally-appended rows are already committed — resetting $USAGE_REL to HEAD."
  rm -f "$ROWS_FILE"
  if [ "$DRY_RUN" -eq 0 ]; then git restore "$USAGE_REL"; fi
  exit 0
fi

echo "Backlog: $N_ROWS row(s) to land:"
sed 's/^/  /' "$ROWS_FILE"
echo
echo "--- attribution report (unresolved names stay skill_raw; aliases only for commands that skip get_skill) ---"
python3 scripts/log_skill_invocation.py --report || true
echo "---"

if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run — no branch, commit, or PR created."
  rm -f "$ROWS_FILE"
  exit 0
fi

# --- Branch, recalibrate, commit ------------------------------------------
STAMP="$(date -u +%Y%m%d-%H%M%S)"
SWEEP_BRANCH="chore/land-usage-backlog-$STAMP"
git checkout -q -b "$SWEEP_BRANCH"

echo "Recalibrating scores (usage feeds auto_score)..."
python3 scripts/recalibrate_scores.py

git add "$USAGE_REL"
if ! git diff --quiet -- data/registry.json; then
  git add data/registry.json
  RECAL_NOTE="recalibrate_scores.py updated data/registry.json in the same commit."
else
  RECAL_NOTE="recalibrate_scores.py: no score changes needed."
fi

git commit -q -m "chore(telemetry): land ${N_ROWS}-row local usage backlog (sweep)

Automated sweep by scripts/land_usage_backlog.sh: locally-appended
data/usage.jsonl rows that exist nowhere else (local writers do not
mirror to Firestore, so the daily CI pull cannot land them).
Validated append-only and deduplicated against origin/main by
(session_id, timestamp) before landing. ${RECAL_NOTE}"

# --- Push, PR, merge -------------------------------------------------------
git push -q -u origin "$SWEEP_BRANCH"
PR_URL="$(gh pr create --base main \
  --title "chore(telemetry): land ${N_ROWS}-row local usage backlog (sweep)" \
  --body "Automated sweep of locally-appended \`data/usage.jsonl\` rows by \`scripts/land_usage_backlog.sh\`. Rows validated append-only and deduplicated against \`origin/main\` by \`(session_id, timestamp)\`. ${RECAL_NOTE}

🤖 Generated with [Claude Code](https://claude.com/claude-code)")"
echo "PR opened: $PR_URL"

# Rescue any rows a writer appended while we worked, then return to main
# BEFORE merging — checkout (ours or gh's) refuses to switch branches with
# usage.jsonl dirty, and the final pull must happen on a clean file too.
MIDRUN="$(mktemp)"
extract_new_rows "$SWEEP_BRANCH" > "$MIDRUN"
git restore "$USAGE_REL"
git checkout -q main

reappend_midrun() {
  if [ -s "$MIDRUN" ]; then
    cat "$MIDRUN" >> "$USAGE_FILE"
    echo "note: $(grep -c . "$MIDRUN") row(s) appended mid-sweep were kept in the working tree for the next sweep."
  fi
  rm -f "$MIDRUN" "$ROWS_FILE"
}

if [ "$NO_MERGE" -eq 1 ]; then
  reappend_midrun
  echo "Done (--no-merge): merge $PR_URL when ready, then 'git pull' here."
  exit 0
fi

echo "Waiting for CI..."
if ! gh pr checks "$PR_URL" --watch --interval 30; then
  reappend_midrun
  echo "ERROR: CI failed on $PR_URL — PR left open for inspection; checkout returned to main." >&2
  exit 1
fi
gh pr merge "$PR_URL" --squash --delete-branch
git pull --ff-only -q origin main
reappend_midrun
echo "Swept $N_ROWS row(s) to main. Checkout is clean on main."
