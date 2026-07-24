---
name: rnpv-modeler
description: >
  Build risk-adjusted net present value models for therapeutic assets incorporating
  phase-gated probability, peak sales forecasts, development cost estimates, and
  time-value discounting with optional Monte Carlo simulation and platform optionality
  valuation. Activate when valuing a biotech asset for investment, licensing, or M&A.
metadata:
  author: nirav
  version: "1.0"
  innovation: "End-to-end rNPV with platform optionality and Monte Carlo — no open-source equivalent"
compatibility: Designed for Claude Code
allowed-tools: Read, bash, WebSearch, WebFetch
---

# rNPV Modeler — The Valuation Engine

Risk-adjusted NPV is the gold standard for biotech asset valuation because it isolates development failure as a discrete variable rather than burying it in the discount rate. A standard DCF says "this asset is worth $500M at a 30% discount rate." An rNPV says "this asset has a 15% chance of generating $3.3B in risk-free present value, minus $350M in certain development costs, yielding $150M in expected value." The second statement is auditable. The first is not.

This skill consumes outputs from pos-calculator (probability), peak-sales-forecaster (revenue), and cost-estimator (costs) to produce the complete valuation.

## How to Run

### Input

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

### Steps

#### Step 1 — Construct the Revenue Model

Build a year-by-year revenue projection from launch through loss of exclusivity (LOE):

```
Year 1-3:  Ramp (S-curve, using launch analog)
Year 3-7:  Growth to peak sales
Year 7-10: Peak plateau
Year 10+:  LOE erosion (small molecule: 80% drop Y1, biologic: 30% drop Y1-3)
```

Apply: `Net Revenue = Gross Revenue x (1 - rebates/discounts)`
Typical net-to-gross: 60-75% in US (after Medicaid, 340B, commercial rebates)

#### Step 2 — Construct the Cost Model

```
Pre-approval costs:  Phase-by-phase R&D costs (from cost-estimator)
Post-approval costs: COGS + SG&A + Medical Affairs
  COGS: 10-25% of net sales (modality-dependent)
  SG&A: 25-35% of net sales (Year 1-3), declining to 15-25% at maturity
  Medical Affairs: 5-10% of net sales
```

#### Step 3 — Apply Phase-Gated Probabilities

This is what makes rNPV different from standard NPV. Each cash flow is weighted by the cumulative probability of reaching that point:

```
rNPV = Σ [ (Revenue_t - Cost_t) x PoS_cumulative_t ] / (1 + r)^t
```

Where `PoS_cumulative_t` is the probability that the drug has reached the stage generating that cash flow:

| Cash Flow Period | PoS Weight | Explanation |
|---|---|---|
| Phase 1 costs | 100% | Already committed |
| Phase 2 costs | P(Phase 1 success) | Only incurred if Phase 1 succeeds |
| Phase 3 costs | P(Phase 1) x P(Phase 2) | Only if both prior phases succeed |
| Regulatory costs | P(P1) x P(P2) x P(P3) | Only if Phase 3 succeeds |
| Commercial revenue | P(P1) x P(P2) x P(P3) x P(Approval) = LOA | Only if approved |

**Critical nuance:** Development costs are probability-weighted because they are decision-dependent (you stop spending if the drug fails). Some models treat costs as certain — this overestimates negative cash flows and understates rNPV.

#### Step 4 — Select Discount Rate

| Company Type | WACC Range | When to Use |
|---|---|---|
| Large Pharma (top 20) | 8-10% | Licensing/M&A from pharma buyer's perspective |
| Mid-Cap Biotech ($2-20B) | 10-15% | Standalone biotech valuation |
| Small/Pre-Revenue Biotech | 15-20% | Early-stage startup valuation |
| Pure rNPV (risk-free base) | 3-5% | When PoS already captures all development risk |

**Decision rule:** Use pure rNPV (risk-free rate) when PoS inputs are well-calibrated and program-specific. Use WACC when PoS inputs are generic base rates without program adjustments. The pure approach avoids double-counting risk.

#### Step 5 — Calculate rNPV

```
rNPV = Σ [(Revenue_t x LOA - Cost_t x PoS_t) / (1 + WACC)^t]
```

Express as:
- **Point estimate:** Single rNPV value with stated assumptions
- **Range:** Low / Base / High scenarios varying PoS, peak sales, and discount rate
- **Per-share:** rNPV / fully diluted shares (for public company valuation)

