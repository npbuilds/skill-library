# tick_decision Emitter Contract

Every strategist's final output is exactly one JSON block titled `## tick_decision`. The autotrader profile's `SOUL.md` treats absence of this block as a crash. This file is the canonical reference.

## Exact shape

```json
{
  "tick_utc": "<ISO-8601>",
  "strategy": "<skill name>",
  "mode": "review|live",
  "account_value": <number>,
  "buying_power": <number>,
  "actions": [ <RealizedAction>, ... ],
  "circuit_breaker_tripped": <bool>,
  "aborted": "<reason>|null",
  "notes": "<short>"
}
```

## Field rules

| Field | Source | Notes |
|---|---|---|
| `tick_utc` | strategist captures at start of phase 1 | RFC 3339 UTC. |
| `strategy` | strategist `name` from frontmatter | Verbatim. |
| `mode` | strategist `mode` from frontmatter | The *declared* mode, not what the executor actually did. The executor's actual behavior shows up in `actions[].status`. |
| `account_value` | from pre-flight `get_portfolio` | `total_value` field. Capture once at tick start, never re-fetch mid-tick. |
| `buying_power` | from pre-flight `get_portfolio` | `buying_power.buying_power` field. |
| `actions` | executor's `RealizedAction[]` return | Verbatim. Empty `[]` is valid. |
| `circuit_breaker_tripped` | pre-flight | True if today's realized P&L ≤ −5% of day-start portfolio value. When true, only close-side actions are permitted. |
| `aborted` | pre-flight | One of: `null`, `"account_lock_failed"`, `"capability_gated"`, `"outside_time_window"`, `"profile_compatibility_failed"`. When non-null, `actions` MUST be `[]` and no broker calls were made. |
| `notes` | strategist | One short sentence at most. Use for human-readable context the structured fields don't capture. |

## Abort vs. no-op

- **Aborted** (`aborted != null`): pre-flight stopped the tick. Something prevents this strategist from running at all in this context. Operator should investigate.
- **No-op** (`actions == []`, `aborted == null`): pre-flight passed, the strategist evaluated, and there was nothing to do. This is the most common tick outcome and is healthy.

The two states are distinguishable by `aborted`. Do not collapse them.

## Example: healthy no-op

```json
{
  "tick_utc": "2026-06-26T13:45:00Z",
  "strategy": "dca-investor",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 1000.00,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "DCA cadence not due; next tranche at 2026-06-27T13:30Z"
}
```

## Example: capability-gated abort

```json
{
  "tick_utc": "2026-06-26T13:45:00Z",
  "strategy": "options-strategist",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 1000.00,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": "capability_gated",
  "notes": "Account 619508153 option_level is empty; options strategist requires option_level_2."
}
```

## Example: live tick with one placement

```json
{
  "tick_utc": "2026-06-26T14:00:00Z",
  "strategy": "dca-investor",
  "mode": "live",
  "account_value": 1000.00,
  "buying_power": 998.50,
  "actions": [
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
  ],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": null
}
```
