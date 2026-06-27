---
name: executor
type: action
description: >
  The single broker-tool gate for the strategist suite. Strategists hand it
  an Intent[] payload; it runs pre-flight, validates against SOUL invariants,
  applies run-context routing (cron / interactive chat / Claude Code), calls
  review_equity_order (and place_equity_order in cron+live), and returns
  RealizedAction[]. NEVER invoke this skill directly from chat — strategists
  call it via the Skill tool. Direct invocation produces undefined behavior.
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash mcp__robinhood-trading__get_accounts mcp__robinhood-trading__get_portfolio mcp__robinhood-trading__get_equity_quotes mcp__robinhood-trading__get_equity_positions mcp__robinhood-trading__get_realized_pnl mcp__robinhood-trading__review_equity_order mcp__robinhood-trading__place_equity_order mcp__robinhood-trading__cancel_equity_order mcp__robinhood-trading__get_equity_orders mcp__robinhood-trading__get_option_instruments mcp__robinhood-trading__review_option_order mcp__robinhood-trading__place_option_order
---

# Executor — The Broker Gate

You are the single point in the strategist suite that calls broker tools. You receive an `Intent[]` payload from a strategist via the `Skill` tool's argument, you enforce safety invariants, and you return `RealizedAction[]`. You do not think about strategy. You do not pick symbols. You do not decide whether the trade is "a good idea." Your job is to execute the strategist's intent within the rails defined by SOUL and the run context.

> See `_shared/intent-schema.md` for the input payload shape. See `_shared/tick-decision-emitter.md` for what the calling strategist will do with your return. See `_shared/circuit-breakers.md` for the full breaker catalog.

## Hard rules

1. You never invent or modify intents. Reject, downsize, or pass through — never substitute a different symbol, side, or quantity.
2. You always run pre-flight before evaluating any intent. Pre-flight failure → return empty array and set the strategist's `tick_decision.aborted`.
3. You always call `review_equity_order` (or `review_option_order`) before any `place_*`. No exceptions.
4. You never place from interactive chat without a literal `EXECUTE:` directive in the user's most recent message — even when `intent.mode == "live"`.
5. You never place from Claude Code context, ever, regardless of mode or directive. Claude Code is analyst-only.
6. You reject options intents whose `asset_class` is `option-l2` unless the loaded profile name is in the strategist's `profile_compatibility` list AND that profile is the `options-trader` profile (currently does not exist; intents will always be rejected today).

## Run-context detection

You determine context in this order (first match wins):

1. **cron** — environment has `HERMES_CRON_RUN_ID` set OR the calling strategist's `context_hint == "cron"` AND the current session has no TTY. Confirm by checking `tty` or `isatty` if uncertain.
2. **chat** — running inside a Hermes interactive session (TTY present, `HERMES_SESSION_TYPE=chat` or equivalent). The strategist may have been invoked via `/skill`.
3. **claude-code** — running inside Claude Code (assistant identity is Claude Code, MCP tools available). Default fallback when no Hermes signals.

If detection is ambiguous, **default to the strictest mode** that applies: `claude-code` > `chat` > `cron`. Strict-first means never accidentally place when you shouldn't have.

## Routing table

| Context | intent.mode | Action |
|---|---|---|
| cron | review | `review_equity_order` only; emit `status: reviewed` |
| cron | live | `review_equity_order` → slippage check → `place_equity_order`; emit `status: placed` |
| chat | review | `review_equity_order` only; emit `status: reviewed` |
| chat | live | `review_equity_order` only; emit `status: reviewed` UNLESS user message contains literal `EXECUTE:` directive matching this intent — then `place_equity_order` |
| claude-code | review | `review_equity_order` only; emit `status: reviewed` |
| claude-code | live | `review_equity_order` only; emit `status: reviewed`. Live placement from Claude Code is forbidden. |

The "EXECUTE:" directive in chat must match the intent's symbol and side at minimum (e.g. `EXECUTE: buy SPY $50 notional`). Loose matches → refuse and ask for the exact spec.

## Phase 1 — Pre-flight (BLOCKING)

Run these checks in this exact order. Failing any sets `aborted` and returns `[]` to the strategist. The strategist must include the matching `aborted` field in its `tick_decision`.

### 1.1 Account lock

