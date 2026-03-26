---
name: responsive-type
description: >
  Responsive typography — how type behaves across screen sizes, devices, and contexts.
  Covers fluid type scaling, viewport-based sizing, optical adjustments at different sizes,
  mobile-first type strategy, and line length management. Use when type needs to work
  across breakpoints or adapt to different reading contexts.
---

# Responsive Type — Typography Across Screens

How to make typography adapt intelligently across devices and viewports. Type that looks perfect at 1440px desktop can be unreadable on a 375px phone — this skill covers how to handle that.

## The Core Problem

A heading set at 48px looks great on desktop but dominates a mobile screen. Body text at 16px is comfortable on desktop but might need different line height on mobile. The challenge is maintaining readability and hierarchy across every screen size.

## Fluid Type Scaling

### The Modern Approach: CSS Clamp
Instead of hard breakpoints, use continuous scaling:

```
font-size: clamp(minimum, preferred, maximum);
```

**Practical values:**
| Element | Clamp expression | Result |
|---------|-----------------|--------|
| Body | `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)` | 16px → 20px |
| H3 | `clamp(1.25rem, 1rem + 1vw, 1.75rem)` | 20px → 28px |
| H2 | `clamp(1.5rem, 1rem + 2vw, 2.5rem)` | 24px → 40px |
| H1 | `clamp(2rem, 1rem + 3vw, 3.5rem)` | 32px → 56px |

**The mental model:** minimum ensures readability on the smallest screen, maximum caps it for the largest screen, and the preferred value scales smoothly between them.

### Fallback: Breakpoint-Based Scaling
When fluid type isn't available:

| Viewport | Body | H1 | H2 | H3 | Line height |
|----------|------|----|----|-----|-------------|
| < 480px (mobile) | 16px | 28px | 22px | 18px | 1.5 |
| 480-768px (tablet) | 17px | 36px | 26px | 20px | 1.5 |
| 768-1200px (laptop) | 18px | 44px | 30px | 24px | 1.5 |
| > 1200px (desktop) | 18-20px | 48-56px | 32-40px | 26-28px | 1.4-1.5 |

## Optical Adjustments

Type doesn't just scale linearly. Different sizes need different treatments:

### What Changes at Different Sizes

| Property | Small (12-16px) | Medium (18-28px) | Large (32px+) | Display (48px+) |
|----------|----------------|-------------------|----------------|-----------------|
| Letter spacing | Default or +0.01em | Default | -0.01em | -0.02 to -0.03em |
| Line height | 1.5-1.6 | 1.4-1.5 | 1.2-1.3 | 1.0-1.15 |
| Font weight | Regular (400) | Regular-Medium | Medium-Bold | Bold-Black |
| Word spacing | Default | Default | Default | Slightly tightened |

**Why this matters:** At large sizes, default spacing looks loose and airy — tightening creates visual density. At small sizes, the same tightening makes text illegible.

### Optical Size (Variable Fonts)
Modern variable fonts have an `opsz` axis that adjusts letterforms:
- Small optical sizes: wider spacing, open counters, less detail
- Large optical sizes: tighter spacing, finer details, more contrast

If using a variable font with optical sizing (e.g., Source Serif 4, Roboto Flex), let it auto-adjust or set explicitly:
```
font-optical-sizing: auto; /* or */
font-variation-settings: 'opsz' 16; /* match to your font-size */
```

## Mobile-First Type Strategy

### Start from the Smallest Screen

1. **Set body at 16px minimum** — this is the floor, never go below
2. **Set line height at 1.5** — mobile needs more breathing room
3. **Limit headings to 2 levels** on mobile — H1 and H2 are enough. H3 becomes bold body text.
4. **Line length: 35-50 characters** on mobile (natural constraint of screen width)
5. **Increase touch targets** — any tappable text should be at least 44px tall

### Scale Up for Larger Screens

As viewport grows:
- Headings can get larger (more real estate)
- Line height can decrease slightly (wider columns = more horizontal scanning)
- More heading levels become useful (H3, H4)
- Line length must be actively constrained (60-75 chars at desktop — don't let paragraphs stretch across a 1440px viewport)

## Line Length Management

The most overlooked responsive type issue. Long lines kill readability.

### The Container Width Approach
Instead of setting font-size relative to viewport, constrain the reading container:

| Context | Max container width | Result at 18px body |
|---------|-------------------|---------------------|
| Blog/article | 680-720px | ~65 characters per line |
| Documentation | 720-800px | ~70 characters per line |
| Dashboard text | 480-560px | ~50 characters per line |
| Full-width hero | Use clamp for font-size | Scale type up to fill |

### The ch Unit
1ch = width of the "0" character in the current font. Set `max-width: 65ch` on text containers for automatic optimal line length regardless of font size.

## Common Responsive Type Mistakes

- **Not testing on actual devices** — browser resizing isn't the same as a real phone
- **Scaling everything proportionally** — headings should scale more aggressively than body text
- **Forgetting line height adjustment** — desktop line height on mobile creates too much vertical space
- **Viewport-only units (vw)** — `font-size: 5vw` with no clamp makes text unreadable on small screens and absurdly large on wide screens
- **Not constraining line length** — a 16px paragraph spanning 1400px is technically responsive but practically unreadable
- **Breaking the minimum** — 14px is absolute floor. Users with vision needs will leave.
