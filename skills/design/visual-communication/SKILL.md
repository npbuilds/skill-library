---
name: visual-communication
description: >
  Direct the visual communication subdomain — route design questions to the right specialist
  skill, define the learning curriculum, and resolve conflicts between visual design principles.
  Use when the user has a visual design question and you need to determine which knowledge
  skill (color theory, design principles, or visual perception) to consult.
tools: Read, Glob
---

# Visual Communication Director

The department head for visual communication within the design domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Color palettes, harmony, contrast ratios, hue/saturation | `color-theory` | Color-specific methodology |
| Layout, alignment, whitespace, visual hierarchy, grid | `design-principles` | Structural composition |
| Eye tracking, readability, attention flow, visual weight | `visual-perception` | Perceptual science |
| Accessibility, WCAG compliance | `visual-perception` first, then `color-theory` | Perception defines the problem, color solves it |
| "Make this look better" (vague) | All three, in curriculum order | Needs holistic assessment |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:
1. `visual-perception` — understand how the human eye will process it
2. `design-principles` — apply structural rules
3. `color-theory` — refine the color decisions

This order ensures perception constrains principles, and principles constrain color — not the reverse.

## Curriculum Order

For learning or progressive loading:

1. **Visual Perception** (foundation) — How humans see. Without this, design principles are arbitrary rules.
2. **Design Principles** (application) — How to structure visual information. Builds on perception science.
3. **Color Theory** (specialization) — How to work with color. Most effective when you understand why colors work perceptually.

### Level Progression
- **Foundational**: All three current skills are foundational level
- **Intermediate**: (not yet built) Typography, responsive design, motion design
- **Advanced**: (not yet built) Brand systems, design systems, generative design

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Color theory says "use high saturation" but perception says "causes eye strain" | Perception wins | Human limits override aesthetic preference |
| Design principles say "minimize elements" but color theory says "use 5-color palette" | Design principles wins | Simplicity is structural; color serves structure |
| Perception says "readers scan F-pattern" but design principles say "center-align" | Perception wins | Empirical science overrides convention |

**General rule**: When in doubt, perception > principles > color. The human eye is the final arbiter.

## Scope Boundaries

**This director handles**: All visual design questions within the static/2D domain — layout, color, typography fundamentals, readability, accessibility.

**Escalate to the orchestrator when**:
- The question involves animation or motion (interaction design subdomain)
- The question involves brand strategy, not just brand visuals
- The question spans multiple subdomains (e.g., "design a complete app")
- The user needs a specialist agent launched (only orchestrators launch agents)
