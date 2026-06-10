# Patient Population Sizer — Quick Reference


## Input

| Parameter | Required? | Example |
|---|---|---|
| Disease/indication | Yes | Non-small cell lung cancer (NSCLC) |
| Geography | Yes | US, EU5, Japan, Global |
| Line of therapy | Recommended | 1L metastatic, 2L+, adjuvant |
| Biomarker requirement | If applicable | PD-L1 TPS >= 50%, EGFR-mutant |
| Modality constraints | If applicable | IV infusion only (limits to infusion centers) |
| Competitive context | Recommended | Current SOC, anticipated entrants |

## Quick Reference

| Tier | Source | Strengths | Limitations |
|---|---|---|---|
| 1 | GBD (Global Burden of Disease) | Standardized global methodology, 204 countries | Modeled estimates, 2-3yr lag |
| 2 | SEER / national cancer registries | Observed incidence, stage-specific | US/country-specific, cancer-only |
| 3 | Claims databases (Truven, Optum, IQVIA) | Real-world treatment patterns | Commercially insured bias, US-centric |
| 4 | Published epidemiological studies | Disease-specific depth | Single population, may be outdated |
| 5 | KOL estimates / company projections | Forward-looking | Unverifiable, potential bias |

## Quick Reference

| Disease Category | Typical Diagnosis Rate | Key Drivers |
|---|---|---|
| Common cancers (breast, lung, colon) | 85-95% | Screening programs, symptomatic presentation |
| Rare cancers | 70-85% | May be misdiagnosed; referral delays |
| Autoimmune diseases | 50-70% | Lengthy diagnostic odyssey, overlapping symptoms |
| Rare genetic diseases | 5-30% | Requires genetic testing, low awareness |
| Neurodegenerative (early-stage) | 30-60% | Gradual onset, normalization of symptoms |

## Quick Reference

| Factor | Adjustment | Rationale |
|---|---|---|
| Asymptomatic early-stage disease | -20-40% | Watchful waiting, physician and patient reluctance |
| Stigmatized conditions | -15-30% | Mental health, substance abuse, sexual health |
| Elderly/frail patients | -10-20% | May not be offered aggressive therapy |
| Highly symptomatic, life-threatening | -5% or less | Strong motivation to treat |
| Disease with clear treatment guidelines | -5-10% | Guideline-concordant care drives treatment |

## Quick Reference

| Filter | Typical Impact | Examples |
|---|---|---|
| Performance status (ECOG) | -10-20% | ECOG 0-1 required; ECOG 2+ excluded |
| Organ function requirements | -5-15% | Adequate hepatic/renal function |
| Prior therapy requirements | Variable | Must have failed 1L; may exclude pretreated |
| Contraindications | -5-10% | Autoimmune history for IO, cardiac for certain TKIs |
| Age restrictions | -2-5% | Pediatric exclusion, upper age limits |
| Comorbidities | -10-20% | Uncontrolled diabetes, active infections |

## Quick Reference

| Biomarker | Prevalence in Parent Population | Source |
|---|---|---|
| PD-L1 TPS >= 50% (NSCLC) | ~30% | KEYNOTE-024 screening data |
| EGFR mutations (NSCLC) | ~15% (Western), ~40% (Asian) | TCGA, regional registries |
| HER2+ (breast cancer) | ~20% | SEER, clinical databases |
| BRCA1/2 mutations (ovarian) | ~15-20% | Population screening studies |
| MSI-H/dMMR (pan-tumor) | ~4-5% (all solid tumors) | TCGA pan-cancer analysis |
| KRAS G12C (NSCLC) | ~13% | AACR GENIE database |

## Quick Reference

| Line | Typical Reach (Oncology) | Typical Reach (Immunology) |
|---|---|---|
| 1L (first-line) | 100% (all treated patients) | 80-100% (mild may not be treated) |
| 2L | 40-60% | 50-70% |
| 3L | 20-35% | 30-50% |
| 4L+ | 10-15% | 15-25% |

## Quick Reference

| Market | Share of Global Pharma Revenue | Population Multiplier (from US base) |
|---|---|---|
| United States | ~45% of global | 1.0x |
| EU5 (DE, FR, UK, IT, ES) | ~20% of global | 0.8-1.0x (prevalence), 0.4-0.7x (revenue) |
| Japan | ~7% of global | 0.35-0.4x (prevalence), 0.3-0.5x (revenue) |
| China | ~8% of global (growing) | 3.0-4.0x (prevalence), 0.2-0.5x (revenue) |
| Rest of World | ~20% of global | Variable |
