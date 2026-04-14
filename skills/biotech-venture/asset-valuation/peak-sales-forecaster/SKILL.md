---
name: peak-sales-forecaster
description: >
  Forecast peak revenue for a therapeutic asset by modeling patient population,
  market penetration curves, pricing, and competitive dynamics over a 10-year
  commercial horizon to produce probability-weighted revenue projections for
  rNPV valuation and investment sizing.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Peak Sales Forecaster — The Revenue Architect

Peak sales is the single most influential variable in biotech valuation. A 2x difference in peak sales estimate produces roughly a 2x difference in rNPV — making it more impactful than PoS adjustments in most cases. Yet most analysts build revenue models with unstated assumptions about market share and penetration speed. This skill makes every assumption explicit and benchmarked against launch analogs.

The fundamental equation is deceptively simple: **Revenue = Patients x Share x Price x Compliance**. The complexity lives in forecasting each variable over time and across geographies.

## How to Run

### Input

| Parameter | Required? | Example |
|---|---|---|
| Treatable patient population | Yes | 19,000 (from patient-population-sizer) |
| Geography | Yes | US, US + EU5, Global |
| Pricing estimate or range | Recommended | $150,000-$200,000/yr (oncology IV) |
| Competitive landscape | Recommended | 3 approved competitors, 2 Phase 3 |
| Expected launch year | Recommended | 2029 |
| Product differentiation | Recommended | Superior efficacy, better safety, oral formulation |
| Line of therapy | Yes | 1L metastatic |
| Modality | Recommended | Monoclonal antibody |

### Steps

#### Step 1 — Establish Patient Volume Trajectory

Import the treatable addressable population from patient-population-sizer. Model patient volume growth over the forecast period:

| Factor | Annual Growth Rate | Driver |
|---|---|---|
| Incidence/prevalence growth | +1-3%/yr | Aging population, improved diagnosis |
| Biomarker testing adoption | +3-8%/yr (if relevant) | NGS penetration, companion diagnostic uptake |
| Line expansion (label broadening) | Step-change | New indications add discrete patient pools |
| Geographic expansion | Step-change | EU, Japan launches typically 1-2yr post-US |

#### Step 2 — Model Market Penetration (S-Curve)

Drug uptake follows a logistic S-curve. Select a launch analog to calibrate the curve shape:

**Penetration curve formula:** `Share(t) = Peak_Share / (1 + e^(-k * (t - t_midpoint)))`

| Launch Profile | Time to Peak Share | Peak Share Range | Analog Examples |
|---|---|---|---|
| **Best-in-class, high unmet need** | 2-3 years | 40-60% | Keytruda 1L NSCLC, Humira RA |
| **Differentiated entrant, competitive market** | 3-5 years | 15-30% | Opdivo 2L melanoma post-Keytruda |
| **Me-too, crowded market** | 4-6 years | 5-15% | Late PD-1 entrants in NSCLC |
| **First-in-class, novel mechanism** | 3-4 years | 30-50% | Ibrutinib in CLL, semaglutide in obesity |
| **Rare disease, limited competition** | 1-2 years | 60-80% | Spinraza in SMA (before gene therapy) |

**Key S-curve parameters:**
- **Slope (k)**: Steeper for breakthrough designations, strong KOL advocacy, simple dosing. Flatter for complex administration, payer pushback, safety monitoring requirements.
- **Midpoint (t_mid)**: Earlier for high unmet need. Later for markets requiring formulary negotiations or real-world evidence.
- **Plateau duration**: Assume 2-4 years at peak before genericization or next-gen competition erodes share.

#### Step 3 — Set Pricing

Price by modality, therapeutic area, and geography using current market benchmarks:

| Category | US Annual Price Range | EU5 Discount | Japan Discount |
|---|---|---|---|
| Oncology (IV, solid tumor) | $150,000-$250,000 | 30-50% | 20-40% |
| Oncology (oral, targeted) | $100,000-$180,000 | 30-50% | 20-40% |
| Rare disease (enzyme replacement) | $200,000-$500,000 | 10-30% | 10-20% |
| Rare disease (gene therapy, one-time) | $1,000,000-$3,500,000 | 20-40% | 20-30% |
| Immunology (biologic, chronic) | $30,000-$80,000 | 40-60% | 30-50% |
| Obesity (GLP-1 RA, chronic) | $12,000-$20,000 | 40-60% | 30-50% |
| Large-population chronic disease | $5,000-$30,000 | 40-60% | 30-50% |

**Pricing adjustments:**
- Net-to-gross: US payers negotiate 30-60% rebates on list price (higher for competitive classes). Use net price for revenue modeling.
- IRA impact: Medicare negotiation under the Inflation Reduction Act begins 9 years post-approval for small molecules, 13 years for biologics. Model 25-60% price reduction when applicable.
- Biosimilar erosion: Assume 40-80% price erosion over 3-5 years post-LOE for biologics.

#### Step 4 — Apply Compliance and Persistence

Not all patients who start therapy remain on treatment for the full year.

