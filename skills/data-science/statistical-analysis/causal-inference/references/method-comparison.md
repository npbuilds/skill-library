# Causal Method Comparison & Selection Guide

## Method Selection Decision Tree

Use this text-based decision tree to identify candidate methods for your causal question. Start at the top and follow the branches.

```
Was treatment randomly assigned?
├── YES → Randomized Experiment (RCT)
│   ├── Full compliance? → Standard ATE estimation
│   └── Non-compliance? → ITT + IV (assignment as instrument) → LATE
│
└── NO → Observational data. Continue below.
    │
    ├── Is there a sharp cutoff rule for treatment assignment?
    │   ├── YES, deterministic → Sharp RDD
    │   └── YES, probabilistic (jump in probability) → Fuzzy RDD (IV at cutoff)
    │
    ├── Is there a discrete policy change over time with a comparison group?
    │   ├── YES, single treatment date → Difference-in-Differences
    │   ├── YES, staggered rollout → DiD with heterogeneity-robust estimator
    │   │   (Callaway-Sant'Anna, Sun-Abraham, or imputation)
    │   └── YES, but only 1 treated unit → Synthetic Control Method
    │
    ├── Is there a plausible instrument (exogenous source of variation)?
    │   ├── YES, strong first stage (F > 10) → IV / 2SLS
    │   └── YES, weak first stage (F < 10) → LIML or Anderson-Rubin; reconsider instrument
    │
    └── Only cross-sectional observational data with measured confounders?
        ├── Strong overlap and many covariates → Inverse Probability Weighting or Doubly Robust
        ├── Moderate covariates, want interpretability → Propensity Score Matching or CEM
        └── Simple setting, few confounders → Regression adjustment with robustness checks
```

**Important:** Multiple methods may apply. When they do, use them as robustness checks against each other. Agreement across methods with different assumptions strengthens causal claims.

## Full Method Comparison Table

| Method | Data Requirements | Key Assumption | Validates Via | Typical Setting | Effect Estimated | Sample Size Needs |
|--------|------------------|---------------|--------------|----------------|-----------------|-------------------|
| **RCT** | Random assignment; outcome measured for both arms | SUTVA; no attrition bias | Randomization check (covariate balance); attrition analysis | Clinical trials, A/B tests, field experiments | ATE | Determined by power analysis; typically hundreds to thousands per arm |
| **Difference-in-Differences** | Panel or repeated cross-section; treated and control groups observed pre- and post-treatment | Parallel trends in absence of treatment | Pre-trend plots; event study with leads/lags; placebo treatment dates | Policy evaluations; staggered program rollouts | ATT | Moderate; needs sufficient pre-periods (3+ recommended) and units in each group |
| **Sharp RDD** | Running variable with a deterministic cutoff; outcome observed both sides | Continuity of potential outcomes at cutoff; no manipulation of running variable | McCrary density test; covariate smoothness; bandwidth sensitivity; placebo cutoffs | Test score thresholds; eligibility cutoffs; election margins | Local ATE at cutoff | Large N near cutoff; effective sample much smaller than total N |
| **Fuzzy RDD** | Running variable with cutoff where treatment probability jumps but is not deterministic | Same as sharp RDD + monotonicity (no defiers at cutoff) | First-stage jump significance; McCrary test; covariate smoothness | Eligibility thresholds with imperfect compliance | Local LATE at cutoff | Larger than sharp RDD due to fuzzy first stage |
| **IV / 2SLS** | Instrument Z correlated with treatment X; outcome Y | Relevance (Z→X); exclusion (Z→Y only through X); monotonicity | First-stage F-statistic (F > 10); overidentification test if multiple instruments; theoretical argument for exclusion | Distance as instrument; lottery assignment; Bartik/shift-share | LATE (for compliers) | Moderate to large; weak instruments require larger N |
| **Propensity Score Matching** | Cross-sectional or panel; treatment and outcome; rich set of pre-treatment covariates | Selection on observables (no unmeasured confounders); common support (overlap) | Balance diagnostics (SMD < 0.1); overlap plots; sensitivity analysis (Rosenbaum bounds) | Program evaluation when randomization impossible; retrospective studies | ATT (most common) | Moderate; needs substantial overlap region; loses unmatched units |
| **Inverse Probability Weighting** | Same as PSM | Selection on observables; positivity (0 < P(treatment) < 1 for all X) | Weight distribution (check for extreme weights); balance after weighting; trimming sensitivity | Same as PSM but retains full sample | ATE or ATT (depending on weights) | Moderate; sensitive to extreme propensity scores |
| **Doubly Robust** | Same as PSM/IPW | Selection on observables; either outcome model or propensity model is correctly specified | Balance diagnostics; model specification tests; compare to PSM and IPW estimates | Preferred when unsure about functional form | ATE or ATT | Moderate to large |
| **Synthetic Control** | Panel data; small number of treated units; substantial pre-treatment period; donor pool of untreated units | Weighted combination of donors can reproduce treated unit's pre-treatment trajectory; no spillovers to donors | Pre-treatment fit (MSPE); in-space placebo (permutation); in-time placebo; leave-one-out donor sensitivity | State/country-level policy evaluation; single-unit case studies | ATT for treated unit(s) | Few treated units (often 1); 20+ donor units; long pre-period |
| **Regression Adjustment** | Cross-sectional or panel; measured confounders | Correct functional form; selection on observables; no unmeasured confounders | Coefficient stability across specifications; sensitivity analysis (Cinelli-Hazlett); added variable plots | Simple observational comparisons; supplementary to other methods | ATE (conditional on model) | Depends on model complexity; standard regression requirements |

## Assumption Validation Checklists

### RCT

