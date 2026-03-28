# Technique Matrix — Goal to Technology Selection

## Performance Hierarchy

Always select the **lightest** technology that achieves the desired effect:

```
1. CSS-only          ← Best performance. Transforms, transitions, scroll-driven animations.
2. CSS + minimal JS  ← View Transitions API, Container Queries, IntersectionObserver.
3. Canvas 2D         ← Generative art, pixel manipulation, particle systems (up to ~10K elements).
4. SVG + D3          ← Data visualization, complex shapes, small element counts (<5K).
5. WebGL / Three.js  ← 3D scenes, shader effects, large particle systems (10K-1M elements).
6. WebGPU            ← Compute shaders, massive parallelism, fluid dynamics. Cutting edge.
```

Heavier tech is not better tech. A CSS-only animation that achieves the effect is always preferred over a Canvas implementation.

---

## Goal → Technique Mapping

### Animation & Motion

| Goal | Primary Technique | Fallback | Notes |
|------|------------------|----------|-------|
| Scroll-driven effects | CSS `scroll-timeline` | GSAP ScrollTrigger | CSS is off-main-thread, zero JS |
| Page/state transitions | View Transitions API | GSAP + manual DOM swap | VT API handles cross-fade automatically |
| Micro-interactions (hover, click) | CSS transitions + `:hover`/`:active` | Motion/Framer spring physics | CSS for simple, spring for bouncy/playful |
| Choreographed sequences | GSAP timeline | CSS `@keyframes` with `animation-delay` | GSAP for complex, CSS for simple stagger |
| Spring physics | CSS `linear()` easing | Motion `type: "spring"` or custom spring fn | CSS springs landed in 2025 |
| Parallax | CSS `scroll-timeline` + `translateZ` | GSAP ScrollTrigger | CSS perspective-based is smoothest |
| Entry animations | CSS `@starting-style` + transitions | GSAP `.from()` | `@starting-style` is the modern CSS approach |
| Exit animations | View Transitions API | `AnimatePresence` (Motion) | VT API handles unmounting gracefully |

### Rendering

| Goal | Primary Technique | Fallback | Notes |
|------|------------------|----------|-------|
| Generative art (2D) | p5.js or Canvas 2D | SVG (small element counts) | p5.js for creative coding, raw Canvas for performance |
| Generative art (3D) | Three.js | CSS 3D transforms (simple) | Three.js for real 3D; CSS for card flips, perspective tricks |
| Data visualization | D3.js (SVG) | D3 + Canvas (large datasets) | SVG under 5K elements, Canvas above |
| Shader effects | WebGL + GLSL | CSS `paint()` worklets | Shaders for per-pixel computation |
| Particle systems (small) | Canvas 2D | CSS animations (very few particles) | Canvas handles thousands efficiently |
| Particle systems (large) | WebGL instanced rendering | WebGPU compute shaders | 10K+ particles need GPU |
| Text rendering | DOM/CSS | Canvas `fillText` (if in canvas context) | DOM text is always sharper and more accessible |
| 3D product showcase | Three.js + GLB models | CSS 3D transforms (flat objects) | Use OrbitControls for interaction |

### Interaction

| Goal | Primary Technique | Notes |
|------|------------------|-------|
| Drag & drop | Pointer Events API + `requestAnimationFrame` | Use `touch-action: none` for mobile |
| Gesture recognition | Pointer Events + velocity tracking | Calculate from position delta / time delta |
| Magnetic cursor | `mousemove` + lerp toward target | `current += (target - current) * 0.1` per frame |
| Scroll snapping | CSS `scroll-snap-type` | Pure CSS, no JS needed |
| Pinch/zoom | Touch Events + transform matrix | Or use a library like Panzoom |
| Physics-based interaction | Custom spring/verlet integration | Or matter.js for full rigid body |
| Keyboard navigation | DOM focus management + `keydown` | Essential for accessibility |
| Audio interaction | Web Audio API | `AudioContext` must be started from user gesture |

### Data

