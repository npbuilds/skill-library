# Circuit Breakers

Hard checks that gate *whether a strategist runs at all*, or *what subset of actions it may emit*. Most live in the executor's pre-flight; strategists must re-check the ones marked "Strategist enforces" before emitting any intent.

## Pre-flight breakers (executor enforces, strategist mirrors)

These run in phase 1. Failing any of them aborts the tick — `aborted` is set, `actions: []`, and no broker tool is called.

### Account lock

```
required: account.account_number == strategist.account_lock
required: account.agentic_allowed == true
```

For autotrader-bound strategists, `account_lock` is always `"619508153"`. The check finds the account whose `account_number` matches; if not present or `agentic_allowed` is false, abort with `aborted: "account_lock_failed"`.

### Capability gate

```
for each cap in strategist.capability_requires:
    if cap == "option_level_2":
        required: account.option_level in {"option_level_2", "option_level_3"}
    if cap == "fractional_eligible":
        required: account.fractional_eligible == true
```

Failure → abort with `aborted: "capability_gated"`. The strategist records which capability was missing in `notes`.

### Profile compatibility

```
required: current_profile_name in strategist.profile_compatibility
```

Failure → abort with `aborted: "profile_compatibility_failed"`. This is the firewall that prevents `options-strategist` from running in the equity-only `autotrader` profile.

### Time window (placement-only)

```
if strategist.time_window is set:
    if current_time outside time_window AND any intent would call place_*:
        abort: outside_time_window
```

Analysis-only ticks (mode=review, no place call) may proceed outside the window. This matters for end-of-day reviews, rebalance pre-staging, etc.

### Daily loss circuit breaker (SOUL §"Daily loss circuit breaker")

```
realized_pnl = get_realized_pnl(span="day").total_realized_gain
day_start_value = account_value at first tick of the day  # see "Stateful breakers" below
loss_pct = realized_pnl / day_start_value

if loss_pct <= -0.05:
    circuit_breaker_tripped = true
```

When tripped, the strategist may emit *only* close-side intents (selling existing positions). New entry intents are silently dropped by the executor with `status: skipped, reason: "circuit_breaker_tripped"`.

The breaker resets at 00:00 America/New_York.

## In-tick breakers (strategist enforces, executor double-checks)

These don't abort the whole tick — they shape the intent set.

### Allowlist

```
for each intent in intents:
    required: intent.symbol in strategist.allowlist
```

If an intent's symbol isn't in the allowlist, the strategist must not emit it. Executor rejects with `status: skipped, reason: "off_allowlist"` as a defensive backup.

### Per-name cap

```
position_notional = qty * current_price  (for shares)
                  = notional_usd          (for notional)

required: position_notional <= buying_power * max_position_pct
```

If violated, strategist must downsize before emitting. Executor enforces by trimming.

### Concurrent positions

```
distinct_symbols_after_this_tick <= max_concurrent_positions
```

Strategist counts current positions from `get_equity_positions` + intents being emitted this tick. Executor trims excess intents (FIFO — older intents win).

### Slippage bound

```
realized_review_price = review_equity_order(...).price
slippage_pct = (realized_review_price - intent_price) / intent_price * 100

if abs(slippage_pct) > intent.max_slippage_pct:
    abort intent with status: slippage_aborted
```

Executor enforces this on every action.

## Stateful breakers (cron-only)

A few breakers need cross-tick state. The autotrader profile uses Hermes's session store keyed by date:

- `day_start_value` — captured by the first cron tick after midnight ET. Stored at `~/.hermes/profiles/autotrader/state/day-start.json`.
- `consecutive_review_anomalies` — incremented when an action lands `status: review_anomaly`. If it hits 3 in a single day, the executor halts placements for the rest of the day even if no loss threshold has been crossed (something is wrong upstream).

Interactive (chat / claude-code) ticks do not write to this state — they are read-only against it.

## What never trips a breaker

- The strategist deciding to do nothing. No-op is not an error.
- A failed `get_equity_quotes` for a *single* symbol — the strategist drops just that intent with `status: skipped, reason: "quote_unavailable"`. If *all* quotes fail, that's a `data_anomaly`, not a circuit breaker.
- The user manually placing a trade through the Robinhood app. The strategist sees the position appear via `get_equity_positions` and adjusts; no breaker fires.
