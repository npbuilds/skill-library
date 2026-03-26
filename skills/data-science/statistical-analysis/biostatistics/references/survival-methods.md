# Survival Analysis Method Selection Guide

Decision framework for choosing the right time-to-event method.

## Decision Tree

```
Is the goal description or comparison?
├── Description (single group)
│   ├── Non-parametric estimate → Kaplan-Meier
│   ├── Median survival + CIs → KM with Greenwood formula
│   └── Landmark survival probability → KM at time t
│
├── Comparison (two+ groups, no covariates)
│   ├── Proportional hazards expected?
│   │   ├── Yes → Log-rank test
│   │   └── No (delayed effect, crossing curves)
│   │       ├── MaxCombo test (combines multiple weighted log-rank)
│   │       ├── RMST difference (restricted mean survival time)
│   │       └── Milestone analysis (survival at specific time points)
│   │
│   └── Competing risks present?
│       ├── Yes → Gray's test for CIF comparison
│       └── No → Log-rank or MaxCombo
│
└── Regression (adjusting for covariates)
    ├── Proportional hazards assumption holds?
    │   ├── Yes → Cox PH model
    │   └── No
    │       ├── Time-varying coefficients (Cox with interactions)
    │       ├── Stratified Cox (stratify by non-PH variable)
    │       ├── AFT model (parametric: Weibull, log-normal, log-logistic)
    │       └── RMST regression
    │
    ├── Competing risks present?
    │   ├── Interested in event-specific hazard → Cause-specific Cox model
    │   └── Interested in cumulative incidence → Fine-Gray model
    │
    ├── Recurrent events?
    │   ├── Andersen-Gill model (extended Cox for recurrent events)
    │   ├── PWP (Prentice-Williams-Peterson) model
    │   └── Frailty model (random effect for within-subject correlation)
    │
    └── High-dimensional covariates?
        ├── Regularized Cox (Lasso/Ridge/Elastic Net)
        ├── Random Survival Forest
        └── Gradient Boosted Survival (scikit-survival)
```

## Method Comparison Table

| Method | Assumptions | Handles Covariates | Handles Competing Risks | Handles Non-PH | Output |
|--------|------------|-------------------|------------------------|----------------|--------|
| **Kaplan-Meier** | Independent censoring | No | No (overestimates CIF) | N/A | Survival curve, median, landmarks |
| **Log-rank test** | PH, independent censoring | No (but can stratify) | No | No | p-value for group comparison |
| **MaxCombo** | Independent censoring | No | No | **Yes** | p-value (better power for delayed effects) |
| **Cox PH** | PH, independent censoring, linearity | **Yes** | Cause-specific only | No (by default) | Hazard ratios, survival curves |
| **Stratified Cox** | PH within strata | **Yes** | Cause-specific only | Partially (via stratification) | Hazard ratios (common across strata) |
| **Cox with time-varying coefficients** | Independent censoring | **Yes** | Cause-specific only | **Yes** | Time-dependent hazard ratios |
| **Fine-Gray** | Independent censoring of competing risks | **Yes** | **Yes** | No | Subdistribution hazard ratios |
| **Cause-specific hazards** | Independent censoring | **Yes** | **Yes** (each event modeled) | No (per cause) | Cause-specific hazard ratios |
| **Weibull AFT** | Weibull distribution, independent censoring | **Yes** | No | **Yes** (non-PH via AFT) | Time ratios (acceleration factors) |
| **Log-normal AFT** | Log-normal distribution | **Yes** | No | **Yes** | Time ratios |
| **RMST** | Independent censoring, specified time horizon | Limited (regression extensions) | Via separate models | **Yes** | Mean survival difference in time units |
| **Random Survival Forest** | Minimal | **Yes** (non-linear) | Via competing risk extensions | **Yes** (inherently) | Predicted survival curves, variable importance |
| **Gradient Boosted Survival** | Minimal | **Yes** (non-linear) | Limited | **Yes** | Predicted risk scores |

## Proportional Hazards Diagnostics

**Test before using Cox PH.** If PH is violated, the overall hazard ratio is a weighted average that may not represent the treatment effect at any specific time.

