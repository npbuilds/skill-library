---
name: asset-valuation
description: >
  Direct rNPV modeling, peak sales forecasting, development cost estimation, and deal economics
  questions to the appropriate specialist skill. Activate when building a risk-adjusted valuation
  for a clinical asset, modeling revenue potential, estimating clinical program costs, or analyzing
  licensing and M&A deal terms. rNPV is the gold standard of biotech valuation — this director
  ensures models are built from the bottom up with explicit assumptions at every layer.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Asset Valuation Director

Biotech valuation is fundamentally different from traditional DCF. The rNPV (risk-adjusted net present value) framework discounts each cash flow by the probability that it will actually occur — gating future revenues by cumulative PoS and applying phase-specific discount rates. This director routes valuation questions to specialist skills that build models from bottom-up components: peak sales forecasting, development cost estimation, PoS-gated revenue streams, and deal economics analysis.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| rnpv-modeler | action | Building risk-adjusted NPV models, applying phase-gated probability discounts, running valuation sensitivity analysis, comparing rNPV to market cap, modeling optionality for platform technologies |
| peak-sales-forecaster | action | Estimating peak annual revenue by indication — patient population x market share x price x compliance x duration of therapy, modeling launch curves, analoging to comparable launches |
| cost-estimator | action | Estimating remaining development costs by phase and indication — trial costs, CMC costs, regulatory costs, commercial build-out, SG&A ramp, modeling cash runway and dilution |
| deal-economics | knowledge | Understanding licensing deal structures, milestone economics, royalty stacking, M&A valuation methodologies, earnout mechanics, option deal structures, and comparable transaction analysis |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| rNPV, risk-adjusted value, NPV, valuation model, discount rate, phase-gated DCF | rnpv-modeler | "What is the rNPV of this Phase 2 asset?" / "Build me an rNPV model for this program" |
| Peak sales, revenue potential, market size, pricing, market share, launch curve, patient uptake | peak-sales-forecaster | "What are peak sales for a best-in-class NASH therapy?" / "Model the launch curve for this rare disease drug" |
| Development costs, trial costs, burn rate, cash runway, dilution, cost to approval | cost-estimator | "How much will it cost to get this asset to approval?" / "What is the remaining development spend?" |
| Deal terms, licensing, royalties, milestones, M&A, comparable transactions, earnouts | deal-economics | "What are typical licensing terms for a Phase 2 oncology asset?" / "How should I think about the earnout structure?" |
| Full valuation | peak-sales-forecaster then cost-estimator then rnpv-modeler | "Value this clinical-stage biotech" |
| Deal evaluation | rnpv-modeler then deal-economics | "Is this licensing deal fair?" |

## Multi-Skill Questions

1. **Full rNPV Build**: "What is this Phase 2 oncology asset worth?"
   - Load peak-sales-forecaster to model revenue: addressable population x market share x price x compliance
   - Load cost-estimator to model remaining development costs through approval and launch
   - Load rnpv-modeler to assemble the model: risk-adjust revenues by cumulative PoS from each phase gate, subtract risk-adjusted costs, apply appropriate WACC (typically 10-15% for clinical-stage biotech)
   - Synthesize: The rNPV is only as good as its inputs. Always present the key drivers (peak sales, PoS, discount rate) with sensitivity ranges.

2. **Deal Evaluation**: "Is this licensing deal accretive?"
   - Load rnpv-modeler to establish standalone asset value
   - Load deal-economics to decompose the deal structure — upfront, milestones, royalties, co-promote rights
   - Compare: Is the total deal value (probability-weighted milestones + royalty stream) greater than or less than the standalone rNPV? What optionality is the licensor giving up?

3. **Portfolio Valuation**: "What is the sum-of-parts valuation for this company?"
   - Load peak-sales-forecaster and cost-estimator for each asset
   - Load rnpv-modeler for each program independently
   - Sum individual rNPVs, add net cash, subtract corporate overhead
   - Compare to enterprise value to identify over/undervaluation

## Curriculum Order

1. **peak-sales-forecaster** — Foundation. Revenue is the numerator of all biotech valuation. Learn to build peak sales estimates from patient population, market share, pricing, and compliance. Understand launch curve dynamics and analog-based forecasting.
2. **cost-estimator** — Second. Costs are the denominator. Learn to estimate remaining development spend by phase, model the commercial build-out, and project cash runway. Costs determine dilution risk and capital efficiency.
3. **deal-economics** — Third. Before building rNPV, understand the deal structures that govern how value flows between parties. Licensing terms, royalty stacking, milestone triggers, and M&A mechanics create the framework in which rNPV is applied.
4. **rnpv-modeler** — Fourth. With revenue, cost, and deal structure literacy, build the integrated rNPV model. This is the capstone skill that synthesizes all inputs into a single risk-adjusted valuation.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Peak sales forecast implies blockbuster potential but cost-estimator shows the development program is prohibitively expensive | Compute the rNPV ratio (rNPV / remaining investment) — a ratio below 1.5-2x is generally unattractive despite high peak sales | High revenue potential means nothing if the cost and risk to get there consume the value. Capital efficiency matters as much as peak sales. |
| rnpv-modeler gives a high standalone value but deal-economics suggests the company will have to license at a discount | Present both standalone rNPV and likely realized value based on deal market conditions | For undercapitalized companies, the standalone rNPV is theoretical. The realized value depends on negotiating leverage, competitive interest, and funding alternatives. |
| Peak sales forecasts differ significantly depending on market share assumptions | Present bear/base/bull scenarios with explicit market share assumptions tied to differentiation evidence | Market share is the most subjective input in peak sales forecasting. Anchor to comparable launches and clinical differentiation data rather than aspirational assumptions. |

## Scope Boundaries

**This director handles**: All questions about biotech asset valuation, rNPV modeling, peak sales forecasting, development cost estimation, deal economics, licensing valuation, M&A analysis, portfolio sum-of-parts valuation, and valuation sensitivity analysis.

**Route to Asclepius when**:
- The question requires PoS estimates as inputs to the rNPV model (route to probability-of-success)
- The question involves clinical program design that drives development costs (route to clinical-development)
- The question involves regulatory pathway that affects timeline and cost assumptions (route to regulatory-strategy)
- The question involves competitive landscape that drives market share assumptions (route to competitive-intelligence)
- The question involves manufacturing cost drivers (route to manufacturing-ip)
- The question spans multiple diligence pillars and needs orchestrator-level coordination

## Cross-Domain Connections

- **Biotech-venture/rnpv-modeler, peak-sales-forecaster, cost-estimator, deal-economics**: Child skills that execute the component analyses this director orchestrates
- **Investing/intrinsic-value**: rNPV is the biotech-specific implementation of discounted cash flow valuation — same conceptual framework, adapted for probability-gated clinical milestones
- **Investing/archon**: The general investing orchestrator; asset-valuation specializes its valuation methodology for the unique risk structure of clinical-stage biotech assets
