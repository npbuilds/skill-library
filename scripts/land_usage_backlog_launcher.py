#!/usr/bin/env python3
"""Launchd trampoline for land_usage_backlog.sh.

macOS TCC silently denies launchd background jobs access to protected
folders (Desktop, Documents) when the job's executable is an Apple platform
binary like /bin/bash — the sweep dies with exit 126 "Operation not
permitted" before the script even loads, and no permission prompt ever
appears. File-access grants attach per executable, and a user-installed
python can hold (or be granted) a Files & Folders entitlement that the
whole child process tree then inherits. install_usage_backlog_launchd.sh
therefore points the LaunchAgent at this file, run by such a python;
arguments pass through to the sweep script unchanged.
"""

import subprocess
import sys
from pathlib import Path

script = Path(__file__).resolve().parent / "land_usage_backlog.sh"
sys.exit(subprocess.call(["/bin/bash", str(script), *sys.argv[1:]]))
