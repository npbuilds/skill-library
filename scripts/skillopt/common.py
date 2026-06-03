#!/usr/bin/env python3
"""common.py — shared paths and small helpers for the SkillOpt pilot.

All new data/logs live under data/skillopt/ and never at the repo root, per the
project's file-placement rules.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
EVOLUTION_LOG = PROJECT_ROOT / "data" / "evolution.jsonl"
SKILLOPT_DIR = PROJECT_ROOT / "data" / "skillopt"

# The harness is reusable across skills: choose the target with SKILLOPT_SKILL.
# Its SKILL.md location is resolved from the registry (source of truth), with a
# small fallback map so the modules import even if the registry is mid-edit.
SKILL_NAME = os.environ.get("SKILLOPT_SKILL", "game-solver").strip()

_LOCATION_FALLBACK = {
    "game-solver": "skills/game-theory/strategic-foundations/game-solver/SKILL.md",
    "bluf-shaper": "skills/binding-vow/bluf-shaper/SKILL.md",
}


def _resolve_location(name: str) -> str:
    try:
        with open(REGISTRY_PATH) as f:
            loc = json.load(f)["skills"][name]["location"]
            if loc:
                return loc
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass
    if name in _LOCATION_FALLBACK:
        return _LOCATION_FALLBACK[name]
    raise KeyError(f"Cannot resolve SKILL.md location for skill '{name}'")


SKILL_REL = _resolve_location(SKILL_NAME)
SKILL_PATH = PROJECT_ROOT / SKILL_REL
TASKS_PATH = SKILL_PATH.parent / "eval" / "tasks.yaml"

LOG_PATH = SKILLOPT_DIR / f"{SKILL_NAME}.log.jsonl"
REJECTED_PATH = SKILLOPT_DIR / f"{SKILL_NAME}.rejected.jsonl"
BASELINE_SNAPSHOT = SKILLOPT_DIR / f"{SKILL_NAME}.baseline.md"
OPTIMIZED_SNAPSHOT = SKILLOPT_DIR / f"{SKILL_NAME}.optimized.md"
REPORT_PATH = SKILLOPT_DIR / f"{SKILL_NAME}.gonogo.md"

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(\n|$)", re.DOTALL)


def ensure_dirs() -> None:
    SKILLOPT_DIR.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter_block_including_delimiters, body)."""
    m = _FM_RE.match(text)
    if not m:
        return "", text
    return text[: m.end()], text[m.end():]


def read_skill_text(path: Path | None = None) -> str:
    return (path or SKILL_PATH).read_text(errors="replace")


def read_skill_body(path: Path | None = None) -> str:
    """The body is what we treat as the editable + injectable skill content."""
    _, body = split_frontmatter(read_skill_text(path))
    return body


def write_skill_body(new_body: str, path: Path | None = None) -> None:
    """Rewrite SKILL.md preserving its YAML frontmatter, replacing the body."""
    p = path or SKILL_PATH
    fm, _ = split_frontmatter(read_skill_text(p))
    p.write_text(fm + new_body)


def append_jsonl(path: Path, record: dict) -> None:
    ensure_dirs()
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def load_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def save_registry(reg: dict) -> None:
    with open(REGISTRY_PATH, "w") as f:
        json.dump(reg, f, indent=2)
        f.write("\n")


def write_task_score(skill_name: str, task_score: dict) -> bool:
    """Idempotently store the LATEST task_score object on a registry skill.

    `task_score` is a SEPARATE signal from auto_score/composite_score — this
    never touches the composite/auto math. Latest-only by design (full history
    lives in data/evolution.jsonl). Returns False if the skill is unknown.
    """
    reg = load_registry()
    entry = reg["skills"].get(skill_name)
    if entry is None:
        return False
    entry["task_score"] = task_score
    save_registry(reg)
    return True
