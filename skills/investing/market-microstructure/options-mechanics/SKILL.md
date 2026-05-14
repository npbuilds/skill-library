---
name: options-mechanics
description: >
  Knowledge skill covering options market microstructure — 0DTE dynamics, gamma exposure (GEX),
  dealer hedging mechanics, volatility surface analysis, vanna and charm flows, options expiration
  effects, and retail options impact. Use when analyzing how options market mechanics create
  non-fundamental price movements in the underlying.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Options Mechanics

## The 0DTE Revolution

Zero-days-to-expiration (0DTE) options — contracts that expire on the same day they are traded — have become the dominant force in US equity options markets. As of 2024, 0DTE options on the S&P 500 (SPX) account for over 50% of total SPX options volume on most trading days. Including near-dated (1DTE, 2DTE) contracts, ultra-short-dated options represent the majority of all US index options activity.

### Why 0DTE Options Exist at This Scale

The CBOE introduced daily SPX expirations in 2022 (previously only Monday, Wednesday, Friday), creating a 0DTE contract available every trading day. This change unlocked massive demand from several participant types:

**Institutional hedgers:**
- Portfolio managers who want overnight risk but not intraday gamma exposure
- Dealers offering structured products with daily reset features
- Pension funds and endowments hedging specific event windows (FOMC, CPI releases)

**Systematic strategies:**
- 0DTE premium selling (systematic short straddle/strangle strategies collecting theta)
- Intraday momentum/reversal strategies using options for leverage
- Vol-of-vol strategies that trade the curvature of 0DTE implied volatility through the day

**Retail participants:**
- 0DTE options are cheap in dollar terms (low premium because minimal time value)
- They offer extreme leverage — a 0.05 delta 0DTE call can return 100x+ on a large move
- The "lottery ticket" appeal attracts retail flow, concentrated in directional bets

### Why 0DTE Matters: Concentrated Gamma Exposure

The critical property of 0DTE options is that their gamma is extremely high. Gamma measures how fast an option's delta changes as the underlying price moves. For options near expiration:

- At-the-money (ATM) 0DTE options have the highest gamma of any option in the chain
- This gamma is concentrated in a narrow strike range (within 0.5-1% of the current price)
- As expiration approaches throughout the trading day, gamma increases further
- Dealer hedging of this concentrated gamma drives mechanical intraday flows

**Practical implication**: The 0DTE options market creates a "gamma field" around the current price that can either pin prices (when dealers are long gamma) or amplify moves (when dealers are short gamma). This field changes minute by minute as time passes and options are traded.

---

## Gamma Exposure (GEX): The Market's Structural Bias

### What GEX Measures

GEX (Gamma Exposure) quantifies the aggregate gamma position of options market makers (dealers) across all strikes and expirations. It answers a critical question: when the market moves 1%, how much do dealers need to buy or sell to remain delta-hedged?

**The formula in principle:**
- For each option contract outstanding (open interest), estimate whether a dealer is long or short that option
- Calculate the gamma of each position
- Aggregate across all strikes and expirations
- The result is a net gamma position: positive (dealers are long gamma) or negative (dealers are short gamma)

**Dealer positioning assumptions:**
- Dealers are generally assumed to be net short options to end users (investors buy protection, dealers sell it)
- However, dealers are net long options when customer flow is dominated by selling (e.g., systematic covered call writing, cash-secured put selling)
- The sign of GEX is an estimate — different data providers use different assumptions and arrive at different numbers
- Directional accuracy matters more than precise magnitude

### Positive Gamma Regime (GEX > 0)

When dealers are net long gamma, their hedging activity dampens market moves:

**Mechanics:**
- Market rises → dealer long gamma positions increase in delta → dealers must sell the underlying to rebalance → selling pressure counteracts the rally
- Market falls → dealer long gamma positions decrease in delta → dealers must buy the underlying to rebalance → buying pressure counteracts the decline
- Net effect: dealers act as a stabilizing force, buying dips and selling rallies mechanically

