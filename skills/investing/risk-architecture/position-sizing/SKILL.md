---
name: position-sizing
description: >
  Deep expertise in position sizing methodologies — Kelly criterion, risk budgeting,
  volatility-adjusted sizing, conviction-based concentration, and portfolio heat management.
  Use when determining how much capital to allocate to a specific trade or position.
---

# Position Sizing — The Most Important Decision You Make

Position sizing is the single most consequential decision in investing. A mediocre idea with excellent sizing outperforms a brilliant idea with reckless sizing. This skill covers the full spectrum of sizing methodologies, from the mathematically optimal Kelly criterion to the practitioner wisdom of Tudor Jones and Druckenmiller.

The core question is always the same: **given my edge, my capital, my risk tolerance, and my conviction — how much?**

## The Kelly Criterion

### The Formula

The Kelly criterion maximizes the long-term geometric growth rate of capital. For a simple binary bet:

```
f* = (bp - q) / b
```

Where:
- `f*` = fraction of capital to bet
- `b` = odds received on the bet (net profit per dollar risked)
- `p` = probability of winning
- `q` = 1 - p = probability of losing

**Example**: You believe a stock has a 60% chance of going up 50% and a 40% chance of going down 30%.
- b = 50/30 = 1.667
- p = 0.60, q = 0.40
- f* = (1.667 x 0.60 - 0.40) / 1.667 = (1.0 - 0.40) / 1.667 = 0.36

Kelly says bet 36% of your capital. This is almost certainly too aggressive for real-world application.

### Why Kelly Is Optimal

Kelly maximizes the expected value of log(wealth), which is equivalent to maximizing the geometric growth rate. Over a sufficiently long time horizon, a Kelly bettor will almost surely end up with more wealth than any other fixed-fraction strategy. The key insight: **arithmetic mean returns don't determine long-term wealth — geometric mean returns do.** Volatility destroys compounding, and Kelly optimally trades off return and volatility.

The geometric growth rate under Kelly is:

```
g = p * ln(1 + f*b) + q * ln(1 - f*)
```

Any fraction above Kelly reduces the geometric growth rate. At 2x Kelly, the expected geometric growth rate is zero — you're guaranteed to go broke eventually despite a positive edge.

### Fractional Kelly: What Practitioners Actually Use

Full Kelly is almost never used in practice because:

1. **Parameter uncertainty**: Kelly assumes you know p and b exactly. You don't. Overestimating your edge is the most common and dangerous mistake.
2. **Drawdown severity**: Full Kelly produces enormous drawdowns. The maximum drawdown probability under Kelly is roughly proportional to `1/n` where n is the ratio of edge to bet frequency. A full-Kelly bettor should expect to lose 50% of capital at some point.
3. **Non-binary outcomes**: Real positions have continuous, complex payoff distributions, not simple win/lose.
4. **Psychological tolerance**: Few humans can stomach full-Kelly volatility without intervening.

**Fractional Kelly solves this by betting a fraction of the Kelly-optimal amount:**

| Fraction | Expected Growth (% of Kelly) | Drawdown Reduction | Use When |
|----------|------------------------------|-------------------|----------|
| Full Kelly (1.0) | 100% | Baseline | Never in practice |
| Half Kelly (0.5) | 75% | ~50% reduction | High confidence in edge estimate |
| Quarter Kelly (0.25) | ~56% | ~75% reduction | Moderate confidence, or correlated bets |
| Tenth Kelly (0.1) | ~34% | ~90% reduction | Low confidence, exploratory positions |

The critical insight: **half Kelly gives you 75% of the growth rate with roughly half the variance.** This is the most common practitioner choice. You sacrifice 25% of expected growth to dramatically reduce ruin risk and drawdowns.

### Multi-Asset Kelly

For a portfolio of correlated assets, the Kelly criterion generalizes to:

```
f* = C^(-1) * mu
```

Where:
- `f*` = vector of optimal position sizes
- `C^(-1)` = inverse of the covariance matrix of returns
- `mu` = vector of expected excess returns

This is mathematically equivalent to maximizing the Sharpe ratio of the portfolio (mean-variance optimization with a specific risk aversion parameter). The multi-asset Kelly framework reveals that position sizes should account for correlations — two highly correlated positions should each be smaller than two uncorrelated ones.

