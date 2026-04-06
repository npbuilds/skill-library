# Chart Selection — Quick Reference


## Quick Reference

| Message Category | Core Question | Primary Chart Families |
|---|---|---|
| **Comparison** | How do values differ across categories? | Bar (horizontal/vertical/grouped/stacked), dot plot, bullet chart, slope chart |
| **Composition** | What are the parts of a whole? | Stacked bar, treemap, waffle chart, pie/donut (limited use) |
| **Distribution** | How are values spread? What is typical? | Histogram, box plot, violin plot, density plot, strip/jitter plot |
| **Relationship** | How do two or more variables relate? | Scatter plot, bubble chart, heatmap, connected scatter |
| **Trend over time** | How have values changed? | Line chart, area chart, sparklines, slope chart |
| **Geographic** | Where are values concentrated? | Choropleth, cartogram, dot density map, hex bin map |
| **Flow / Process** | How do values move between states? | Sankey diagram, alluvial plot, funnel chart, waterfall chart |

## Quick Reference

| Message Type | Few Categories (<6) | Many Categories (6-20) | Continuous Data | Multiple Series |
|---|---|---|---|---|
| **Comparison** | Vertical bar | Horizontal bar | Dot plot / lollipop | Grouped bar, small multiples |
| **Composition** | Stacked bar, pie | Treemap | Stacked area | Stacked bar (100%) |
| **Distribution** | Histogram, box plot | Violin plot, ridgeline | Density plot | Overlaid histograms (max 3), small multiples |
| **Relationship** | Scatter plot | Heatmap | Scatter + regression | Bubble chart, faceted scatter |
| **Trend** | Line chart | Small multiples, sparklines | Area chart (single series only) | Multi-line (max 5), slope chart |
| **Flow** | Waterfall | Sankey | Funnel | Alluvial |

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
