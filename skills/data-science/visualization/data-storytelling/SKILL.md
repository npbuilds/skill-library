---
name: data-storytelling
description: >
  Design data narratives — sequence visualizations into a story that holds attention and lands a
  decision. Use when turning a set of charts into an argument, building a scrollytelling piece or
  data-driven report, pacing a guided reveal, choosing annotation-as-message, or adapting a
  narrative across dashboard, presentation, and report contexts.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Data Storytelling — From Charts to Argument

A single chart answers a question. A data story sequences several charts so the reader arrives at a *conclusion* — and remembers it. This skill is the synthesis layer: it assumes each chart is already correct and accessible (`chart-selection`) and, where interactive, well-delivered (`interactive-dashboards`), and asks the next question — **in what order, with what framing, does this data change what the audience believes or does?**

The bridge from `chart-selection` is direct: that skill starts every chart with "what should the audience think after seeing this?" A data story chains those single-chart takeaways into one narrative takeaway.

## The Narrative Spine

Before sequencing any charts, write the story in one sentence — the *spine*. If you cannot state "the data shows X, therefore we should Y" in a sentence, there is no story yet, only a chart collection.

A durable structure for analytical narratives:

1. **Hook / context** — the status quo or the question. Orient the reader in the domain and the stakes.
2. **Complication** — the tension: a surprising number, a gap, a trend that breaks. This is the chart that makes the reader lean in.
3. **Development** — the evidence, in the order that builds the case. Each chart earns the next.
4. **Resolution** — the takeaway and its consequence: the decision, the recommendation, the "so what."

Not every piece needs all four, but every piece needs a spine and an ordered path from tension to resolution. Charts placed in "whatever order I made them" is the most common storytelling failure.

## Annotation-as-Message

In a story, annotation is not decoration — it *is* the narrative layer. An unannotated chart asks the reader to rediscover the point; most will not. For each chart in the sequence:

- State the takeaway *in the chart*, as a title or callout, in plain language ("Revenue fell 12% — driven entirely by the West region"), not a neutral label ("Figure 3: Revenue by region").
- Call out the one element that carries the argument: the inflection point, the outlier, the crossover, the benchmark line.
- Gray out everything the current beat is not about. Highlight-one-mute-the-rest is how you point without a laser pointer.
- Let annotation carry continuity: each chart's callout should hand off to the next chart's question.

## Guided Reveal & Pacing

Stories control *when* the reader sees each thing. Techniques:

- **Staged build.** Show the baseline, then the comparison, then the annotation — not all at once. In a presentation this is animation; in a report it is sequential figures; on the web it is scroll-driven.
- **One message per beat.** A slide, a scroll step, or a paragraph-with-figure carries exactly one point. Two messages in one view means the reader gets neither.
- **Overview → zoom → detail** as a narrative arc, not just a dashboard interaction: open on the aggregate, then walk into the segment that matters.
- **Consistent anchoring.** Keep axes, scales, and color mappings stable across the sequence so change reads as *data* changing, not the chart changing.

## Scrollytelling (the web-native form)

Scroll-driven narrative — a fixed or evolving visual on one side, text that advances it as the reader scrolls — is the dominant 2026 format for data-driven web pieces (the house style of outlets like The Pudding).

- **Tooling:** `Scrollama` (v3.2.0) is the de-facto standard, built on the browser's `IntersectionObserver` API to trigger steps as elements enter the viewport. It is framework-agnostic; historic setups pair it with React, and Svelte support is now strong.
- **Pattern:** a sticky graphic + a column of "steps"; each step, on entering view, updates the graphic's state (filter, highlight, zoom, or swap). The reader drives the pace with the scrollbar.
- **Discipline:** every scroll step is one message (see pacing above). Resist the temptation to change three things per step; the reader loses the thread.
- **Accessibility:** scroll-jacking and motion can exclude readers. Provide a non-scroll linear fallback, respect `prefers-reduced-motion`, and keep the underlying content readable without the interaction.

## Adapting to Context

The same spine is delivered differently by medium (this refines the context guidance in `chart-selection`):

| Context | Optimize for | Story mechanics |
|---|---|---|
| **Dashboard** | Repeated scanning by experts | The "story" is implicit — layout and consistent encoding do the narrating; minimal prose |
| **Presentation** | One message per slide, seconds of attention | Staged animation builds; large type; bold single annotation; the presenter is the narrator |
| **Report / scrollytelling** | A reader following alone, no narrator | Explicit prose carries the spine; annotation and captions must stand without you in the room |

## Common Mistakes

1. **No spine.** A deck of charts in creation order is not a story. Write the one-sentence "X therefore Y" first.
2. **Neutral labels instead of takeaway titles.** "Figure 3" makes the reader do the work; a stated takeaway does it for them.
3. **Burying the complication.** If nothing surprises, nothing holds attention. Lead the reader to the tension early.
4. **More than one message per beat.** Two points per slide/step means zero points land.
5. **Chart-changing instead of data-changing.** Switching chart types or scales mid-sequence hides the very change you're trying to show. Hold the frame stable.
6. **Sacrificing honesty for drama.** A reveal that leans on a truncated axis is a lie with good pacing. Re-stage it honestly (route back to `chart-selection`).

## When This Applies

Use this skill whenever you are:
- Turning an analysis into a report, memo, deck, or web piece meant to persuade or inform
- Sequencing multiple charts into a single argument
- Building a scrollytelling or explanatory data-journalism piece
- Deciding what to annotate and how to pace a reveal
- Adapting one analysis across a dashboard, a presentation, and a written report

For narrative structures, scrollytelling patterns, and annotation templates with provenance, see `references/narrative-patterns.md`.
