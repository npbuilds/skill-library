---
name: reflexivity-trader
type: strategist
description: >
  Soros-style reflexive position trader. Heavily composes the
  reflexivity-sentiment director to identify adoption-validation feedback
  loops in real-time narratives (AI capex, obesity drugs, etc.), then sizes
  by the director's reported conviction. Weekly cadence, ≤30 day holds. Use
  when user asks "is X a reflexive setup", "narrative trade ideas", or "what
  does the reflexivity trader see". Default review-only.
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash WebSearch
strategist:
  mode: review
  asset_class: equity
  account_lock: "619508153"
  time_window: "10:00-15:55 America/New_York"
  cron_hint: "0 15 * * 3"
  allowlist: [NVDA, AMD, AVGO, SMCI, ARM, TSLA, LLY, NVO, VST, CEG, TLN, COIN, MSTR, PLTR, META]
  max_position_pct: 33
  max_concurrent_positions: 2
  capability_requires: []
  profile_compatibility: [autotrader]
  requires_directors: [reflexivity-sentiment]
director_response_schema:
  required_fields: [symbol, direction, confidence, phase, invalidation]
  phases: [emergence, validation, acceleration, exhaustion, reversal]
max_hold_days: 30
exit_on_phase: [exhaustion, reversal]
---

# Reflexivity Trader

Trades positions where price action *validates* the narrative, which in turn attracts more flows, which further validates — Soros's reflexive feedback. The hard part is detection. This strategist delegates detection entirely to the `reflexivity-sentiment` director and acts on its structured response.

> Required: `_shared/intent-schema.md`. See `references/decision-rules.md` and `references/example-ticks.md`. The director's existing `reflexivity-sentiment/SKILL.md` and its sub-skills are the authoritative source for the reflexivity framework.

## Strategy summary

- **Universe:** 15 narrative-heavy large/mid-caps spanning AI, obesity, AI capex, crypto-equity, defense compute.
- **Signal source:** the `reflexivity-sentiment` director's structured response (see below).
- **Entry:** director identifies a `validation` or `acceleration` phase with confidence ≥ 0.5 on a symbol in allowlist.
- **Exit:** director returns `exhaustion` or `reversal` phase on the held symbol, OR 30-day hold cap, OR position drops below the director's stated `invalidation` price.
- **Sizing:** `notional = buying_power * 0.33 * confidence`.
- **Cadence:** Weekly, Wednesday 11am ET.

## 6-phase protocol

### Phase 1 — Pre-flight

Read state file. If a previous tick this week has already evaluated → skip.

### Phase 2 — Compose context (the load-bearing phase)

Invoke `reflexivity-sentiment` with this exact prompt:

> "Identify the single highest-conviction reflexive setup currently active in equities. Respond ONLY with a JSON object matching this schema:
>
> ```json
> {
>   "symbol": "<ticker>",
>   "direction": "long|short",
>   "phase": "emergence|validation|acceleration|exhaustion|reversal",
>   "confidence": <float 0.0-1.0>,
>   "invalidation": {"price": <number>, "reason": "<string>"},
>   "narrative": "<one sentence>"
> }
> ```
>
> If no setup meets ≥0.5 confidence, respond with `{"symbol": null}`.
>
> Also check the held positions: `{state.open_positions}`. For each, report current `phase`. Append as `{held_status: [{symbol, current_phase}]}`."

Parse the response. If `symbol` is null → skip phase 4 entries.

### Phase 3 — Signal gather

For the director's symbol (if any) + all held symbols:

- `get_equity_quotes(symbols=[...])` — current prices and prior closes.
- `get_equity_fundamentals(symbols=[...])` — market cap, P/E (for sanity, not for entry).

### Phase 4 — Decide

**Exits** (held positions):
```
for pos in open_positions:
    held_phase = director.held_status[pos.symbol]
    current_price = quotes[pos.symbol].last_trade_price
    age_days = today - pos.opened_at

    if held_phase in exit_on_phase: emit sell; reason: f"phase_{held_phase}"
    elif age_days >= max_hold_days: emit sell; reason: "max_hold_days"
    elif current_price <= pos.invalidation_price (long) or >= invalidation (short): emit sell; reason: "invalidation_hit"
```

**Entries** (director identified a setup):
```
if director.symbol and director.confidence >= 0.5 and director.phase in {"validation", "acceleration"}:
    if director.symbol in allowlist and not held:
        target_notional = buying_power * 0.33 * director.confidence
        qty = floor(target_notional / quote.last_trade_price)
        if qty == 0: skip
        if director.direction == "short": skip (cash account, no shorts)
        emit buy intent (qty, limit_price=current*1.002, reason: director.narrative)
        record director.invalidation.price in state
```

### Phase 5 — Hand off to executor

### Phase 6 — Emit & persist

State file records `open_positions` with the director's stated `invalidation_price`, `narrative`, `entry_phase`. Future exit logic uses these.

## Interactive mode

- "What does the reflexivity trader see?" — run phases 1-4 in review mode, surface the director's full response in `notes`.
- "Is NVDA a reflexive setup?" — invoke `reflexivity-sentiment` directly with NVDA-specific prompt; report director's view.

## What this strategist will never do

- Short. Cash account.
- Trade without a director call. The signal source is the director, period.
- Override director invalidation. If price hits invalidation, exit. No "but the story is still good."
- Trade outside the 15-symbol allowlist (director may flag others; strategist ignores them).
- Hold past 30 days. Reflexive themes have shelf life.
- Pyramid — single entry per symbol per cycle.
