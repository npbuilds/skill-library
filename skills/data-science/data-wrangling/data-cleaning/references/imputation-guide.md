# Imputation Method Reference

This reference provides detailed comparisons of imputation methods, guidance on selecting among them, and techniques for validating imputation quality. Use it alongside the main data-cleaning skill when deciding how to handle missing values.

---

## Method Comparison Table

| Method | Assumptions | Pros | Cons | Best For | Computational Cost |
|--------|------------|------|------|----------|-------------------|
| **Listwise Deletion** | MCAR; missingness is rare | Simple; no bias under MCAR; preserves original distributions | Loses complete rows; biased under MAR/MNAR; reduces statistical power | MCAR with < 5% missingness; large datasets where power loss is acceptable | Negligible |
| **Pairwise Deletion** | MCAR; different analyses can use different subsets | Uses more data than listwise; each analysis uses all available cases for its variables | Inconsistent sample sizes across analyses; can produce non-positive-definite covariance matrices | Correlation and covariance estimation under MCAR | Negligible |
| **Mean / Median** | MCAR; univariate missingness | Trivial to implement; preserves column mean (for mean imputation) | Distorts variance (shrinks it); weakens correlations between variables; biased under MAR/MNAR | Quick exploratory analysis; MCAR with < 5% missingness; when speed matters more than precision | Negligible |
| **Mode** | MCAR; categorical data | Simple for categorical variables; preserves most frequent category | Inflates frequency of the mode; ignores relationships between variables | Categorical columns with low missingness and a clear dominant category | Negligible |
| **Hot-Deck** | Similar records have similar values; MCAR or MAR | Produces plausible real values (no impossible imputations); preserves distribution shape | Results vary with sort order and donor selection; no formal uncertainty quantification | Survey data; preserving distributional properties; when imputed values must be realistic | Low |
| **KNN Imputation** | Local similarity in feature space; MCAR or MAR | Captures local structure; handles mixed types (numeric + categorical); no distributional assumptions | Sensitive to k, distance metric, and feature scaling; slow on large datasets; struggles with high dimensionality | MAR data with moderate missingness; mixed-type datasets; when local patterns are informative | Moderate (O(n^2) distance computation; mitigated with approximate neighbors) |
| **MICE** | MAR; each variable's conditional distribution can be reasonably modeled | Flexible (different model per variable); handles mixed types; produces multiple imputations for proper uncertainty | Assumes MAR; no theoretical guarantee of convergence; requires careful model specification per variable; computationally intensive | MAR data with complex multivariate patterns; inference requiring proper uncertainty quantification | High (iterates over all variables for multiple imputations) |
| **EM Algorithm** | MAR; data is multivariate normal (or can be transformed to approximate normality) | Principled maximum-likelihood approach; converges to MLE under correct model | Assumes joint normality; single imputation (point estimates) unless bootstrapped; underestimates variance without modification | Continuous data that is approximately multivariate normal; when a parametric model is justified | Moderate to High |
| **Deep Learning — GAIN** | Flexible distributional assumptions; MAR or weak MNAR | Captures complex nonlinear patterns; GAN framework generates realistic imputations; no explicit distributional assumption | Requires tuning (architecture, hyperparameters); needs substantial data; hard to interpret; training instability | Large datasets with complex nonlinear relationships; when traditional methods underperform and resources allow experimentation | Very High (GPU recommended) |
| **Deep Learning — MIDA** | Denoising autoencoder framework; MAR | Handles high-dimensional data; learns robust representations; can handle mixed types with proper encoding | Black box; requires sufficient data for training; architecture decisions affect results; reproducibility concerns | High-dimensional datasets (many variables); when MICE becomes impractical due to variable count | Very High (GPU recommended) |

---

## Selecting an Imputation Method

### Decision Flowchart

```
Is missingness < 5% and MCAR?
  YES --> Mean/median (numeric) or mode (categorical) is sufficient.
          Listwise deletion is also acceptable if sample size is large.
  NO  --> Continue.

Is the data MAR with moderate missingness (5-25%)?
  YES --> Is the dataset small to medium (< 100k rows, < 50 variables)?
            YES --> Use MICE with 5-10 imputations.
            NO  --> Use KNN imputation or MICE with reduced iterations.
  NO  --> Continue.

Is the data MNAR?
  YES --> No imputation method fully corrects MNAR bias.
          Options:
          - Model the missingness mechanism explicitly (selection models, pattern-mixture models).
          - Use MICE + sensitivity analysis to bound the potential bias.
          - Add a binary "was_missing" indicator and impute under MAR assumption
            as a pragmatic compromise, documenting the limitation.
  NO  --> Continue.

Is missingness > 25% in key variables?
  YES --> Multiple imputation (MICE) is strongly recommended.
          Consider whether the variable should be retained at all.
          Validate heavily.
  NO  --> Re-evaluate mechanism classification. If truly MCAR, simpler methods suffice.
```

### When Multiple Imputation Is Worth the Complexity

