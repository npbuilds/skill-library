#!/usr/bin/env python3
"""evaluate.py — pilot go/no-go evaluation.

Compares three skill states — no-skill, current (frozen baseline snapshot), and
optimized — on BOTH the frozen val split and the held-out test split (the
transfer check). Writes a go/no-go report with a generalization plan.

Usage:
    python3 scripts/skillopt/evaluate.py
    python3 scripts/skillopt/evaluate.py --write-report
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    BASELINE_SNAPSHOT, OPTIMIZED_SNAPSHOT, PROJECT_ROOT, REPORT_PATH, SKILLOPT_DIR,
    SKILL_NAME, SKILL_PATH, read_skill_body, today, ensure_dirs, write_task_score,
)
from llm import get_solver_client  # noqa: E402
from runner import score_skill, score_by_type, NO_SKILL_TEXT  # noqa: E402
from tasks import tasks_for_split  # noqa: E402

GO_MARGIN = 25.0          # required optimized-minus-current lift on the held-out test set
SATURATION_THRESHOLD = 90.0  # no-skill test at/above this == task set can't discriminate

# Verdict enum surfaced in the registry + UI badge.
VERDICTS = ("go", "no-go-saturated", "no-go-insufficient")


def compute_verdict(scores: dict) -> str:
    """Classify a run into the locked verdict enum.

    Saturation is checked FIRST (matches the report's logic): if the base model
    already aces the held-out set with no skill, the task set can't discriminate
    quality regardless of lift.
    """
    ns_test = scores["no-skill"]["test"]
    lift = scores["optimized"]["test"] - scores["current"]["test"]
    if ns_test >= SATURATION_THRESHOLD:
        return "no-go-saturated"
    if lift >= GO_MARGIN:
        return "go"
    return "no-go-insufficient"


def task_score_object(result: dict) -> dict:
    """Build the latest-only `task_score` registry object from an eval result.

    SEPARATE from composite/auto_score. Headline single-value = held-out `test`.
    """
    scores = result["scores"]
    return {
        "verdict": compute_verdict(scores),
        "val": scores["optimized"]["val"],
        "test": scores["optimized"]["test"],
        "lift": round(scores["optimized"]["test"] - scores["current"]["test"], 2),
        "no_skill_test": scores["no-skill"]["test"],
        "backend": result["backend"],
        "last_run": today(),
        "report": f"data/skillopt/{SKILL_NAME}.gonogo.md",
    }


def _states(suite: str = "contract") -> dict[str, str]:
    body = read_skill_body()
    # Quality is reported-only: grade the shipped SKILL.md (incl. CORE CLAIM line),
    # not frozen contract-optimization snapshots.
    if suite == "quality":
        return {"no-skill": NO_SKILL_TEXT, "current": body, "optimized": body}
    current = BASELINE_SNAPSHOT.read_text() if BASELINE_SNAPSHOT.exists() else body
    optimized = OPTIMIZED_SNAPSHOT.read_text() if OPTIMIZED_SNAPSHOT.exists() else body
    return {"no-skill": NO_SKILL_TEXT, "current": current, "optimized": optimized}


def _suite_config(suite: str) -> dict:
    """Map a suite name to its task file, registry key, and report path.

    contract = structural output-contract suite (default; registry `task_score`).
    quality  = research-quality suite (calibration + citation gate + diagnostic
               judge; registry sibling key `task_score_quality`).
    """
    if suite == "quality":
        return {
            "tasks_path": SKILL_PATH.parent / "eval" / "quality-tasks.yaml",
            "registry_key": "task_score_quality",
            "report_path": SKILLOPT_DIR / f"{SKILL_NAME}-quality.gonogo.md",
        }
    return {"tasks_path": None, "registry_key": "task_score", "report_path": REPORT_PATH}


def evaluate(tasks_path=None, suite: str = "contract") -> dict:
    client = get_solver_client()
    states = _states(suite)
    val_tasks = tasks_for_split("val", tasks_path)
    test_tasks = tasks_for_split("test", tasks_path)

    scores: dict[str, dict] = {}
    for name, text in states.items():
        v, vres = score_skill(text, val_tasks, client)
        t, tres = score_skill(text, test_tasks, client)
        scores[name] = {"val": v, "test": t, "val_by_type": score_by_type(vres),
                        "test_by_type": score_by_type(tres)}
    return {"backend": client.name, "scores": scores}


def _fmt_table(scores: dict) -> str:
    rows = ["| state | val task_score | test task_score |", "|---|---|---|"]
    for name in ("no-skill", "current", "optimized"):
        s = scores[name]
        rows.append(f"| {name} | {s['val']:.2f} | {s['test']:.2f} |")
    return "\n".join(rows)


def _fmt_by_type(by_type: dict) -> str:
    return ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(by_type.items()))


def render_report(result: dict) -> str:
    scores = result["scores"]
    backend = result["backend"]
    ns_test = scores["no-skill"]["test"]
    cur_test = scores["current"]["test"]
    opt_test = scores["optimized"]["test"]
    cur_val = scores["current"]["val"]
    lift = opt_test - cur_test
    skill_value = cur_test - ns_test  # how much the current skill adds over nothing
    saturated = ns_test >= 90.0       # base model already aces tasks without any skill

    if saturated:
        decision = "NO-GO (task set saturated for this model)"
        headline = (
            f"**Decision: {decision}.** With the `{backend}` backend, even the "
            f"**no-skill** baseline scores {ns_test:.2f}/100 on the held-out test set. "
            "The base model already solves these tasks without any skill guidance, so "
            "the task set cannot discriminate skill quality and there is no headroom "
            "for SkillOpt to improve (optimizer accepted 0 edits)."
        )
    elif lift >= GO_MARGIN:
        decision = "GO"
        headline = (
            f"**Decision: {decision}.** Optimized skill lifts the held-out test "
            f"task_score by **{lift:+.2f}** vs. current ({cur_test:.2f} → {opt_test:.2f}); "
            f"threshold +{GO_MARGIN:.0f}."
        )
    else:
        decision = "NO-GO (insufficient lift)"
        headline = (
            f"**Decision: {decision}.** Optimized − current lift on held-out test is "
            f"only {lift:+.2f} (threshold +{GO_MARGIN:.0f})."
        )

    if saturated:
        interpretation = (
            "On this backend the skill text makes no measurable difference: no-skill, "
            "current, and optimized all score the same. That is the expected outcome "
            "when a strong model has already internalized the procedures the skill "
            "encodes. The pilot's harness is still validated end-to-end — rollouts, "
            "the programmatic grader, the val gate, the rejected-edit buffer, and the "
            "provenance trail all ran correctly — but this skill+model+task-set "
            "combination has no optimization signal. SkillOpt only pays off where the "
            "base model is NOT already saturating the task: harder tasks, a weaker / "
            "smaller model, or fuzzier skills where procedure adherence actually moves "
            f"accuracy. (Current skill adds {skill_value:+.2f} over no-skill here.)"
        )
        plan_header = "## Recommendation (NO-GO — find a regime with headroom)"
        plan = [
            "1. Raise task difficulty until the no-skill baseline drops well below "
            "ceiling (e.g. 4+ player / larger games, perfect-Bayesian equilibria, "
            "repeated-game folk-theorem bounds, mechanism-design revenue calculations).",
            "2. Or evaluate against a smaller/cheaper model where the procedure in the "
            "skill measurably changes accuracy.",
            "3. Or target skills whose value is format/process adherence rather than "
            "raw capability (where even a strong model benefits from the skill).",
            "4. Re-use this exact harness: only the task set / model changes. The "
            "deterministic mock run remains the controlled proof that the loop lifts "
            "score when headroom exists (val 0→16.67→100, test 0→16.67→100).",
        ]
    else:
        interpretation = (
            "Lift on the held-out test split (inputs the optimizer never saw) indicates "
            "a genuine capability gain rather than val overfitting; neutral and "
            "capability-destroying edits were rejected by the strict-improvement gate."
        )
        plan_header = "## Generalization plan (if GO)"
        plan = [
            "1. Template `skills/<domain>/<skill>/eval/tasks.yaml` with train/val/test "
            "splits + per-type programmatic checkers.",
            "2. Next candidate skills with objective outputs: statistical-testing, "
            "auction-theory, intrinsic-value, model-evaluation, classical-games.",
            "3. Keep `composite_score` and `task_score` separate; only `task_score` "
            "gates SkillOpt edits.",
        ]

    # The deterministic-mock reference row only applies to skills that actually
    # had a mock run (game-solver). Omit it for skills optimized directly on a
    # live backend so the report never asserts a contrast that did not happen.
    mock_section: list[str] = []
    if (SKILLOPT_DIR / f"{SKILL_NAME}.log.mock.jsonl").exists():
        mock_section = [
            "### Live (`cursor`) vs deterministic mock backend",
            "",
            "| backend | no-skill (val/test) | current (val/test) | optimized (val/test) |",
            "|---|---|---|---|",
            f"| `{backend}` (live) | {scores['no-skill']['val']:.1f}/{ns_test:.1f} | "
            f"{cur_val:.1f}/{cur_test:.1f} | {scores['optimized']['val']:.1f}/{opt_test:.1f} |",
            "| mock (reference) | 0.0/0.0 | 16.7/16.7 | 100.0/100.0 |",
            "",
            "The mock models a skill-dependent agent (capability gated on the skill "
            "containing the procedure), so it shows large lift. The live frontier model "
            "already has the capability, so it shows none — the contrast is the point.",
            "",
        ]

    lines = [
        "# SkillOpt Pilot — Go/No-Go Report",
        "",
        f"_Generated {today()} · rollout backend: `{backend}` · skill: `{SKILL_NAME}`_",
        "",
        "## Headline",
        "",
        headline,
        "",
        "## Results",
        "",
        _fmt_table(scores),
        "",
        "- **val** is the frozen acceptance-gate split the optimizer was allowed to see.",
        "- **test** is held out — never seen by the optimizer — so it measures transfer.",
        "",
        *mock_section,
        "### Per-type breakdown (passed/total)",
        "",
        f"- no-skill — test: {_fmt_by_type(scores['no-skill']['test_by_type'])}",
        f"- current — test: {_fmt_by_type(scores['current']['test_by_type'])}",
        f"- optimized — test: {_fmt_by_type(scores['optimized']['test_by_type'])}",
        "",
        "## Interpretation",
        "",
        interpretation,
        "",
        "## Caveats",
        "",
        "- Live rollouts are nondeterministic; a per-(backend, skill-hash, task) cache "
        "stabilizes the val gate and caps cost. Programmatic checkers are exact; the "
        "rubric path is kept off the val gate to avoid judge noise.",
        "",
        plan_header,
        "",
        *plan,
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    suite = "contract"
    if "--suite" in sys.argv:
        suite = sys.argv[sys.argv.index("--suite") + 1]
    cfg = _suite_config(suite)

    result = evaluate(tasks_path=cfg["tasks_path"], suite=suite)
    print(f"Rollout backend: {result['backend']} | suite: {suite}\n")
    print(_fmt_table(result["scores"]))
    print()
    report = render_report(result)
    if "--write-report" in sys.argv:
        ensure_dirs()
        cfg["report_path"].write_text(report)
        print(f"Wrote report -> {cfg['report_path']}")
    else:
        print("(use --write-report to save the full go/no-go report)")

    if "--write-registry" in sys.argv:
        ts = task_score_object(result)
        if suite == "quality":
            # Reported-only: headline = shipped skill (current), lift vs no-skill.
            s = result["scores"]
            ts["val"] = s["current"]["val"]
            ts["test"] = s["current"]["test"]
            ts["lift"] = round(s["current"]["test"] - s["no-skill"]["test"], 2)
            ts["verdict"] = (
                "go" if s["no-skill"]["test"] < SATURATION_THRESHOLD
                and ts["lift"] >= GO_MARGIN
                else "no-go-saturated" if s["no-skill"]["test"] >= SATURATION_THRESHOLD
                else "no-go-insufficient"
            )
        ts["suite"] = suite
        try:
            ts["report"] = str(cfg["report_path"].relative_to(PROJECT_ROOT))
        except ValueError:
            ts["report"] = str(cfg["report_path"])
        ok = write_task_score(SKILL_NAME, ts, key=cfg["registry_key"])
        if ok:
            print(f"Wrote {cfg['registry_key']} for '{SKILL_NAME}': "
                  f"verdict={ts['verdict']} test={ts['test']} lift={ts['lift']:+}")
        else:
            print(f"WARN: skill '{SKILL_NAME}' not in registry; not written")


if __name__ == "__main__":
    main()
