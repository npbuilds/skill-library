---
name: probability-of-success
description: >
  Direct probability of success estimation, phase transition analysis, and mechanism-based risk
  adjustment to the appropriate specialist skill. Activate when calculating PoS for a clinical
  asset, adjusting base rates for program-specific factors, or evaluating target validation
  evidence. PoS is the spine of every biotech valuation — this director ensures estimates are
  explicit, assumption-driven, and anchored to empirical base rates.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Probability of Success Director

PoS is the single most important number in biotech investing. It determines the risk-adjusted value of every clinical asset, drives portfolio construction, and separates disciplined investors from narrative-driven ones. This director routes PoS questions to specialist skills that ground estimates in BIO/Informa base rates, adjust for mechanism-specific evidence, and produce transparent, auditable probability chains rather than gut-feel estimates.

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

## Multi-Skill Questions

1. **Full PoS Build**: "What is the PoS for this Phase 2b asset in moderate-to-severe atopic dermatitis targeting IL-13?"
   - Load pos-base-rates for the indication/phase/modality base rate (dermatology, Phase 2 to approval, biologic)
   - Load mechanism-risk-adjuster to apply program-specific modifiers (IL-13 validated by dupilumab, positive Phase 2b dose-response, but crowded competitive landscape)
   - Load pos-calculator to compute the cumulative PoS chain and produce the waterfall
   - Synthesize: Start from base rate, apply each modifier with explicit rationale, output a point estimate with a credible range

2. **Market Implied vs Estimated**: "Is the market overpricing this asset's risk?"
   - Load pos-calculator to back-calculate implied PoS from enterprise value and peak sales assumptions
   - Load pos-base-rates and mechanism-risk-adjuster to build an independent PoS estimate
   - Compare: If implied PoS exceeds estimated PoS, the market is underpricing risk. If estimated exceeds implied, the asset may be undervalued on a risk-adjusted basis.

3. **Portfolio PoS Aggregation**: "What is the portfolio-level PoS for a company with three clinical assets?"
   - Load pos-calculator for each asset individually
   - Then calculate portfolio PoS: P(at least one success) = 1 - product of (1 - individual PoS)
   - This is the correct framing for platform companies with multiple shots on goal

## Curriculum Order

1. **pos-base-rates** — Foundation. Before adjusting anything, learn the empirical base rates. Know that oncology Phase 2-to-approval is roughly 10-15%, that rare disease is 2-3x higher, that first-in-class is lower than best-in-class. These base rates are the anchor from which all estimates start.
2. **mechanism-risk-adjuster** — Second. Once you know the base rate, learn how to adjust it. Genetic validation (Mendelian randomization, GWAS hits) can increase PoS 2-3x. Prior failures on the same target decrease it. Clinical signal strength, biomarker enrichment, and competitive readthrough all modify the prior.
3. **pos-calculator** — Third. With adjusted probabilities in hand, learn to compute cumulative PoS, build waterfalls, run sensitivity analyses, and back-calculate implied PoS from market valuations. This is the computational layer that turns assumptions into actionable numbers.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Base rate is low but mechanism-risk-adjuster gives strong uplift (e.g., genetic validation on a historically difficult indication) | Cap the adjusted PoS at 2-3x the base rate unless there is truly exceptional evidence; clearly state the adjustment magnitude and rationale | Even strong genetic validation cannot overcome all sources of clinical failure (safety, formulation, dosing). Uncapped adjustments lead to overconfidence. |
| Mechanism-risk-adjuster says "reduce PoS due to prior target failures" but the current program has a differentiated mechanism of action | Assess whether the prior failures were mechanism-related or execution-related; adjust accordingly | If prior failures were due to the target itself (biology wrong), reduce PoS significantly. If prior failures were due to trial design, dosing, or patient selection (execution wrong), a differentiated approach may genuinely have higher PoS. |
| Implied PoS from market valuation differs dramatically from estimated PoS | Present both estimates transparently; do not default to market as "efficient" | In biotech, the market frequently misprices PoS — both too high (narrative-driven momentum) and too low (neglected small caps). The discrepancy is the investment thesis. |

## Scope Boundaries

**This director handles**: All questions about probability of technical and regulatory success for clinical assets, phase transition probabilities, base rate lookups, mechanism-based risk adjustment, PoS sensitivity analysis, implied PoS calculations, and target validation evidence assessment.

**Route to Asclepius when**:
- The question requires clinical trial design input that feeds PoS (route to clinical-development)
- The question requires translating PoS into rNPV or asset value (route to asset-valuation)
- The question involves regulatory pathway risk rather than clinical success probability (route to regulatory-strategy)
- The question involves competitive readthrough that requires full pipeline analysis (route to competitive-intelligence)
- The question spans multiple diligence pillars and needs orchestrator-level coordination

## Cross-Domain Connections

- **Biotech-venture/pos-calculator, pos-base-rates, mechanism-risk-adjuster**: Child skills that compute, look up, and adjust probability of success estimates
- **Investing/risk-architecture**: Structural parallel — both domains quantify multi-factor risk by decomposing aggregate probability into independent risk components
- **Investing/reflexivity-theory**: The biotech reflexivity concept is imported from Soros — market pricing of PoS affects company behavior (capital access, trial design ambition), which in turn affects actual PoS