**Market behavior in positive gamma:**
- Low realized volatility (moves are dampened)
- Mean-reverting intraday price action
- "Pinning" around strikes with high open interest
- The market feels calm and controlled
- VIX tends to drift lower

**Trading implication:** In positive gamma regimes, selling volatility (short straddles, iron condors) tends to be profitable because realized volatility undershoots implied volatility. Range-bound strategies work well.

### Negative Gamma Regime (GEX < 0)

When dealers are net short gamma, their hedging activity amplifies market moves:

**Mechanics:**
- Market rises → dealer short gamma positions become more negative in delta → dealers must buy the underlying to rebalance → buying pressure amplifies the rally
- Market falls → dealer short gamma positions become more positive in delta → dealers must sell the underlying to rebalance → selling pressure amplifies the decline
- Net effect: dealers act as a destabilizing force, buying into rallies and selling into selloffs

**Market behavior in negative gamma:**
- High realized volatility (moves are amplified)
- Trending and momentum-driven price action
- Large intraday ranges
- Gap moves and overnight volatility
- VIX tends to spike

**Trading implication:** In negative gamma regimes, buying volatility and momentum strategies tend to work. Selling volatility is dangerous because realized vol can massively overshoot implied vol.

### The GEX Flip Point

The "gamma flip" or "zero gamma" level is the price at which aggregate dealer gamma transitions from positive to negative (or vice versa):

**Above the flip point:** Positive gamma territory — dealers dampen moves, market tends to be calm and range-bound.

**Below the flip point:** Negative gamma territory — dealers amplify moves, market tends to trend and experience larger swings.

**Why the flip point matters:**
- It acts as a "speed limit" level — above it, the market is structurally calmer
- A break below the flip point can trigger a cascade: the move below → negative gamma → dealer selling → more downside → more negative gamma
- Flip points tend to cluster near major put open interest concentrations
- During market selloffs, monitoring the flip point helps anticipate when selling pressure becomes self-reinforcing

### GEX Data Sources

- **SpotGamma**: Daily GEX levels, flip points, strike-level gamma mapping for SPX and major single stocks. Subscription service with real-time updates.
- **SqueezeMetrics**: DIX (Dark Index) and GEX indicators. Publicly available with some delay.
- **Unusual Whales**: Options flow data, gamma exposure estimates, and unusual activity detection. Retail-oriented platform.
- **GammaLab / Orats**: Professional-grade options analytics including gamma exposure modeling.
- **CBOE data**: Raw options data (volume, open interest) that can be used to construct custom GEX estimates.

**Caveat**: All GEX estimates rely on assumptions about dealer positioning. No provider knows the actual dealer book. Treat GEX as directionally informative, not precisely accurate.

---

## Volatility Surface Analysis

### Implied Volatility Term Structure

The term structure of implied volatility plots implied vol across different expirations (1-day, 1-week, 1-month, 3-month, 6-month, 1-year):

**Contango (normal):** Longer-dated options have higher implied vol than shorter-dated options. This is the default state because:
- More time = more uncertainty
- Longer expirations carry more event risk (earnings, elections, policy decisions)
- Short-dated vol gets crushed by theta decay approaching expiration

**Backwardation (fear):** Shorter-dated options have higher implied vol than longer-dated. This signals:
- An imminent known event creating near-term uncertainty (CPI report, FOMC, earnings)
- Acute market stress where fear of immediate moves exceeds longer-term concerns
- Demand for short-dated hedges spiking (e.g., portfolio managers panic-buying puts)

**Practical reading:**
- Persistent backwardation without a clear catalyst = structural stress, elevated crash risk
- Backwardation concentrated in a specific expiration = event-driven (check the calendar)
- Steep contango = complacency, low near-term fear, potentially a contrarian signal for buying protection cheaply

### Volatility Skew

