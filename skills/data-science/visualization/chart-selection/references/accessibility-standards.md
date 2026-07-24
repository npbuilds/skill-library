# Chart Accessibility Standards — 2026

> Provenance tags: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>`. Sourced from `research/dataviz-landscape-2026.md` (Brief `SPK-20260723-dataviz-2026`).

## The standards that apply

- **WCAG 2.2** — the current success-criteria baseline (supersedes 2.1, which the older skill cited). `ext-verified` (disabilityworld, chartgen 2026), `vintage:2026`.
- **ARIA graphics practices** — roles/labels for chart structure. `ext-verified`, `vintage:2026`.
- **W3C RQTF "Data Visualization Accessibility" note** — the dataviz-specific guidance layered on top of WCAG. `ext-verified`, `vintage:2026`.

## Three layers of color accessibility

1. **Palette selection** — use a colorblind-safe categorical palette; sequential/diverging for ordered data.
2. **Contrast ratios** — WCAG AA: 4.5:1 normal text, 3:1 large text and graphical elements (unchanged from 2.1). `ext-verified`, `vintage:2026`.
3. **Redundant encoding** — never color alone; pair with shape, pattern, position, or label.

`ext-verified` (engineering a11y primers, 2026), `vintage:2026`.

## The Wong palette (concrete default)

Bang Wong's 8-color palette (Nature Methods) stays distinguishable across protanopia, deuteranopia, and tritanopia — the safe default categorical set. `ext-verified` (Wong 2011; rgblind 2026), `vintage:2011/reaffirmed-2026`.

| Name | Hex |
|---|---|
| Black | `#000000` |
| Orange | `#E69F00` |
| Sky blue | `#56B4E9` |
| Bluish green | `#009E73` |
| Yellow | `#F0E442` |
| Blue | `#0072B2` |
| Vermillion | `#D55E00` |
| Reddish purple | `#CC79A7` |

For ordered data use **viridis-family** (viridis/inferno/plasma/magma) — perceptually uniform — or ColorBrewer2 sequential/diverging scales. Avoid rainbow/jet. `ext-verified`, `vintage:2026`.

## Prevalence (why it matters)

Roughly **1 in 12 men and 1 in 200 women** have some color vision deficiency. `ext-verified` (rgblind 2026), `vintage:2026`.

## Beyond color — the fuller checklist

- **Text alternatives:** every chart needs a caption/alt-text stating the key message and data range. A screen reader cannot interpret a PNG. `ext-verified`, `vintage:2026`.
- **SVG structure:** expose ARIA role + label; SVG marks are addressable elements for free.
- **Keyboard navigation:** interactive charts should let a keyboard user move between data points.
- **Alternative data-table view:** offer the underlying numbers as a table — mandatory when the chart is Canvas/WebGL and the marks aren't DOM elements.
- **Sonification** (data-to-audio) — emerging for time-series; not yet a hard requirement. `Likely`, `ext-verified` (a11y tooling scorecards 2026), `vintage:2026`.
- **Print/grayscale:** supplement color with hatching/pattern fills; test in grayscale.
- **Reduced motion:** respect `prefers-reduced-motion` for any animated or scroll-driven chart.

## The WebGL accessibility cliff

Moving a chart from SVG to WebGL for scale **silently removes** screen-reader access, keyboard focus, and print fidelity — the marks stop being DOM elements. Before going GPU, aggregate/downsample to stay in SVG/Canvas; if you must go WebGL, rebuild the floor (alt-table + keyboard path + ARIA summary). `internal-estimate` + `ext-verified` (W3C dataviz-a11y note), `vintage:2026`. See `interactive-dashboards/references/rendering-by-volume.md`.

## Library accessibility defaults (2026 scorecard, directional)

An engineering primer scored Vega-Lite, Plotly, Observable Plot, ECharts, and D3 against: SVG/ARIA output, colorblind-safe default palettes, keyboard-navigable data points, screen-reader hierarchy, and an alternative table view. Declarative/SVG libraries (Vega-Lite, Observable Plot) tend to start closer to accessible; raw D3 and Canvas/WebGL libraries require the most manual work. `Likely`, `ext-verified` (disabilityworld 2026), `vintage:2026`.

## Refuted lore — `do-not-use`

- "Cite WCAG 2.1 for chart contrast." Superseded — 2.2 is current. `do-not-use`.
- "A colorblind-safe palette makes a chart accessible." Necessary, not sufficient — redundant encoding + text alternative + keyboard/table access are all required. `do-not-use` as a complete claim.
