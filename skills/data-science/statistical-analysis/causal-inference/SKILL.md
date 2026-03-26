---
name: causal-inference
description: >
  Causal inference methods for estimating treatment effects from observational data. Reference
  when designing quasi-experiments, selecting causal identification strategies, validating
  causal assumptions, or interpreting treatment effect estimates. Use when the question is
  "does X cause Y" rather than "does X predict Y."
---

# Causal Inference — The Why Engine

Correlation is not causation — but causation is what decisions require. Predicting that umbrella sales correlate with rain is useful for forecasting; knowing that a new drug *causes* recovery is what justifies prescribing it. Causal inference provides the formal machinery for moving from "X and Y move together" to "X makes Y happen."

The fundamental problem of causal inference is that we never observe both potential outcomes for the same unit. For any individual, we see what happened under the treatment they received, but we never see what *would have happened* under the alternative. Under the **Rubin causal model** (potential outcomes framework), each unit i has two potential outcomes: Y_i(1) under treatment, Y_i(0) under control. The individual treatment effect is Y_i(1) - Y_i(0), but we only ever observe one side. Every causal method is, at its core, a strategy for constructing a credible estimate of the missing counterfactual.

## The Identification Problem

The central challenge is **selection bias**: units that receive treatment differ systematically from those that do not. If sicker patients seek treatment, a naive comparison of treated vs untreated conflates the treatment effect with the severity difference. **Confounding** occurs when a variable influences both treatment assignment and the outcome.

**Directed Acyclic Graphs (DAGs)** are the primary tool for reasoning about causal structure. In a DAG, nodes represent variables and directed edges represent causal relationships. DAGs make assumptions explicit and reveal which variables must be controlled for.

- **Backdoor criterion:** A set of variables Z satisfies the backdoor criterion relative to treatment X and outcome Y if (1) no node in Z is a descendant of X, and (2) Z blocks every path between X and Y that has an arrow into X. Controlling for Z eliminates confounding.
- **Front-door criterion:** When unmeasured confounders exist between X and Y, but X operates entirely through a mediator M that has no direct confounders with Y, the front-door criterion can identify the causal effect.
- **Collider bias:** Conditioning on a common effect of two variables (a collider) *opens* a spurious path. Never control for post-treatment variables or colliders.

**Practical rule:** Before selecting a method, draw the DAG. If you cannot articulate the causal structure, no statistical technique will rescue the analysis.

## Randomized Experiments

Randomization is the gold standard because it breaks the link between treatment assignment and potential outcomes, eliminating both observed and unobserved confounding.

**Key estimands:**

| Estimand | Definition | When to use |
|----------|-----------|-------------|
| **ATE** | Average Treatment Effect across entire population | Policy affects everyone |
| **ATT** | Average Treatment Effect on the Treated | Evaluating effect on those who actually took treatment |
| **ATU** | Average Treatment Effect on the Untreated | Predicting impact of expanding a program |
| **ITT** | Intent-to-Treat: effect of being *assigned* treatment | Non-compliance exists, want conservative estimate |
| **LATE** | Local Average Treatment Effect (compliers only) | IV setting, effect for those induced by instrument |

**SUTVA** (Stable Unit Treatment Value Assumption): one unit's outcome is unaffected by another unit's treatment assignment, and there is only one version of treatment. Violations occur with spillovers (vaccination herd immunity), network effects, or general equilibrium impacts.

**Compliance issues:** When subjects do not comply with assignment, ITT estimates a diluted effect. IV methods (using assignment as instrument for actual treatment) recover the LATE for compliers. Always report both ITT and IV estimates.

## Difference-in-Differences

DiD compares the change in outcomes over time between a treated group and a control group, leveraging the assumption that both groups would have followed parallel trends absent treatment.

**Parallel trends assumption checklist:**

- [ ] Plot pre-treatment outcome trends for treated and control groups
- [ ] Run event study specification with leads and lags — pre-treatment coefficients should be near zero
- [ ] Test for differential pre-trends using a formal F-test on pre-treatment period interactions
- [ ] Consider whether anticipation effects could violate the assumption
- [ ] Verify that no concurrent policy changes differentially affected groups

**Staggered adoption pitfalls:** Standard two-way fixed effects (TWFE) with staggered treatment timing produces biased estimates because already-treated units serve as controls, and treatment effect heterogeneity across cohorts creates negative weights. Use modern estimators:

