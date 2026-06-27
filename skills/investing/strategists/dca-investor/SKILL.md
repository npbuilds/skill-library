---
name: dca-investor
type: strategist
description: >
  Dollar-cost-averages a fixed weekly tranche of notional into a broad-ETF basket.
  Equity-only, cash-account safe. No conviction calls, no market timing, no exits —
  just a metronome. Use when the user asks "DCA into X", "set up automated buying",
  "schedule weekly investments", or "what does the DCA strategist say". Default
  mode is review-only; live mode requires explicit promotion.
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash
strategist:
  mode: review
  asset_class: equity
  account_lock: "619508153"
  time_window: "09:35-15:55 America/New_York"
  cron_hint: "0 14 * * 1"
  allowlist: [SPY, VOO, VTI, QQQ, BND]
  max_position_pct: 50
  max_concurrent_positions: 5
  capability_requires: []
  assumes:
    fractional_shares: true   # cash individual accounts on Robinhood; not a capability the broker reports
  profile_compatibility: [autotrader]
  requires_directors: [regime-intelligence]
basket:
  SPY: 0.50
  QQQ: 0.30
  BND: 0.20
tranche_size_usd: 50.00
cadence: weekly_monday
---

# DCA Investor

A boring strategist. Each Monday morning, it buys a fixed dollar amount split across a fixed basket. It does not try to time entries. It does not skip weeks because "the market looks toppy." It does not double up after a drawdown. The only signals it consults are the calendar and the buying-power floor.

This is the simplest possible strategist — and on purpose. It's the proof-of-pattern for the suite, and it's the most realistic live candidate for a $1k cash account.

> **Required reading before authoring/modifying:** `_shared/intent-schema.md`, `_shared/tick-decision-emitter.md`, `_shared/circuit-breakers.md`, `_shared/position-sizing.md`. The numeric rules below live in `references/decision-rules.md`.

## Strategy summary

- **Universe**: SPY, QQQ, BND (broad equity + tech-equity + total-bond).
- **Weights**: SPY 50% · QQQ 30% · BND 20%.
- **Tranche**: $50/week total. Per-symbol: SPY $25, QQQ $15, BND $10.
- **Cadence**: weekly, Monday after market open. Cron hint `0 14 * * 1` (10am ET).
- **Mode**: review-only until the human reviews tick logs and promotes to live.
- **Exit rule**: none. DCA is one-way. Sells are out of scope for this strategist.
- **Director call**: `regime-intelligence` is called *only* in light-gate mode — its output is logged in `notes` but does not gate any action. A future v2 may add a regime gate; v1 is intentionally pure.

## 6-phase protocol

### Phase 1 — Pre-flight (BLOCKING)

Run `_shared/executor`'s pre-flight via the executor — but capture inputs first so this strategist can short-circuit before invoking it. Specifically:

1. Determine cadence eligibility:
   - Read the last successful DCA tick timestamp from `~/.hermes/profiles/autotrader/state/dca-investor.json` (if it exists).
   - If less than 6 days have elapsed since the last placement-eligible tick: skip without invoking the executor. Emit `tick_decision` with `actions: []` and `notes: "cadence_not_due; next_at <ISO>"`.
2. If cadence IS due, proceed to phase 2.

(The executor will still run its full pre-flight when invoked in phase 5. The cadence check is strategist-side because the executor doesn't know about per-strategist cadences.)

### Phase 2 — Compose context

Invoke `regime-intelligence` via the `Skill` tool with the prompt:

> "Three-line summary of the current macro regime — growth direction, inflation direction, monetary stance. No prose."

Capture the response into a `regime_summary` string (≤200 chars). It will be embedded in `tick_decision.notes`. It does NOT affect any sizing or skip decision in v1.

### Phase 3 — Signal gather

Call `get_equity_quotes(symbols=["SPY", "QQQ", "BND"])` to capture current prices. Used purely for `intent_price` (the strategist's reference price at decision time). No filtering on this — DCA proceeds at any price.

### Phase 4 — Decide

Construct three intents (one per basket member):

```json
[
  {
    "symbol": "SPY",
    "side": "buy",
    "quantity_type": "notional",
    "notional_usd": 25.00,
    "order_type": "market",
    "intent_price": <SPY quote.ask_price>,
    "max_slippage_pct": 1.0,
    "time_in_force": "gfd",
    "reason": "DCA weekly tranche — SPY 50% of $50 = $25",
    "expires_at": "<today 15:55 ET as ISO>",
    "asset_class": "equity",
    "option_leg": null
  },
  /* QQQ $15, BND $10 — same shape */
]
```

Notes on the intent shape:
- `quantity_type: notional` because the basket weights are designed in dollars, not shares. The executor routes this to Robinhood's `dollar_amount` parameter.
- `max_slippage_pct: 1.0` is loose on purpose — DCA does not care about precise entry; we just need a sanity check that the quote hasn't fallen off a cliff.
- `expires_at` is end-of-RTH today. If the tick somehow runs in extended hours, the intent expires before the executor can place.

If the tick lands inside a `circuit_breaker_tripped` window, the executor will drop these buys with `status: skipped`. That's fine — DCA simply waits for the next week.

### Phase 5 — Hand off to executor

Invoke `_shared/executor` via the `Skill` tool with:

```json
{
  "strategy": "dca-investor",
  "mode": "<mode from frontmatter>",
  "context_hint": "<best guess>",
  "intents": [ ...three intents... ]
}
```

The executor returns:

```json
{
  "aborted": null | "<reason>",
  "circuit_breaker_tripped": <bool>,
  "account_value": <number>,
  "buying_power": <number>,
  "actions": [ <three RealizedAction objects> ]
}
```

### Phase 6 — Emit & persist

Write the `## tick_decision` block. If any action was `status: placed`, update `~/.hermes/profiles/autotrader/state/dca-investor.json` with the placement timestamp (so phase 1 can read it next tick).

If `aborted` is set: do not update state. The next tick will retry from scratch.

## Interactive mode

In Claude Code or `autotrader chat`:

- "What does DCA say about this week?" — run phases 1-5; emit `tick_decision`. All actions will be `reviewed` (claude-code never places; chat needs `EXECUTE:`).
- "Skip this week" — emit `tick_decision` with `actions: []` and `notes: "user_skipped"`. Do NOT update the state file (so next week's tick is unaffected).
- "Increase tranche to $100" — refuse. Tranche size is a frontmatter constant. The user must edit `tranche_size_usd` in the SKILL.md frontmatter, not at runtime.

## Promoting to live

1. Run paper ticks for at least 4 consecutive Mondays. Inspect the `tick_decision` log for each.
2. Confirm:
   - No `aborted` outcomes you don't understand.
   - Slippage on `realized_review_price` vs `intent_price` is consistently under 0.3%.
   - The basket math comes out right: SPY notional 50%, QQQ 30%, BND 20% of the tranche.
3. Edit this skill's frontmatter: `mode: review` → `mode: live`.
4. Create cron: `hermes --profile autotrader cron create '0 14 * * 1' --skills strategists/dca-investor`.
5. Watch the first live tick. Verify the order lands in `get_equity_orders`.

## What this strategist will never do

- Skip a week because the market is "expensive" or "looks toppy."
- Buy extra after a drawdown.
- Sell — even to "take profits" or "rebalance."
- Trade anything outside the basket.
- Override the buying-power cap or per-name cap.
- Run on a non-Monday.
- Run from a profile other than `autotrader`.
