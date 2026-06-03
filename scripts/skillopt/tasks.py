#!/usr/bin/env python3
"""tasks.py — load the game-solver task set and compose rollout prompts.

The task YAML stays clean (human-readable prompt + structured input + gold). The
runner composes the *full* prompt here: the natural-language problem, a
machine-readable TASK_SPEC block (so a deterministic mock can parse it, and a
real LLM has the exact game spec), and the required answer protocol.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from common import TASKS_PATH


def load_tasks(path: Path | None = None) -> list[dict]:
    data = yaml.safe_load((path or TASKS_PATH).read_text())
    tasks = data.get("tasks", [])
    # DRY: a contract declared once in `meta.contract` is inherited by every
    # contract task that doesn't define its own. Authoring a new skill then
    # needs only one contract block + the per-task prompts.
    meta_contract = (data.get("meta") or {}).get("contract")
    if meta_contract is not None:
        for t in tasks:
            if t.get("checker") == "contract" and "contract" not in t:
                t["contract"] = meta_contract
    return tasks


def tasks_for_split(split: str, path: Path | None = None) -> list[dict]:
    return [t for t in load_tasks(path) if t.get("split") == split]


ANSWER_SCHEMA = {
    "strictly_dominant": '"<strategy label>" or "none"',
    "best_response": '"<strategy label>"',
    "pure_nash": '[["<row>", "<col>"], ...]',
    "mixed_nash_2x2": '{"p": <float>, "q": <float>}',
    "zero_sum_value": "<number>",
    "maximin": '"<strategy label>"',
    "iesds": '[["<row>", "<col>"], ...]',
    "pareto": '[["<row>", "<col>"], ...]',
    "backward_induction": '{"path": ["<action>", ...], "payoff": [<p1>, <p2>]}',
    "interpretation": '"<short paragraph>"',
}


def compose_prompt(task: dict) -> str:
    """Build the full user prompt for one rollout."""
    # Format-adherence tasks: present a realistic, format-AGNOSTIC request. The
    # output contract must come from the SKILL.md (when injected), NOT the
    # prompt — otherwise the no-skill baseline would trivially comply.
    if task.get("checker") == "contract":
        return task["prompt"].strip() + "\n\nWrite your response now."

    spec = {"type": task["type"], "input": task.get("input", {})}
    for k in ("player", "opponent_strategy"):
        if k in task:
            spec[k] = task[k]
    schema = ANSWER_SCHEMA.get(task["type"], '"<answer>"')
    parts = [
        task["prompt"].strip(),
        "",
        "TASK_SPEC (authoritative game specification):",
        "```json",
        json.dumps(spec, indent=2),
        "```",
        "",
        "Show brief reasoning, then end with exactly one line:",
        f"ANSWER: {schema}",
    ]
    return "\n".join(parts)
