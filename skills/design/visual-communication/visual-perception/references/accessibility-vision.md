# Accessibility and Vision

Design for the full spectrum of human visual ability.

## Color Vision Deficiency (Color Blindness)

Affects ~8% of males and ~0.5% of females. Design must work for all types.

### Types

| Type | Prevalence | Confusion pairs |
|------|-----------|-----------------|
| Deuteranopia (no green cones) | ~5% of males | Red ↔ Green, Orange ↔ Green |
| Protanopia (no red cones) | ~1.5% of males | Red ↔ Green, Red appears dark |
| Tritanopia (no blue cones) | ~0.01% | Blue ↔ Yellow, Purple ↔ Red |
| Achromatopsia (no color) | ~0.003% | Everything is lightness only |

### Design Rules for Color Blindness

1. **Never use color alone** to encode meaning — always pair with shape, icon, text, or pattern
2. **Red/green is the worst pair** — most common deficiency. Use red/blue or orange/blue instead
3. **Test with a simulator** — Coblis, Color Oracle, or built-in browser devtools (Chrome: Rendering panel → Emulate vision deficiency)
4. **For data visualization:** use colorblind-safe palettes (viridis, inferno, cividis, ColorBrewer2)
5. **For status indicators:** pair colors with icons (checkmark for success, X for error, triangle for warning)

### Safe Color Combinations

These pairs are distinguishable by all common color vision types:
- Blue + Orange
- Blue + Red
- Blue + Yellow
- Purple + Yellow-green
- Dark blue + Light orange

Avoid relying on:
- Red + Green (most common confusion)
- Green + Brown/Orange
- Blue + Purple (tritanopia confusion)

## Low Vision

~3% of the global population has significant visual impairment beyond correctable with glasses.

### Design Accommodations

- **Minimum font size:** 16px base, user-scalable up to 200%
- **Minimum contrast:** 4.5:1 for text, 3:1 for UI components (WCAG AA)
- **Touch target size:** 44×44px minimum (WCAG 2.5.5)
- **Focus indicators:** clearly visible outline on keyboard focus (not just color change)
- **Zoom support:** layout must not break at 200% browser zoom
- **Text reflow:** at 400% zoom, content should reflow to single column without horizontal scrolling

## Motion Sensitivity

~35% of adults report some motion sensitivity. ~5% have vestibular disorders.

### Triggers to Avoid or Gate Behind `prefers-reduced-motion`

- Parallax scrolling
- Auto-playing video/animation
- Spinning or rotating elements
- Rapid zooming
- Persistent background motion
- Full-screen transitions (zoom/fly-through)

### Safe Motion Patterns

- Opacity fades (0 to 1 or 1 to 0)
- Small position shifts (< 100px)
- Scale transitions within 90-110% range
- Color/background transitions

### Implementation

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001s !important;
    transition-duration: 0.001s !important;
  }
}
```

## Cognitive Accessibility

Affects attention, memory, processing speed, and executive function.

- **Limit choices:** 5-7 options maximum per decision point
- **Clear labels:** say what things do, not what they are ("Save document" not "Disk icon")
- **Consistent navigation:** same location, same order, every page
- **Error prevention:** confirm destructive actions, allow undo, validate input live
- **Chunk information:** break long content into scannable sections with clear headings
- **Plain language:** avoid jargon, use active voice, keep sentences short
