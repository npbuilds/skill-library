# Scope Bounder — Quick Reference


## The Three Boundary Types

| Boundary | What it specifies | Failure signal |
|---|---|---|
| **Time** | Period the statement applies to | "Always" implicitly — no temporal anchor |
| **Population** | People, accounts, units the statement applies to | "Customers" with no segmentation; "users" without cohort |
| **Context** | Conditions, environment, regime under which the statement holds | No mention of regime, market state, or operational context |

## Quick Reference

| Status | Meaning |
|---|---|
| **Explicit** | The statement names this boundary directly |
| **Implicit-defensible** | The boundary is implicit but clearly inferable from context |
| **Implicit-questionable** | The boundary is implicit and ambiguous; a reasonable reader could interpret differently |
| **Missing** | The statement makes no claim about this boundary; it's universal-by-default |

## Step 3 — Score the scope axis

| Pattern | Scope axis score |
|---|---|
| All three explicit; defensible | 5 |
| Two explicit; one implicit-defensible | 4 |
| One explicit; two implicit-defensible | 3 |
| One or two explicit; one or more implicit-questionable | 2 |
| One or zero explicit; rest missing or questionable | 1 |

## Failure Modes

| Failure | Response |
|---|---|
| `assumption-excavator` unavailable | Inline a degraded version: ask the three boundary questions directly without the full assumption framework |
| Statement is so short there's no scope claim to surface | Return "ungraded" and route back to Phase 1 (Intake) for restatement |
| Two boundaries are tangled (population implicitly bounds time) | Note the entanglement; score the more-explicit of the two normally and flag the tangle |

## Output Format

```
SCOPE — [first 60 chars of statement...]
─────────────────────────────────────────────
Time:       [explicit | implicit-defensible | implicit-questionable | missing] | [signal]
Population: [status] | [signal]
Context:    [status] | [signal]

Score: [1-5]
Hints (per missing/questionable boundary):
  - [hint]
```
