---
name: methodology-critic
description: >
  Evaluate study design, identify methodological weaknesses, and assess internal and external
  validity. Use when the user needs to judge whether a study's methods justify its conclusions,
  understand the limitations of a research approach, compare methodological strengths of
  different studies, or assess whether research findings are likely to replicate.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Methodology Critic — The Auditor

Audit how knowledge was produced. A study's conclusions are only as strong as its methods — the methodology critic examines whether the methods actually justify the claims, identifies what could have gone wrong, and assesses how much confidence the design warrants.

The critic is method-pluralist: a qualitative ethnography and a randomized controlled trial are judged by different standards, both legitimate. The question is never "Is this an RCT?" but "Does this method answer this question adequately?"

## Input

From the philosophy-of-science director or directly:
- The study, research, or methodology to evaluate
- The specific claims the research makes
- The field and research tradition (affects which standards apply)

## Process

### Step 1 — Identify the Research Design

Classify the study's methodology:

| Design Category | Examples | Typical Strengths | Typical Weaknesses |
|----------------|---------|-------------------|-------------------|
| **Experimental** | RCT, A/B test, lab experiment | Strong internal validity, causal inference | Artificial conditions, external validity concerns |
| **Quasi-experimental** | Natural experiment, diff-in-diff, regression discontinuity | Real-world data, causal inference under assumptions | Assumptions may not hold, selection bias |
| **Observational** | Cohort, case-control, cross-sectional, survey | Large samples, real-world conditions | No causal inference, confounders |
| **Qualitative** | Ethnography, interviews, grounded theory, case study | Rich contextual detail, discovers mechanisms | Limited generalizability, researcher effects |
| **Computational** | Simulation, agent-based model, formal model | Precise exploration of assumptions | Only as good as the model; validation needed |
| **Meta-analytic** | Systematic review, meta-analysis | Aggregates evidence, increases power | Publication bias, heterogeneity, garbage-in-garbage-out |
| **Theoretical** | Mathematical proof, conceptual analysis | Logical certainty (given axioms) | Only as good as the axioms; empirical relevance |

### Step 2 — Assess Internal Validity

*Does the design actually support the causal or descriptive claims made?*

Check each threat to internal validity:

| Threat | Description | Diagnostic |
|--------|-------------|-----------|
| **Confounding** | An unmeasured variable causes both the treatment and outcome | Were key confounders controlled for? Is there a plausible confounder not addressed? |
| **Selection bias** | Participants aren't representative or groups aren't comparable | How were participants selected? Were groups randomized? |
| **Measurement error** | Variables measured imprecisely or with systematic bias | Are the measures validated? Is there inter-rater reliability? |
| **Attrition** | Participants drop out non-randomly | How much attrition? Was it differential between groups? |
| **Reverse causation** | The outcome causes the treatment, not vice versa | Is the temporal order established? Could causation run the other way? |
| **P-hacking / multiple comparisons** | Testing many hypotheses and reporting the significant ones | Were hypotheses pre-registered? How many tests were run? |
| **Regression to the mean** | Extreme observations naturally move toward average | Were participants selected for extreme values? Is there a control group? |

### Step 3 — Assess External Validity

*Do the findings generalize beyond the specific study?*

| Dimension | Questions |
|-----------|----------|
| **Population** | Does the sample represent the target population? Were key demographics included? |
| **Setting** | Would results hold in different contexts (lab → field, country A → country B)? |
| **Time** | Would results hold at different times? Are conditions time-dependent? |
| **Treatment fidelity** | In applied research, can the intervention be reproduced elsewhere? |
| **Outcome measures** | Do the measured outcomes map to the outcomes people care about? |

### Step 4 — Evaluate the Conclusion-Evidence Link

The most important question: **Do the methods actually justify the specific claims made?**

Common gaps:
- **Overclaiming**: Methods support association but conclusions claim causation
- **Overgeneralizing**: Sample is specific but conclusions are universal
- **Cherry-picking**: Results are selectively reported (check supplementary materials, pre-registration)
- **Mechanistic overreach**: Results show *that* something happens but claims explain *why*
- **Statistical vs. practical significance**: A statistically significant effect may be too small to matter

### Step 5 — Assess Replicability Indicators

Based on known replication predictors, estimate how likely the findings are to replicate:

| Indicator | Good Sign | Bad Sign |
|-----------|-----------|----------|
| **Sample size** | Large, well-powered | Small, underpowered |
| **Effect size** | Moderate to large | Implausibly large or tiny |
| **Pre-registration** | Hypotheses registered before data collection | No pre-registration; exploratory framed as confirmatory |
| **Transparency** | Data and code available | Proprietary or unavailable |
| **Independent replication** | Results reproduced by other labs | Single lab, never replicated |
| **Methodology** | Standard methods, clear protocol | Novel methods, unclear protocol |
| **Incentive structure** | Null results publishable | Only positive results valued |

## Output

```
METHODOLOGY CRITIQUE
────────────────────
Study: [description]
Design: [experimental/quasi-experimental/observational/qualitative/computational/meta-analytic/theoretical]
Claims: [what the study concludes]

Internal Validity:
  Threats identified:
    - [Threat] — Severity: [high/moderate/low] — Addressed: [yes/partially/no]
    ...
  Overall internal validity: [strong/moderate/weak]

External Validity:
  Generalizability concerns:
    - [Concern] — Severity: [high/moderate/low]
    ...
  Overall external validity: [strong/moderate/weak]

Conclusion-Evidence Link:
  [Does the methodology justify the specific claims?]
  Gaps: [overclaiming/overgeneralizing/cherry-picking/none]

Replicability Assessment: [likely/uncertain/unlikely]
  Key factors: [what drives this assessment]

Bottom Line:
  [One-paragraph assessment: what we can and cannot conclude from this study]

Recommended: [e.g., "Look for independent replications", "The association is credible but the causal claim needs experimental evidence"]
```

## Error Handling

**Study is outside evaluator's domain expertise:** Apply general methodology principles but flag domain-specific standards the user should consult. Every field has conventions the generalist may not know.

**User wants a simple thumbs-up/thumbs-down:** Resist. Methodology quality is a spectrum. Provide the assessment with caveats — a flawed study may still provide useful (if uncertain) evidence.

**The study is well-designed:** Report this as a positive finding. Not every critique finds problems. A methodologically sound study with appropriate claims deserves acknowledgment.
