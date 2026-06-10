# Rnpv Modeler — Quick Reference


## Input

| Parameter | Source | Required? |
|---|---|---|
| Cumulative PoS by phase | pos-calculator | Yes |
| Peak sales estimate + revenue curve | peak-sales-forecaster | Yes |
| Development costs by phase | cost-estimator | Yes |
| Discount rate (WACC) | User or benchmarks below | Yes |
| Development timeline (years per phase) | User or benchmarks | Yes |
| COGS as % of net sales | cost-estimator or modality default | Yes |
| Patent/exclusivity expiration | patent-analyzer or estimate | Recommended |
| Number of indications (platform) | User | Optional (for optionality) |

## Quick Reference

| Cash Flow Period | PoS Weight | Explanation |
|---|---|---|
| Phase 1 costs | 100% | Already committed |
| Phase 2 costs | P(Phase 1 success) | Only incurred if Phase 1 succeeds |
| Phase 3 costs | P(Phase 1) x P(Phase 2) | Only if both prior phases succeed |
| Regulatory costs | P(P1) x P(P2) x P(P3) | Only if Phase 3 succeeds |
| Commercial revenue | P(P1) x P(P2) x P(P3) x P(Approval) = LOA | Only if approved |

## Step 4 — Select Discount Rate

| Company Type | WACC Range | When to Use |
|---|---|---|
| Large Pharma (top 20) | 8-10% | Licensing/M&A from pharma buyer's perspective |
| Mid-Cap Biotech ($2-20B) | 10-15% | Standalone biotech valuation |
| Small/Pre-Revenue Biotech | 15-20% | Early-stage startup valuation |
| Pure rNPV (risk-free base) | 3-5% | When PoS already captures all development risk |

## Error Handling

| Scenario | Response |
|---|---|
| No peak sales estimate available | Use therapeutic area benchmarks from peak-sales-forecaster reference tables |
| No PoS available | Use base rates from pos-base-rates; flag as "unajusted base rate — high uncertainty" |
| Discount rate uncertainty | Present at 3 rates: 8%, 12%, 15% to bracket range |
| Multiple indications | Calculate rNPV per indication; sum for total pipeline value |
| Pre-Phase 1 (preclinical) | Apply ~5% LOA with extremely wide confidence band; note as highly speculative |

## Formula / Pseudocode

```
Year 1-3:  Ramp (S-curve, using launch analog)
Year 3-7:  Growth to peak sales
Year 7-10: Peak plateau
Year 10+:  LOE erosion (small molecule: 80% drop Y1, biologic: 30% drop Y1-3)
```

## Step 2 — Construct the Cost Model

```
Pre-approval costs:  Phase-by-phase R&D costs (from cost-estimator)
Post-approval costs: COGS + SG&A + Medical Affairs
  COGS: 10-25% of net sales (modality-dependent)
  SG&A: 25-35% of net sales (Year 1-3), declining to 15-25% at maturity
  Medical Affairs: 5-10% of net sales
```

## Formula / Pseudocode

```
SENSITIVITY ANALYSIS — [Asset Name]

                          rNPV Impact (Low → High)
Peak Sales        ████████████████████████ ($-80M → $+80M)
Phase 2 PoS       ██████████████████ ($-60M → $+60M)
Discount Rate      ████████████████ ($-50M → $+50M)
Phase 3 Cost        ██████████ ($-30M → $+30M)
Launch Year          ████████ ($-25M → $+25M)
COGS %                ██████ ($-20M → $+20M)
```

## Formula / Pseudocode

```
Platform Value = Lead Indication rNPV + Σ [Follow-on Indication rNPV x P(platform works)]
Where P(platform works) = PoS of lead indication (success validates the platform)
```
