---
name: cost-estimator
description: >
  Estimate clinical development costs, regulatory costs, and launch costs for a
  therapeutic program by phase, therapeutic area, and trial complexity using
  industry benchmarks, cost driver analysis, and the Tufts CSDD framework to
  produce phased investment timelines for rNPV modeling.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Cost Estimator — The Development Budget Architect

The second pillar of biotech valuation — after revenue — is cost. An rNPV model requires probability-weighted cash outflows at each development phase, and the range between a lean biotech program and a fully loaded pharma program can be 5-10x. This skill produces defensible cost estimates by phase, grounded in Tufts CSDD benchmarks, CRO pricing data, and therapeutic-area-specific complexity factors.

Getting costs right matters for two reasons: it determines how much capital a company needs to raise (dilution risk) and it sets the denominator for return-on-investment calculations that drive deal economics.

## How to Run

### Input

| Parameter | Required? | Example |
|---|---|---|
| Therapeutic area | Yes | Oncology (NSCLC) |
| Current phase | Yes | Preclinical / Phase 1 / Phase 2 / Phase 3 |
| Modality | Yes | Small molecule, mAb, ADC, cell therapy, gene therapy |
| Trial design parameters | Recommended | Sample size, endpoints, comparator, duration |
| Number of indications planned | Recommended | 1 lead + 2 expansion |
| Geography (trial sites) | Recommended | US + EU, global, US-only |
| Sponsor type | Recommended | Virtual biotech, mid-size, large pharma partner |
| Regulatory strategy | If applicable | Standard, accelerated, breakthrough |

### Steps

#### Step 1 — Establish Phase-by-Phase Cost Benchmarks

Start with industry median costs by phase. These benchmarks derive from Tufts CSDD, DiMasi et al. (Journal of Health Economics, 2016), and updated with 2023-2025 CRO market data:

| Phase | Median Cost | Range | Key Cost Driver |
|---|---|---|---|
| Discovery to IND | $5-15M | $2-30M | Modality complexity, CMC for biologics |
| Phase 1 (FIH) | $15-30M | $5-50M | Dose escalation cohorts, PK/PD monitoring |
| Phase 2 (POC) | $20-80M | $10-150M | Sample size, endpoint complexity, biomarker program |
| Phase 3 (Pivotal) | $100-500M | $50M-$1B+ | Patient number, global sites, comparator costs, duration |
| Regulatory (NDA/BLA) | $5-20M | $3-50M | Filing complexity, advisory committees, REMS |
| Pre-launch / Launch | $50-200M | $20-500M | Field force, MSLs, market access, patient support |

**Tufts CSDD framework context:** DiMasi et al. estimated the fully capitalized cost of developing a new drug at $2.6B (2013 dollars, ~$3.2B in 2025 dollars). This includes failures — the cost of the ~90% of programs that never reach approval amortized across the ~10% that do. For a single program cost estimate, use the direct out-of-pocket costs above, not the fully loaded figure.

#### Step 2 — Apply Therapeutic Area Multipliers

Clinical trial costs vary significantly by therapeutic area due to differences in trial complexity, patient availability, and endpoint requirements:

| Therapeutic Area | Cost Multiplier (vs. median) | Key Drivers |
|---|---|---|
| Oncology (solid tumors) | 1.0-1.5x | Comparator drug costs, imaging endpoints, long follow-up |
| Oncology (hematology) | 0.8-1.2x | Smaller trials, faster endpoints (CR, MRD) |
| Rare disease | 0.5-1.0x | Smaller trials, but higher per-patient cost, global recruitment |
| CNS / Neurodegeneration | 1.5-2.5x | Large trials, 18-24mo endpoints, high screen-fail rates |
| Cardiovascular (outcomes) | 2.0-3.0x | 10,000+ patient MACE trials, 3-5yr follow-up |
| Immunology / Inflammation | 1.0-1.5x | Moderate trial sizes, validated endpoints |
| Infectious disease (vaccines) | 1.5-3.0x | Large efficacy trials, manufacturing at scale |
| Gene therapy / Cell therapy | 0.8-1.5x | Small trials but extremely high manufacturing and per-patient costs |

