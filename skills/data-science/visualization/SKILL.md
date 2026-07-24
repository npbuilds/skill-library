---
name: visualization
description: >
  Direct the visualization subdomain — route a data-communication need to the right specialist:
  single-chart messaging, at-scale or interactive dashboards, or narrative data storytelling.
  Use when the user needs to choose a chart, build a dashboard, render large data, or tell a
  story with data. Resolves conflicts between clarity, scale, and narrative.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Visualization Director

The department head for data communication within the data-science domain. Routes visualization questions to the right specialist, defines the learning order, and resolves conflicts between analytical clarity, rendering scale, and narrative pull.

The organizing principle for the whole subdomain is inherited from `chart-selection`: **a visualization begins with a message, not a chart type, a library, or a framework.** Every child skill assumes the message is already articulated; if it is not, start there.

## Routing Table

When a visualization question arrives, classify it and route accordingly:

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| "Which chart for this message?", chart-type choice, redesign a misleading chart | `chart-selection` | Chart-type selection + design principles |
| Accessibility of a chart, colorblind-safe palette, WCAG compliance | `chart-selection` | Owns the accessibility checklist + Wong palette |
| Anti-patterns (truncated axis, dual-axis, 3D, rainbow maps) | `chart-selection` | Owns the honesty rules |
| "Build a dashboard", real-time / streaming views, embedded analytics | `interactive-dashboards` | Live, multi-view, in-product delivery |
| "This is slow / crashes", millions of points, WebGL/WebGPU, Canvas vs SVG | `interactive-dashboards` | Rendering-by-data-volume decision |
| Library / framework choice (ECharts, Recharts, Visx, deck.gl, Vega-Lite, Plotly) | `interactive-dashboards` | Owns the 2026 library landscape |
| "Tell a story with this data", scrollytelling, a report or presentation narrative | `data-storytelling` | Narrative structure + annotation-as-message |
| Sequencing charts into an argument, guided reveal, one-message-per-slide | `data-storytelling` | Ordering and pacing of a data narrative |
| "Make this chart", generic | `chart-selection` first | Message + chart type before anything else |

### Multi-Skill Questions

Some questions need more than one skill. Load them in this order:

1. `chart-selection` — settle the message and the per-chart form first.
2. `interactive-dashboards` — choose renderer, framework, and interaction model for delivery.
3. `data-storytelling` — sequence and annotate the charts into a narrative.

This order is intentional: a fast, scalable dashboard of the *wrong* chart is still wrong, and a beautiful narrative built on a misleading chart amplifies the error. Correct form precedes delivery precedes narrative.

**Example multi-skill question**: "Build an interactive dashboard that walks execs through why revenue dropped."
1. `chart-selection` → pick the diagnostic charts (waterfall for the bridge, small multiples by segment) and annotate the drivers.
2. `interactive-dashboards` → Recharts/ECharts by data volume, linked filters, progressive disclosure (overview → drill-down).
3. `data-storytelling` → order the views as a narrative, one message per view, with a guided-reveal path for the presentation.

## Curriculum Order

For learning or progressive loading:

1. **Chart Selection** (foundation) — how to translate a message into an honest, accessible chart. Prerequisite to everything else: you cannot scale or narrate a chart that does not communicate.
2. **Interactive Dashboards** (application) — how to deliver charts at scale and interactively, choosing the renderer by data volume and the framework by fit.
3. **Data Storytelling** (synthesis) — how to sequence charts into an argument that holds attention and lands a decision.

### Level Progression
- **Foundational**: Chart Selection
- **Intermediate**: Interactive Dashboards
- **Advanced**: Data Storytelling
- **Not yet built**: geospatial visualization, animation/transitions as explanation, notebook-native EDA visualization

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| `interactive-dashboards` wants WebGL for scale, but `chart-selection` needs the chart screen-reader accessible | Keep SVG/Canvas with a downsample or aggregation; add an alternative data-table view if forced to WebGL | Accessibility is a floor, not a trade; aggregate before you abandon it |
| `data-storytelling` wants a dramatic reveal that relies on a truncated axis | Narrative loses; re-stage the reveal with annotation on a zero-baseline chart | An honest chart that surprises beats a misleading one that dazzles |
| `interactive-dashboards` favors a dense multi-series view, `chart-selection` flags overload (>5 series) | Highlight-one-gray-the-rest, or small multiples, inside the dashboard | Density is not the same as legibility |
| `chart-selection` picks a static form, but the data streams in real time | Escalate to `interactive-dashboards` for the live variant of the same chart family | The message stays; the delivery changes |

**General rule**: Message > honesty > accessibility > scale > interactivity > polish. When in doubt, protect the reader's correct understanding before the engineering.

## Scope Boundaries

**This director handles**: all data-communication questions — chart-type choice, design and accessibility, dashboard construction, rendering at scale, library/framework selection, and data storytelling.

**Escalate to the orchestrator when**:
- The underlying numbers need statistical validation before they are shown (Statistical Analysis)
- The data must be cleaned or reshaped before it can be plotted (Data Wrangling)
- A model's outputs are being visualized and need evaluation context (Modeling)
- The visualization exposes fairness or representational-bias concerns (Frontier — responsible-ai)
- The question spans multiple subdomains and needs orchestrator-level coordination

For the subdomain map, the 2026 library landscape at a glance, and the rendering-by-volume cheat sheet, see `references/quick-reference.md`.
