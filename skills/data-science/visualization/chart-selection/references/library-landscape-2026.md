# Visualization Library Landscape — 2026

> Provenance tags: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>`. Sourced from `research/dataviz-landscape-2026.md` (Brief `SPK-20260723-dataviz-2026`).
> Fast-decay layer — re-verify ~every 6–12 months. For the delivery/rendering angle and selection
> heuristics, the fuller matrix lives at `interactive-dashboards/references/dashboard-frameworks-2026.md`.

## Two framing rules

- **Rendering follows data volume:** SVG < ~10k marks · Canvas ~10k–500k · WebGL/WebGPU > ~500k. Canvas ceiling ~500k–1M; crashes near 10M. `ext-verified` (lightningchart 2026), `vintage:2026`.
- **90/10 rule:** chart library for the standard 90%, raw D3 for the bespoke 10%. `ext-verified` (youngju.dev 2026-05), `vintage:2026-05`.

## What changed since this suite was first written (Mar 2026 baseline)

| Change | Detail | Provenance |
|---|---|---|
| **ECharts 6 shipped** | Nov 2025; universal, Canvas-first, framed as a "visualization platform," not just a chart library | `ext-verified`, `vintage:2025-11` |
| **React camp split three ways** | Recharts (simple) · Visx (D3 primitives for React) · Nivo (batteries-included) — "use Recharts" is no longer a complete answer | `ext-verified`, `vintage:2026-05` |
| **Observable Plot matured** | Now the grammar-of-graphics layer maintained by D3's authors; the default over raw D3 for exploratory/report charts | `ext-verified`, `vintage:2026` |
| **Vega-Lite 6** | 6.0.0 released 2025-03-27 (latest 6.4.x); declarative grammar of interaction; `Altair` tracks it in Python | `ext-verified` (vega/vega-lite releases; Wikipedia), `vintage:2025-03` |
| **deck.gl 9 + WebGPU** | GPU framework for millions of points, geospatial-first; the answer above the Canvas ceiling | `ext-verified`, `vintage:2026` |

## JavaScript quick map

- **Standard React dashboard** → Recharts. Outgrowing it → Visx. `internal-estimate`.
- **Universal business dashboard, many chart types** → ECharts 6. `internal-estimate`.
- **Report / blog / exploratory** → Observable Plot. `internal-estimate`.
- **Reproducible, spec-driven** → Vega-Lite 6 (Altair in Python). `internal-estimate`.
- **Millions of points / geospatial** → deck.gl 9, or aggregate server-side first. `internal-estimate`.
- **Novel visual no library expresses** → D3 (the 10%). `internal-estimate`.

## Python quick map

`matplotlib` (full control) · `seaborn` (statistical defaults) · `plotly` (interactive/3D, `scattergl` past ~100k pts) · `altair` (declarative, Vega-Lite 6) · `bokeh` (pure-Python web) · `streamlit`/`dash`/`panel` (dashboard apps). The Python stack barely moved; the *recommendation logic* changed more than the libraries. `ext-verified` (knowledgehut/technotification 2026) + `internal-estimate`, `vintage:2026`.

## Refuted lore — `do-not-use`

- "For anything interactive on the web, hand-write D3." False in 2026 for standard charts. `do-not-use`.
- "Recharts is *the* React charting library." Incomplete — three-way split now. `do-not-use` as a complete answer.
- "Canvas scales to any dataset." False — GPU tier begins past ~500k–1M points. `do-not-use`.
