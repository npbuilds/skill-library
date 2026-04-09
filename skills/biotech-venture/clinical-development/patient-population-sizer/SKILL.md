---
name: patient-population-sizer
description: >
  Estimate addressable patient populations from epidemiological data, applying
  diagnostic rates, treatment-eligible filters, biomarker prevalence, and
  geographic adjustments to produce treatable population estimates for peak
  sales forecasting and clinical trial feasibility analysis.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Patient Population Sizer — The Epidemiology-to-TAM Funnel

The gap between "50 million Americans have disease X" and "how many patients will take this drug" is where most revenue forecasts go wrong. A headline prevalence number is not a market. This skill builds a rigorous waterfall from total disease burden down to the treatable addressable population for a specific therapeutic asset, with sourced estimates at every step. The output feeds directly into peak-sales-forecaster as the patient volume input.

Every biotech pitch deck inflates patient numbers. This skill deflates them to reality.

## How to Run

### Input

| Parameter | Required? | Example |
|---|---|---|
| Disease/indication | Yes | Non-small cell lung cancer (NSCLC) |
| Geography | Yes | US, EU5, Japan, Global |
| Line of therapy | Recommended | 1L metastatic, 2L+, adjuvant |
| Biomarker requirement | If applicable | PD-L1 TPS >= 50%, EGFR-mutant |
| Modality constraints | If applicable | IV infusion only (limits to infusion centers) |
| Competitive context | Recommended | Current SOC, anticipated entrants |

### Steps

#### Step 1 — Establish Disease Burden (Top of Funnel)

Start with the broadest defensible population estimate. Use the data source hierarchy — always cite the highest-tier source available:

| Tier | Source | Strengths | Limitations |
|---|---|---|---|
| 1 | GBD (Global Burden of Disease) | Standardized global methodology, 204 countries | Modeled estimates, 2-3yr lag |
| 2 | SEER / national cancer registries | Observed incidence, stage-specific | US/country-specific, cancer-only |
| 3 | Claims databases (Truven, Optum, IQVIA) | Real-world treatment patterns | Commercially insured bias, US-centric |
| 4 | Published epidemiological studies | Disease-specific depth | Single population, may be outdated |
| 5 | KOL estimates / company projections | Forward-looking | Unverifiable, potential bias |

**Prevalence vs. incidence.** Use prevalence for chronic diseases where patients accumulate (e.g., rheumatoid arthritis, diabetes). Use incidence for diseases with rapid turnover (e.g., metastatic cancers where median survival < 2 years, acute infections). For oncology, annual incidence is typically the right starting point; for immunology, point prevalence.

#### Step 2 — Apply Diagnostic Rate Filter

Not all patients with a disease are diagnosed. This filter is often the largest single reduction in the funnel.

| Disease Category | Typical Diagnosis Rate | Key Drivers |
|---|---|---|
| Common cancers (breast, lung, colon) | 85-95% | Screening programs, symptomatic presentation |
| Rare cancers | 70-85% | May be misdiagnosed; referral delays |
| Autoimmune diseases | 50-70% | Lengthy diagnostic odyssey, overlapping symptoms |
| Rare genetic diseases | 5-30% | Requires genetic testing, low awareness |
| Neurodegenerative (early-stage) | 30-60% | Gradual onset, normalization of symptoms |

Formula: `Diagnosed population = Disease burden x Diagnosis rate`

#### Step 3 — Apply Treatment-Seeking Filter

Not all diagnosed patients seek or accept treatment.

| Factor | Adjustment | Rationale |
|---|---|---|
| Asymptomatic early-stage disease | -20-40% | Watchful waiting, physician and patient reluctance |
| Stigmatized conditions | -15-30% | Mental health, substance abuse, sexual health |
| Elderly/frail patients | -10-20% | May not be offered aggressive therapy |
| Highly symptomatic, life-threatening | -5% or less | Strong motivation to treat |
| Disease with clear treatment guidelines | -5-10% | Guideline-concordant care drives treatment |

Formula: `Treatment-seeking = Diagnosed x Treatment-seeking rate`

#### Step 4 — Apply Treatment Eligibility Filters

Clinical trial inclusion/exclusion criteria and label restrictions reduce the eligible population.

| Filter | Typical Impact | Examples |
|---|---|---|
| Performance status (ECOG) | -10-20% | ECOG 0-1 required; ECOG 2+ excluded |
| Organ function requirements | -5-15% | Adequate hepatic/renal function |
| Prior therapy requirements | Variable | Must have failed 1L; may exclude pretreated |
| Contraindications | -5-10% | Autoimmune history for IO, cardiac for certain TKIs |
| Age restrictions | -2-5% | Pediatric exclusion, upper age limits |
| Comorbidities | -10-20% | Uncontrolled diabetes, active infections |

Formula: `Eligible = Treatment-seeking x (1 - sum of exclusion rates)`

#### Step 5 — Apply Biomarker Prevalence Filter

If the drug requires biomarker selection, this can dramatically reduce the addressable population.

