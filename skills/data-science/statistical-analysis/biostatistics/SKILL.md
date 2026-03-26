---
name: biostatistics
description: >
  Biostatistics methods for clinical trials, epidemiology, and life sciences research. Reference
  when designing clinical trials, performing survival analysis, evaluating diagnostic tests,
  computing epidemiological measures, conducting meta-analyses, handling multiplicity in clinical
  endpoints, or navigating FDA/EMA regulatory statistical requirements. Use when the data
  involves patient outcomes, censored time-to-event data, or regulatory submissions.
---

# Biostatistics — The Clinical Lens

Statistical methods shaped by regulatory requirements, censored data, and the clinical consequences of being wrong. Every method choice here must be justifiable in a pre-specified statistical analysis plan, because the wrong decision can delay a treatment that saves lives — or approve one that doesn't.

## The Estimands Framework (ICH E9 R1)

The modern organizing principle for clinical trial statistics. Before choosing any method, define the **estimand** — the precise clinical question your analysis answers.

An estimand has five attributes:

| Attribute | Defines | Example |
|-----------|---------|---------|
| **Population** | Who | Adults with moderate-to-severe plaque psoriasis |
| **Treatment** | What intervention | Drug X 300mg vs placebo |
| **Endpoint** | What outcome | PASI 90 response at Week 16 |
| **Intercurrent events** | What happens post-randomization that complicates interpretation | Treatment discontinuation, rescue medication, death |
| **Summary measure** | How treatment effects are quantified | Difference in proportions, hazard ratio, RMST difference |

**Intercurrent event strategies** — the key innovation:

| Strategy | Handles IC Event By | Use When |
|----------|-------------------|----------|
| **Treatment policy** | Analyze regardless (classic ITT) | The policy question: "what happens if we prescribe this?" |
| **Composite** | Fold IC event into the endpoint | Death before response = non-responder |
| **While-on-treatment** | Only count time on assigned treatment | Interest is in direct pharmacological effect |
| **Hypothetical** | Estimate what would have happened without the IC event | "What if no one discontinued?" |
| **Principal stratum** | Focus on subgroup defined by IC event behavior | Effect in those who would comply regardless of arm |

**Practical impact:** Align the estimand with the clinical question BEFORE designing the trial. The estimand drives the design, data collection, and analysis — not the other way around.

## Survival Analysis (Time-to-Event)

The foundational biostatistics method. Used whenever the outcome is "time until something happens" and some subjects haven't experienced the event yet (censoring).

### Core Methods

**Kaplan-Meier estimator:** Non-parametric survival curve. The default visualization for time-to-event data. Reports median survival and survival probabilities at landmark times.

**Log-rank test:** Compares survival curves between groups. Optimal when hazards are proportional (constant hazard ratio over time). For non-proportional hazards (common in immunotherapy), consider:
- **MaxCombo test:** Combines multiple weighted log-rank tests. Better power when treatment effects are delayed or diminishing.
- **RMST difference:** Restricted mean survival time. Compares average survival within a clinically meaningful time horizon. Increasingly recommended as a primary or co-primary endpoint.

**Cox proportional hazards model:** Semi-parametric regression. Estimates hazard ratios adjusted for covariates.
- **Key assumption:** Proportional hazards — the hazard ratio is constant over time. Test via Schoenfeld residuals, log-log survival plots, or time-covariate interactions.
- **When PH fails:** Use time-varying coefficients, stratified Cox, or switch to RMST/milestone analysis.

**Competing risks:** When subjects can experience one of several mutually exclusive events (e.g., death from disease vs. death from other causes).
- Standard KM **overestimates** cumulative incidence when competing risks exist.
- **Cumulative incidence function (CIF):** Accounts for competing events. Fine-Gray model for regression.
- **Cause-specific hazards:** Alternative approach — model each event type separately.

### Parametric Models

| Distribution | Hazard Shape | Use When |
|-------------|-------------|----------|
| Exponential | Constant | Simple survival, memoryless process |
| Weibull | Monotone increasing/decreasing | Hazard changes steadily over time |
| Log-normal | Non-monotone (hump-shaped) | Initial risk peaks then declines |
| Log-logistic | Non-monotone | Similar to log-normal, heavier tails |

Accelerated failure time (AFT) models are the parametric alternative to Cox PH — they model how covariates accelerate or decelerate time-to-event rather than multiplicatively shifting hazards.

## Clinical Trial Design

### Randomization

| Method | When to Use | Key Property |
|--------|------------|-------------|
| **Simple** | Large trials (n > 200) | Unpredictable but may produce imbalance |
| **Permuted block** | Most trials | Ensures balance within blocks; block size should vary and be concealed |
| **Stratified block** | Important prognostic factors (site, disease severity) | Balance across strata |
| **Covariate-adaptive** (minimization) | Many prognostic factors | Best overall balance; slightly predictable |
| **Response-adaptive** | Ethical pressure to assign more patients to better arm | Complex; can introduce time trends |

