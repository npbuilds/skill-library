# Responsive Type — Quick Reference


## Quick Reference

| Element | Clamp expression | Result |
|---------|-----------------|--------|
| Body | `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)` | 16px → 20px |
| H3 | `clamp(1.25rem, 1rem + 1vw, 1.75rem)` | 20px → 28px |
| H2 | `clamp(1.5rem, 1rem + 2vw, 2.5rem)` | 24px → 40px |
| H1 | `clamp(2rem, 1rem + 3vw, 3.5rem)` | 32px → 56px |

## Quick Reference

| Viewport | Body | H1 | H2 | H3 | Line height |
|----------|------|----|----|-----|-------------|
| < 480px (mobile) | 16px | 28px | 22px | 18px | 1.5 |
| 480-768px (tablet) | 17px | 36px | 26px | 20px | 1.5 |
| 768-1200px (laptop) | 18px | 44px | 30px | 24px | 1.5 |
| > 1200px (desktop) | 18-20px | 48-56px | 32-40px | 26-28px | 1.4-1.5 |

## What Changes at Different Sizes

| Property | Small (12-16px) | Medium (18-28px) | Large (32px+) | Display (48px+) |
|----------|----------------|-------------------|----------------|-----------------|
| Letter spacing | Default or +0.01em | Default | -0.01em | -0.02 to -0.03em |
| Line height | 1.5-1.6 | 1.4-1.5 | 1.2-1.3 | 1.0-1.15 |
| Font weight | Regular (400) | Regular-Medium | Medium-Bold | Bold-Black |
| Word spacing | Default | Default | Default | Slightly tightened |

## Quick Reference

| Context | Max container width | Result at 18px body |
|---------|-------------------|---------------------|
| Blog/article | 680-720px | ~65 characters per line |
| Documentation | 720-800px | ~70 characters per line |
| Dashboard text | 480-560px | ~50 characters per line |
| Full-width hero | Use clamp for font-size | Scale type up to fill |

## Formula / Pseudocode

```
font-optical-sizing: auto; /* or */
font-variation-settings: 'opsz' 16; /* match to your font-size */
```
