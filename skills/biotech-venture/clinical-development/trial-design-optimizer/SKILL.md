---
name: trial-design-optimizer
description: >
  Generate optimized clinical trial designs given a therapeutic hypothesis, target population,
  and development stage. Incorporates adaptive designs, modern estimand frameworks, and
  synthetic control arm feasibility assessment. Reference when evaluating whether a company's
  trial design maximizes probability of success while minimizing cost and timeline, or when
  designing de novo studies for platform companies.
metadata:
  author: nirav
  version: "1.0"
  parent: clinical-development
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Trial Design Optimizer — Engineering the Experiment That Answers the Right Question

Trial design is where clinical development budgets are won or lost. A well-designed Phase 2 with an adaptive enrichment strategy can deliver the same signal as a conventional Phase 3 at one-third the cost. A poorly designed pivotal trial burns $150-300M and 3-4 years before delivering an uninterpretable result. The physician-scientist's edge in venture is recognizing design flaws that financial analysts cannot see: an inadequate run-in period, a composite endpoint that dilutes signal, a control arm that will be obsolete by readout.

> **Trial-cost benchmarks:** for per-phase / per-patient trial cost and SCA/platform savings, use cost-estimator's `references/development-cost-benchmarks.md` rather than a separate table here.

## ICH E9 R1 Estimand Framework

Every modern trial design begins with the estimand — the precise question the trial is designed to answer. ICH E9 R1 (2019) formalized this into five attributes that must be specified before choosing a statistical method:

| Attribute | Definition | Design Implication |
|---|---|---|
| **Population** | Who is the target patient? | Inclusion/exclusion criteria, enrichment strategy |
| **Treatment** | What treatment regimen? | Dose, duration, combination rules |
| **Endpoint** | What variable is measured? | Primary endpoint selection (see endpoint-selection skill) |
| **Intercurrent events** | What happens that affects interpretation? | Treatment switching, rescue medication, discontinuation |
| **Population-level summary** | What statistical measure? | Mean difference, hazard ratio, responder rate |

The intercurrent events strategy is where most trial designs fail in venture diligence. Five strategies exist:

1. **Treatment policy** — analyze all patients regardless of what happens (ITT). Use when: the real-world question is "what happens if I prescribe this drug?"
2. **Composite** — incorporate the intercurrent event into the endpoint. Use when: discontinuation due to AEs is itself informative.
3. **Hypothetical** — estimate what would have happened without the intercurrent event. Use when: treatment switching confounds OS.
4. **Principal stratum** — analyze only patients who would not experience the intercurrent event. Use when: adherent subpopulations are of interest.
5. **While on treatment** — only measure while patients remain on treatment. Use when: pharmacodynamic endpoints matter.

## Adaptive Design Taxonomy

| Design Type | Mechanism | Best For | Regulatory Acceptance |
|---|---|---|---|
| **Group Sequential** | Pre-planned interim analyses with stopping rules | Efficacy/futility early stopping | Well-accepted; FDA Guidance 2019 |
| **Sample Size Re-estimation (SSR)** | Adjust N at interim based on variance | Uncertain effect size | Accepted if blinded; unblinded SSR requires justification |
| **Adaptive Randomization** | Shift allocation toward better-performing arms | Multi-arm dose-finding | Accepted in Phase 2; less common Phase 3 |
| **Adaptive Enrichment** | Restrict enrollment to responsive subgroup at interim | Biomarker-driven oncology | Increasingly accepted; KEYNOTE-042 model |
| **MAMS (Multi-Arm Multi-Stage)** | Multiple experimental arms, dropping losers at interim stages | Platform trials, dose-finding | Strong precedent (RECOVERY, STAMPEDE) |
| **Bayesian Adaptive** | Continuous updating of posterior probability | Rare disease, pediatric, device | FDA receptive; requires strong prior justification |
| **Platform Trial** | Perpetual protocol, arms added/dropped dynamically | Pandemic response, oncology master protocols | RECOVERY trial validated; I-SPY 2 model |

### Platform Trial Architecture

Platform trials (I-SPY 2, RECOVERY, GBM AGILE) represent the most capital-efficient trial design innovation in a decade:

- **Shared control arm**: 50-70% reduction in control patients needed across arms
- **Bayesian adaptive randomization**: shift enrollment to arms showing signal
- **Seamless Phase 2/3**: graduate arms directly to registration
- **Cost efficiency**: $15-25M per arm vs $50-100M for standalone trials
- **Speed**: 6-12 months to initial signal vs 18-24 months conventional

## Basket, Umbrella, and Master Protocols

| Design | Structure | Example | When to Use |
|---|---|---|---|
| **Basket** | One drug, multiple tumor types sharing a biomarker | Larotrectinib (NTRK+ tumors), vemurafenib (BRAF V600E) | Targeted therapy with tumor-agnostic mechanism |
| **Umbrella** | One disease, multiple biomarker-drug pairs | Lung-MAP (NSCLC), ALCHEMIST | When multiple actionable biomarkers exist in one disease |
| **Platform** | Perpetual protocol, any drug can enter/exit | I-SPY 2 (breast cancer), RECOVERY (COVID-19) | When many candidates need testing efficiently |

## Synthetic Control Arm (SCA) Decision Engine

