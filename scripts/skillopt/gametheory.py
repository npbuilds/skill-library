#!/usr/bin/env python3
"""gametheory.py — deterministic solvers for the game-solver task set.

Two jobs:
  1. `solve(task_type, input)` independently re-derives the canonical answer for
     a task. Used by `--validate` to prove the gold answers in tasks.yaml are
     mathematically correct (a guard against authoring mistakes), and by the
     deterministic runner to model a *competent* agent.
  2. `naive_guess(task_type, input)` models an agent that lacks the procedure:
     it returns a plausible-but-usually-wrong answer. Used to model an
     *incompetent* agent (no relevant skill guidance).

Plus `COMPETENCE_MARKERS`: per task-type substrings that, if present in a
SKILL.md, indicate the skill teaches the procedure for that type. This is what
lets the deterministic harness model "the skill confers capability."

Usage:
    python3 scripts/skillopt/gametheory.py --validate
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

# ── Competence markers ────────────────────────────────────────────────────────
# A skill is "competent" at a task type if its (lowercased) text contains ANY of
# the marker phrases for that type. The phrases are precise procedural cues that
# a crisp recipe would contain — not vague topic mentions.
COMPETENCE_MARKERS: dict[str, list[str]] = {
    "pure_nash": ["best response", "best-response", "mutual best response"],
    "best_response": ["best response", "best-response"],
    "iesds": ["iterated elimination", "dominated strateg", "dominance reasoning"],
    "backward_induction": ["backward induction", "subgame perfect"],
    "strictly_dominant": [
        "strictly dominates every",
        "higher payoff against each",
        "higher payoff regardless",
        "dominant against every",
    ],
    "mixed_nash_2x2": [
        "make the opponent indifferent",
        "opponent indifferent",
        "indifference condition",
        "set expected payoffs equal",
    ],
    "zero_sum_value": [
        "value of the game",
        "saddle point",
        "minimax theorem",
        "maximin equals minimax",
    ],
    "maximin": ["maximin", "security level", "guaranteed worst-case"],
    "pareto": ["pareto-optimal", "pareto optimal", "pareto efficient", "pareto frontier"],
    # interpretation (rubric) competence: the skill must teach plain-language interpretation
    "interpretation": ["interpret", "plain-language", "plain language"],
}


def is_competent(skill_text: str, task_type: str) -> bool:
    markers = COMPETENCE_MARKERS.get(task_type, [])
    if not markers:
        return False
    low = skill_text.lower()
    return any(m in low for m in markers)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _payoff(inp: dict, r: str, c: str) -> tuple[float, float]:
    pr, pc = inp["payoffs"][r][c]
    return float(pr), float(pc)


def _rows(inp: dict) -> list[str]:
    return list(inp["row_strategies"])


def _cols(inp: dict) -> list[str]:
    return list(inp["col_strategies"])


# ── Solvers (the "competent" path / gold re-derivation) ────────────────────────

def solve_strictly_dominant(inp: dict, player: str = "row") -> str:
    rows, cols = _rows(inp), _cols(inp)
    if player == "row":
        for cand in rows:
            others = [r for r in rows if r != cand]
            if all(
                all(_payoff(inp, cand, c)[0] > _payoff(inp, o, c)[0] for c in cols)
                for o in others
            ):
                return cand
    else:
        for cand in cols:
            others = [c for c in cols if c != cand]
            if all(
                all(_payoff(inp, r, cand)[1] > _payoff(inp, r, o)[1] for r in rows)
                for o in others
            ):
                return cand
    return "none"


def solve_best_response(inp: dict, player: str, opponent_strategy: str) -> str:
    rows, cols = _rows(inp), _cols(inp)
    if player == "row":
        best, arg = None, None
        for r in rows:
            v = _payoff(inp, r, opponent_strategy)[0]
            if best is None or v > best:
                best, arg = v, r
        return arg
    else:
        best, arg = None, None
        for c in cols:
            v = _payoff(inp, opponent_strategy, c)[1]
            if best is None or v > best:
                best, arg = v, c
        return arg


def solve_pure_nash(inp: dict) -> list[list[str]]:
    rows, cols = _rows(inp), _cols(inp)
    eq = []
    for r in rows:
        for c in cols:
            rp, cp = _payoff(inp, r, c)
            row_ok = all(rp >= _payoff(inp, r2, c)[0] for r2 in rows)
            col_ok = all(cp >= _payoff(inp, r, c2)[1] for c2 in cols)
            if row_ok and col_ok:
                eq.append([r, c])
    return eq


def solve_mixed_nash_2x2(inp: dict) -> dict:
    rows, cols = _rows(inp), _cols(inp)
    if len(rows) != 2 or len(cols) != 2:
        raise ValueError("mixed_nash_2x2 requires a 2x2 game")
    r1, r2 = rows
    c1, c2 = cols
    # q = P(col plays c1) makes ROW indifferent between r1 and r2
    # row(r1) = q*u(r1,c1) + (1-q)*u(r1,c2); row(r2) = q*u(r2,c1)+(1-q)*u(r2,c2)
    a = _payoff(inp, r1, c1)[0] - _payoff(inp, r1, c2)[0]
    b = _payoff(inp, r1, c2)[0]
    d = _payoff(inp, r2, c1)[0] - _payoff(inp, r2, c2)[0]
    e = _payoff(inp, r2, c2)[0]
    # a*q + b = d*q + e  ->  q*(a-d) = e-b
    q = Fraction(int(round((e - b))), 1) if (a - d) == 0 else Fraction(e - b).limit_denominator() / Fraction(a - d).limit_denominator()
    # p = P(row plays r1) makes COL indifferent between c1 and c2
    a2 = _payoff(inp, r1, c1)[1] - _payoff(inp, r2, c1)[1]
    b2 = _payoff(inp, r2, c1)[1]
    d2 = _payoff(inp, r1, c2)[1] - _payoff(inp, r2, c2)[1]
    e2 = _payoff(inp, r2, c2)[1]
    p = None if (a2 - d2) == 0 else Fraction(e2 - b2).limit_denominator() / Fraction(a2 - d2).limit_denominator()
    return {"p": round(float(p), 4), "q": round(float(q), 4)}


def solve_zero_sum_value(inp: dict) -> float:
    """Saddle-point value to the row player (maximin == minimax)."""
    rows, cols = _rows(inp), _cols(inp)
    row_mins = {r: min(_payoff(inp, r, c)[0] for c in cols) for r in rows}
    col_maxs = {c: max(_payoff(inp, r, c)[0] for r in rows) for c in cols}
    maximin = max(row_mins.values())
    minimax = min(col_maxs.values())
    if maximin != minimax:
        raise ValueError(f"no pure saddle point (maximin={maximin}, minimax={minimax})")
    v = maximin
    return int(v) if float(v).is_integer() else v


def solve_maximin(inp: dict, player: str) -> str:
    rows, cols = _rows(inp), _cols(inp)
    if player == "row":
        scores = {r: min(_payoff(inp, r, c)[0] for c in cols) for r in rows}
    else:
        scores = {c: min(_payoff(inp, r, c)[1] for r in rows) for c in cols}
    return max(scores, key=scores.get)


def solve_iesds(inp: dict) -> list[list[str]]:
    rows, cols = _rows(inp), _cols(inp)
    R, C = list(rows), list(cols)
    changed = True
    while changed:
        changed = False
        # eliminate strictly dominated row strategies
        for cand in list(R):
            if any(
                all(_payoff(inp, o, c)[0] > _payoff(inp, cand, c)[0] for c in C)
                for o in R if o != cand
            ):
                R.remove(cand)
                changed = True
        # eliminate strictly dominated column strategies
        for cand in list(C):
            if any(
                all(_payoff(inp, r, o)[1] > _payoff(inp, r, cand)[1] for r in R)
                for o in C if o != cand
            ):
                C.remove(cand)
                changed = True
    return [[r, c] for r in R for c in C]


def solve_pareto(inp: dict) -> list[list[str]]:
    rows, cols = _rows(inp), _cols(inp)
    cells = [(r, c) for r in rows for c in cols]
    out = []
    for r, c in cells:
        rp, cp = _payoff(inp, r, c)
        dominated = False
        for r2, c2 in cells:
            if (r2, c2) == (r, c):
                continue
            rp2, cp2 = _payoff(inp, r2, c2)
            if rp2 >= rp and cp2 >= cp and (rp2 > rp or cp2 > cp):
                dominated = True
                break
        if not dominated:
            out.append([r, c])
    return out


def solve_backward_induction(inp: dict) -> dict:
    """SPE via backward induction on an explicit tree.

    Node = {"player": "P1"|"P2", "actions": {label: child}} where a child is
    either another node or a leaf {"payoff": [p1, p2]}. Returns the equilibrium
    path (list of action labels) and the resulting payoff.
    """
    player_index = {"P1": 0, "P2": 1}

    def rec(node: dict) -> tuple[list[str], list[float]]:
        if "payoff" in node:
            return [], list(node["payoff"])
        idx = player_index[node["player"]]
        best_path, best_payoff, best_action = None, None, None
        for action, child in node["actions"].items():
            path, payoff = rec(child)
            if best_payoff is None or payoff[idx] > best_payoff[idx]:
                best_payoff, best_path, best_action = payoff, path, action
        return [best_action] + best_path, best_payoff

    path, payoff = rec(inp["tree"])
    return {"path": path, "payoff": [int(x) if float(x).is_integer() else x for x in payoff]}


SOLVERS = {
    "strictly_dominant": lambda inp, t: solve_strictly_dominant(inp, t.get("player", "row")),
    "best_response": lambda inp, t: solve_best_response(inp, t.get("player", "row"), t["opponent_strategy"]),
    "pure_nash": lambda inp, t: solve_pure_nash(inp),
    "mixed_nash_2x2": lambda inp, t: solve_mixed_nash_2x2(inp),
    "zero_sum_value": lambda inp, t: solve_zero_sum_value(inp),
    "maximin": lambda inp, t: solve_maximin(inp, t.get("player", "row")),
    "iesds": lambda inp, t: solve_iesds(inp),
    "pareto": lambda inp, t: solve_pareto(inp),
    "backward_induction": lambda inp, t: solve_backward_induction(inp),
}


def solve(task: dict) -> Any:
    """Re-derive the canonical answer for a task from its structured input."""
    fn = SOLVERS.get(task["type"])
    if fn is None:
        return None
    return fn(task["input"], task)


# ── Naive guessers (the "incompetent" path) ────────────────────────────────────
# Deterministic, plausible-but-usually-wrong answers. Some happen to be correct
# (e.g. matching-pennies-style symmetric mixes), giving realistic non-zero
# baselines rather than a degenerate 0/100 step function.

def naive_guess(task: dict) -> Any:
    t = task["type"]
    inp = task.get("input", {})
    rows = inp.get("row_strategies", [])
    cols = inp.get("col_strategies", [])
    if t == "strictly_dominant":
        return "none"
    if t == "best_response":
        return rows[0] if task.get("player", "row") == "row" else cols[0]
    if t == "pure_nash":
        return [[rows[0], cols[0]]] if rows and cols else []
    if t == "mixed_nash_2x2":
        return {"p": 0.5, "q": 0.5}
    if t == "zero_sum_value":
        return 0
    if t == "maximin":
        return rows[0] if task.get("player", "row") == "row" else cols[0]
    if t == "iesds":
        return [[r, c] for r in rows for c in cols]  # guess nothing eliminated
    if t == "pareto":
        # guess only the joint-payoff-maximizing cell
        best, arg = None, None
        for r in rows:
            for c in cols:
                pr, pc = inp["payoffs"][r][c]
                s = pr + pc
                if best is None or s > best:
                    best, arg = s, [r, c]
        return [arg] if arg else []
    if t == "backward_induction":
        node = inp.get("tree", {})
        path = []
        while "actions" in node:
            action = next(iter(node["actions"]))
            path.append(action)
            node = node["actions"][action]
        return {"path": path, "payoff": node.get("payoff", [])}
    if t == "interpretation":
        return ""
    return None


# ── Validation entrypoint ──────────────────────────────────────────────────────

def _validate() -> int:
    # Local import to avoid a hard dependency when only solving.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "skillopt_tasks", Path(__file__).resolve().parent / "tasks.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    from grader import answers_match  # type: ignore

    tasks = mod.load_tasks()
    failures = 0
    by_split: dict[str, int] = {}
    for task in tasks:
        by_split[task["split"]] = by_split.get(task["split"], 0) + 1
        if task["checker"] != "programmatic":
            continue
        derived = solve(task)
        if not answers_match(task, derived, task["gold"]):
            failures += 1
            print(f"  ✗ {task['id']:24s} gold={task['gold']!r} solver={derived!r}")
        else:
            print(f"  ✓ {task['id']:24s} {task['type']}")
    print()
    print(f"Splits: " + ", ".join(f"{k}={v}" for k, v in sorted(by_split.items())))
    if failures:
        print(f"VALIDATION FAILED: {failures} gold/solver mismatch(es)")
    else:
        print("VALIDATION PASSED: all programmatic gold answers match the independent solver.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    if "--validate" in sys.argv:
        raise SystemExit(_validate())
    print(__doc__)