- [ ] Randomization produced balanced groups (test covariate balance across arms)
- [ ] SUTVA holds: no interference between units; single version of treatment
- [ ] Attrition is low and balanced across arms (< 5% differential attrition)
- [ ] ITT analysis is pre-specified as primary; per-protocol is secondary
- [ ] No post-randomization selection (do not drop non-compliers from analysis)
- [ ] Pre-registration documents match reported analysis

### Difference-in-Differences

- [ ] Pre-treatment trends are parallel (visual inspection of raw trends)
- [ ] Event study coefficients are near zero for all pre-treatment periods
- [ ] No differential shocks coinciding with treatment timing
- [ ] Composition of groups is stable over time (no selective migration)
- [ ] No anticipation effects visible in periods just before treatment
- [ ] If staggered adoption: heterogeneity-robust estimator used (not standard TWFE)
- [ ] Standard errors clustered at the appropriate level (unit of treatment assignment)
- [ ] Sufficient number of clusters for reliable inference (rule of thumb: 30+; otherwise wild bootstrap)

### Sharp RDD

- [ ] Running variable is continuous (or discrete with many values)
- [ ] McCrary density test: no evidence of sorting/manipulation at cutoff
- [ ] Pre-determined covariates are smooth through the cutoff (no jumps)
- [ ] Results are robust to bandwidth choice (half, double, MSE-optimal)
- [ ] Local linear regression used (not high-order global polynomials)
- [ ] Placebo cutoffs: no effect at false threshold values
- [ ] Donut hole test: results hold when excluding observations nearest to cutoff
- [ ] Treatment effect is estimated with appropriate standard errors (Calonico-Cattaneo-Titiunik robust SEs)

### Fuzzy RDD

- [ ] All sharp RDD checks above
- [ ] First stage: statistically significant jump in treatment probability at cutoff
- [ ] Monotonicity: crossing the cutoff does not cause anyone to move away from treatment
- [ ] Report both reduced-form (outcome jump) and first-stage (treatment jump) separately

### IV / 2SLS

- [ ] Relevance: first-stage F-statistic reported; F > 10 for standard inference
- [ ] If F < 10: use weak-instrument-robust methods (Anderson-Rubin CI, LIML) and flag weakness
- [ ] Exclusion restriction: provide theoretical/institutional argument; discuss threats
- [ ] Monotonicity: argue no defiers (instrument shifts treatment in one direction for all)
- [ ] If multiple instruments: overidentification test (Sargan/Hansen J-test)
- [ ] Reduced-form effect reported (instrument on outcome directly) as sanity check
- [ ] Clearly state population of compliers; do not generalize LATE without justification
- [ ] Check for heterogeneity in first stage across subgroups

### Propensity Score Matching

- [ ] Propensity score model includes all confounders identified in DAG
- [ ] No post-treatment variables in the propensity score model
- [ ] Balance achieved: standardized mean differences < 0.1 for all covariates after matching
- [ ] Variance ratios near 1 for continuous covariates after matching
- [ ] Common support: overlap plot shows sufficient shared propensity score region
- [ ] Observations outside common support are dropped or flagged
- [ ] Matching algorithm and caliper specified and justified
- [ ] Sensitivity analysis conducted (Rosenbaum bounds or E-value)
- [ ] Report number of treated units matched vs unmatched

### Inverse Probability Weighting

- [ ] Propensity score model is well-specified (same checks as PSM)
- [ ] Positivity: no propensity scores are exactly 0 or 1
- [ ] Extreme weight diagnostics: check maximum weight, effective sample size
- [ ] Weight trimming or truncation applied if extreme weights exist (report threshold)
- [ ] Balance after weighting verified with weighted SMDs
- [ ] Compare trimmed and untrimmed estimates for sensitivity
- [ ] Stabilized weights used when possible (ratio of marginal to conditional probability)

### Doubly Robust

- [ ] Propensity score model balance checks pass (same as IPW)
- [ ] Outcome model specification is reasonable
- [ ] Both PSM/IPW and regression estimates reported alongside DR estimate
- [ ] If all three agree, confidence increases; if they diverge, investigate which model is misspecified
- [ ] Sensitivity analysis reported

### Synthetic Control

- [ ] Pre-treatment fit is strong: synthetic unit closely tracks treated unit pre-treatment
- [ ] Pre-treatment MSPE (mean squared prediction error) is low
- [ ] Donor pool excludes units affected by spillovers or same policy
- [ ] No single donor receives disproportionate weight (check weight distribution)
- [ ] In-space placebo test: treated unit's effect is an outlier in the distribution of placebos
- [ ] In-time placebo test: no effect found when using a fake earlier treatment date
- [ ] Leave-one-out: results are robust to dropping any single donor from the pool
- [ ] Pre-treatment period is long relative to post-treatment period

## Quick Reference: Choosing Between Similar Methods

**DiD vs Synthetic Control:**
Use DiD when you have many treated and control units. Use synthetic control when you have very few treated units (1-5) and aggregate data.

**PSM vs IPW vs Doubly Robust:**
Start with doubly robust if feasible — it is robust to misspecification of one model. Use IPW when you want to retain the full sample. Use PSM when interpretability of matched pairs matters. Always check balance regardless of method.

**Sharp RDD vs IV:**
If the assignment mechanism creates a cutoff, prefer RDD — it has weaker assumptions (local continuity vs global exclusion restriction). Use IV when there is no cutoff but an exogenous source of variation exists.

**DiD vs RDD:**
DiD exploits timing of a policy change. RDD exploits a threshold rule. If both apply (a policy change with an eligibility cutoff), RDD is often more credible because the identifying variation is more local.

**When nothing works:**
If no method has credible assumptions in your setting, the honest answer is that causal identification is not possible with the available data. Presenting correlational results with appropriate caveats is better than applying a causal method with violated assumptions.
