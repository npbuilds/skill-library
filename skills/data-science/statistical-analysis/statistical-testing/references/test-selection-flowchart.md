# Test Selection Flowchart — Complete Reference

This reference provides the full decision tree and detailed profiles for every common statistical test. Use it alongside the main skill to select, verify, and interpret hypothesis tests.

## Decision Tree

Follow this tree from top to bottom. Start with your outcome variable type.

```
What is your outcome variable type?
|
├── CONTINUOUS (or approximately continuous)
│   |
│   ├── How many groups/conditions?
│   │   |
│   │   ├── ONE group (compare to known value)
│   │   │   ├── Normality holds? → One-sample t-test
│   │   │   └── Normality violated? → Wilcoxon signed-rank test (one-sample variant)
│   │   │
│   │   ├── TWO groups
│   │   │   ├── Independent samples?
│   │   │   │   ├── Normality + equal variance? → Student's two-sample t-test
│   │   │   │   ├── Normality + unequal variance? → Welch's t-test (preferred default)
│   │   │   │   └── Non-normal or ordinal? → Mann-Whitney U test
│   │   │   └── Paired/matched samples?
│   │   │       ├── Normality of differences? → Paired t-test
│   │   │       └── Non-normal differences? → Wilcoxon signed-rank test
│   │   │
│   │   └── THREE or more groups (k groups)
│   │       ├── Independent samples?
│   │       │   ├── Normality + equal variance? → One-way ANOVA
│   │       │   │   └── Post-hoc: Tukey HSD (all pairs), Dunnett (vs control)
│   │       │   ├── Normality + unequal variance? → Welch's ANOVA
│   │       │   └── Non-normal? → Kruskal-Wallis H test
│   │       │       └── Post-hoc: Dunn's test with correction
│   │       └── Paired/repeated measures?
│   │           ├── Normality + sphericity? → Repeated measures ANOVA
│   │           │   └── Sphericity violated? → Greenhouse-Geisser or Huynh-Feldt correction
│   │           └── Non-normal? → Friedman test
│   │               └── Post-hoc: Nemenyi test or pairwise Wilcoxon with correction
│   │
│   └── TWO continuous variables (association)
│       ├── Both normal, linear relationship? → Pearson correlation
│       ├── Non-normal or ordinal? → Spearman rank correlation
│       └── Small n or many ties? → Kendall's tau
│
├── CATEGORICAL (nominal)
│   |
│   ├── One variable, known expected proportions?
│   │   ├── All expected counts >= 5? → Chi-square goodness of fit
│   │   └── Small expected counts? → Exact multinomial test
│   │
│   ├── Two categorical variables (independence/association)?
│   │   ├── Independent samples?
│   │   │   ├── 2x2 table, all expected >= 5? → Chi-square test of independence
│   │   │   ├── 2x2 table, any expected < 5? → Fisher's exact test
│   │   │   └── Larger table, all expected >= 5? → Chi-square test of independence
│   │   └── Paired/matched samples?
│   │       ├── Two conditions (2x2)? → McNemar's test
│   │       └── Three+ conditions? → Cochran's Q test
│   │
│   └── Comparing proportions across groups?
│       ├── Two groups? → Z-test for proportions or Fisher's exact
│       └── k groups? → Chi-square test, then pairwise comparisons with correction
│
├── ORDINAL
│   ├── Two groups, independent? → Mann-Whitney U
│   ├── Two groups, paired? → Wilcoxon signed-rank
│   ├── k groups, independent? → Kruskal-Wallis H
│   ├── k groups, paired? → Friedman test
│   └── Association between two ordinal variables? → Spearman or Kendall's tau
│
└── TWO or MORE FACTORS (factorial designs)
    ├── All between-subjects? → Two-way (or N-way) ANOVA
    ├── All within-subjects? → Two-way repeated measures ANOVA
    └── Mixed (some between, some within)? → Mixed ANOVA (split-plot design)
```

