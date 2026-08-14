#!/usr/bin/env bash
# install_usage_backlog_launchd.sh — wire land_usage_backlog.sh to a daily launchd job.
#
# Generates ~/Library/LaunchAgents/studio.neocortex.usage-backlog-sweep.plist
# pointing at THIS checkout's scripts/land_usage_backlog.sh and bootstraps it.
# The checkout path is derived from the installer's own location at install
# time, so no private workspace path is ever committed to this public repo.
#
# The job runs daily at 09:30 local time; the sweep is idempotent (exits
# immediately when there is no backlog), and launchd never overlaps runs of
# the same label. Logs: ~/Library/Logs/usage-backlog-sweep.log
#
# Usage:
#   bash scripts/install_usage_backlog_launchd.sh              # install / refresh
#   bash scripts/install_usage_backlog_launchd.sh --uninstall  # remove the job
#
# Re-run after moving the checkout. Must be run from the PRIMARY checkout —
# the sweep itself refuses to run from a worktree, so installing from one
# would schedule a job that only ever errors.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LABEL="studio.neocortex.usage-backlog-sweep"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/usage-backlog-sweep.log"
DOMAIN="gui/$(id -u)"

if [ "${1:-}" = "--uninstall" ]; then
  launchctl bootout "$DOMAIN" "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Uninstalled $LABEL."
  exit 0
fi

if [ ! -d "$PROJECT_ROOT/.git" ]; then
  echo "ERROR: $PROJECT_ROOT is not the primary checkout (.git is not a directory) — install from the main checkout, not a worktree." >&2
  exit 1
fi
if [ ! -f "$PROJECT_ROOT/scripts/land_usage_backlog.sh" ]; then
  echo "ERROR: scripts/land_usage_backlog.sh not found next to this installer." >&2
  exit 1
fi

# The job must NOT run /bin/bash directly: macOS TCC silently denies launchd
# background jobs run by Apple platform binaries any access to protected
# folders (Desktop/Documents) — exit 126, no prompt. A user-installed python
# can hold a Files & Folders grant that the child bash inherits, so the job
# runs land_usage_backlog_launcher.py instead. Override the interpreter with
# SWEEP_LAUNCHER=/path/to/python if the default python3 lacks the grant.
LAUNCHER="${SWEEP_LAUNCHER:-$(command -v python3)}"
if [ -z "$LAUNCHER" ] || [ ! -x "$LAUNCHER" ]; then
  echo "ERROR: no usable python3 found (set SWEEP_LAUNCHER=/path/to/python)." >&2
  exit 1
fi

# gh and the launcher's python live outside launchd's minimal default PATH.
JOB_PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
PY_DIR="$(dirname "$LAUNCHER")"
case ":$JOB_PATH:" in *":$PY_DIR:"*) ;; *) JOB_PATH="$PY_DIR:$JOB_PATH" ;; esac

mkdir -p "$HOME/Library/LaunchAgents" "$HOME/Library/Logs"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>

    <key>ProgramArguments</key>
    <array>
        <string>$LAUNCHER</string>
        <string>$PROJECT_ROOT/scripts/land_usage_backlog_launcher.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>$PROJECT_ROOT</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>$JOB_PATH</string>
    </dict>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string>$LOG</string>

    <key>StandardErrorPath</key>
    <string>$LOG</string>
</dict>
</plist>
EOF

# Refresh cleanly if already installed (bootout is a no-op on first install).
launchctl bootout "$DOMAIN" "$PLIST" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"

echo "Installed $LABEL:"
echo "  launcher: $LAUNCHER"
echo "  sweeps:   $PROJECT_ROOT/data/usage.jsonl"
echo "  schedule: daily 09:30 local"
echo "  log:      $LOG"
echo "Trigger a run now with: launchctl kickstart $DOMAIN/$LABEL"
