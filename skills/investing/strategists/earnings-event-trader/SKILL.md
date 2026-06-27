---
name: earnings-event-trader
type: strategist
description: >
  Post-earnings drift fade strategist. Identifies allowlist names that just
  reported an EPS BEAT but gapped DOWN ≥2% — irrational reaction setup. Buys
  on the gap, exits at +3% or 5 trading days. Equity-only in v1; an options
  variant lives in options-strategist. Use when user asks "earnings setups
  today", "did X beat", or "what does the earnings trader see". Review-only default.
do_not_promote: true
kill_reason: wrong_universe_pead_absent_mega_cap
kill_reason_long: "PEAD (post-earnings announcement drift) literature documents the beat-but-down reversion on small-caps. The allowlist is entirely mega-cap, where institutional traders price-discover within minutes and PEAD is minimal-to-absent. Wrong-universe is a thesis-level problem, not a parameter tune. Per the v0.2 dive (see _shared/v0.2-improvement-spec.md). SKILL.md retained for analyst-mode use; this strategist must not be promoted to mode: live."
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash
strategist:
  mode: review
  asset_class: equity
  account_lock: "619508153"
  time_window: "10:00-15:55 America/New_York"
  cron_hint: "0 14 * * 1-5"
  allowlist: [SPY, QQQ, AAPL, MSFT, NVDA, GOOGL, META, AMZN, AMD, NFLX]
  max_position_pct: 25
  max_concurrent_positions: 2
  capability_requires: []
  profile_compatibility: [autotrader]
  requires_directors: [regime-intelligence, special-situations]
gap_down_threshold_pct: 2.0
exit_target_pct: 3.0
exit_max_days: 5
---

# Earnings Event Trader

A single, specific setup: a quality name beats EPS but the market punishes it anyway. The "beat-but-down" reaction is empirically a slow-fade — the price often recovers over the next several days as the noise (guidance, one-line items, sector rotation) gets parsed. This strategist takes that bet.

> Required: `_shared/intent-schema.md`, `_shared/circuit-breakers.md`. See `references/decision-rules.md`.

## Strategy summary

- **Universe:** 10 mega-cap quality names from allowlist.
- **Trigger:** symbol reported earnings in the prior session (AM today or PM previous trading day), `actual_eps > estimated_eps`, current price gapped DOWN ≥ 2% from prior close.
- **Entry:** buy at next regular-hours open or current price (limit at +0.1%).
- **Exit:** +3% from entry OR 5 trading days, whichever first.
- **Sizing:** fixed 25% of buying power.
- **Cadence:** daily, once (10am ET tick).

## 6-phase protocol

### Phase 1 — Pre-flight (strategist-side)

Read `~/.hermes/profiles/autotrader/state/earnings-event-trader.json`. If today's date already has an entry attempt logged → skip to phase 4 (exit logic for any open positions).

### Phase 2 — Compose context

`regime-intelligence` with: *"Is this an earnings season where beats are getting rewarded, or punished broadly? One line."*

`special-situations` with: *"Any quality names that reported recently with notable management commentary worth flagging?"*

Both into `notes`. The regime response can suppress entries (if response includes `"beats_punished_broadly"`, skip phase 4 entries entirely — the strategy thesis is broken).

### Phase 3 — Signal gather

```
calendar = get_earnings_calendar(start_date=<yesterday>, days=1, filter="high_market_cap")
```

For each entry in `calendar.results` where `symbol in allowlist`:

- Pull recent EPS: `get_earnings_results(symbol=symbol)` — read most recent quarter's `actual_eps` and `estimated_eps`.
- Pull recent prices: `get_equity_quotes(symbols=[symbol])` for current price and prior session close.

Compute:
```
beat = actual_eps > estimated_eps
gap_pct = (current_price - prior_close) / prior_close * 100
trigger = beat AND gap_pct <= -gap_down_threshold_pct
```

### Phase 4 — Decide

**Exits first** (any open earnings positions):
```
for pos in open_positions:
    current_price = quotes[pos.symbol].last_trade_price
    pnl_pct = (current_price - pos.entry_price) / pos.entry_price * 100
    age_days = today - pos.opened_at (trading days)
    if pnl_pct >= exit_target_pct:
        emit sell intent; reason: "target_hit"
    elif age_days >= exit_max_days:
        emit sell intent; reason: "max_age"
```

**Entries** (only if context didn't say `beats_punished_broadly`):
```
for symbol in triggered_symbols:
    if symbol in open_positions: skip
    notional = buying_power * 0.25
    qty = floor(notional / current_price)
    if qty == 0: skip
    emit buy intent (limit, limit_price=current_price*1.001, reason: f"beat ${actual} vs ${est}, gap {gap_pct:.1f}%")
    break  # one entry per tick (max_concurrent_positions enforced)
```

### Phase 5 — Hand off to executor

### Phase 6 — Emit & persist

Log entry attempts (regardless of fill) so phase 1 next tick can short-circuit.

## Interactive mode

- "Any beat-but-down setups today?" — run phases 1-4 in review mode, report what triggered (zero is the common answer).
- "Did NVDA beat?" — call `get_earnings_results(symbol="NVDA")`, report.

## What this strategist will never do

- Trade on a miss. Beats only.
- Trade on a gap UP. The fade is one-directional.
- Buy pre-earnings. The strategy is post-event.
- Hold past 5 trading days. Force exit.
- Trade outside allowlist.