Skew measures the difference in implied volatility between out-of-the-money (OTM) puts and OTM calls at the same expiration:

**Equity index skew (normally negative):**
- OTM puts are more expensive (higher implied vol) than OTM calls
- This reflects structural demand for downside protection (portfolio hedging)
- The 25-delta put typically has 5-15 vol points more implied vol than the 25-delta call
- Skew steepened dramatically after the 1987 crash and has remained elevated since

**What skew tells you:**
- **Steepening skew** (puts getting more expensive relative to calls): Increasing demand for crash protection. Institutions are buying puts. Fear of left-tail events is rising.
- **Flattening skew** (puts getting relatively cheaper): Hedging demand is declining. Complacency is building. Potentially a contrarian signal — protection is cheap.
- **Inverted skew** (calls more expensive than puts): Rare for indices, common for single stocks with squeeze potential. Signals extreme upside demand — often retail-driven.

### Smile Dynamics During Stress

The full volatility surface (term structure x skew) behaves predictably during market stress:

**Phase 1 — Early stress (market down 2-5%):**
- Short-dated implied vol spikes (term structure inverts to backwardation)
- Skew steepens (put demand surges)
- VIX rises sharply
- Vol-of-vol (VVIX) spikes

**Phase 2 — Acute crisis (market down 5-15%):**
- Entire surface shifts higher
- Skew can actually flatten temporarily as realized vol catches up to put implied vol
- Correlation spikes (single-stock vol converges to index vol)
- Term structure backwardation becomes extreme

**Phase 3 — Resolution/recovery:**
- Short-dated vol collapses first (term structure normalizes to contango)
- Skew remains elevated (hedging demand persists)
- VIX declines but the "floor" resets higher than pre-stress levels
- Full normalization takes weeks to months

---

## Dealer Positioning and Mechanical Flows

### Vanna Flows: Volatility-Driven Delta Hedging

Vanna measures how an option's delta changes as implied volatility changes. When vol drops, the delta of OTM options decreases (they become more OTM in vol-adjusted terms). When vol rises, OTM option deltas increase.

**Dealer vanna mechanics:**
- Dealers are typically net short OTM puts (sold as protection to investors)
- When vol drops → put deltas decrease → dealers' short put positions require less short stock to hedge → dealers buy back stock → buying pressure → market rallies → vol drops further
- This creates a positive feedback loop: falling vol → buying → higher prices → lower vol
- The reverse applies when vol rises: rising vol → put deltas increase → dealers must sell more stock to hedge → selling pressure → market falls → vol rises further

**Vanna flows are strongest when:**
- There is large OTM put open interest (lots of put vanna to hedge)
- Implied vol is moving sharply (large changes in delta to adjust)
- The move happens into known vol-compressing events (approaching OpEx, after VIX futures roll)

**The "vanna rally" pattern:**
- After a vol spike (market selloff), the subsequent vol compression drives mechanical buying through dealer vanna hedging
- This explains why post-selloff bounces are often sharp and feel "mechanical" — they partly are
- The rally can extend beyond fundamental justification because vanna buying is price-insensitive

### Charm Flows: Time-Driven Delta Hedging

Charm (delta decay or "dcharm") measures how an option's delta changes as time passes, holding price constant. As options approach expiration:

- OTM options lose delta (delta decays toward zero)
- ITM options gain delta (delta approaches +1 or -1)
- ATM options: delta stays near 0.5 but gamma intensifies

**Dealer charm mechanics into OpEx:**
- Dealers are typically short puts below the market
- As time passes, these OTM puts lose delta → dealers' short put positions require less short stock to hedge → dealers buy back short stock hedges → buying pressure
- This creates the "charm rally" — a mechanical bid for stocks heading into options expiration, especially in the final 2-3 days before monthly OpEx
- The rally is strongest when there is large put open interest below the market and the market is in a positive gamma regime