Multiple imputation (generating m completed datasets, analyzing each, and pooling via Rubin's rules) adds substantial complexity to your workflow. It is worth it when:

1. **You are performing statistical inference** — hypothesis tests, confidence intervals, or p-values. Single imputation produces artificially narrow confidence intervals because it treats the imputed values as known. Multiple imputation propagates the uncertainty from the missing data into your standard errors.

2. **Missingness exceeds 10%** in variables that are central to your analysis. At low missingness rates, the difference between single and multiple imputation is negligible for most practical purposes.

3. **The downstream decision depends on effect sizes or significance thresholds.** If you are deciding whether a drug works or a policy change had an effect, underestimated uncertainty could lead to a wrong conclusion.

4. **Regulatory or publication standards require it.** Many clinical trial guidelines (ICH E9, FDA guidance) expect or require multiple imputation or sensitivity analyses for missing data.

**When simpler methods suffice:**

- Exploratory data analysis where you need directional insights, not precise estimates.
- Prediction-focused tasks (machine learning) where the model's own cross-validation captures performance uncertainty. Note: you should still impute train and test separately.
- Very low missingness (< 5%) under MCAR, where the impact on inference is minimal.
- Time-constrained prototyping where you will revisit the imputation strategy later.

---

## Validating Imputation Quality

Imputation is a form of modeling, and like any model, its output should be validated. The following checks help ensure your imputed values are plausible and that the imputation has not distorted your data.

### Distribution Comparison

Compare the marginal distribution of each imputed variable before and after imputation:

- **Visual checks:** Overlay density plots of observed values versus imputed values. The imputed values should follow a similar distribution to the observed ones (unless MAR patterns make the missing subpopulation genuinely different).
- **Summary statistics:** Compare mean, median, standard deviation, skewness, and kurtosis before and after imputation. Large shifts indicate potential problems.
- **KS test or similar:** A two-sample Kolmogorov-Smirnov test can quantify whether the imputed distribution diverges from the observed distribution.

### Correlation Preservation

Imputation should preserve the relationships between variables:

- Compute the correlation matrix on complete cases and on the imputed dataset. Compare them element-by-element.
- Mean/median imputation systematically attenuates correlations. If you see correlation shrinkage, consider a method that respects multivariate structure (KNN, MICE).

### Predictive Accuracy (Simulation-Based Validation)

The most rigorous validation approach:

1. Take a complete subset of your data (rows with no missing values).
2. Artificially introduce missingness matching the pattern in your actual data (same percentage, same mechanism if possible).
3. Apply your imputation method.
4. Compare imputed values to the known true values using RMSE (numeric) or accuracy (categorical).
5. Repeat across multiple random missingness patterns to get stable estimates.

This gives you a concrete measure of imputation error under conditions that approximate your real problem.

### Sensitivity Analysis

For MNAR data or when the mechanism is uncertain:

- Run your downstream analysis under multiple imputation scenarios (e.g., imputed values shifted up by 10%, shifted down by 10%, worst-case assumptions).
- If your conclusions are stable across scenarios, the missing data is unlikely to invalidate your findings.
- If conclusions change, report the range of results and acknowledge the sensitivity.

### Convergence Diagnostics (MICE-Specific)

When using MICE:

- Plot the mean and standard deviation of imputed values across iterations. They should stabilize (converge) after a sufficient number of iterations (typically 10-20).
- If traces show trends or oscillation, increase the number of iterations or reconsider the imputation models.
- Compare results across different numbers of imputations (m = 5, 10, 20). If pooled estimates change meaningfully when going from 5 to 20, you likely need more imputations.

---

## Implementation Notes

### Library Reference

| Language | Library | Methods Supported | Notes |
|----------|---------|-------------------|-------|
| Python | `scikit-learn` | KNN (`KNNImputer`), simple (`SimpleImputer`), iterative (`IterativeImputer` / experimental MICE) | `IterativeImputer` is experimental; set `random_state` for reproducibility |
| Python | `fancyimpute` | KNN, MICE, nuclear norm minimization, matrix factorization | Good for experimentation; some methods require dense matrices |
| Python | `miceforest` | MICE with LightGBM backend | Fast MICE for large datasets; handles mixed types well |
| R | `mice` | MICE (the reference implementation) | Gold standard; extensive diagnostics; `parlMICE` for parallelism |
| R | `Amelia` | EM-based multiple imputation | Assumes multivariate normality; very fast |
| R | `missForest` | Random forest imputation | Nonparametric; handles mixed types; OOB error for validation |

### Practical Tips

- **Always set random seeds** for reproducibility. MICE and KNN with randomized tie-breaking will produce different results across runs otherwise.
- **Scale numeric features before KNN imputation.** Unscaled features with large ranges dominate the distance calculation.
- **Use m = 5-20 imputations for MICE.** The original recommendation of m = 5 is often sufficient for low-missingness scenarios. For higher missingness (> 25%), m = 20 or more may be needed for stable pooled estimates.
- **Impute on the training set, transform the test set.** Fit your imputation model (the means, the KNN index, the MICE models) on training data. Apply the fitted imputer to test data without refitting.
- **Log everything.** Record the method used, parameters chosen, number of values imputed per variable, and validation metrics. This log is essential for reproducibility and auditing.
