---
name: chart-selection
description: >
  Data visualization chart selection and design principles. Reference when choosing chart types
  for specific messages, designing accessible visualizations, avoiding misleading patterns,
  or applying direct labeling and annotation strategies. Use when communicating data insights
  visually to any audience.
---

# Chart Selection — The Visual Translator

Every effective visualization begins with a message, not a chart type. The most common failure in data visualization is opening a tool and browsing chart options before articulating what the audience should understand. Define the insight first. The chart is just the delivery mechanism.

This skill provides a structured approach: identify your analytical message, match it to a chart family, then refine using design principles, accessibility requirements, and context constraints.

## The Message-First Framework

Before selecting any chart, answer one question: **"What should the audience think or do after seeing this?"** If you cannot state the takeaway in one sentence, the visualization is not ready to build.

Analytical messages fall into seven categories, each mapping to specific chart families:

| Message Category | Core Question | Primary Chart Families |
|---|---|---|
| **Comparison** | How do values differ across categories? | Bar (horizontal/vertical/grouped/stacked), dot plot, bullet chart, slope chart |
| **Composition** | What are the parts of a whole? | Stacked bar, treemap, waffle chart, pie/donut (limited use) |
| **Distribution** | How are values spread? What is typical? | Histogram, box plot, violin plot, density plot, strip/jitter plot |
| **Relationship** | How do two or more variables relate? | Scatter plot, bubble chart, heatmap, connected scatter |
| **Trend over time** | How have values changed? | Line chart, area chart, sparklines, slope chart |
| **Geographic** | Where are values concentrated? | Choropleth, cartogram, dot density map, hex bin map |
| **Flow / Process** | How do values move between states? | Sankey diagram, alluvial plot, funnel chart, waterfall chart |

Start with the message category. Then consult the decision matrix in `references/chart-decision-matrix.md` to narrow to a specific chart type based on your data shape, number of categories, and audience context.

## Chart Type Decision Matrix

The following table covers the most common selections. For the full matrix with 20+ chart types, constraints, and max category guidance, see the reference document.

| Message Type | Few Categories (<6) | Many Categories (6-20) | Continuous Data | Multiple Series |
|---|---|---|---|---|
| **Comparison** | Vertical bar | Horizontal bar | Dot plot / lollipop | Grouped bar, small multiples |
| **Composition** | Stacked bar, pie | Treemap | Stacked area | Stacked bar (100%) |
| **Distribution** | Histogram, box plot | Violin plot, ridgeline | Density plot | Overlaid histograms (max 3), small multiples |
| **Relationship** | Scatter plot | Heatmap | Scatter + regression | Bubble chart, faceted scatter |
| **Trend** | Line chart | Small multiples, sparklines | Area chart (single series only) | Multi-line (max 5), slope chart |
| **Flow** | Waterfall | Sankey | Funnel | Alluvial |

**Key constraints to remember:**
- Bar charts: horizontal when labels are long or categories exceed 6-7.
- Line charts: only for continuous or ordinal x-axes. Never for categorical data.
- Pie charts: only effective for 2-3 slices where the message is about one dominant share. Beyond 5 categories, switch to a bar chart.
- Scatter plots: require at least 30-50 points to reveal patterns. Below that, a table may communicate better.
- Small multiples: the best option when you are tempted to put more than 5 series on a single line or bar chart.

## Design Principles

**Data-ink ratio.** Every element on the chart should encode data or aid comprehension. Remove gridlines that do not help the reader locate values. Remove borders, backgrounds, and decorative elements. Tufte's principle holds: maximize the share of ink devoted to data.

**Direct labeling over legends.** Place labels directly on or next to the data elements they describe. This eliminates the back-and-forth eye movement between a legend and the chart. Research shows direct labeling reduces interpretation time by roughly 30% compared to color-coded legends. When direct labeling creates clutter, use a legend but keep it positioned inside the plot area near the relevant data.

**Annotation for key insights.** If the chart has a message, annotate it. Call out the specific data point, trend, or comparison that supports the takeaway. Annotations transform a chart from "here is some data" to "here is what matters." Annotate: maximum/minimum values, inflection points, targets or benchmarks, anomalies, and contextual events (policy changes, product launches).

**Progressive disclosure.** For complex data, layer the presentation: overview first (high-level aggregation), then allow zoom (filter or drill-down), then expose detail (individual data points). Dashboards should follow this pattern across linked views.

**Consistent color encoding.** Within a report or dashboard, the same category should always use the same color. If "Region A" is blue on slide 3, it must be blue on slide 7. Inconsistent encoding forces the audience to re-learn mappings and erodes trust.

## Accessibility

Accessible visualizations reach a wider audience and are often better designed for everyone. Follow this checklist:

- [ ] **Never rely on color alone** to convey meaning. Pair color with shape, pattern, label, or position.
- [ ] **Use colorblind-safe palettes.** ColorBrewer2 palettes are tested for deuteranopia, protanopia, and tritanopia. Avoid red-green pairings as the sole differentiator.
- [ ] **Ensure sufficient contrast.** Text and data elements should meet WCAG 2.1 AA contrast ratios (4.5:1 for normal text, 3:1 for large text and graphical elements).
- [ ] **Provide text alternatives.** Every chart should have a descriptive alt-text or caption summarizing the key message and data range. Screen readers cannot interpret a PNG.
- [ ] **Use pattern fills for print.** When a chart may be printed in grayscale, supplement color with hatching, dots, or crosshatch patterns.
- [ ] **Label axes and units explicitly.** Never assume the audience knows the unit. Include currency symbols, percentage signs, and date formats.
- [ ] **Avoid thin lines and small points.** Minimum line weight of 2px and point size of 6px for legibility.
- [ ] **Test at reduced size.** If the chart will appear in a mobile view or as a dashboard tile, verify readability at 50% of the design size.

