---
name: statement-grader
description: >
  Score a problem statement on six axes — specificity, falsifiability, scope, audience-fit,
  answerability, root-vs-symptom — using calibrated 1-5 rubrics. Use as the keystone audit
  step in binding-vow's six-eyes orchestrator, or directly when checking whether a problem
  statement is good enough to act on. Returns per-axis scores plus reformulation hints;
  any axis below 3/5 triggers the re-state loop.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Statement Grader — The Keystone Audit

Six-axis quality scoring for problem statements. The grader is the keystone of binding-vow: every other audit skill targets one or more of its axes, and the re-state loop gates on its output. A statement that scores ≥3/5 on every axis is action-ready; any sub-threshold axis triggers reformulation.

The full per-axis calibration rubric lives in `references/grader-axes.md` — read it directly when scoring. This SKILL.md describes *process*, not *rubrics*.

## The Six Axes

| Axis | Question it answers | Failure signal |
|---|---|---|
| **Specificity** | Is the statement precise enough to act on? | Vague verbs, fuzzy nouns, undefined terms |
| **Falsifiability** | Could observation prove this wrong? | Tautology, circular, immune to evidence |
| **Scope** | Are time/population/context boundaries explicit? | Implicit "everyone, always, everywhere" |
| **Audience-fit** | Does the statement match its target audience's frame? | Wrong shape (LLM gets prose; exec gets decomposition) |
| **Answerability** | Could any evidence resolve this? | Values-disguised-as-fact; no resolution pathway |
| **Root-vs-symptom** | Is this addressing the actual cause or a downstream effect? | XY pattern; one-level-too-shallow framing |

## Process

### Step 1 — Read `references/grader-axes.md`

Each axis has a 1-5 calibrated rubric with example statements at each score level. Score level 3 is the action-ready threshold; below 3 triggers re-state.

### Step 2 — Score each axis independently

For each of the six axes:

1. **Read the axis's rubric** (in `references/grader-axes.md`)
2. **Match the statement** against the closest score level (1 = catastrophic failure, 5 = exemplary)
3. **Note the specific signal** — what concrete property of the statement justifies this score?
4. **Surface the gap** if score < 3 — what would move it to 3+?

Score axes independently. Do not let one axis's score anchor another. Specifically:
- A statement can be highly specific *and* unfalsifiable (precision without empirical content)
- A statement can be perfectly answerable *and* a Type III error (right answer to wrong question — root-vs-symptom catches this)
- A statement can fit its audience *and* conflate root with symptom (audience-fit ≠ correctness)

### Step 3 — Compute the gate

| Pattern | Gate result |
|---|---|
| All six axes ≥3/5 | **Pass** — statement is action-ready; no re-state needed |
| One or two axes <3/5 | **Local fail** — trigger re-state at Level 1 (rephrase) or Level 2 (decompose) |
| Three or more axes <3/5 | **Structural fail** — trigger re-state at Level 3 (depth upgrade) |
| Any axis at 1/5 | **Catastrophic fail** — even if other axes pass; trigger re-state at Level 3 minimum |

The "any axis below 3 triggers re-state" rule is non-negotiable. A statement that scores 5/5/5/5/5/2 still re-states; it just re-states on the root-vs-symptom axis specifically.

### Step 4 — Generate reformulation hints

For each sub-threshold axis, produce a hint:

- **Specificity** — list the vague terms; suggest replacements
- **Falsifiability** — name an observation that would refute the claim; if none exists, suggest reframing as values/preferences
- **Scope** — surface the missing time/population/context; ask which is intended
- **Audience-fit** — identify the audience mismatch; suggest the right structure (BLUF / SCQA / Pyramid / Anthropic-canonical)
- **Answerability** — name the evidence type that would resolve; if none exists, flag as values-question
- **Root-vs-symptom** — propose a candidate Y (the underlying goal); apply XY-detector framing

Hints feed the re-state loop. Loop back to Phase 4 (Reframe) with the hints as input, not just the failure flags.

### Step 5 — Output the grade card

Produce a structured output:

```
STATEMENT GRADE — [first 60 chars of statement...]
─────────────────────────────────────────────
Specificity      [score]/5  | [signal]                          [hint if <3]
Falsifiability   [score]/5  | [signal]                          [hint if <3]
Scope            [score]/5  | [signal]                          [hint if <3]
Audience-fit     [score]/5  | [signal]                          [hint if <3]
Answerability    [score]/5  | [signal]                          [hint if <3]
Root-vs-symptom  [score]/5  | [signal]                          [hint if <3]

Gate: [pass | local fail | structural fail | catastrophic]
Re-state level recommended: [none | L1 | L2 | L3]
Reformulation hints:
  - [hint 1]
  - [hint 2]
  ...
```

## Threshold Rule

The 3/5 threshold is the calibrated action-ready level. Score 3 means: "this axis would not actively mislead a downstream solver, but it's not exemplary either." That's the bar a statement needs to clear on every axis.

The threshold is intentionally per-axis, not aggregate. A statement that averages 4 but has a 1 on root-vs-symptom is an XY problem in disguise — the average masks the catastrophic failure. Per-axis gating prevents this.

## Calibration

Score 1 (catastrophic) and score 5 (exemplary) anchor the scale. The middle scores require calibration against examples in `references/grader-axes.md`. When uncertain between two adjacent scores, default to the lower — strictness on this axis pays for itself in re-state loop savings.

For domain-specific calibration (clinical, investing, essay, etc.), consult [[binding-vow-build-plan-v2]] for the deferred-to-v3 domain-specific reframer modules. Until those exist, use the general rubric and flag domain-specificity as a meta-note in the grade card.

## Output Contract for `six-eyes`

When called from `six-eyes` Phase 6, return:

- The structured grade card
- The Gate result (pass / local fail / structural fail / catastrophic)
- The recommended re-state level (none / L1 / L2 / L3)
- Reformulation hints keyed by axis (for the loop's input to Phase 4)

`six-eyes` uses the Gate result to decide whether to enter the re-state loop and at which Level. It uses the hints to seed the next iteration's reframe.

## Failure Modes

| Failure | Response |
|---|---|
| Statement is too short to score (single word, single phrase) | Return an "ungraded" verdict and route back to Phase 1 (Intake) for restatement |
| Two axes seem identical for this statement (e.g., specificity and scope co-vary) | Score both anyway; the rubric is designed to keep them independent. If genuinely tangled, note in the signal field and proceed |
| All six axes score 5 on first pass | Re-check — this is rare. Possible XY pattern or anchoring effect. Apply `xy-detector` before declaring pass |
| Score is unstable across re-runs on the same statement | Calibration drift. Re-read `references/grader-axes.md` and rescore using the canonical examples |

## Connections

- `six-eyes` (binding-vow) — calls this in Phase 6; gates re-state loop on output
- `xy-detector`, `answerability-tester`, `falsifiability-checker`, `scope-bounder` (binding-vow) — feed signals to specific axes
- `kahneman-framing` (binding-vow) — the four cognitive failure modes the grader's rubric is calibrated against
- `argument-analyst` (philosophy/logic) — adjacent skill; argument-analyst grades arguments, statement-grader grades problem statements

## Sources

- The six axes are derived from synthesizing: Polya 1945 (Step 1 verification), Popper 1959 (falsifiability), Mitroff & Kilmann 1978 (Type III), Minto 1987 (audience-fit), Reiter-Palmon 2017 (problem construction quality).
- Calibration anchors in `references/grader-axes.md` draw from worked examples in [[binding-vow-research-findings]].
