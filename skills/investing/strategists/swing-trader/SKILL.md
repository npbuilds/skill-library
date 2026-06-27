---
name: swing-trader
type: strategist
description: >
  RSI(14) mean reversion on a small allowlist of liquid large caps. Buys oversold
  (RSI<30), exits at RSI>70 or after 10 days. Conviction-scaled sizing. Daily
  cadence; many ticks no-op. Use when the user asks "swing trade ideas",
  "is X oversold", or "what does the swing trader say". Default review-only.
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
  cron_hint: "0 14 * * 1-5"
  allowlist: [SPY, QQQ, AAPL, MSFT, NVDA, GOOGL, META, AMZN]
  max_position_pct: 25
  max_concurrent_positions: 3
  capability_requires: []
  profile_compatibility: [autotrader]
  requires_directors: [market-microstructure, risk-architecture]
rsi:
  period: 14
  oversold: 30
  overbought: 70
hold:
  max_days: 10
sizing:
  conviction_floor: 0.3
  conviction_ceiling: 1.0
---

# Swing Trader

RSI(14)-based mean reversion on liquid large caps. Buys names that are statistically oversold (RSI<30), exits when they revert (RSI>70) or after 10 trading days regardless. Sizing is conviction-scaled — deeper oversold = larger position (within `max_position_pct`).

> Required: `_shared/intent-schema.md`, `_shared/position-sizing.md` §"Conviction-scaled". See `references/decision-rules.md`.

## Strategy summary

- **Universe:** 8 liquid large caps + 2 broad ETFs.
- **Entry:** RSI(14) closes below 30 — and the *current* RSI is still below 30 at tick time (no chasing past signals).
- **Exit:** RSI(14) closes above 70, OR position is 10 trading days old, whichever first.
- **Sizing:** conviction = `(30 - current_rsi) / 30` clamped to `[conviction_floor, conviction_ceiling]`. Position notional = `buying_power * max_position_pct * conviction`.
- **Cadence:** daily (one tick per RTH session).
- **No stops.** Exits are RSI- and time-driven. A SOUL-level loss circuit breaker still applies.

## 6-phase protocol

### Phase 1 — Pre-flight

Strategist-side: check that `time_window` is active. Read `~/.hermes/profiles/autotrader/state/swing-trader.json` for current open positions opened by this strategist (so we can age them for exit).

### Phase 2 — Compose context

`market-microstructure` with: *"Are we in a regime where mean reversion in large caps is reliable, or is momentum dominant? One line."*

`risk-architecture` with: *"Anything in current swing-trader positions that warrants early exit?"* (Pass position list.)

Both into `notes`. Microstructure response can downgrade conviction by 0.5x if response includes the literal token `"momentum_dominant"` — handled in phase 4.

### Phase 3 — Signal gather

For each symbol in `allowlist`:

- `get_equity_historicals(symbols=[symbol], start_time=<30 trading days ago>, interval=day)` — fetch 30 daily bars (enough for RSI(14) with warmup).
- `get_equity_quotes(symbols=[symbol])` — for `intent_price`.

Compute RSI(14) from the bars. Standard formula:

```
gains  = sum of positive close-to-close changes over 14 bars
losses = abs(sum of negative changes) over 14 bars
RS  = avg_gain / avg_loss
RSI = 100 - 100 / (1 + RS)
```

### Phase 4 — Decide

**Exits first** (check each currently-open swing position):
```
for pos in open_positions:
    age_days = today - pos.opened_at
    current_rsi = rsi[pos.symbol]
    if current_rsi >= overbought or age_days >= max_days:
        emit sell intent for pos.qty (shares); reason: "rsi_revert" or "max_age"
```

**Entries** (for each symbol NOT already held):
```
for symbol in allowlist:
    if symbol in open_positions: skip
    if rsi[symbol] >= oversold: skip
    conviction = clamp((oversold - rsi[symbol]) / oversold, conviction_floor, conviction_ceiling)
    if microstructure_says_momentum_dominant: conviction *= 0.5
    target_notional = buying_power * max_position_pct/100 * conviction
    qty = floor(target_notional / quote.last_trade_price)
    if qty == 0: skip
    emit buy intent: shares=qty, order_type=limit, limit_price=quote.ask_price * 1.001
```

Concurrent-positions cap: if entries would exceed `max_concurrent_positions`, take the lowest-RSI candidates first.

### Phase 5 — Hand off to executor

Standard envelope.

### Phase 6 — Emit & persist

For any `status: placed` buy, append to state file:

```json
{
  "open_positions": [
    {"symbol": "AAPL", "opened_at": "<ISO>", "qty": 1, "entry_rsi": 22.4, "entry_price": 184.50, "order_id": "..."}
  ]
}
```

For any `status: placed` sell, remove from state. Reviewed-only ticks do not touch state.

## Interactive mode

- "Is NVDA a swing buy today?" — run phases 1-4 for just NVDA, emit `tick_decision` with one intent (review-only).
- "Exit all swing positions" — refuse. Exit logic is rule-based; user can edit `hold.max_days` to 0 to force liquidation on next tick.
- "What positions does swing have open?" — return state file contents as a table.

## What this strategist will never do

- Buy a symbol off the allowlist.
- Hold past `hold.max_days` (force exit on the next tick).
- Average down. If a position drops and RSI re-prints below 30, this strategist sees the symbol is already held and skips re-entry.
- Use stop-loss orders. Exits are rule-driven, not price-triggered.
