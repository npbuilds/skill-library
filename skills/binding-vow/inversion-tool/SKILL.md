---
name: inversion-tool
description: >
  Apply Munger inversion to a problem statement — instead of asking how to succeed, ask
  what would guarantee failure, then negate to surface preconditions for success. Use during
  binding-vow's Phase 4 reframing as a complement to frame-rotator. Distinct from steel-manning
  the opposing view; this inverts the success/failure axis. Returns the inverted statement
  plus negation-derived preconditions.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Inversion Tool — Munger's Move

"All I want to know is where I'm going to die, so I'll never go there." Charlie Munger's recurring move: instead of asking how to achieve X, ask what would guarantee not-X. Then ensure none of those failure conditions are present. The negative space defines the positive solution more sharply than direct optimization does.

Inversion is distinct from steel-manning (which builds the strongest *opposing* argument) and from frame-rotator (which produces alternative formulations of the same goal). Inversion takes the *same* goal and asks: what makes failure certain?

## When Inversion Helps

| Helps when | Doesn't help when |
|---|---|
| Multiple paths to success, hard to compare | Single obviously-correct path |
| Failure modes are easier to enumerate than success modes | Pure-creative problems with open-ended success |
| Asymmetric outcomes — avoid catastrophe matters more than maximize | Symmetric optimization with clear objective function |
| Plan is in pre-mortem stage (before execution) | Plan is in execution — inversion-derived preconditions should already be in place |

The skill is most useful for *decisions* and *plans* where the stakes are real and failure has clear shape. Less useful for pure exploration.

## Process

### Step 1 — Restate the statement as a success criterion

If the statement isn't already framed as "we want X" or "succeed at X", reformulate so the success state is explicit. Inversion needs a clear success-failure axis.

### Step 2 — Enumerate failure modes

Ask: "what would guarantee not-X?" Generate the failure catalog. Aim for 5–10 failure modes covering different layers:

| Layer | Example failure modes |
|---|---|
| **Strategic** | Wrong target; missing the actual problem; pursuing the wrong metric |
| **Tactical** | Right target, wrong approach; insufficient resources; bad sequencing |
| **Operational** | Right approach, broken execution; missed handoff; quality drift |
| **Cultural** | Misaligned incentives; coordination failure; political resistance |
| **External** | Environmental shifts that invalidate the plan; black swans |

Be specific. "Things go wrong" is not a failure mode. "We launch in Q3 but our competitor pre-empts in July" is.

### Step 3 — Negate each failure mode

For each enumerated failure, state the *opposite condition* — the precondition that must hold for that failure not to occur.

Example:
- Failure mode: "We launch in Q3 but competitor pre-empts in July"
- Negation (precondition): "Either we accelerate to launch by July, OR we differentiate enough that being second doesn't kill the play"

### Step 4 — Aggregate preconditions

The set of negated failure modes forms a list of preconditions for success. This is sharper than a generic success spec.

### Step 5 — Cross-check with original

Compare the precondition list to the original statement. Are any preconditions *missing* from the original framing? Those are the candidates the original statement was leaving implicit — surface them.

## Output Format

```
INVERSION — [first 60 chars of original statement...]
─────────────────────────────────────────────
Original goal:   [success criterion restated explicitly]

Failure catalog (what would guarantee not-X):
  Strategic:
    F1. [failure mode] — specificity check: [specific or vague]
  Tactical:
    F2. [failure mode]
  Operational:
    F3. [failure mode]
  Cultural:
    F4. [failure mode]
  External:
    F5. [failure mode]

Negation-derived preconditions:
  P1. [opposite of F1]
  P2. [opposite of F2]
  P3. [opposite of F3]
  P4. [opposite of F4]
  P5. [opposite of F5]

Preconditions NOT in the original framing:
  - [precondition that the original statement leaves implicit; this is the value of inversion]

Inverted statement (alternative formulation):
  [The problem reframed as "ensure none of the failure modes are present" — useful when this
   framing is more tractable than the direct "achieve success" framing]
```

## Distinction from Adjacent Skills

| Skill | What it does | When to prefer |
|---|---|---|
| **inversion-tool** | Asks "what guarantees failure"; derives preconditions by negation | Decision/plan with clear failure shape |
| `steel-man-forge` (philosophy/dialectical-tools) | Builds strongest *opposing* argument | Persuasion or stress-testing a position |
| `frame-rotator` (binding-vow) | Produces alternative formulations of the same goal | Original framing feels narrow |
| `xy-detector` (binding-vow) | Detects solution-disguised-as-problem | Statement is mechanism-shaped |

These can chain. For high-stakes decisions, run frame-rotator + inversion-tool together: frame-rotator opens the solution space; inversion-tool sharpens the success conditions inside that space.

## Failure Modes

| Failure | Response |
|---|---|
| Failure modes are vague ("things go wrong") | Force specificity — name actors, timelines, mechanisms. Vague failure modes produce vague preconditions |
| Failure mode is unfalsifiable ("we lack the right culture") | Call `assumption-excavator` to surface what specifically the cultural-failure framing assumes; convert to a falsifiable mode |
| Cannot generate 5+ failure modes | The statement may be too narrow for inversion — escalate to `frame-rotator` to widen scope first |
| Preconditions list duplicates the original success criterion verbatim | Inversion isn't producing new insight; the original framing is already comprehensive. Document this and return |

## Output Contract for `six-eyes`

Called from Phase 4 (Reframe) in standard or deep mode. Returns:
- Failure catalog
- Precondition list
- The "preconditions NOT in original" — this is the load-bearing output for downstream phases
- Optional: inverted-statement alternative formulation

`six-eyes` uses the "missing preconditions" set to determine if the original statement is missing structurally important elements. If 2+ missing preconditions surface, the statement should be re-stated with those preconditions made explicit before continuing to compression.

## Connections

- `frame-rotator` (binding-vow) — sibling reframing skill; often run together
- `steel-man-forge` (philosophy/dialectical-tools) — adjacent but different operation
- `assumption-excavator` (philosophy/logic) — escalation path for vague failure modes
- `statement-grader` (binding-vow) — downstream consumer; missing-preconditions feed the specificity and scope axes

## Sources

- Munger, C. (collected speeches and *Poor Charlie's Almanack*) — the canonical contemporary articulation of inversion as a thinking tool.
- Jacobi, C. G. J. — "Invert, always invert" — the historical mathematical anchor.
- Heath, C. & Heath, D. (2013). *Decisive*. — pre-mortem as the structured form of inversion in decision contexts.
