# Probability Of Success — Quick Reference


## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| pos-calculator | action | Computing cumulative PoS from phase-specific transition probabilities, building PoS waterfalls, sensitivity analysis on PoS assumptions, back-calculating implied PoS from market cap |
| pos-base-rates | knowledge | Looking up empirical phase transition rates by indication, modality, endpoint type, line of therapy, and biomarker status from BIO/Informa and similar datasets |
| mechanism-risk-adjuster | action | Adjusting base-rate PoS for program-specific factors — target validation strength, preclinical data quality, clinical signal magnitude, competitive readthrough, and prior failures on the same target |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Calculate PoS, cumulative probability, PoS waterfall, phase transition probability, implied PoS | pos-calculator | "What is the cumulative PoS for this Phase 2 oncology asset?" / "What PoS is the market implying at this valuation?" |
| Base rate, historical approval rate, indication-specific PoS, phase success rate, BIO data | pos-base-rates | "What is the Phase 2 to Phase 3 transition rate for NASH?" / "How does oncology PoS compare to rare disease?" |
| Target validation, mechanism risk, preclinical evidence, genetic evidence, prior failures, competitive readthrough | mechanism-risk-adjuster | "This target has failed twice before — how should I adjust PoS?" / "There is strong Mendelian randomization evidence — what uplift does that give?" |
| Full PoS assessment | pos-base-rates then mechanism-risk-adjuster then pos-calculator | "Give me a full PoS estimate for this asset" |
| Implied PoS vs estimated PoS comparison | pos-calculator (twice — once for implied, once for estimated) | "Is the market pricing this asset correctly on a PoS basis?" |

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Base rate is low but mechanism-risk-adjuster gives strong uplift (e.g., genetic validation on a historically difficult indication) | Cap the adjusted PoS at 2-3x the base rate unless there is truly exceptional evidence; clearly state the adjustment magnitude and rationale | Even strong genetic validation cannot overcome all sources of clinical failure (safety, formulation, dosing). Uncapped adjustments lead to overconfidence. |
| Mechanism-risk-adjuster says "reduce PoS due to prior target failures" but the current program has a differentiated mechanism of action | Assess whether the prior failures were mechanism-related or execution-related; adjust accordingly | If prior failures were due to the target itself (biology wrong), reduce PoS significantly. If prior failures were due to trial design, dosing, or patient selection (execution wrong), a differentiated approach may genuinely have higher PoS. |
| Implied PoS from market valuation differs dramatically from estimated PoS | Present both estimates transparently; do not default to market as "efficient" | In biotech, the market frequently misprices PoS — both too high (narrative-driven momentum) and too low (neglected small caps). The discrepancy is the investment thesis. |
