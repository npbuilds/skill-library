# Frame Rotator — Quick Reference


## Quick Reference

| Move | What it does | When it helps |
|---|---|---|
| **Specialize** | Narrow to a specific case, smaller scope, single instance | Original feels too abstract to act on; need a concrete starting point |
| **Generalize** | Broaden to a class of cases, larger scope, abstraction up | Original feels too narrow; solving the general case might be easier than the specific one (Polya's counterintuitive move) |

## Mode Behavior

| Mode | Behavior |
|---|---|
| Quick | Skip frame-rotator entirely (quick mode skips Phase 4) |
| Standard | Produce 2–3 alternatives covering at least 2 of the 3 operations |
| Deep | Produce ≥3 alternatives covering all 3 operations; mandatory diff-check on each |

## Failure Modes

| Failure | Response |
|---|---|
| All generated alternatives are cosmetic | Diff-check should catch them. If 3+ fail diff-check in a row, the input is too narrow to rotate — escalate to `claim-decomposer` to widen scope, then retry |
| HMW formulation feels forced (the "for [user]" or "so that [outcome]" is invented) | The statement may not have a clear user/outcome; surface this rather than fabricate. The statement may be values-shaped, not problem-shaped — escalate to `answerability-tester` |
| Specialize and Generalize produce alternatives that are identical (because the original is at the right level) | Skip those operations; rely on HMW + framing-swap. Document that level-shifting wasn't fruitful |
| `assumption-excavator` returns no contestable framing assumptions | The statement may be exceptionally well-framed already. If frame-rotation finds no real alternatives, statement-grader's framing-related axes are likely passing on their own |

## Formula / Pseudocode

```
How might we [intended action verb] for [potential user/subject]
so that [desired outcome]?
```
