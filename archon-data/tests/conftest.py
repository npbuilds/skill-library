"""Test bootstrap for Archon Data's flat module layout."""

import sys
from pathlib import Path


ARCHON_ROOT = Path(__file__).resolve().parents[1]
if str(ARCHON_ROOT) not in sys.path:
    sys.path.insert(0, str(ARCHON_ROOT))
