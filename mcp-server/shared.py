"""Shared utilities for the Skill Library MCP server and CLI."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REGISTRY_PATH = DATA_DIR / "registry.json"
USAGE_LOG = DATA_DIR / "usage.jsonl"
GAPS_LOG = DATA_DIR / "gaps.jsonl"
FEEDBACK_LOG = DATA_DIR / "feedback.jsonl"
SKILLS_DIR = PROJECT_ROOT / "skills"


def load_log(path: Path) -> list[dict]:
    """Load all events from a JSONL log file."""
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events