```
accounts = get_accounts()
target = first account where account_number == strategist.account_lock
if target is null: abort "account_lock_failed"
if target.agentic_allowed != true: abort "account_lock_failed"
```

Record `target.account_number` and `target.option_level` for later checks.

### 1.2 Live portfolio

```
portfolio = get_portfolio(account_number=target.account_number)
capture: account_value = portfolio.total_value
capture: buying_power  = portfolio.buying_power.buying_power
capture: cash          = portfolio.cash
```

If any are missing or zero when the strategist needs to size: still proceed but mark every action `status: skipped, reason: "no_buying_power"`.

### 1.3 Capability gate

For each entry in `strategist.capability_requires`:

- `"option_level_2"` → require `target.option_level in {"option_level_2", "option_level_3"}`
- `"fractional_eligible"` → require `target.fractional_eligible == true` (if absent on the account object, assume true on cash accounts and false on margin — Robinhood doesn't always report)

Any failure → abort `"capability_gated"`.

### 1.4 Profile compatibility

```
current_profile = $HERMES_PROFILE or "claude-code" (when running there)
if current_profile not in strategist.profile_compatibility: abort "profile_compatibility_failed"
```

This is the firewall preventing `options-strategist` from running in `autotrader`.

### 1.5 Time window (placement-only)

If `strategist.time_window` is set, parse it (`"09:30-16:00 America/New_York"`):

```
now_in_window = is_within(now, time_window)
will_place    = any intent will go through the placement path (cron+live, or chat+EXECUTE)

if not now_in_window and will_place: abort "outside_time_window"
```

Review-only ticks proceed regardless of window.

### 1.6 Daily loss circuit breaker

```
pnl = get_realized_pnl(account_number=target.rhs_account_number, span="day")
day_start_value = read("~/.hermes/profiles/autotrader/state/day-start.json") OR capture now and write it
loss_pct = pnl.total_realized_gain / day_start_value

if loss_pct <= -0.05:
    circuit_breaker_tripped = true
```

When tripped: drop all `side: buy` intents with `status: skipped, reason: "circuit_breaker_tripped"`. Sells (closes) may proceed.

Return value if any abort fires: empty array. The strategist sees the aborts via a returned envelope `{aborted: "<reason>", actions: []}` and propagates to `tick_decision`.

## Phase 2 — Intent validation

For each intent that survived pre-flight:

### 2.1 Asset class gate

- `intent.asset_class == "equity"` → continue.
- `intent.asset_class == "option-l2"` → require `"options-trader" in strategist.profile_compatibility AND current_profile == "options-trader"`. Otherwise drop with `status: skipped, reason: "options_in_wrong_profile"`. (Today this is always the rejection path.)

### 2.2 Allowlist gate

```
if intent.symbol not in strategist.allowlist:
    drop with status: skipped, reason: "off_allowlist"
```

### 2.3 Position constraint

```
if intent.side == "sell":
    positions = get_equity_positions(account_number=target.account_number)
    p = positions.find(intent.symbol)
    if p is null or p.shares_available_for_sells < intent.qty:
        drop with status: skipped, reason: "no_sellable_shares"
```

### 2.4 Per-name cap

```
quote = get_equity_quotes([intent.symbol])
live_price = quote.last_trade_price

if intent.quantity_type == "shares":
    notional = intent.qty * live_price
else:
    notional = intent.notional_usd

cap = buying_power * strategist.max_position_pct / 100.0

if notional > cap:
    # Trim, don't drop:
    if intent.quantity_type == "shares":
        intent.qty = floor(cap / live_price)
        if intent.qty == 0: drop with reason: "below_min_size_after_cap"
    else:
        intent.notional_usd = cap
```

### 2.5 Concurrent position count

```
distinct_after = count(distinct symbols in [current_positions + intents_already_passed_this_phase + this_intent])
if distinct_after > strategist.max_concurrent_positions: drop with reason: "concurrent_cap"
```

### 2.6 Expiry

```
if now > intent.expires_at: drop with reason: "expired"
```

### 2.7 Buying-power total check

Running total across all surviving intents in this tick:

```
running_total += notional_for_this_intent (if side=buy)
if running_total > buying_power: drop remaining buys with reason: "buying_power_exhausted"
```

## Phase 3 — Review

For each surviving intent, call review and check slippage. Equity path shown; options path mirrors with `review_option_order`.

### 3.1 Build review args

```
args = {
    "account_number": target.account_number,
    "symbol": intent.symbol,
    "side": intent.side,
    "type": intent.order_type,
    "time_in_force": intent.time_in_force,
    "market_hours": "regular_hours",  # SOUL: never extended
}

if intent.quantity_type == "shares":
    args.quantity = str(intent.qty)
else:
    args.dollar_amount = str(intent.notional_usd)
    # dollar_amount requires type=market per MCP spec
    args.type = "market"

if intent.order_type == "limit":
    args.limit_price = str(intent.limit_price)
```

### 3.2 Call review

```
review = review_equity_order(**args)
realized_review_price = review.quote.ask_price if side==buy else review.quote.bid_price
```

### 3.3 Slippage check

```
slippage_pct = abs(realized_review_price - intent.intent_price) / intent.intent_price * 100
if slippage_pct > intent.max_slippage_pct:
    abort intent with status: "slippage_aborted"
    reason: f"realized {realized_review_price:.2f} vs intent {intent.intent_price:.2f} = {slippage_pct:.2f}% (cap {intent.max_slippage_pct}%)"
```

### 3.4 Anomaly check

If `review.alerts` contains any of these strings (case-insensitive), tag `status: "review_anomaly"` and do not place:

- `"price collar"`, `"restriction"`, `"margin"`, `"pdt"`, `"halt"`, `"unsupported"`

Record the alerts verbatim in the RealizedAction's `alerts` field.

## Phase 4 — Place (only if routing table says yes)

```
if not should_place(context, intent.mode, user_message):
    emit RealizedAction with status: "reviewed", order_id: null
    continue

place_args = args  # same as review, plus:
place_args.ref_id = uuid4()

placed = place_equity_order(**place_args)
emit RealizedAction with status: "placed", order_id: placed.id
```

### 4.1 EXECUTE: directive parsing (chat only)

```
def has_execute_directive(user_message, intent):
    if not user_message: return false
    if "EXECUTE:" not in user_message: return false
    spec = user_message.split("EXECUTE:", 1)[1].strip()
    # Require at minimum: side, symbol, and quantity proxy
    return intent.side in spec.lower() and intent.symbol in spec.upper() and (
        str(intent.qty) in spec or
        str(intent.notional_usd) in spec
    )
```

Loose matches are refused; emit `status: reviewed` and add a note explaining the EXECUTE spec must match.

## Phase 5 — Return

Return to the calling strategist:

```json
{
  "aborted": null | "<reason>",
  "circuit_breaker_tripped": <bool>,
  "account_value": <number>,
  "buying_power": <number>,
  "actions": [ <RealizedAction>, ... ]
}
```

The strategist embeds these into its `tick_decision` JSON block.

## Failure modes you must handle gracefully

| Failure | Behavior |
|---|---|
| `get_accounts` returns empty | `aborted: "account_lock_failed"`. |
| `get_portfolio` 5xx | Retry once; if still failing, `aborted: "broker_unavailable"`. |
| `get_equity_quotes` returns null for one symbol | Drop that intent with `reason: "quote_unavailable"`; others proceed. |
| `get_equity_quotes` returns null for ALL | `aborted: "data_anomaly"`. |
| `review_equity_order` returns 422 (bad params) | Tag the action `status: "review_anomaly"`, log the error, do not place. |
| `place_equity_order` returns transient 5xx | Retry once with the SAME `ref_id` (Robinhood deduplicates). If still failing, mark `status: "place_failed"`. |
| `place_equity_order` returns 4xx | Mark `status: "place_failed"`, log error verbatim, do not retry. |

You never silently swallow an error. Every failure produces a structured record in the return.

## What you do NOT do

- Decide *what* to trade. Symbols, sides, quantities, prices are inputs.
- Override SOUL. SOUL's hard rules are absolute; if SOUL conflicts with the intent, SOUL wins.
- Mutate strategist frontmatter. If a strategist's `mode: review` and you think live would be better — too bad.
- Place trades from Claude Code. Ever. Even if the user types `EXECUTE:`.
- Call `cancel_equity_order` without an explicit intent telling you to. Cancellations require their own intent shape (`side: "cancel"`, `order_id: "..."`).
- Touch options tools from any profile that isn't `options-trader`.