### Kelly's Blind Spots

Kelly assumes:
- **Known probabilities**: You know p and b. In reality, you estimate them with error. Overconfidence in your edge estimate is the primary reason Kelly fails in practice.
- **Independent bets**: Each bet is independent. In a portfolio, positions are correlated. A single factor (like a market crash) can hit all your positions simultaneously.
- **Infinite divisibility**: You can bet any fraction. In reality, there are minimum position sizes, round lots, and discrete contracts.
- **No liquidity constraints**: You can always bet at the quoted odds. In reality, large positions move markets, and liquidity evaporates in crises.
- **No time constraints**: Kelly optimizes for infinite horizons. Real investors have finite horizons, liabilities, and career risk.

**The meta-rule**: Use Kelly as a ceiling, not a target. If Kelly says bet 20%, bet less than 20%. If Kelly says bet 2%, that's probably about right.

## The 2:1 Rule (Paul Tudor Jones)

Tudor Jones's core risk management principle: **never enter a position unless the expected reward is at least 2x the expected risk.**

```
Minimum reward/risk ratio = 2:1
```

This is simpler than Kelly but enormously powerful in practice because:

1. **It forces pre-trade discipline**: Before entering, you must define your target and your stop. If you can't articulate a 2:1 setup, you don't have a trade.
2. **It creates a positive expectancy buffer**: Even if you're only right 40% of the time, a 2:1 R:R ratio produces a positive expected value: `0.40 * 2 - 0.60 * 1 = +0.20` per unit risked.
3. **It filters low-quality setups**: Most "ideas" don't have 2:1 setups. The rule eliminates the marginal trades that destroy returns.

### Applying the 2:1 Rule

For each potential position:
1. Define the entry price
2. Define the stop-loss level (where the thesis is invalidated)
3. Define the target price (where the thesis is fulfilled)
4. Calculate: `(Target - Entry) / (Entry - Stop) >= 2.0`
5. If the ratio is below 2.0, either find a better entry, tighten the stop (if justified), or pass on the trade

**Example**: Stock at $100. Your thesis says it should reach $130. Your analysis says the thesis is wrong if it breaks below $90.
- Reward = $130 - $100 = $30
- Risk = $100 - $90 = $10
- R:R = 3:1 — passes the filter

Some practitioners use 3:1 or even 5:1 minimums. The higher the ratio, the fewer trades you take but the higher the quality.

## Risk Budgeting

Risk budgeting allocates a fixed amount of total portfolio risk across positions. Instead of thinking "I'll buy $100K of this stock," you think "I'll allocate 50bps of portfolio risk to this idea."

### Volatility Targeting

Adjust position size so each position contributes approximately equal volatility to the portfolio:

```
Position size = Target vol contribution / Position volatility
```

**Example**: You want each position to contribute 1% weekly volatility to the portfolio.
- Stock A has 3% weekly vol → position size = 1%/3% = 33% of portfolio
- Stock B has 6% weekly vol → position size = 1%/6% = 17% of portfolio
- Stock C has 1.5% weekly vol → position size = 1%/1.5% = 67% of portfolio (likely capped)

This ensures no single position dominates portfolio volatility simply because it's more volatile. The most volatile assets get the smallest positions.

### Equal Risk Contribution (Position-Level Risk Parity)

Each position contributes the same amount of total portfolio risk, accounting for correlations:

```
RC_i = w_i * (Sigma * w)_i / (w' * Sigma * w)
```

Where RC_i is position i's risk contribution, w is the weight vector, and Sigma is the covariance matrix. Set all RC_i equal and solve for weights.

This is more sophisticated than simple volatility targeting because it accounts for how positions interact. A position highly correlated with the rest of the portfolio gets downsized even if its standalone volatility is moderate.

### Maximum Position Loss

The simplest risk budgeting approach: "I'm willing to lose X% of portfolio on this idea."

```
Position size = (Max acceptable loss %) / (Distance to stop-loss %)
```

**Example**: You're willing to lose 2% of portfolio if this trade goes wrong. Your stop is 10% below entry.
- Position size = 2% / 10% = 20% of portfolio

