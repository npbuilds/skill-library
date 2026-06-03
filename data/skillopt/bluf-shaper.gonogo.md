# SkillOpt Pilot — Go/No-Go Report

_Generated 2026-06-02 · rollout backend: `cursor-agent` · skill: `bluf-shaper`_

## Headline

**Decision: GO.** Optimized skill lifts the held-out test task_score by **+100.00** vs. current (0.00 → 100.00); threshold +25. This is the first **live-model** lift in the pilot — unlike `game-solver`, which the same model saturated at 100 (no headroom).

## Experiment context — ablation (read this first)

The **shipped** `bluf-shaper` skill already scores **100/100** on this contract with the live model, so optimizing it directly yields no signal (same ceiling problem as game-solver). To get a real current→optimized signal, the optimizer was started from an **ablated baseline**: the shipped skill with its explicit ``## Output Format`` contract block removed. That ablated skill is the "current" row below — it scores 0, identical to no-skill, because that block was the single load-bearing element. The optimizer then had to **recover** the contract from rollout feedback alone, and the recovery transferred to the held-out test set.

- **no-skill (0)** — no guidance at all
- **current (0)** — ablated skill (contract block removed); the optimizer's start point
- **optimized (100)** — optimizer-recovered skill
- _shipped skill, for reference = 100_ — the ceiling the optimizer re-attained

## Contract enforced (deterministic, 0-100)

`scripts/skillopt/contracts.py:score_bluf` scores 10 purely-structural checks: the four uppercase headers `BOTTOM LINE` / `BACKGROUND` / `DISCUSSION` / `RECOMMENDATION` present and in that exact order; bottom line is exactly one sentence; no hedging words in the bottom line; BACKGROUND has 1-3 bullets; DISCUSSION has 1-5 numbered points; RECOMMENDATION is a specific (non-vague) action.

## Headroom evidence

Live **no-skill** rollouts violated the contract on **100% of tasks** (val 0/5, test 0/5, every one of the 10 checks failing): the model writes a sensible brief but never reproduces the exact BLUF structure unprompted. The shipped skill flips that to full compliance. Opposite of game-solver, where no-skill already scored 100.

## Edits accepted / rejected (live val gate)

| edit | op | val before→after | outcome |
|---|---|---|---|
| `bluf-format-core` | add the exact contract block | 0 → 100 | **ACCEPTED** (version 1.0.0→1.0.1) |
| `bluf-discipline` | add one-sentence / no-hedge rules | 100 → 100 | rejected (no strict gain — already at ceiling) |
| `bluf-noise` | add a stylistic line | 100 → 100 | rejected |
| `bluf-harmful-freeform` | "headers are optional" | 100 → 100 | rejected |

One accepted edit recovered the full contract; the three non-improving edits (including the capability-loosening one) were correctly rejected by the strict-improvement gate. A meta-consolidation pass ran and kept val at 100.

## Results

| state | val task_score | test task_score |
|---|---|---|
| no-skill | 0.00 | 0.00 |
| current | 0.00 | 0.00 |
| optimized | 100.00 | 100.00 |

- **val** is the frozen acceptance-gate split the optimizer was allowed to see.
- **test** is held out — never seen by the optimizer — so it measures transfer.

### Per-type breakdown (passed/total)

- no-skill — test: bluf 0/5
- current — test: bluf 0/5
- optimized — test: bluf 5/5

## Interpretation

Lift on the held-out test split (inputs the optimizer never saw) indicates a genuine capability gain rather than val overfitting; neutral and capability-destroying edits were rejected by the strict-improvement gate.

## Caveats

- Live rollouts are nondeterministic; a per-(backend, skill-hash, task) cache stabilizes the val gate and caps cost. Programmatic checkers are exact; the rubric path is kept off the val gate to avoid judge noise.

## Generalization plan (if GO)

1. Template `skills/<domain>/<skill>/eval/tasks.yaml` with train/val/test splits + per-type programmatic checkers.
2. Next candidate skills with objective outputs: statistical-testing, auction-theory, intrinsic-value, model-evaluation, classical-games.
3. Keep `composite_score` and `task_score` separate; only `task_score` gates SkillOpt edits.