| Biomarker | Prevalence in Parent Population | Source |
|---|---|---|
| PD-L1 TPS >= 50% (NSCLC) | ~30% | KEYNOTE-024 screening data |
| EGFR mutations (NSCLC) | ~15% (Western), ~40% (Asian) | TCGA, regional registries |
| HER2+ (breast cancer) | ~20% | SEER, clinical databases |
| BRCA1/2 mutations (ovarian) | ~15-20% | Population screening studies |
| MSI-H/dMMR (pan-tumor) | ~4-5% (all solid tumors) | TCGA pan-cancer analysis |
| KRAS G12C (NSCLC) | ~13% | AACR GENIE database |

Formula: `Biomarker-positive = Eligible x Biomarker prevalence`

**Testing rate adjustment.** Not all eligible patients are tested for the biomarker. Apply a testing rate multiplier: NGS adoption ~70-80% in academic centers, ~40-60% in community oncology (US, 2024). Testing rates are rising 5-10% annually in oncology.

Formula: `Tested and positive = Eligible x Testing rate x Biomarker prevalence`

#### Step 6 — Apply Line-of-Therapy Share

If the drug targets a specific treatment line, estimate the share of patients who reach that line.

| Line | Typical Reach (Oncology) | Typical Reach (Immunology) |
|---|---|---|
| 1L (first-line) | 100% (all treated patients) | 80-100% (mild may not be treated) |
| 2L | 40-60% | 50-70% |
| 3L | 20-35% | 30-50% |
| 4L+ | 10-15% | 15-25% |

#### Step 7 — Apply Geographic Weighting

Scale from primary geography to target markets.

| Market | Share of Global Pharma Revenue | Population Multiplier (from US base) |
|---|---|---|
| United States | ~45% of global | 1.0x |
| EU5 (DE, FR, UK, IT, ES) | ~20% of global | 0.8-1.0x (prevalence), 0.4-0.7x (revenue) |
| Japan | ~7% of global | 0.35-0.4x (prevalence), 0.3-0.5x (revenue) |
| China | ~8% of global (growing) | 3.0-4.0x (prevalence), 0.2-0.5x (revenue) |
| Rest of World | ~20% of global | Variable |

#### Step 8 — Compile Population Waterfall

### Output

```
PATIENT POPULATION ESTIMATE — [Indication]
Geography: [market]
Date: [assessment date]

POPULATION WATERFALL:
  Total disease burden (prevalence/incidence):    [N]     Source: [GBD/SEER/etc]
  x Diagnosis rate ([X]%):                        [N]     Source: [citation]
  x Treatment-seeking rate ([X]%):                [N]     Source: [citation]
  x Treatment eligibility ([X]%):                 [N]     Filters: [key exclusions]
  x Biomarker prevalence ([X]%):                  [N]     Biomarker: [name]
  x Biomarker testing rate ([X]%):                [N]     Source: [citation]
  x Line-of-therapy reach ([X]%):                 [N]     Line: [1L/2L/3L+]
  ──────────────────────────────
  TREATABLE ADDRESSABLE POPULATION:               [N]     [geography]

  Global extrapolation (US x [multiplier]):       [N]

CONFIDENCE RANGE:
  Conservative (lower bound estimates):           [N]
  Base case:                                      [N]
  Optimistic (upper bound estimates):             [N]

KEY ASSUMPTIONS:
  1. [Most impactful assumption — which filter matters most]
  2. [Second most impactful]
  3. [Key trend that could change the estimate — e.g., biomarker testing adoption]

WORKED EXAMPLE BENCHMARK:
  [Brief comparison to a marketed drug's actual patient volume in the same indication]
```

**Worked example — Pembrolizumab 1L NSCLC (PD-L1 >= 50%, US):**
- US NSCLC incidence: ~238,000/yr (ACS 2024)
- Metastatic at diagnosis: ~57% = ~136,000
- Diagnosis rate: ~90% = ~122,000
- Treatment-seeking (ECOG 0-1): ~70% = ~85,000
- PD-L1 TPS >= 50%: ~30% = ~25,500
- Testing rate: ~75% = ~19,100
- Treatable addressable population: ~19,000 patients/yr (US)
- Cross-check: Keytruda 1L NSCLC US revenue implies ~18,000-22,000 treated patients at ~$170K/yr — validates the funnel.

### Error Handling

| Scenario | Response |
|---|---|
| No reliable epidemiological data | Use multiple lower-tier sources and triangulate; widen confidence range; flag data quality as key risk |
| Rare disease (<10,000 prevalence) | Use rare disease registries (Orphanet, NORD); note that small populations amplify uncertainty at every funnel step; consider natural history study data |
| New biomarker without prevalence data | Estimate from TCGA/GENIE genomic databases for oncology; for other TAs, use screening study data from clinical trials; flag as major assumption |
| Geographic data mismatch | Clearly state which geography the base data represents; apply epidemiological adjustment factors for target geography; note ethnic/genetic prevalence differences (e.g., EGFR mutation rates 3x higher in Asia) |
| Rapidly evolving diagnostic landscape | Date-stamp all testing rate assumptions; note directional trends; provide sensitivity analysis on testing rate |

## Cross-Domain Connections

- **Biotech-venture/peak-sales-forecaster**: Primary consumer — patient population is the volume input to revenue modeling
- **Biotech-venture/endpoint-selection**: Biomarker prevalence affects trial feasibility and enrichment strategy
- **Biotech-venture/clinical-development**: Trial enrollment feasibility depends on population size at the eligible-patient step
- **Biotech-venture/competitive-intelligence**: Competitive entries affect line-of-therapy share estimates
