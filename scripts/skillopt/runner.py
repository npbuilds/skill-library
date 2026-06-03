#!/usr/bin/env python3
"""runner.py — rollout runner + baselines.

Given a SKILL.md body (text) and a task, run one agent rollout with the skill
injected and capture the answer. Aggregating over a split yields a 0-100
task_score. Establishes the no-skill and current-skill baselines.

Usage:
    python3 scripts/skillopt/runner.py --baselines            # all splits
    python3 scripts/skillopt/runner.py --baselines --split val
    SKILLOPT_LLM=anthropic python3 scripts/skillopt/runner.py --baselines
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import read_skill_body, SKILLOPT_DIR, ensure_dirs  # noqa: E402
from grader import grade_one, aggregate  # noqa: E402
from llm import get_solver_client  # noqa: E402
from tasks import tasks_for_split, load_tasks  # noqa: E402

NO_SKILL_TEXT = (
    "# (no skill)\n\nNo domain guidance is provided. Answer from general knowledge.\n"
)

# ── Rollout cache ──────────────────────────────────────────────────────────────
# Keyed by (backend, sha(skill_text), task_id). With a nondeterministic live
# model this (a) caps cost — the optimizer re-scores the same body many times —
# and (b) makes the strict-improvement val gate stable: a given skill body always
# yields the same task_score. Disable with SKILLOPT_NO_CACHE=1.
_CACHE_PATH = SKILLOPT_DIR / "rollout_cache.json"
_CACHE: dict | None = None


def _cache() -> dict:
    global _CACHE
    if _CACHE is None:
        try:
            _CACHE = json.loads(_CACHE_PATH.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            _CACHE = {}
    return _CACHE


def _cache_key(backend: str, skill_text: str, task_id: str) -> str:
    h = hashlib.sha256(skill_text.encode("utf-8")).hexdigest()[:16]
    return f"{backend}:{h}:{task_id}"


def _cache_put(key: str, value: dict) -> None:
    c = _cache()
    c[key] = value
    ensure_dirs()
    _CACHE_PATH.write_text(json.dumps(c))


def _cache_enabled() -> bool:
    return os.environ.get("SKILLOPT_NO_CACHE", "").lower() not in ("1", "true", "yes")


def score_skill(skill_text: str, tasks: list[dict], client=None) -> tuple[float, list[dict]]:
    """Roll out every task with `skill_text` injected; return (task_score, results)."""
    client = client or get_solver_client()
    judge = getattr(client, "judge", None)
    use_cache = _cache_enabled()
    results = []
    for task in tasks:
        rollout = None
        key = _cache_key(client.name, skill_text, task["id"]) if use_cache else None
        if use_cache:
            rollout = _cache().get(key)
        if rollout is None:
            rollout = client.rollout(skill_text, task)
            if use_cache:
                _cache_put(key, rollout)
        results.append(grade_one(task, rollout, judge=judge))
    return aggregate(results), results


def score_by_type(results: list[dict]) -> dict[str, tuple[int, int]]:
    """Map task type -> (passed, total) for a result list."""
    agg: dict[str, list[int]] = {}
    for r in results:
        a = agg.setdefault(r["type"], [0, 0])
        a[0] += 1 if r["passed"] else 0
        a[1] += 1
    return {k: (v[0], v[1]) for k, v in agg.items()}


def run_baselines(split: str | None = None) -> None:
    client = get_solver_client()
    print(f"Rollout backend: {client.name}\n")
    splits = [split] if split else ["train", "val", "test"]
    no_skill_body = NO_SKILL_TEXT
    current_body = read_skill_body()

    print(f"{'split':6s} {'no-skill':>10s} {'current':>10s}")
    print("-" * 30)
    for sp in splits:
        tasks = tasks_for_split(sp)
        if not tasks:
            continue
        ns, _ = score_skill(no_skill_body, tasks, client)
        cur, cur_results = score_skill(current_body, tasks, client)
        print(f"{sp:6s} {ns:>10.2f} {cur:>10.2f}")
    print()
    # Per-type detail on val (the gate set) for the current skill
    val_tasks = tasks_for_split("val")
    if val_tasks:
        _, cur_results = score_skill(current_body, val_tasks, client)
        print("Current skill — per-type on val:")
        for ttype, (p, n) in sorted(score_by_type(cur_results).items()):
            flag = "" if p == n else "   <- headroom"
            print(f"  {ttype:18s} {p}/{n}{flag}")


def main() -> None:
    args = sys.argv[1:]
    split = None
    if "--split" in args:
        split = args[args.index("--split") + 1]
    if "--baselines" in args or not args:
        run_baselines(split)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