## Anti-Patterns

These patterns mislead audiences or waste cognitive effort. Avoid them.

**Truncated y-axes.** Starting a bar chart y-axis at a value other than zero exaggerates differences. A bar that appears twice as tall should represent twice the value. Line charts have more flexibility here because they encode change via slope, not area, but always label the axis clearly if it does not start at zero.

**Dual y-axes.** Two y-axes on one chart almost always mislead. The creator chooses the scaling, which controls whether the lines appear to correlate, diverge, or converge. Use two separate charts with aligned x-axes instead, or index both series to a common baseline.

**Pie charts for more than five categories.** Humans are poor at comparing angles and areas. Beyond three slices, a sorted horizontal bar chart communicates the same composition message more accurately and supports precise comparison.

**3D charts.** Three-dimensional perspective distorts values. A 3D bar chart makes bars in the back appear smaller. A 3D pie chart makes the front slice look larger. There is no analytical reason to use 3D for 2D data.

**Chartjunk.** Decorative illustrations, gradient fills, drop shadows, and background images all reduce the data-ink ratio and distract from the message. A plain chart with good typography communicates faster.

**Rainbow color maps.** Rainbow (jet/spectral) color scales are perceptually non-uniform: equal data intervals do not produce equal perceived color differences. Use sequential single-hue or multi-hue palettes (viridis, inferno, plasma) for ordered data.

**Area charts for comparison.** Stacked area charts make it nearly impossible to compare any series except the bottom one, because all other series have a shifting baseline. Use line charts or small multiples for comparison across time.

## Context-Specific Guidance

**Dashboard charts.** Optimize for density and scanning speed. Use sparklines, bullet charts, and small multiples. Minimize decoration. Assume the viewer checks this repeatedly and already knows the domain. Provide clear KPI indicators (up/down arrows, color-coded thresholds) rather than lengthy annotations.

**Presentation charts.** Optimize for one message per slide. Use large fonts (18pt minimum for labels), bold annotation, and ample whitespace. Remove gridlines. Animate builds if the platform supports it: show the baseline, then the comparison, then the annotation. The audience has seconds to absorb each chart.

**Report and paper charts.** Optimize for precision and reproducibility. Include confidence intervals, error bars, and sample sizes. Ensure charts are legible in grayscale. Use figure captions that state the takeaway, not just "Figure 3: Sales data." Follow publication style guides (APA, journal-specific).

**Exploratory charts.** Optimize for speed. Use defaults, skip polish, and iterate rapidly. Histograms, scatter matrices, and box plots are workhorses here. The audience is you. Delete these charts when the analysis is done — they are not meant for communication.

## Common Mistakes

1. **Choosing the chart before the message.** Browsing a chart gallery leads to picking what looks interesting rather than what communicates the insight. Always start with the sentence you want the audience to take away.

2. **Too many series on one chart.** More than five lines or more than seven grouped bars causes visual overload. Use small multiples or highlight the one series that matters and gray out the rest.

3. **Using time on the y-axis.** Time is almost always expected on the x-axis (horizontal). Placing it vertically confuses readers who have a deeply ingrained left-to-right temporal mental model.

4. **Ignoring the zero baseline for bar charts.** Bar charts encode magnitude through length. A non-zero baseline makes differences look larger than they are. Line charts encoding rate of change are less sensitive to this, but bars must start at zero.

5. **Defaulting to a line chart for everything.** Line charts imply continuity between points. Categorical data (departments, product names, regions) should use bar charts. If the x-axis has no inherent order, a line connecting the points is misleading.

6. **Skipping annotations.** An unannotated chart forces the audience to discover the message on their own. Most will not bother. Add a text callout for the single most important finding.

## Implementation Libraries

| Purpose | Python | R | JavaScript |
|---------|--------|---|------------|
| Foundational plotting, full control | `matplotlib` | base `graphics` | `D3.js` |
| Statistical visualization, sensible defaults | `seaborn` | `ggplot2` | `Observable Plot` |
| Interactive charts, dashboards | `plotly` | `plotly` | `Plotly.js` |
| Declarative grammar of graphics | `altair` (Vega-Lite) | `ggplot2` | `Vega-Lite` |
| Interactive web-based visualization | `bokeh` | `shiny` + `plotly` | `D3.js` |
| Quick EDA visualization | `seaborn`, `pandas.plot` | `ggplot2` + `GGally` | — |
| Dashboard frameworks | `streamlit`, `dash` | `shiny` | `React` + `Recharts` |

**Recommended starting stack (Python):** `matplotlib` for full control + `seaborn` for statistical plots + `plotly` for interactivity. Use `altair` if you prefer declarative specification over imperative code.

## When This Applies

Use this skill whenever you are:
- Choosing a chart type for a specific analytical message
- Reviewing a visualization for clarity, accuracy, or accessibility
- Designing a dashboard, report, or presentation with data
- Advising on visualization best practices
- Critiquing or improving an existing chart
- Building exploratory plots during data analysis

For the full decision matrix covering 20+ chart types with detailed constraints, palette recommendations, annotation patterns, and the small multiples decision guide, see `references/chart-decision-matrix.md`.
