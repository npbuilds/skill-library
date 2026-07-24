# Charting Framework Matrix — 2026

> Provenance tags: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>`. Sourced from `research/dataviz-landscape-2026.md` (Brief `SPK-20260723-dataviz-2026`).
> This is the fast-decay layer of the suite — re-verify ~every 6–12 months.

## The 90/10 rule (the framing)

Use a **charting library for the standard 90%** of charts; reserve **raw D3 for the bespoke 10%** — a genuinely novel visual no library can express. In 2026 the development and maintenance cost of hand-written D3 for standard chart types rarely justifies itself. `ext-verified` (youngju.dev deep-dive 2026-05; databrain 2026), `vintage:2026-05`.

## Three orthogonal choices when picking a JS library

1. **Rendering:** SVG vs Canvas vs WebGL/WebGPU (see `rendering-by-volume.md`).
2. **Framework binding:** framework-agnostic (ECharts, Vega-Lite) vs framework-bound (Recharts/Visx/Nivo for React).
3. **License:** MIT/Apache-2.0 vs commercial.
`ext-verified` (noble desktop / usedatabrain 2026), `vintage:2026`.

## JavaScript / web

| Library | Rendering | Binding | Best for | Provenance |
|---|---|---|---|---|
| **ECharts 6** | Canvas (SVG option) | Agnostic | Enterprise/business dashboards, many chart types; "visualization platform" (Nov 2025) | `ext-verified`, `vintage:2025-11` |
| **Recharts** | SVG | React | The common 80% of React dashboards; simplest declarative API | `ext-verified`, `vintage:2026-05` |
| **Visx** (Airbnb) | SVG | React | D3 primitives as React components; control past Recharts, short of raw D3 | `ext-verified`, `vintage:2026-05` |
| **Nivo** | SVG/Canvas | React | Batteries-included, strong server-side rendering | `ext-verified`, `vintage:2026-05` |
| **Observable Plot** | SVG (Canvas option) | Agnostic | Exploratory + report charts; grammar-of-graphics from D3's authors | `ext-verified`, `vintage:2026` |
| **Vega-Lite 6** | SVG/Canvas (via Vega) | Agnostic | Declarative, reproducible, specification-driven; interaction grammar. `Altair` = Python front end | `ext-verified` (6.0.0 2025-03-27), `vintage:2025-03` |
| **Plotly.js** | SVG + WebGL traces | Agnostic | Interactive/3D; `scattergl` for larger data | `ext-verified`, `vintage:2026` |
| **deck.gl 9** | WebGL2/WebGPU | Agnostic (React layer) | Millions of points; geospatial-first (Uber origin) | `ext-verified`, `vintage:2026` |
| **D3** | SVG/Canvas | Agnostic | The bespoke 10% only | `ext-verified`, `vintage:2026` |

## The 2026 landscape in one paragraph

Observable Plot sits as a grammar layer on top of D3; the React camp splits into Visx, Recharts, and Nivo; enterprise goes to ECharts 6 and Plotly; Vega-Lite 6.x carries the declarative side; deck.gl owns millions-of-points GPU rendering. For ~80% of needs, **Recharts (React) · ECharts (universal) · Observable Plot (blog/report)** cover it. `ext-verified` (youngju.dev 2026-05), `vintage:2026-05`.

## Python

| Library | Role | Notes |
|---|---|---|
| **matplotlib** | Foundational full-control | The base layer everything else sits beside | `ext-verified`, `vintage:2026` |
| **seaborn** | Statistical defaults | Sensible statistical plots over matplotlib | `ext-verified`, `vintage:2026` |
| **plotly** | Interactive / 3D | Built on plotly.js; use `scattergl` (WebGL) past ~100k points | `ext-verified`, `vintage:2026` |
| **altair** | Declarative | Vega-Lite grammar in Python; tracks Vega-Lite 6.x | `ext-verified`, `vintage:2026` |
| **bokeh** | Pure-Python web | Browser-targeted without writing JS | `ext-verified`, `vintage:2026` |
| **streamlit / dash / panel** | Dashboard apps | Turn scripts/notebooks into shareable dashboards | `ext-verified`, `vintage:2026` |

The Python stack is **more stable than the JS stack** — the libraries barely moved; the *recommendation logic* (which to reach for) is what changed. `internal-estimate`.

## Selection heuristics

- **React app, standard charts** → Recharts. Outgrowing it → Visx. `internal-estimate`.
- **Framework-agnostic business dashboard, many chart types** → ECharts 6. `internal-estimate`.
- **Report / blog / exploratory** → Observable Plot (JS) or Altair (Python). `internal-estimate`.
- **Reproducible, spec-driven, shareable JSON** → Vega-Lite / Altair. `internal-estimate`.
- **Millions of points or geospatial** → deck.gl 9 (or server-side aggregation first). `internal-estimate`.
- **Novel visual no library expresses** → D3, and only then. `internal-estimate`.

## Refuted lore — `do-not-use`

- "For anything interactive on the web you should write D3 by hand." False in 2026 for standard charts. `do-not-use`.
- "Recharts is the React charting answer." Incomplete — the React camp is now a three-way split (Recharts/Visx/Nivo). `do-not-use` as a complete answer.
