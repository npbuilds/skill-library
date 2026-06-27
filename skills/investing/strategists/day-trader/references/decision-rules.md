# Day Trader — Decision Rules

## Constants

| Constant | Value |
|---|---|
| `opening_range_minutes` | 15 (09:30-09:45 ET) |
| `vwap_confirmation_required` | true |
| `hard_exit_at` | 15:55 ET |
| `max_position_pct` | 30 |
| `max_concurrent_positions` | 1 (whole allowlist) |
| `max_slippage_pct` (per intent) | 0.3 |

## Opening Range computation

```
bars_in_or = bars where 09:30 <= bar.timestamp < 09:45 ET
or_high    = max(bar.high for bar in bars_in_or)
or_low     = min(bar.low  for bar in bars_in_or)
```

If fewer than 3 bars in OR window: skip (data anomaly).

## VWAP computation

```
cumulative_pv  = sum(bar.typical_price * bar.volume for bar in today's bars so far)
cumulative_v   = sum(bar.volume for bar in today's bars so far)
vwap           = cumulative_pv / cumulative_v   (if cumulative_v > 0 else null)

# typical_price = (high + low + close) / 3 per bar
```

If `vwap` is null or `cumulative_v == 0`: skip (data anomaly).

## Entry condition

```
breakout = current_close > or_high
vwap_ok  = (not vwap_confirmation_required) or (current_close > vwap)
entry    = breakout AND vwap_ok
```

When `microstructure response contains "choppy"`: require `current_close > or_high * 1.001` (an extra 10bps cushion) to reduce false breakouts.

## Exit conditions (per open position)

| Trigger | Action | Reason tag |
|---|---|---|
| `current_price <= stop_price` | Sell full qty | `stop_hit` |
| `current_price >= target_price` | Sell full qty | `target_hit` |
| `now >= 15:55 ET` | Sell full qty (market) | `hard_close` |

Stops are evaluated as soft alerts — the strategist emits a market sell intent when triggered; it does NOT use Robinhood's stop-loss order type. This keeps execution in the executor's review→place path with slippage check.

## Target / Stop calculation

```
stop_price   = or_low
target_price = or_high + (or_high - or_low)
```

Risk/reward = 1:1 if entry exactly at breakout. Often better in practice because entry includes slippage above breakout.

## Anti-rules

| Refused | Reason |
|---|---|
| Pyramid into a winner | Max 1 position. |
| Re-enter after stop | One entry per day, period. |
| Hold overnight | 15:55 hard-close enforced. |
| Short sell | Cash account. |
| Trade pre-OR or post-hard-close | Time window. |

## State file shape

`~/.hermes/profiles/autotrader/state/day-trader.json`:

```json
{
  "open_position": {
    "symbol": "NVDA",
    "qty": 3,
    "opened_at": "2026-06-26T10:35:00-04:00",
    "entry_price": 122.40,
    "stop_price": 121.00,
    "target_price": 124.20,
    "order_id": "..."
  } | null,
  "today_entry_attempted": true,
  "today_date": "2026-06-26",
  "closed_today": [
    {"symbol": "...", "pnl_pct": -0.012, "reason": "stop_hit"}
  ]
}
```

`today_date` ensures the state resets when a new day begins. Any tick whose `today_date != now.date()` clears `open_position`, `today_entry_attempted`, and `closed_today` before evaluating.
