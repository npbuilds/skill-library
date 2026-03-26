# Chart Decision Matrix — Complete Reference

## Full Chart Type Matrix

The following table covers 24 chart types with detailed selection criteria. Use the message type and data characteristics to identify candidates, then check the constraints and limits columns to confirm suitability.

### Comparison Charts

| Chart Type | Message | When to Use | When to Avoid | Max Categories | Max Series | Data Requirements |
|---|---|---|---|---|---|---|
| **Vertical bar** | Compare values across categories | Few categories (3-7), short labels, single or few series | >8 categories, long labels, continuous x-axis | 8 | 3 grouped | Categorical x, numeric y |
| **Horizontal bar** | Compare values, rank items | Long category labels, many categories, showing rankings | Time series, few items where vertical works | 20-25 | 2 grouped | Categorical y, numeric x |
| **Grouped bar** | Compare values across categories AND series | 2-3 series, <7 categories, direct comparison needed | >3 series, >7 categories (use small multiples) | 7 | 3 | Categorical x, numeric y, grouping variable |
| **Stacked bar** | Compare totals AND show composition | Part-to-whole within comparisons, <5 segments | Comparing individual segments (except bottom), >6 segments | 12 | 5 segments | Categorical x, numeric y per segment |
| **100% stacked bar** | Compare proportional composition | Share/percentage comparison across categories, totals differ | Absolute value comparison needed | 12 | 5 segments | Categorical x, percentage y per segment |
| **Dot plot / lollipop** | Compare values with precision | Many categories, values are close together, sparse data | Audiences unfamiliar with the form | 30+ | 2 (paired) | Categorical axis, numeric axis |
| **Bullet chart** | Compare actual vs target | KPIs, dashboards, progress tracking | General audience unfamiliar with form | 1 per chart (stack vertically) | 1 + target + ranges | Actual value, target, qualitative ranges |
| **Slope chart** | Compare change between two time points | Before/after, two-period comparison, highlighting crossovers | >2 time periods, >10 items (overlap) | 10-12 | N/A | Two paired values per item |

### Trend Charts

| Chart Type | Message | When to Use | When to Avoid | Max Series | Data Requirements |
|---|---|---|---|---|---|
| **Line chart** | Show change over continuous interval | Time series, ordered data, detecting trends/cycles | Categorical x-axis, >5 overlapping series | 5 (highlight 1-2) | Ordered/time x, numeric y |
| **Area chart (single)** | Show magnitude over time | Emphasizing volume/cumulative quantity, single series | Multiple series (stacked area misleads), comparison | 1 | Time x, numeric y |
| **Stacked area** | Show composition change over time | Part-to-whole over time, few segments, total matters | Comparing individual series (shifting baselines), >4 series | 4 segments | Time x, numeric y per segment |
| **Sparkline** | Show trend inline with text or table | Dashboards, tables, dense layouts, context is known | Standalone use, precision needed, annotation required | 1 | Time x, numeric y (minimal points: 10+) |
| **Small multiples (line)** | Compare trends across many categories | >5 series, same scale meaningful, pattern comparison | Few series (single chart suffices), different y-scales needed | 1 per panel, 20+ panels | Time x, numeric y, faceting variable |

### Distribution Charts

| Chart Type | Message | When to Use | When to Avoid | Max Groups | Data Requirements |
|---|---|---|---|---|---|
| **Histogram** | Show frequency distribution shape | Single variable distribution, identifying skew/modes | Comparing >3 distributions (overlap), categorical data | 3 overlaid (with transparency) | Numeric variable, n > 30 |
| **Box plot** | Show distribution summary (median, quartiles, outliers) | Comparing distributions across categories, compact summary | Audience unfamiliar with form, multimodal data (hides modes) | 15-20 | Numeric variable, optional grouping |
| **Violin plot** | Show full distribution shape with density | Multimodal distributions, comparing shape across groups | General audience (unfamiliar form), <20 data points per group | 10-12 | Numeric variable, grouping variable, n > 20 per group |
| **Strip / jitter plot** | Show individual data points in distribution | Small datasets (n < 100), exact values matter, overlaid on box | Large n (overplotting), need summary statistics only | 8-10 | Numeric variable, optional grouping |
| **Ridgeline (joy plot)** | Compare many distribution shapes | Many groups (10-20), time-based distributions, visual impact | Precise comparison, values at tails matter | 20 | Numeric variable, ordered grouping variable |

### Relationship Charts

| Chart Type | Message | When to Use | When to Avoid | Data Requirements |
|---|---|---|---|---|
| **Scatter plot** | Show relationship between two variables | Correlation, clusters, outliers, n > 30 | Categorical data, <10 points (use table), severe overplotting | Two numeric variables, n > 30 |
| **Bubble chart** | Show relationship with a third variable (size) | Three numeric dimensions, <50 bubbles, size differences large | Many bubbles (overplotting), small size differences, precision | Three numeric variables, n < 50 |
| **Heatmap** | Show patterns in matrix data | Two categorical axes with numeric values, correlation matrices | Few cells (<9), precise value comparison needed | Two categorical variables, numeric fill |
| **Connected scatter** | Show how two variables co-evolve over time | Cyclical patterns, phase relationships, time as implicit third variable | Audience expects time on x-axis, >1 series | Two numeric variables + time ordering |

