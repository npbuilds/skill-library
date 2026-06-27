# Earnings Event Trader — Example Ticks

## Example 1: No earnings yesterday/today (typical tick)

**Context:** Tuesday 10:00 ET. No allowlist names reported in the last 24h.

```json
{
  "actions": [],
  "notes": "no_earnings_in_window"
}
```

---

## Example 2: Earnings reported, no trigger (beat + gap up)

**Context:** AAPL reported AM today. Beat by $0.12. Gap UP 1.5%.

Trigger: `beat=true, gap=+1.5%` → not below -2% threshold → skip.

```json
{
  "actions": [],
  "notes": "AAPL beat $1.50 vs $1.38 est, but gap +1.5% (no fade setup)"
}
```

---

## Example 3: Triggered entry — NVDA beat-but-down

**Context:** NVDA reported PM yesterday. Beat $0.45 vs $0.42 est. Today's open gapped down 3.2% from prior close. Current price $118.50, prior close $122.40. Buying power $1000.

```
notional = 250
qty = floor(250 / 118.50) = 2 shares
limit = 118.62
```

```json
{
  "symbol": "NVDA",
  "side": "buy",
  "quantity_type": "shares",
  "qty": 2,
  "order_type": "limit",
  "limit_price": 118.62,
  "intent_price": 118.50,
  "status": "reviewed",
  "reason": "beat $0.45 vs $0.42, gap -3.2%"
}
```

---

## Example 4: Exit on target

**Context:** NVDA entered at $118.50 three trading days ago. Current price $122.20. P&L = +3.1%.

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 2,
  "order_type": "market",
  "status": "reviewed",
  "reason": "target_hit"
}
```

---

## Example 5: Suppressed by regime

**Context:** AAPL beat AM, gapped down 2.5%. But `regime-intelligence` returned a one-line summary including "beats_punished_broadly" (e.g. early-cycle, multiple compression season).

Phase 4 skips entries. Existing open positions still exit by rules.

```json
{
  "actions": [],
  "notes": "AAPL beat-but-down setup triggered (gap -2.5%) but suppressed: regime=beats_punished_broadly"
}
```