**Charm effect on the day of expiration:**
- Delta decay accelerates dramatically on expiration day
- OTM options rapidly approach zero delta; ITM options rapidly approach full delta
- The delta adjustments by dealers in the final hours can create erratic intraday moves
- The 3:00-4:00 PM window on OpEx Friday often shows unusual volume and volatility

---

## Options Expiration (OpEx) Effects

### Monthly OpEx (Third Friday)

Monthly options expirations are significant flow events because they involve the largest open interest:

**Pre-OpEx dynamics (Monday-Thursday of OpEx week):**
- Charm flows create a mild positive bias (see above)
- Gamma pinning intensifies as expiration approaches — stocks tend to "pin" to strikes with high open interest
- Implied vol declines as the expiration approaches (theta crush)

**OpEx day (Friday):**
- Large open interest rolls off — options expire or are exercised
- The removal of this open interest reduces the gamma "field" around prices
- Post-expiration, the pinning effect disappears → larger moves become possible

**Post-OpEx dynamics (following week):**
- Historically, the Monday-Wednesday after monthly OpEx shows elevated realized volatility
- Without the stabilizing gamma from expired options, the market is "unpinned"
- New options positions are established, creating a fresh gamma landscape
- Large directional moves often begin in post-OpEx windows

### Quarterly OpEx (Triple/Quadruple Witching)

Quarterly expirations (March, June, September, December) involve the simultaneous expiry of:
1. Stock options
2. Stock index options
3. Stock index futures
4. Single-stock futures (now minimal volume, but historically the "quadruple")

**Scale:**
- Quarterly OpEx typically involves 2-4x the notional open interest of monthly OpEx
- The last hour of trading on quarterly OpEx regularly exceeds $1 trillion in notional turnover
- Index rebalancing (S&P, MSCI) often occurs on the same day, compounding the flow

**Impact:**
- Enormous volume but not always directional — much of it is roll activity (closing expiring positions, opening new ones)
- The final 30 minutes (the "witching window") can see extreme volume and price swings
- Closing auction imbalances are typically 5-10x larger than normal
- Realized volatility in the final hour can be 2-3x the rest of the day

### LEAPS and Quarterly Expirations

Long-dated options (LEAPS, 1-2 year expirations) have low gamma individually but collectively represent significant open interest:

- LEAPS expiry (typically January) can create flow events if concentrated
- Quarterly expirations in non-witching months (January, April, July, October) carry moderate open interest
- The key is concentration: if open interest is skewed toward a specific strike or expiration, the flow effects are amplified

---

## Retail Options Impact

### The Retail Options Revolution

Retail investors now account for an estimated 25-30% of total options volume (by contract count) and an outsized share of single-stock options activity. Enabled by:

- Commission-free options trading (Robinhood, Schwab, E*Trade)
- Fractional-like access through cheap OTM options
- Social media coordination (Reddit, Twitter/X, YouTube)
- Gamification of trading platforms

### Gamma Squeeze Mechanics

A gamma squeeze occurs when concentrated directional options buying forces dealers to hedge in the underlying, creating a self-reinforcing price spiral:

**The setup:**
1. A stock has high short interest (significant bearish positioning)
2. Retail or speculative buyers aggressively purchase OTM calls
3. Dealers selling these calls must delta-hedge by buying the underlying stock
4. The buying pushes the stock price up, moving more calls from OTM to ATM
5. ATM options have higher delta → dealers must buy even more stock
6. The rising price triggers short covering by short sellers → additional buying pressure
7. Steps 3-6 repeat, creating an explosive upward move

**The classic example: GameStop (GME), January 2021:**
- GME had 140% short interest (more shares shorted than existed in float)
- Retail buyers on r/WallStreetBets purchased massive quantities of OTM calls
- Market makers hedging these calls bought GME stock, pushing the price from ~$20 to $483 in two weeks
- Short sellers covering added fuel; dealers hedging OTM calls that went ITM added more
- The move was almost entirely mechanical — not driven by fundamental revaluation

