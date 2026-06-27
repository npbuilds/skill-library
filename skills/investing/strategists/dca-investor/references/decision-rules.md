# DCA Investor — Decision Rules

The explicit numeric rules, separated from prose so they're auditable and (eventually) testable.

## Constants (from frontmatter)

| Constant | Value | Source |
|---|---|---|
| `account_lock` | `"619508153"` | frontmatter |
| `tranche_size_usd` | `50.00` | frontmatter `tranche_size_usd` |
| `basket` | `{SPY: 0.50, QQQ: 0.30, BND: 0.20}` | frontmatter `basket` |
| `cadence` | `weekly_monday` | frontmatter `cadence` |
| `time_window` | `09:35-15:55 America/New_York` | frontmatter |
| `max_position_pct` | `50` | frontmatter |
| `max_slippage_pct` | `1.0` | hard-coded per intent |
| `circuit_breaker_loss_pct` | `5.0` | inherited from SOUL |

## Per-symbol notional

```
for symbol, weight in basket.items():
    notional_usd[symbol] = round(tranche_size_usd * weight, 2)
```

Resulting per-tick intent set:

| Symbol | Notional |
|---|---|
| SPY | 25.00 |
| QQQ | 15.00 |
| BND | 10.00 |

## Cadence

A tick is **placement-eligible** when ALL hold:

1. Current day-of-week (in `America/New_York`) is Monday.
2. Current time is inside the strategist's `time_window`.
3. Today is not a US market holiday (executor handles this implicitly — `get_equity_quotes` will return stale prices on a holiday; the strategist double-checks by reading the quote's `last_trade_at` and rejecting if it's not today).
4. At least 6 calendar days have elapsed since the last successful tick (read from `~/.hermes/profiles/autotrader/state/dca-investor.json`).
5. The strategist's mode allows it (in `review` mode, placement-eligible means "will be reviewed", not actually placed).

If any condition fails: skip the tick with the structured reason.

## State file shape

`~/.hermes/profiles/autotrader/state/dca-investor.json`:

```json
{
  "last_placed_at": "2026-06-23T14:00:00-04:00",
  "last_placed_actions": [
    {"symbol": "SPY", "qty": 0.052, "notional_usd": 25.00, "order_id": "..."},
    {"symbol": "QQQ", "qty": 0.038, "notional_usd": 15.00, "order_id": "..."},
    {"symbol": "BND", "qty": 0.137, "notional_usd": 10.00, "order_id": "..."}
  ],
  "tick_count": 7
}
```

Updated only when at least one action lands `status: placed`. Reviewed-only ticks do not touch this file.

## Anti-rules (things this strategist will refuse to do)

| Refused action | Reason |
|---|---|
| Skip a Monday because regime looks bad | DCA is unconditional. Regime is logged, not gated. |
| Buy extra after a drawdown | No martingale. |
| Sell any holdings | DCA is one-way; sells are out of scope. |
| Trade off-basket symbols | The basket is the basket. Edit frontmatter to change it. |
| Trade in extended hours | Notional orders require `regular_hours`; `time_window` enforces. |
| Run from non-Monday | Cadence guard. |
| Tranche-size override at runtime | Frontmatter constant. |

## Edge cases

### First-ever tick

`state/dca-investor.json` doesn't exist. Treat last-placement as the Unix epoch → 6-day check trivially passes. Proceed normally.

### Holiday Monday

`get_equity_quotes` returns stale `last_trade_at` (Friday's close). Strategist detects: `last_trade_at` date != today's date → skip with `notes: "holiday — no fresh quotes"`. Do not update state.

### Cadence skipped (e.g. Hermes was down for 2 weeks)

Cadence guard only requires `>= 6 days` — it doesn't double-up to "catch up." A 2-week outage produces exactly one tick on the first Monday Hermes comes back. The user can manually trigger a catch-up by deleting state.

### Buying power below tranche size

If `buying_power < tranche_size_usd`, the per-name caps will downsize each intent proportionally via the executor. If the resulting intents are too small to be useful (notional < $1), they're dropped with `reason: "below_min_size_after_cap"`. The tick still emits a clean `tick_decision` — just with zero placed actions.