| Modality/Setting | Annual Compliance Rate | Key Drivers |
|---|---|---|
| IV infusion (clinic-administered) | 85-95% | Physician-directed, high adherence |
| Oral daily (oncology) | 70-85% | Pill fatigue, side effects |
| Subcutaneous self-injection (weekly) | 75-85% | Injection burden, refrigeration |
| Subcutaneous self-injection (monthly) | 85-90% | Less frequent, better persistence |
| Gene therapy (one-time) | 100% | Single administration |

Formula: `Effective treated patients = Starting patients x Compliance rate`

#### Step 5 — Build 10-Year Revenue Curve

Assemble the annual revenue model:

```
Year [t] Revenue = Population(t) x Share(t) x Net_Price(t) x Compliance
```

Apply these temporal dynamics:
- **Years 1-2**: Launch ramp (S-curve early phase), limited geographic coverage
- **Years 3-5**: Rapid uptake, geographic expansion (EU5 launch Year 2-3, Japan Year 3-4)
- **Years 5-7**: Peak sales plateau; potential label expansions add new patient pools
- **Years 7-10**: Competitive erosion, potential LOE, IRA negotiation impact

#### Step 6 — Benchmark Against Peak Sales Analogs

Cross-check the forecast against real-world peak sales by therapeutic area:

| Category | Peak Sales Range | Benchmark Drug(s) |
|---|---|---|
| Oncology (solid tumor, single indication) | $1-5B | Tagrisso ($5.8B), Imbruvica ($4.5B peak) |
| Oncology (pan-tumor/multi-indication) | $5-25B | Keytruda ($25B), Opdivo ($9B) |
| Rare disease | $500M-$3B | Spinraza ($2B peak), Trikafta ($8.9B — CF is borderline rare) |
| Immunology (biologic) | $3-15B | Humira ($21B peak), Dupixent ($13B+) |
| Obesity / metabolic (GLP-1) | $5-30B+ | Wegovy ($8B+ and growing), Mounjaro ($12B+) |
| Gene therapy (single indication) | $200M-$1B | Zolgensma ($1.4B peak) |

If the forecast significantly exceeds the top analog, scrutinize assumptions. If far below the lowest analog in the category, consider whether the indication is too narrow.

#### Step 7 — Compile Forecast

### Output

```
PEAK SALES FORECAST — [Asset Name]
Indication: [disease, line of therapy]
Geography: [markets]
Launch Year: [year]

REVENUE BUILD:
  Treatable population (Year 1):          [N] patients
  Peak market share:                      [X]%
  Time to peak share:                     [X] years
  US net price (annual):                  $[X]
  Compliance rate:                        [X]%
  
10-YEAR REVENUE CURVE ($M):
  Year 1:   $[X]    (launch)
  Year 2:   $[X]    (ramp)
  Year 3:   $[X]    (US peak + EU launch)
  Year 4:   $[X]
  Year 5:   $[X]    << PEAK SALES YEAR >>
  Year 6:   $[X]    (plateau)
  Year 7:   $[X]    (competitive erosion begins)
  Year 8:   $[X]
  Year 9:   $[X]    (IRA/LOE impact if applicable)
  Year 10:  $[X]

PEAK ANNUAL REVENUE:     $[X]M (Year [N])
CUMULATIVE 10-YR REVENUE: $[X]M

SENSITIVITY:
  Bull case (peak share +10%, price +20%):   $[X]M peak
  Base case:                                  $[X]M peak
  Bear case (peak share -10%, price -20%):   $[X]M peak

LAUNCH ANALOG: [drug name] — [rationale for selection]

KEY ASSUMPTIONS:
  1. [Patient volume assumption]
  2. [Pricing/reimbursement assumption]
  3. [Competitive timing assumption]

KEY RISKS TO FORECAST:
  1. [Competitive threat — specific drug/company]
  2. [Pricing risk — IRA, payer pushback, ICER review]
  3. [Market access risk — formulary restrictions, step edits]
```

### Error Handling

| Scenario | Response |
|---|---|
| No clear launch analog | Use therapeutic-area averages for S-curve parameters; widen confidence range; present multiple penetration scenarios |
| First-in-class with no pricing precedent | Benchmark against nearest therapeutic analog by value delivered; apply ICER threshold analysis ($100-150K/QALY); present price sensitivity table |
| Rapidly evolving competitive landscape | Model multiple competitive scenarios (current, expected, worst-case); assign probabilities to each; present expected-value weighted forecast |
| Indication too new for prevalence data | Use bottom-up clinical trial screening data to estimate eligible population; flag as high-uncertainty input |
| Global forecast requested but limited data outside US | Model US in detail; apply regional multipliers from Step 7 of patient-population-sizer; clearly state which geographies are extrapolated vs. modeled |

## Cross-Domain Connections

- **Biotech-venture/patient-population-sizer**: Provides the patient volume input (Step 1)
- **Biotech-venture/cost-estimator**: Development and launch costs offset against peak revenue in rNPV
- **Biotech-venture/pos-calculator**: Probability weighting applied to this revenue stream in rNPV
- **Biotech-venture/competitive-intelligence**: Competitive entrants directly impact market share assumptions
- **Biotech-venture/deal-economics**: Peak sales drives deal valuation and royalty economics