- **Callaway-Sant'Anna:** Group-time specific ATTs, then aggregate. Allows for heterogeneous effects by cohort and time.
- **Sun-Abraham:** Interaction-weighted estimator that avoids contamination from already-treated cohorts.
- **Borusyak-Jaravel-Spiess:** Imputation approach estimating counterfactuals from untreated observations.

**Rule of thumb:** If treatment rolls out at different times across units, do not use basic TWFE. Use a heterogeneity-robust estimator and report event study plots.

## Regression Discontinuity

RDD exploits a cutoff rule where treatment is assigned based on a running variable crossing a threshold. Units just above and just below the cutoff are nearly identical, creating a local quasi-experiment.

**Sharp vs Fuzzy:**
- **Sharp RDD:** Treatment deterministically changes at the cutoff. Estimate is a local ATE at the cutoff.
- **Fuzzy RDD:** Treatment probability jumps at the cutoff but is not deterministic. Estimate is a local LATE for compliers at the cutoff. Implemented as IV with cutoff-crossing as instrument.

**Validity checklist:**

- [ ] **McCrary density test:** No bunching or manipulation of the running variable at the cutoff (plot histogram, run formal density test)
- [ ] **Covariate smoothness:** Pre-determined covariates are continuous through the cutoff
- [ ] **Bandwidth sensitivity:** Results are robust across multiple bandwidth choices (use MSE-optimal bandwidth from Calonico-Cattaneo-Titiunik, then show sensitivity)
- [ ] **Polynomial order:** Use local linear (order 1) as default; higher-order polynomials overfit and produce erratic estimates at boundaries
- [ ] **Placebo cutoffs:** No treatment effect at false cutoff values away from the true threshold
- [ ] **Donut hole test:** Results hold when excluding observations very close to the cutoff (rules out precise manipulation)

## Instrumental Variables

An instrument Z affects the outcome Y only through the treatment X. IV isolates the variation in X that is driven by Z, removing bias from confounders.

**Three core assumptions:**

1. **Relevance:** Z is correlated with X (testable — first-stage F-statistic)
2. **Exclusion restriction:** Z affects Y only through X (not testable — requires theoretical argument)
3. **Monotonicity:** Z shifts everyone in the same direction (no defiers)

**Weak instruments problem:**

| First-stage F-statistic | Interpretation | Action |
|------------------------|---------------|--------|
| F > 104 (Stock-Yogo) | Strong instrument | Proceed with standard 2SLS |
| 10 < F < 104 | Moderate; some bias toward OLS | Use weak-instrument robust inference (Anderson-Rubin, LIML) |
| F < 10 | Weak instrument | Do not trust 2SLS; 2SLS bias approaches OLS bias |

**Common instruments in practice:** geographic distance to a facility (demand estimation), lottery assignment (returns to education), rainfall (conflict and economic outcomes), shift-share/Bartik instruments (labor economics). Each requires a domain-specific argument for the exclusion restriction.

## Matching & Propensity Scores

Matching methods construct a comparison group by pairing treated and untreated units with similar characteristics, attempting to approximate the randomization that was absent.

**Methods from least to most flexible:**

| Method | How it works | Strengths | Weaknesses |
|--------|-------------|-----------|------------|
| **Exact matching** | Match on identical covariate values | No functional form assumptions | Curse of dimensionality; many unmatched units |
| **Coarsened exact matching** | Coarsen covariates into bins, then exact match | Reduces dimensionality; controls imbalance bound | Requires thoughtful binning |
| **Propensity score matching** | Match on estimated P(treatment \| X) | Collapses many covariates to one score | Model-dependent; can discard data; hides imbalance |
| **Inverse probability weighting** | Weight observations by 1/P(treatment) | Uses all data; efficient | Extreme weights when propensity scores near 0 or 1 |
| **Doubly robust** | Combines outcome model + propensity weighting | Consistent if either model is correct | More complex; still requires overlap assumption |

**Balance diagnostics (mandatory, not optional):**
- Standardized mean differences (SMD) for each covariate: target SMD < 0.1 after matching
- Variance ratios: should be close to 1
- Overlap (common support) plot: verify sufficient overlap in propensity score distributions
- Do NOT rely on p-values for balance assessment — use SMD

## Synthetic Controls

When treatment affects a single unit or a small number of aggregate units (a state, a country, a firm), synthetic controls construct a weighted combination of untreated units that mimics the treated unit's pre-treatment trajectory.

