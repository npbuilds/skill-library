# Reflexivity Trader — Decision Rules

## Constants

| Constant | Value |
|---|---|
| `max_position_pct` | 33 |
| `max_concurrent_positions` | 2 |
| `confidence_floor` | 0.5 |
| `max_hold_days` | 30 (calendar) |
| `max_slippage_pct` (per intent) | 0.5 |

## Director response contract

The `reflexivity-sentiment` director MUST respond to the phase-2 prompt with valid JSON. Strict schema:

```json
{
  "symbol": "<ticker or null>",
  "direction": "long|short",
  "phase": "emergence|validation|acceleration|exhaustion|reversal",
  "confidence": 0.0-1.0,
  "invalidation": {"price": <number>, "reason": "<string>"},
  "narrative": "<one sentence>",
  "held_status": [{"symbol": "<>", "current_phase": "<>"}]
}
```

If the director's response is not valid JSON or is missing required fields: log `data_anomaly`, skip the tick.

## Entry condition

```
director.symbol is not null
director.confidence >= 0.5
director.phase in {"validation", "acceleration"}
director.direction == "long"      # shorts disabled
director.symbol in allowlist
director.symbol not in held
```

All must hold.

## Sizing

```
target_notional = buying_power * 0.33 * director.confidence
qty = floor(target_notional / current_price)
```

Example: confidence 0.7, buying_power $1000 → target $231 → at NVDA $120, qty = 1. The conviction-confidence product is the lever.

## Exit conditions

| Trigger | Action | Reason tag |
|---|---|---|
| Director reports `phase: exhaustion` for held symbol | Sell full | `phase_exhaustion` |
| Director reports `phase: reversal` for held symbol | Sell full | `phase_reversal` |
| Calendar age >= 30 days | Sell full | `max_hold_days` |
| Price <= invalidation_price (long) | Sell full | `invalidation_hit` |
| SOUL daily circuit breaker tripped | Director's exits proceed; new entries skipped | (handled by executor) |

## Anti-rules

| Refused | Reason |
|---|---|
| Short selling | Cash account. |
| Override director invalidation | The director sets the invalidation; the strategist obeys. |
| Re-enter after invalidation hit (same cycle) | Once invalidation hits, the thesis is dead. Wait for director to re-flag. |
| Pyramid | Single entry per symbol per cycle. |
| Trade off-allowlist | Hard rule. |

## State file shape

`~/.hermes/profiles/autotrader/state/reflexivity-trader.json`:

```json
{
  "this_week_evaluated": "2026-W26",
  "open_positions": [
    {
      "symbol": "NVDA",
      "opened_at": "2026-06-19T15:00:00-04:00",
      "qty": 1,
      "entry_price": 120.50,
      "entry_phase": "acceleration",
      "entry_confidence": 0.7,
      "invalidation_price": 110.00,
      "narrative": "AI capex acceleration with major-tenant validation",
      "order_id": "..."
    }
  ]
}
```

`this_week_evaluated` is ISO week format — prevents same-week re-runs.