| Goal | Primary Technique | Notes |
|------|------------------|-------|
| Standard charts | D3.js | Or Chart.js for quick prototypes |
| Force-directed graphs | D3-force | Canvas rendering for large graphs |
| Geographic maps | D3-geo + TopoJSON | Or Leaflet/Mapbox for tile-based |
| Treemaps / sunbursts | D3-hierarchy | SVG for interactive, Canvas for large |
| Real-time streaming | WebSocket + D3 transitions | Throttle updates to 60fps max |
| Scrollytelling data | Scrollama + D3 | Sticky container + step detection |

### Narrative

| Goal | Primary Technique | Notes |
|------|------------------|-------|
| Scrollytelling | Scrollama (step detection) + GSAP (animation) | Or pure CSS scroll-driven for simpler narratives |
| Branching stories | State machine + DOM rendering | JSON-based story graph with transition logic |
| Progressive reveal | IntersectionObserver + CSS transitions | Reveal elements as they enter viewport |
| Section transitions | View Transitions API | Morph elements between story sections |
| Snap scrolling | CSS `scroll-snap-type: y mandatory` | Add `scroll-snap-align: start` to sections |

---

## Single-File Architecture

Most artifacts should be deliverable as a **single HTML file** (an "HTML ROM"):

**Rules:**
- All CSS inlined in `<style>` tags
- All JavaScript inlined in `<script>` tags
- External libraries loaded via CDN `<script src>` tags
- Images as base64 data URIs (or SVG inline) when possible
- Fonts via Google Fonts CDN link or system font stack

**CDN sources for common libraries:**
```html
<!-- p5.js -->
<script src="https://cdn.jsdelivr.net/npm/p5@1/lib/p5.min.js"></script>

<!-- Three.js -->
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170/build/three.module.min.js"}}</script>

<!-- D3.js -->
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

<!-- GSAP + ScrollTrigger -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>

<!-- Tone.js (audio) -->
<script src="https://cdn.jsdelivr.net/npm/tone@14"></script>
```

**When single-file is not feasible:** Multi-component React apps, apps requiring build steps, or artifacts with large asset dependencies should use `/web-artifacts-builder` for proper project scaffolding.

---

## Animation Timing Reference

| Context | Duration | Easing |
|---------|----------|--------|
| Hover state | 100-200ms | `ease-out` or spring (high stiffness) |
| Click feedback | 50-150ms | `ease-out` |
| Element entry | 300-500ms | `ease-out` or spring (medium stiffness) |
| Page transition | 300-600ms | `ease-in-out` or View Transitions default |
| Scroll-driven | continuous | `linear` (scroll position IS the timeline) |
| Loading reveal | 500-1000ms | `ease-out` with stagger |
| Stagger delay | 30-80ms between elements | — |
| Attention pulse | 1-2s repeating | `ease-in-out` |

**Spring presets:**
```
Snappy button:    stiffness: 500, damping: 30, mass: 1
Bouncy element:   stiffness: 200, damping: 10, mass: 1
Smooth slide:     stiffness: 100, damping: 20, mass: 1
Heavy/dramatic:   stiffness: 80,  damping: 15, mass: 2
Wobbly playful:   stiffness: 150, damping: 8,  mass: 0.8
```

---

## Browser Compatibility Notes (2025-2026)

| Feature | Chrome | Firefox | Safari | Use? |
|---------|--------|---------|--------|------|
| CSS scroll-driven animations | Stable | Flag | Safari 26+ | Yes, with GSAP fallback |
| View Transitions API (SPA) | Stable | Stable | Stable | Yes |
| Container Queries | Stable | Stable | Stable | Yes |
| CSS `@starting-style` | Stable | Stable | Safari 18.2+ | Yes |
| WebGPU | Stable | Flag | Partial | Only for advanced use cases |
| CSS `paint()` worklets | Stable | No | No | Chrome-only, use with caution |
| Vibration API | Stable | Stable | No | Mobile-only enhancement |
| View Transitions (MPA) | Stable | Partial | Partial | Use with caution |
