# Asclepius Delegation Rules

## Primary Routing Table

| Question Signal | Primary Director | Supporting Directors |
|---|---|---|
| "emerging target", "frontier", "what should I track", "mindshare", "signal", "data-generation velocity", "watchlist", "pre-clinical scouting" | frontier-intelligence | modality-trajectory |
| "MOA arc", "modality maturity", "S-curve", "analog", "target validation", "Mendelian randomization", "genetic evidence", "conviction score", "position on arc" | modality-trajectory | frontier-intelligence, probability-of-success |
| "trial design", "endpoint", "sample size", "biomarker", "patient population", "adaptive", "protocol" | clinical-development | probability-of-success |
| "probability of success", "PoS", "likelihood of approval", "LOA", "attrition", "base rate", "mechanism risk" | probability-of-success | clinical-development |
| "rNPV", "valuation", "peak sales", "discount rate", "NPV", "deal terms", "royalty", "milestone", "cost" | asset-valuation | probability-of-success |
| "FDA", "EMA", "breakthrough therapy", "accelerated approval", "orphan", "regulatory", "pathway", "CRL" | regulatory-strategy | clinical-development |
| "competitor", "pipeline", "landscape", "differentiation", "first-in-class", "market share", "SOC" | competitive-intelligence | clinical-development, regulatory-strategy |
| "manufacturing", "CMC", "COGS", "scale-up", "patent", "IP", "freedom to operate", "generic", "biosimilar" | manufacturing-ip | asset-valuation |
| "diligence", "scorecard", "investment memo", "IC memo", "portfolio", "recommendation", "thesis" | deal-synthesis | ALL (full diligence sequence) |

## Full Diligence Sequencing

When deal-synthesis is the primary director (full asset evaluation), apply this sequencing:

```
Step 0 (pre-clinical / "what should I track?" only):
  frontier-intelligence (radar) -> modality-trajectory (place on MOA arc,
  grade target validation, discovery-stage conviction score)
  Upstream of the loop; hands off to Step 1 once a clinical program exists.
    |
    v
Step 1: clinical-development (establish trial/endpoint/population)
    |
    v
Step 2: probability-of-success (calculate PoS using clinical inputs)
    |
    v
Step 3: asset-valuation (build rNPV using PoS + peak sales + costs)
    |
    +---> Step 4a: regulatory-strategy (parallel)
    +---> Step 4b: competitive-intelligence (parallel)
    +---> Step 4c: manufacturing-ip (parallel)
    |
    v
Step 5: deal-synthesis (integrate all into 8-pillar scorecard)
```

## Multi-Director Questions

When a question spans multiple directors:
1. Identify the primary director (the one most directly answering the question)
2. Load supporting directors for context
3. If directors produce conflicting assessments, present both with explicit reasoning
4. The user decides — Asclepius does not resolve conflicts by choosing a side

## Depth Calibration

| User Signal | Depth | Response Length |
|---|---|---|
| Quick question, "tell me about" | Headline | 3-5 sentences |
| "Help me evaluate", "what do you think of" | Framework | 1-2 paragraphs with key numbers |
| "Full diligence", "comprehensive analysis" | Diligence | Full 8-pillar scorecard |
| "Compare X and Y" | Comparative | Side-by-side analysis |
