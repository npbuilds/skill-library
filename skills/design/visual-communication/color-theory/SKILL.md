---
name: color-theory
description: >
  Color theory foundations for design decisions. Reference when selecting palettes, evaluating
  color harmony, choosing contrast strategies, or understanding how colors interact perceptually.
  Use when any design agent needs to justify or refine color choices.
---

# Color Theory — The Spectrum

Foundational color knowledge for making and evaluating chromatic design decisions.

## Color Models

### HSL — The Designer's Model

Think in HSL (Hue, Saturation, Lightness), not hex. It maps to human intention:

- **Hue** (0-360°): The color itself. 0=red, 120=green, 240=blue.
- **Saturation** (0-100%): Intensity. 0%=grey, 100%=pure color.
- **Lightness** (0-100%): Light/dark. 0%=black, 50%=pure color, 100%=white.

This matters because design operations map directly to HSL channels:
- "Make it more muted" → reduce saturation
- "Make it feel warmer" → shift hue toward red/orange (0-60°)
- "Create a tint" → increase lightness
- "Create a shade" → decrease lightness

### Color Temperature

Warm (red/orange/yellow, 0-60° and 300-360°) advances — feels closer, more energetic.
Cool (blue/green/violet, 120-270°) recedes — feels calmer, more distant.
Neutral (pure grey, desaturated tones) anchors — provides rest for the eye.

Temperature is relative: a blue-green feels warm next to pure blue, cool next to yellow-green.

## Harmony Systems

These are relationships on the color wheel that produce reliably pleasing combinations.

| System | Wheel relationship | Character | Best for |
|--------|-------------------|-----------|----------|
| **Monochromatic** | One hue, vary S and L | Cohesive, calm, low contrast | Backgrounds, subtle UIs, elegant minimalism |
| **Analogous** | 2-3 adjacent hues (30° apart) | Harmonious, natural, easy | Most design work, safe default |
| **Complementary** | Opposite hues (180° apart) | High contrast, vibrant, tense | Accent strategies, call-to-action, alerts |
| **Split-complementary** | One hue + two adjacent to its complement | Contrast with less tension | Balanced designs needing variety |
| **Triadic** | Three hues 120° apart | Vibrant, balanced, playful | Children's brands, playful products, diverse palettes |
| **Tetradic** | Two complementary pairs | Rich, complex, hard to balance | Complex data visualization, editorial |

### The 60-30-10 Rule

For any palette application:
- **60%** dominant (backgrounds, large surfaces) — usually the most neutral
- **30%** secondary (supporting elements, containers) — medium saturation
- **10%** accent (CTAs, highlights, key data) — highest contrast/saturation

This ratio prevents visual chaos and gives the eye a clear hierarchy.

## Building Palettes

### From a Single Seed Color

1. Start with the brand/mood color as seed
2. Generate neutrals: desaturate the seed to 5-10% saturation, create a lightness scale (5 steps minimum: near-white, light, mid, dark, near-black)
3. Generate accent: take the complement or split-complement of the seed
4. Test: place seed on lightest neutral, accent on seed, text on all backgrounds

### Palette Structures for Common Use Cases

**Brand palette (5-7 colors):** 1 primary, 1 secondary, 3-5 neutrals, 1 accent
**UI palette (12-16 colors):** Primary scale (3), secondary scale (3), neutral scale (5-7), semantic (success/warning/error/info)
**Data visualization (5-8 colors):** Sequential ramp OR categorical set — never both in one chart
**Editorial (3-4 colors):** Dominant + accent + 1-2 neutrals — restraint is key

## Contrast and Accessibility

### WCAG Contrast Ratios

- **4.5:1** minimum for normal text (AA)
- **3:1** minimum for large text (18px+) and UI components (AA)
- **7:1** for enhanced contrast (AAA)

### Practical Contrast Rules

- Dark text on light background: text lightness < 35%, background > 85%
- Light text on dark background: text lightness > 80%, background < 25%
- Never rely on color alone to convey meaning (add icons, labels, or patterns)
- Test with a desaturation filter — if hierarchy disappears, your lightness contrast is insufficient

## Color Psychology (Use Carefully)

These associations are **culturally dependent** — read `references/cultural-color-meanings.md` for regional variations.

Western default associations:
- **Red**: urgency, passion, danger, energy — strongest attention-grabber
- **Blue**: trust, calm, professionalism — most universally "safe" color
- **Green**: growth, nature, success, go — positive semantic
- **Yellow/Orange**: warmth, optimism, caution — high energy, hard to read as text
- **Purple**: luxury, creativity, mystery — often overused, be intentional
- **Black**: sophistication, power, formality — highest contrast anchor
- **White**: cleanliness, space, simplicity — the most important "color" in minimal design

## Common Mistakes

1. **Too many hues** — most designs need 2-3 hues max, not 6
2. **Fighting saturation** — mixing high-saturation colors creates visual noise; let one dominate
3. **Ignoring lightness** — two colors can have different hues but the same lightness, making them impossible to distinguish
4. **Semantic collisions** — using red for a non-error positive action, green for a destructive action
5. **Screen-to-print mismatch** — RGB gamut is wider than CMYK; saturated blues and greens will look different printed