#### Step 3 — Model Cost Drivers in Detail

For each phase, assess the specific cost drivers:

**Clinical Operations (50-60% of trial cost):**

| Driver | Low Cost | Medium Cost | High Cost |
|---|---|---|---|
| Sample size | <100 patients | 100-500 patients | >500 patients |
| Number of sites | <30 sites | 30-100 sites | >100 sites (global) |
| Trial duration | <12 months | 12-24 months | >24 months |
| Screen failure rate | <20% | 20-40% | >40% (rare disease, CNS) |
| Site cost per patient (US) | $30-50K | $50-80K | $80-150K |
| Site cost per patient (EU) | $20-40K | $40-60K | $60-100K |
| Site cost per patient (ROW) | $10-25K | $25-40K | $40-60K |
| Comparator drug cost | $0 (placebo) | $10-50K/patient | $50-200K/patient (IO) |

**CMC / Manufacturing (10-20% of program cost):**

| Modality | CMC Through Phase 3 | Key Cost Items |
|---|---|---|
| Small molecule | $10-30M | Process chemistry, formulation, scale-up, stability |
| Monoclonal antibody | $30-80M | Cell line development, upstream/downstream process, fill-finish |
| ADC | $50-120M | Antibody + linker-payload, conjugation, specialized fill-finish |
| Cell therapy (autologous) | $40-100M | Apheresis logistics, manufacturing per patient ($50-150K/pt) |
| Gene therapy (AAV) | $50-150M | Vector production at scale, potency assays, analytical methods |

**CRO vs. In-House Execution:**

| Model | Cost Impact | When Appropriate |
|---|---|---|
| Full CRO outsource | +10-20% premium | Virtual biotechs, <50 employees, speed priority |
| Hybrid (FSP model) | Baseline | Mid-size biotechs with some internal capability |
| Full in-house | -10-15% on per-trial basis | Large pharma with infrastructure (but higher fixed costs) |

#### Step 4 — Estimate Regulatory Costs

| Activity | Cost Range | Notes |
|---|---|---|
| IND preparation and filing | $1-3M | Includes CMC module, nonclinical package |
| Pre-NDA meetings (Type A/B/C) | $200-500K per meeting | FDA meeting preparation, briefing documents |
| NDA/BLA preparation | $3-10M | eCTD compilation, medical writing, QC |
| Advisory Committee preparation | $1-3M | If required — panel preparation, rehearsals |
| REMS development (if required) | $2-5M | Risk management program design and implementation |
| Post-marketing commitments | $5-50M | Confirmatory trials, long-term safety studies |
| EU/Japan regulatory submissions | $2-5M per geography | Adapted dossiers, local regulatory teams |

**Regulatory strategy impact on cost:**
- Accelerated Approval: Saves 1-2 years of development time; requires confirmatory trial (add $50-200M post-approval)
- Breakthrough Therapy: Does not reduce trial cost but compresses timelines by 30-40% (reduces time-cost-of-capital)
- Orphan Drug: Smaller trials but still requires adequate safety database; fee waivers save $1-3M

#### Step 5 — Estimate Launch and Commercialization Costs

| Component | Cost Range | Key Variables |
|---|---|---|
| Field force (sales reps) | $20-100M/yr | 50-200 reps at $200-500K fully loaded each |
| Medical affairs (MSLs) | $10-30M/yr | 30-80 MSLs for specialty launch |
| Market access / HEOR | $5-15M | Payer dossier, ICER engagement, outcomes studies |
| Patient support programs | $5-20M/yr | Hub services, copay assistance, adherence programs |
| Marketing / branding | $10-30M | DTC (if applicable), HCP marketing, congress presence |
| Distribution and logistics | $2-10M | Specialty pharmacy network, cold chain (biologics) |

