---
name: falsifiability-checker
description: >
  Test whether a problem statement (treated as a claim) is falsifiable in Popperian terms:
  what observation would prove it wrong? Thin coordinator over philosophy/philosophy-of-science/demarcation-judge
  that translates problem-statement framing into the claim-shaped input demarcation-judge
  expects. Use in binding-vow's Phase 6 audit, especially for statements containing implicit
  predictions or causal claims.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Falsifiability Checker — The Popperian Translator

A thin coordinator that translates a problem statement into the claim-shaped input that `demarcation-judge` (philosophy/philosophy-of-science) evaluates, then translates the output back into binding-vow's grader-axis terms.

The actual falsifiability assessment is done by `demarcation-judge`. This skill's value is the *translation* — problem statements rarely arrive shaped as claims, and feeding them to `demarcation-judge` directly produces nonsense. The translation step is small but load-bearing.

## Process

### Step 1 — Extract implicit claims

Most problem statements embed claims rather than make them explicit. Extract:

- **Predictive claims** ("if we do X, Y will happen") — directly falsifiable
- **Causal claims** ("X is causing Y") — falsifiable if mechanism is specified
- **Existence claims** ("Y is happening to N% of users") — falsifiable via measurement
- **Comparative claims** ("X is worse than Z") — falsifiable via head-to-head data

If the statement is purely interrogative ("how do I do X?") with no embedded claim, return verdict `N/A — interrogative` and skip to output.

### Step 2 — Reformulate as claims and pass to `demarcation-judge`

For each extracted claim, pass to `demarcation-judge` with:

- The claim text (in declarative form)
- The domain context (clinical, software, business, etc.)
- The implicit prediction the claim makes

Receive back the falsifiability verdict per claim.

### Step 3 — Aggregate and translate

Translate `demarcation-judge`'s output back into binding-vow's terms:

| `demarcation-judge` verdict | binding-vow translation | Falsifiability axis score |
|---|---|---|
| Falsifiable, makes risky predictions | Empirically grounded | 5 |
| Falsifiable but cautious; predictions are weak | Acceptable | 4 |
| Falsifiable in principle but practically untestable | Borderline | 3 |
| Probabilistic / hedged; falsification requires base-rate context | Weak | 2 |
| Unfalsifiable — tautology, ad hoc, or values-shaped | Fail | 1 |

If the statement contains multiple claims with mixed verdicts, the axis score is the *minimum* across claims (the weakest link drives the score).

## Output Format

```
FALSIFIABILITY — [first 60 chars of statement...]
─────────────────────────────────────────────
Implicit claims extracted: [list]
Per-claim verdicts: [from demarcation-judge]
Aggregate score: [1-5]
Reformulation hint (if score < 3): [what would make this falsifiable]
```

## Output Contract for `six-eyes`

Returns the falsifiability axis score (1-5) and reformulation hint for `statement-grader`. If aggregate score < 3, the re-state loop should reformulate the statement to make at least one claim falsifiable.

## Scope Boundaries

- **falsifiability-checker handles:** translating problem-statement format ↔ claim format, aggregating multi-claim verdicts.
- **falsifiability-checker does NOT:** perform the falsifiability assessment itself — that's `demarcation-judge`'s job. If `demarcation-judge` is unavailable, return "deferred" rather than guessing.

## Failure Modes

| Failure | Response |
|---|---|
| No claims extractable from statement | Return `N/A — interrogative or pure description`; mark falsifiability axis as not-applicable |
| `demarcation-judge` unavailable | Return "deferred — call demarcation-judge directly"; do not fabricate the verdict |
| Statement contains a values claim ("we should X") | Pass to `demarcation-judge` anyway; expect verdict "unfalsifiable as values-shaped" and translate accordingly |

## Connections

- `statement-grader` (binding-vow) — feeds the falsifiability axis
- `demarcation-judge` (philosophy/philosophy-of-science) — primary cross-domain call
- `argument-analyst` (philosophy/logic) — adjacent skill for evaluating the argument that supports the claim

## Sources

- Popper, K. R. (1959). *The Logic of Scientific Discovery*. (Falsifiability as the demarcation criterion.)
- See [[kahneman-framing]] for the cognitive failure modes (especially attribute substitution) that produce unfalsifiable problem statements.