## Complete Test Profiles

### One-Sample t-Test

| Property | Detail |
|----------|--------|
| **Purpose** | Test whether the mean of a single population equals a specified value |
| **Null hypothesis** | mu = mu_0 (population mean equals hypothesized value) |
| **Assumptions** | (1) Continuous data, (2) observations are independent, (3) approximately normal distribution (or n > 30) |
| **Test statistic** | t = (x_bar - mu_0) / (s / sqrt(n)), df = n - 1 |
| **Effect size** | Cohen's d = (x_bar - mu_0) / s |
| **Non-parametric alternative** | Wilcoxon signed-rank test (one-sample variant) |
| **Sample size guidance** | n >= 30 for CLT robustness; for d = 0.5, need n ~ 34 for 80% power at alpha = 0.05 |

### Independent Two-Sample t-Test (Student's and Welch's)

| Property | Detail |
|----------|--------|
| **Purpose** | Compare means of two independent groups |
| **Null hypothesis** | mu_1 = mu_2 (no difference in population means) |
| **Assumptions** | (1) Continuous data, (2) independence between and within groups, (3) normality in each group (or large n), (4) equal variances (Student's only — Welch's does not require this) |
| **Test statistic** | Student's: t = (x_bar_1 - x_bar_2) / (s_p * sqrt(1/n1 + 1/n2)); Welch's: uses separate variances with Welch-Satterthwaite df |
| **Effect size** | Cohen's d = (x_bar_1 - x_bar_2) / s_pooled |
| **Non-parametric alternative** | Mann-Whitney U test |
| **Sample size guidance** | For d = 0.5, need n ~ 64 per group for 80% power. Use Welch's as default — it performs well even when variances are equal. |

### Paired t-Test

| Property | Detail |
|----------|--------|
| **Purpose** | Compare means of two related measurements (before/after, matched pairs) |
| **Null hypothesis** | mu_d = 0 (mean of within-pair differences equals zero) |
| **Assumptions** | (1) Continuous data, (2) paired observations, (3) differences are approximately normally distributed |
| **Test statistic** | t = d_bar / (s_d / sqrt(n)), df = n - 1, where d = within-pair differences |
| **Effect size** | Cohen's d_z = d_bar / s_d (using the SD of differences) |
| **Non-parametric alternative** | Wilcoxon signed-rank test |
| **Sample size guidance** | For d_z = 0.5, need n ~ 34 pairs for 80% power. Paired designs are often more powerful than independent designs because they remove between-subject variability. |

### One-Way ANOVA

