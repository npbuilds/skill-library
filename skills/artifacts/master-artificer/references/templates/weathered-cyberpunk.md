# Template: Weathered Cyberpunk

*Source: Archon Investment Intelligence Briefing (2026-03-28)*
*Status: Go-to template — user-approved with strong positive signal*

## When to Use

Dashboard-style artifacts, data-heavy displays, intelligence briefings, monitoring interfaces, or any output that needs to feel **serious, data-rich, and atmospheric** without being dark-mode-only. Works especially well for:
- Financial / investment dashboards
- System monitoring / status pages
- Data exploration tools
- Technical reports with visual elements
- Any "command center" aesthetic

## Design DNA

**In three words:** Clinical futurism, weathered.

**The feel:** A high-end control room terminal that's been running for years. Not pristine — *lived in*. The neon has faded, the CRT has burn-in, but the data is razor sharp. Think Blade Runner 2049's muted palette applied to Bloomberg Terminal's information density.

## Color System

### Light Mode (preferred)

```css
:root {
  --bg-deep: #e8ecf2;        /* Page background — blue-gray */
  --bg-panel: #f0f3f8;       /* Panel/card background */
  --bg-panel-hover: #dce2ec;  /* Hover state */
  --border-dim: #c0c8d8;     /* Default borders */
  --border-glow: #8898b8;    /* Active/hover borders */

  /* Accent palette — faded neon */
  --cyan-faded: #1a7070;     /* Primary accent — section titles, links */
  --cyan-bright: #0e8a8a;    /* Emphasis */
  --magenta-faded: #8a2a5a;  /* Secondary accent — insights, warnings */
  --magenta-bright: #a83880;
  --amber-faded: #7a6a20;    /* Tertiary — caution, neutral signals */
  --amber-bright: #9a8420;
  --red-faded: #983030;      /* Negative values, danger */
  --red-bright: #c04040;
  --green-faded: #1a7830;    /* Positive values, safe */
  --green-bright: #208a38;

  /* Text */
  --text-primary: #3a4050;   /* Body text */
  --text-dim: #6a7488;       /* Labels, secondary text */
  --text-bright: #1a2030;    /* Headlines, emphasis */
}
```

### Dark Mode (original cyberpunk)

```css
:root {
  --bg-deep: #06070d;
  --bg-panel: #0b0d18;
  --bg-panel-hover: #10132a;
  --border-dim: #1a1d3a;
  --border-glow: #2a3a6a;
  --cyan-faded: #3a8a8a;
  --cyan-bright: #5acece;
  --magenta-faded: #8a3a6a;
  --magenta-bright: #ce5aaa;
  --amber-faded: #8a7a3a;
  --amber-bright: #ceb45a;
  --red-faded: #8a3a3a;
  --red-bright: #ce5a5a;
  --green-faded: #3a8a4a;
  --green-bright: #5ace6a;
  --text-primary: #a0aab8;
  --text-dim: #5a6478;
  --text-bright: #d0dae8;
}
```

### Palette Rules
- 60% background (bg-deep, bg-panel)
- 30% text + borders (text-primary, border-dim)
- 10% accent (cyan-faded as primary, others for semantic meaning)
- Accent colors carry **meaning**, not decoration — cyan = structure, magenta = insight, amber = caution, red = danger, green = positive

## Typography

Three-font stack from Google Fonts:

```
Orbitron:wght@400;500;600;700;800;900  — Display / headlines
Share Tech Mono                        — Body / data / monospace
Rajdhani:wght@300;400;500;600;700      — Labels / tags / secondary
```

### Usage Rules

| Element | Font | Weight | Size | Spacing | Transform |
|---------|------|--------|------|---------|-----------|
| Logo / page title | Orbitron | 800 | 32px | 8px | — |
| Section titles | Orbitron | 600 | 12px | 4px | uppercase |
| Data headlines (regime, scenario) | Orbitron | 700 | 22-28px | 2px | — |
| Gauge numbers | Orbitron | 700 | 24px | — | — |
| Ticker symbols | Orbitron | 500 | 11px | 1px | — |
| Body text | Share Tech Mono | 400 | 13px | — | — |
| Table data | Share Tech Mono | 400 | 12px | — | — |
| Labels / tags | Rajdhani | 300-500 | 10-11px | 2-4px | uppercase |
| Subtitle | Rajdhani | 300 | 14px | 6px | uppercase |

## Layout System

### Container
- Max-width: 1400px, centered
- Padding: 20px
- No border-radius anywhere (sharp edges throughout)

