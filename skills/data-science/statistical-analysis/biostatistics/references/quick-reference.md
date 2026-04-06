# Biostatistics — Quick Reference


## Quick Reference

| Attribute | Defines | Example |
|-----------|---------|---------|
| **Population** | Who | Adults with moderate-to-severe plaque psoriasis |
| **Treatment** | What intervention | Drug X 300mg vs placebo |
| **Endpoint** | What outcome | PASI 90 response at Week 16 |
| **Intercurrent events** | What happens post-randomization that complicates interpretation | Treatment discontinuation, rescue medication, death |
| **Summary measure** | How treatment effects are quantified | Difference in proportions, hazard ratio, RMST difference |

## Quick Reference

| Strategy | Handles IC Event By | Use When |
|----------|-------------------|----------|
| **Treatment policy** | Analyze regardless (classic ITT) | The policy question: "what happens if we prescribe this?" |
| **Composite** | Fold IC event into the endpoint | Death before response = non-responder |
| **While-on-treatment** | Only count time on assigned treatment | Interest is in direct pharmacological effect |
| **Hypothetical** | Estimate what would have happened without the IC event | "What if no one discontinued?" |
| **Principal stratum** | Focus on subgroup defined by IC event behavior | Effect in those who would comply regardless of arm |

## Parametric Models

| Distribution | Hazard Shape | Use When |
|-------------|-------------|----------|
| Exponential | Constant | Simple survival, memoryless process |
| Weibull | Monotone increasing/decreasing | Hazard changes steadily over time |
| Log-normal | Non-monotone (hump-shaped) | Initial risk peaks then declines |
| Log-logistic | Non-monotone | Similar to log-normal, heavier tails |

## Randomization

| Method | When to Use | Key Property |
|--------|------------|-------------|
| **Simple** | Large trials (n > 200) | Unpredictable but may produce imbalance |
| **Permuted block** | Most trials | Ensures balance within blocks; block size should vary and be concealed |
| **Stratified block** | Important prognostic factors (site, disease severity) | Balance across strata |
| **Covariate-adaptive** (minimization) | Many prognostic factors | Best overall balance; slightly predictable |
| **Response-adaptive** | Ethical pressure to assign more patients to better arm | Complex; can introduce time trends |

## Quick Reference

| Boundary | Philosophy | Alpha Spent Early | Alpha Remaining for Final |
|----------|-----------|-------------------|--------------------------|
| **O'Brien-Fleming** | Conservative early, liberal late | Very little | Most |
| **Pocock** | Equal stopping criteria at each look | Equal portions | Less at final |
| **Lan-DeMets** | Flexible alpha-spending function | Customizable | Depends on function |

## Diagnostic Test Evaluation

| Metric | Formula | Depends on Prevalence? | Interpretation |
|--------|---------|----------------------|----------------|
| **Sensitivity** | TP / (TP + FN) | No | Probability of positive test given disease |
| **Specificity** | TN / (TN + FP) | No | Probability of negative test given no disease |
| **PPV** | TP / (TP + FP) | **Yes** | Probability of disease given positive test |
| **NPV** | TN / (TN + FN) | **Yes** | Probability of no disease given negative test |
| **LR+** | Sensitivity / (1 - Specificity) | No | How much a positive test increases disease probability |
| **LR-** | (1 - Sensitivity) / Specificity | No | How much a negative test decreases disease probability |

## Epidemiological Measures

| Measure | Setting | Formula (Conceptual) | Interpretation |
|---------|---------|---------------------|----------------|
| **Relative Risk (RR)** | Cohort studies, RCTs | Incidence_exposed / Incidence_unexposed | How many times more likely in exposed group |
| **Odds Ratio (OR)** | Case-control, logistic regression | (a/b) / (c/d) from 2x2 table | Approximates RR when outcome is rare (<10%) |
| **Absolute Risk Reduction (ARR)** | RCTs | Incidence_control - Incidence_treated | Absolute difference in event rates |
| **Number Needed to Treat (NNT)** | RCTs | 1 / ARR | Patients to treat for one additional benefit |
| **Incidence rate** | Cohort studies | Events / Person-time at risk | Events per unit of person-time |
| **Prevalence** | Cross-sectional | Cases / Population at time point | Proportion with condition |

## Quick Reference

| Strategy | How It Works | Use When |
|----------|-------------|----------|
| **Fixed-sequence** | Test H1 → H2 → H3 in order; stop at first failure | Clear scientific ordering of hypotheses |
| **Gatekeeping** | Primary endpoints are "gatekeepers" for secondary | Primary/secondary hierarchy exists |
| **Graphical approach** (Bretz) | Hypotheses as nodes, alpha flows between them on rejection | Complex hypothesis structures |
| **Hochberg step-up** | Less conservative than Bonferroni | Independent or positively correlated endpoints |
| **Holm step-down** | Valid under any correlation structure | Default when no structure is assumed |
