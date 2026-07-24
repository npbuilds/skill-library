# Data Narrative Patterns — Reference

> Provenance tags: `ext-verified` (named external source), `internal-estimate` (our synthesis),
> `vintage:<date>`. Sourced from `research/dataviz-landscape-2026.md` (Brief `SPK-20260723-dataviz-2026`).

## Narrative structures

| Structure | Shape | Use when |
|---|---|---|
| **Hook → Complication → Development → Resolution** | Classic analytical arc | Persuading toward a decision; the default | `internal-estimate` |
| **Martini glass** | Author-driven intro, then reader-driven free exploration | A guided opening that opens into a dashboard | `ext-verified` (Segel & Heer narrative-viz taxonomy), `vintage:2010/still-standard-2026` |
| **Interactive slideshow** | Stepwise, author-paced, with exploration at each step | Presentations, scrollytelling steps | `ext-verified` (Segel & Heer), `vintage:2010` |
| **Drill-down story** | Overview → the reader picks a thread → detail | Self-serve reports where readers have different questions | `internal-estimate` |

The **martini-glass** and **interactive-slideshow** patterns come from the Segel & Heer "Narrative Visualization" taxonomy, still the reference vocabulary in 2026. `ext-verified`, `vintage:2010/reaffirmed`.

## The spine test

Write one sentence: *"The data shows **X**, therefore we should **Y**."* If you can't, there is no story yet — only a chart collection. Everything downstream (order, annotation, pacing) serves this sentence. `internal-estimate`.

## Annotation templates (takeaway-first)

- **Takeaway title:** "Revenue fell 12% — driven entirely by the West region" — not "Figure 3: Revenue by region." `internal-estimate`.
- **Point callout:** arrow + short phrase on the single mark that carries the beat (inflection, outlier, crossover, benchmark). `internal-estimate`.
- **Highlight-one-mute-the-rest:** color/emphasize the series in focus, gray the others. Reduces cognitive load without deleting context. `internal-estimate`.
- **Handoff line:** end each chart's annotation pointing at the next question ("…so where did the West lose it?"). `internal-estimate`.

## Scrollytelling toolchain

- **Scrollama** — de-facto standard, **v3.2.0**, built on the browser `IntersectionObserver` API; framework-agnostic, heavy React history, growing Svelte support. House style of **The Pudding**. `ext-verified` (cssauthor 2026; Pudding), `vintage:2026`.
- **Pattern:** sticky graphic + column of steps; each step entering the viewport updates the graphic (filter / highlight / zoom / swap). Reader paces via scroll. `ext-verified`, `vintage:2026`.
- **One message per step.** The most common scrollytelling failure is changing three things per scroll step. `internal-estimate`.
- **Beyond journalism:** scroll-driven narrative is being studied for dense content like privacy-policy presentation (interleaving full text with animated visuals). `ext-verified` (arXiv 2026), `vintage:2026`, `Likely`.

## Accessibility of narratives

- Provide a **non-scroll linear fallback**; respect **`prefers-reduced-motion`**; keep underlying content readable without the interaction. `ext-verified` (WCAG 2.2 / dataviz-a11y note), `vintage:2026`.
- Motion and scroll-jacking exclude some readers — the story must survive with motion off. `internal-estimate`.

## Context adaptation

| Context | Narrator | Spine carried by |
|---|---|---|
| Dashboard | None (implicit) | Layout + consistent encoding | `internal-estimate` |
| Presentation | The presenter | Staged animation, large type, one message/slide | `internal-estimate` |
| Report / scrollytelling | None (reader alone) | Explicit prose + takeaway annotations that stand without you | `internal-estimate` |

## Refuted lore — `do-not-use`

- "A dashboard of all the relevant charts is a data story." False — without a spine and order it's a collection. `do-not-use`.
- "Drama justifies a truncated axis if it makes the point land." False — re-stage honestly; route back to `chart-selection`. `do-not-use`.