This directly ties position size to your pain threshold. It answers the question: "If this goes completely wrong and I hit my stop, how much of my portfolio do I lose?"

**Common loss budgets by strategy type:**

| Strategy | Max loss per position | Rationale |
|----------|----------------------|-----------|
| Core holdings | 3-5% of portfolio | High conviction, long time horizon |
| Tactical trades | 1-2% of portfolio | Moderate conviction, defined catalyst |
| Speculative/binary | 0.25-0.5% of portfolio | Low probability, high payoff |
| Hedges | N/A (premium is the cost) | Insurance cost, not a loss budget |

## Volatility-Adjusted Position Sizing

Size positions inversely proportional to their volatility. More volatile assets get smaller positions:

```
Position size_i = k / sigma_i
```

Where k is a scaling constant and sigma_i is the asset's volatility (typically annualized standard deviation or ATR).

**Why this works**: Volatility is the best short-term predictor of future volatility. By sizing inversely to volatility, you:
- Equalize the expected dollar risk across positions
- Avoid being dominated by a single volatile position
- Automatically reduce exposure when volatility spikes (if you rebalance)

**ATR-based sizing** (popular with systematic traders):

```
Position size (shares) = (Portfolio value * Risk per position) / (N * ATR)
```

Where ATR is the Average True Range and N is a multiplier (commonly 2-3). This was popularized by the Turtle Traders and remains one of the most robust practical sizing methods.

## Druckenmiller's Concentration Principle

Stanley Druckenmiller's philosophy: **"The way to build long-term returns is through preservation of capital and home runs... When you have tremendous conviction on a trade, you have to go for the jugular."**

This directly contradicts the diversification orthodoxy. Druckenmiller's logic:

1. **Edge is rare**: Genuinely high-conviction, high-edge opportunities occur rarely — perhaps a few times per year.
2. **Diversification dilutes edge**: Spreading capital equally across 50 positions ensures mediocrity. Your best ideas are drowned by your average ones.
3. **Size expresses conviction**: Position size is the primary mechanism for expressing the *magnitude* of your edge, not just its direction.

### Calibrating "Highest Conviction"

The danger of concentration is obvious: what feels like highest conviction may be overconfidence. Calibration criteria:

| Factor | Weak Conviction (small size) | Strong Conviction (large size) |
|--------|------------------------------|-------------------------------|
| Thesis quality | Pattern recognition, analogy | Deep fundamental understanding of causation |
| Variant perception | Consensus-adjacent | Clearly differentiated from market consensus |
| Asymmetry | Symmetric upside/downside | Highly asymmetric (much more upside) |
| Catalyst clarity | Vague timing | Specific catalyst with defined timeline |
| Downside understanding | Unclear what could go wrong | Exhaustive bear case that you've specifically rebutted |
| Edge persistence | Edge might be arbitraged away quickly | Structural edge (behavioral, informational, analytical) |

**The Druckenmiller test**: Can you articulate exactly why the market is wrong, exactly what will change its mind, and exactly what it looks like if you're wrong? If yes to all three, you may have a high-conviction opportunity.

## The Anti-Martingale Principle

A martingale system increases bet size after losses ("doubling down"). An anti-martingale system increases bet size after wins and decreases after losses.

Tudor Jones's axiom: **"Losers average losers."** Averaging down into a losing position is:
- Increasing exposure to a thesis the market is currently disproving
- Concentrating risk at precisely the wrong time
- Psychologically satisfying but financially destructive

**The anti-martingale framework:**

| Scenario | Action | Rationale |
|----------|--------|-----------|
| Position is profitable | Consider adding (pyramiding) | The market is confirming your thesis; let winners run |
| Position is at entry | Hold at current size | No new information |
| Position is at a small loss | Reduce or hold, depending on thesis | Mild negative signal |
| Position is at a large loss | Reduce or exit | Strong negative signal; the market knows something you don't |

**Pyramiding rules** (adding to winners):
1. Only add if the original thesis is playing out as expected
2. Each addition should be smaller than the previous one (inverted pyramid)
3. Move the stop-loss up to protect accumulated profits
4. Total position size should still respect Kelly/risk-budget constraints
5. Never pyramid into a move that's already extended — add on pullbacks within the trend

