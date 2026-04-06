---
name: statistical-testing
description: >
  Statistical hypothesis testing frameworks for data analysis. Reference when choosing between
  parametric and non-parametric tests, designing hypothesis tests, computing power and effect
  sizes, correcting for multiple comparisons, or deciding between Bayesian and frequentist
  approaches. Use when any analysis needs rigorous statistical inference.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Statistical Testing — The Inference Engine

Statistical testing is the machinery that converts data into defensible claims. It provides the formal framework for deciding whether observed patterns reflect genuine phenomena or merely noise. Mastering this framework means knowing not just which test to run, but understanding what the results actually tell you — and, critically, what they do not.

This skill covers the full lifecycle of statistical inference: formulating hypotheses, selecting the right test, verifying assumptions, quantifying effect sizes, planning for adequate power, and handling the complications that arise when you test more than one thing at once.

## The Hypothesis Testing Framework

Every hypothesis test begins with two competing statements. The **null hypothesis (H0)** asserts no effect, no difference, or no association — it is the default position. The **alternative hypothesis (H1)** asserts the effect you are investigating exists. The test evaluates whether the data provide sufficient evidence to reject H0 in favor of H1.

**Key concepts:**

- **Significance level (alpha):** The probability of rejecting H0 when it is actually true (Type I error). Conventionally set at 0.05, but this is a social norm, not a law of nature. Use 0.01 for high-stakes decisions, 0.10 for exploratory analysis.
- **Type I error (false positive):** Concluding an effect exists when it does not.
- **Type II error (false negative):** Failing to detect an effect that genuinely exists. The probability of this is beta; power = 1 - beta.
- **p-value:** The probability of observing data at least as extreme as what was collected, assuming H0 is true. It is NOT the probability that H0 is true. It is NOT the probability of the result being due to chance. It does not measure effect size or practical importance.
- **Confidence intervals:** A 95% CI means that if you repeated the study many times, 95% of the constructed intervals would contain the true parameter. CIs are the dual of hypothesis tests — if the CI for a difference excludes zero, the corresponding test rejects H0 at that alpha level. Always report CIs alongside p-values; they convey both the estimate and its uncertainty.

Remember: a statistically significant result may be trivially small, and a non-significant result may reflect insufficient power rather than absence of effect.

## Test Selection

Choosing the correct test depends on four factors: data type, number of groups, study design (paired vs independent), and whether parametric assumptions hold. See `references/test-selection-flowchart.md` for the complete decision tree and detailed test profiles.

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

**Quick decision path:** Start with the outcome variable type, then count groups, then check design, then verify assumptions. If assumptions fail, move to the non-parametric column.

## Assumptions and Diagnostics

Parametric tests earn their power from distributional assumptions. When those assumptions hold, parametric tests are more efficient. When they break, results can be misleading.

**Core assumptions and how to check them:**

| Assumption | Diagnostic Test | Visual Check |
|------------|----------------|--------------|
| Normality | Shapiro-Wilk (n < 50), Anderson-Darling, Kolmogorov-Smirnov | Q-Q plot, histogram |
| Homogeneity of variance | Levene's test (robust to non-normality), Bartlett's test (sensitive to non-normality) | Residual plots, box plots |
| Independence | Study design review — no statistical test can confirm independence | — |

**When assumptions are violated:**

1. **Mild non-normality with large n (n > 30):** The Central Limit Theorem protects you. Proceed with parametric tests, but report the violation.
2. **Moderate non-normality:** Apply transformations — log, square root, Box-Cox. Re-check assumptions after transforming.
3. **Severe non-normality or small n:** Switch to non-parametric alternatives (see table above).
4. **Unequal variances (two groups):** Use Welch's t-test (default in most modern software) instead of Student's t-test.
5. **Unequal variances (ANOVA):** Use Welch's ANOVA or Brown-Forsythe test.
6. **Non-independence:** This is the most serious violation. Redesign the analysis using mixed models, GEE, or cluster-robust standard errors.

## Effect Sizes

A p-value tells you whether an effect is likely to be non-zero. An effect size tells you whether it is large enough to matter. Always report both.

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

Cohen's benchmarks are defaults, not goals. A "small" effect in medicine (e.g., a drug that reduces mortality by 2%) can be profoundly important. A "large" effect in a poorly controlled study may be an artifact. Context determines what counts as practically significant.

## Power Analysis

Statistical power is the probability of detecting a true effect. The four quantities — alpha, power, effect size, and sample size — are mathematically linked: fix any three and you can solve for the fourth.

**A priori power analysis (before data collection):** Determine the minimum sample size needed to detect a meaningful effect at your chosen alpha and power level. This is the standard approach and should be part of every study protocol.

- Target power: 0.80 is conventional (accepting a 20% chance of missing a real effect). Use 0.90 or 0.95 for critical decisions.
- Effect size: Estimate from pilot data, prior literature, or the smallest effect that would be practically meaningful.
- Alpha: Typically 0.05, but adjust based on context.

**Post-hoc power analysis (after data collection):** Calculating power using the observed effect size is circular and uninformative — it maps one-to-one with the p-value. If your study was non-significant, the useful question is: "What effect sizes could this study have detected?" Report a sensitivity analysis or confidence intervals instead.

**Why power matters:**

