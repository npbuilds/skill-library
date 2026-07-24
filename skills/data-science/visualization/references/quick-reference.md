# Visualization Subdomain — Quick Reference

> Provenance tags: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>` (as-of date for perishable facts). Sourced from `research/dataviz-landscape-2026.md`
> (Brief `SPK-20260723-dataviz-2026`). Refuted lore is tagged `do-not-use`.

## Subdomain map

| Skill | Layer | Owns |
|---|---|---|
| `visualization` | director | Routing, curriculum, conflict resolution |
| `chart-selection` | knowledge | Chart-type choice, design principles, accessibility, anti-patterns |
| `interactive-dashboards` | knowledge | Rendering by volume, framework choice, dashboards, streaming, embedded |
| `data-storytelling` | knowledge | Narrative spine, annotation-as-message, scrollytelling, pacing |

## The one rule that orders everything

Message → honest chart → scalable delivery → narrative. `internal-estimate`.
A fast dashboard of the wrong chart is still wrong; a beautiful story on a misleading chart amplifies the error.

## Rendering by data volume (the cheat sheet)

| Marks | Renderer | Libraries |
|---|---|---|
| < ~10k | SVG | Vega-Lite, Recharts, Observable Plot |
| ~10k–500k | Canvas | ECharts 6, Plotly, Chart.js |
| > ~500k → millions | WebGL/WebGPU | deck.gl 9, WebGPU charting |

Canvas ceiling: degrades past ~500k–1M points, crashes near 10M. `ext-verified` (lightningchart 2026), `vintage:2026`.

## 2026 library landscape at a glance

- **90/10 rule:** chart library for the standard 90%, D3 only for the bespoke 10%. `ext-verified`, `vintage:2026-05`.
- **ECharts 6** — Nov 2025, universal, "platform." `ext-verified`, `vintage:2025-11`.
- **React split:** Recharts (simple) · Visx (control) · Nivo (batteries-included). `ext-verified`, `vintage:2026-05`.
- **Observable Plot** — D3-team grammar-of-graphics layer. `ext-verified`, `vintage:2026`.
- **Vega-Lite 6.0.0** — Mar 2025; `Altair` is its Python front end. `ext-verified`, `vintage:2025-03`.
- **deck.gl 9** — GPU, millions of points, geospatial-first. `ext-verified`, `vintage:2026`.

## Accessibility floor

WCAG 2.2 + W3C dataviz-a11y note; Wong 8-color palette; never color alone. `ext-verified`, `vintage:2026`. Details in `chart-selection/references/accessibility-standards.md`.

## Refuted lore — `do-not-use`

- "Always hand-write D3 for web interactivity." False in 2026 for standard charts. `do-not-use`.
- "Canvas scales to any dataset." False — GPU tier begins past ~500k–1M points. `do-not-use`.

## Refresh cadence

Library/renderer facts are `vintage`-dated; re-verify ~every 6–12 months.
