# Regulatory Standards Reference

A mapping of key regulatory documents to their statistical requirements.

## ICH Guidelines

| Document | Title | Statistical Impact |
|----------|-------|-------------------|
| **ICH E9** | Statistical Principles for Clinical Trials (1998) | Foundation: randomization, sample size, analysis sets (ITT, per-protocol), interim analyses, multiplicity |
| **ICH E9(R1)** | Estimands and Sensitivity Analysis (2019) | Requires defining estimands before analysis. Five intercurrent event strategies. Now the global standard. |
| **ICH E6(R3)** | Good Clinical Practice (2023 revision) | Risk-based monitoring, decentralized trial elements, electronic records. Supports digital endpoints. |
| **ICH E17** | Multi-Regional Clinical Trials (2017) | Consistency of treatment effects across regions. Methods for evaluating regional differences. |
| **ICH E20** | Adaptive Clinical Trials (in development) | Will formalize adaptive design requirements beyond current FDA guidance. |
| **ICH M14** | Use of Real-World Data (in development) | Framework for RWD quality and fitness-for-purpose in regulatory decisions. |

## FDA Guidance Documents

| Guidance | Year | Key Statistical Requirements |
|----------|------|------------------------------|
| **Adaptive Designs for Clinical Trials** | 2019 | Pre-specification, simulation-based operating characteristics, type I error control. Covers sample size re-estimation, arm dropping, enrichment. |
| **Multiple Endpoints in Clinical Trials** | 2022 | Multiplicity adjustment required for all primary and key secondary endpoints. Gatekeeping and graphical approaches acceptable. |
| **Bayesian Methodology in Clinical Trials** | 2026 (draft) | Informative priors acceptable with justification. Requires simulation for operating characteristics. Prior sensitivity analysis mandatory. |
| **Real-World Evidence Program** | 2018+ | Framework for using RWE to support regulatory decisions. Requires data quality assessment, study design justification, and sensitivity analyses. |
| **Enrichment Strategies for Clinical Trials** | 2019 | Statistical methods for designing enriched trials (prognostic, predictive, practical enrichment). |
| **Non-Inferiority Clinical Trials** | 2016 | Margin selection, constancy assumption, both ITT and per-protocol required. |
| **Patient-Focused Drug Development (Series)** | 2020-2024 | PRO (patient-reported outcomes) as endpoints: validation, missing data handling, responder definitions. |

## EMA Guidelines

| Guideline | Key Statistical Requirements |
|-----------|------------------------------|
| **Points to Consider on Multiplicity** | Requires strong control of FWER for confirmatory claims. Allows Hochberg, Holm, gatekeeping, graphical. |
| **Guideline on Missing Data** | Sensitivity analyses mandatory. Primary analysis should reflect the estimand. Pattern-mixture and selection models for MNAR. |
| **Guideline on Adjustment for Baseline Covariates** | ANCOVA recommended over change-from-baseline. Stratification factors should match randomization strata. |
| **Qualification of Novel Methodologies** | Pathway for qualifying new statistical methods, biomarkers, or clinical outcomes for regulatory use. |

## Reporting Standards

| Standard | Applies To | Statistical Checklist Items |
|----------|-----------|----------------------------|
| **CONSORT 2025** | Randomized trials | Sample size justification, randomization method, ITT population, multiplicity, interim analyses, statistical methods with enough detail to replicate |
| **STROBE** | Observational studies | Variable handling, confounders, subgroups, sensitivity analyses, missing data approach |
| **PRISMA 2020** | Systematic reviews / meta-analysis | Search strategy, risk of bias assessment, heterogeneity, synthesis methods, certainty of evidence (GRADE) |
| **STARD** | Diagnostic accuracy studies | Index test, reference standard, blinding, cross-tabulation, sensitivity/specificity with CIs |
| **TRIPOD** | Prediction models | Model development/validation, sample size, missing data, discrimination, calibration, internal/external validation |

## Regulatory Acceptance of Software

| Software | FDA Status | Notes |
|----------|-----------|-------|
| **SAS** | Established | Historically the default. Validated by vendor. Still dominant in legacy pharma. |
| **R** | Accepted | Fully accepted with validation. Use `valtools` or `theValidatoR` for package qualification. The R Validation Hub provides a risk assessment framework. |
| **Python** | Increasingly accepted | Less established than R for regulatory. No equivalent of `valtools`. Growing use in exploratory and ML-based analyses. |
| **Julia** | Emerging | Not yet widely used in regulatory submissions. |

## Alpha and Power Conventions by Trial Phase

| Phase | Typical Alpha | Typical Power | Justification |
|-------|--------------|---------------|---------------|
| Phase 1 | 0.05 (two-sided) or descriptive | N/A (often descriptive) | Safety and PK focus |
| Phase 2 | 0.05-0.10 (two-sided) | 80% | Signal detection; higher alpha acceptable for learning |
| Phase 3 (confirmatory) | 0.025 (one-sided) = 0.05 (two-sided) | 80-90% | Regulatory requirement for pivotal efficacy claims |
| Phase 3 (non-inferiority) | 0.025 (one-sided) | 80-90% | Both ITT and per-protocol must show NI |

## Estimands in Practice — Decision Template

For each endpoint in a trial, complete this template:

```
Estimand: [name]
Population:     [who is included]
Treatment:      [what is being compared]
Endpoint:       [what is measured and when]
IC Events:      [list each intercurrent event and its strategy]
  - Discontinuation due to AE:  [treatment policy / composite / ...]
  - Rescue medication use:      [treatment policy / composite / ...]
  - Death before assessment:    [composite / ...]
Summary Measure: [difference in means / hazard ratio / odds ratio / ...]
Primary Analysis: [statistical method]
Sensitivity Analyses: [list methods for each IC event strategy assumption]
```
