# SkillOpt Pilot — Go/No-Go Report

_Generated 2026-06-02 · rollout backend: `cursor-agent` · skill: `game-solver`_

## Headline

**Decision: NO-GO (task set saturated for this model).** With the `cursor-agent` backend, even the **no-skill** baseline scores 100.00/100 on the held-out test set. The base model already solves these tasks without any skill guidance, so the task set cannot discriminate skill quality and there is no headroom for SkillOpt to improve (optimizer accepted 0 edits).

## Results

| state | val task_score | test task_score |
|---|---|---|
| no-skill | 100.00 | 100.00 |
| current | 100.00 | 100.00 |
| optimized | 100.00 | 100.00 |

- **val** is the frozen acceptance-gate split the optimizer was allowed to see.
- **test** is held out — never seen by the optimizer — so it measures transfer.

### Live (`cursor`) vs deterministic mock backend

| backend | no-skill (val/test) | current (val/test) | optimized (val/test) |
|---|---|---|---|
| `cursor-agent` (live) | 100.0/100.0 | 100.0/100.0 | 100.0/100.0 |
| mock (reference) | 0.0/0.0 | 16.7/16.7 | 100.0/100.0 |

The mock models a skill-dependent agent (capability gated on the skill containing the procedure), so it shows large lift. The live frontier model already has the capability, so it shows none — the contrast is the point.

### Per-type breakdown (passed/total)

- no-skill — test: iesds 1/1, maximin 1/1, mixed_nash_2x2 1/1, pareto 1/1, strictly_dominant 1/1, zero_sum_value 1/1
- current — test: iesds 1/1, maximin 1/1, mixed_nash_2x2 1/1, pareto 1/1, strictly_dominant 1/1, zero_sum_value 1/1
- optimized — test: iesds 1/1, maximin 1/1, mixed_nash_2x2 1/1, pareto 1/1, strictly_dominant 1/1, zero_sum_value 1/1

## Interpretation

On this backend the skill text makes no measurable difference: no-skill, current, and optimized all score the same. That is the expected outcome when a strong model has already internalized the procedures the skill encodes. The pilot's harness is still validated end-to-end — rollouts, the programmatic grader, the val gate, the rejected-edit buffer, and the provenance trail all ran correctly — but this skill+model+task-set combination has no optimization signal. SkillOpt only pays off where the base model is NOT already saturating the task: harder tasks, a weaker / smaller model, or fuzzier skills where procedure adherence actually moves accuracy. (Current skill adds +0.00 over no-skill here.)

## Caveats

- Live rollouts are nondeterministic; a per-(backend, skill-hash, task) cache stabilizes the val gate and caps cost. Programmatic checkers are exact; the rubric path is kept off the val gate to avoid judge noise.

## Recommendation (NO-GO — find a regime with headroom)

1. Raise task difficulty until the no-skill baseline drops well below ceiling (e.g. 4+ player / larger games, perfect-Bayesian equilibria, repeated-game folk-theorem bounds, mechanism-design revenue calculations).
2. Or evaluate against a smaller/cheaper model where the procedure in the skill measurably changes accuracy.
3. Or target skills whose value is format/process adherence rather than raw capability (where even a strong model benefits from the skill).
4. Re-use this exact harness: only the task set / model changes. The deterministic mock run remains the controlled proof that the loop lifts score when headroom exists (val 0→16.67→100, test 0→16.67→100).
