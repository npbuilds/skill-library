# Earnings Event Trader — Decision Rules

## Constants

| Constant | Value |
|---|---|
| `gap_down_threshold_pct` | 2.0 |
| `exit_target_pct` | 3.0 |
| `exit_max_days` | 5 (trading days) |
| `max_position_pct` | 25 |
| `max_concurrent_positions` | 2 |
| `max_slippage_pct` (per intent) | 0.5 |

## Trigger condition

```
beat   = report.actual_eps > report.estimated_eps
gap    = (quote.current_price - quote.prior_close) / quote.prior_close * 100
trigger = beat AND gap <= -gap_down_threshold_pct
```

A "beat" requires both EPS values present and not null. If either is null: skip with `data_anomaly`.

## Position lifecycle

| Trigger | Action |
|---|---|
| Trigger condition met, not held | Buy at current+0.1% limit |
| `pnl_pct >= 3` | Sell market |
| `age_days >= 5` | Sell market |
| Regime says "beats_punished_broadly" | Skip new entries; existing positions still exit by rules |

## Anti-rules

| Refused | Reason |
|---|---|
| Trade on a miss | Thesis doesn't apply. |
| Trade on a gap up | Fade is one-directional. |
| Pre-earnings entry | Strategy is post-event. |
| Hold past 5 days | Force exit. |
| Average down | Single entry per name; ignore re-triggers. |

## State file shape

`~/.hermes/profiles/autotrader/state/earnings-event-trader.json`:

```json
{
  "open_positions": [
    {"symbol": "NVDA", "opened_at": "2026-06-25T14:00:00-04:00", "qty": 1, "entry_price": 118.50, "trigger_gap_pct": -3.2, "order_id": "..."}
  ],
  "today_evaluated": "2026-06-26",
  "closed_30d": [
    {"symbol": "AAPL", "pnl_pct": 0.031, "reason": "target_hit", "days_held": 3}
  ]
}
```
