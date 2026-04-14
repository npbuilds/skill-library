# rNPV Discount Rate & Worked Example Reference

## Discount Rate Framework (2024-2025 Benchmarks)

### By Company Type (WACC)

| Type | Equity Beta | Cost of Equity | WACC | Source |
|---|---|---|---|---|
| Large Pharma | 0.7-1.0 | 8-10% | 8-10% | 30-50% debt leverage |
| Mid-Cap Biotech | 1.0-1.5 | 10-14% | 10-15% | Minimal debt |
| Small Biotech | 1.5-2.5 | 14-20% | 15-20% | Equity-only |
| Pre-Revenue | N/A | 18-25% | 18-25% | No revenue to anchor |

### 2024-2025 CAPM Parameters

```
Cost of Equity = Risk-Free Rate + Beta x Market Risk Premium
  Risk-Free Rate (10yr UST): ~4.5-5.0%
  Market Risk Premium: ~5.5-6.5%
  Biotech Beta: ~1.2 (sector average)
  → Base Cost of Equity: ~11-13%
```

### Pure rNPV vs WACC-Based Approach

| Approach | Rate | When to Use | Advantage |
|---|---|---|---|
| Pure rNPV | 3-5% (risk-free) | PoS is calibrated and program-specific | Avoids double-counting risk; cleanest methodology |
| WACC-based | 10-15% | PoS uses generic base rates | Compensates for PoS estimation error with higher discount |
| Hybrid | 8-12% | Mix of calibrated and estimated PoS | Middle ground for most analyses |

## Worked Example: Phase 2 Oncology Asset

### Setup
- **Asset:** Novel PD-1/VEGF bispecific antibody for 1L NSCLC
- **Current Phase:** Phase 2 (single-arm, n=120)
- **Phase 2 Data:** ORR 42%, median PFS 8.3 months
- **Biomarker:** PD-L1 CPS >= 1 (enriched)

### Revenue Assumptions
- **Patient population:** 180K new NSCLC/yr US x 60% PD-L1+ x 40% 1L eligible = 43K patients
- **Market share at peak:** 15% (3rd entrant after pembro + nivo combos) = 6,500 patients
- **Pricing:** $180K/yr (in line with IO benchmark)
- **Compliance:** 75% (8-9 months average duration)
- **Peak net revenue:** 6,500 x $180K x 0.75 x 0.65 (net-to-gross) = ~$570M
- **Ramp:** Year 1: 15%, Year 2: 40%, Year 3: 65%, Year 4: 85%, Year 5: 100%

### Cost Assumptions
- **Phase 3:** $250M (global RCT, 800 patients, OS primary)
- **Regulatory:** $10M
- **Launch:** $150M (US commercial build)
- **COGS:** 20% of net sales
- **SG&A:** 30% of net sales (declining to 20%)
- **Timeline:** Phase 3 start Year 0, approval Year 4, launch Year 5

### PoS Assumptions (from pos-calculator)
- Base rate NSCLC Phase 2: 10.6% LOA
- Biomarker enrichment: +20% → 12.7%
- Competitive validation (PD-1 approved): +15% → 14.6%
- Adequate capital ($400M cash): neutral
- **Final LOA:** 14.6%
- Phase-specific: P2→P3: 30%, P3→NDA: 55%, NDA→Appr: 88%

### rNPV Calculation (Pure rNPV, r = 4%)

| Year | Cash Flow | PoS Weight | Weighted CF | PV (4%) |
|---|---|---|---|---|
| 0 | -$50M (P3 startup) | 100% | -$50M | -$50M |
| 1 | -$100M (P3 enrollment) | 100% | -$100M | -$96M |
| 2 | -$100M (P3 follow-up) | 100% | -$100M | -$92M |
| 3 | -$10M (regulatory) | 30% | -$3M | -$2.7M |
| 4 | -$50M (pre-launch) | 16.5% | -$8.3M | -$7.1M |
| 5 | $86M (15% ramp) | 14.6% | $12.5M | $10.3M |
| 6 | $228M (40% ramp) | 14.6% | $33.3M | $26.3M |
| 7 | $371M (65% ramp) | 14.6% | $54.1M | $41.1M |
| 8 | $485M (85% ramp) | 14.6% | $70.8M | $51.7M |
| 9 | $570M (peak) | 14.6% | $83.2M | $58.4M |
| 10-14 | $570M/yr (plateau) | 14.6% | $83.2M/yr | ~$200M total |
| 15+ | LOE erosion | 14.6% | declining | ~$30M total |

**rNPV = ~$170M** (sum of all PV-weighted cash flows)

### Value Inflection Points

| Event | LOA Change | rNPV Change | Multiple |
|---|---|---|---|
| Positive Phase 2 (current) | 14.6% | $170M | — |
| Phase 3 initiated | 14.6% → 16.5% | $195M | 1.15x |
| Positive Phase 3 (OS benefit) | 16.5% → 48.4% | $540M | 3.2x |
| NDA filed | 48.4% → 88% | $850M | 5.0x |
| FDA approval | 88% → 100% | $950M | 5.6x |

The **Phase 3 readout is the largest value inflection** — a 3.2x increase in rNPV from a single data point. This is why biotech VCs disproportionately target Phase 2 assets.

## Net-to-Gross Revenue Adjustment Factors

| Channel | Rebate/Discount | Typical Impact |
|---|---|---|
| Medicaid (mandatory) | 23.1% base + inflation | 3-8% of total sales |
| 340B (covered entities) | ~25-50% off WAC | 5-10% of total sales |
| Commercial (PBM rebates) | 15-40% depending on competition | 10-25% of total sales |
| Medicare Part D | Coverage gap + manufacturer discount | 5-15% of total sales |
| International (ex-US) | 30-60% below US WAC | If ex-US included |
| **Net-to-gross ratio** | | **60-75% for US; 40-55% ex-US** |
