# The Anti-Slop Codex — Quality Gates for Extraordinary Artifacts

"Slop" is the generic, default-feeling output that AI-generated artifacts tend toward. The Codex exists to catch and kill it before delivery.

---

## The Seven Deadly Defaults

These are the patterns that make an artifact feel AI-generated rather than crafted. Every artifact must be checked against all seven.

### 1. The Gradient Sin
**Slop:** Purple-to-blue gradients applied to everything. Background gradients with no conceptual purpose.
**Gate:** Every gradient must answer "why this direction? why these colors? what does the gradient communicate?" If it's decorative filler, remove it.
**Instead:** Solid colors with purpose. If a gradient is needed, derive it from the concept (heat map, depth, time passage).

### 2. The Center Trap
**Slop:** Everything centered. Centered headings, centered content, centered layout. Symmetrical, static, lifeless.
**Gate:** At least one major element must break center alignment. Intentional asymmetry creates visual tension and energy.
**Instead:** Left-aligned text with right-weighted imagery. Off-center focal points. Deliberate imbalance that draws the eye.

### 3. The Rounded Corner Plague
**Slop:** `border-radius: 12px` on everything. Cards, buttons, containers, images — all the same soft rounding.
**Gate:** Border radius must vary by purpose. Not everything needs rounding. Sharp corners communicate precision; large rounding communicates friendliness. Mix them.
**Instead:** Purposeful geometry. Sharp containers with rounded interactive elements. Or fully sharp. Or organic curves that aren't circular.

### 4. The Font Surrender
**Slop:** System font or Inter everywhere. No typographic hierarchy. Every heading the same weight.
**Gate:** Typography must be a conscious choice that reinforces the concept. Weight, size, and spacing must create clear hierarchy.
**Instead:** One distinctive display font for headings + one readable body font. Or a monospace system for technical artifacts. Or a single font family used across 4+ weights for rhythm.

### 5. The Card Grid Cemetery
**Slop:** Equal-sized cards in a uniform grid. Every card identical. No visual rhythm or hierarchy.
**Gate:** If using cards, vary them — size, emphasis, density, or interaction. At least one card must be visually distinct.
**Instead:** Masonry layouts. Featured + supporting cards. Cards with variable height based on content. Magazine-style mixed layouts.

### 6. The Skeleton Screen
**Slop:** A technically functional artifact with no personality. Correct but sterile. Clean but forgettable.
**Gate:** The artifact must have at least one detail that someone would screenshot and share. One "how did they do that" moment.
**Instead:** Add soul — an unexpected animation, a clever empty state, a delightful hover effect, a poetic loading message, a hidden interaction.

### 7. The Motion Desert
**Slop:** Static everything. Or the opposite — everything animating simultaneously with no choreography.
**Gate:** Motion must be purposeful, staggered, and responsive. Nothing should move without reason. Nothing interactive should be motionless.
**Instead:** Entry animations staggered by 30-80ms. Hover states that respond in 100-200ms. Transitions that ease naturally (spring or cubic-bezier, never linear for UI).

---

## Technical Quality Gates

### Performance
- [ ] Animations target 60fps — use `transform` and `opacity` for GPU compositing
- [ ] No layout thrashing — batch DOM reads and writes
- [ ] Images and heavy assets are lazy-loaded or progressive
- [ ] Canvas/WebGL renders are throttled to `requestAnimationFrame`
- [ ] No memory leaks in animation loops (cleanup on unmount/removal)

### Accessibility
- [ ] `prefers-reduced-motion` is respected — provide meaningful static alternative
- [ ] `prefers-color-scheme` is considered where applicable
- [ ] Interactive elements are keyboard-navigable
- [ ] Color contrast meets WCAG AA (4.5:1 for text, 3:1 for large text)
- [ ] Screen reader content exists for non-decorative visuals
- [ ] Focus indicators are visible and styled (not the default blue outline unless it fits)

### Responsiveness
- [ ] Artifact is usable on mobile viewport (375px minimum)
- [ ] Touch interactions work where mouse interactions do
- [ ] No horizontal scrolling on mobile
- [ ] Font sizes are readable without zooming (16px minimum body)
- [ ] Canvas/WebGL resizes correctly on viewport change

### Code Quality
- [ ] No inline styles that could be CSS classes (unless dynamic)
- [ ] Event listeners are cleaned up
- [ ] No `setInterval` without cleanup — use `requestAnimationFrame` for animation
- [ ] Error boundaries exist for dynamic content
- [ ] Console is clean — no leftover logs, warnings, or errors

---

## The Wow Moment Checklist

Before delivery, verify the artifact's wow moment:

1. **Is it specific?** — "The particles scatter when you click" not "it looks cool"
2. **Is it discoverable?** — Can the user find it without instruction? (Or is it an intentional easter egg?)
3. **Is it first?** — Does the wow moment happen within the first 5 seconds of interaction?
4. **Is it shareable?** — Would someone screenshot or screen-record it to show someone else?
5. **Is it earned?** — Does the technical craft behind it deserve respect?

If the artifact lacks a clear wow moment, it's not ready. Return to Phase 3.

---

## Pre-Flight Checklist

Before presenting any artifact to the user:

```
ANTI-SLOP PRE-FLIGHT
─────────────────────
[ ] No gradient sin
[ ] No center trap
[ ] No rounded corner plague
[ ] No font surrender
[ ] No card grid cemetery
[ ] No skeleton screen
[ ] No motion desert
[ ] Performance gates pass
[ ] Accessibility gates pass
[ ] Responsiveness gates pass
[ ] Wow moment is clear and specific
[ ] No inline styles that could be CSS classes (unless dynamic)
[ ] Event listeners cleaned up on teardown
[ ] No setInterval without cleanup — use requestAnimationFrame for animation
[ ] Error boundaries exist for dynamic content
[ ] Console is clean — no leftover logs, warnings, or errors
```

If any gate fails, fix it before presenting.
