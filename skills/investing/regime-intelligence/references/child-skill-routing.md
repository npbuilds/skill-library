# Regime Intelligence — Child Skill Routing

## When to Delegate

| Question Type | Route To | Why |
|---------------|----------|-----|
| "Where are we in the business cycle?" | `macro-cycles` | Full cycle phase analysis, leading vs lagging indicators |
| "What is the Fed doing / what will it do?" | `monetary-regime` | Rate path, QE/QT, financial conditions index |
| "What is fiscal policy doing?" | `fiscal-regime` | Deficit trajectory, spending mix, automatic stabilizers |
| "What regime are we in right now?" | This skill directly | Synthesizes all three child skills into a regime label |

## Child Skill Summaries

### macro-cycles
The business cycle engine. Covers: expansion/peak/contraction/trough identification, PMI interpretation, credit cycle, yield curve, leading/lagging/coincident indicators, recession probability models. Use when the question is about *timing* within a cycle.

### monetary-regime
Central bank policy and its transmission. Covers: Fed reaction function, rate path modeling, QE/QT mechanics, financial conditions indices, global central bank divergence, currency policy spillovers. Use when the question involves *interest rates* or *liquidity conditions*.

### fiscal-regime
Government spending and taxation. Covers: deficit/surplus trajectories, fiscal multipliers, automatic stabilizers, spending composition (investment vs transfer), debt sustainability, MMT vs austerian debate. Use when the question involves *government deficits*, *spending programs*, or *tax policy*.

## Synthesis Rule

The regime label requires all three:
```
Regime = f(macro-cycles, monetary-regime, fiscal-regime)
         ↓
         Growth trajectory (macro-cycles + fiscal-regime)
         × Inflation trajectory (monetary-regime + fiscal-regime)
         = One of four quadrants
```

A monetary tightening cycle that outpaces fiscal expansion = deflationary signal.
A fiscal expansion that outpaces monetary tightening = inflationary signal.
