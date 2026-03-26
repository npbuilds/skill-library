# Fairness Metrics Reference

Comprehensive reference for fairness metrics used in ML auditing. Covers formal definitions, impossibility results, domain-specific selection guidance, and regulatory mappings.

## Complete Fairness Metrics Table

The following table defines each metric, states when it is satisfied, identifies impossibility conflicts, lists typical domains, and provides implementation guidance.

### Statistical Parity (Demographic Parity)

- **Formal definition:** P(Y_hat = 1 | A = 0) = P(Y_hat = 1 | A = 1). The selection rate (positive prediction rate) is equal across groups defined by protected attribute A.
- **Satisfied when:** The proportion of positive predictions is identical (or within a tolerance, typically the 4/5ths rule threshold) for all groups.
- **Impossibility conflicts with:** Calibration and predictive parity when base rates differ across groups. If Group A has a 30% positive base rate and Group B has a 10% base rate, equalizing selection rates forces the model to either over-select from Group B or under-select from Group A, breaking calibration.
- **Typical domain:** Hiring (adverse impact analysis under EEOC guidelines), lending (ECOA fair lending), any context where equal selection rates are legally or ethically required.
- **Implementation:** Compute positive prediction rate per group. Use the ratio of the lowest group rate to the highest group rate. The 4/5ths (80%) rule from EEOC guidelines flags disparate impact when this ratio falls below 0.80. Libraries: `fairlearn.metrics.demographic_parity_difference`, `aif360.metrics.BinaryLabelDatasetMetric.disparate_impact`.

### Equalized Odds

- **Formal definition:** P(Y_hat = 1 | Y = 1, A = a) = P(Y_hat = 1 | Y = 1, A = b) AND P(Y_hat = 1 | Y = 0, A = a) = P(Y_hat = 1 | Y = 0, A = b). Both the true positive rate (TPR) and false positive rate (FPR) are equal across groups.
- **Satisfied when:** The model's error rates (both types) are balanced across groups. The model is equally accurate for each group conditional on the true label.
- **Impossibility conflicts with:** Calibration when base rates differ (Chouldechova 2017). Cannot simultaneously have equal TPR, equal FPR, and calibrated scores unless base rates are identical or the model is perfect.
- **Typical domain:** Criminal justice (pretrial risk assessment — errors in both directions carry significant harm), medical diagnosis (false negatives and false positives both matter).
- **Implementation:** Compute TPR and FPR per group. Report the absolute difference or ratio. Libraries: `fairlearn.metrics.equalized_odds_difference`, `aif360.metrics.ClassificationMetric.equal_opportunity_difference` (note: AIF360 names this differently).

### Equal Opportunity

- **Formal definition:** P(Y_hat = 1 | Y = 1, A = a) = P(Y_hat = 1 | Y = 1, A = b). The true positive rate is equal across groups. This is a relaxation of equalized odds that only constrains TPR.
- **Satisfied when:** Among individuals who truly deserve a positive outcome, the model identifies them at equal rates regardless of group membership.
- **Impossibility conflicts with:** Predictive parity when base rates differ. Satisfying equal opportunity while maintaining equal PPV is generally impossible with unequal base rates.
- **Typical domain:** Hiring (qualified candidates from all groups should be identified at equal rates), loan approval (creditworthy applicants should be approved equally), scholarship selection.
- **Implementation:** Compute recall (TPR) per group and compare. Libraries: `fairlearn.metrics.true_positive_rate` computed per group, `aif360.metrics.ClassificationMetric.equal_opportunity_difference`.

### Predictive Parity

