# Statement Grader — Quick Reference


## The Six Axes

| Axis | Question it answers | Failure signal |
|---|---|---|
| **Specificity** | Is the statement precise enough to act on? | Vague verbs, fuzzy nouns, undefined terms |
| **Falsifiability** | Could observation prove this wrong? | Tautology, circular, immune to evidence |
| **Scope** | Are time/population/context boundaries explicit? | Implicit "everyone, always, everywhere" |
| **Audience-fit** | Does the statement match its target audience's frame? | Wrong shape (LLM gets prose; exec gets decomposition) |
| **Answerability** | Could any evidence resolve this? | Values-disguised-as-fact; no resolution pathway |
| **Root-vs-symptom** | Is this addressing the actual cause or a downstream effect? | XY pattern; one-level-too-shallow framing |

## Step 3 — Compute the gate

| Pattern | Gate result |
|---|---|
| All six axes ≥3/5 | **Pass** — statement is action-ready; no re-state needed |
| One or two axes <3/5 | **Local fail** — trigger re-state at Level 1 (rephrase) or Level 2 (decompose) |
| Three or more axes <3/5 | **Structural fail** — trigger re-state at Level 3 (depth upgrade) |
| Any axis at 1/5 | **Catastrophic fail** — even if other axes pass; trigger re-state at Level 3 minimum |

## Failure Modes

| Failure | Response |
|---|---|
| Statement is too short to score (single word, single phrase) | Return an "ungraded" verdict and route back to Phase 1 (Intake) for restatement |
| Two axes seem identical for this statement (e.g., specificity and scope co-vary) | Score both anyway; the rubric is designed to keep them independent. If genuinely tangled, note in the signal field and proceed |
| All six axes score 5 on first pass | Re-check — this is rare. Possible XY pattern or anchoring effect. Apply `xy-detector` before declaring pass |
| Score is unstable across re-runs on the same statement | Calibration drift. Re-read `references/grader-axes.md` and rescore using the canonical examples |