### Composition and Flow Charts

| Chart Type | Message | When to Use | When to Avoid | Max Segments | Data Requirements |
|---|---|---|---|---|---|
| **Pie / donut** | Show dominant share of whole | 2-3 slices, one slice is the story, informal context | >5 slices, precise comparison needed, scientific context | 3-5 (ideally 2-3) | Categories summing to 100% |
| **Treemap** | Show hierarchical composition | Nested part-to-whole, many categories, space-efficient | Precise comparison, no hierarchy, few items | 30+ (with hierarchy) | Hierarchical categories, numeric size |
| **Waffle chart** | Show percentage as discrete units | Single percentage or simple comparison, engagement context | Many categories, precise fractional values | 2-3 | Percentage values |
| **Sankey diagram** | Show flow between stages | Multi-step processes, resource/money/user flow, showing transfers | >5 stages, >15 flows (spaghetti), precise values | 5 stages, 15 flows | Source, target, flow magnitude |
| **Waterfall chart** | Show cumulative effect of positive/negative changes | Financial bridges (revenue to profit), sequential additions/subtractions | Non-sequential data, >12 steps | 12 steps | Sequential additive values |
| **Funnel chart** | Show progressive reduction through stages | Conversion funnels, pipeline stages, sequential filtering | Non-sequential stages, values that increase | 6-8 stages | Sequential decreasing values |

---

## Palette Recommendations by Use Case

### Sequential Palettes (ordered data, low to high)

Use for: heatmaps, choropleths, any single-variable intensity encoding.

| Palette Family | Best For | Avoid When |
|---|---|---|
| **Single-hue progression** (e.g., light blue to dark blue) | Clean, professional look, single variable | Need to distinguish many discrete levels |
| **Multi-hue sequential** (e.g., viridis, inferno, plasma) | Perceptual uniformity, wide value ranges, colorblind safe | Print in grayscale (some multi-hue palettes lose distinction) |
| **Viridis** | Default recommendation — perceptually uniform, colorblind safe, prints in grayscale | Aesthetic mismatch with brand palette |
| **Gray sequential** | Secondary emphasis, background context layers | Primary data encoding (too subtle) |

Guidance: Always ensure the lightest and darkest values in the palette are distinguishable in grayscale. Test by converting the chart to grayscale and confirming the ordering is still apparent.

### Diverging Palettes (data with a meaningful midpoint)

Use for: values above/below a target, positive/negative change, deviation from average.

| Palette Family | Best For | Avoid When |
|---|---|---|
| **Blue-Red diverging** | Temperature, profit/loss, above/below average | Colorblind audience without additional encoding |
| **Blue-Orange diverging** | Colorblind-safe alternative to blue-red | Cultural contexts where orange has specific meaning |
| **Purple-Green diverging** | Colorblind-safe, neutral associations | Audiences associate green with "good" (creates unintended bias) |
| **Brown-Teal diverging** | Nature/environment contexts, colorblind-safe | Need high visual contrast at extremes |

Guidance: The midpoint color should be neutral (white, light gray). Both ends should be equally saturated so neither pole appears dominant. Ensure the midpoint value is meaningful (zero, average, target), not arbitrary.

### Categorical Palettes (unordered groups)

Use for: distinguishing discrete categories with no inherent order.

| Palette | Max Distinct Categories | Notes |
|---|---|---|
| **ColorBrewer Set2** | 8 | Muted, colorblind-safe, professional |
| **ColorBrewer Dark2** | 8 | Higher contrast, good for thin lines and small points |
| **Tableau 10** | 10 | Widely recognized, good separation |
| **Custom brand palette** | Varies | Use when organizational identity matters, test for accessibility |

Guidance: Limit distinct categorical colors to 7 or fewer. Beyond that, the audience cannot reliably map colors to categories without constant legend reference. Use direct labeling instead, or switch to small multiples.

### Highlight Palettes (draw attention to one element)

Use for: emphasizing a single series, category, or data point against a muted background.

