# Biomarker Enrichment — Quick Reference


## Quick Reference

| Biomarker Type | Definition | Enrichment Role | Example |
|---|---|---|---|
| **Predictive** | Identifies patients likely to respond to a specific treatment | Primary enrichment tool | HER2 for trastuzumab, PD-L1 for pembrolizumab, BRCA for olaparib |
| **Prognostic** | Predicts disease outcome regardless of treatment | Risk stratification, not enrichment | Oncotype DX in breast cancer, IPSS-R in MDS |
| **Pharmacodynamic (PD)** | Measures biological response to treatment | Dose optimization, proof-of-mechanism | Phospho-protein levels, target occupancy |
| **Safety** | Identifies patients at risk for adverse events | Exclusion criteria, monitoring | HLA-B*5701 for abacavir, UGT1A1 for irinotecan |
| **Susceptibility/Risk** | Identifies individuals at risk of developing disease | Prevention trial enrollment | BRCA1/2 for breast cancer prevention |
| **Monitoring** | Tracks disease status during/after treatment | Response assessment, MRD | ctDNA, PSA, CA-125 |

## Enrichment Design Taxonomy

| Strategy | Mechanism | When to Use | Risk |
|---|---|---|---|
| **All-comers with retrospective subgroup** | Enroll broadly, analyze biomarker subgroups post-hoc | Early development, biomarker unvalidated | Underpowered subgroups, multiple comparison penalties |
| **Prospective enrichment** | Screen all, enroll only biomarker-positive | Validated predictive biomarker, pivotal trials | Smaller addressable market, screening costs |
| **Stratified design** | Randomize within biomarker strata, power for interaction test | Uncertain if biomarker is predictive vs prognostic | Requires large N to test interaction; complex |
| **Adaptive enrichment** | Begin all-comers, restrict to biomarker-positive at interim | Biomarker hypothesis strong but unconfirmed | Requires pre-specified adaptation rules; alpha penalty |
| **Biomarker-strategy design** | Randomize to biomarker-guided vs standard care | Testing a diagnostic strategy, not just a drug | Very large N required; rarely used in drug development |

## Quick Reference

| Scenario | Prevalence | R_pos | R_neg | R_all | N (unenriched) | N (enriched) | Savings |
|---|---|---|---|---|---|---|---|
| Strong predictive (HER2-like) | 20% | 45% | 5% | 13% | 1,200 | 180 | 85% |
| Moderate predictive (PD-L1-like) | 50% | 35% | 15% | 25% | 600 | 280 | 53% |
| Weak predictive | 40% | 25% | 15% | 19% | 850 | 520 | 39% |
| Prognostic only | 30% | 20% | 10% | 13% | 1,200 | 1,050 | 12% |

## Quick Reference

| CDx Pathway | Requirements | Timeline | Cost |
|---|---|---|---|
| **PMA (Class III)** | Analytical validation, clinical validation, bridging studies | 12-18 months | $10-30M |
| **510(k) (Class II)** | Substantial equivalence to predicate | 6-12 months | $3-10M |
| **LDT (Lab-Developed Test)** | CLIA lab validation; no FDA clearance needed | 3-6 months | $1-3M |
| **Complementary diagnostic** | Informs treatment but not required | Same as PMA | $10-30M |

## Quick Reference

| Digital Biomarker | Modality | Therapeutic Area | Maturity |
|---|---|---|---|
| **6-minute walk distance (via accelerometer)** | Wearable | Pulmonary, heart failure, neuromuscular | High — FDA-accepted endpoint |
| **Sleep architecture** | Wearable/app | Insomnia, depression, Parkinson's | Moderate — emerging endpoint |
| **Gait speed and variability** | Smartphone sensors | MS, Parkinson's, frailty | Moderate — exploratory endpoint |
| **Voice biomarkers** | App | Depression, Parkinson's, respiratory | Early — research stage |
| **Continuous glucose monitoring** | Wearable (CGM) | Diabetes | High — established in T1D/T2D |
| **Digital cognitive assessment** | App/tablet | Alzheimer's, ADHD | Moderate — Lilly/Cogstate validation |
| **PRO via ePRO apps** | App | All therapeutic areas | High — standard practice |