## Portfolio Heat

Portfolio heat measures the total risk across all open positions. It answers: "If everything goes wrong simultaneously, how much do I lose?"

```
Portfolio heat = Sum of (position size * distance to stop-loss) for all positions
```

**Heat thresholds:**

| Heat Level | Total risk | Action |
|------------|-----------|--------|
| Cool | < 5% portfolio | Room to add positions; may be under-invested |
| Comfortable | 5-10% portfolio | Normal operating range for most strategies |
| Warm | 10-15% portfolio | Approaching limits; only add if conviction is high |
| Hot | 15-20% portfolio | At capacity; no new positions unless one is closed |
| Overheated | > 20% portfolio | Reduce immediately; you're one bad week from trouble |

These thresholds assume uncorrelated positions. If positions are correlated (e.g., all long equities), the effective heat is higher than the arithmetic sum suggests.

**When to stop adding positions:**
1. Portfolio heat exceeds your threshold
2. Adding a new position would increase correlation concentration
3. You're adding because you feel you "should be doing something" rather than because of genuine edge
4. The macro environment has shifted to a regime where your strategy historically underperforms

## Practical Framework: Step-by-Step Position Sizing

For every new position, work through this methodology:

### Step 1 — Define the Setup

- **Entry price**: Where you will buy/sell
- **Stop-loss**: Where the thesis is invalidated (define BEFORE entry)
- **Target**: Where the thesis is fulfilled
- **R:R ratio**: Must be >= 2:1 (Tudor Jones filter)

### Step 2 — Calculate Maximum Position Size (Kelly Ceiling)

- Estimate probability of reaching target vs hitting stop
- Calculate Kelly fraction: `f* = (bp - q) / b`
- Apply fractional Kelly: use half-Kelly as default, quarter-Kelly if uncertain

### Step 3 — Calculate Risk-Budget Position Size

- Determine risk budget for this position type (1-2% for tactical, 0.5% for speculative)
- Calculate: `Position size = Risk budget / Distance to stop`
- This is typically more conservative than Kelly — **use the smaller of Kelly and risk-budget sizes**

### Step 4 — Apply Volatility Adjustment

- Measure the position's recent volatility (20-day realized vol or ATR)
- Compare to portfolio average volatility
- If position vol is 2x portfolio average, halve the size from Step 3

### Step 5 — Apply Conviction Multiplier

- Score conviction using the calibration table above
- Weak conviction: 0.5x the Step 4 size
- Moderate conviction: 1.0x (no adjustment)
- High conviction (Druckenmiller-level): up to 1.5x — but never above Kelly ceiling from Step 2

### Step 6 — Check Portfolio Heat

- Add this position's risk to existing portfolio heat
- If total heat exceeds your threshold, reduce size or defer entry
- Check correlation with existing positions — if highly correlated, reduce further

### Step 7 — Document and Commit

- Record: entry, stop, target, position size, thesis, conviction level
- This becomes your accountability record
- The stop is now inviolable unless the thesis fundamentally changes (not the price)

### Summary Decision Tree

```
Start
  |
  v
R:R >= 2:1? --No--> Pass on trade
  |
  Yes
  v
Calculate Kelly ceiling (fractional)
  |
  v
Calculate risk-budget size
  |
  v
Take the SMALLER of Kelly and risk-budget
  |
  v
Adjust for volatility (size inversely to vol)
  |
  v
Adjust for conviction (0.5x to 1.5x)
  |
  v
Check portfolio heat --Overheated--> Defer or reduce
  |
  OK
  v
Enter position, document everything
```

## Related Skills

- **`drawdown-psychology`** (Risk Architecture) — consult when calibrating loss tolerance and uncle points that determine maximum position size; psychological limits override mathematical optima
- **`correlation-regimes`** (Risk Architecture) — consult when sizing positions within a portfolio context; correlated positions require smaller individual sizes than uncorrelated ones
- **`tail-risk`** (Risk Architecture) — consult when sizing convex bets and tail hedges where standard Kelly and risk-budget frameworks need adaptation for asymmetric payoffs
