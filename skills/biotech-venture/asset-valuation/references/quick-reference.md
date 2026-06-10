# Asset Valuation — Quick Reference


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

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| Peak sales forecast implies blockbuster potential but cost-estimator shows the development program is prohibitively expensive | Compute the rNPV ratio (rNPV / remaining investment) — a ratio below 1.5-2x is generally unattractive despite high peak sales | High revenue potential means nothing if the cost and risk to get there consume the value. Capital efficiency matters as much as peak sales. |
| rnpv-modeler gives a high standalone value but deal-economics suggests the company will have to license at a discount | Present both standalone rNPV and likely realized value based on deal market conditions | For undercapitalized companies, the standalone rNPV is theoretical. The realized value depends on negotiating leverage, competitive interest, and funding alternatives. |
| Peak sales forecasts differ significantly depending on market share assumptions | Present bear/base/bull scenarios with explicit market share assumptions tied to differentiation evidence | Market share is the most subjective input in peak sales forecasting. Anchor to comparable launches and clinical differentiation data rather than aspirational assumptions. |