- **Formal definition:** P(Y = 1 | Y_hat = 1, A = a) = P(Y = 1 | Y_hat = 1, A = b). The positive predictive value (precision) is equal across groups.
- **Satisfied when:** A positive prediction is equally trustworthy regardless of the individual's group membership. If the model says "high risk," the actual probability of the outcome is the same for all groups.
- **Impossibility conflicts with:** Equalized odds and equal opportunity when base rates differ. If one group has a lower base rate, achieving equal PPV while also having equal TPR is mathematically impossible (Chouldechova 2017).
- **Typical domain:** Risk assessment tools where the meaning of a score must be consistent (recidivism prediction, credit risk scoring), any context where decision-makers act on positive predictions and need them to mean the same thing across groups.
- **Implementation:** Compute precision per group and compare. Libraries: `sklearn.metrics.precision_score` computed per group.

### Calibration by Group

- **Formal definition:** P(Y = 1 | S = s, A = a) = s for all score values s and all groups a. The predicted probability matches the observed frequency within each group at every score level.
- **Satisfied when:** A predicted probability of 0.7 means a 70% chance of the positive outcome for every group. The score is equally meaningful regardless of group membership.
- **Impossibility conflicts with:** Equalized odds and equal opportunity (when base rates differ). A well-calibrated model with different base rates will necessarily produce different selection rates and different TPR/FPR across groups.
- **Typical domain:** Any system where predicted probabilities are used directly for decision-making rather than just ranking: insurance pricing, medical risk scores, credit scoring with continuous risk tiers.
- **Implementation:** Partition predictions into bins, compute observed positive rate per bin per group, and compare. Reliability diagrams (calibration curves) per group provide visual assessment. Libraries: `sklearn.calibration.calibration_curve` computed per group, then compare curves.

### Individual Fairness

- **Formal definition:** For a Lipschitz condition on the model: d_output(f(x_i), f(x_j)) <= L * d_input(x_i, x_j). Similar individuals (as measured by a task-relevant distance metric d_input) receive similar predictions (as measured by d_output).
- **Satisfied when:** The model does not produce wildly different predictions for individuals who differ only in protected attributes or irrelevant features. The definition of "similar" is encoded in the distance metric.
- **Impossibility conflicts with:** Group fairness metrics in general. Individual fairness can produce group-level disparities if the distance metric reflects features correlated with group membership. Conversely, enforcing group parity may require treating similar individuals from different groups differently.
- **Typical domain:** Personalized decisions where group-level statistics are less relevant: personalized medicine, individualized pricing, any context where the fairness concern is "why was I treated differently from someone like me?"
- **Implementation:** The core challenge is defining d_input. Approaches include: learning the metric from human judgments (Ilvento 2020), using domain expert specifications, or using causal distance (counterfactual similarity). Libraries: limited tooling; often requires custom implementation. `fairlearn` has some support for individual fairness via metric frames.

### Counterfactual Fairness

