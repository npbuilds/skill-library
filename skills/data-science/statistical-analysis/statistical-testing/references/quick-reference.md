# Statistical Testing — Quick Reference


## Quick Reference

| Data Type | Groups | Design | Assumptions Met | Test |
|-----------|--------|--------|-----------------|------|
| Continuous | 1 | — | Yes | One-sample t-test |
| Continuous | 2 | Independent | Yes | Independent two-sample t-test |
| Continuous | 2 | Paired | Yes | Paired t-test |
| Continuous | k (3+) | Independent | Yes | One-way ANOVA |
| Continuous | k (3+) | Paired/Repeated | Yes | Repeated measures ANOVA |
| Continuous | 2 | Independent | No | Mann-Whitney U |
| Continuous | 2 | Paired | No | Wilcoxon signed-rank |
| Continuous | k (3+) | Independent | No | Kruskal-Wallis H |
| Continuous | k (3+) | Paired/Repeated | No | Friedman test |
| Categorical | 2+ | Independent | n >= 5 per cell | Chi-square test of independence |
| Categorical | 2 | Independent | Small n | Fisher's exact test |
| Categorical | 2 | Paired | — | McNemar's test |
| Categorical | k (3+) | Paired/Repeated | — | Cochran's Q |
| Ordinal | 2 | Independent | — | Mann-Whitney U |
| Ordinal | k (3+) | Independent | — | Kruskal-Wallis H |

## Quick Reference

| Assumption | Diagnostic Test | Visual Check |
|------------|----------------|--------------|
| Normality | Shapiro-Wilk (n < 50), Anderson-Darling, Kolmogorov-Smirnov | Q-Q plot, histogram |
| Homogeneity of variance | Levene's test (robust to non-normality), Bartlett's test (sensitive to non-normality) | Residual plots, box plots |
| Independence | Study design review — no statistical test can confirm independence | — |

## Quick Reference

| Measure | Used With | Small | Medium | Large |
|---------|-----------|-------|--------|-------|
| Cohen's d | t-tests (mean differences) | 0.2 | 0.5 | 0.8 |
| Pearson's r | Correlations | 0.1 | 0.3 | 0.5 |
| Eta-squared (eta^2) | ANOVA | 0.01 | 0.06 | 0.14 |
| Partial eta-squared | Factorial ANOVA | 0.01 | 0.06 | 0.14 |
| Omega-squared (omega^2) | ANOVA (less biased) | 0.01 | 0.06 | 0.14 |
| Odds ratio | Logistic regression, 2x2 tables | 1.5 | 2.5 | 4.3 |
| Relative risk | Cohort studies, RCTs | 1.2 | 1.8 | 3.0 |
| Cramer's V | Chi-square tests | 0.1 | 0.3 | 0.5 |
| Cohen's w | Chi-square goodness of fit | 0.1 | 0.3 | 0.5 |

## Quick Reference

| Method | Controls | Approach | When to Use |
|--------|----------|----------|-------------|
| Bonferroni | FWER | alpha / m | Few comparisons, need strict control |
| Holm-Bonferroni | FWER | Sequential step-down | Default FWER control — uniformly more powerful than Bonferroni |
| Hochberg | FWER | Sequential step-up | When test statistics are independent or non-negatively correlated |
| Benjamini-Hochberg | FDR | Sequential step-up on ranked p-values | Many comparisons, exploratory analysis |
| Tukey's HSD | FWER | Pairwise post-hoc for ANOVA | All pairwise comparisons after significant ANOVA |
| Dunnett's test | FWER | Compare treatments to control | When you have a single control group |

## Quick Reference

| Aspect | Frequentist | Bayesian |
|--------|------------|----------|
| Core output | p-value, confidence interval | Posterior distribution, credible interval |
| Interpretation of interval | 95% of intervals from repeated samples contain the true value | 95% probability the parameter lies in this interval (given the prior and data) |
| Prior information | Not formally incorporated | Explicitly encoded via prior distributions |
| Evidence for H0 | Cannot confirm H0, only fail to reject | Bayes factor can quantify evidence for H0 |
| Sample size | Fixed in advance | Can update sequentially |
| Multiple comparisons | Requires explicit correction | Handled naturally through hierarchical models |

## Implementation Libraries

| Method | Python | R |
|--------|--------|---|
| t-tests, ANOVA, chi-square, Mann-Whitney, Kruskal-Wallis | `scipy.stats` | base `stats` |
| ANOVA (detailed), regression-based tests, power analysis | `statsmodels` | `pwr`, `stats` |
| Clean API for common tests (t, ANOVA, correlation, post-hoc) | `pingouin` | `rstatix` |
| Post-hoc tests (Dunn's, Nemenyi, Conover) | `scikit-posthocs` | `PMCMRplus` |
| Bayesian tests, Bayes factors | `pymc`, `baycomp` | `BayesFactor`, `brms` |
| Multiple comparison correction | `statsmodels.stats.multitest` | `stats::p.adjust` |
| Effect size computation | `pingouin` (built-in) | `effectsize` |
| Power analysis and sample size | `statsmodels.stats.power` | `pwr` |
