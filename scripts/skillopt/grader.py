#!/usr/bin/env python3
"""grader.py — turn rollout outputs into a 0-100 task_score.

Two grading paths, matching the plan:
  - programmatic: exact / structured comparison against the gold answer
    (per-type normalization with numeric tolerance for mixed/zero-sum).
  - rubric: a judge scores an open-ended answer against keyword anchors,
    mirroring agents/skill-tester.md's expect_contains concept. The judge is
    pluggable (real LLM or a deterministic keyword-coverage mock).
"""
from __future__ import annotations

import json
import re
from typing import Any

TOL = 0.02


def parse_answer(raw: str) -> Any:
    """Extract the structured answer from a rollout's text output.

    Looks for the last `ANSWER: ...` line and JSON-parses its payload. Falls
    back to a bare-string answer when the payload is not valid JSON.
    """
    if raw is None:
        return None
    matches = re.findall(r"ANSWER:\s*(.+)$", raw, re.MULTILINE)
    payload = matches[-1].strip() if matches else raw.strip()
    # Strip surrounding markdown/code ticks if present.
    payload = payload.strip("`").strip()
    try:
        return json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return payload.strip('"').strip()


def _norm_str(x: Any) -> str:
    return str(x).strip().strip('"').lower()


def _as_pair_set(x: Any) -> set[tuple[str, str]]:
    out = set()
    if isinstance(x, (list, tuple)):
        for item in x:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                out.add((_norm_str(item[0]), _norm_str(item[1])))
    return out


def _as_float(x: Any) -> float | None:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def answers_match(task: dict, candidate: Any, gold: Any) -> bool:
    """Programmatic equality check, normalized per task type."""
    t = task["type"]
    if t in ("strictly_dominant", "best_response", "maximin"):
        return _norm_str(candidate) == _norm_str(gold)
    if t in ("pure_nash", "iesds", "pareto"):
        return _as_pair_set(candidate) == _as_pair_set(gold)
    if t == "zero_sum_value":
        c, g = _as_float(candidate), _as_float(gold)
        return c is not None and g is not None and abs(c - g) <= TOL
    if t == "mixed_nash_2x2":
        if not isinstance(candidate, dict):
            return False
        cp, cq = _as_float(candidate.get("p")), _as_float(candidate.get("q"))
        gp, gq = _as_float(gold.get("p")), _as_float(gold.get("q"))
        return None not in (cp, cq, gp, gq) and abs(cp - gp) <= TOL and abs(cq - gq) <= TOL
    if t == "backward_induction":
        if not isinstance(candidate, dict):
            return False
        path_ok = [
            _norm_str(a) for a in candidate.get("path", [])
        ] == [_norm_str(a) for a in gold.get("path", [])]
        cpay = [_as_float(x) for x in candidate.get("payoff", [])]
        gpay = [_as_float(x) for x in gold.get("payoff", [])]
        pay_ok = len(cpay) == len(gpay) and all(
            a is not None and b is not None and abs(a - b) <= TOL for a, b in zip(cpay, gpay)
        )
        return path_ok and pay_ok
    return _norm_str(candidate) == _norm_str(gold)


def rubric_score(task: dict, answer_text: str, judge=None) -> float:
    """Score an open-ended answer 0-100.

    If a `judge` callable is provided (real LLM judge), delegate to it.
    Otherwise use deterministic keyword coverage over `expect_contains`.
    """
    if judge is not None:
        return float(judge(task, answer_text))
    anchors = task.get("expect_contains", [])
    if not anchors:
        return 0.0
    low = (answer_text or "").lower()
    hits = sum(1 for a in anchors if a.lower() in low)
    return round(100.0 * hits / len(anchors), 1)


