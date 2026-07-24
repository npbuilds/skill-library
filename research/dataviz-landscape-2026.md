# The Data Visualization Landscape 2026 — What the Data-Science Suite Must Know

**Compiled: 2026-07-23** · Brief ID: `SPK-20260723-dataviz-2026` · Depth: standard · Classification: investigative + generative

> Research round feeding the `skills/data-science/visualization/` expansion. Evidence is confidence-tagged
> (**Confirmed / Likely / Speculative / Contested**) per the spelunker contract. Figures destined for reference
> docs also carry a provenance tag: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>` (as-of date for perishable claims). Refuted lore is recorded, not deleted, tagged `do-not-use`.

---

## CORE CLAIM CONFIDENCE

**Confirmed** — The perishable layer of `chart-selection` (library table, accessibility version, rendering guidance) has measurably drifted from the 2026 landscape, while its principle layer (message-first framing, Tufte data-ink, anti-patterns) remains current. The suite's highest-leverage update is (a) a rendering-by-data-volume decision framework, (b) a refreshed 2026 library map, (c) a WCAG 2.2 accessibility upgrade, and (d) two new capability areas — interactive/at-scale dashboards and data storytelling — that the single-leaf `visualization` subdomain does not currently cover.

---

## KEY FINDINGS

1. **Charting is now a two-tier decision: pick a chart library for the standard 90%, reach for D3 only for the bespoke 10%.** [Confirmed] The 2023-era instinct to hand-roll D3 is a 2026 anti-pattern for standard charts — maintenance cost rarely justifies it.
2. **Rendering technology is chosen by data volume, not preference.** [Confirmed] SVG below ~10k marks, Canvas ~10k–500k, WebGL/WebGPU above ~500k into the millions. This is the single most important framework absent from the current skill.
3. **ECharts 6 (Nov 2025) repositioned itself as a "visualization platform," and deck.gl 9 + WebGPU own the millions-of-points tier.** [Confirmed] Canvas libraries (ECharts included) degrade past 500k–1M points and crash tabs near 10M.
4. **The React charting camp fragmented** into Recharts (simple/declarative), Visx (low-level D3-primitives-for-React), and Nivo (batteries-included). [Confirmed] "Use Recharts" is no longer a complete answer.
5. **Accessibility moved to WCAG 2.2** plus the W3C dataviz-a11y note; the Wong palette (8 colorblind-safe hexes) and redundant encoding are the concrete defaults, with sonification and keyboard-navigable data points emerging. [Confirmed / Likely]
6. **Data storytelling and scrollytelling matured into a discipline** with a de-facto standard toolchain (Scrollama v3.2.0, IntersectionObserver-driven), not just a newsroom novelty. [Confirmed]
7. **AI-assisted chart recommendation, real-time/streaming dashboards, and embedded analytics** are the dominant 2026 product trends. [Likely] — trend-report sourced, directionally strong but vendor-inflected.

---

## DETAILED FINDINGS

### 1. Library landscape 2026

**JavaScript/web.** Confidence: [Confirmed] because corroborated across independent 2026 comparison sources.
- **The 90/10 rule.** Use a chart library for standard charts; reserve D3 for genuinely unique visuals no library can express. `ext-verified` (youngju.dev deep-dive, 2026-05; databrain 2026), `vintage:2026-05`.
- **ECharts 6** shipped Nov 2025, framed as a "visualization platform, not a chart library"; universal (framework-agnostic), Canvas-first, strong for enterprise dashboards. `ext-verified` (lightningchart 2026), `vintage:2025-11`.
- **React split:** Recharts (declarative, simplest, covers the common 80%), Visx (Airbnb; D3 primitives as React components, maximum control), Nivo (batteries-included, server-render friendly). `ext-verified` (youngju.dev 2026), `vintage:2026-05`.
- **Observable Plot** is now the grammar-of-graphics layer maintained by D3's authors — the recommended default for exploratory + report charts where you'd otherwise write raw D3. `ext-verified` (Observable/Vega docs), `vintage:2026`.
- **Vega-Lite 6.0.0** released 2025-03-27 (latest 6.4.x); declarative grammar of *interaction*, compiles to Vega→SVG; **Altair** (Python) tracks it. `ext-verified` (vega/vega-lite releases; Wikipedia), `vintage:2025-03`.
- **deck.gl 9** — GPU (WebGL2/WebGPU) framework for millions of points, geospatial-first (Uber origin). `ext-verified` (deck.gl), `vintage:2026`.

**Python.** Confidence: [Confirmed].
- **matplotlib** remains the foundational full-control layer; **seaborn** the statistical-defaults layer; **plotly** the interactive/3D layer (built on plotly.js); **Altair** the declarative (Vega-Lite) layer; **bokeh** the pure-Python web layer. This part of the stack is stable — the *recommendation logic* changed more than the libraries. `ext-verified` (knowledgehut, technotification 2026), `vintage:2026`.

**Refuted lore** — `do-not-use`: "For anything interactive on the web you should write D3 by hand." False in 2026 for standard charts; only true for the bespoke 10%.

### 2. Rendering by data volume — the missing framework

Confidence: [Confirmed] because it is the consistent organizing principle across every 2026 comparison reviewed.

| Marks on screen | Renderer | Why | Representative libs |
|---|---|---|---|
| < ~10,000 | **SVG** | DOM nodes = crisp, inspectable, ARIA-addressable, print-quality | Vega-Lite→SVG, Recharts, Observable Plot (SVG mode), D3-SVG |
| ~10k – ~500k | **Canvas** | Immediate-mode raster; no per-mark DOM node | ECharts 6, Plotly, Chart.js |
| > ~500k → millions | **WebGL / WebGPU** | GPU parallelism; downsampling (e.g. LTTB) as compute shader; GPU hit-testing | deck.gl 9, regl-based, WebGPU charting |

- Canvas libraries "hit their ceiling" past 500k–1M points; ECharts crashes near 10M. `ext-verified` (lightningchart 2026), `vintage:2026`.
- WebGPU charting can pan/zoom a million points with LTTB downsampling on the GPU. [Likely] `ext-verified` but early-adoption, `vintage:2026`.
- **Trade-off to teach:** SVG buys accessibility + print for free; WebGL buys scale but you must *rebuild* accessibility (alt-table, keyboard nav) yourself.

### 3. Accessibility — upgrade to WCAG 2.2

Confidence: [Confirmed] on standard + palette; [Likely] on sonification adoption.
- Grounded in **WCAG 2.2** success criteria, ARIA graphics practices, and the **W3C RQTF "Data Visualization Accessibility"** note. `ext-verified` (disabilityworld, chartgen 2026), `vintage:2026`. *(The skill cited WCAG 2.1 before this round — one version stale; upgraded to 2.2 as part of this update.)*
- **Wong palette** (Nature Methods, Bang Wong) — the safest categorical set across protanopia/deuteranopia/tritanopia: black `#000000`, orange `#E69F00`, sky blue `#56B4E9`, bluish green `#009E73`, yellow `#F0E442`, blue `#0072B2`, vermillion `#D55E00`, reddish purple `#CC79A7`. `ext-verified` (rgblind, Wong 2011), `vintage:2011/reaffirmed-2026`.
- **~1 in 12 men, ~1 in 200 women** have color vision deficiency. `ext-verified`, `vintage:2026`.
- **Three layers of color accessibility:** palette selection · contrast ratios (4.5:1 text / 3:1 graphical, unchanged from 2.1) · redundant encoding (never color alone — add shape/pattern/position/label). `ext-verified`.
- **Emerging:** sonification (data-to-audio), keyboard-navigable data points, screen-reader hierarchy, and a mandatory alternative data-table view. [Likely] `ext-verified` (accessibility scoring of Vega-Lite/Plotly/Plot/ECharts/D3), `vintage:2026`.

