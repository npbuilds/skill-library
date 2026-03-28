# Composition Recipes — Layout Patterns for Artifacts

## Full-Viewport Patterns

### The Hero Canvas
One full-screen element dominates. All interaction happens within this single canvas.

```
┌─────────────────────────────┐
│                             │
│                             │
│      [FULL CANVAS]          │
│                             │
│                             │
│              [small controls│
│               bottom-right] │
└─────────────────────────────┘
```

**Use for:** Generative art, simulations, immersive experiences
**CSS:** `width: 100vw; height: 100vh; position: fixed;`
**Controls:** Overlay with `pointer-events: none` on container, `pointer-events: auto` on controls

### The Split Stage
Two zones: a persistent visual element and a scrolling content area.

```
┌──────────────┬──────────────┐
│              │              │
│   [STICKY    │  [SCROLLING  │
│    VISUAL]   │   CONTENT]   │
│              │              │
│              │              │
└──────────────┴──────────────┘
```

**Use for:** Scrollytelling, data narratives, documentation with live preview
**CSS:** Grid with `position: sticky` on the visual column
**Mobile:** Stack vertically, visual becomes a fixed mini-bar or collapses

### The Layered Depth
Multiple overlapping layers at different visual depths.

```
┌─────────────────────────────┐
│  ░░░░░ [BACKGROUND LAYER]   │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░ │
│     ┌───────────────┐       │
│     │ [MIDGROUND]   │       │
│     │               │       │
│     │  ┌─────────┐  │       │
│     │  │[FORE-   │  │       │
│     │  │ GROUND] │  │       │
│     └──┴─────────┴──┘       │
└─────────────────────────────┘
```

**Use for:** Immersive experiences, atmospheric pieces, parallax
**CSS:** `position: fixed` layers with `z-index` stacking, `filter: blur()` for depth
**Interaction:** Parallax on scroll or cursor position

---

## Content-Driven Patterns

### The Magazine Spread
Mixed-size elements with editorial rhythm. Not a uniform grid.

```
┌─────────────────────────────┐
│ [LARGE FEATURE IMAGE/VIZ]   │
│                             │
├───────────┬─────────────────┤
│ [CAPTION] │ [BODY TEXT      │
│           │  flowing around │
│           │  the visual]    │
├───────────┴────┬────────────┤
│ [PULL QUOTE    │ [SMALL     │
│  large text]   │  VISUAL]   │
└────────────────┴────────────┘
```

**Use for:** Data stories, articles, case studies
**CSS:** CSS Grid with `grid-template-areas` for named regions
**Rhythm:** Alternate between full-width moments and two-column sections

### The Dashboard Mosaic
Multiple data panels with varied sizing reflecting importance.

```
┌───────────────────┬─────────┐
│ [PRIMARY METRIC   │ [SMALL  │
│  large, prominent]│  METRIC]│
├─────────┬─────────┼─────────┤
│ [CHART  │ [CHART  │ [SMALL  │
│  medium]│  medium]│  METRIC]│
├─────────┴─────────┴─────────┤
│ [DETAIL TABLE / LIST        │
│  full width, scrollable]    │
└─────────────────────────────┘
```

**Use for:** Dashboards, monitoring, status pages
**CSS:** CSS Grid with `grid-template-rows: auto` and varying `span` values
**Anti-slop:** Vary card sizes. Never make all cards identical.

### The Card River
A flowing, varied collection. Not a grid — a curated stream.

```
┌──────────┐
│ [CARD    │  ┌────────────────┐
│  small]  │  │ [CARD          │
└──────────┘  │  large, spans  │
┌─────────────┤  two rows]     │
│ [CARD       │                │
│  medium]    └────────────────┘
│             │  ┌──────────┐
└─────────────┘  │ [CARD    │
                 │  small]  │
                 └──────────┘
```

**Use for:** Portfolios, galleries, collections, search results
**CSS:** CSS `column-count` for masonry, or CSS Grid with `grid-auto-flow: dense`
**Interaction:** Cards expand on click/tap to reveal detail

---

## Scroll Patterns

### The Snap Sections
Full-viewport sections with mandatory snap scrolling.

```
┌─────────────────┐
│ [SECTION 1]     │ ← snap
│                 │
└─────────────────┘
┌─────────────────┐
│ [SECTION 2]     │ ← snap
│                 │
└─────────────────┘
┌─────────────────┐
│ [SECTION 3]     │ ← snap
│                 │
└─────────────────┘
```

**CSS:** `scroll-snap-type: y mandatory` on container, `scroll-snap-align: start` on sections
**Use for:** Presentations, product showcases, sequential reveals
**Caution:** Mandatory snap can feel restrictive. Use `proximity` for gentler snapping.

### The Infinite Scroll Canvas
Content extends in one or more directions beyond the viewport.

**Use for:** Explorable visualizations, zoomable interfaces, spatial narratives
**CSS:** Large canvas with `overflow: auto` or custom scroll handling
**Interaction:** Pan (drag), zoom (pinch/wheel), minimap for orientation

---

## Responsive Adaptation Strategies

| Pattern | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Split Stage | Side-by-side | Side-by-side (narrower) | Stacked vertically |
| Magazine Spread | Full layout | Simplified grid | Single column |
| Dashboard Mosaic | Multi-column | 2-column | Single column, cards stack |
| Card River | Multi-column masonry | 2-column | Single column |
| Snap Sections | Full viewport | Full viewport | Full viewport (works naturally) |
| Hero Canvas | Full viewport | Full viewport | Full viewport (touch interaction) |
| Layered Depth | Full parallax | Reduced parallax | Flat (no parallax) |

**Universal mobile rules:**
- Touch targets minimum 44x44px
- No hover-dependent interactions (hover can enhance, but not gate)
- Font sizes minimum 16px body (prevents iOS zoom)
- Reduce motion on mobile (performance and battery)
