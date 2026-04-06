---
name: responsible-ai
description: >
  Responsible AI governance, fairness metrics, and bias mitigation for ML systems. Reference
  when auditing models for fairness, selecting appropriate fairness criteria, implementing
  bias mitigation strategies, creating model cards, or ensuring compliance with AI governance
  frameworks like the EU AI Act or NIST AI RMF. Use when any model affects human decisions.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Responsible AI — The Conscience

Responsible AI is no longer aspirational — it is a regulatory requirement, a litigation risk, and a business differentiator. The EU AI Act imposes fines up to 7% of global revenue. US agencies (EEOC, CFPB, FTC) actively investigate algorithmic discrimination. Organizations that treat fairness as an afterthought face enforcement actions, reputational damage, and models that silently harm the people they claim to serve. This skill provides the decision frameworks, metrics, and workflows needed to build ML systems that are fair, transparent, and accountable.

## 1. Fairness Definitions

Fairness is not a single property. It is a family of competing mathematical criteria, and choosing among them is a values decision, not a technical one.

**Group fairness** asks whether outcomes are distributed equitably across protected groups. **Individual fairness** asks whether similar people receive similar predictions. **Counterfactual fairness** asks whether a prediction would change if a person's protected attribute were different.

| Metric | Definition | Prioritize When | Key Limitation |
|---|---|---|---|
| Statistical / Demographic Parity | P(Y_hat=1 \| A=0) = P(Y_hat=1 \| A=1) | Selection rates must appear equal (hiring, lending) | Ignores base rate differences; can mandate less qualified selections |
| Equalized Odds | TPR and FPR equal across groups | Errors must be balanced (criminal justice) | Requires labeled ground truth; hard to satisfy simultaneously with calibration |
| Equal Opportunity | TPR equal across groups | Missing positive outcomes is the primary harm | Allows unequal false positive rates |
| Predictive Parity | PPV equal across groups | Trust in positive predictions must be equal | Conflicts with equalized odds when base rates differ |
| Calibration by Group | P(Y=1 \| score=s, A=a) = s for all groups | Scores are used directly for decision thresholds | Compatible with large disparities in selection rates |
| Individual Fairness | d(f(x), f(x')) <= L * d(x, x') | Similar individuals exist and similarity is definable | Requires a task-specific distance metric that is itself value-laden |
| Counterfactual Fairness | Y_hat remains the same in counterfactual world where A differs | Causal reasoning about protected attributes is feasible | Requires a causal model; sensitive to model specification |

**The impossibility theorem.** Chouldechova (2017) and Kleinberg et al. (2016) proved that when base rates differ between groups, you cannot simultaneously satisfy calibration, equalized odds, and predictive parity — except in trivial cases (perfect prediction or equal base rates). This means every deployment involves a fairness trade-off. Document the trade-off explicitly. Do not pretend it does not exist.

## 2. Bias Sources

Bias enters ML systems at every stage. Identifying the source determines the mitigation.

| Bias Source | How It Enters | Detection Method | Mitigation |
|---|---|---|---|
| **Historical** | Training data reflects past discrimination (e.g., biased hiring decisions) | Compare label distributions across groups; audit data provenance | Relabel, reweight, or collect new unbiased data |
| **Representation** | Protected groups underrepresented in training data | Measure group counts and coverage in feature space | Oversample, collect targeted data, use synthetic augmentation |
| **Measurement** | Proxy variables correlate with protected attributes (e.g., zip code as proxy for race) | Mutual information or correlation analysis between features and protected attributes | Remove proxies, use causal feature selection |
| **Aggregation** | Single model applied to heterogeneous subpopulations | Stratified performance analysis; test for interaction effects | Train separate models or include group-aware features |
| **Evaluation** | Benchmark data does not represent deployment population | Compare benchmark demographics to deployment demographics | Create deployment-representative evaluation sets |
| **Deployment** | System used in contexts it was not designed for | Monitor real-world usage patterns; user feedback analysis | Usage guidelines, hard guardrails, restricted access |

## 3. Bias Mitigation Strategies

Mitigation operates at three stages. Use multiple stages for defense in depth.

**Pre-processing** — Modify the data before training.
- *Resampling*: Oversample underrepresented groups or undersample overrepresented ones. Simple but can cause overfitting or information loss.
- *Reweighting*: Assign higher sample weights to disadvantaged groups. Preserves all data but shifts the learned distribution.
- *Representation learning*: Learn fair embeddings that remove protected attribute information (e.g., adversarial representation learning). Powerful but adds model complexity.

**In-processing** — Modify the learning algorithm.
- *Adversarial debiasing*: Train a predictor and an adversary simultaneously; the adversary tries to predict the protected attribute from predictions. The predictor learns to be accurate while the adversary fails.
- *Fairness constraints*: Add fairness metrics as constraints or regularization terms to the loss function. Directly targets the chosen fairness definition.
- *Exponentiated gradient / reduction approaches*: Reduce fair classification to a sequence of cost-sensitive classification problems (Agarwal et al. 2018).

**Post-processing** — Modify predictions after training.
- *Threshold adjustment*: Use different classification thresholds per group to equalize a chosen metric. Fast to implement but can feel like a patch.
- *Calibration by group*: Recalibrate predicted probabilities within each group using isotonic regression or Platt scaling. Preserves model internals.

| Stage | Pros | Cons |
|---|---|---|
| Pre-processing | Model-agnostic; addresses root cause in data | May reduce data quality; can't fix algorithmic bias |
| In-processing | Directly optimizes for fairness; theoretically principled | Tightly coupled to model; harder to audit |
| Post-processing | Fast; does not require retraining | Treats symptoms not causes; may degrade calibration |

## 4. Governance Frameworks

**EU AI Act** classifies AI systems into four risk tiers:

| Risk Tier | Examples | Requirements |
|---|---|---|
| Unacceptable | Social scoring, real-time biometric ID in public spaces | Prohibited |
| High-risk | Hiring tools, credit scoring, criminal justice, medical devices | Conformity assessment, risk management system, data governance, human oversight, transparency, accuracy/robustness requirements |
| Limited risk | Chatbots, deepfake generators | Transparency obligations (disclose AI interaction) |
| Minimal risk | Spam filters, AI-enabled games | No specific requirements |

**NIST AI RMF** provides four functions: **Map** (context and risk identification), **Measure** (quantify risks with metrics), **Manage** (prioritize and act on risks), **Govern** (organizational policies, roles, culture).

**High-risk AI compliance checklist:**
- [ ] Risk management system documented and maintained
- [ ] Training data governance: provenance, quality, representativeness assessed
- [ ] Fairness metrics selected, measured, and thresholds defined
- [ ] Human oversight mechanism in place (human-in-the-loop or human-on-the-loop)
- [ ] Technical documentation and model card completed
- [ ] Logging and audit trail enabled
- [ ] Post-deployment monitoring plan with drift and fairness tracking
- [ ] Incident response procedure for detected bias

## 5. Model Cards & Documentation

A **model card** (Mitchell et al. 2019) is a standardized document that accompanies a trained model.

**Template sections:**
1. **Model details** — Architecture, version, owner, date, license.
2. **Intended use** — Primary use cases. Out-of-scope uses explicitly listed.
3. **Training data** — Source, size, collection methodology, known gaps.
4. **Evaluation data** — How evaluation set was constructed; demographic breakdown.
5. **Metrics** — Performance metrics overall and disaggregated by protected group.
6. **Ethical considerations** — Sensitive use cases, potential harms, fairness trade-offs chosen.
7. **Caveats and limitations** — Known failure modes, populations where performance degrades.

**Datasheets for datasets** (Gebru et al. 2021) apply the same principle to training data: motivation, composition, collection process, preprocessing, distribution, and maintenance.

Create model cards for any model that affects human decisions. Create datasheets for any dataset used to train such models. These are living documents — update them when models are retrained or deployment contexts change.

## 6. Transparency & Explainability

Stakeholders need different levels of explanation.

| Audience | Method | Output |
|---|---|---|
| ML engineers | SHAP values, feature importance, partial dependence plots | Debug model behavior, identify proxy features |
| Regulators | Model cards, aggregate fairness metrics, counterfactual explanations | Demonstrate compliance, justify design choices |
| End users | Natural language explanations, top contributing factors | Understand and contest individual decisions |

**Key methods:**
- **SHAP** (SHapley Additive exPlanations): Game-theoretic attribution of each feature's contribution. Consistent and theoretically grounded. Computationally expensive for large models.
- **LIME** (Local Interpretable Model-agnostic Explanations): Fits an interpretable model locally around a prediction. Fast but unstable across perturbations.
- **Counterfactual explanations**: Show the smallest change to inputs that would flip the decision. Highly intuitive for end users ("If your income were $5K higher, the loan would be approved").
- **Attention visualization**: For transformer models, visualize attention weights. Useful for debugging but attention does not always equal importance.

GDPR Article 22 grants individuals the right not to be subject to decisions based solely on automated processing. While the exact scope of the "right to explanation" is debated, providing meaningful information about the logic involved is a practical necessity.

## 7. Audit Workflow

A structured audit prevents ad hoc fairness checks that miss systemic issues.

**Step-by-step process:**

1. **Define protected attributes** — Identify legally protected characteristics relevant to the domain (race, sex, age, disability, etc.). Consult legal counsel on jurisdiction-specific requirements.
2. **Select fairness metrics** — Choose 2-3 metrics aligned with the harm model. Use the domain guide in `references/fairness-metrics.md`. Document why each metric was chosen and what trade-offs were accepted.
3. **Measure baseline** — Compute chosen metrics on the current model using a representative evaluation set disaggregated by protected group.
4. **Test for statistical significance** — Use bootstrap confidence intervals or permutation tests. Small group sizes require careful statistical treatment. A disparity that is not statistically significant may still matter if the affected group is small.
5. **Mitigate if needed** — Apply pre-processing, in-processing, or post-processing techniques. Re-measure. Iterate.
6. **Document** — Complete a model card. Record all metrics, thresholds, trade-off decisions, and mitigation steps taken.
7. **Monitor ongoing** — Deploy fairness dashboards that track metrics over time. Set alerts for metric drift. Re-audit on a fixed schedule (quarterly for high-risk systems) and after any retraining.

**Audit checklist:**
- [ ] Protected attributes defined with legal review
- [ ] Fairness metrics selected with documented rationale
- [ ] Baseline metrics computed and disaggregated
- [ ] Statistical significance assessed
- [ ] Intersectional analysis performed (e.g., race x gender)
- [ ] Mitigation applied and re-measured
- [ ] Model card completed
- [ ] Monitoring dashboard deployed
- [ ] Re-audit schedule established

## Common Mistakes

1. **Optimizing for a single fairness metric and ignoring trade-offs.** The impossibility theorem guarantees conflicts. Document which metric you prioritize and why — do not pretend you satisfy all of them.
2. **Treating fairness as a one-time check.** Data drift, population shifts, and feedback loops cause fairness to degrade over time. Continuous monitoring is mandatory, not optional.
3. **Removing protected attributes and assuming the model is fair.** Proxy variables (zip code, name, school) carry protected attribute information. Removing the attribute itself rarely eliminates bias.
4. **Using overall accuracy as evidence of fairness.** A model can be 95% accurate overall while having a 70% false positive rate for a minority group. Always disaggregate metrics.
5. **Skipping intersectional analysis.** A model may be fair across race and fair across gender but unfair for Black women specifically. Test subgroup intersections.
6. **Confusing explanation with justification.** SHAP values explain what a model does; they do not prove the model is fair or ethical. Explainability is necessary but not sufficient.

## Implementation Libraries

| Task | Python | R |
|------|--------|---|
| Fairness metrics, bias mitigation, dashboards | `fairlearn` (Microsoft) | `fairness` |
| Comprehensive bias detection and mitigation | `aif360` (IBM) | — |
| Bias audit toolkit | `aequitas` | — |
| SHAP values (feature attribution) | `shap` | `shapr`, `fastshap` |
| LIME (local interpretable explanations) | `lime` | `lime` |
| Interpretable ML, glass-box models (EBM) | `interpret` (InterpretML) | `iml` |
| Model-agnostic explanations (counterfactual, anchors) | `alibi` (Alibi Explain) | — |
| Partial dependence, feature interaction | `sklearn.inspection` | `pdp`, `iml` |
| Model cards generation | `model-card-toolkit` (Google) | — |
| Causal fairness, counterfactual reasoning | `dowhy` | — |

**Recommended starting stack (Python):** `fairlearn` for fairness metrics and mitigation + `shap` for feature attribution + `interpret` for glass-box models and unified explanations. Add `aequitas` for automated bias audits.

## When This Applies

- Any model whose output influences decisions about people: hiring, lending, insurance, criminal justice, healthcare, education, content moderation, advertising
- Models subject to regulatory oversight (EU AI Act high-risk, US ECOA/FCRA, sector-specific regulations)
- Models deployed in contexts where errors have asymmetric consequences across demographic groups
- Any system where users or affected individuals have a right to explanation or contest decisions
- Internal models that affect employee evaluations, resource allocation, or access to opportunities

If a model affects human outcomes, this skill applies. When in doubt, audit anyway — the cost of a false positive (unnecessary audit) is far lower than the cost of a false negative (undetected discrimination).

See `references/fairness-metrics.md` for detailed metric definitions, impossibility proofs, domain selection guides, and regulatory mappings.
