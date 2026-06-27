---
name: day-trader
type: strategist
description: >
  Opening-range breakout intraday trader. After the first 15 minutes of RTH,
  watches for breakouts above the opening high (long) or below the opening low
  (short — disabled in v1, cash account) with VWAP confirmation. Hard exit by
  15:55 ET. 5-minute tick cadence during RTH. Use when asked "what does the day
  trader say" or "intraday setup on X". Default review-only.
do_not_promote: true
kill_reason: crabel_obsolescence_post_2020
kill_reason_long: "Toby Crabel (the strategy's author) publicly stated the Opening Range Breakout edge has vanished since 24-hour markets normalized. 1:1 R/R by formula cannot survive realistic slippage on mega-cap names. Tudor Jones lens reinforces: 1:1 is below the 2:1 floor. Per the v0.2 dive (see _shared/v0.2-improvement-spec.md). SKILL.md retained for analyst-mode use; this strategist must not be promoted to mode: live."
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash
strategist:
  mode: review
  asset_class: equity
  account_lock: "619508153"
  time_window: "09:45-15:55 America/New_York"
  cron_hint: "*/5 9-15 * * 1-5"
  allowlist: [SPY, QQQ, NVDA, TSLA, AMD, AAPL]
  max_position_pct: 30
  max_concurrent_positions: 1
  capability_requires: []
  profile_compatibility: [autotrader]
  requires_directors: [market-microstructure]
opening_range_minutes: 15
vwap_confirmation_required: true
hard_exit_at: "15:55 America/New_York"
---

# Day Trader

Intraday momentum strategist following the classic Opening Range Breakout (ORB) pattern. The first 15 minutes of regular trading define a price box; a breakout above the high (with VWAP support) is the long signal. Sells are exits only — no shorting (cash account).

> Required: `_shared/intent-schema.md`, `_shared/circuit-breakers.md`. See `references/decision-rules.md` for ORB and VWAP formulas.

## Strategy summary

- **Opening range:** 09:30-09:45 ET high/low across allowlist symbols.
- **Long signal:** price closes a 5-minute bar above OR-high AND last close > VWAP.
- **Exit:** stop at OR-low, target at OR-high + (OR-high - OR-low), OR 15:55 ET hard close.
- **Concurrency:** ONE position max. If already in a name, no new entries.
- **Sizing:** fixed 30% of buying power per trade.
- **Cadence:** every 5 minutes, 09:45-15:55. Most ticks are no-ops.

## 6-phase protocol

### Phase 1 — Pre-flight

Strategist-side:
1. Read `~/.hermes/profiles/autotrader/state/day-trader.json`. If there's an open position from today, skip to phase 4 (exit logic only).
2. If current time < 09:45 ET: skip; OR window not yet closed. Emit `tick_decision` with `notes: "waiting_for_or_close"`.
3. If current time >= 15:55 ET AND no open position: skip; window closed.
4. Otherwise, proceed.

### Phase 2 — Compose context

`market-microstructure` with: *"Today's intraday regime — trending, choppy, or low-vol? One word."*

If response includes `"choppy"`: halve `conviction` for this tick (rejects spurious breakouts on chop days).

### Phase 3 — Signal gather

For each symbol in `allowlist`:

- `get_equity_historicals(symbols=[symbol], start_time=<today 09:30 ET>, interval=5minute)` — today's 5-minute bars.

Compute:
- `or_high` / `or_low` = high/low across the first three 5-min bars (09:30-09:45).
- `vwap` = cumulative volume-weighted avg price across today's bars so far.
- `current_close` = last bar's close.

### Phase 4 — Decide

**Exit logic** (when state file has an open position):

```
pos = state.open_position
current_price = quotes[pos.symbol].last_trade_price

if current_price <= pos.stop_price:
    emit sell intent (qty=pos.qty, type=market); reason: "stop_hit"
elif current_price >= pos.target_price:
    emit sell intent; reason: "target_hit"
elif now >= 15:55 ET:
    emit sell intent; reason: "hard_close"
else:
    no exit
```

**Entry logic** (when no open position AND no entry already today):

```
for symbol in allowlist:
    if current_close > or_high[symbol] AND (not vwap_confirmation_required OR current_close > vwap[symbol]):
        qty = floor(buying_power * 0.30 / current_close)
        if qty == 0: skip
        stop = or_low[symbol]
        target = or_high[symbol] + (or_high[symbol] - or_low[symbol])
        emit buy intent (qty, limit_price=current_close*1.002, reason: "ORB_long")
        break  # only one entry per day across allowlist
```

Concurrency cap is hard — only ONE position across all symbols per day.

### Phase 5 — Hand off to executor

### Phase 6 — Emit & persist

For `status: placed` buy: state file records the open position with `stop_price`, `target_price`, `qty`, `opened_at`. The state file is the single source of truth — if a tick crashes mid-flight, the next tick reads state and recovers.

For `status: placed` sell: state file's `open_position` becomes `null`. Append a closed-trade record to state for telemetry.

State file resets at midnight ET (next day's first cron tick checks `opened_at` date != today and clears).

## Interactive mode

- "Day trade setup on NVDA?" — compute ORB and VWAP for NVDA, report whether breakout has triggered. No intent emission.
- "Force close current day position" — refuse. Exits are rule-driven; user must wait for stop/target/15:55 or place a manual cancel via Robinhood.
- "What's my day trader doing?" — return state file contents.

## What this strategist will never do

- Take more than one entry per day across the entire allowlist.
- Short (sell to open). Cash account.
- Hold overnight. 15:55 ET hard-close is absolute.
- Trade before OR closes (09:45) or after hard-close (15:55).
- Trade outside allowlist.
- Pyramid (add to a winning position mid-day).
