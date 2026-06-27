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
| `allow_cap_downsize` | optional, default `false` | When `true`, the executor's per-name cap may trim the order to fit `max_position_pct` without aborting at the phase 3.5 intent-drift check. Strategists that explicitly opt in to "fill at smaller size" accept the cap-shrunk order; strategists that don't get an `intent_drift_aborted` action when the cap would trim by more than 1%. Most strategists should leave this `false` — accidental cap trims are usually a bug, not a feature. |
| `allow_multiple_per_symbol` | optional, default `false` | **Not currently supported.** Reserved for a future v0.3 change. Today the executor's phase 2.0 always drops same-symbol duplicates with `status: "duplicate_symbol_in_tick"`. Setting this `true` has no effect and is silently ignored. Strategists that need split-order semantics must split across ticks. |

### Optional opt-in flags

Both flags above are *strategist opt-ins* to behavior that's otherwise blocked by the executor's safety contract. They are not safety overrides — they shift the trade-off between "this order is bigger/smaller than I asked for" and "the order didn't happen". A strategist sets them when its decision rules already accommodate the alternative outcome.

- **Set `allow_cap_downsize: true`** when the strategist would rather get *some* exposure than none. Example: a rebalancer trimming an overweight position can accept a smaller trim than requested.
- **Leave `allow_cap_downsize` unset (default `false`)** when the strategist's sizing is load-bearing for the strategy thesis. Example: DCA tranches are calibrated; a smaller tranche distorts the schedule. Better to abort and log than to silently underweight.

### What strategists must NOT do

- Call `review_equity_order`, `place_equity_order`, `review_option_order`, `place_option_order`, `cancel_equity_order`, `cancel_option_order`, or `add_to_watchlist` directly. These are executor-exclusive.
- Emit intents for symbols outside their declared `allowlist`. The executor will reject, but it's a bug to emit them at all.
- Emit intents for `asset_class: "option-l2"` from a strategist whose `profile_compatibility` doesn't include an options-permitted profile.
- Emit more than `max_concurrent_positions` distinct symbols per tick (executor will trim).

## Executor return shape

The executor returns a structured envelope, NOT a bare `RealizedAction[]`. The envelope carries pre-flight outcomes (`aborted`, `circuit_breaker_tripped`) AND the realized actions in one object:

```json
{
  "aborted": null,
  "circuit_breaker_tripped": false,
  "account_value": 1000.00,
  "buying_power": 998.50,
  "actions": [
    {
      "symbol": "SPY",
      "side": "buy",
      "quantity_type": "notional",
      "qty": 0.103,
      "notional_usd": 50.00,
      "original_qty": null,
      "original_notional_usd": 50.00,
      "intent_price": 481.50,
      "realized_review_price": 482.07,
      "status": "placed",
      "reason": "DCA tranche 2 of 4 for the week",
      "order_id": "f3a8...",
      "alerts": []
    }
  ]
}
```

### Envelope field semantics

| Field | Required | Notes |
|---|---|---|
| `aborted` | always | One of: `null`, `promotion_blocked`, `mode_mismatch`, `manifest_missing`, `manifest_path_invalid`, `manifest_identity_mismatch`, `account_lock_failed`, `capability_gated`, `outside_time_window`, `profile_compatibility_failed`, `broker_unavailable`, `data_anomaly`. When non-null, `actions` MUST be `[]` and no broker call was made. The strategist propagates this to `tick_decision.aborted`. |
| `circuit_breaker_tripped` | always | True if SOUL's daily-loss circuit breaker fired in pre-flight. When true, only close-side intents survive. |
| `account_value` | non-aborted ticks only | From `get_portfolio.total_value` captured at the start of the tick. 0 when `aborted`. |
| `buying_power` | non-aborted ticks only | From `get_portfolio.buying_power.buying_power`. 0 when `aborted`. |
| `actions` | always | Array of RealizedAction. Empty when `aborted`. |

### RealizedAction field semantics

- `qty` and `notional_usd` are always both populated in the return, even when only one was in the input. The executor computes the other from the live quote.
- `original_qty` and `original_notional_usd` are the strategist's pre-cap values, captured at phase 2.4 entry. The drift check at phase 3.5 compares against these. Whichever doesn't apply to the intent's `quantity_type` is `null`.
- `status` reflects what actually happened. Valid values (matched verbatim to SOUL):
  - `reviewed`, `placed`, `skipped`, `review_anomaly`, `slippage_aborted`
  - `intent_drift_aborted` (phase 3.5 — SOUL 1% rule)
  - `duplicate_symbol_in_tick` (phase 2.0 — SOUL one-per-symbol rule)
  - `place_failed` (phase 4 — broker rejected or 5xx twice)
- `order_id` is populated only on `status: placed`. May be present-but-failed on `status: place_failed` if the broker returned an id with the error.
- `alerts` carries Robinhood's `order_checks` array verbatim — useful for the strategist to log but not act on (the executor has already adjudicated them).

The strategist embeds the envelope's `actions` array directly into its `tick_decision.actions` JSON block, and copies `aborted`, `circuit_breaker_tripped`, `account_value`, `buying_power` to the tick_decision top-level.