- **Underpowered studies** waste resources: they are unlikely to detect real effects and produce unreliable estimates with exaggerated effect sizes (the "winner's curse").
- **Overpowered studies** may detect trivially small effects that have no practical significance, and they consume more participants than necessary — an ethical concern, particularly in clinical research.

## Multiple Comparisons

Testing multiple hypotheses simultaneously inflates the overall false positive rate. If you run 20 independent tests at alpha = 0.05, you expect one false positive on average even when all null hypotheses are true.

**Correction methods:**

| Method | Controls | Approach | When to Use |
|--------|----------|----------|-------------|
| Bonferroni | FWER | alpha / m | Few comparisons, need strict control |
| Holm-Bonferroni | FWER | Sequential step-down | Default FWER control — uniformly more powerful than Bonferroni |
| Hochberg | FWER | Sequential step-up | When test statistics are independent or non-negatively correlated |
| Benjamini-Hochberg | FDR | Sequential step-up on ranked p-values | Many comparisons, exploratory analysis |
| Tukey's HSD | FWER | Pairwise post-hoc for ANOVA | All pairwise comparisons after significant ANOVA |
| Dunnett's test | FWER | Compare treatments to control | When you have a single control group |

**Decision guide:**

1. **Confirmatory analysis with few tests (< 10):** Use Holm-Bonferroni. It controls FWER and is strictly more powerful than Bonferroni.
2. **Exploratory analysis or genomics/many tests:** Use Benjamini-Hochberg FDR. Accept that some discoveries will be false, but maintain a controlled rate.
3. **Post-hoc pairwise comparisons after ANOVA:** Use Tukey's HSD (all pairs) or Dunnett's (vs. control).
4. **Pre-specified primary and secondary outcomes:** Consider a hierarchical testing procedure — test the primary outcome first at full alpha, then proceed to secondary outcomes only if the primary is significant.

## Bayesian vs Frequentist

Both paradigms answer different questions. The frequentist approach asks: "How surprising are these data if H0 is true?" The Bayesian approach asks: "How should I update my beliefs given these data?"

| Aspect | Frequentist | Bayesian |
|--------|------------|----------|
| Core output | p-value, confidence interval | Posterior distribution, credible interval |
| Interpretation of interval | 95% of intervals from repeated samples contain the true value | 95% probability the parameter lies in this interval (given the prior and data) |
| Prior information | Not formally incorporated | Explicitly encoded via prior distributions |
| Evidence for H0 | Cannot confirm H0, only fail to reject | Bayes factor can quantify evidence for H0 |
| Sample size | Fixed in advance | Can update sequentially |
| Multiple comparisons | Requires explicit correction | Handled naturally through hierarchical models |

**When to prefer Bayesian methods:**

- You have meaningful prior information from previous studies or domain expertise.
- You need to quantify evidence for the null hypothesis (not just against it).
- You want sequential analysis — examining data as it accumulates without inflating error rates.
- The question is naturally about probabilities of hypotheses, not long-run frequencies.

**When to prefer frequentist methods:**

- Regulatory or publication contexts that require p-values.
- You lack defensible prior information and want to avoid prior sensitivity debates.
- The analysis is simple and well-served by standard tests.
- Computational resources or expertise for Bayesian methods are limited.

**Bayes factor guidelines (Kass and Raftery scale):** BF > 3 is positive evidence, BF > 20 is strong evidence, BF > 150 is very strong evidence. A BF of 1 indicates the data are equally consistent with both hypotheses.

## Common Mistakes

1. **p-hacking:** Running multiple analyses and reporting only the significant ones. Pre-register your analysis plan and report all tests conducted.
2. **HARKing (Hypothesizing After Results are Known):** Presenting exploratory findings as if they were predicted a priori. Label exploratory analyses honestly.
3. **Confusing statistical and practical significance:** A p-value of 0.001 with Cohen's d of 0.05 means you have strong evidence for a negligible effect. Always report and interpret effect sizes.
4. **Ignoring assumptions:** Running a t-test on heavily skewed data with n = 8 produces unreliable results. Check assumptions before interpreting output.
5. **Interpreting non-significance as "no effect":** Absence of evidence is not evidence of absence. Report power or equivalence tests to support claims of no difference.
6. **Dropping outliers without justification:** Removing data points because they are inconvenient is data manipulation. Use pre-specified rules or robust methods instead.

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

**Recommended starting stack (Python):** `scipy.stats` for standard tests + `pingouin` for a cleaner API and built-in effect sizes + `statsmodels` for power analysis and ANOVA tables.

## When This Applies

- Comparing group means or proportions in experimental or observational studies
- A/B testing and product experimentation
- Clinical trial design and analysis
- Survey analysis with categorical or ordinal outcomes
- Quality control and process monitoring
- Any analysis where you need to distinguish signal from noise with quantified uncertainty
- Power calculations and sample size planning before data collection
- Reviewing or auditing statistical claims in published research

## Cross-Domain Connections

- **Investing/portfolio-construction/factor-exposure**: Factor validation IS hypothesis testing — determining whether a factor's historical outperformance is statistically significant or data-mined. Multiple comparison correction (Bonferroni, BH) is critical for the "factor zoo" problem where hundreds of candidate factors are tested.
- **Investing/adaptive-monitoring/alt-data-monitoring**: Alternative data signal discovery requires power analysis (how much history do you need?) and multiple hypothesis correction (you're testing dozens of signals — most will be spurious).