| Strategy | Implementation |
|---|---|
| **Single highlight** | One saturated color (blue, orange, red) for the focal element. All others in light gray (e.g., #CCCCCC). |
| **Two-tone highlight** | Focal element in saturated color, secondary comparison in medium gray, all others in light gray. |
| **Sequential highlight** | Focal category in darkest shade of a sequential palette, related categories in progressively lighter shades. |
| **Alert highlight** | Red for critical/negative, amber for warning, green for positive — but always pair with icon or label for accessibility. |

Guidance: Highlighting works best when the chart has one clear message. If multiple elements need emphasis, consider separate charts. A chart where everything is highlighted communicates nothing.

---

## Annotation Pattern Library

Annotations transform charts from data displays into insight delivery tools. Every chart with a communication purpose should have at least one annotation.

### What to Annotate

| Annotation Target | When to Use | Example Text Pattern |
|---|---|---|
| **Maximum / Minimum** | The peak or trough is the message | "Peak: 1,247 units in March" |
| **Inflection point** | A change in direction matters | "Growth reversed in Q3 after pricing change" |
| **Target / Benchmark** | Performance against a goal | Horizontal reference line + "Target: 500" |
| **Anomaly / Outlier** | An unusual value needs explanation | "Server outage on June 12 caused 4-hour data gap" |
| **Context event** | An external event explains a pattern | Vertical reference line + "New regulation effective Jan 1" |
| **Period comparison** | Two specific time points are compared | Bracket or arrow connecting two points + "42% increase" |
| **Cumulative milestone** | A running total crosses a threshold | "Reached 1M users on Sept 15" |
| **Confidence / Uncertainty** | Range around estimate matters | Shaded band + "95% confidence interval" |

### How to Style Annotations

**Text callouts:**
- Use a concise sentence fragment, not a paragraph.
- Font size: slightly smaller than axis labels but larger than tick labels.
- Color: match the data element being annotated, or use dark gray for neutral callouts.
- Position: place near the data point, connected with a thin leader line if needed. Avoid overlapping other data.

**Reference lines:**
- Horizontal: for targets, averages, thresholds. Use dashed style to distinguish from data lines. Label on the right end.
- Vertical: for events, time markers. Use dashed or dotted. Label at the top.
- Color: gray or muted tone unless the reference itself is the message (e.g., a red danger threshold).

**Shaded regions:**
- Use for confidence intervals, goal ranges, or highlighting a specific time period.
- Opacity: 10-20% of the fill color so underlying data remains visible.
- Border: none or very thin, same color at higher opacity.

**Arrows and brackets:**
- Use sparingly — one per chart maximum.
- Arrows: from annotation text to the data point. Thin, with a small arrowhead.
- Brackets: to span a range (e.g., "This period" bracketing three months). Keep thin.

### Annotation Placement Priority

When multiple annotations compete for space:
1. The primary message annotation always gets placement priority.
2. Reference lines and shaded regions go behind data.
3. Secondary annotations can be placed in margins or as footnotes.
4. If annotations cause clutter, remove lower-priority ones. A cluttered annotated chart is worse than a clean unannotated one.

---

## Small Multiples vs. Faceting Decision Guide

Small multiples and faceting both show data split across panels. The decision depends on what the audience needs to compare.

### Definitions

- **Small multiples:** Identical chart structure repeated for each category, with consistent axes. The eye compares patterns across panels.
- **Faceting:** A broader term that includes small multiples but also covers cases where panels have different axis ranges or even different chart types for different data subsets.

### When to Use Small Multiples

| Scenario | Why Small Multiples Win |
|---|---|
| Comparing trend shapes across 6-20 categories | Avoids spaghetti lines on a single chart |
| Each category has similar data range | Shared axes make cross-panel comparison valid |
| The audience needs to find their own category | Scanning a grid is faster than decoding a legend with 15 colors |
| Showing geographic patterns across regions | Each panel is a region; the spatial layout can mirror geography |
| Distribution comparison across many groups | Side-by-side histograms or density plots per group |

### When to Use a Single Chart Instead

| Scenario | Why a Single Chart Wins |
|---|---|
| Fewer than 5 series | Direct overlay with color is faster to read than scanning panels |
| Cross-series interaction is the message | Crossovers, convergence, and divergence are visible only when lines share a panel |
| Precise value comparison between series at a given x | Overlaid series allow vertical comparison at a point |
| Space is severely constrained | A single chart with highlighting uses less space |

### When to Allow Free (Non-Shared) Axes

Shared axes are the default for small multiples because they enable fair visual comparison. However, free axes are appropriate when:

- The absolute scale differs drastically between panels (e.g., GDP of the US vs. Luxembourg) and the message is about pattern shape, not magnitude.
- Each panel represents a fundamentally different metric (rare — consider whether these belong in the same figure at all).
- The audience explicitly needs to see detail within each panel that would be crushed by a shared scale.

When using free axes, always add a clear visual indicator (e.g., different axis label colors, a note) so the audience does not mistakenly compare heights across panels.

### Layout Guidelines for Small Multiples

| Parameter | Recommendation |
|---|---|
| **Grid arrangement** | Prefer rows for time series (left-to-right reading), columns for ranking |
| **Panel count** | 4-25 is the sweet spot. Below 4, use a single chart. Above 25, consider aggregation or interactive filtering |
| **Panel size** | Each panel must be large enough to read the pattern — minimum 150x100px on screen |
| **Ordering** | Order panels by a meaningful variable: alphabetical for lookup, by a summary statistic (mean, max) for ranking, by geography for spatial |
| **Shared elements** | Show axis labels and titles on outer edges only. Repeat tick marks on every panel for reference. Use a single shared legend at the top or bottom |
| **Highlight** | Consider highlighting one panel (the focal category) with a colored background or thicker lines, while keeping all other panels in gray as context |
