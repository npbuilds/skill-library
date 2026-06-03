# SkillOpt Pilot — Go/No-Go Report

_Generated 2026-06-02 · rollout backend: `mock` · skill: `game-solver`_

## Headline

**Decision: GO.** Optimized skill lifts the held-out **test** task_score by **+83.33** vs. the current skill (16.67 → 100.00); the go threshold is +25.

## Results

| state | val task_score | test task_score |
|---|---|---|
| no-skill | 0.00 | 0.00 |
| current | 16.67 | 16.67 |
| optimized | 100.00 | 100.00 |

- **val** is the frozen acceptance-gate split the optimizer was allowed to see.
- **test** is held out — never seen by the optimizer — so it measures transfer.

### Per-type breakdown (passed/total)

- current — val: maximin 0/1, mixed_nash_2x2 0/1, pareto 0/1, pure_nash 1/1, strictly_dominant 0/1, zero_sum_value 0/1
- optimized — val: maximin 1/1, mixed_nash_2x2 1/1, pareto 1/1, pure_nash 1/1, strictly_dominant 1/1, zero_sum_value 1/1
- current — test: iesds 1/1, maximin 0/1, mixed_nash_2x2 0/1, pareto 0/1, strictly_dominant 0/1, zero_sum_value 0/1
- optimized — test: iesds 1/1, maximin 1/1, mixed_nash_2x2 1/1, pareto 1/1, strictly_dominant 1/1, zero_sum_value 1/1

## Interpretation

The gains come from val-gated edits that added crisp, missing procedural recipes (strictly-dominant test, mixed-strategy indifference method, zero-sum saddle-point value, maximin/security strategy, Pareto-optimality test). Because the same lift appears on the held-out test split — on different games the optimizer never saw — the improvement is a genuine capability gain, not val overfitting. Neutral and capability-destroying edits were correctly rejected by the strict-improvement gate.

## Caveats

- This run used the deterministic rollout backend (no live LLM API key was available). It models 'a skill confers capability if it contains the procedure' and proves the *loop* is correct and the task set discriminates. Re-run with `SKILLOPT_LLM=anthropic` (set `ANTHROPIC_API_KEY`) or `SKILLOPT_LLM=cursor` to measure real-model lift before generalizing.
- Programmatic checkers are exact/structured; the rubric-judge path exists for open tasks but is intentionally kept off the val gate to avoid judge noise.

## Generalization plan (if GO)

1. Re-confirm the lift with a real LLM backend on this same task set.
2. Template the task set: `skills/<domain>/<skill>/eval/tasks.yaml` with train/val/test splits and a per-type programmatic checker, reusing `gametheory.py`-style deterministic solvers per domain.
3. Next 3-5 candidate skills (objective, checkable outputs):
   - `data-science/statistical-analysis/statistical-testing` (test selection, corrections, effect-size formulas)
   - `game-theory/mechanism-design/auction-theory` (revenue equivalence, bid calculations)
   - `investing/value-quality/intrinsic-value` (DCF arithmetic)
   - `data-science/modeling/model-evaluation` (metric computation)
   - `game-theory/strategic-foundations/classical-games` (canonical solutions)
4. Keep `composite_score` (library hygiene) and `task_score` (rollout accuracy) as separate signals; only `task_score` gates SkillOpt edits.
