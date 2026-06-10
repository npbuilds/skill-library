# Falsifiability Checker — Quick Reference


## Quick Reference

| `demarcation-judge` verdict | binding-vow translation | Falsifiability axis score |
|---|---|---|
| Falsifiable, makes risky predictions | Empirically grounded | 5 |
| Falsifiable but cautious; predictions are weak | Acceptable | 4 |
| Falsifiable in principle but practically untestable | Borderline | 3 |
| Probabilistic / hedged; falsification requires base-rate context | Weak | 2 |
| Unfalsifiable — tautology, ad hoc, or values-shaped | Fail | 1 |

## Failure Modes

| Failure | Response |
|---|---|
| No claims extractable from statement | Return `N/A — interrogative or pure description`; mark falsifiability axis as not-applicable |
| `demarcation-judge` unavailable | Return "deferred — call demarcation-judge directly"; do not fabricate the verdict |
| Statement contains a values claim ("we should X") | Pass to `demarcation-judge` anyway; expect verdict "unfalsifiable as values-shaped" and translate accordingly |

## Output Format

```
FALSIFIABILITY — [first 60 chars of statement...]
─────────────────────────────────────────────
Implicit claims extracted: [list]
Per-claim verdicts: [from demarcation-judge]
Aggregate score: [1-5]
Reformulation hint (if score < 3): [what would make this falsifiable]
```
