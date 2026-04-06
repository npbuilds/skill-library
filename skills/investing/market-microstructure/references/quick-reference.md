# Market Microstructure — Quick Reference


## Routing Logic

| Question Pattern | Route To | Examples |
|---|---|---|
| Index funds, passive investing, ETF flows, index inclusion/exclusion, Russell reconstitution, S&P 500 addition, rebalancing flows, passive dominance, price discovery degradation, DCA flows | `passive-flow-dynamics` | "How do index rebalancing flows affect prices?" / "What happens when a stock gets added to the S&P 500?" / "Is passive investing breaking price discovery?" |
| ETF creation/redemption, authorized participants, NAV discounts/premiums, in-kind baskets, ETF arbitrage mechanism | `passive-flow-dynamics` | "How does ETF arbitrage work?" / "Why did bond ETFs trade at a discount in March 2020?" |
| Factor ETFs, smart beta, market-cap weighting feedback loops, index concentration | `passive-flow-dynamics` | "Does market-cap weighting create a bubble in mega-caps?" / "How do factor ETF flows amplify momentum?" |
| 0DTE options, gamma exposure, GEX, dealer hedging, gamma squeeze, short gamma, positive gamma, gamma flip | `options-mechanics` | "What is GEX telling us?" / "Are we in a positive or negative gamma regime?" / "How do 0DTE options affect intraday volatility?" |
| Volatility surface, implied vol, skew, term structure, contango, backwardation, VIX | `options-mechanics` | "What does the vol surface look like?" / "Why is skew elevated?" / "Is the VIX term structure in backwardation?" |
| Options expiration, OpEx, triple witching, vanna, charm, delta hedging, dealer positioning, retail options | `options-mechanics` | "How does OpEx affect the market?" / "What are vanna and charm flows?" / "Could this be a gamma squeeze?" |
| Liquidity, bid-ask spreads, market depth, dark pools, order flow toxicity, VPIN, flash crash, HFT | `liquidity-topology` | "Is the market truly liquid right now?" / "What caused the flash crash?" / "How much volume goes through dark pools?" |
| Payment for order flow, PFOF, retail order routing, execution quality, market maker withdrawal | `liquidity-topology` | "Does PFOF hurt retail investors?" / "Why does liquidity evaporate during stress?" |
| Circuit breakers, LULD, market structure fragility, ETF liquidity illusion | `liquidity-topology` | "What are the circuit breaker thresholds?" / "Can ETFs cause a liquidity crisis?" |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Passive flows suggest buying pressure (index inclusion) but options mechanics suggest negative gamma (amplified selling) | Time horizon matters — passive inclusion flows build over days/weeks as index funds rebalance, while gamma effects are intraday/intraweek. Short-term negative gamma can overwhelm inclusion buying temporarily, but the passive flow eventually dominates | Passive flows are slow and persistent; options flows are fast and ephemeral |
| Options mechanics suggest a calm, pinned market (positive gamma) but liquidity topology shows deteriorating depth | Positive gamma can mask underlying fragility. The market appears calm because dealers are dampening moves, but if a catalyst pushes price through the gamma flip point, the thin liquidity underneath will amplify the move violently | Surface calm does not equal structural stability |
| Passive flows suggest predictable rebalancing but liquidity data shows dark pool activity surging | Institutional players are likely front-running the rebalancing. The "predictable" flow may already be priced if enough participants are positioning ahead of it. Check dark pool prints in affected names for size and direction | Predictable flows get arbitraged; the edge decays as more participants exploit it |