**Launch models by company type:**
- Virtual biotech with partner: $0 (partner bears commercial cost; company receives royalties/milestones)
- Co-commercialization: $50-100M first year; split with partner
- Independent launch (specialty): $100-200M first year
- Independent launch (primary care): $300-500M+ first year (large field force required)

#### Step 6 — Compile Development Cost Timeline

### Output

```
DEVELOPMENT COST ESTIMATE — [Asset Name]
Indication: [disease]
Modality: [type]
Current Phase: [phase]
Date: [assessment date]

PHASE-BY-PHASE COST TIMELINE:

Phase          | Duration  | Cost ($M)        | Cumulative ($M)  | Key Assumptions
──────────────────────────────────────────────────────────────────────────────────
IND-enabling   | 12-18mo   | $[X]-[Y]        | $[X]-[Y]         | [CMC, tox studies]
Phase 1        | 12-18mo   | $[X]-[Y]        | $[X]-[Y]         | [dose escalation design]
Phase 2        | 18-24mo   | $[X]-[Y]        | $[X]-[Y]         | [N patients, endpoints]
Phase 3        | 24-36mo   | $[X]-[Y]        | $[X]-[Y]         | [N patients, sites, geography]
Regulatory     | 12-18mo   | $[X]-[Y]        | $[X]-[Y]         | [filing strategy]
Launch (Yr 1)  | 12mo      | $[X]-[Y]        | $[X]-[Y]         | [field force, market access]
──────────────────────────────────────────────────────────────────────────────────
TOTAL PRE-APPROVAL:         $[X]-[Y]M
TOTAL THROUGH LAUNCH:       $[X]-[Y]M

COGS ESTIMATE (POST-APPROVAL):
  Modality: [type]
  COGS as % of net revenue: [X]-[Y]%
  Gross margin: [X]-[Y]%

COGS BENCHMARKS:
  Small molecule:    10-20% COGS (80-90% gross margin)
  Monoclonal antibody: 15-25% COGS (75-85% gross margin)
  ADC:               20-30% COGS (70-80% gross margin)
  Cell therapy:      30-50% COGS (50-70% gross margin)
  Gene therapy:      15-25% COGS (75-85% gross margin) — high fixed, low variable

CAPITAL REQUIREMENT ANALYSIS:
  Cash needed to next value inflection: $[X]M
  Value inflection: [Phase 2 data / Phase 3 interim / NDA filing]
  Months to inflection: [X]
  Implied monthly burn rate: $[X]M/mo

KEY COST RISKS:
  1. [Enrollment risk — screen failure rate or site activation delays]
  2. [CMC risk — manufacturing scale-up complexity]
  3. [Comparator cost risk — expensive active comparator required]
```

### Error Handling

| Scenario | Response |
|---|---|
| Novel modality with no cost precedent | Use closest modality analog; add 20-50% uncertainty premium for first-generation manufacturing; flag CMC as key risk |
| Adaptive trial design (flexible sample size) | Model minimum and maximum enrollment scenarios; present range reflecting interim analysis outcomes |
| Multi-indication program | Estimate lead indication in detail; apply 40-60% marginal cost for expansion indications (shared CMC, overlapping regulatory); present total program cost |
| Partnership with cost-sharing | Separate partner-funded vs. company-funded costs; model both gross program cost and net cost to company |
| Global trial in emerging markets | Apply geographic cost multipliers from Step 3; note that lower site costs may be offset by monitoring complexity and regulatory requirements |

## Cross-Domain Connections

- **Biotech-venture/peak-sales-forecaster**: Revenue minus costs drives NPV; cost timing affects discount factor weighting
- **Biotech-venture/pos-calculator**: Failed program costs are sunk; PoS determines expected cost per successful drug
- **Biotech-venture/deal-economics**: Development costs inform upfront/milestone structure; cost-sharing in partnerships
- **Biotech-venture/asset-valuation**: Cost timeline is the negative cash flow stream in rNPV models
- **Biotech-venture/manufacturing-ip**: CMC costs and COGS connect to manufacturing strategy and IP protection
