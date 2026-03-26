# Palette Recipes

Reusable palette construction patterns for common design scenarios.

## Recipe 1: Corporate / Professional

```
Seed: desaturated blue (HSL 210, 40%, 45%)
Structure: analogous + neutral scale
Steps:
  1. Primary: HSL(210, 40%, 45%)
  2. Secondary: HSL(195, 35%, 50%) — shifted 15° cooler
  3. Accent: HSL(25, 65%, 55%) — warm complement for CTAs
  4. Neutrals: HSL(210, 8%, 15/30/50/75/95%) — tinted greys
Result: trustworthy, calm, professional with warm call-to-action contrast
```

## Recipe 2: Warm / Approachable

```
Seed: warm terracotta (HSL 15, 55%, 55%)
Structure: analogous warm + cool neutral
Steps:
  1. Primary: HSL(15, 55%, 55%)
  2. Secondary: HSL(35, 50%, 60%) — golden shift
  3. Accent: HSL(190, 45%, 45%) — cool complement for balance
  4. Neutrals: HSL(30, 10%, 15/30/50/75/95%) — warm-tinted greys
Result: friendly, earthy, human — good for wellness, food, community
```

## Recipe 3: Bold / Energetic

```
Seed: saturated primary (HSL 350, 80%, 50%)
Structure: split-complementary + dark neutrals
Steps:
  1. Primary: HSL(350, 80%, 50%)
  2. Secondary: HSL(170, 70%, 40%) — split complement A
  3. Tertiary: HSL(200, 70%, 45%) — split complement B
  4. Neutrals: HSL(220, 15%, 10/20/35/60/90%) — cool-dark base
Result: high-energy, attention-demanding — sports, entertainment, youth
```

## Recipe 4: Minimal / Elegant

```
Seed: near-black (HSL 0, 0%, 12%)
Structure: monochromatic + single accent
Steps:
  1. Primary: HSL(0, 0%, 12%) — near-black
  2. Surface: HSL(0, 0%, 98%) — near-white
  3. Text: HSL(0, 0%, 25%) — dark grey
  4. Accent: HSL(any, 50%, 50%) — single color, used sparingly
  5. Neutrals: HSL(0, 0%, 40/60/80/92%) — pure grey scale
Result: sophisticated, restrained — luxury, editorial, fashion
```

## Recipe 5: Data Visualization (Sequential)

```
Purpose: encode low-to-high values
Structure: single hue, vary lightness
Steps:
  1. Pick a hue that matches the data context (blue=cold, red=heat, green=growth)
  2. Lowest value: HSL(hue, 20%, 90%) — very light
  3. Mid value: HSL(hue, 50%, 55%) — medium
  4. Highest value: HSL(hue, 70%, 25%) — dark and saturated
  5. Generate 5-7 even steps between min and max
Rule: must be distinguishable in greyscale (lightness must be evenly spaced)
```

## Recipe 6: Data Visualization (Categorical)

```
Purpose: distinguish unrelated categories
Structure: maximally spaced hues, equal lightness
Steps:
  1. Start at hue 0
  2. Space evenly around wheel: 360/n degrees apart
  3. Keep saturation at 55-65% (readable but not garish)
  4. Keep lightness at 48-55% (passes contrast on white)
  5. Max 7-8 categories — beyond that, use shape/pattern encoding
Rule: every pair must have >3:1 contrast with each other and background
```

## Testing Any Palette

After constructing a palette, validate:

1. **Greyscale test**: convert to greyscale — is hierarchy still visible?
2. **Contrast test**: check every text/background combination against WCAG 4.5:1
3. **Adjacency test**: place all colors next to each other — any vibrating/clashing pairs?
4. **Context test**: mock up actual usage — does the 60-30-10 ratio feel balanced?
5. **Colorblind test**: simulate deuteranopia (red-green) and tritanopia (blue-yellow)
