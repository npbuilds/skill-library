---
name: portfolio-analyzer
description: >
  Portfolio-level analysis for biotech venture funds including PoS-weighted expected
  portfolio value, portfolio probability of at least one success, therapeutic area
  concentration (Herfindahl index), phase distribution, correlation modeling, portfolio
  optimization, vintage year analysis, and reserve allocation. Activate when evaluating
  how an individual asset fits within a portfolio or assessing overall fund risk and return.
metadata:
  author: nirav
  version: "1.0"
  parent: deal-synthesis
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Portfolio Analyzer — Fund-Level Risk and Return

Individual deal quality is necessary but not sufficient for fund returns. A portfolio of individually strong biotech investments can still produce poor fund-level returns if the assets are correlated (all in the same therapeutic area, same phase, same mechanism class), under-reserved (insufficient capital for follow-on), or poorly timed (vintage concentration). This skill analyzes biotech venture portfolios at the fund level, evaluating concentration, correlation, expected value, and construction.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Portfolio of assets (names, TAs, phases, rNPVs, PoS) | User / rnpv-modeler | Yes |
| Investment amounts per asset | User | Yes |
| Total fund size and deployment pace | User | Recommended |
| New asset under consideration (for fit analysis) | User / diligence-scorecard | Optional |

### Steps

#### Step 1 — Expected Portfolio Value (PoS-Weighted rNPV)

Calculate the probability-weighted expected value of the entire portfolio:

```
PORTFOLIO EXPECTED VALUE

| Asset | TA | Phase | Investment | rNPV | LOA | Expected Value | EV/Investment |
|-------|-----|-------|------------|------|-----|----------------|---------------|
| A     | Onc | Ph 2  | $15M       | $300M| 12% | $36M           | 2.4x          |
| B     | Imm | Ph 1  | $8M        | $500M| 6%  | $30M           | 3.8x          |
| C     | Rare| Ph 3  | $25M       | $200M| 55% | $110M          | 4.4x          |
| D     | CNS | Ph 2  | $12M       | $150M| 10% | $15M           | 1.3x          |
| ...   |     |       |            |      |     |                |               |

Portfolio Totals:
  Total Invested: $[X]M
  Total Expected Value: $[X]M
  Portfolio Expected Multiple: [X]x
  Portfolio IRR (time-weighted): [X]%
```

**Benchmark:** Top-quartile biotech venture funds target 3-4x gross MOIC. Expected portfolio multiple should exceed 3x to account for losses on failed programs.

#### Step 2 — Portfolio Probability of Success

The probability that at least one asset in the portfolio succeeds (reaches approval and generates meaningful return):

```
P(at least one success) = 1 - Π(1 - PoS_i)   [for independent assets]

Example:
  5 assets with LOA of 10%, 8%, 12%, 6%, 15%
  P(all fail) = 0.90 x 0.92 x 0.88 x 0.94 x 0.85 = 0.582
  P(at least one success) = 1 - 0.582 = 41.8%
```

**Fund viability threshold:** P(at least one success) should exceed 70% for a viable biotech fund. Below 50%, the fund has meaningful probability of total loss.

**Important caveat:** This calculation assumes independence. Correlated assets (same TA, same target class) have lower effective portfolio PoS than the independent calculation suggests. See Step 4.

#### Step 3 — Therapeutic Area Concentration (Herfindahl Index)

Measure portfolio concentration using the Herfindahl-Hirschman Index (HHI):

```
HHI = Σ (share_i)^2

Where share_i = investment in TA_i / total portfolio investment

HHI INTERPRETATION:
  <0.15 (1,500):  Diversified — no single TA dominates
  0.15-0.25:      Moderate concentration — acceptable for focused funds
  0.25-0.40:      High concentration — deliberate strategy required
  >0.40:          Very high concentration — single-TA risk

THERAPEUTIC AREA DISTRIBUTION:
| Therapeutic Area | # Assets | Investment | Share | Share^2 |
|------------------|----------|------------|-------|---------|
| Oncology         | 3        | $40M       | 40%   | 0.160   |
| Immunology       | 2        | $25M       | 25%   | 0.063   |
| Rare Disease     | 2        | $20M       | 20%   | 0.040   |
| CNS              | 1        | $15M       | 15%   | 0.023   |

HHI = 0.285 → High concentration (oncology-heavy)
```