- **Formal definition:** P(Y_hat_A<-a(U) = y | X = x, A = a) = P(Y_hat_A<-a'(U) = y | X = x, A = a) for all a, a', y. The prediction would be the same in a counterfactual world where the individual's protected attribute A took a different value a', holding the causal background variables U fixed.
- **Satisfied when:** Changing a person's protected attribute (and all downstream causal effects of that attribute) does not change the prediction. This requires a causal model specifying which variables are causally affected by the protected attribute.
- **Impossibility conflicts with:** Accuracy, if features causally downstream of the protected attribute are also genuinely predictive. For example, in a lending model, if income is causally affected by race (through historical discrimination), counterfactual fairness requires ignoring income's race-attributable component, which may reduce accuracy.
- **Typical domain:** Contexts where causal reasoning is feasible and the causal structure is understood: policy analysis, scenarios where you can articulate "what would have happened if this person had been a different race/gender?"
- **Implementation:** Requires specifying a causal DAG. Fit a structural equation model, intervene on the protected attribute, and check whether predictions change. Libraries: `dowhy` for causal inference, custom implementations using pyro or other probabilistic programming frameworks.

### Treatment Equality

- **Formal definition:** FN/FP ratio is equal across groups. The ratio of false negatives to false positives is the same for all groups.
- **Satisfied when:** The relative balance of error types is consistent across groups, even if absolute error rates differ. If one group has twice as many false positives as false negatives, every group should have that same 2:1 ratio.
- **Impossibility conflicts with:** Statistical parity and equalized odds in most practical settings. Treatment equality focuses on the ratio of errors rather than their rates.
- **Typical domain:** Criminal justice (balancing the harm of wrongful detention vs. failure to detain), medical screening (balancing unnecessary procedures vs. missed diagnoses).
- **Implementation:** Compute false negative count and false positive count per group. Take the ratio FN/FP per group and compare. No dedicated library function; compute from confusion matrices per group.

## Impossibility Results Explained

### The Core Impossibility (Chouldechova 2017)

For a binary classifier with a binary protected attribute where the two groups have different base rates (P(Y=1 | A=0) != P(Y=1 | A=1)), it is mathematically impossible to simultaneously achieve:

1. Equal false positive rates across groups (part of equalized odds)
2. Equal false negative rates across groups (part of equalized odds)
3. Equal positive predictive values across groups (predictive parity)

Unless the classifier is perfect (zero errors) or the base rates are actually equal.

**Example:** Consider a recidivism prediction tool where Group A has a 40% recidivism base rate and Group B has a 20% base rate. If the model is calibrated (a score of 0.6 means 60% chance of recidivism for both groups), then at any fixed threshold:
- Group A will have more true positives relative to its size (higher TPR) because more of its members are above the threshold.
- To equalize TPR, you must lower the threshold for Group B, which increases Group B's FPR.
- But increasing Group B's FPR while keeping calibration means the PPV for Group B decreases.

You cannot fix all three simultaneously. The choice of which to prioritize is a normative decision.

### Kleinberg, Mullainathan, and Raghavan (2016)

Independently proved that calibration is incompatible with balance (equal error rates across groups) when base rates differ. They showed that the only classifiers satisfying both are perfect classifiers or those that assign the same score to everyone.

### Practical Implication

Every fairness audit must begin with a normative choice: which type of error matters most, and for whom? This choice should be made by stakeholders (not just engineers), documented explicitly, and revisited as context changes.

## Metric Selection Guide by Domain

### Criminal Justice (Pretrial Risk Assessment)

**Primary metric:** Equalized odds (balance both TPR and FPR).
**Rationale:** Both false positives (wrongful detention) and false negatives (failure to identify risk) cause serious harm. Neither error type should fall disproportionately on one group.
**Secondary metric:** Calibration by group — if judges use scores directly, a "7 out of 10" must mean the same thing regardless of defendant's race.
**Trade-off to document:** Equalizing error rates across groups with different base rates will break calibration. The system must choose between equally meaningful scores and equally distributed errors.

### Hiring and Employment

**Primary metric:** Statistical parity (4/5ths rule) for initial screening; equal opportunity for final decisions.
**Rationale:** EEOC guidelines use the 4/5ths rule as an initial screen for adverse impact. Beyond legal compliance, equal opportunity ensures qualified candidates from all groups are identified at equal rates.
**Secondary metric:** Treatment equality — the ratio of qualified-but-rejected to unqualified-but-accepted should not vary by group.
**Trade-off to document:** Enforcing statistical parity may require selecting less-qualified candidates from some groups, which can conflict with predictive parity.

### Lending and Credit

**Primary metric:** Equal opportunity (qualified borrowers approved at equal rates) combined with calibration by group (risk scores are equally meaningful).
**Rationale:** ECOA and FCRA require non-discriminatory lending. Creditworthy applicants from all groups deserve equal access. Calibration ensures risk-based pricing is fair.
**Secondary metric:** Statistical parity (monitored for disparate impact under fair lending regulations).
**Trade-off to document:** If historical credit data reflects discriminatory access to credit-building opportunities, equal opportunity on biased labels may perpetuate disparities. Consider alternative data sources and label correction.

### Healthcare

**Primary metric:** Equal opportunity (patients with a condition are identified at equal rates across groups).
**Rationale:** Missed diagnoses in underserved populations cause direct physical harm. The Obermeyer et al. (2019) study showed that using healthcare costs as a proxy for health need disadvantaged Black patients.
**Secondary metric:** Calibration by group — risk scores must be equally predictive across demographic groups to avoid misallocation of clinical resources.
**Trade-off to document:** Measurement bias is pervasive in healthcare (e.g., cost != need, lab values have race-specific reference ranges). Audit the label and features, not just the model.

### Content Moderation

**Primary metric:** Equalized odds across language/dialect groups and demographic groups.
**Rationale:** Both over-moderation (censoring legitimate speech, disproportionately affecting minority dialects) and under-moderation (failing to remove harmful content targeting specific groups) cause harm.
**Secondary metric:** Statistical parity in moderation action rates across content creators of different demographic backgrounds.
**Trade-off to document:** Dialects, code-switching, and cultural context make content moderation fairness exceptionally difficult. Error rates often vary significantly by language variety.

## Regulatory Mapping

This table maps fairness metrics to regulatory requirements. A check indicates the metric directly supports compliance evidence for the regulation.

| Metric | EU AI Act (High-Risk) | EEOC / Adverse Impact | ECOA / Fair Lending | GDPR Art. 22 | NIST AI RMF |
|---|---|---|---|---|---|
| Statistical Parity | Supports non-discrimination requirement | Primary metric (4/5ths rule) | Monitored for disparate impact | Not directly required | Supports Measure function |
| Equalized Odds | Supports accuracy and robustness requirements | Supports defense against disparate treatment claims | Relevant for error rate analysis | Not directly required | Supports Measure function |
| Equal Opportunity | Supports non-discrimination requirement | Supports disparate impact analysis | Primary metric for approval rate equity | Not directly required | Supports Measure function |
| Predictive Parity | Supports accuracy requirements | Supports business necessity defense | Relevant for risk score consistency | Not directly required | Supports Measure function |
| Calibration by Group | Supports accuracy and robustness requirements | Limited direct relevance | Important for risk-based pricing fairness | Not directly required | Supports Measure function |
| Individual Fairness | Supports transparency and human oversight | Limited direct relevance | Limited direct relevance | Supports right to individual review | Supports Govern function |
| Counterfactual Fairness | Supports non-discrimination requirement | Supports disparate treatment defense | Supports disparate treatment analysis | Supports right to explanation | Supports Map function |
| Treatment Equality | Supports accuracy requirements | Supports error analysis in investigations | Relevant for error balance review | Not directly required | Supports Measure function |

**EU AI Act notes:** High-risk AI systems must demonstrate accuracy, robustness, and non-discrimination. No specific metric is mandated; conformity assessments require evidence of fairness testing using appropriate metrics for the use case. Document metric selection rationale.

**EEOC notes:** The 4/5ths rule (statistical parity ratio >= 0.80) is a screening tool, not a legal standard. Employers can defend disparate impact by demonstrating business necessity. Equalized odds and equal opportunity provide supporting evidence.

**ECOA / Fair Lending notes:** Regulation B prohibits discrimination in credit decisions. Both disparate treatment (intentional) and disparate impact (unintentional) are actionable. Equal opportunity and calibration are most relevant for demonstrating fair outcomes.

**GDPR Article 22 notes:** Grants the right not to be subject to solely automated decisions with legal or significant effects. Requires "meaningful information about the logic involved." Counterfactual explanations and individual fairness metrics support this requirement. Explainability methods (SHAP, LIME) complement the metrics.

**NIST AI RMF notes:** The framework is voluntary and does not mandate specific metrics. It provides a structure (Map, Measure, Manage, Govern) for organizations to select and track appropriate fairness metrics. All metrics in this table can be integrated into the Measure function. The choice of which metrics to track should be documented under the Govern function.
