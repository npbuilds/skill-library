# Statistical Analysis — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Hypothesis testing, p-values, confidence intervals, A/B tests, power analysis | `statistical-testing` | Core frequentist inference |
| Multiple comparisons, correction methods, family-wise error | `statistical-testing` | Advanced testing methodology |
| Does X cause Y, treatment effects, natural experiments, diff-in-diff | `causal-inference` | Causal identification strategies |
| Instrumental variables, regression discontinuity, propensity scores | `causal-inference` | Quasi-experimental methods |
| Survival curves, hazard ratios, Kaplan-Meier, Cox regression | `biostatistics` | Time-to-event analysis |
| Clinical trial design, sample size, randomization, regulatory stats | `biostatistics` | Clinical and regulatory methodology |
| Meta-analysis, systematic review, effect size pooling | `biostatistics` | Evidence synthesis |
| Epidemiological measures, relative risk, odds ratios, incidence | `biostatistics` | Population health statistics |
| "Is this result real?", "can I trust this finding?" | `statistical-testing` first | Start with validity, escalate to causation if needed |
| "What caused this change?" | `causal-inference` | "Why" implies causation, not just association |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| statistical-testing says "significant" but causal-inference says "no causal claim possible" | Causal inference wins — report as association, not causation | Statistical significance ≠ causal evidence; identification strategy determines whether causal language is warranted |
| causal-inference recommends an IV approach but biostatistics says the clinical context violates the exclusion restriction | Biostatistics wins on domain knowledge | Domain expertise constrains method choice; a technically valid method can fail in context |
| statistical-testing says "not significant" but effect size is clinically meaningful | Report both — statistical significance ≠ practical significance | Underpowered studies can miss real effects; effect size and confidence interval matter more than p-value alone |
| biostatistics recommends survival analysis but causal-inference prefers diff-in-diff | Depends on the question — survival analysis for time-to-event, diff-in-diff for policy evaluation | Match the method to the estimand, not the data structure |
