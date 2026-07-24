# Rendering by Data Volume — Decision Reference

> Provenance tags: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>`. Sourced from `research/dataviz-landscape-2026.md` (Brief `SPK-20260723-dataviz-2026`).
> Point-count ceilings are **source-reported, not independently benchmarked here** — treat as order-of-magnitude.

## The decision

Choose the renderer by the number of marks drawn at once, sized for the **ceiling** of your data, not the demo.

| Marks on screen | Renderer | Mechanism | Cost | Representative libraries |
|---|---|---|---|---|
| **< ~10,000** | **SVG** | One DOM node per mark | Element count; slows as nodes grow | Vega-Lite (→SVG), Recharts, Observable Plot, D3-SVG |
| **~10k – ~500k** | **Canvas** | Immediate-mode raster, one `<canvas>` | Redraw cost per frame; no free interactivity | ECharts 6, Plotly, Chart.js |
| **> ~500k → millions** | **WebGL / WebGPU** | GPU-parallel draw; shader downsampling; GPU hit-testing | Setup complexity; accessibility must be rebuilt | deck.gl 9, regl-based, WebGPU charting |

## Ceilings (source-reported)

- Canvas libraries, ECharts included, become the bottleneck **past ~500k–1M points**. `ext-verified` (lightningchart 2026), `vintage:2026`.
- At **~10M points**, ECharts can **crash the browser tab**. `ext-verified` (lightningchart 2026), `vintage:2026`.
- WebGPU charting can **pan/zoom ~1M points** smoothly with LTTB downsampling as a compute shader and GPU hit-testing. `ext-verified` but early-adoption / demo-sourced, treat as `Likely`, `vintage:2026`.

## What each tier buys and costs

**SVG** — buys: crisp at any zoom, per-mark inspectability, ARIA/keyboard access, print quality. Costs: dies on element count above ~10k. `internal-estimate`.

**Canvas** — buys: escapes the DOM element-count wall; smooth into the hundreds of thousands. Costs: no free hit-testing (you compute it), no free accessibility (marks aren't elements). `internal-estimate`.

**WebGL/WebGPU** — buys: millions of marks, GPU-accelerated pan/zoom and hit-testing. Costs: setup complexity, and **accessibility is gone by default** — you must add an alternative data-table view, keyboard navigation, and an ARIA summary. `internal-estimate`.

## The accessibility trade (do not skip)

Moving from SVG to WebGL silently drops screen-reader access, keyboard focus, and print fidelity, because the marks stop being DOM elements. Before going GPU:

1. **Aggregate or downsample first.** A 4000px-wide chart shows at most ~8000 meaningful points; LTTB or min/max-per-pixel gets you back under the SVG/Canvas ceilings for most series. `internal-estimate`.
2. **If you must go WebGL**, rebuild the floor: alternative data-table view + keyboard path + ARIA summary. `ext-verified` (W3C dataviz-a11y guidance), `vintage:2026`.

## Server-side escape hatch

For genuinely massive data, aggregate **before it reaches the browser** (server-side rollups, tiling, or pre-binned aggregates). The fastest browser renderer is the one you never make draw 10M raw points. `internal-estimate`.

## Refuted lore — `do-not-use`

- "Canvas scales to any dataset." False — the GPU tier begins past ~500k–1M points. `do-not-use`.
- "WebGL is always faster, so default to it." False — under ~10k marks SVG is simpler, accessible, and fast; GPU setup is wasted. `do-not-use`.