Also calculate by modality, mechanism class, and geography for multi-dimensional concentration assessment.

#### Step 4 — Correlation Modeling

Biotech assets are not independent. Correlation reduces effective diversification:

**Sources of correlation:**

| Correlation Type | Description | Impact |
|---|---|---|
| TA correlation | Assets in the same therapeutic area face correlated regulatory and market risks | Moderate (ρ = 0.2-0.4) |
| Mechanism class | Assets targeting the same pathway may face correlated scientific risk | High (ρ = 0.3-0.6) |
| Platform correlation | Assets built on the same platform (mRNA, AAV, etc.) share technology risk | Very high (ρ = 0.4-0.7) |
| Regulatory correlation | FDA policy changes affect multiple assets simultaneously | Low-Moderate (ρ = 0.1-0.3) |
| Payer/commercial | Market access decisions in a TA affect all assets in that TA | Moderate (ρ = 0.2-0.4) |

**Correlation-adjusted portfolio PoS:**

When assets are correlated, the effective portfolio PoS is lower than the independent calculation:

```
P(at least one success, correlated) ≈ 1 - Π(1 - PoS_i) x (1 + correlation_adjustment)

Correlation adjustment:
  For 2 correlated assets: factor = ρ x PoS_1 x PoS_2 / [P(both fail, independent)]
  
Simplified approach for portfolio-level:
  Average pairwise ρ across portfolio
  Effective PoS = Independent PoS x (1 - average_ρ/2)
```

**Portfolio implication:** A portfolio of 5 oncology assets with average pairwise ρ = 0.3 provides the diversification equivalent of ~3.5 independent assets, not 5.

#### Step 5 — Phase Distribution Analysis

Optimal biotech venture portfolios balance risk across development phases:

```
PHASE DISTRIBUTION

| Phase | # Assets | Investment | % of Fund | PoS Range | Expected Data |
|-------|----------|------------|-----------|-----------|---------------|
| Preclinical | [N] | $[X]M | [X]% | 3-5% LOA | [timeline] |
| Phase 1     | [N] | $[X]M | [X]% | 5-10% LOA | [timeline] |
| Phase 2     | [N] | $[X]M | [X]% | 10-25% LOA | [timeline] |
| Phase 3     | [N] | $[X]M | [X]% | 40-65% LOA | [timeline] |

OPTIMAL BENCHMARKS (for balanced biotech fund):
  Preclinical + Phase 1: 20-35% of capital (high risk, high multiple)
  Phase 2: 35-45% of capital (core portfolio)
  Phase 3+: 20-35% of capital (de-risked, lower multiple)
```

**J-curve consideration:** Early-stage heavy portfolios have longer J-curves (3-5 years before first positive cash event). Late-stage heavy portfolios have shorter J-curves but lower return potential. Balance based on fund LP expectations and fund life.

#### Step 6 — Portfolio Optimization

Given a set of available deals and a capital constraint, optimize portfolio construction:

**Objective:** Maximize expected portfolio value subject to:
- Total investment <= fund allocation for new deals
- TA concentration HHI <= target threshold
- Phase distribution within target ranges
- Minimum portfolio PoS threshold met

**Marginal contribution analysis for a new asset:**

```
MARGINAL PORTFOLIO CONTRIBUTION — [New Asset Name]

Standalone Metrics:
  rNPV: $[X]M
  LOA: [X]%
  Expected Value: $[X]M
  EV/Investment: [X]x

Portfolio Impact:
  Portfolio Expected Value: $[X]M → $[X]M  (Δ = +$[X]M)
  Portfolio PoS (≥1 success): [X]% → [X]%  (Δ = +[X]%)
  TA HHI: [X] → [X]  ([improving/worsening] concentration)
  Phase distribution: [impact on phase balance]
  Correlation with existing assets: ρ = [X] ([Low/Moderate/High])

Marginal Verdict: [Adds diversification / Increases concentration / Neutral]
```

#### Step 7 — Vintage Year Analysis

Biotech venture fund returns are vintage-dependent. Assess portfolio timing:

