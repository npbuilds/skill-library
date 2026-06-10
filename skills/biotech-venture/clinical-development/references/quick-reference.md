# Clinical Development — Quick Reference


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

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Endpoint selection favors a surrogate but trial design recommends powering for OS | endpoint-selection leads if there is regulatory precedent for the surrogate; trial-design-optimizer leads if the indication lacks surrogate acceptance | Regulatory precedent is the binding constraint. If FDA has accepted the surrogate in prior approvals, use it. If not, powering for OS is safer despite longer timelines. |
| Biomarker enrichment improves effect size but patient-population-sizer shows enrollment becomes infeasible | Quantify the tradeoff explicitly — compare total patients needed (enriched vs all-comers) and enrollment duration | Often enrichment reduces total patients needed despite a smaller eligible pool. If the math does not work, consider a biomarker-stratified (not enriched) design. |
| Trial design recommends adaptive but endpoint selection shows the endpoint requires fixed-duration follow-up | endpoint-selection takes priority — the regulatory endpoint constrains the design, not the reverse | An adaptive design with a time-to-event endpoint works differently than one with a fixed-timepoint responder endpoint. The endpoint dictates which adaptive elements are feasible. |
