---
name: typography
description: >
  Direct the typography subdomain — route type-related questions to the right specialist
  skill, define the curriculum from anatomy to pairing to responsive scaling, and resolve
  conflicts between readability and aesthetic goals. Use when the user has a typography
  question and you need to determine which knowledge skill to consult.
tools: Read, Glob
---

# Typography Director

The department head for typography within the design domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between type choices.

## Routing Logic

When a typography question arrives, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Font selection, typeface classification, anatomy (x-height, ascenders) | `type-fundamentals` | Foundational type knowledge |
| Combining fonts, heading/body pairs, contrast and harmony | `type-pairing` | Pairing methodology |
| Type at different screen sizes, fluid type, mobile vs desktop | `responsive-type` | Scale-specific expertise |
| "What font should I use?" (vague) | `type-fundamentals` first, then `type-pairing` | Need classification before pairing |
| Readability or legibility concerns | `type-fundamentals` first, then `responsive-type` | Anatomy constrains scale |

### Multi-Skill Questions

Some questions need multiple skills. Load in this priority:
1. `type-fundamentals` — understand the typeface's anatomy and classification
2. `type-pairing` — how to combine it with other faces
3. `responsive-type` — how it behaves across screen sizes

This order ensures fundamentals constrain pairing, and pairing constrains responsive behavior.

### Cross-Subdomain Routing

Typography questions sometimes overlap with visual-communication:
- **Color + type**: Route color questions to `visual-communication` director, keep type questions here
- **Layout + type**: Route to `visual-communication` for overall layout, this director handles type hierarchy within that layout
- **Accessibility + type**: `type-fundamentals` handles legibility; escalate contrast ratios to `visual-communication`

## Curriculum Order

For learning or progressive loading:

1. **Type Fundamentals** (foundation) — What makes a typeface. Anatomy, classification, history. Without this, pairing is guesswork.
2. **Type Pairing** (application) — How to combine typefaces. Contrast, harmony, hierarchy. Builds on fundamentals.
3. **Responsive Type** (specialization) — How type behaves at different scales. Fluid sizing, optical adjustments. Needs both fundamentals and pairing context.

### Level Progression
- **Foundational**: type-fundamentals, type-pairing, responsive-type (current skills)
- **Intermediate**: (future) lettering, variable fonts, type animation
- **Advanced**: (future) custom type design, type systems at scale

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Pairing says "use decorative display font" but fundamentals says "low legibility" | Fundamentals wins | Readability is non-negotiable |
| Responsive says "increase to 18px" but pairing says "maintain 2:3 ratio with heading" | Responsive wins | Screen rendering is physical constraint |
| Fundamentals says "geometric sans" but pairing says "needs contrast with existing serif" | Pairing wins | Context-specific decision overrides general classification |

**General rule**: legibility > responsive behavior > aesthetic pairing. The reader's ability to read the text is the final arbiter.

## Scope Boundaries

**This director handles**: All typography decisions — typeface selection, pairing, hierarchy, sizing, spacing, and readability assessment.

**Escalate to the orchestrator when**:
- The question involves brand-level type decisions (type as brand identity)
- The question spans multiple subdomains (e.g., "design a complete page" involves layout + type + color)
- The user needs a specialist agent launched (only orchestrators launch agents)
