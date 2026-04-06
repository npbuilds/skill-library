# Responsible Ai — Quick Reference


## Quick Reference

| Metric | Definition | Prioritize When | Key Limitation |
|---|---|---|---|
| Statistical / Demographic Parity | P(Y_hat=1 \| A=0) = P(Y_hat=1 \| A=1) | Selection rates must appear equal (hiring, lending) | Ignores base rate differences; can mandate less qualified selections |
| Equalized Odds | TPR and FPR equal across groups | Errors must be balanced (criminal justice) | Requires labeled ground truth; hard to satisfy simultaneously with calibration |
| Equal Opportunity | TPR equal across groups | Missing positive outcomes is the primary harm | Allows unequal false positive rates |
| Predictive Parity | PPV equal across groups | Trust in positive predictions must be equal | Conflicts with equalized odds when base rates differ |
| Calibration by Group | P(Y=1 \| score=s, A=a) = s for all groups | Scores are used directly for decision thresholds | Compatible with large disparities in selection rates |
| Individual Fairness | d(f(x), f(x')) <= L * d(x, x') | Similar individuals exist and similarity is definable | Requires a task-specific distance metric that is itself value-laden |
| Counterfactual Fairness | Y_hat remains the same in counterfactual world where A differs | Causal reasoning about protected attributes is feasible | Requires a causal model; sensitive to model specification |

## Quick Reference

| Bias Source | How It Enters | Detection Method | Mitigation |
|---|---|---|---|
| **Historical** | Training data reflects past discrimination (e.g., biased hiring decisions) | Compare label distributions across groups; audit data provenance | Relabel, reweight, or collect new unbiased data |
| **Representation** | Protected groups underrepresented in training data | Measure group counts and coverage in feature space | Oversample, collect targeted data, use synthetic augmentation |
| **Measurement** | Proxy variables correlate with protected attributes (e.g., zip code as proxy for race) | Mutual information or correlation analysis between features and protected attributes | Remove proxies, use causal feature selection |
| **Aggregation** | Single model applied to heterogeneous subpopulations | Stratified performance analysis; test for interaction effects | Train separate models or include group-aware features |
| **Evaluation** | Benchmark data does not represent deployment population | Compare benchmark demographics to deployment demographics | Create deployment-representative evaluation sets |
| **Deployment** | System used in contexts it was not designed for | Monitor real-world usage patterns; user feedback analysis | Usage guidelines, hard guardrails, restricted access |

## Quick Reference

| Stage | Pros | Cons |
|---|---|---|
| Pre-processing | Model-agnostic; addresses root cause in data | May reduce data quality; can't fix algorithmic bias |
| In-processing | Directly optimizes for fairness; theoretically principled | Tightly coupled to model; harder to audit |
| Post-processing | Fast; does not require retraining | Treats symptoms not causes; may degrade calibration |

## Quick Reference

| Risk Tier | Examples | Requirements |
|---|---|---|
| Unacceptable | Social scoring, real-time biometric ID in public spaces | Prohibited |
| High-risk | Hiring tools, credit scoring, criminal justice, medical devices | Conformity assessment, risk management system, data governance, human oversight, transparency, accuracy/robustness requirements |
| Limited risk | Chatbots, deepfake generators | Transparency obligations (disclose AI interaction) |
| Minimal risk | Spam filters, AI-enabled games | No specific requirements |

## Quick Reference

| Audience | Method | Output |
|---|---|---|
| ML engineers | SHAP values, feature importance, partial dependence plots | Debug model behavior, identify proxy features |
| Regulators | Model cards, aggregate fairness metrics, counterfactual explanations | Demonstrate compliance, justify design choices |
| End users | Natural language explanations, top contributing factors | Understand and contest individual decisions |

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
