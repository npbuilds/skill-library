# Diligence Scorecard — Quick Reference


## Quick Reference

| Input Source | Pillar(s) Fed |
|---|---|
| pos-calculator | Pillar 1 (Clinical Strength) |
| endpoint-selection | Pillar 1, Pillar 2 |
| trial-design-optimizer | Pillar 1 |
| regulatory-precedent + pathway-analyzer | Pillar 2 (Regulatory Positioning) |
| regulatory-risk-scorer | Pillar 2 |
| clinical-differentiator + pipeline-mapper | Pillar 3 (Competitive Position) |
| market-dynamics | Pillar 3 |
| cmc-risk-assessor + modality-manufacturing | Pillar 4 (Manufacturing Feasibility) |
| patent-analyzer + ip-valuation | Pillar 5 (IP Fortress) |
| rnpv-modeler + peak-sales-forecaster + deal-economics | Pillar 6 (Financial Attractiveness) |
| User assessment / public information | Pillar 7 (Team & Execution) |
| User assessment / public information | Pillar 8 (Computational Infrastructure) |

## Step 5 — Generate Recommendation

| Aggregate | Recommendation | Position Sizing |
|---|---|---|
| 8.0-10.0 | **Strong Buy** | Maximum position (3-5% of fund) |
| 6.5-7.9 | **Buy** | Standard position (1-3% of fund) |
| 5.0-6.4 | **Hold** | Monitor for catalysts; small position if specific thesis |
| 3.5-4.9 | **Cautious** | Below average; avoid unless compelling contrarian thesis |
| 1.0-3.4 | **Avoid** | Fundamental concerns; do not invest |

## Error Handling

| Scenario | Response |
|---|---|
| Missing upstream analysis for a pillar | Score based on available information; flag as "limited data" in output; widen confidence range |
| Private company (limited public data) | Pillars 7-8 may rely on investor deck + news; note data source limitations |
| Pre-clinical company | Pillars 1, 2, 3 scored conservatively; emphasize platform/team over clinical data |
| Multi-asset company | Score lead asset as primary; note pipeline optionality as green flag |
| User disagrees with a pillar score | Pillar weights are configurable; user can adjust weight to 0% to exclude a pillar |
