# Swing Trader — Decision Rules

## Constants

| Constant | Value |
|---|---|
| `rsi.period` | 14 |
| `rsi.oversold` | 30 |
| `rsi.overbought` | 70 |
| `hold.max_days` | 10 (trading days) |
| `sizing.conviction_floor` | 0.3 |
| `sizing.conviction_ceiling` | 1.0 |
| `max_position_pct` | 25 |
| `max_concurrent_positions` | 3 |
| `max_slippage_pct` (per intent) | 0.3 |

## RSI(14) computation

```
returns[i] = bars[i].close - bars[i-1].close
gains  = average over last 14 of max(returns[i], 0)
losses = average over last 14 of abs(min(returns[i], 0))
if losses == 0: RSI = 100
else: RSI = 100 - 100 / (1 + gains/losses)
```

Use Wilder's smoothing (first 14 simple-average, subsequent recursive) for parity with most charting platforms.

## Conviction → sizing

```
conviction = (oversold - current_rsi) / oversold
conviction = clamp(conviction, conviction_floor, conviction_ceiling)
if microstructure response contains "momentum_dominant": conviction *= 0.5

target_notional = buying_power * max_position_pct/100 * conviction
qty = floor(target_notional / quote.last_trade_price)
```

Example: RSI 22 → `conviction = (30-22)/30 = 0.27`, clamped up to floor `0.3`. With $1000 BP and 25% cap: target = $1000 * 0.25 * 0.3 = $75. NVDA at $120 → qty = 0. Skip.

Example: RSI 15 → `conviction = 0.5`. Target = $125. NVDA $120 → qty = 1. Emit.

## Exit rules

| Condition | Action |
|---|---|
| `current_rsi >= overbought` | Sell full position. reason: `rsi_revert`. |
| `position age >= max_days` (trading days) | Sell full position. reason: `max_age`. |
| `tick_count == 1` after promotion to live | NO automatic close of pre-existing manual positions. |

## Anti-rules

| Refused | Reason |
|---|---|
| Stop-loss orders | Exits are rule-driven, not price-triggered. |
| Average down on existing swing position | Strategist sees symbol is held and skips re-entry. |
| Short selling | Cash account; SOUL hard rule. |
| Hold past `max_days` | Force-close on the next eligible tick. |
| Trade outside allowlist | Hard rule. |

## State file shape

`~/.hermes/profiles/autotrader/state/swing-trader.json`:

```json
{
  "open_positions": [
    {"symbol": "AAPL", "opened_at": "2026-06-20T14:00:00-04:00", "qty": 1, "entry_rsi": 22.4, "entry_price": 184.50, "order_id": "..."}
  ],
  "closed_count_30d": 4,
  "win_rate_30d": 0.5
}
```

The strategist updates `closed_count_30d` and `win_rate_30d` on every sell (used for telemetry; not a circuit breaker in v1).
