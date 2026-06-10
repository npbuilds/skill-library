# Portfolio Analyzer — Quick Reference


## Input

| Parameter | Source | Required? |
|---|---|---|
| Portfolio of assets (names, TAs, phases, rNPVs, PoS) | User / rnpv-modeler | Yes |
| Investment amounts per asset | User | Yes |
| Total fund size and deployment pace | User | Recommended |
| New asset under consideration (for fit analysis) | User / diligence-scorecard | Optional |

## Quick Reference

| Asset | TA | Phase | Investment | rNPV | LOA | Expected Value | EV/Investment |
|-------|-----|-------|------------|------|-----|----------------|---------------|
| A     | Onc | Ph 2  | $15M       | $300M| 12% | $36M           | 2.4x          |
| B     | Imm | Ph 1  | $8M        | $500M| 6%  | $30M           | 3.8x          |
| C     | Rare| Ph 3  | $25M       | $200M| 55% | $110M          | 4.4x          |
| D     | CNS | Ph 2  | $12M       | $150M| 10% | $15M           | 1.3x          |
| ...   |     |       |            |      |     |                |               |

## Quick Reference

| Therapeutic Area | # Assets | Investment | Share | Share^2 |
|------------------|----------|------------|-------|---------|
| Oncology         | 3        | $40M       | 40%   | 0.160   |
| Immunology       | 2        | $25M       | 25%   | 0.063   |
| Rare Disease     | 2        | $20M       | 20%   | 0.040   |
| CNS              | 1        | $15M       | 15%   | 0.023   |

## Quick Reference

| Correlation Type | Description | Impact |
|---|---|---|
| TA correlation | Assets in the same therapeutic area face correlated regulatory and market risks | Moderate (ρ = 0.2-0.4) |
| Mechanism class | Assets targeting the same pathway may face correlated scientific risk | High (ρ = 0.3-0.6) |
| Platform correlation | Assets built on the same platform (mRNA, AAV, etc.) share technology risk | Very high (ρ = 0.4-0.7) |
| Regulatory correlation | FDA policy changes affect multiple assets simultaneously | Low-Moderate (ρ = 0.1-0.3) |
| Payer/commercial | Market access decisions in a TA affect all assets in that TA | Moderate (ρ = 0.2-0.4) |

## Quick Reference

| Phase | # Assets | Investment | % of Fund | PoS Range | Expected Data |
|-------|----------|------------|-----------|-----------|---------------|
| Preclinical | [N] | $[X]M | [X]% | 3-5% LOA | [timeline] |
| Phase 1     | [N] | $[X]M | [X]% | 5-10% LOA | [timeline] |
| Phase 2     | [N] | $[X]M | [X]% | 10-25% LOA | [timeline] |
| Phase 3     | [N] | $[X]M | [X]% | 40-65% LOA | [timeline] |

## Quick Reference

| Vintage Year | # Assets | Investment | Key Catalyst Year |
|--------------|----------|------------|-------------------|
| 2023         | 2        | $20M       | 2025-2026         |
| 2024         | 3        | $35M       | 2026-2027         |
| 2025         | 2        | $25M       | 2027-2028         |

## Error Handling

| Scenario | Response |
|---|---|
| Fewer than 3 assets in portfolio | Portfolio analysis is limited; note that concentration metrics are less meaningful at small N |
| No correlation data available | Default to TA-based correlation estimates; flag as "estimated correlations" |
| Reserve allocation not specified | Model at 50% reserve ratio as default; sensitivity test at 40% and 60% |
| Mixed fund (biotech + non-biotech) | Analyze biotech sub-portfolio separately; note cross-asset correlations |

## Formula / Pseudocode

```
P(at least one success) = 1 - Π(1 - PoS_i)   [for independent assets]

Example:
  5 assets with LOA of 10%, 8%, 12%, 6%, 15%
  P(all fail) = 0.90 x 0.92 x 0.88 x 0.94 x 0.85 = 0.582
  P(at least one success) = 1 - 0.582 = 41.8%
```