**When to use:** Small number of treated units, aggregate-level data, long pre-treatment panel, clear treatment date.

**Implementation steps:**

1. Select a donor pool of untreated units (exclude units affected by spillovers)
2. Choose predictor variables and pre-treatment outcome lags
3. Optimize weights to minimize pre-treatment prediction error
4. Assess pre-treatment fit — poor fit invalidates the method
5. Estimate treatment effect as the gap between treated and synthetic unit post-treatment

**Inference via placebo tests:**
- **In-space placebo:** Apply the method to each donor unit, treating them as if they were treated. The true treated unit's effect should be an outlier in the distribution of placebo effects. Compute a p-value as the rank of the treated unit's effect.
- **In-time placebo:** Apply the method using a fake treatment date before the actual treatment. No effect should appear.

## Sensitivity Analysis

No observational study is assumption-free. Sensitivity analysis quantifies how robust conclusions are to potential violations.

- **Rosenbaum bounds:** For matched designs, ask: "How much hidden bias (unmeasured confounding) would be needed to overturn the finding?" Report the Gamma value at which significance disappears.
- **E-value:** The minimum strength of association (on the risk ratio scale) that an unmeasured confounder would need to have with both treatment and outcome to fully explain away the observed effect. Higher E-values indicate more robust findings.
- **Cinelli-Hazlett partial R-squared framework:** For regression-based studies, benchmarks the strength of unmeasured confounding against observed covariates. Ask: "Would an omitted variable need to be stronger than the strongest observed confounder to nullify the result?"

**Reporting standard:** Every causal claim from observational data should include at least one sensitivity metric. State explicitly: "An unmeasured confounder would need to [specific magnitude] to explain away this result."

## Common Mistakes

1. **Not validating parallel trends.** Asserting parallel trends without evidence is the most common DiD failure. Always show pre-trend plots and event study coefficients.
2. **Controlling for post-treatment variables.** Adjusting for variables affected by treatment introduces collider bias and blocks causal pathways. Only condition on pre-treatment covariates.
3. **Ignoring weak instruments.** Reporting 2SLS with a first-stage F < 10 produces estimates more biased than OLS. Always report the first-stage F and use robust inference if marginal.
4. **P-hacking specification choices.** Running many bandwidth choices, covariate sets, or matching algorithms and reporting only the significant one inflates false positive rates. Pre-specify the primary specification; report others as robustness.
5. **Confusing estimands.** DiD estimates ATT; IV estimates LATE; RDD estimates a local effect at the cutoff. Generalizing without justification misleads policy decisions.
6. **Skipping balance checks in matching.** Reporting propensity score matching without standardized mean differences is meaningless. If balance is poor, the estimate is unreliable regardless of the p-value.

## Implementation Libraries

| Method | Python | R |
|--------|--------|---|
| General causal inference framework, DAGs, identification | `dowhy` | `dagitty` |
| Heterogeneous treatment effects (CATE), double ML | `econml` | `grf` (generalized random forests) |
| Uplift modeling, treatment effect estimation | `causalml` | `uplift` |
| Difference-in-differences | `differences`, `pyfixest` | `fixest`, `did` (Callaway-Sant'Anna) |
| Regression discontinuity | `rdrobust` (Python port) | `rdrobust`, `rddensity` |
| IV / 2SLS, panel data | `linearmodels` | `fixest`, `ivreg` |
| Propensity score matching, weighting | `causallib`, `dowhy` | `MatchIt`, `WeightIt` |
| Synthetic control | `SparseSC`, `SyntheticControlMethods` | `Synth`, `gsynth` |
| Bayesian causal impact (structural time series) | `causalimpact`, `tfcausalimpact` | `CausalImpact` (Google) |
| Sensitivity analysis (Cinelli-Hazlett) | `pysensemakr` | `sensemakr` |

**Recommended starting stack (Python):** `dowhy` for causal graph reasoning + `econml` for effect estimation + `linearmodels` for IV/panel data. For DiD specifically, `pyfixest` mirrors R's `fixest` closely.

## When This Applies

Use this skill when the question is causal: "Did this intervention work?", "What would happen if we changed this policy?", "Does this feature cause retention?" If the goal is prediction or description, standard ML and statistical methods suffice. If the goal is to *attribute* an effect to a cause, you need the tools here.

See `references/method-comparison.md` for a decision tree that maps your data situation to the appropriate causal method, along with full assumption checklists for each approach.