**Identifying gamma squeeze potential:**
- High short interest (>20% of float) — necessary for short-covering fuel
- Rising call/put ratio concentrated in OTM strikes — retail accumulation
- Low float (fewer shares available amplify price impact per dollar of flow)
- Increasing open interest in OTM calls over several days/weeks
- Widening bid-ask spreads in the underlying (market makers reducing exposure)
- Social media buzz and coordinated interest (r/WallStreetBets, FinTwit)

**The unwind:**
- Gamma squeezes are inherently temporary — they reverse when buying pressure exhausts
- As price rises parabolically, call buyers take profits (selling calls back to dealers)
- Dealers sell their delta hedges → selling pressure
- Short interest declines as shorts cover, removing that fuel source
- The collapse is typically faster than the ascent because long gamma unwind (dealer selling) compounds with profit-taking

### Retail Flow Patterns

Retail options flow has distinctive signatures:

**What retail buys:**
- Short-dated OTM calls on individual stocks (lottery tickets)
- 0DTE SPX options (both calls and puts, but skewed toward calls)
- Call options on stocks with social media momentum
- Options on meme stocks, high-short-interest names, and recent IPOs

**What retail sells:**
- Covered calls (income-generating strategy, especially popular in retirement accounts)
- Cash-secured puts (the "Wheel" strategy popular on Reddit)
- These selling patterns make retail a net supplier of upside gamma (through covered calls) and downside gamma (through put selling)

**Impact on dealer positioning:**
- When retail is aggressively buying calls → dealers are short upside gamma → amplification of rallies
- When retail is aggressively selling covered calls → dealers are long upside gamma → dampening of rallies
- The net retail position shifts the GEX landscape, sometimes significantly

---

## Practical Framework: Reading Options for Non-Fundamental Signals

### Daily Options Market Assessment Checklist

1. **GEX regime**: Positive or negative? Above or below the flip point? Check SpotGamma or equivalent data provider.

2. **0DTE activity**: Volume, put/call ratio, and concentration of strikes. Heavy 0DTE call buying → intraday gamma squeeze risk to upside. Heavy 0DTE put buying → intraday gamma cascade risk to downside.

3. **Term structure shape**: Contango (normal, calm) or backwardation (fear, event risk)? Any kinks around specific expirations (event-driven)?

4. **Skew level**: Elevated (demand for protection is high) or compressed (complacency)? Compare current skew to 6-month and 12-month percentile.

5. **Upcoming OpEx**: How many days until monthly or quarterly OpEx? Large open interest rolls off at expiration → reduced pinning → potential for larger moves post-OpEx.

6. **Vanna/charm direction**: Is vol rising or falling? Rising vol + large put OI = vanna selling pressure. Falling vol + large put OI = vanna buying. Approaching OpEx = charm buying.

7. **Unusual activity**: Any single-stock names showing outsized call buying relative to historical averages? High call volume + high short interest = gamma squeeze watch.

### Integrating Options Signals With Other Microstructure Data

Options mechanics do not operate in isolation. Combine with:

- **Passive flows** (sibling skill): When index rebalancing coincides with OpEx, the combined flow effects are amplified. Check the passive flow calendar against the options expiration calendar.
- **Liquidity conditions** (sibling skill): Negative gamma + thin market depth = risk of flash-crash-like moves. Always check liquidity before concluding that options flows will dominate.
- **Fundamental catalysts**: Options mechanics amplify fundamental moves. A negative earnings surprise in a negative gamma environment will produce a much larger price decline than the same surprise in positive gamma. The options environment determines the "gain" on any fundamental signal.

## Related Skills

- **hedging-architecture** — Options are a primary hedging instrument. Hedging-architecture provides the strategic framework (what to hedge, when, with what budget); options-mechanics provides the instrument-level Greek and structure logic.
