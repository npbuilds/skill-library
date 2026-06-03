---
name: statement-audit
description: >
  Route a candidate problem statement through the audit battery — XY-pattern detection,
  answerability, falsifiability, scope bounding, and the six-axis grader. Activate at six-eyes
  Phase 6 (Audit) to catch the standard failure modes before a statement is accepted, and to
  decide whether the re-state loop must fire. This director owns the "is this statement actually
  sound?" question.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Statement Audit — Director

The last line of defense before a statement is handed to a solver. This director realizes
six-eyes' Phase 6 (Audit): it runs the candidate statement through the standard failure-mode
checks and ends with the six-axis grader whose sub-threshold result triggers the re-state loop.
Audit is adversarial by design — its job is to *break* the statement, not to bless it.

## Routing Table

| Child skill | Checks for | Trigger if it fails |
|---|---|---|
| `xy-detector` | Asking about an attempted solution rather than the real goal | Return the inferred underlying goal; re-state |
| `answerability-tester` | Could any evidence in principle resolve this? | Unanswerable → reframe or narrow |
| `falsifiability-checker` | What observation would prove it wrong? (Popper) | Unfalsifiable → tighten the claim |
| `scope-bounder` | Are time / population / context boundaries explicit? | Unbounded → add scope |
| `statement-grader` | Six axes: specificity, falsifiability, scope, audience-fit, answerability, root-vs-symptom | Any axis < 3/5 → re-state loop |

## Routing Logic

1. Run the checks in order — `xy-detector` first (an XY pattern invalidates everything
   downstream), then answerability, falsifiability, scope.
2. End with `statement-grader`. Any axis below 3/5 returns control to `six-eyes`, which re-enters
   Phase 4 (Reframe) with the failure diagnosis as input. Cap at 3 iterations.
3. Surface the per-axis scores so the convergence trajectory is auditable, never loop silently.

## Scope Boundaries

- **In scope:** validating logic, answerability, falsifiability, scope, and overall quality.
- **Out of scope:** generating fixes (→ `problem-reframing`), shaping the output
  (→ `statement-compression`). Audit *diagnoses* failure; the orchestrator routes the fix.
- **Escalate to `six-eyes`** on multi-axis failure across iterations — that signals a deep-lane
  upgrade, not another cosmetic re-state.