### Sample Size Essentials

Every trial requires a justified sample size. Key inputs:

- **Significance level (alpha):** Usually 0.025 one-sided (= 0.05 two-sided) for regulatory trials
- **Power (1 - beta):** Typically 80-90%
- **Clinically meaningful difference:** The minimum effect the trial is designed to detect — not the expected effect, but the smallest worthwhile effect
- **Variance estimate or event rate:** From prior studies, pilot data, or literature

For **survival trials**, additionally specify: accrual rate, accrual period, follow-up period, and expected dropout/crossover rates. The number of events (not patients) drives power.

### Group Sequential Designs

Planned interim analyses that allow early stopping for efficacy or futility while controlling overall type I error.

| Boundary | Philosophy | Alpha Spent Early | Alpha Remaining for Final |
|----------|-----------|-------------------|--------------------------|
| **O'Brien-Fleming** | Conservative early, liberal late | Very little | Most |
| **Pocock** | Equal stopping criteria at each look | Equal portions | Less at final |
| **Lan-DeMets** | Flexible alpha-spending function | Customizable | Depends on function |

**Critical rule:** Each interim look inflates the overall type I error. You cannot simply do repeated significance tests at alpha = 0.05. The spending function controls how much alpha is "spent" at each interim and how much is reserved for the final analysis.

### Adaptive Designs

Pre-specified modifications during the trial based on accumulating data:
- **Sample size re-estimation:** Adjust N based on observed variance or effect size (blinded or unblinded)
- **Arm dropping:** Remove underperforming treatment arms in multi-arm trials
- **Population enrichment:** Narrow the population to a responsive subgroup
- **Seamless Phase 2/3:** Combine learning and confirmatory phases

All adaptations must be pre-specified in the protocol and validated via simulation to demonstrate type I error control.

## Diagnostic Test Evaluation

| Metric | Formula | Depends on Prevalence? | Interpretation |
|--------|---------|----------------------|----------------|
| **Sensitivity** | TP / (TP + FN) | No | Probability of positive test given disease |
| **Specificity** | TN / (TN + FP) | No | Probability of negative test given no disease |
| **PPV** | TP / (TP + FP) | **Yes** | Probability of disease given positive test |
| **NPV** | TN / (TN + FN) | **Yes** | Probability of no disease given negative test |
| **LR+** | Sensitivity / (1 - Specificity) | No | How much a positive test increases disease probability |
| **LR-** | (1 - Sensitivity) / Specificity | No | How much a negative test decreases disease probability |

**Critical insight:** PPV and NPV change dramatically with prevalence. A test with 95% sensitivity and 95% specificity has a PPV of only 16% when prevalence is 1%. Always report prevalence alongside PPV/NPV.

**ROC analysis:** Plot sensitivity vs. (1 - specificity) across all thresholds. AUC summarizes overall discriminative ability. Compare AUCs between tests using DeLong's test.

## Epidemiological Measures

| Measure | Setting | Formula (Conceptual) | Interpretation |
|---------|---------|---------------------|----------------|
| **Relative Risk (RR)** | Cohort studies, RCTs | Incidence_exposed / Incidence_unexposed | How many times more likely in exposed group |
| **Odds Ratio (OR)** | Case-control, logistic regression | (a/b) / (c/d) from 2x2 table | Approximates RR when outcome is rare (<10%) |
| **Absolute Risk Reduction (ARR)** | RCTs | Incidence_control - Incidence_treated | Absolute difference in event rates |
| **Number Needed to Treat (NNT)** | RCTs | 1 / ARR | Patients to treat for one additional benefit |
| **Incidence rate** | Cohort studies | Events / Person-time at risk | Events per unit of person-time |
| **Prevalence** | Cross-sectional | Cases / Population at time point | Proportion with condition |

**NNT is the most clinically interpretable measure.** A drug with RR = 0.70 sounds impressive, but if baseline risk is 1%, NNT = 333. If baseline risk is 30%, NNT = 10. Always report absolute measures alongside relative ones.

## Meta-Analysis

Quantitatively combines results across studies to produce a pooled estimate with greater precision.

**Fixed-effects vs. random-effects:**
- Fixed: assumes all studies estimate the same true effect. Use only when studies are methodologically identical.
- Random: assumes true effects vary across studies. Almost always more appropriate. Produces wider confidence intervals.

**Heterogeneity assessment:**
- **Cochran's Q:** Tests whether variability exceeds sampling error. Low power with few studies.
- **I-squared:** Proportion of variability due to heterogeneity. 25% = low, 50% = moderate, 75% = high.
- **Tau-squared:** The between-study variance itself. More interpretable than I-squared for clinical meaning.

