# Day Trader — Example Ticks

## Example 1: Waiting for OR close

**Context:** 09:35 ET, no positions. OR window still open.

```json
{
  "tick_utc": "2026-06-26T13:35:00Z",
  "strategy": "day-trader",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 1000.00,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "waiting_for_or_close"
}
```

---

## Example 2: No breakouts (typical mid-morning tick)

**Context:** 10:30 ET. Today's OR for each name has been computed. No symbol has closed a 5-min bar above its OR-high. No open position.

```json
{
  "actions": [],
  "notes": "no_breakouts; closest: NVDA 0.4% below OR-high"
}
```

---

## Example 3: Long entry on NVDA breakout

**Context:** 10:40 ET. NVDA OR (09:30-09:45): high=$122.30, low=$120.80. Current 5-min close: $122.40 (above OR-high). VWAP $121.60 (close > VWAP, confirmation passes). Buying power $1000.

```
qty = floor(1000 * 0.30 / 122.40) = floor(2.45) = 2 shares
stop = 120.80
target = 122.30 + 1.50 = 123.80
```

**tick_decision action:**
```json
{
  "symbol": "NVDA",
  "side": "buy",
  "quantity_type": "shares",
  "qty": 2,
  "order_type": "limit",
  "limit_price": 122.65,
  "intent_price": 122.40,
  "status": "reviewed",
  "reason": "ORB_long; OR=120.80-122.30; current 122.40>OR-high & >VWAP 121.60"
}
```

State updated: `open_position = {symbol: NVDA, qty: 2, stop: 120.80, target: 123.80, ...}`.

---

## Example 4: Stop hit on open position

**Context:** 11:20 ET. NVDA open position with stop $120.80, current price $120.65.

**Phase 4 exit:** `current_price <= stop_price` → sell.

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 2,
  "order_type": "market",
  "status": "reviewed",
  "reason": "stop_hit"
}
```

State updated: `open_position = null`, `closed_today` gets a record with negative pnl_pct.

---

## Example 5: Hard close at 15:55

**Context:** 15:55 ET. Open NVDA position, current price $123.50 (between stop and target). Neither stop nor target hit yet, but the hard-close timer fires.

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 2,
  "order_type": "market",
  "status": "reviewed",
  "reason": "hard_close"
}
```

Position liquidated at market. NVDA closes the day flat for the day-trader strategist; the SOUL hard rule "no overnight holds" is upheld.
