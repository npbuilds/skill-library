---
name: clinical-development
description: >
  Direct clinical trial design, endpoint selection, biomarker enrichment, and patient population
  sizing questions to the appropriate specialist skill. Activate when evaluating a clinical program's
  design choices, adaptive strategies, synthetic control arms, or enrollment feasibility. The clinical
  data package is the product in biotech — this director ensures every design question gets rigorous,
  quantitative analysis.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Clinical Development Director

Clinical development is where biotech value is created or destroyed. A well-designed trial with the right endpoint, enriched patient population, and robust biomarker strategy can turn a marginal molecule into a blockbuster approval. A poorly designed trial can kill a genuinely effective drug. This director routes clinical program questions to the right specialist and sequences multi-skill analyses so that each decision builds on the one before it.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| trial-design-optimizer | action | Designing or critiquing a trial protocol — adaptive designs, randomization schemes, control arm selection, sample size justification, interim analysis plans |
| endpoint-selection | knowledge | Choosing primary/secondary/exploratory endpoints, understanding regulatory endpoint precedent by indication, surrogate vs clinical endpoints, composite endpoints |
| biomarker-enrichment | action | Designing biomarker-driven enrollment strategies, predictive vs prognostic biomarker analysis, companion diagnostic requirements, subgroup pre-specification |
| patient-population-sizer | action | Estimating addressable patient populations, prevalence/incidence modeling, screen failure rate estimation, enrollment feasibility by geography |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Trial design, protocol, adaptive, randomization, control arm, sample size, interim analysis | trial-design-optimizer | "Should this be an adaptive design?" / "What sample size do we need for 90% power?" |
| Endpoint, primary endpoint, surrogate, composite endpoint, clinical outcome, OS vs PFS | endpoint-selection | "Is PFS an acceptable primary endpoint in this indication?" / "Should we use a composite endpoint?" |
| Biomarker, enrichment, companion diagnostic, predictive biomarker, subgroup, patient selection | biomarker-enrichment | "Should we enrich for biomarker-positive patients?" / "What CDx strategy makes sense here?" |
| Patient population, prevalence, incidence, addressable patients, enrollment, screen failure | patient-population-sizer | "How many patients can we realistically enroll?" / "What is the addressable population for this rare disease?" |
| Trial design + endpoint together | trial-design-optimizer then endpoint-selection | "Design a registrational trial for this asset" |
| Biomarker + population together | biomarker-enrichment then patient-population-sizer | "If we enrich for HER2-low, what does that do to our enrollment timeline?" |
| Full clinical program review | All four in sequence | "Evaluate this Phase 3 protocol" |

## Multi-Skill Questions

Most clinical development questions span multiple children. Common combinations:

1. **Trial Design + Endpoint**: "What is the optimal registrational strategy for this asset?"
   - Load endpoint-selection first to establish regulatory precedent for acceptable endpoints in the indication
   - Then load trial-design-optimizer to build the protocol around the chosen endpoint
   - Synthesize: The endpoint drives the design. An OS endpoint requires a larger, longer trial than a surrogate. An adaptive design may allow a surrogate-to-OS transition.

2. **Biomarker + Population**: "Should we enrich, and what does that do to feasibility?"
   - Load biomarker-enrichment to assess whether a predictive biomarker exists and what enrichment ratio is achievable
   - Then load patient-population-sizer to model the impact on addressable population and enrollment timelines
   - Synthesize: Enrichment increases effect size but shrinks the denominator. The net impact on sample size and enrollment duration determines whether enrichment is operationally viable.

3. **Full Protocol Review**: "Critique this Phase 3 design"
   - Sequence all four: endpoint-selection (is the endpoint right?) then trial-design-optimizer (is the design right?) then biomarker-enrichment (is patient selection right?) then patient-population-sizer (is enrollment feasible?)
   - Each analysis feeds the next. Endpoint choice constrains design. Design constrains biomarker strategy. Biomarker strategy constrains population size.

## Curriculum Order

1. **endpoint-selection** — Foundation. You cannot design a trial until you know what you are measuring. Endpoint literacy is the prerequisite for everything else.
2. **trial-design-optimizer** — Second. Once the endpoint is chosen, the trial design follows. Adaptive designs, randomization, control arms, interim analyses — all depend on the endpoint.
3. **biomarker-enrichment** — Third. Enrichment is a design modifier. It changes who enters the trial and how the treatment effect manifests. Requires understanding of trial design to appreciate the tradeoffs.
4. **patient-population-sizer** — Fourth. Population sizing is the operational reality check. It takes the designed trial and asks: can we actually run this? Requires all prior skills as inputs.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Endpoint selection favors a surrogate but trial design recommends powering for OS | endpoint-selection leads if there is regulatory precedent for the surrogate; trial-design-optimizer leads if the indication lacks surrogate acceptance | Regulatory precedent is the binding constraint. If FDA has accepted the surrogate in prior approvals, use it. If not, powering for OS is safer despite longer timelines. |
| Biomarker enrichment improves effect size but patient-population-sizer shows enrollment becomes infeasible | Quantify the tradeoff explicitly — compare total patients needed (enriched vs all-comers) and enrollment duration | Often enrichment reduces total patients needed despite a smaller eligible pool. If the math does not work, consider a biomarker-stratified (not enriched) design. |
| Trial design recommends adaptive but endpoint selection shows the endpoint requires fixed-duration follow-up | endpoint-selection takes priority — the regulatory endpoint constrains the design, not the reverse | An adaptive design with a time-to-event endpoint works differently than one with a fixed-timepoint responder endpoint. The endpoint dictates which adaptive elements are feasible. |

## Scope Boundaries

**This director handles**: All questions about clinical trial design, protocol optimization, endpoint selection, biomarker enrichment strategy, patient population sizing, enrollment feasibility, adaptive trial methodology, and clinical development strategy for therapeutic assets.

**Route to Asclepius when**:
- The question requires translating clinical design into probability of success (route to probability-of-success)
- The question involves regulatory pathway strategy beyond endpoint precedent (route to regulatory-strategy)
- The question involves competitive differentiation based on clinical design choices (route to competitive-intelligence)
- The question requires cost estimation for the clinical program (route to asset-valuation)
- The question spans multiple diligence pillars and needs orchestrator-level coordination

## Cross-Domain Connections

- **Biotech-venture/endpoint-selection, trial-design-optimizer, biomarker-enrichment, patient-population-sizer**: Child skills that execute specialist clinical development analyses
- **Data-science/statistical-testing**: Biomarker enrichment power calculations and sample size estimation rely on statistical testing foundations
- **Research/spelunker**: Deep research on clinical trial design precedent, regulatory endpoint acceptance history, and adaptive design methodology
