---
name: type-fundamentals
description: >
  Typography foundations — typeface anatomy, classification systems, and legibility principles.
  Covers x-height, stroke contrast, serifs vs sans-serifs, monospaced vs proportional, optical
  sizing, and the core properties that determine how a typeface feels and performs.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Type Fundamentals — The Anatomy of Letters

The foundational knowledge for all typography decisions. Before you can pair fonts, set hierarchy, or scale type responsively, you need to understand what makes a typeface what it is.

## Typeface Anatomy

Every letterform has measurable properties that determine its personality and performance:

### Key Measurements
- **x-height**: Height of lowercase letters (a, e, o). Higher x-height = more readable at small sizes. Compare: Verdana (tall x-height) vs Garamond (short x-height)
- **Cap height**: Height of uppercase letters. Defines the visual "loudness" of the face
- **Ascenders/descenders**: Parts extending above x-height (b, d, h) or below baseline (g, p, y). Long ascenders/descenders need more line height
- **Stroke contrast**: Difference between thick and thin strokes. High contrast = elegant/formal. Low contrast = stable/modern
- **Counter**: Enclosed or partially enclosed white space (inside o, e, a). Open counters improve legibility at small sizes
- **Aperture**: Openings in letters like c, e, s. Wide apertures = better readability

### What Anatomy Tells You
- **Large x-height + open counters** → good for body text, screens, small sizes
- **High stroke contrast + small x-height** → good for display, headings, print
- **Uniform stroke width** → geometric/modern feel, good for UI
- **Variable stroke width** → humanist/organic feel, good for editorial

## Classification System

### The Big Four Categories

**1. Serif** — Has small decorative strokes at letter terminals
- *Old Style* (Garamond, Palatino): Diagonal stress, low contrast, warm
- *Transitional* (Times, Georgia, Baskerville): Vertical stress, moderate contrast, balanced
- *Modern/Didone* (Bodoni, Didot): Strong vertical stress, extreme contrast, elegant
- *Slab Serif* (Rockwell, Courier, Roboto Slab): Thick block serifs, sturdy, mechanical

**2. Sans-Serif** — No decorative strokes
- *Grotesque* (Helvetica, Arial): Nearly uniform stroke, neutral, ubiquitous
- *Neo-Grotesque* (Univers, Roboto): Refined grotesque, very clean
- *Geometric* (Futura, Poppins, Montserrat): Based on circles/squares, modern, mathematical
- *Humanist* (Gill Sans, Fira Sans, Open Sans): Calligraphic influence, warm, readable

**3. Monospaced** — Every character same width
- *Code faces* (JetBrains Mono, Fira Code): Designed for programming, ligatures
- *Typewriter faces* (Courier): Traditional, nostalgic
- Use for: code blocks, tabular data, deliberate "technical" aesthetic

**4. Display/Decorative** — Designed for large sizes only
- Script, blackletter, ornamental, novelty
- Never use below 24px
- One display face maximum per project

## Legibility Principles

### The Non-Negotiables
1. **Body text**: 16-20px on screen (never below 14px)
2. **Line length**: 45-75 characters per line (ideal: 65)
3. **Line height**: 1.4-1.6x font size for body text
4. **Letter spacing**: Default for body, slightly increased for all-caps, slightly tightened for large headings
5. **Word spacing**: Typically leave at default; only adjust for justified text

### Screen vs Print
| Property | Screen | Print |
|----------|--------|-------|
| Minimum size | 14px (prefer 16px+) | 9pt (prefer 10pt+) |
| Preferred serif style | Slab or transitional | Old style or transitional |
| Preferred sans style | Humanist or neo-grotesque | Any |
| Line height | 1.4-1.6x | 1.2-1.4x |
| Stroke contrast | Low-medium | Any |

### Quick Legibility Test
Before committing to a typeface for body text, check:
- ✅ Can you distinguish Il1 (capital I, lowercase l, number 1)?
- ✅ Can you distinguish 0O (zero, capital O)?
- ✅ Is the x-height at least 65% of cap height?
- ✅ Are counters open enough at your target size?
- ✅ Does it render cleanly at your smallest planned size?

## When to Use Each Category

| Goal | Reach for | Why |
|------|-----------|-----|
| Long-form reading (blog, article) | Humanist sans or transitional serif | Optimized for sustained reading |
| UI / interface | Geometric or neo-grotesque sans | Clean, neutral, doesn't compete with content |
| Luxury / editorial | Modern serif (Didone) | Contrast creates elegance |
| Technical / data | Monospaced or tabular figures | Alignment matters more than aesthetics |
| Headlines / impact | Display or high-contrast serif | Personality at large sizes |
| Friendly / approachable | Rounded sans or humanist sans | Organic shapes feel warm |
| Authority / tradition | Old style or transitional serif | Historical associations |

## Anti-Patterns

- **Comic Sans for professional work** — obvious, but also: Papyrus, Curlz, Bleeding Cowboys
- **More than 3 typefaces** in one project — cognitive overload
- **Display face for body text** — designed for 36px+, breaks at 16px
- **Thin weights on low-res screens** — sub-pixel rendering makes them disappear
- **All-caps body text** — reduces reading speed by 10-20%
- **Justified text without hyphenation** — creates "rivers" of white space
