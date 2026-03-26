---
name: brand-identity
description: >
  Direct the brand-identity subdomain — route brand questions to the right specialist
  skill, define the relationship between brand strategy and visual execution, and resolve
  conflicts between brand consistency and creative expression. Use when the user has a
  branding question and you need to determine which knowledge skill to consult.
tools: Read, Glob
---

# Brand Identity Director

The department head for brand identity within the design domain. Routes questions to the right specialist, defines the learning order, and ensures brand decisions cascade consistently across all touchpoints.

## Routing Logic

When a brand question arrives, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Brand values, positioning, audience, mission, personality | `brand-foundations` | Strategic layer — must be defined before visual execution |
| Logo, color palette, imagery style, iconography, brand marks | `visual-identity` | Visual execution of brand strategy |
| Tone, writing style, messaging, taglines, content voice | `brand-voice` | Verbal execution of brand strategy |
| "Build me a brand" (vague) | `brand-foundations` first | Strategy must precede execution |
| "Redesign our logo" | `visual-identity`, but check `brand-foundations` first | Visual changes must align with strategy |
| Brand guidelines / style guide | All three skills | Guidelines synthesize all layers |

### Multi-Skill Questions

Brand work almost always requires multiple skills. Load in this priority:
1. `brand-foundations` — understand the strategic positioning
2. `visual-identity` — translate strategy into visual systems
3. `brand-voice` — translate strategy into verbal systems

This order ensures strategy constrains execution. Never design a logo without knowing the brand's values. Never write copy without knowing the brand's voice.

### Cross-Subdomain Routing

Brand identity touches every other design subdomain:
- **Brand + typography**: Route typeface selection to `typography` director, but brand-voice and brand-foundations inform the emotional requirements
- **Brand + color**: Route palette decisions to `visual-communication` for color theory, but `visual-identity` defines the brand's color system
- **Brand + layout**: Route to `visual-communication` for hierarchy/composition, `visual-identity` for brand-specific layout patterns

**Critical rule**: Brand foundations act as constraints on all other design decisions. When a color-theory skill suggests a palette that conflicts with brand positioning, brand foundations win. The brand is the organizing principle.

## Curriculum Order

For learning or progressive loading:

1. **Brand Foundations** (strategy) — What the brand stands for. Values, audience, positioning, personality. Without this, visual and verbal decisions are arbitrary.
2. **Visual Identity** (visual execution) — How the brand looks. Logo systems, color, imagery, iconography. Translates strategy into visual language.
3. **Brand Voice** (verbal execution) — How the brand speaks. Tone, vocabulary, messaging frameworks. Translates strategy into written and spoken language.

### Level Progression
- **Foundational**: brand-foundations, visual-identity, brand-voice (current skills)
- **Intermediate**: (future) brand systems at scale, multi-brand architecture, brand evolution
- **Advanced**: (future) brand valuation, cultural positioning, brand as business strategy

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Visual identity says "minimalist mark" but brand foundations says "playful, expressive" | Foundations wins — find a minimalist approach that still feels playful | Strategy overrides aesthetic preference |
| Brand voice says "formal" but visual identity uses casual illustration | Reconcile — formality in voice doesn't require formality in visuals, but flag the tension | Voice and visuals can contrast intentionally |
| Visual identity says "blue palette" but color theory says "blue conveys wrong emotion for this audience" | Escalate to brand foundations — re-examine the color rationale against positioning | Strategy arbitrates when execution skills disagree |

**General rule**: foundations > visual identity = brand voice. Strategy is the arbiter. Visual and verbal are parallel execution layers — neither outranks the other, but both answer to the strategic layer.

## Scope Boundaries

**This director handles**: All brand-level decisions — positioning, identity systems, voice guidelines, and brand consistency across touchpoints.

**Escalate to the orchestrator when**:
- The question spans brand + another subdomain (e.g., "design a branded landing page" involves layout + type + brand)
- The user needs a full brand system built from scratch (orchestrator coordinates the multi-subdomain effort)
- Brand decisions require market research or competitive analysis beyond design expertise
