---
name: rebalancer
type: strategist
description: >
  Maintains a target asset-weight basket via drift-triggered rebalancing. Emits both
  buy and sell intents (the only strategist in v1 that sells). Monthly cadence by
  default; off-cadence ticks fire only if drift exceeds the panic threshold. Use
  when the user asks "rebalance my book", "am I overweight X", or "bring me back
  to target". Default mode is review-only.
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash
strategist:
  mode: review
  asset_class: equity
  account_lock: "619508153"
  time_window: "09:35-15:55 America/New_York"
  cron_hint: "0 14 1 * *"
  allowlist: [SPY, QQQ, BND, VTI, VOO]
  max_position_pct: 70
  max_concurrent_positions: 5
  capability_requires: []
  assumes:
    fractional_shares: true   # cash individual accounts on Robinhood; not a capability the broker reports
  profile_compatibility: [autotrader]
  requires_directors: [portfolio-construction, risk-architecture]
target_weights:
  SPY: 0.50
  QQQ: 0.30
  BND: 0.20
drift_thresholds:
  normal: 0.025
  panic: 0.10
per_tick_clamp_pct: 0.10
---

# Rebalancer

Keeps the portfolio at a target weight by computing drift and emitting just-enough trades to close the gap. This is the only strategist in v1 that emits `side: sell` — it sells the overweight, buys the underweight. See `_shared/position-sizing.md` §"Target-weight rebalance" for the canonical formula.

> Required: `_shared/intent-schema.md`, `_shared/circuit-breakers.md`, `_shared/position-sizing.md`. See `references/decision-rules.md` for the numeric rules.

## Strategy summary

- **Target weights:** SPY 50%, QQQ 30%, BND 20% (matches `dca-investor` basket).
- **Drift thresholds:** Normal 2.5% — fire only on first-of-month. Panic 10% — fire any tick.
- **Per-tick clamp:** Trade no more than 10% of account value in a single tick (prevents lurching on noisy days).
- **Cadence:** Monthly (first trading day) for normal drift; off-cadence is allowed only when drift exceeds panic.
- **Tax-loss harvesting:** Out of scope for v1. A future v2 may check `get_equity_positions` for unrealized losses on the overweight before selling.

## 6-phase protocol

### Phase 1 — Pre-flight (strategist-side gate)

1. Determine cadence: is today the first trading day of the calendar month? Check via `get_equity_quotes` last-trade dates to identify the first session of the month.
2. If yes: proceed to phase 2 (normal cadence path).
3. If no: continue to phase 2 anyway, but mark this tick as `panic_only` — phase 4 will only emit intents if some symbol's drift exceeds `panic` threshold.

### Phase 2 — Compose context

Invoke `portfolio-construction` with: *"Three-line summary of current weight philosophy — equity/bond/cash, tilt, hedges."* Then `risk-architecture` with: *"Anything in current positions that suggests trimming faster or slower than normal?"*

Both responses go into `tick_decision.notes`. They do NOT change the numeric rules in v1.

### Phase 3 — Signal gather

Parallel calls:

- `get_equity_positions(account_number=619508153)` — current shares per symbol.
- `get_portfolio(account_number=619508153)` — `total_value` for the denominator.
- `get_equity_quotes(symbols=allowlist)` — current prices to value positions.

Compute current weights:

```
position_value[symbol] = positions[symbol].quantity * quotes[symbol].last_trade_price
current_weight[symbol] = position_value[symbol] / total_value
```

### Phase 4 — Decide

For each symbol in `target_weights`:

```
delta_pct = target_weight - current_weight

if panic_only and abs(delta_pct) < drift_thresholds.panic: skip this symbol
if abs(delta_pct) < drift_thresholds.normal: skip this symbol

delta_usd = delta_pct * total_value
delta_usd = clamp(delta_usd, -total_value * per_tick_clamp_pct, total_value * per_tick_clamp_pct)

intent = {
    "symbol": symbol,
    "side": "buy" if delta_usd > 0 else "sell",
    "quantity_type": "notional",
    "notional_usd": abs(delta_usd),
    "order_type": "market",
    "intent_price": quotes[symbol].last_trade_price,
    "max_slippage_pct": 0.5,
    "time_in_force": "gfd",
    "reason": f"Drift {delta_pct*100:+.1f}% from target {target_weight*100:.0f}%",
    ...
}
```

Symbols in `allowlist` but NOT in `target_weights` are checked: if held, emit a sell intent to liquidate (drift = -current). This handles allowlist contraction.

### Phase 5 — Hand off to executor

Standard envelope to `_shared/executor`. The executor enforces buying-power on the buy side and sellable-shares on the sell side.

### Phase 6 — Emit & persist

Write `tick_decision`. State file at `~/.hermes/profiles/autotrader/state/rebalancer.json` records:

```json
{
  "last_normal_cadence_at": "<ISO>",
  "last_panic_fire_at": "<ISO>",
  "rebalance_count": <int>
}
```

`last_normal_cadence_at` updates on every normal-cadence run (regardless of whether any intents fired). `last_panic_fire_at` updates only when a panic intent placed.

## Interactive mode

- "Am I drifting?" — run phases 1-4, emit `tick_decision` with `actions: []` if no drift exceeds threshold, otherwise show what *would* fire. Always review-only.
- "Force rebalance now" — refuse. Cadence is the cadence. Operator can edit frontmatter or wait for next first-of-month.
- "What's my current allocation?" — compute current_weight per symbol and present as a table. Do NOT emit intents.

## What this strategist will never do

- Trade tax-inefficiently in v1 (no TLH check — just sells overweight).
- Trade outside the allowlist.
- Buy and sell the same symbol in one tick.
- Run more than once per day in normal-cadence mode.
- Fire on a non-first-of-month unless panic drift is hit.
