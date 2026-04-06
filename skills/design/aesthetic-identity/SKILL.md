---
name: aesthetic-identity
description: >
  A living model of the user's evolving visual aesthetic — dimensional fingerprint, palette
  tendencies, compositional preferences, and motion feel. Consult before any creative output
  to ground design decisions in the user's established (and evolving) identity. Activates
  when setting creative direction, choosing palettes, establishing mood, or when any design
  skill needs a starting point that reflects the user rather than generic defaults.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Aesthetic Identity — The Living Style Fingerprint

Your aesthetic isn't static. It drifts, sharpens, pivots, and deepens over time. This skill maintains a dimensional model of your current visual identity — not as rigid rules, but as a gravitational field that creative decisions fall toward unless deliberately pushed away.

Every design skill should consult this before defaulting to generic choices.

## The Dimensional Model

Each dimension is a spectrum between two poles. Your position is a float (0.0–1.0) with a **confidence** score (0.0 = no data, 1.0 = highly consistent pattern). Low-confidence dimensions are flexible starting points. High-confidence dimensions are strong defaults that should only be overridden with intent.

Read `references/dimension-registry.md` for the full set of active dimensions with current positions and confidence.

Read `references/current-profile.md` for the synthesized profile — the human-readable summary of what the dimensions mean in practice.

### How Dimensions Work

**Seeded dimensions** ship with the system as reasonable starting axes for visual identity. They cover the most common aesthetic differentiators. All start at 0.5 (neutral) with 0.0 confidence (unknown).

**Discovered dimensions** emerge when the observer detects a consistent pattern that doesn't map to existing axes. For example, if the user consistently chooses circular/radial compositions over rectilinear ones, the observer may propose a "Rectilinear ↔ Radial" dimension. Discovered dimensions start with the evidence that triggered them.

**Dimension lifecycle:**
1. **Proposed** — observer detects pattern, suggests new dimension with evidence
2. **Active** — accumulating data, confidence rising
3. **Stable** — high confidence, strong default
4. **Dormant** — confidence decaying because recent work doesn't engage this axis

### Reading the Profile

When consulting the aesthetic identity for a creative decision:

1. Read `references/current-profile.md` for the narrative summary
2. For specific decisions, check the relevant dimension(s) in `references/dimension-registry.md`
3. High-confidence dimensions (>0.7) → use as strong defaults, note in creative brief
4. Medium-confidence (0.3–0.7) → use as soft suggestions, open to override
5. Low-confidence (<0.3) → treat as neutral, don't constrain

### Applying the Profile

The profile translates to concrete creative decisions:

**Palette selection:** Temperature, Chromatic Range, and Contrast dimensions → narrow the palette search space. "Warm, muted, medium-contrast" is a much more useful starting point than "choose a palette."

**Composition:** Density, Symmetry, and Depth dimensions → guide spatial arrangement before any content is placed.

**Motion:** The Motion Feel dimension plus any discovered motion-specific axes → set easing curves, transition speeds, animation density.

**Typography:** Cross-reference with typography director. Precision and Temporal Register dimensions influence whether type feels mechanical or humanist, retro or contemporary.

**Mood anchors:** Emotional Register plus the narrative summary in current-profile.md → generate the 3–5 adjective anchors that orchestrators pass to sub-agents.

## Integration Points

**Design Orchestrator** — Phase 2.5 (after classify, before set direction): read profile, pre-populate creative brief fields, flag any dimension with high confidence as a default.

**Master Artificer** — Phase 1 (Divine the Intent): read profile to inform the Artifact Blueprint's Visual Direction. If the user doesn't specify mood/palette/motion, the profile fills the gaps.

**Style Evolution Observer** — after every creative output, observer reads what was built, maps it to dimensional positions, and updates confidence scores.

## What This Skill Does NOT Do

- Generate designs (consult design-orchestrator or master-artificer)
- Override explicit user direction (profile is a default, not a constraint)
- Track non-visual preferences (use writing domain's style-dna for prose)
- Make judgments about quality (the profile is descriptive, not evaluative)
