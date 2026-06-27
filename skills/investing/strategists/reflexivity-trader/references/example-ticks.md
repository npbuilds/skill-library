# Reflexivity Trader — Example Ticks

## Example 1: Director returns null (no high-confidence setup)

**Context:** Wednesday 11:00 ET. Director responds:
```json
{"symbol": null, "held_status": []}
```

```json
{
  "actions": [],
  "notes": "director: no setup ≥0.5 confidence active"
}
```

State updated with `this_week_evaluated` so next tick won't double-evaluate.

---

## Example 2: Director flags NVDA, qualifying entry

**Context:** Buying power $1000. Director response:
```json
{
  "symbol": "NVDA",
  "direction": "long",
  "phase": "acceleration",
  "confidence": 0.7,
  "invalidation": {"price": 108.00, "reason": "200d SMA breach"},
  "narrative": "AI capex acceleration; major tenant CapEx revisions up 25%",
  "held_status": []
}
```

Phase 4 entry: NVDA in allowlist, not held, confidence ≥ 0.5, phase in {validation, acceleration}, direction=long.

```
target = 1000 * 0.33 * 0.7 = $231
NVDA at $120 → qty = floor(231 / 120) = 1
```

```json
{
  "symbol": "NVDA",
  "side": "buy",
  "quantity_type": "shares",
  "qty": 1,
  "order_type": "limit",
  "limit_price": 120.24,
  "intent_price": 120.00,
  "status": "reviewed",
  "reason": "AI capex acceleration; major tenant CapEx revisions up 25%"
}
```

State records `invalidation_price: 108.00`.

---

## Example 3: Director flags short-only setup (refused)

**Context:** Director response:
```json
{"symbol": "TSLA", "direction": "short", "phase": "reversal", "confidence": 0.8, ...}
```

Phase 4 entry check: `direction != "long"` → skip with `notes: "director_signal_short_refused_cash_account"`.

---

## Example 4: Held position exits on director's exhaustion call

**Context:** NVDA held 14 days at entry $120, current $135. Director response includes:
```json
{
  "held_status": [{"symbol": "NVDA", "current_phase": "exhaustion"}]
}
```

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 1,
  "order_type": "market",
  "status": "reviewed",
  "reason": "phase_exhaustion"
}
```

State `open_positions` empty.

---

## Example 5: Invalidation hit between director ticks

**Context:** Wednesday tick. NVDA held at entry $120, invalidation $108. Director currently reports NVDA still in `acceleration`. But current price dropped to $107.50 since last director read.

Phase 4 exit check: `current_price <= invalidation_price (108)` → sell regardless of director's view.

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 1,
  "status": "reviewed",
  "reason": "invalidation_hit"
}
```

The strategist obeys the *prior* director's invalidation even when the *current* director hasn't yet caught up. The invalidation is a hard rule.
