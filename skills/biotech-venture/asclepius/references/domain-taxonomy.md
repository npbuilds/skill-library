# Asclepius Domain Taxonomy

## Skill Tree

```
asclepius (orchestrator) — God of Medicine
|
+-- frontier-intelligence (director) — Frontier Discovery: radar [upstream of diligence]
|   +-- signal-scanner (action) — Second-derivative signal detection across sources
|   +-- mindshare-tracker (action) — Weighted attention/mindshare scoring
|   +-- data-generation-monitor (action) — Data-engine velocity monitoring
|   +-- emerging-target-radar (action) — Target×modality watchlist integration
|
+-- modality-trajectory (director) — Frontier Discovery: trajectory [upstream of diligence]
|   +-- modality-lifecycle (knowledge) — Modality maturity S-curve placement
|   +-- moa-analog-engine (action) — Historical MOA-arc analog matching
|   +-- target-validation-ladder (action) — Genetic/biological validation grading
|   +-- frontier-conviction-scorer (action) — Discovery-stage conviction score
|
+-- clinical-development (director)
|   +-- endpoint-selection (knowledge) — FDA/EMA endpoint acceptance by TA
|   +-- trial-design-optimizer (action) — Protocol design with adaptive/synthetic controls
|   +-- biomarker-enrichment (action) — Enrichment strategy with power/cost tradeoffs
|   +-- patient-population-sizer (action) — Epidemiology-to-TAM funnel
|
+-- probability-of-success (director)
|   +-- pos-base-rates (knowledge) — Phase transition tables by TA/modality
|   +-- pos-calculator (action) — Cumulative PoS with adjustment audit trail
|   +-- mechanism-risk-adjuster (action) — Target validation + reflexivity + MR evidence
|
+-- asset-valuation (director)
|   +-- rnpv-modeler (action) — rNPV with Monte Carlo + platform optionality
|   +-- peak-sales-forecaster (action) — Revenue curves with competitive dynamics
|   +-- cost-estimator (action) — Development cost by phase/TA/complexity
|   +-- deal-economics (knowledge) — Licensing terms, M&A premiums, royalty benchmarks
|
+-- regulatory-strategy (director)
|   +-- regulatory-precedent (knowledge) — Approval case law by TA/endpoint/pathway
|   +-- pathway-analyzer (action) — Optimal FDA/EMA pathway recommendation
|   +-- regulatory-risk-scorer (action) — 6-dimension regulatory risk rating
|
+-- competitive-intelligence (director)
|   +-- pipeline-mapper (action) — Competitive landscape matrix with timelines
|   +-- clinical-differentiator (action) — Cross-trial comparison + contrarian analysis
|   +-- market-dynamics (knowledge) — Launch sequencing, class saturation, game theory
|
+-- manufacturing-ip (director)
|   +-- modality-manufacturing (knowledge) — CMC profiles by modality
|   +-- cmc-risk-assessor (action) — FMEA risk matrix + COGS trajectory
|   +-- patent-analyzer (action) — Patent cliff, FTO, generic entry risk
|   +-- ip-valuation (knowledge) — IP contribution to enterprise value
|
+-- deal-synthesis (director)
    +-- diligence-scorecard (action) — 8-pillar scoring framework
    +-- investment-memo-writer (action) — IC memo generation
    +-- portfolio-analyzer (action) — Fund-level portfolio optimization
```

## Skill Type Distribution

| Type | Count | Percentage |
|---|---|---|
| Orchestrator | 1 | 2% |
| Director | 9 | 21% |
| Knowledge | 8 | 19% |
| Action | 24 | 57% |
| **Total** | **42** | 100% |

> Registry note: `data/registry.json` types every non-director/orchestrator skill flatly as `knowledge` (32 knowledge / 9 director / 1 orchestrator). The Knowledge-vs-Action split above is a finer *descriptive* classification used in this taxonomy only.

## Innovation Features (Unique to Asclepius)

1. **Biotech Reflexivity** — PoS is path-dependent on capital and sentiment (mechanism-risk-adjuster)
2. **Mendelian Randomization** — Genetic target validation using MR evidence (mechanism-risk-adjuster)
3. **Platform Optionality** — Real options valuation for multi-indication platforms (rnpv-modeler)
4. **Synthetic Control Arms** — RWD-based external controls recommendation (trial-design-optimizer)
5. **8th Pillar: Computational Infrastructure** — AI/ML capability assessment (diligence-scorecard)
6. **Game-Theoretic Dynamics** — Competitive modeling using mechanism-design (market-dynamics)
7. **Second-Level Clinical Thinking** — Contrarian analysis of consensus data (clinical-differentiator)
8. **Digital Biomarkers** — Wearable/sensor endpoint feasibility (biomarker-enrichment)
9. **Historical MOA Trajectory** — Placing a target×modality on the target-ID → tool → first-in-human → first-approval → class-explosion arc (moa-analog-engine)
10. **Genetics-Calibrated Target Validation** — MR/allelic-series evidence ladder with ~2.6× success-rate calibration (target-validation-ladder)