| Property | Detail |
|----------|--------|
| **Purpose** | Compare means across three or more independent groups |
| **Null hypothesis** | mu_1 = mu_2 = ... = mu_k (all group means are equal) |
| **Assumptions** | (1) Continuous data, (2) independence, (3) normality within each group, (4) homogeneity of variance (Levene's test) |
| **Test statistic** | F = MS_between / MS_within, df = (k-1, N-k) |
| **Effect size** | Eta-squared = SS_between / SS_total; omega-squared (less biased) |
| **Non-parametric alternative** | Kruskal-Wallis H test |
| **Post-hoc tests** | Tukey HSD (all pairs), Bonferroni, Holm, Dunnett (vs control), Games-Howell (unequal variances) |
| **Sample size guidance** | For f = 0.25 (medium), k = 3, need n ~ 52 per group for 80% power |

### Two-Way ANOVA

| Property | Detail |
|----------|--------|
| **Purpose** | Test main effects of two factors and their interaction on a continuous outcome |
| **Null hypothesis** | Three separate H0s: no main effect of factor A, no main effect of factor B, no A x B interaction |
| **Assumptions** | (1) Continuous outcome, (2) independence, (3) normality within each cell, (4) homogeneity of variance across cells |
| **Test statistic** | Separate F statistics for each main effect and the interaction |
| **Effect size** | Partial eta-squared for each effect |
| **Non-parametric alternative** | Aligned rank transform ANOVA; Scheirer-Ray-Hare (limited) |
| **Sample size guidance** | Interactions require larger samples than main effects. Plan for at least 20 observations per cell. |

### Repeated Measures ANOVA

| Property | Detail |
|----------|--------|
| **Purpose** | Compare means across three or more related conditions (within-subjects design) |
| **Null hypothesis** | mu_1 = mu_2 = ... = mu_k (all condition means are equal) |
| **Assumptions** | (1) Continuous data, (2) normality, (3) sphericity — the variances of all pairwise differences are equal (Mauchly's test) |
| **Test statistic** | F ratio; apply Greenhouse-Geisser or Huynh-Feldt correction if sphericity is violated |
| **Effect size** | Partial eta-squared, generalized eta-squared |
| **Non-parametric alternative** | Friedman test |
| **Sample size guidance** | More powerful than between-subjects designs due to within-subject control. For medium effect, n ~ 28 for 3 conditions. |

### Chi-Square Goodness of Fit

| Property | Detail |
|----------|--------|
| **Purpose** | Test whether observed frequency distribution matches expected proportions |
| **Null hypothesis** | The data follow the specified distribution |
| **Assumptions** | (1) Categorical data, (2) independence, (3) all expected frequencies >= 5 |
| **Test statistic** | chi^2 = sum((O_i - E_i)^2 / E_i), df = k - 1 |
| **Effect size** | Cohen's w = sqrt(chi^2 / N) |
| **Non-parametric alternative** | Exact multinomial test (for small samples) |
| **Sample size guidance** | Need expected count >= 5 in each category. For w = 0.3 (medium), df = 3, need N ~ 122 for 80% power. |

### Chi-Square Test of Independence

| Property | Detail |
|----------|--------|
| **Purpose** | Test whether two categorical variables are associated |
| **Null hypothesis** | The two variables are independent |
| **Assumptions** | (1) Categorical data, (2) independent observations, (3) expected frequency >= 5 in at least 80% of cells, no cell < 1 |
| **Test statistic** | chi^2 = sum((O_ij - E_ij)^2 / E_ij), df = (r-1)(c-1) |
| **Effect size** | Cramer's V = sqrt(chi^2 / (N * min(r-1, c-1))); phi for 2x2 tables |
| **Non-parametric alternative** | Fisher's exact test (for small samples) |
| **Sample size guidance** | Rule of thumb: N >= 5 * (number of cells). For 2x2, w = 0.3, need N ~ 88 for 80% power. |

### Fisher's Exact Test

| Property | Detail |
|----------|--------|
| **Purpose** | Test association in a 2x2 table when sample sizes are small |
| **Null hypothesis** | The two variables are independent (the odds ratio equals 1) |
| **Assumptions** | (1) 2x2 contingency table (extensions exist for larger tables), (2) independent observations, (3) fixed marginals |
| **Test statistic** | Exact p-value computed from the hypergeometric distribution |
| **Effect size** | Odds ratio |
| **When to use** | Any expected cell count < 5 in a 2x2 table. Also valid for larger samples (but computationally intensive for large tables). |
| **Sample size guidance** | No minimum sample size — the test is exact. Preferred over chi-square for all small-sample 2x2 analyses. |

### Mann-Whitney U Test (Wilcoxon Rank-Sum)

| Property | Detail |
|----------|--------|
| **Purpose** | Compare distributions of two independent groups |
| **Null hypothesis** | The two groups have identical distributions (often interpreted as equal medians when distributions have the same shape) |
| **Assumptions** | (1) Ordinal or continuous data, (2) independent observations, (3) similar distribution shapes (for median interpretation) |
| **Test statistic** | U = sum of ranks in one group minus the minimum possible; z-approximation for large n |
| **Effect size** | r = Z / sqrt(N), rank-biserial correlation |
| **Parametric counterpart** | Independent two-sample t-test |
| **Sample size guidance** | About 95% as efficient as the t-test when normality holds, and can be more powerful when it does not. For medium effect, n ~ 67 per group for 80% power. |

### Wilcoxon Signed-Rank Test

| Property | Detail |
|----------|--------|
| **Purpose** | Compare two related conditions when normality cannot be assumed |
| **Null hypothesis** | The median of the differences equals zero |
| **Assumptions** | (1) Ordinal or continuous data, (2) paired observations, (3) the distribution of differences is symmetric |
| **Test statistic** | W = sum of signed ranks; z-approximation for large n |
| **Effect size** | r = Z / sqrt(N) |
| **Parametric counterpart** | Paired t-test |
| **Sample size guidance** | For medium effect, n ~ 37 pairs for 80% power. |

### Kruskal-Wallis H Test

| Property | Detail |
|----------|--------|
| **Purpose** | Compare distributions across three or more independent groups |
| **Null hypothesis** | All groups have identical distributions |
| **Assumptions** | (1) Ordinal or continuous data, (2) independent observations, (3) similar distribution shapes across groups |
| **Test statistic** | H = (12 / (N(N+1))) * sum(R_i^2 / n_i) - 3(N+1), approximately chi-square with df = k - 1 |
| **Effect size** | Epsilon-squared = H / ((N^2 - 1) / (N + 1)) |
| **Parametric counterpart** | One-way ANOVA |
| **Post-hoc tests** | Dunn's test with Bonferroni or Holm correction |
| **Sample size guidance** | Need at least 5 observations per group. For medium effect, n ~ 55 per group for 80% power with k = 3. |

### Friedman Test

| Property | Detail |
|----------|--------|
| **Purpose** | Compare distributions across three or more related conditions |
| **Null hypothesis** | All conditions have identical distributions |
| **Assumptions** | (1) Ordinal or continuous data, (2) repeated measures or matched groups, (3) same participants in all conditions |
| **Test statistic** | Chi-square approximation based on rank sums across conditions, df = k - 1 |
| **Effect size** | Kendall's W = chi^2_F / (n * (k - 1)) |
| **Parametric counterpart** | Repeated measures ANOVA |
| **Post-hoc tests** | Nemenyi test, or pairwise Wilcoxon signed-rank tests with correction |
| **Sample size guidance** | For medium effect, need n ~ 30 for k = 3 conditions at 80% power. |

### McNemar's Test

| Property | Detail |
|----------|--------|
| **Purpose** | Test for change in a dichotomous outcome across two related conditions |
| **Null hypothesis** | The marginal probabilities are equal (proportion switching A to B equals proportion switching B to A) |
| **Assumptions** | (1) Dichotomous outcome, (2) paired observations, (3) sufficient discordant pairs (b + c >= 25 for chi-square approximation) |
| **Test statistic** | chi^2 = (b - c)^2 / (b + c), df = 1 (exact binomial for small samples) |
| **Effect size** | Odds ratio of discordant pairs = b / c |
| **Parametric counterpart** | None (this is the standard test for paired binary data) |
| **Sample size guidance** | Depends on the discordant proportion. Need at least 25 discordant pairs for the chi-square version; use exact binomial for fewer. |

### Cochran's Q Test

| Property | Detail |
|----------|--------|
| **Purpose** | Extension of McNemar's test to three or more related dichotomous conditions |
| **Null hypothesis** | The proportion of successes is the same across all conditions |
| **Assumptions** | (1) Dichotomous outcome, (2) same subjects in all conditions, (3) sufficiently large sample (n * k >= 24 as rough guide) |
| **Test statistic** | Q statistic, approximately chi-square with df = k - 1 |
| **Effect size** | No single standard; report pairwise odds ratios for follow-up |
| **Parametric counterpart** | Repeated measures logistic regression |
| **Post-hoc tests** | Pairwise McNemar's tests with Bonferroni or Holm correction |
| **Sample size guidance** | At least 10 subjects per condition as a minimum. |

### Pearson Correlation

| Property | Detail |
|----------|--------|
| **Purpose** | Measure and test linear association between two continuous variables |
| **Null hypothesis** | rho = 0 (no linear correlation in the population) |
| **Assumptions** | (1) Both variables continuous, (2) bivariate normality, (3) linear relationship, (4) homoscedasticity, (5) no extreme outliers |
| **Test statistic** | t = r * sqrt((n-2) / (1-r^2)), df = n - 2 |
| **Effect size** | r itself is the effect size |
| **Non-parametric alternative** | Spearman rank correlation |
| **Sample size guidance** | For r = 0.3 (medium), need n ~ 85 for 80% power at alpha = 0.05. |

### Spearman Rank Correlation

| Property | Detail |
|----------|--------|
| **Purpose** | Measure and test monotonic association between two variables |
| **Null hypothesis** | rho_s = 0 (no monotonic association) |
| **Assumptions** | (1) Ordinal or continuous data, (2) monotonic relationship (not necessarily linear), (3) independent observations |
| **Test statistic** | r_s = 1 - (6 * sum(d_i^2)) / (n(n^2 - 1)); for large n, use t-approximation |
| **Effect size** | r_s itself is the effect size (same benchmarks as Pearson's r) |
| **Parametric counterpart** | Pearson correlation |
| **Sample size guidance** | Similar to Pearson but slightly less powerful for truly linear relationships. For r_s = 0.3, need n ~ 90. |

### Kendall's Tau

| Property | Detail |
|----------|--------|
| **Purpose** | Measure and test monotonic association, robust to ties and small samples |
| **Null hypothesis** | tau = 0 (no concordance between rankings) |
| **Assumptions** | (1) Ordinal or continuous data, (2) independent observations |
| **Test statistic** | tau = (concordant - discordant) / (n(n-1)/2); z-approximation for significance |
| **Effect size** | tau itself (note: tau values tend to be smaller than r_s for the same data — roughly tau ~ 0.67 * r_s) |
| **Parametric counterpart** | Pearson correlation |
| **When to prefer over Spearman** | Small samples (n < 20), many tied values, or when a more robust measure is needed. Kendall's tau has better statistical properties and more intuitive interpretation as a probability. |
| **Sample size guidance** | For tau = 0.2 (roughly equivalent to r_s = 0.3), need n ~ 100 for 80% power. |

## Quick-Reference Summary Table

| Test | Data Type | Groups | Design | Parametric? |
|------|-----------|--------|--------|-------------|
| One-sample t | Continuous | 1 | — | Yes |
| Two-sample t | Continuous | 2 | Independent | Yes |
| Paired t | Continuous | 2 | Paired | Yes |
| One-way ANOVA | Continuous | k | Independent | Yes |
| Two-way ANOVA | Continuous | k (2 factors) | Independent | Yes |
| Repeated measures ANOVA | Continuous | k | Paired | Yes |
| Mann-Whitney U | Continuous/Ordinal | 2 | Independent | No |
| Wilcoxon signed-rank | Continuous/Ordinal | 2 | Paired | No |
| Kruskal-Wallis H | Continuous/Ordinal | k | Independent | No |
| Friedman | Continuous/Ordinal | k | Paired | No |
| Chi-square GOF | Categorical | 1 | — | — |
| Chi-square independence | Categorical | 2 vars | Independent | — |
| Fisher's exact | Categorical | 2 vars | Independent | — |
| McNemar's | Categorical (binary) | 2 | Paired | — |
| Cochran's Q | Categorical (binary) | k | Paired | — |
| Pearson r | Continuous | 2 vars | — | Yes |
| Spearman r_s | Continuous/Ordinal | 2 vars | — | No |
| Kendall's tau | Continuous/Ordinal | 2 vars | — | No |