**Publication bias detection:** Funnel plot (visual), Egger's test (regression), trim-and-fill (sensitivity). Absence of asymmetry does not prove absence of bias.

**Network meta-analysis (NMA):** Compares multiple treatments simultaneously using both direct (head-to-head) and indirect (via common comparator) evidence. Requires consistency assumption — direct and indirect evidence agree. Use when no single trial compares all treatments of interest.

## Multiplicity in Clinical Trials

Every additional hypothesis tested inflates the probability of a false positive. Regulatory submissions require pre-specified multiplicity strategies.

| Strategy | How It Works | Use When |
|----------|-------------|----------|
| **Fixed-sequence** | Test H1 → H2 → H3 in order; stop at first failure | Clear scientific ordering of hypotheses |
| **Gatekeeping** | Primary endpoints are "gatekeepers" for secondary | Primary/secondary hierarchy exists |
| **Graphical approach** (Bretz) | Hypotheses as nodes, alpha flows between them on rejection | Complex hypothesis structures |
| **Hochberg step-up** | Less conservative than Bonferroni | Independent or positively correlated endpoints |
| **Holm step-down** | Valid under any correlation structure | Default when no structure is assumed |

**Rule of thumb:** Pre-specify the multiplicity strategy in the protocol. Post-hoc multiplicity adjustments are viewed skeptically by regulators.

## Implementation Libraries

| Task | Python | R |
|------|--------|---|
| Survival analysis (KM, Cox, AFT) | `lifelines`, `scikit-survival` | `survival`, `survminer` |
| Competing risks (Fine-Gray, CIF) | `lifelines`, `scikit-survival` | `cmprsk`, `tidycmprsk` |
| Group sequential and adaptive designs | — (use R via `rpy2`) | `rpact`, `gsDesign` |
| Clinical trial simulation | — | `simtrial`, `rpact` |
| Sample size calculation | `statsmodels.stats.power` | `TrialSize`, `pwr`, `rpact` |
| Mixed effects / longitudinal (LMM, GEE) | `statsmodels` (MixedLM, GEE) | `lme4`, `nlme` |
| Meta-analysis (fixed, random, network) | `pymare`, `PythonMeta` | `metafor`, `meta`, `netmeta` |
| Epidemiological measures and causal methods | `zepid` | `epiR`, `epitools` |
| ROC analysis, diagnostic test evaluation | `sklearn.metrics` | `pROC`, `DTComPair` |
| Bayesian clinical models, prior elicitation | `pymc` + `bambi`, `preliz` | `brms`, `rstanarm` |
| Multiple imputation (clinical-grade) | `sklearn.impute.IterativeImputer` | `mice` |
| CONSORT flow diagram generation | — | `consort` |
| R package validation for regulatory use | — | `valtools` |

**Recommended starting stack (Python):** `lifelines` for survival analysis + `statsmodels` for mixed models/GEE + `zepid` for epidemiological measures + `sklearn.metrics` for diagnostics.

**Recommended starting stack (R):** `survival` + `survminer` for survival + `rpact` for trial design + `metafor` for meta-analysis + `lme4` for mixed models.

**Regulatory note:** R is now fully accepted by FDA for regulatory submissions (with validated packages). Python is gaining acceptance but has fewer validated clinical packages. SAS remains common in legacy pharma workflows.

## Common Mistakes

1. **Not accounting for multiplicity.** Testing five endpoints at alpha = 0.05 gives a ~23% chance of at least one false positive. Regulators will reject uncontrolled multiplicity in pivotal trials.
2. **Using standard logistic regression for time-to-event data.** Ignoring censoring discards information and biases estimates. Use survival methods whenever follow-up varies across subjects.
3. **Reporting hazard ratios when proportional hazards fails.** In immunotherapy trials with delayed treatment effects, the overall HR is misleading. Report RMST or milestone survival rates instead.
4. **Interpreting PPV without prevalence context.** A screening test with 99% sensitivity in a 0.1% prevalence population has a PPV under 10%. Always compute PPV at the relevant prevalence.
5. **Conflating odds ratios with relative risk.** When the outcome is common (>10%), the OR substantially overstates the RR. Use log-binomial or Poisson regression with robust variance for RR estimation.
6. **Performing unplanned interim analyses.** Looking at unblinded data mid-trial without a pre-specified spending function invalidates the type I error control. Every look at the data must be accounted for.

## When This Applies

- Clinical trial design, sample size calculation, or regulatory submission
- Any analysis involving time-to-event data with censoring
- Diagnostic test evaluation or epidemiological study design
- Meta-analysis or systematic review
- Longitudinal clinical data with repeated measures
- Any analysis destined for FDA, EMA, or journal submission with CONSORT/STROBE requirements
- Studies where the estimands framework should guide the analysis plan

See `references/regulatory-standards.md` for a mapping of regulatory documents to statistical requirements, and `references/survival-methods.md` for detailed survival analysis method selection guidance.
