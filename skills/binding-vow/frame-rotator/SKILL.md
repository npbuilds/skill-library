---
name: frame-rotator
description: >
  Produce 2-3 alternative formulations of a problem statement using IDEO's How Might We
  formula, Polya's specialize/generalize operations (level-shifting), and
  assumption-excavator-driven framing rotation. Use during binding-vow's Phase 4 reframing.
  Returns alternative formulations each with one-line rationale and the framing assumption
  being relaxed or shifted.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Frame Rotator — Alternative Formulations

A problem statement is one of many possible formulations. The framing chooses what counts as relevant and constrains the solution space. Frame-rotator rotates through alternatives that would lead to different solution spaces. The goal isn't to find "the right framing" — that's downstream — but to expose that the original framing is not unique.

The skill applies three rotation operations: How Might We (IDEO), level-shifting (Polya specialize/generalize), and framing-assumption swap (via `assumption-excavator`). Most useful alternatives come from a mix of all three.

## The Three Rotation Operations

### 1. HMW (How Might We) — IDEO

Reformulate the statement using the canonical HMW formula:

```
How might we [intended action verb] for [potential user/subject]
so that [desired outcome]?
```

The verbs are deliberately exploratory: "explore", "enable", "remove the need for", "redesign", "reframe", "delight". *Not* "build", "implement", "fix" — those are mechanism-shaped, not goal-shaped.

The "might" matters: it preserves multiple possible solutions. "How do we" forecloses; "how might we" opens.

### 2. Level-shifting — Polya specialize/generalize

Two opposite moves Polya named in *How to Solve It*:

| Move | What it does | When it helps |
|---|---|---|
| **Specialize** | Narrow to a specific case, smaller scope, single instance | Original feels too abstract to act on; need a concrete starting point |
| **Generalize** | Broaden to a class of cases, larger scope, abstraction up | Original feels too narrow; solving the general case might be easier than the specific one (Polya's counterintuitive move) |

For each statement, both directions are valid candidates. The skill produces at least one of each on deep-mode runs.

### 3. Framing-assumption swap

Call `assumption-excavator` (philosophy/logic) with `depth=deep, category=framing`. Receive:
- The framing assumption(s) the statement makes
- Counterfactuals: "if this framing assumption is false, then [consequence]"

For each contestable framing assumption, produce an alternative formulation that *swaps* that assumption. Example: a statement framed as "engagement optimization" might be rotated to a "wellbeing optimization" framing — the metric (and so the solution space) changes.

## Process

1. **Verify input** is an audited statement (from `statement-grader`). Unaudited input gets routed back.
2. **Run HMW reformulation** — at least one alternative.
3. **Run level-shifting** — at least one specialize and one generalize alternative.
4. **Call `assumption-excavator`** with `depth=deep, category=framing`. Receive the framing assumptions.
5. **For each load-bearing framing assumption**, produce an alternative that swaps it.
6. **Deduplicate** — collapse near-identical alternatives. Aim for 2–3 *meaningfully different* formulations in standard mode; ≥3 in deep mode.
7. **Diff-check** — confirm each alternative is *structurally different* from the original, not just lexically rephrased.

## The Diff-Check Discipline

A frame rotation must change *what counts as a solution*, not just what words describe the problem. The diff-check question: would a downstream solver propose a *different solution* given the alternative formulation? If no, the rotation is cosmetic, not structural. Discard.

Example (cosmetic, fails check):
- Original: "Reduce customer churn"
- Alternative: "Decrease the rate at which customers leave"
- → Same solution space. Reject.

Example (structural, passes check):
- Original: "Reduce customer churn"
- Alternative (specialize): "Reduce churn specifically in the first 30 days post-signup"
- Alternative (generalize): "Improve the customer's *value-realization curve* — churn is one symptom"
- Alternative (framing swap): "Stop optimizing for retention; optimize for the customers we actually want to retain"
- → All three open different solution spaces. Pass.

## Output Format

```
FRAME ROTATION — [first 60 chars of original statement...]
─────────────────────────────────────────────
Original framing:        [the statement as input]
Framing assumption(s):   [from assumption-excavator — what's being assumed]

Alternative 1 (HMW):
  Formulation: [rewritten as HMW]
  Operation:   How Might We
  What changes: [what assumption is relaxed; what solution space opens]
  Diff-check: pass

Alternative 2 (Specialize):
  Formulation: [narrower version]
  Operation:   Specialize
  What changes: [the narrowing dimension; why the smaller case is more tractable]
  Diff-check: pass

Alternative 3 (Generalize):
  Formulation: [broader version]
  Operation:   Generalize
  What changes: [the abstraction; what becomes solvable at the higher level]
  Diff-check: pass

[Optional, deep mode] Alternative 4 (Framing swap):
  Formulation: [swapped framing]
  Operation:   Framing assumption swap
  Original assumption: [what's being swapped]
  What changes: [new solution space]
  Diff-check: pass

Diff-check failures: [list of generated alternatives that were cosmetic-only and were rejected]
```

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

## Output Contract for `six-eyes`

Called from Phase 4 (Reframe). Returns 2–3 (standard) or ≥3 (deep) alternative formulations. Each is a candidate for `six-eyes` to grade via `statement-grader`. If any alternative scores better than the original on the audit axes, that alternative becomes the new working statement for downstream phases.

## Connections

- `assumption-excavator` (philosophy/logic) — primary cross-domain call for framing-assumption excavation
- `polya-method` (binding-vow) — foundational reference for specialize/generalize operations
- `inversion-tool` (binding-vow) — sibling reframing skill (Munger inversion is complementary to HMW)
- `stakeholder-rotator` (binding-vow) — sibling for stakeholder-perspective rotation
- `statement-grader` (binding-vow) — downstream consumer; grades each alternative
- `claim-decomposer` (research) — escalation path when rotation fails due to narrow scope

## Sources

- IDEO / d.school — *How Might We* methodology. ([designkit.org](https://www.designkit.org/methods/how-might-we.html))
- Pólya, G. (1945). *How to Solve It*. — specialize/generalize heuristic family.
- See [[polya-heuristics-catalog]] in skill-lab for the catalog of Polya heuristics this skill draws from.
