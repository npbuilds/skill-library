---
name: interactive-dashboards
description: >
  Build interactive, at-scale, and real-time data visualizations. Reference when choosing a
  rendering technology by data volume (SVG vs Canvas vs WebGL/WebGPU), selecting a 2026 charting
  framework (ECharts, Recharts, Visx, Nivo, deck.gl, Vega-Lite, Plotly), designing dashboards
  with linked views and progressive disclosure, or handling streaming and embedded analytics.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Interactive Dashboards — Delivery at Scale

`chart-selection` decides *what* to show. This skill decides *how to render and deliver it* when the chart is interactive, the data is large, or the view updates in real time. The two most common failures here are the opposite of each other: reaching for hand-written D3 on a chart a library would draw in ten lines, and reaching for a Canvas library on a dataset that needs a GPU. Both are choices this skill exists to get right.

The single most important decision is **rendering technology, and it is dictated by data volume, not preference.**

## Rendering by Data Volume

| Marks on screen | Renderer | Why it wins here | Representative libraries |
|---|---|---|---|
| **< ~10,000** | **SVG** | Each mark is a DOM node — crisp at any zoom, inspectable, ARIA-addressable, print-quality. Accessibility and interactivity are close to free. | Vega-Lite (→SVG), Recharts, Observable Plot, D3-SVG |
| **~10k – ~500k** | **Canvas** | Immediate-mode raster — one `<canvas>`, no per-mark DOM node, so the browser stops choking on element count. | ECharts 6, Plotly, Chart.js |
| **> ~500k → millions** | **WebGL / WebGPU** | GPU parallelism draws points in bulk; downsampling (e.g. LTTB) runs as a compute shader; hit-testing is GPU-accelerated. | deck.gl 9, regl-based renderers, WebGPU charting |

**The ceiling is real.** Canvas libraries — ECharts included — degrade past roughly 500k–1M points and can crash a browser tab near 10M. If you are plotting more than a million marks, the answer is a WebGL/WebGPU framework *or* server-side aggregation before the data ever reaches the browser.

**The accessibility trade.** SVG gives you screen-reader access, keyboard focus, and print fidelity for free because the marks are real elements. The moment you move to WebGL you *lose* all of that and must rebuild it deliberately: an alternative data-table view, keyboard navigation, and an ARIA summary. Never let scale silently cost you accessibility — aggregate or downsample first, and only go GPU when the data genuinely demands it.

## Framework Selection (2026)

There is no single "best" library; pick by ecosystem and job. See `references/dashboard-frameworks-2026.md` for the full matrix with versions and provenance.

**The 90/10 rule.** Use a charting library for the standard 90% of charts. Reserve raw D3 for the bespoke 10% — a genuinely novel visual no library can express. In 2026 the maintenance cost of hand-rolled D3 for standard charts rarely pays off.

**JavaScript / web:**
- **ECharts 6** (Nov 2025) — universal, framework-agnostic, Canvas-first; repositioned as a "visualization platform." The default for enterprise/business dashboards with many chart types.
- **React camp (now split three ways):**
  - **Recharts** — declarative, simplest, covers the common 80%. Default for a straightforward React dashboard.
  - **Visx** (Airbnb) — D3 primitives as React components. Maximum control when you're outgrowing Recharts but not writing raw D3.
  - **Nivo** — batteries-included with strong server-render support.
- **Observable Plot** — the grammar-of-graphics layer maintained by D3's authors. The right default for exploratory and report charts you'd otherwise hand-write in D3.
- **Vega-Lite 6** (6.0.0, Mar 2025) — declarative grammar of *interaction*; compiles to Vega→SVG. Excellent for specification-driven, reproducible charts. `Altair` is its Python front end.
- **deck.gl 9** — GPU (WebGL2/WebGPU) framework for millions of points; geospatial-first.
- **D3** — the bespoke 10% only.

**Python:** `plotly` (interactive/3D, built on plotly.js), `bokeh` (pure-Python web), `altair` (declarative, Vega-Lite), `streamlit`/`dash`/`panel` (dashboard apps). For anything beyond ~100k points in the browser, prefer `plotly` with WebGL traces (`scattergl`) or push aggregation server-side.

## Dashboard Design

**Progressive disclosure** is the backbone. Layer the interface: overview first (aggregated), then zoom/filter, then detail-on-demand (individual records). This is Shneiderman's mantra and it scales cleanly to large data — the overview is cheap because it's aggregated, and detail is fetched only when asked for.

**Linked views.** A selection in one chart should filter the others (brushing-and-linking). Keep one shared data model so every view reads the same filtered state; inconsistent filters across tiles erode trust faster than any visual flaw.

**Density over decoration.** Dashboards are scanned repeatedly by domain experts. Optimize for scanning speed: sparklines, bullet charts, small multiples, KPI tiles with up/down deltas and threshold colors. Minimize chrome. Assume the viewer already knows the domain and checks this daily.

**Consistent encoding across tiles.** If "Region A" is blue in one tile it is blue in every tile. Cross-tile color drift forces the viewer to re-learn the mapping on every glance.

## Real-Time & Streaming

- **Update the data, not the chart.** Re-render the marks against new data; do not tear down and rebuild the chart object each tick. Most libraries have a data-update path that diffs efficiently — use it.
- **Windowing.** Streaming views need a bounded window (last N points / last T minutes). Unbounded append is the most common cause of a dashboard that starts fast and degrades over an afternoon.
- **Throttle to the human, not the socket.** Data may arrive at 60+ messages/sec; the eye reads maybe 4–10 updates/sec. Batch incoming messages and repaint on an animation frame, not per message.
- **Downsample on ingest.** For high-frequency series, apply LTTB or min/max-per-pixel downsampling before drawing — a 4000-pixel-wide chart cannot show more than ~8000 meaningful points anyway.

## Embedded Analytics

The 2026 shift is from standalone dashboards to analytics *inside* the product. When embedding:
- Prefer a framework-native library (Recharts/Visx in React) so the charts inherit the host app's theme, state, and build.
- Isolate the data layer so the embedded view reads the same source of truth as the rest of the app.
- Respect the host's theme (light/dark) and container sizing — charts must be responsive to their tile, not a fixed pixel size.

## Common Mistakes

1. **Hand-writing D3 for a standard chart.** The bespoke 10% is real but small. If a library draws it, use the library.
2. **Canvas for millions of points.** It will feel fine at 100k and crash at 10M. Choose the renderer for the *ceiling*, not the demo dataset.
3. **Losing accessibility at the WebGL boundary** without adding an alt-table and keyboard path back.
4. **Repainting per stream message** instead of batching to an animation frame.
5. **Unbounded streaming buffers** that leak memory and slow the page over time.
6. **Independent filters per tile** instead of one shared, linked data model.

## When This Applies

Use this skill whenever you are:
- Choosing a rendering technology or charting framework for a real project
- Building a dashboard with multiple linked or drill-down views
- Diagnosing a slow, janky, or crashing visualization
- Handling real-time, streaming, or high-frequency data
- Embedding analytics inside a product UI

For the full 2026 framework matrix (versions, rendering model, license, provenance) see `references/dashboard-frameworks-2026.md`; for the rendering decision with source-tagged point-count ceilings see `references/rendering-by-volume.md`.