#### Step 6 — Sensitivity Analysis (Tornado Diagram)

Vary each input +/- 20% and measure rNPV impact:

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

The tornado identifies which assumptions matter most — focus diligence effort there.

#### Step 7 — Monte Carlo Simulation (Optional)

For higher-fidelity analysis, run 10,000+ simulations varying:
- Peak sales: lognormal distribution around base case
- PoS: beta distribution bounded by low/high estimates
- Costs: normal distribution with +/- 30% range
- Timeline: uniform distribution +/- 1 year per phase
- Discount rate: triangular distribution around WACC estimate

Output: probability distribution of rNPV showing:
- Probability of positive rNPV (investment attractiveness)
- Median vs. mean rNPV (mean > median indicates positive skew = option value)
- P10/P50/P90 values for range communication

#### Step 8 — Platform Optionality (Innovation)

Traditional rNPV values a single indication. But platform technologies have cross-indication optionality that rNPV misses. Apply real options framework:

**Embedded options in biotech:**
- **Option to expand:** Success in Indication 1 de-risks the platform for Indications 2-5. Value = rNPV of additional indications x probability of platform validation x option discount
- **Option to abandon:** Ability to stop spending if data is negative. Value already captured in phase-gated PoS
- **Option to defer:** Ability to delay investment pending competitive/scientific developments

**Platform premium calculation:**
```
Platform Value = Lead Indication rNPV + Σ [Follow-on Indication rNPV x P(platform works)]
Where P(platform works) = PoS of lead indication (success validates the platform)
```

For mRNA, gene therapy vectors, ADC linkers, or other platform technologies, this premium can be 50-200% of lead indication rNPV.

### Output

```
rNPV VALUATION — [Asset Name]
Indication: [primary indication]
Current Phase: [phase]
Date: [assessment date]

Key Assumptions:
  Peak Sales: $[X]B (Year [Y] post-launch)
  LOA: [X]% (from pos-calculator)
  WACC: [X]%
  Development Timeline: [X] years to approval
  Remaining Dev Costs: $[X]M
  COGS: [X]% of net sales
  Patent Expiry: [Year]

rNPV Summary:
  Base Case: $[X]M
  Low (P25):  $[X]M  [key driver]
  High (P75): $[X]M  [key driver]

  rNPV per Share: $[X] (vs current price: $[X])
  Implied Upside/Downside: [X]%

Value Inflection Analysis:
  Current rNPV (Phase [N]):     $[X]M
  Post-positive data rNPV:      $[X]M  (=[X]x increase)
  Post-approval rNPV:           $[X]M  (=[X]x increase)

Sensitivity: [Top 3 drivers in tornado format]

Platform Optionality (if applicable):
  Lead indication rNPV:          $[X]M
  Follow-on indications (N=[X]): $[X]M (probability-weighted)
  Total platform value:          $[X]M
  Platform premium:              [X]% above lead-only rNPV

Monte Carlo (if run):
  P(rNPV > 0):    [X]%
  Mean rNPV:       $[X]M
  Median rNPV:     $[X]M
  P10 / P50 / P90: $[X]M / $[X]M / $[X]M
```

## Error Handling

| Scenario | Response |
|---|---|
| No peak sales estimate available | Use therapeutic-area benchmarks from `peak-sales-forecaster/references/launch-analog-benchmarks.md` |
| No PoS available | Use base rates from pos-base-rates; flag as "unajusted base rate — high uncertainty" |
| Discount rate uncertainty | Present at 3 rates: 8%, 12%, 15% to bracket range |
| Multiple indications | Calculate rNPV per indication; sum for total pipeline value |
| Pre-Phase 1 (preclinical) | Apply ~5% LOA with extremely wide confidence band; note as highly speculative |

## Cross-Domain Connections

- **Biotech-venture/pos-calculator**: Provides probability inputs (the most impactful variable)
- **Biotech-venture/peak-sales-forecaster**: Provides revenue inputs
- **Biotech-venture/cost-estimator**: Provides cost inputs
- **Biotech-venture/deal-economics**: Uses rNPV to derive deal terms (25-35% rule)
- **Biotech-venture/diligence-scorecard**: rNPV feeds the financial attractiveness pillar
- **Investing/intrinsic-value**: rNPV is the biotech-specific version of DCF valuation
- **Investing/risk-architecture**: Parallel framework — both quantify risk-weighted expected values
