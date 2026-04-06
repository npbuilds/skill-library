# Tail Risk — Quick Reference


## Quick Reference

| Property | Gaussian (Normal) | Fat-tailed (Power Law) |
|----------|-------------------|----------------------|
| Tail probability | Decays exponentially | Decays polynomially (much slower) |
| 4-sigma event | 1 in 31,574 days (~127 years) | Occurs every few years |
| 6-sigma event | 1 in ~1.4 billion days | Occurs every few decades |
| Kurtosis | 3 (by definition) | Often 10-50+ for daily returns |
| Impact of extremes | Negligible | Dominates the average |
| Variance | Finite, stable | May be infinite or unstable |

## Quick Reference

| Position Type | Why Fragile | Failure Mode |
|--------------|-------------|-------------|
| Leveraged long positions | Leverage amplifies losses; margin calls force selling at worst moment | Forced liquidation at maximum panic |
| Short volatility (selling options) | Unlimited downside, limited upside by structure | Blows up precisely when everything else blows up |
| Illiquid assets with leverage | Can't exit when you need to; forced selling into no bid | Mark-to-market losses trigger doom loop |
| Carry trades (borrow low, lend high) | Works until it doesn't; funding dries up in crisis | Sudden currency or credit moves wipe years of carry |
| Complex structured products | Opaque risks; correlation assumptions break in crisis | What you don't understand will hurt you |
| Strategies dependent on low correlation | Assume diversification holds in all environments | Correlation goes to 1 in crisis |

## Quick Reference

| Position Type | Why Antifragile | Gain Mechanism |
|--------------|-----------------|----------------|
| Long deep OTM options | Pay small premium; gain enormously if tail event occurs | Convexity: option value accelerates as it moves in-the-money |
| Cash during crisis | Buying power increases precisely when assets are cheapest | Optionality: cash is a call option on future distressed assets |
| Trend-following strategies | Profit from sustained moves in either direction | Convexity: cut losers short, let winners run |
| Distressed debt expertise | Buy claims on bankrupt companies at pennies on the dollar | Asymmetry: limited downside (already distressed), large upside if recovery |
| Short fragile competitors | If your competitor is fragile, their failure is your gain | Competitive antifragility: stress kills the weak, strengthens survivors |

## Quick Reference

|                                                  |
|  SAFE LEG (85-90%)          CONVEX LEG (10-15%)  |
|  Maximum preservation       Maximum optionality   |
|  Near-zero risk             Very high risk         |
|  Boring                     Exciting               |
|  Provides survival          Provides upside         |
|                                                  |
|  ============= NO MIDDLE GROUND ===============  |

## Quick Reference

| Instrument | Typical Cost | Crisis Payoff | Conviction Required |
|-----------|-------------|---------------|-------------------|
| Deep OTM puts on equity indices | 1-3% per year | 10-100x in crash | Low (insurance) |
| Deep OTM calls on tail assets (gold, vol) | 0.5-2% per year | 5-50x in crisis | Low-moderate |
| VC-style equity bets | Total allocation | 0 or 10-100x | High in selection |
| Distressed debt | Below par purchase | Par or above at recovery | High in analysis |
| Binary catalyst bets (FDA, elections) | Defined risk | 3-10x | Moderate in thesis |
| Long volatility strategies | Carry cost | Large in vol spikes | Low (systematic) |

## When Tail Hedging Works and When It Doesn't

| Environment | Tail Hedge Performance | Net Portfolio Impact |
|-------------|----------------------|---------------------|
| Bull market (gradual) | Continuous bleed (cost) | Slight drag on returns |
| Sideways market | Continuous bleed (cost) | Moderate drag |
| Bear market (slow decline) | Partially effective | Some protection, but option decay hurts |
| Crash (fast, violent) | Extremely effective | Massive protection + rebalancing opportunity |
| Volatility spike without market drop | Options gain value | Small positive contribution |

## Black Swans vs Predictable Crises

| True Black Swan | Predictable Crisis (Gray Rhino) |
|----------------|-------------------------------|
| COVID-19 pandemic shutting global economy | 2008 housing bubble (many warned about subprime) |
| 9/11 attacks | Dot-com bubble burst (valuations were extreme) |
| Fukushima nuclear disaster | European debt crisis (debt levels were visible) |
| Discovery of a paradigm-changing technology | Emerging market currency crises (classic pattern) |

## Quick Reference

| Position | Size | Fragile? | Why? | Fix |
|----------|------|----------|------|-----|
| [Name] | [%] | [Yes/No/Partial] | [Specific fragility] | [Via negativa or hedge] |