Synthetic control arms using real-world data (RWD) represent the highest-impact innovation in trial design economics. When appropriate, they can save $100-200M in development costs and accelerate enrollment by 30%.

### SCA Appropriateness Decision Tree

```
START: Is there a well-established standard of care?
  |
  YES --> Is the natural history well-characterized with existing data?
  |         |
  |         YES --> Are primary endpoints objective and measurable in RWD?
  |         |         |
  |         |         YES --> Is the patient population identifiable in RWD sources?
  |         |         |         |
  |         |         |         YES --> SCA FEASIBLE: Proceed to data quality assessment
  |         |         |         NO  --> SCA NOT RECOMMENDED: population matching impossible
  |         |         NO  --> SCA NOT RECOMMENDED: endpoint not capturable in RWD
  |         NO  --> SCA NOT RECOMMENDED: insufficient historical context
  |
  NO --> Is this a single-arm trial in severe/rare disease?
            |
            YES --> SCA STRONGLY RECOMMENDED (FDA/EMA precedent in rare disease)
            NO  --> SCA NOT RECOMMENDED: randomized control required
```

### SCA Data Quality Requirements

| Criterion | Minimum Standard | Gold Standard |
|---|---|---|
| **Sample size** | 2:1 external:treated ratio | 5:1 or greater |
| **Data recency** | Within 5 years of trial enrollment | Concurrent with trial period |
| **Endpoint capture** | Primary endpoint measurable | Primary + key secondaries |
| **Covariate overlap** | Key prognostic factors available | Full propensity score matching |
| **Data source** | Single registry or EHR system | Multiple linked sources (Flatiron, Tempus, Optum) |

### Regulatory Precedent for SCAs

- **Bavencio (avelumab)**: FDA accepted external control for urothelial carcinoma maintenance
- **Zolgensma (onasemnogene)**: SMA natural history as external comparator
- **Blincyto (blinatumomab)**: Historical control for ALL accelerated approval
- **FDA Draft Guidance (2023)**: Framework for using RWD/RWE in regulatory decision-making
- **EMA Qualification**: DARWIN EU platform for population-level RWD studies

### Cost-Benefit Analysis

| Parameter | Traditional RCT | SCA-Augmented Design |
|---|---|---|
| Control arm enrollment | 100% randomized | 0-50% randomized + external |
| Per-patient cost (control) | $40,000-80,000 | $5,000-15,000 (data licensing) |
| Enrollment timeline | 18-36 months | 12-24 months |
| Total savings potential | Baseline | $50-200M depending on indication |
| Regulatory risk | Low | Moderate (mitigated by pre-submission FDA dialogue) |

## Sample Size Estimation Logic

### Key Inputs for Power Calculation

1. **Primary endpoint type**: continuous, binary, time-to-event
2. **Expected effect size**: informed by Phase 2 data, competitor data, or mechanism
3. **Alpha level**: typically 0.025 one-sided (0.05 two-sided)
4. **Power**: 80% (minimum), 90% (preferred for pivotal)
5. **Dropout rate**: 10-30% depending on disease and duration
6. **Interim analysis penalty**: alpha spending function (O'Brien-Fleming, Lan-DeMets)

### Rules of Thumb for Venture Diligence

- If a company claims <200 patients for a pivotal trial in a non-orphan indication, interrogate the assumptions
- Adaptive enrichment can reduce required N by 30-50% but introduces operational complexity
- Time-to-event trials: the number of events, not patients, drives power
- Bayesian designs can achieve equivalent evidence with 20-30% fewer patients but require regulatory pre-agreement

## Structured Output Format

When generating a trial design recommendation, output:

```
TRIAL DESIGN RECOMMENDATION
============================
Therapeutic Hypothesis: [one-sentence hypothesis]
Development Stage: [Phase 1b/2/2b/3]
Target Population: [population definition]

ESTIMAND:
  Population: [target population]
  Treatment: [regimen]
  Endpoint: [primary endpoint]
  Intercurrent Event Strategy: [strategy + rationale]
  Summary Measure: [statistical measure]

RECOMMENDED DESIGN:
  Type: [conventional/adaptive/platform/basket]
  Adaptive Features: [if applicable]
  Estimated N: [sample size with assumptions]
  Control Arm: [active comparator/placebo/synthetic/external]
  Key Interim Analyses: [timing and decision rules]

SYNTHETIC CONTROL ASSESSMENT:
  Feasibility: [feasible/not recommended]
  Rationale: [3-4 sentences]
  Potential Savings: [$X-YM]
  Regulatory Risk: [low/moderate/high]

DESIGN RISKS:
  1. [Risk + mitigation]
  2. [Risk + mitigation]
  3. [Risk + mitigation]

TIMELINE ESTIMATE: [months to primary endpoint readout]
BUDGET ESTIMATE: [range based on design parameters]
```

## Cross-Domain Connections

- **Biotech-venture/endpoint-selection**: Endpoint choice drives trial design parameters — an OS endpoint requires fundamentally different design than a surrogate
- **Biotech-venture/biomarker-enrichment**: Enrichment strategies affect design complexity, adding adaptive elements and modifying sample size requirements
- **Biotech-venture/cost-estimator**: Trial design directly determines development costs — adaptive designs, platform trials, and SCAs each have distinct cost profiles
- **Research/spelunker**: Deep research on regulatory precedent for novel trial designs, synthetic control arm acceptance, and adaptive methodology