def grade_one(task: dict, rollout: dict, judge=None, judge_complete=None) -> dict:
    """Grade a single rollout dict {answer, raw_text}. Returns a result dict.

    `judge` is the keyword/rubric judge; `judge_complete` is a raw
    complete(system, user)->str backend used by the research-quality suite's
    DIAGNOSTIC-ONLY structured judge (never affects the gate score).
    """
    detail = None
    if task["checker"] == "contract":
        import contracts  # local import: only needed for format-adherence skills
        res = contracts.score_contract(task, rollout.get("raw_text", ""))
        score = res["score"]
        detail = res["checks"]
        passed = score >= 90.0
    elif task["checker"] == "quality":
        import quality  # research-quality suite (calibration + citation gate, judged diagnostics)
        res = quality.score_quality(task, rollout.get("raw_text", ""), judge_complete=judge_complete)
        score = res["score"]
        passed = res["passed"]
        detail = {k: res[k] for k in ("calibration", "citation_integrity", "judged", "weights")}
    elif task["checker"] == "rubric":
        score = rubric_score(task, rollout.get("raw_text", ""), judge=judge)
        passed = score >= 75.0
    else:
        candidate = rollout.get("answer")
        passed = answers_match(task, candidate, task["gold"])
        score = 100.0 if passed else 0.0
    return {
        "id": task["id"],
        "type": task["type"],
        "split": task["split"],
        "checker": task["checker"],
        "score": score,
        "passed": passed,
        "answer": rollout.get("answer"),
        "gold": task.get("gold"),
        "detail": detail,
    }


def aggregate(results: list[dict]) -> float:
    """Mean task_score across a set, 0-100."""
    if not results:
        return 0.0
    return round(sum(r["score"] for r in results) / len(results), 2)


def _selftest() -> int:
    """Tiny self-check of the declarative contract engine + legacy parity."""
    import contracts
    good = (
        "BOTTOM LINE: Approve the $2M Q3 onboarding rebuild.\n\n"
        "BACKGROUND:\n- Churn rose to 12%.\n- Onboarding is the top driver.\n\n"
        "DISCUSSION:\n1. Activation window is the leak.\n2. Fix is 4 eng-quarters.\n\n"
        "RECOMMENDATION: Approve $2M and reallocate 3 engineers this week."
    )
    unstructured = "Here's a quick take: you should probably consider rebuilding onboarding."
    decl = {
        "sections": ["BOTTOM LINE:", "BACKGROUND:", "DISCUSSION:", "RECOMMENDATION:"],
        "checks": [
            {"type": "sections_in_order"},
            {"type": "one_sentence", "section": "BOTTOM LINE:"},
            {"type": "must_not_include", "section": "BOTTOM LINE:", "patterns": ["likely", "probably"]},
            {"type": "list_items", "section": "BACKGROUND:", "style": "bullet", "min": 1, "max": 3},
            {"type": "list_items", "section": "DISCUSSION:", "style": "numbered", "min": 1, "max": 5},
            {"type": "non_empty", "section": "RECOMMENDATION:"},
        ],
    }
    cases = [
        ("declarative good", contracts.evaluate_contract(good, decl)["score"], 100.0),
        ("declarative unstructured", contracts.evaluate_contract(unstructured, decl)["score"], 0.0),
        ("legacy score_bluf good", contracts.score_bluf(good)["score"], 100.0),
        ("legacy score_bluf bad", contracts.score_bluf(unstructured)["score"], 0.0),
        # individual checkers
        ("json_valid", contracts.evaluate_contract(
            '{"verdict": "go", "n": 3}',
            {"sections": [], "checks": [{"type": "json_valid", "required_keys": ["verdict", "n"],
                                         "types": {"verdict": "str", "n": "int"}}]})["score"], 100.0),
        ("length max", contracts.evaluate_contract(
            "one two three four five",
            {"sections": [], "checks": [{"type": "length", "unit": "words", "max": 3}]})["score"], 0.0),
        ("must_include any", contracts.evaluate_contract(
            "the plan is approved",
            {"sections": [], "checks": [{"type": "must_include", "patterns": ["approved", "rejected"],
                                         "mode": "any"}]})["score"], 100.0),
    ]
    failures = 0
    for name, got, want in cases:
        ok = abs(got - want) < 1e-6
        print(f"  {'✓' if ok else '✗'} {name}: got {got} want {want}")
        failures += 0 if ok else 1
    print("grader selftest:", "OK" if not failures else f"{failures} FAILURE(S)")
    return 1 if failures else 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    print(__doc__)
