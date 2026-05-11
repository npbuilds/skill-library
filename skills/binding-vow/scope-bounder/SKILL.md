---
name: scope-bounder
description: >
  Surface the scope boundaries (time period, population, context) of a problem statement
  and check whether they are explicit and defensible. Thin coordinator over
  philosophy/logic/assumption-excavator with depth=surface and category=scope. Use in
  binding-vow's Phase 6 audit. Returns explicit/implicit/missing assessment per boundary
  type plus reformulation hints.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Scope Bounder — The Boundary Surfacer

A thin coordinator that calls `assumption-excavator` (philosophy/logic) with `depth=surface, category=scope` and translates the output into the scope axis on `statement-grader`.

The hardest part of scope-bounding is recognizing that universal statements are usually wrong; the easiest part is asking "for whom, when, and in what context?" This skill makes the easy part routine.

## The Three Boundary Types

| Boundary | What it specifies | Failure signal |
|---|---|---|
| **Time** | Period the statement applies to | "Always" implicitly — no temporal anchor |
| **Population** | People, accounts, units the statement applies to | "Customers" with no segmentation; "users" without cohort |
| **Context** | Conditions, environment, regime under which the statement holds | No mention of regime, market state, or operational context |

A statement that explicitly bounds all three is well-scoped. A statement that bounds two of three is acceptable. One or zero boundaries explicit triggers the re-state loop on this axis.

## Process

### Step 1 — Call `assumption-excavator`

Pass:
- The statement
- Domain context
- `depth=surface` (don't excavate every assumption — only scope)
- `category=scope`

Receive:
- Hidden scope assumptions across the three boundary types
- For each: visibility (hidden/semi-visible/visible-but-unchallenged), contestability, load-bearing assessment

### Step 2 — Categorize each boundary

For each of (Time, Population, Context):

| Status | Meaning |
|---|---|
| **Explicit** | The statement names this boundary directly |
| **Implicit-defensible** | The boundary is implicit but clearly inferable from context |
| **Implicit-questionable** | The boundary is implicit and ambiguous; a reasonable reader could interpret differently |
| **Missing** | The statement makes no claim about this boundary; it's universal-by-default |

### Step 3 — Score the scope axis

| Pattern | Scope axis score |
|---|---|
| All three explicit; defensible | 5 |
| Two explicit; one implicit-defensible | 4 |
| One explicit; two implicit-defensible | 3 |
| One or two explicit; one or more implicit-questionable | 2 |
| One or zero explicit; rest missing or questionable | 1 |

### Step 4 — Generate hints

For each Missing or Implicit-questionable boundary, produce a hint:
- "Specify the time period: is this Q3 2026? The next 12 months? Indefinitely?"
- "Specify the population: enterprise customers? Free-tier users? All segments?"
- "Specify the context: under current pricing? After the rebrand? In the EU regulatory regime?"

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

## Output Contract for `six-eyes`

Feeds the scope axis on `statement-grader` (axis 3). Hints feed the re-state loop's input to Phase 4.

## Scope Boundaries (of the skill itself)

- **scope-bounder handles:** the three-boundary check and scoring.
- **scope-bounder does NOT:** evaluate whether the bounded scope is *correct* — it evaluates whether the scope is *explicit*. A confidently-bounded but wrong scope still scores well; that's a different audit (often answerability).

## Failure Modes

| Failure | Response |
|---|---|
| `assumption-excavator` unavailable | Inline a degraded version: ask the three boundary questions directly without the full assumption framework |
| Statement is so short there's no scope claim to surface | Return "ungraded" and route back to Phase 1 (Intake) for restatement |
| Two boundaries are tangled (population implicitly bounds time) | Note the entanglement; score the more-explicit of the two normally and flag the tangle |

## Connections

- `statement-grader` (binding-vow) — feeds the scope axis
- `assumption-excavator` (philosophy/logic) — primary cross-domain call (with category=scope)
- `wicked-vs-tame` (binding-vow) — wicked problems often have inherently fuzzy scope; that's a property of the problem type, not a defect

## Sources

- The three-boundary frame (time / population / context) is canonical in epidemiology and program evaluation; see Rothman's *Epidemiology* for the reference treatment.
- See [[kahneman-framing]] for the universal-by-default cognitive bias that scope-bounder targets.
