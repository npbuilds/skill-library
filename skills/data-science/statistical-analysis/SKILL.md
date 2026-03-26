---
name: statistical-analysis
description: >
  Direct the statistical analysis subdomain — route inference questions to the right specialist
  skill, define the learning curriculum, and resolve conflicts between analytical frameworks.
  Use when the user needs hypothesis testing, causal inference, survival analysis, clinical
  trial design, or any question requiring rigorous statistical reasoning.
tools: Read, Glob
---

# Statistical Analysis Director

The department head for statistical inference within the data-science domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between frequentist and causal frameworks.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

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

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `statistical-testing` — establish whether the effect exists and quantify uncertainty
2. `causal-inference` — determine whether the association is causal and identify the mechanism
3. `biostatistics` — apply domain-specific methodology for clinical/biological contexts

This order ensures we first confirm the signal is real, then determine causality, then apply specialized methods.

**Example multi-skill question**: "Did our new drug reduce 30-day mortality compared to standard of care?"
1. `statistical-testing` → test for significant difference in mortality rates, compute confidence intervals
2. `causal-inference` → assess whether the trial design supports causal claims (randomization quality, confounders)
3. `biostatistics` → survival analysis with Kaplan-Meier curves and Cox proportional hazards, regulatory-grade reporting

## Curriculum Order

For learning or progressive loading:

1. **Statistical Testing** (foundation) — The language of inference. Every other statistical method assumes you understand p-values, confidence intervals, power, and the logic of hypothesis testing. Without this, causal and biostatistical methods are opaque.

2. **Causal Inference** (extension) — Addresses the question statistical testing leaves open: "is it causal?" Builds on testing by adding identification strategies that distinguish association from causation.

3. **Biostatistics** (specialization) — Domain-specific methods for clinical and biological data. Requires both testing and causal foundations. Adds survival analysis, clinical trial design, regulatory requirements, and meta-analysis.

### Level Progression
- **Foundational**: Statistical Testing, Causal Inference
- **Intermediate**: Biostatistics
- **Advanced**: (not yet built) Bayesian Inference, Nonparametric Methods, Sequential Analysis

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| statistical-testing says "significant" but causal-inference says "no causal claim possible" | Causal inference wins — report as association, not causation | Statistical significance ≠ causal evidence; identification strategy determines whether causal language is warranted |
| causal-inference recommends an IV approach but biostatistics says the clinical context violates the exclusion restriction | Biostatistics wins on domain knowledge | Domain expertise constrains method choice; a technically valid method can fail in context |
| statistical-testing says "not significant" but effect size is clinically meaningful | Report both — statistical significance ≠ practical significance | Underpowered studies can miss real effects; effect size and confidence interval matter more than p-value alone |
| biostatistics recommends survival analysis but causal-inference prefers diff-in-diff | Depends on the question — survival analysis for time-to-event, diff-in-diff for policy evaluation | Match the method to the estimand, not the data structure |

**General rule**: Causal reasoning > statistical significance > convention. When frameworks disagree, present both with the assumptions that drive the disagreement. Never let a p-value alone drive a conclusion.

## Scope Boundaries

**This director handles**: All statistical inference questions — hypothesis testing, power analysis, causal identification, survival analysis, clinical trial design, meta-analysis, epidemiological measures.

**Escalate to the orchestrator when**:
- The question requires data cleaning or feature engineering before analysis can begin (Data Wrangling)
- The question requires building a predictive model, not just testing hypotheses (Modeling)
- The question requires visualizing results for communication (Visualization)
- The question involves model fairness or bias assessment (Frontier)
- The question spans multiple subdomains and needs orchestrator-level coordination