### 4. Data storytelling & scrollytelling

Confidence: [Confirmed] on toolchain; [Likely] on "critical inflection point" framing (trend-source language).
- **Scrollama v3.2.0** is the de-facto standard, IntersectionObserver-based, heavily used by **The Pudding**; strong in data journalism, growing Svelte support alongside the historic React setups. `ext-verified` (cssauthor 2026; Pudding), `vintage:2026`.
- The discipline = narrative structure + annotation-as-message + staged reveals (overview → zoom → detail as the reader scrolls). Bridges directly from the existing message-first framing in `chart-selection`.
- Distinguish three delivery contexts (already latent in `chart-selection`'s context section): **dashboard** (scan speed), **presentation** (one message/slide), **report/scrollytelling** (guided narrative).

### 5. Product trends (context, lower weight)

Confidence: [Likely] — synthesized from vendor trend reports (Ajelix, Softweb, Infogram, Luzmo); directionally consistent but commercially motivated. Treat as `internal-estimate`.
- **AI-assisted charting** — tools recommend chart types, detect patterns, flag anomalies automatically.
- **Real-time / streaming dashboards** — table stakes for fintech, logistics, healthcare, IoT.
- **Embedded analytics** — the shift from standalone dashboards to analytics inside the product.
- **Personalization & spatial/immersive** — more speculative; noted, not built on. [Speculative]

### 6. Building visualizations with Claude Code (the CC-native workflow)

Confidence: [Confirmed] on capabilities present in this environment.
This is the "what can I actually do" answer — a workflow, not a library choice:

- **Artifacts** render a chart live in a side panel and iterate in-session — build an interactive **React + Recharts** dashboard, a self-contained HTML/D3 page, or a **Mermaid** diagram, then refine by conversation. Best for shareable, interactive deliverables. Self-contained only (inline CSS/JS, no external CDN), theme-aware, responsive.
- **The `dataviz` skill** (Anthropic) — a design-system-agnostic method: a form heuristic, a color formula with a runnable validator, and a *validated default palette* in `references/palette.md`. Load it **before writing any chart code** in any medium. Complements our `chart-selection` (which is chart-*type* selection); `dataviz` is the *visual-system* layer.
- **The `data:` plugin skills** — `data:create-viz`, `data:build-dashboard`, `data:data-visualization` for turnkey chart/dashboard generation from CSVs/dataframes.
- **`show_widget` (visualize MCP)** — render inline SVG/HTML widgets alongside chat for quick, non-artifact visuals; supports a `sendPrompt()` callback for interactivity.
- **Browser-preview verification loop** — `preview_start` → `read_page`/`read_console_messages`/`screenshot` to *prove* a chart renders correctly rather than asking the user to check. This is the honest-verification pattern for any web viz.
- **Live exemplar in this repo:** the **Neural Observatory** (`app/`, Firebase Hosting, https://skill-library-prod.web.app) is a production dashboard reading from Firestore — a working reference for the streaming/embedded patterns above.

**How these compose:** `chart-selection` (what chart) → `dataviz` skill (visual system + palette) → `interactive-dashboards` (renderer + framework by volume) → Artifact or `app/` (deliverable) → browser-preview loop (verify).

---

## EVIDENCE MAP

| Claim | Confidence | Basis |
|---|---|---|
| 90/10 chart-library-vs-D3 rule | Confirmed | Multiple independent 2026 comparisons |
| Rendering by volume (SVG/Canvas/WebGL) | Confirmed | Consistent across all 2026 sources |
| ECharts 6 Nov 2025, platform framing | Confirmed | lightningchart, youngju.dev |
| deck.gl 9 for millions of points | Confirmed | deck.gl docs, lightningchart |
| React split Recharts/Visx/Nivo | Confirmed | youngju.dev deep-dive |
| Vega-Lite 6.0.0 (2025-03-27) | Confirmed | vega/vega-lite releases, Wikipedia |
| WCAG 2.2 + Wong palette hexes | Confirmed | disabilityworld, rgblind, Wong 2011 |
| Sonification/keyboard-nav emerging | Likely | a11y tooling scorecards, 2026 |
| Scrollama v3.2.0 standard | Confirmed | cssauthor 2026, The Pudding |
| AI-charting / streaming / embedded trends | Likely | vendor trend reports (motivated) |
| Personalization / immersive | Speculative | trend reports only |

## GAPS & LIMITATIONS

- **Vendor bias:** the "trends" tier (§5) leans on marketing content; treated as `internal-estimate`, not built into hard skill recommendations.
- **WebGPU maturity:** browser support and library stability were improving through 2026 but uneven; "pan a million points" claims are demo-sourced. [Likely, not Confirmed]
- **No primary benchmarking:** point-count ceilings (500k/1M/10M) are source-reported, not independently measured here. Tagged accordingly in reference docs.
- **Fast-decay:** everything in §1–2 is `vintage`-dated; expect a refresh cadence of ~6–12 months.

## CONFIDENCE SUMMARY

The principle layer of the suite is durable and needs no change. The perishable layer (libraries, renderers, WCAG version) is confidently established as stale and confidently updatable from the sources above. Two genuine capability gaps — at-scale/interactive dashboards and data storytelling — justify new leaf skills rather than edits. Product-trend claims are directionally reliable but should inform framing, not hard rules.

## SOURCES

- [Web Data Viz Libraries 2026 — D3/Plot/Visx/Recharts/ECharts/Vega compared (youngju.dev, 2026-05)](https://www.youngju.dev/blog/culture/2026-05-14-data-visualization-libraries-2026-d3-plot-visx-recharts-echarts-vega-comparison-deep-dive-2026.en)
- [Best Apache ECharts Alternative in 2026 (LightningChart)](https://lightningchart.com/blog/best-apache-echarts-alternative-in-2026/)
- [Best D3.js Alternatives 2026 (DataStackHub)](https://www.datastackhub.com/alternatives-to/d3-js-alternatives/)
- [deck.gl](https://deck.gl/)
- [Vega-Lite releases (GitHub)](https://github.com/vega/vega-lite/releases) · [Vega & Vega-Lite (Wikipedia)](https://en.wikipedia.org/wiki/Vega_and_Vega-Lite_visualisation_grammars)
- [Accessible Data-Visualisation Tooling in 2026 (Disability World)](https://www.disabilityworld.org/articles/accessible-data-viz-tooling-2026/)
- [Color Blind Friendly Chart Colors & Palettes 2026 (rgblind)](https://rgblind.com/blog/color-blindness-friendly-chart-colors)
- [Chart Accessibility Guide / WCAG (chartgen.ai)](https://chartgen.ai/resources/blog/chart-accessibility-inclusive-data-visualization)
- [Best JS Scrollytelling Libraries 2026 (cssauthor)](https://cssauthor.com/best-javascript-scroll-animation-scrollytelling-libraries/)
- [Top Data Visualization Trends 2026 (Ajelix)](https://ajelix.com/data/data-visualization-trends/) · [Infogram](https://infogram.com/blog/10-trends-in-data-visualization-to-watch-in-2026/) · [Luzmo](https://www.luzmo.com/blog/data-visualization-trends)
- [Top 12 Python Data Viz Libraries 2026 (KnowledgeHut)](https://www.knowledgehut.com/blog/business-intelligence-and-visualization/python-data-visualization-libraries)

## NEXT STEPS

1. Expand `skills/data-science/visualization/` — add director + `interactive-dashboards` + `data-storytelling` leaves; modernize `chart-selection`.
2. Encode §1–4 as provenance-tagged reference docs (`library-landscape-2026.md`, `accessibility-standards.md`, `rendering-by-volume.md`, `dashboard-frameworks-2026.md`, `narrative-patterns.md`).
3. Fix the orchestrator's "no director yet" gap for visualization; run the registry sync trinity.
4. Schedule a ~6–12 month refresh of the `vintage`-dated figures.

---

*Calibration: log outcomes with `/calibrate SPK-20260723-dataviz-2026 <claim_id> <true|false|partial>`. Feedback: `/feedback spelunker <1-5>`.*
