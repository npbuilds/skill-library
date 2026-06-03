# SkillOpt Pilot — Go/No-Go Report

_Generated 2026-06-03 · rollout backend: `cursor-agent` · skill: `spelunker`_

## Headline

**Decision: NO-GO (insufficient lift).** Optimized − current lift on held-out test is only +21.68 (threshold +25).

## Results

| state | val task_score | test task_score |
|---|---|---|
| no-skill | 0.00 | 0.00 |
| current | 56.66 | 66.66 |
| optimized | 95.00 | 88.34 |

- **val** is the frozen acceptance-gate split the optimizer was allowed to see.
- **test** is held out — never seen by the optimizer — so it measures transfer.

### Per-type breakdown (passed/total)

- no-skill — test: spelunker-brief 0/5
- current — test: spelunker-brief 0/5
- optimized — test: spelunker-brief 3/5

## Interpretation

Lift on the held-out test split (inputs the optimizer never saw) indicates a genuine capability gain rather than val overfitting; neutral and capability-destroying edits were rejected by the strict-improvement gate.

## Caveats

- Live rollouts are nondeterministic; a per-(backend, skill-hash, task) cache stabilizes the val gate and caps cost. Programmatic checkers are exact; the rubric path is kept off the val gate to avoid judge noise.

## Generalization plan (if GO)

1. Template `skills/<domain>/<skill>/eval/tasks.yaml` with train/val/test splits + per-type programmatic checkers.
2. Next candidate skills with objective outputs: statistical-testing, auction-theory, intrinsic-value, model-evaluation, classical-games.
3. Keep `composite_score` and `task_score` separate; only `task_score` gates SkillOpt edits.
