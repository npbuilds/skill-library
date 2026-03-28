---
name: visual-composer
description: >
  Knowledge skill for artifact layout, composition, visual rhythm, and
  typography-as-art. Covers grid-breaking layouts, spatial arrangement,
  density control, visual tension, and the compositional principles that
  make artifacts feel intentional rather than assembled. Consulted by
  the Master Artificer when visual arrangement decisions are needed.
---

# Visual Composer — The Architecture of Seeing

How elements are arranged in space determines whether an artifact feels designed or dumped. Composition is the skeleton — animation, color, and interaction are the flesh. Get the skeleton wrong and nothing else matters.

## Composition Principles for Artifacts

### Visual Hierarchy — The Reading Order

Every artifact has a reading order, even non-textual ones. The eye follows a path. Design that path.

**Hierarchy tools (strongest to weakest):**
1. **Scale** — Bigger draws attention first
2. **Contrast** — High contrast against background demands focus
3. **Position** — Top-left (in LTR cultures) and center carry natural weight
4. **Isolation** — An element with space around it commands attention
5. **Motion** — Moving elements pull the eye (use with restraint)
6. **Color saturation** — Vivid against muted creates focal points
7. **Detail density** — Areas with more detail attract longer attention

**Rule:** An artifact should have exactly one primary focal point, 2-3 secondary elements, and everything else as supporting texture.

### Visual Tension — The Energy of Arrangement

Static, symmetrical layouts feel calm but lifeless. Tension creates energy.

**Tension sources:**
- **Asymmetric balance** — Unequal visual weight on either side of center, balanced by contrast or isolation
- **Edge proximity** — Elements near the viewport edge create anxiety/energy; centered elements create calm
- **Scale contrast** — Very large next to very small creates dramatic tension
- **Direction conflict** — Elements pointing in opposing directions create dynamic energy
- **Negative space** — Large empty areas create tension through anticipation
- **Breaking the grid** — One element that violates the established spatial system draws maximum attention

### Density and Breathing Room

**The density spectrum:**

```
Sparse          Balanced         Rich            Layered
─────────────────────────────────────────────────────────
Few elements    Comfortable      Many elements   Overlapping
Lots of space   Clear hierarchy  Dense but        Depth and
Minimal feel    Professional     organized        complexity
```

**Rules:**
- **Sparse:** Every element is precious. Placement must be precise. One pixel matters.
- **Balanced:** Follow grid systems. Use consistent spacing tokens (4px, 8px, 16px, 24px, 32px, 48px, 64px).
- **Rich:** Establish clear groupings. Use proximity and alignment to prevent overwhelm. Vary visual weight.
- **Layered:** Use depth (z-index, blur, opacity, scale) to create spatial hierarchy. Foreground, midground, background.

### Grid Systems for Artifacts

Not every artifact needs a grid — but every artifact needs spatial logic.

**When to use grids:**
- Multi-element layouts (dashboards, galleries, card collections)
- Text-heavy content (articles, documentation, narratives)
- Responsive layouts that must reflow predictably

**When to break grids:**
- Generative art (spatial logic comes from the algorithm)
- Immersive experiences (the viewport IS the canvas)
- Single-focus artifacts (one main element, nothing else to align)

**Grid vocabulary:**
- **CSS Grid:** For 2D layouts with explicit rows and columns
- **Flexbox:** For 1D distribution along a single axis
- **Subgrid:** For nested components that align with parent grid
- **Container queries:** For component-level responsive behavior
- **No grid:** For absolute/fixed positioning in canvas-like layouts

### Typography in Artifacts

Typography is not just text styling — it's a compositional element.

**Typography as structure:**
- Heading hierarchy creates the visual skeleton
- Font weight variation creates rhythm (light/regular/bold alternation)
- Line length affects reading comfort (45-75 characters optimal)
- Line height affects density (1.2 for headings, 1.5-1.6 for body)

**Typography as art:**
- Oversized type as the primary visual element
- Variable fonts with animated axes (weight, width, slant)
- Text as texture — repeating, overlapping, fading text as background
- Kinetic typography — text that moves, splits, reassembles
- Mixed type scales — extreme size contrast (12px body next to 200px display)

**Font pairing shortcuts:**
- **Technical/precise:** Monospace heading + sans-serif body
- **Warm/human:** Serif heading + sans-serif body
- **Modern/clean:** Geometric sans heading + humanist sans body
- **Bold/editorial:** Heavy sans or slab heading + light serif body
- **Minimal:** Single font family, multiple weights

### Color as Composition

Color creates spatial relationships:

- **Warm colors advance** — elements feel closer to the viewer
- **Cool colors recede** — elements feel further away
- **High saturation draws attention** — use for focal points
- **Low saturation recedes** — use for background and supporting elements
- **Value contrast creates hierarchy** — more than hue contrast

**Palette sizing:**
- 1 dominant color (60% of visual space)
- 1-2 supporting colors (30%)
- 1 accent color (10%) — used sparingly for emphasis

---

## Composition Patterns

Read `references/composition-recipes.md` for specific layout patterns with implementation details.

## When to Consult This Skill

The Master Artificer or its agents should consult this skill when:
- Deciding on the spatial arrangement of an artifact
- Choosing between grid-based and free-form layouts
- Establishing visual hierarchy in a multi-element artifact
- Making typography decisions (font, scale, weight, spacing)
- Determining density and breathing room
- Creating tension or calm through arrangement
