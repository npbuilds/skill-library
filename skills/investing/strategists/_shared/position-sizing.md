# Position Sizing

How strategists translate a directional signal into a notional or share quantity. The executor enforces the absolute ceilings; this doc defines the *strategy-level* sizing logic strategists use to fill in the `qty` / `notional_usd` fields on each `Intent`.

## Inputs

- `buying_power` — live from `get_portfolio` at tick start. Hard ceiling per SOUL.
- `max_position_pct` — strategist frontmatter. Per-name fraction of buying power.
- `max_concurrent_positions` — strategist frontmatter. Cap on distinct symbols open.
- `conviction` — strategist's internal score on the signal. Typically `[0.0, 1.0]`.
- `cost_basis_in_name` — optional, from `get_equity_positions`. Used by strategies that scale into a position.

## Three sizing modes

### 1. Fixed notional (DCA, rebalancer top-up)

A flat dollar amount per tranche.

```
intent.quantity_type = "notional"
intent.notional_usd  = min(tranche_size_usd, buying_power * max_position_pct)
```

When `buying_power * max_position_pct < tranche_size_usd`, the strategist either:
- emits a smaller intent (preferred for DCA — partial fill of the schedule), or
- emits zero intents this tick and logs the reason (preferred for rebalancers — don't lurch).

### 2. Conviction-scaled (swing, day, reflexivity)

Scale into a position by conviction.

```
target_notional = buying_power * max_position_pct * conviction
intent.quantity_type = "shares"
intent.qty           = floor(target_notional / current_quote.last_trade_price)
```

`floor` because integer shares are required outside fractional-eligible orders. If `qty == 0`, skip — don't emit a one-cent token order.

### 3. Target-weight rebalance (rebalancer, macro-overlay)

Move toward a target weight; emit only the *delta*.

```
current_pct  = position_value / account_value
target_pct   = strategist_target_weights[symbol]
delta_pct    = target_pct - current_pct

# Only act if delta exceeds a drift threshold (default 2.5%):
if abs(delta_pct) < 0.025: skip

# Notional to trade:
delta_usd = delta_pct * account_value

# Cap per-tick rebalance magnitude (prevents lurching on noisy days):
delta_usd = clamp(delta_usd, -account_value * 0.10, account_value * 0.10)

intent.side          = "buy" if delta_usd > 0 else "sell"
intent.quantity_type = "notional"
intent.notional_usd  = abs(delta_usd)
```

## The Kelly-light constraint (for risk-managed strategists)

When a strategist has a defined edge (win probability `p`, win/loss ratio `b`), Kelly fraction is `f* = p - (1-p)/b`. We use a fractional-Kelly cap to avoid the well-known volatility of full Kelly:

```
kelly_fraction = max(0, p - (1-p) / b)
size_fraction  = min(max_position_pct, 0.25 * kelly_fraction)   # quarter-Kelly cap
```

Most strategists in this suite don't compute Kelly because their edge isn't quantified. They use the fixed-notional or conviction-scaled modes above. Kelly is documented here for strategists that *do* have a backtested edge (none yet).

## What never happens

- **No leverage.** Notional must not exceed `buying_power`. Executor enforces.
- **No short selling.** `side: sell` requires an existing position with `quantity_available_for_sells >= intent.qty`. Executor enforces.
- **No size-up after a loss.** Martingale-style increase after a losing trade is forbidden. If a strategist wants to scale into a name, it does so at decision time based on conviction, not based on prior P&L.
- **No emergency upsizing.** "The trade looks really good" is not a reason to exceed `max_position_pct`. The cap is hard.

## Examples

### DCA into SPY with $50 weekly tranches

```json
{
  "quantity_type": "notional",
  "notional_usd": 50.00,
  "order_type": "market",
  "reason": "Weekly DCA tranche 1 of 4"
}
```

### Conviction-scaled swing buy on NVDA, conviction 0.6, max_position_pct 25%, buying_power $1000, NVDA at $120

```
target_notional = 1000 * 0.25 * 0.6 = $150
qty = floor(150 / 120) = 1 share
```

```json
{
  "quantity_type": "shares",
  "qty": 1,
  "order_type": "limit",
  "limit_price": 120.50,
  "reason": "Swing entry — RSI(14) crossed up from 28; conviction 0.6"
}
```

### Rebalance from current 70% VTI / 30% BND toward target 60% / 40%, account_value $1000

```
VTI delta_pct = -0.10  →  delta_usd = -$100   →  sell $100 of VTI
BND delta_pct = +0.10  →  delta_usd = +$100   →  buy $100 of BND
```

Both clamped within ±$100 (10% of $1000), no action needed. Two intents emitted.
