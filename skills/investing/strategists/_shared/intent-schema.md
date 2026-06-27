# Intent Schema (strategist → executor contract)

The single source of truth for how a strategist hands trade ideas to the executor. Every strategist emits this shape; the executor consumes it. Nothing else.

## Payload

```json
{
  "strategy": "<skill-name>",
  "mode": "review|live",
  "context_hint": "cron|chat|claude-code",
  "intents": [ <Intent>, ... ]
}
```

- `strategy` — the strategist skill name (e.g. `"dca-investor"`). Used by the executor for logging and for SOUL invariant lookups.
- `mode` — strategist's declared mode from frontmatter. `live` is *advisory only*; the executor enforces the actual run-context rules and may downgrade to `review` regardless. A strategist whose frontmatter says `mode: review` can never be placed live in any context.
- `context_hint` — the strategist's best guess at the run context. The executor verifies this against environment signals (`HERMES_CRON_RUN_ID`, presence of TTY, Claude Code session markers) and overrides if the hint is wrong.
- `intents` — zero or more `Intent` objects. Empty array is valid and common (no-op tick).

## Intent

```json
{
  "symbol": "SPY",
  "side": "buy|sell",
  "quantity_type": "shares|notional",
  "qty": 1.5,
  "notional_usd": 50.00,
  "order_type": "market|limit",
  "limit_price": 482.10,
  "intent_price": 481.50,
  "max_slippage_pct": 0.5,
  "time_in_force": "gfd|gtc",
  "reason": "DCA tranche 2 of 4 for the week",
  "expires_at": "2026-06-26T15:55:00-04:00",
  "asset_class": "equity|option-l2",
  "option_leg": null
}
```

### Field semantics

| Field | Required when | Notes |
|---|---|---|
| `symbol` | always | Uppercase ticker. Executor validates against the strategist's `allowlist`. |
| `side` | always | `"buy"` or `"sell"`. Sells require an existing position (no shorting). |
| `quantity_type` | always | `"shares"` or `"notional"`. |
| `qty` | quantity_type == "shares" | Decimal allowed. Robinhood supports fractional on `type: market` + `regular_hours`. For non-fractional eligibility, executor rounds down. |
| `notional_usd` | quantity_type == "notional" | USD cost ceiling. Robinhood's `dollar_amount` parameter on `place_equity_order` consumes this directly (market + regular_hours only). |
| `order_type` | always | `"market"` or `"limit"`. Notional orders must be market. |
| `limit_price` | order_type == "limit" | Price ceiling for buys, floor for sells. |
| `intent_price` | always | Strategist's reference price at decision time. Used for slippage check. |
| `max_slippage_pct` | always | Executor aborts the action with `status: slippage_aborted` if `(realized_review_price - intent_price) / intent_price * 100` exceeds this for buys (or the inverse for sells). 0.5 is a typical default. |
| `time_in_force` | always | `"gfd"` (good-for-day) or `"gtc"` (good-till-cancelled). |
| `reason` | always | One-line human-readable explanation. Lands in `tick_decision`. |
| `expires_at` | always | ISO-8601 timestamp. If the executor evaluates the intent after this, it skips with `status: skipped` and `reason: "expired"`. |
| `asset_class` | always | `"equity"` for stocks/ETFs. `"option-l2"` for single-leg options (only valid when the strategist's `profile_compatibility` includes `options-trader` AND the loaded profile is `options-trader`). |
| `option_leg` | asset_class == "option-l2" | Object with `option_id`, `position_effect: open\|close`, `ratio_quantity` (defaults to 1). The executor calls `get_option_instruments` to validate. |

### What strategists must NOT do

- Call `review_equity_order`, `place_equity_order`, `review_option_order`, `place_option_order`, `cancel_equity_order`, `cancel_option_order`, or `add_to_watchlist` directly. These are executor-exclusive.
- Emit intents for symbols outside their declared `allowlist`. The executor will reject, but it's a bug to emit them at all.
- Emit intents for `asset_class: "option-l2"` from a strategist whose `profile_compatibility` doesn't include an options-permitted profile.
- Emit more than `max_concurrent_positions` distinct symbols per tick (executor will trim).

## Executor return shape

The executor returns `RealizedAction[]` back to the calling strategist:

```json
[
  {
    "symbol": "SPY",
    "side": "buy",
    "quantity_type": "notional",
    "qty": 0.103,
    "notional_usd": 50.00,
    "intent_price": 481.50,
    "realized_review_price": 482.07,
    "status": "placed",
    "reason": "DCA tranche 2 of 4 for the week",
    "order_id": "f3a8...",
    "alerts": []
  }
]
```

- `qty` and `notional_usd` are always both populated in the return, even when only one was in the input. The executor computes the other from the live quote.
- `status` reflects what actually happened: `reviewed`, `placed`, `skipped`, `review_anomaly`, `slippage_aborted`.
- `order_id` is populated only on `status: placed`.
- `alerts` carries Robinhood's `order_checks` array verbatim — useful for the strategist to log but not act on (the executor has already adjudicated them).

The strategist embeds this array directly into its `tick_decision.actions` JSON block.
