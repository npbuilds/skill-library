# Rebalancer — Decision Rules

## Constants (from frontmatter)

| Constant | Value |
|---|---|
| `target_weights` | `{SPY: 0.50, QQQ: 0.30, BND: 0.20}` |
| `drift_thresholds.normal` | `0.025` (2.5%) |
| `drift_thresholds.panic` | `0.10` (10%) |
| `per_tick_clamp_pct` | `0.10` (10% of account value) |
| `max_slippage_pct` | `0.5` (per intent) |

## Drift formula

```
current_weight[s] = (positions[s].quantity * quotes[s].last_trade_price) / total_value
delta_pct[s]      = target_weights[s] - current_weight[s]
delta_usd[s]      = delta_pct[s] * total_value
```

## Firing rules

| Cadence | Condition | Fire? |
|---|---|---|
| First-of-month tick | `abs(delta_pct) >= 0.025` for any symbol | Yes |
| First-of-month tick | All drift < 0.025 | No (clean tick) |
| Mid-month tick | `abs(delta_pct) >= 0.10` for any symbol | Yes (panic) |
| Mid-month tick | All drift < 0.10 | No |

## Clamp formula

```
delta_usd = max(-account_value * 0.10, min(delta_usd, account_value * 0.10))
```

Effect: a single tick rebalances at most 10% of the portfolio. Multi-tick convergence is intentional.

## Order-of-operations

When emitting both buy and sell intents in the same tick, sells go first in the intent array. The executor processes them in order, freeing buying power before the buys evaluate. (The executor's per-name cap is buying-power-based; selling first widens the cap for the buys.)

## Allowlist-contraction handling

```
held_symbols = {p.symbol for p in positions if p.quantity > 0}
target_symbols = set(target_weights.keys())

for symbol in held_symbols - target_symbols:
    if symbol not in allowlist: skip (something else put us in it; let user resolve)
    delta_pct = -current_weight[symbol]
    if abs(delta_pct) < drift_thresholds.normal: skip
    emit sell intent for full position (clamp applies)
```

## Anti-rules

| Refused action | Reason |
|---|---|
| Rebalance more than once per day in normal cadence | Cadence guard. |
| Trade outside allowlist | Hard rule. |
| TLH-style coordinated buy/sell within 30 days | Out of scope v1. |
| Override target weights at runtime | Frontmatter constant. |

## State file shape

`~/.hermes/profiles/autotrader/state/rebalancer.json`:

```json
{
  "last_normal_cadence_at": "2026-06-01T14:00:00-04:00",
  "last_panic_fire_at": "2026-04-12T14:30:00-04:00",
  "rebalance_count": 3
}
```