```
VINTAGE DISTRIBUTION

| Vintage Year | # Assets | Investment | Key Catalyst Year |
|--------------|----------|------------|-------------------|
| 2023         | 2        | $20M       | 2025-2026         |
| 2024         | 3        | $35M       | 2026-2027         |
| 2025         | 2        | $25M       | 2027-2028         |

Concentration risk: [X]% of capital deployed in single vintage year
Data readout clustering: [N] assets with data in same 12-month window
```

**Risk:** If multiple assets have data readouts in the same window and the market is risk-off, mark-to-market losses can be severe even for programs that are proceeding well.

#### Step 8 — Reserve Allocation for Follow-On

Biotech venture investing requires capital reserves for follow-on rounds in winning assets:

```
RESERVE ANALYSIS

Total Fund Size: $[X]M
Initial deployment (new deals): $[X]M  ([X]% of fund)
Follow-on reserves: $[X]M  ([X]% of fund)
Management fees + expenses: $[X]M  ([X]% of fund)

Reserve Adequacy:
  Assets expected to need follow-on: [N] (assets advancing past Phase 2)
  Average follow-on per advancing asset: $[X]M
  Total follow-on demand (expected): $[X]M
  Reserve coverage ratio: [X]x  (>1.5x recommended)

RESERVE ALLOCATION POLICY:
  Phase 1 → Phase 2 advance: Reserve $[X]M per asset
  Phase 2 → Phase 3 advance: Reserve $[X]M per asset
  Phase 3 → Commercial: Reserve $[X]M per asset (if pre-revenue company)

Reserve sufficiency: [Adequate / Tight / Insufficient]
```

**Critical rule:** Under-reserved funds are forced to dilute in winning positions (selling winners to other investors at lower returns) or allow pro-rata to lapse. Top-quartile funds reserve 40-60% of capital for follow-on.

### Output

```
PORTFOLIO ANALYSIS — [Fund Name / Portfolio]
Date: [assessment date]

SUMMARY METRICS:
  Total Assets: [N]
  Total Invested: $[X]M
  Portfolio Expected Value: $[X]M
  Expected Multiple: [X]x
  Portfolio PoS (≥1 success): [X]%
  TA HHI: [X] ([diversified/moderate/concentrated])

CONCENTRATION ANALYSIS:
  Top TA: [name] at [X]% of capital
  Top Modality: [name] at [X]% of capital
  Top Mechanism Class: [name] at [X]% of capital

PHASE DISTRIBUTION: [balanced / early-heavy / late-heavy]

CORRELATION ASSESSMENT: Average pairwise ρ = [X]
  Effective independent assets: [X] (vs [N] actual)
  Correlation-adjusted PoS: [X]%

RESERVE STATUS: [Adequate / Tight / Insufficient]
  Reserve coverage ratio: [X]x

NEW ASSET FIT (if evaluating): [Adds value / Neutral / Increases risk]

KEY PORTFOLIO RISKS:
1. [Top risk — e.g., TA concentration]
2. [Second risk — e.g., vintage clustering]
3. [Third risk — e.g., reserve inadequacy]

OPTIMIZATION RECOMMENDATIONS:
1. [Action to improve portfolio — e.g., seek CNS asset for diversification]
2. [Action — e.g., reserve additional capital for Phase 3 advances]
3. [Action — e.g., reduce oncology exposure in next deployment]
```

## Error Handling

| Scenario | Response |
|---|---|
| Fewer than 3 assets in portfolio | Portfolio analysis is limited; note that concentration metrics are less meaningful at small N |
| No correlation data available | Default to TA-based correlation estimates; flag as "estimated correlations" |
| Reserve allocation not specified | Model at 50% reserve ratio as default; sensitivity test at 40% and 60% |
| Mixed fund (biotech + non-biotech) | Analyze biotech sub-portfolio separately; note cross-asset correlations |

## Cross-Domain Connections

- **deal-synthesis/diligence-scorecard**: Individual asset scores are inputs to portfolio-level analysis
- **deal-synthesis/investment-memo-writer**: Portfolio fit is a section in the investment memo
- **asset-valuation/rnpv-modeler**: rNPV per asset feeds expected portfolio value calculation
- **probability-of-success/pos-calculator**: PoS per asset feeds portfolio PoS calculation
- **competitive-intelligence/market-dynamics**: TA market dynamics affect correlation assumptions
