# Trial Design Optimizer — Quick Reference


## Quick Reference

| Attribute | Definition | Design Implication |
|---|---|---|
| **Population** | Who is the target patient? | Inclusion/exclusion criteria, enrichment strategy |
| **Treatment** | What treatment regimen? | Dose, duration, combination rules |
| **Endpoint** | What variable is measured? | Primary endpoint selection (see endpoint-selection skill) |
| **Intercurrent events** | What happens that affects interpretation? | Treatment switching, rescue medication, discontinuation |
| **Population-level summary** | What statistical measure? | Mean difference, hazard ratio, responder rate |

## Adaptive Design Taxonomy

| Design Type | Mechanism | Best For | Regulatory Acceptance |
|---|---|---|---|
| **Group Sequential** | Pre-planned interim analyses with stopping rules | Efficacy/futility early stopping | Well-accepted; FDA Guidance 2019 |
| **Sample Size Re-estimation (SSR)** | Adjust N at interim based on variance | Uncertain effect size | Accepted if blinded; unblinded SSR requires justification |
| **Adaptive Randomization** | Shift allocation toward better-performing arms | Multi-arm dose-finding | Accepted in Phase 2; less common Phase 3 |
| **Adaptive Enrichment** | Restrict enrollment to responsive subgroup at interim | Biomarker-driven oncology | Increasingly accepted; KEYNOTE-042 model |
| **MAMS (Multi-Arm Multi-Stage)** | Multiple experimental arms, dropping losers at interim stages | Platform trials, dose-finding | Strong precedent (RECOVERY, STAMPEDE) |
| **Bayesian Adaptive** | Continuous updating of posterior probability | Rare disease, pediatric, device | FDA receptive; requires strong prior justification |
| **Platform Trial** | Perpetual protocol, arms added/dropped dynamically | Pandemic response, oncology master protocols | RECOVERY trial validated; I-SPY 2 model |

## Basket, Umbrella, and Master Protocols

| Design | Structure | Example | When to Use |
|---|---|---|---|
| **Basket** | One drug, multiple tumor types sharing a biomarker | Larotrectinib (NTRK+ tumors), vemurafenib (BRAF V600E) | Targeted therapy with tumor-agnostic mechanism |
| **Umbrella** | One disease, multiple biomarker-drug pairs | Lung-MAP (NSCLC), ALCHEMIST | When multiple actionable biomarkers exist in one disease |
| **Platform** | Perpetual protocol, any drug can enter/exit | I-SPY 2 (breast cancer), RECOVERY (COVID-19) | When many candidates need testing efficiently |

## SCA Data Quality Requirements

| Criterion | Minimum Standard | Gold Standard |
|---|---|---|
| **Sample size** | 2:1 external:treated ratio | 5:1 or greater |
| **Data recency** | Within 5 years of trial enrollment | Concurrent with trial period |
| **Endpoint capture** | Primary endpoint measurable | Primary + key secondaries |
| **Covariate overlap** | Key prognostic factors available | Full propensity score matching |
| **Data source** | Single registry or EHR system | Multiple linked sources (Flatiron, Tempus, Optum) |

## Cost-Benefit Analysis

| Parameter | Traditional RCT | SCA-Augmented Design |
|---|---|---|
| Control arm enrollment | 100% randomized | 0-50% randomized + external |
| Per-patient cost (control) | $40,000-80,000 | $5,000-15,000 (data licensing) |
| Enrollment timeline | 18-36 months | 12-24 months |
| Total savings potential | Baseline | $50-200M depending on indication |
| Regulatory risk | Low | Moderate (mitigated by pre-submission FDA dialogue) |
