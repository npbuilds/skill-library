---
name: stakeholder-rotator
description: >
  Thin wrapper over philosophy/ethics/values-excavator with binding-vow problem-statement
  framing. Surfaces whose interests are centered in the current formulation, whose are
  invisible, and what alternative formulations would center different stakeholders. Use
  during binding-vow's Phase 4 reframing, especially for adaptive or wicked-typology problems.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Stakeholder Rotator — Re-state from Each Affected Party's Perspective

A thin coordinator that calls `values-excavator` (philosophy/ethics) with problem-statement framing and turns its output into alternative formulations that center different stakeholders.

The actual values excavation is done by `values-excavator`. This skill's value is the *translation* — surfacing whose perspective is centered in the current formulation and producing alternative statements from other parties' frames.

Most useful for **adaptive** typology (Heifetz: stakeholder interests ARE the problem) and **wicked** typology (Rittel: stakeholders define the problem differently). For well-defined or ill-defined typologies, this skill rarely changes the framing meaningfully.

## Process

1. **Call `values-excavator`** (cross-domain — philosophy/ethics) with the problem statement and any context.
2. **Receive**: implicit values, competing goods, whose interests are centered vs invisible, the moral logic of the position.
3. **Identify the implicit primary stakeholder** in the current formulation. Whose problem is this stated as?
4. **For each invisible-but-affected stakeholder**, produce an alternative formulation stated from that stakeholder's perspective.
5. **Cap at 3–4 alternatives** to avoid noise. Pick the stakeholders whose interests are most materially affected by the decision.
6. **Note tensions** between stakeholder perspectives — these are the actual contested questions inside the problem.

## Output Format

```
STAKEHOLDER ROTATION — [first 60 chars of statement...]
─────────────────────────────────────────────
Primary stakeholder (implicit in original): [whose problem this is, as stated]
Affected but invisible stakeholders: [list, from values-excavator]

Rotated formulations:
  From [stakeholder 1]'s perspective: [restated statement]
    What changes: [different success criteria / different acceptable solutions]
  From [stakeholder 2]'s perspective: [restated statement]
    What changes: [...]
  From [stakeholder 3]'s perspective: [restated statement]
    What changes: [...]

Tensions surfaced: [conflicts between perspectives — these are the contested questions]
Recommended: [whether the original framing is defensible, needs widening, or needs
              explicit acknowledgment of which stakeholder it serves]
```

## When to Run This Skill

| Typology / context | Run? |
|---|---|
| Adaptive (Heifetz) | **Mandatory** — adaptive problems require stakeholder rotation by definition |
| Wicked (Rittel) | **Mandatory** — wicked problems have contested formulations across stakeholders |
| Mess (Ackoff) | Recommended — the mess often is the stakeholder conflict |
| Ill-defined | Optional — depends on whether stakeholders are material |
| Well-defined | Skip — stakeholders are typically clear |
| Audience tag `public` | Recommended regardless of typology — public problems implicate broader stakeholder sets |

## Failure Modes

| Failure | Response |
|---|---|
| `values-excavator` unavailable | Surface a degraded version: ask "whose interests are centered? Whose are invisible?" inline without the full values framework |
| Only one stakeholder is affected (truly individual problem) | Return "no rotation needed" rather than fabricating stakeholders |
| Stakeholder set is so broad that 5+ rotations would be needed | Group stakeholders into 2–3 classes (e.g., "users", "operators", "regulators") and rotate per class |

## Output Contract for `six-eyes`

Called from Phase 4 (Reframe) when typology is adaptive or wicked, or when audience is public. Returns rotated formulations and surfaced tensions. The orchestrator may use a rotated formulation as the new working statement if it scores better on `statement-grader`, or surface the tensions as decision-relevant context for compression.

## Scope Boundaries

- **stakeholder-rotator handles:** translating problem-statement framing to/from `values-excavator`'s input/output formats.
- **stakeholder-rotator does NOT:** judge which stakeholder's framing is "right" — that's a values question for the user. Surfaces all reasonable framings; lets the user choose.

## Connections

- `values-excavator` (philosophy/ethics) — primary cross-domain call
- `problem-typology` (binding-vow) — upstream input; adaptive/wicked typologies trigger this skill
- `frame-rotator` (binding-vow) — sibling reframing skill; complements stakeholder rotation
- `inversion-tool` (binding-vow) — sibling reframing skill
- `wicked-vs-tame` (binding-vow) — foundational reference for when stakeholder rotation is structural vs decorative

## Sources

- Heifetz, R. A. (1994). *Leadership Without Easy Answers*. (Stakeholder work is the adaptive work.)
- Rittel & Webber 1973. (Wicked problems have stakeholder-divergent formulations.)
- See [[wicked-vs-tame]] and `values-excavator` (philosophy/ethics) for the full framework this skill coordinates with.