### Grid utilities
```css
.grid-2 { grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { grid-template-columns: 1fr 1fr 1fr; gap: 16px; }
.grid-4 { grid-template-columns: repeat(4, 1fr); gap: 12px; }
```

### Section panels
- Border: 1px solid var(--border-dim)
- Background: var(--bg-panel)
- No border-radius
- Header: flex row with title (left, Orbitron) + tag (right, Rajdhani in bordered pill)
- Body: 20px padding
- Hover: border brightens to --border-glow, bg shifts to --bg-panel-hover

### Cards (regime-card, scenario-card, crypto-card, factor-block)
- Same border/bg as sections
- Left-edge color bar (4px width) for status signaling
- Inner padding: 14-20px

## Component Library

### Gauge Ring (SVG)
- 120x120px SVG with track + fill-arc circles
- r=45, stroke-width=6, stroke-dasharray=283
- Background track: var(--border-dim)
- Centered number overlay (Orbitron 700 24px)
- Label below (Rajdhani 11px uppercase)

### Data Table
- Full-width, collapse borders
- Header: Rajdhani 10px uppercase, letter-spacing 3px
- Cells: 7px 12px padding
- Row hover: rgba(accent, 0.04) background
- Semantic value classes: .val-pos (green), .val-neg (red), .val-warn (amber), .val-extreme (magenta glow)

### Heat Bar (horizontal bar chart)
- Label (110px right-aligned) → bar track → value
- Center line at 50% for +/- values
- Fill extends left (neg) or right (pos) from center

### Spark Bar (inline mini-bar)
- 60x12px inline bar with center line
- Used inside table cells for visual scale

### Insight Block
- Left border: 2px solid var(--magenta-faded)
- Background: rgba(magenta, 0.06)
- Label: Orbitron 9px with extending line (::after)
- Use for analytical callouts, game theory insights, etc.

### Recommendation Blocks
- .rec-do: left border green, green-tinted bg
- .rec-avoid: left border red, red-tinted bg
- Label: Orbitron 9px letter-spacing 4px

### Scenario Cards
- Large probability number (Orbitron 28px 700)
- Scenario name (Rajdhani 14px 600 uppercase)
- Detail text (11px, dim, with highlighted spans)

## Effects Layer

### CRT Scanline Overlay
```css
.crt-overlay {
  position: fixed; top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none; z-index: 2;
  background: repeating-linear-gradient(0deg,
    transparent, transparent 2px,
    rgba(0,0,0, var(--scanline-opacity)) 2px,
    rgba(0,0,0, var(--scanline-opacity)) 4px);
}
/* Plus radial vignette via ::after */
```
- Light mode: --scanline-opacity: 0.015 (very subtle)
- Dark mode: --scanline-opacity: 0.03

### CSS Digital Rain (background animation)
- Absolute-positioned columns of characters using CSS animation
- Faded green (Rajdhani font), opacity 0.03-0.06
- Purely decorative atmospheric texture

### Neon Divider
```css
background: linear-gradient(90deg, transparent, var(--cyan-faded), var(--magenta-faded), transparent);
height: 1px; opacity: 0.4;
```

### Section Noise Texture
- SVG fractalNoise filter as background-image on section::after
- Opacity: 0.5 dark / 0.15 light

### Header Glow Line
- 2px gradient line at top of header, animated opacity pulse (6s cycle)

## Tooltip System

Uses `position: fixed` pseudo-elements with JS-calculated viewport coordinates to escape stacking contexts. Requires a small `mouseenter` script to set CSS custom properties (`--tip-top`, `--tip-left`, `--tip-arrow-top`).

```html
<span class="tip" data-tip="Explanation text here">Term</span>
```

## Theme Toggle

Button in header top-right, toggles `data-theme="light"` attribute on `<html>`. All colors flow through CSS custom properties, so the toggle is just one attribute change.

## Anti-Patterns (What NOT to Do)

- No border-radius — this template uses sharp 0px corners everywhere
- No gradients on cards/panels — flat solid colors only (gradient reserved for header and dividers)
- No bounce/spring animations — use `ease` and `ease-in-out` only
- No emoji or decorative icons — use SVG line icons sparingly (16x16, 0.6 opacity)
- No sans-serif body text — always monospace (Share Tech Mono) for body
- No high-saturation accents — keep everything faded/muted, the "neon" is always at 40-60% intensity
- No white (#fff) backgrounds even in light mode — always blue-gray tinted

## Source File

Full working implementation: `archon-briefing-2026-03-28.html` (project root)
