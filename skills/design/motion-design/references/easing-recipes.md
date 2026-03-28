# Easing Recipes

Specific easing curves mapped to aesthetic personality. Cross-reference with the aesthetic-identity profile's Motion Feel and Emotional Register dimensions.

## By Personality

### Precise / Corporate
```css
--ease-out: cubic-bezier(0.25, 0, 0.15, 1);
--ease-in-out: cubic-bezier(0.45, 0, 0.15, 1);
--duration-micro: 150ms;
--duration-transition: 250ms;
--duration-entrance: 350ms;
```
No overshoot. Minimal easing variation. Consistent, predictable, reliable.

### Elegant / Editorial
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in: cubic-bezier(0.55, 0, 1, 0.45);
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
--duration-micro: 180ms;
--duration-transition: 300ms;
--duration-entrance: 450ms;
```
Slightly longer durations, pronounced deceleration. Movement feels considered and unhurried.

### Playful / Energetic
```css
--ease-out: cubic-bezier(0.34, 1.56, 0.64, 1);  /* overshoot */
--ease-in-out: cubic-bezier(0.68, -0.55, 0.265, 1.55);  /* anticipation + overshoot */
--spring: spring(1, 180, 12);  /* bouncy */
--duration-micro: 120ms;
--duration-transition: 280ms;
--duration-entrance: 400ms;
```
Overshoot, bounce, spring physics. Movement has energy and surprise.

### Contemplative / Atmospheric
```css
--ease-out: cubic-bezier(0.19, 1, 0.22, 1);  /* long tail */
--ease-in-out: cubic-bezier(0.76, 0, 0.24, 1);
--duration-micro: 200ms;
--duration-transition: 400ms;
--duration-entrance: 600ms;
--duration-ambient: 3000ms;
```
Slow, gentle, long deceleration. Movement breathes. Ambient motion is prominent.

### Kinetic / Technical
```css
--ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);  /* material design standard */
--ease-in: cubic-bezier(0.4, 0.0, 1, 1);
--stagger-delay: 30ms;
--duration-micro: 100ms;
--duration-transition: 200ms;
--duration-entrance: 300ms;
```
Snappy, efficient, systematic. Tight stagger delays. Movement is information, not decoration.

## By Context

### Scroll Reveal
```css
/* Fade up on scroll — works for any personality */
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 500ms ease-out, transform 500ms ease-out;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Loading Skeleton
```css
/* Shimmer — personality-neutral */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(90deg, var(--bg) 25%, var(--shimmer) 50%, var(--bg) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
```

### Stagger Cascade
```js
// Universal stagger — adjust staggerDelay for personality
elements.forEach((el, i) => {
  el.style.animationDelay = `${i * staggerDelay}ms`;
});
```
