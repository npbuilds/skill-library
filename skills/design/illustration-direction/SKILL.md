---
name: illustration-direction
description: >
  Knowledge skill for illustration style taxonomy, icon systems, texture and materiality,
  and visual asset direction. Provides the style vocabulary and decision framework that
  the design-orchestrator's illustration-agent draws upon. Consult when choosing illustration
  style, defining icon systems, selecting textures, or directing any non-photographic
  visual asset creation.
---

# Illustration Direction — The Visual Language Codex

Illustration style is not "what it looks like" — it's a system of constraints that produces visual coherence across all assets. A well-defined illustration direction means any new asset created months later still feels like it belongs.

## Style Taxonomy

### By Rendering Approach

| Style | Characteristics | Best for | Personality |
|-------|----------------|----------|-------------|
| **Flat** | No shadows, solid fills, clean edges | UI icons, infographics, tech products | Modern, clean, scalable |
| **Semi-flat** | Flat + subtle shadows or gradients | Marketing, editorial, apps | Approachable, contemporary |
| **Isometric** | 3D projection, no perspective vanishing | Technical diagrams, architecture, data | Precise, systematic, playful-technical |
| **Line art** | Strokes only, no fills (or minimal) | Editorial, documentation, minimalist | Elegant, intellectual, restrained |
| **Hand-drawn** | Visible imperfection, sketch quality | Personal, artisanal, storytelling | Warm, human, authentic |
| **Geometric abstract** | Shapes as building blocks, no representation | Branding, backgrounds, pattern | Bold, conceptual, high-design |
| **Dimensional/3D** | Realistic lighting, depth, material | Hero images, product shots | Premium, immersive, substantial |
| **Collage** | Mixed media, cut-paper, overlapping textures | Editorial, cultural, experimental | Eclectic, layered, artistic |
| **Pixel art** | Grid-aligned, limited palette, retro | Gaming, nostalgia, playful tech | Retro, charming, constrained |
| **Gradient mesh** | Soft blends, luminous, no hard edges | Ambient, atmospheric, abstract | Ethereal, futuristic, dreamy |

### By Content Approach

| Approach | When to use |
|----------|------------|
| **Literal** | The illustration shows exactly what is described (a house, a person, a process). Best for clarity. |
| **Metaphorical** | The illustration represents an abstract concept through visual analogy. Best for emotional resonance. |
| **Decorative** | The illustration adds visual texture without specific meaning. Best for atmosphere and brand feel. |
| **Diagrammatic** | The illustration explains a system, flow, or relationship. Best for education and documentation. |
| **Narrative** | The illustration tells a story or captures a moment. Best for editorial and marketing. |

## Icon Systems

An icon system is a miniature illustration direction. Consistency rules are stricter because icons appear in dense arrays where any deviation breaks the pattern.

### Grid and Sizing

- **Base grid**: typically 24×24px or 32×32px
- **Padding**: 2px minimum clearance from grid edge (optical safety zone)
- **Stroke weight**: single weight for the entire system (1.5px, 2px common)
- **Corner radius**: consistent across all icons (0 for sharp, 2px for soft, fully rounded for friendly)
- **Optical sizing**: circles and diagonals extend slightly beyond the grid to appear visually equal to squares

### Style Attributes

Define these once, apply everywhere:

- **Fill vs stroke**: filled icons (dense, bold) vs. outlined icons (light, airy) vs. duotone (filled + stroke detail)
- **Corner treatment**: sharp, rounded, or mixed (rounded outer, sharp inner)
- **Detail level**: minimal (3-5 elements max), moderate, detailed
- **Perspective**: always straight-on, always isometric, or mixed (pick one)

## Texture and Materiality

Texture adds tactile quality — the feeling that a surface has physical properties.

| Texture type | Effect | Implementation |
|-------------|--------|----------------|
| **Grain/noise** | Analog warmth, photographic | CSS `filter`, SVG turbulence, noise overlay |
| **Paper** | Physical, crafted, editorial | Background texture image, subtle grain |
| **Halftone** | Retro print, pop art | SVG filter or dot pattern overlay |
| **Gradient mesh** | Luminous, digital, futuristic | CSS gradients, mesh gradient tools |
| **Line texture** | Cross-hatch, engraving | SVG patterns, stroke-based fills |
| **Clean/none** | Digital, precise, minimal | Solid fills, no texture |

**Rule of thumb:** texture should reinforce the Precision dimension from the aesthetic identity. Mechanical/exact aesthetic → clean surfaces. Expressive/handmade aesthetic → visible texture.

## Consistency Checklist

When establishing or evaluating an illustration direction:

- [ ] Stroke weight is consistent across all assets
- [ ] Corner radius is consistent (or follows a clear rule for when it varies)
- [ ] Color usage follows the palette (illustrations don't introduce off-palette colors)
- [ ] Shadow angle is consistent (if shadows are used)
- [ ] Level of detail is consistent (simple icons don't appear next to detailed illustrations)
- [ ] Perspective is consistent (isometric assets don't mix with flat assets)
- [ ] Human representation style is consistent (if applicable — proportions, features, diversity)

## When to Consult This Skill

- Choosing an illustration style for a project or brand
- Defining an icon system's grid, stroke, and style rules
- Selecting textures or materiality for visual assets
- Evaluating whether a new illustration fits an established direction
- Briefing an illustration agent or external illustrator