| Diagnostic | How | Interpretation |
|-----------|-----|----------------|
| **Schoenfeld residuals** | `cox.zph()` in R, `check_assumptions()` in lifelines | Test and plot. Non-zero slope = PH violation. The gold standard. |
| **Log-log survival plot** | Plot log(-log(S(t))) vs log(t) by group | Parallel curves = PH holds. Crossing or diverging = violation. |
| **Time-covariate interaction** | Add `covariate * log(t)` to Cox model | Significant interaction = time-varying effect. |
| **Observed vs. expected plots** | Compare KM curves to Cox-predicted curves | Divergence at specific time points reveals where PH fails. |

**When PH fails, consider:**
1. **Reporting RMST** — Difference in restricted mean survival time. Clinically interpretable, assumption-lean.
2. **Milestone analysis** — Survival difference at pre-specified time points (e.g., 12-month survival rate).
3. **Piecewise Cox** — Allow different hazard ratios in different time intervals.
4. **AFT models** — Model how covariates accelerate/decelerate time, not hazards.

## Sample Size for Survival Trials

The number of **events**, not patients, determines power. Required events:

```
Events = 4 × (z_alpha + z_beta)^2 / (log(HR))^2

For HR = 0.75, 80% power, two-sided alpha = 0.05:
Events = 4 × (1.96 + 0.84)^2 / (log(0.75))^2 = 4 × 7.84 / 0.083 ≈ 378 events
```

Then calculate patients needed based on:
- **Accrual rate:** How many patients enrolled per month
- **Accrual period:** Total enrollment duration
- **Follow-up period:** Additional follow-up after last patient enrolled
- **Event rate:** Expected proportion experiencing the event
- **Dropout rate:** Expected loss to follow-up

**Rule of thumb:** More events = more power. Longer follow-up or higher event rates reduce the number of patients needed.

## Censoring Types and Handling

| Type | Definition | Example | Standard Handling |
|------|-----------|---------|-------------------|
| **Right censoring** | Event hasn't happened by end of observation | Patient alive at data cutoff | KM, Cox — standard methods handle this |
| **Left censoring** | Event happened before observation started | HIV infection detected but onset unknown | Parametric models, interval methods |
| **Interval censoring** | Event happened between two observation times | Disease progression detected at scheduled visit | Interval-censored survival models (icenReg in R) |
| **Informative censoring** | Censoring is related to the event | Sicker patients drop out more | Sensitivity analyses required; IPCW methods |

**Independent censoring is the critical assumption.** If patients who are censored have different prognosis than those who remain, standard methods are biased. Always assess whether dropout is related to the outcome using available baseline and time-varying covariates.

## Competing Risks Decision Guide

```
Are there competing events that prevent the event of interest?
├── No → Standard KM + Cox
└── Yes
    ├── What is the clinical question?
    │   ├── "What is the hazard of event A, ignoring event B?"
    │   │   → Cause-specific hazards model
    │   │   (Censors competing events; estimates cause-specific HR)
    │   │
    │   └── "What is the cumulative probability of event A accounting for event B?"
    │       → Fine-Gray model / Cumulative Incidence Function
    │       (Treats competing event as informative; estimates subdistribution HR)
    │
    └── Report BOTH cause-specific and subdistribution analyses
        (They answer different questions; present both for completeness)
```

## Common Survival Analysis Packages

| Task | Python | R |
|------|--------|---|
| KM curves, Cox PH, AFT | `lifelines` | `survival` |
| Publication-quality survival plots | `lifelines` (built-in) | `survminer` |
| ML-based survival (RSF, boosting, regularized Cox) | `scikit-survival` | `randomForestSRC`, `mboost` |
| Competing risks (CIF, Fine-Gray) | `lifelines`, `scikit-survival` | `cmprsk`, `tidycmprsk` |
| Interval-censored data | — | `icenReg`, `survival` (Surv type "interval") |
| Recurrent events | — | `survival` (counting process), `frailtypack` |
| Multistate models | — | `mstate`, `msm` |
| Survival neural networks (DeepSurv) | `pycox`, `scikit-survival` | — |
| RMST analysis | `lifelines` (restricted_mean_survival_time) | `survRM2` |
