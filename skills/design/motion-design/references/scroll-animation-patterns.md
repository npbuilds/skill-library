# Scroll Animation Patterns

Techniques for scroll-driven motion in artifacts. These use modern CSS Scroll-Driven Animations API where supported, with JS fallbacks.

## Pattern 1: Parallax Layers

Multiple layers move at different speeds relative to scroll, creating depth.

```css
/* CSS Scroll-Driven (modern browsers) */
@keyframes parallax-slow { from { transform: translateY(0); } to { transform: translateY(-100px); } }
@keyframes parallax-fast { from { transform: translateY(0); } to { transform: translateY(-300px); } }

.layer-back { animation: parallax-slow linear both; animation-timeline: scroll(); }
.layer-front { animation: parallax-fast linear both; animation-timeline: scroll(); }
```

**When to use:** Immersive landing pages, storytelling artifacts, atmospheric backgrounds.
**Personality fit:** Contemplative, atmospheric, editorial.

## Pattern 2: Progress-Linked Reveal

Content appears as a function of scroll progress, not scroll events.

```css
@keyframes reveal {
  0% { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}

.reveal-section {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 40%;
}
```

**When to use:** Progressive disclosure, data narratives, scrollytelling.
**Personality fit:** Any — adjust timing and transform for personality.

## Pattern 3: Sticky + Morph

An element sticks in viewport while its properties morph based on scroll.

```css
.sticky-hero {
  position: sticky;
  top: 0;
  animation: shrink-hero linear both;
  animation-timeline: scroll();
  animation-range: 0px 300px;
}

@keyframes shrink-hero {
  from { height: 100vh; border-radius: 0; }
  to { height: 80px; border-radius: 12px; }
}
```

**When to use:** Hero sections that collapse into headers, data cards that pin and update.
**Personality fit:** Technical, editorial, modern.

## Pattern 4: Horizontal Scroll Section

Vertical scroll drives horizontal movement within a pinned section.

**Best implemented with JS** (IntersectionObserver + scroll listener) as CSS scroll-driven animations handle this awkwardly.

**When to use:** Portfolios, timelines, before/after comparisons.
**Personality fit:** Editorial, playful, showcase.

## Performance Notes

- Scroll-driven CSS animations run on the compositor thread — 60fps guaranteed
- JS scroll listeners run on main thread — use `requestAnimationFrame` and `will-change`
- Avoid scroll-linked layout changes (width, height) — animate transforms and opacity only
- Test on low-end devices — scroll jank is more noticeable than click-triggered jank
