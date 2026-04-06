# Methodology Critic — Quick Reference


## Quick Reference

| Design Category | Examples | Typical Strengths | Typical Weaknesses |
|----------------|---------|-------------------|-------------------|
| **Experimental** | RCT, A/B test, lab experiment | Strong internal validity, causal inference | Artificial conditions, external validity concerns |
| **Quasi-experimental** | Natural experiment, diff-in-diff, regression discontinuity | Real-world data, causal inference under assumptions | Assumptions may not hold, selection bias |
| **Observational** | Cohort, case-control, cross-sectional, survey | Large samples, real-world conditions | No causal inference, confounders |
| **Qualitative** | Ethnography, interviews, grounded theory, case study | Rich contextual detail, discovers mechanisms | Limited generalizability, researcher effects |
| **Computational** | Simulation, agent-based model, formal model | Precise exploration of assumptions | Only as good as the model; validation needed |
| **Meta-analytic** | Systematic review, meta-analysis | Aggregates evidence, increases power | Publication bias, heterogeneity, garbage-in-garbage-out |
| **Theoretical** | Mathematical proof, conceptual analysis | Logical certainty (given axioms) | Only as good as the axioms; empirical relevance |

## Quick Reference

| Threat | Description | Diagnostic |
|--------|-------------|-----------|
| **Confounding** | An unmeasured variable causes both the treatment and outcome | Were key confounders controlled for? Is there a plausible confounder not addressed? |
| **Selection bias** | Participants aren't representative or groups aren't comparable | How were participants selected? Were groups randomized? |
| **Measurement error** | Variables measured imprecisely or with systematic bias | Are the measures validated? Is there inter-rater reliability? |
| **Attrition** | Participants drop out non-randomly | How much attrition? Was it differential between groups? |
| **Reverse causation** | The outcome causes the treatment, not vice versa | Is the temporal order established? Could causation run the other way? |
| **P-hacking / multiple comparisons** | Testing many hypotheses and reporting the significant ones | Were hypotheses pre-registered? How many tests were run? |
| **Regression to the mean** | Extreme observations naturally move toward average | Were participants selected for extreme values? Is there a control group? |

## Quick Reference

| Dimension | Questions |
|-----------|----------|
| **Population** | Does the sample represent the target population? Were key demographics included? |
| **Setting** | Would results hold in different contexts (lab → field, country A → country B)? |
| **Time** | Would results hold at different times? Are conditions time-dependent? |
| **Treatment fidelity** | In applied research, can the intervention be reproduced elsewhere? |
| **Outcome measures** | Do the measured outcomes map to the outcomes people care about? |

## Quick Reference

| Indicator | Good Sign | Bad Sign |
|-----------|-----------|----------|
| **Sample size** | Large, well-powered | Small, underpowered |
| **Effect size** | Moderate to large | Implausibly large or tiny |
| **Pre-registration** | Hypotheses registered before data collection | No pre-registration; exploratory framed as confirmatory |
| **Transparency** | Data and code available | Proprietary or unavailable |
| **Independent replication** | Results reproduced by other labs | Single lab, never replicated |
| **Methodology** | Standard methods, clear protocol | Novel methods, unclear protocol |
| **Incentive structure** | Null results publishable | Only positive results valued |
