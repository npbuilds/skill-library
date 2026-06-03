---
name: problem-reframing
description: >
  Route a decomposed problem to the right reframing technique — alternative formulations,
  Munger inversion, stakeholder rotation, and the framing-effects reference. Activate at
  six-eyes Phase 4 (Reframe) when you need to expose that the current formulation is not the
  only one, or when a statement feels stuck or one-sided. This director owns the "is this even
  the right framing?" question.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Problem Reframing — Director

Most problems arrive pre-framed, and the frame is usually invisible to the person who set it.
This director realizes six-eyes' Phase 4 (Reframe): it rotates the formulation through
alternative frames, inverts it to surface failure preconditions, rotates the centered
stakeholder, and grounds the work in the cognitive science of framing effects. The output is
2–3 genuinely different formulations the orchestrator can choose among.

Reframing is where wicked and contested problems earn their keep — a better frame often dissolves
the difficulty that decomposition alone could not.

## Routing Table

| Child skill | Use when | Output |
|---|---|---|
| `frame-rotator` | You need 2–3 alternative formulations (IDEO "How Might We", Polya specialize/generalize) | Alternative problem statements |
| `inversion-tool` | You want to surface preconditions for success by asking what would guarantee failure (Munger) | Inverted failure modes → negated success conditions |
| `stakeholder-rotator` | You need to surface whose interests the current framing centers and whose it hides | A stakeholder map with the invisible parties named |
| `kahneman-framing` | You need the conceptual basis for framing effects, attribute substitution, or the Einstellung effect | Reference: framing/substitution/fixedness |

## Routing Logic

1. Start with `frame-rotator` to generate alternatives; pull `kahneman-framing` to name the
   cognitive trap the original frame fell into.
2. Run `inversion-tool` for high-stakes or "we've been stuck on this" statements.
3. Run `stakeholder-rotator` whenever the problem touches multiple parties — it calls
   philosophy/ethics/values-excavator cross-domain to surface hidden interests.
4. Hand the candidate frames back to `six-eyes`; if the reframe itself is contested, the
   orchestrator escalates to the philosophy dialectic skills.

## Scope Boundaries

- **In scope:** generating and grounding alternative formulations.
- **Out of scope:** scoring the resulting statement (→ `statement-audit`), shaping it for an
  audience (→ `statement-compression`).
- **Escalate to `six-eyes`** when reframing reveals the problem is wicked enough to warrant a
  full deep-lane pass.
