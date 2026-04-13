---
name: adaptation-observer
description: >
  Watch how the product-in-use differs from the product-as-designed. Where are users doing
  unexpected things? Where is the system developing behaviors beyond its initial seed? Where
  is it degrading? The first step in evolution is observation.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Adaptation Observer — Reading the Living Product

Before amplifying or pruning, observe. What is the product actually doing? How does the product-in-use differ from the product-as-seeded?

The gap between design and reality is not a bug — it's the most important data you have.

## What to Observe

### Behavioral Drift

How has the product's behavior changed from its initial conditions?

- **Positive drift:** The system does things better than designed, or does useful things nobody specified
- **Negative drift:** The system does things worse, or develops unhelpful patterns
- **Neutral drift:** Behavior changed but neither better nor worse — just different

### Usage Patterns

How do actual usage patterns compare to expected ones?

- **Frequency:** More or less than expected?
- **Duration:** Longer or shorter sessions?
- **Depth:** Using surface-level or deep capabilities?
- **Paths:** Following designed flows or creating their own?
- **Abandonment:** Where do users stop? What triggers exit?

### Feedback Loop Health

Are the feedback loops designed by `seed/feedback-architect` working?

- **Active loops:** Signals are being detected, responses are firing, effects are visible
- **Dead loops:** Signals exist but aren't being sensed, or responses aren't firing
- **Runaway loops:** Reinforcing loops without balancing — spiraling toward extremes
- **Stale loops:** Loops that were relevant but the context has changed

### Emergence Events

New behaviors that emerged post-surface:

- Cross-domain capability combinations nobody designed
- User-discovered use cases beyond the original thesis
- System adaptations that improve quality without intervention

## Observation Process

1. **Read the data** — Usage logs, feedback signals, behavioral metrics (engage data-science-orchestrator if quantitative analysis needed)
2. **Compare to seed specification** — What was expected? What's different?
3. **Classify the differences** — Positive/negative/neutral drift per dimension
4. **Identify the signals** — Which differences are actionable?
5. **Route** — Positive patterns → amplifier. Negative patterns → pruning-engine. Surprising patterns → emergence-detector.

## Output

```markdown
# Adaptation Observation: {surface name} — {date}

## Behavioral Drift
Positive: {what's working better than designed}
Negative: {what's working worse}
Neutral: {what changed but isn't clearly better/worse}

## Usage vs. Expectation
{Key divergences between expected and actual usage}

## Feedback Loop Status
Active: {which loops are healthy}
Concerning: {which loops need attention — and why}

## Emergence
{New behaviors observed — cross-reference with emergence-detector}

## Recommendations
Amplify: {what to strengthen}
Prune: {what to cut or simplify}
Investigate: {what to watch more closely}
Leave alone: {what's fine and doesn't need intervention}
```
