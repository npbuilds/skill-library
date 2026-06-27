# Rebalancer — Example Ticks

## Example 1: First-of-month, no drift, clean no-op

**Context:** First trading day of month, current weights SPY 51% / QQQ 30% / BND 19%. All within 2.5%.

**tick_decision:**
```json
{
  "tick_utc": "2026-07-01T14:00:00Z",
  "strategy": "rebalancer",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 50.00,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "drift_within_normal: SPY +1.0%, QQQ +0.0%, BND -1.0%"
}
```

State `last_normal_cadence_at` updated. No intents fired.

---

## Example 2: First-of-month, normal drift, sell+buy pair

**Context:** First trading day. SPY drifted up to 55%, QQQ down to 28%, BND down to 17%. Account value $1000.

```
SPY delta = -5%   → sell $50
QQQ delta = +2%   → skip (under 2.5%)
BND delta = +3%   → buy $30
```

Clamp at ±$100 — both within limit.

**tick_decision actions:**
```json
[
  {"symbol": "SPY", "side": "sell", "quantity_type": "notional", "notional_usd": 50.00, "status": "reviewed", "reason": "Drift -5.0% from target 50%"},
  {"symbol": "BND", "side": "buy",  "quantity_type": "notional", "notional_usd": 30.00, "status": "reviewed", "reason": "Drift +3.0% from target 20%"}
]
```

Sells listed first so the executor frees buying power before evaluating buys.

---

## Example 3: Mid-month panic fire

**Context:** Mid-month, market crash. QQQ collapsed; QQQ weight dropped to 18% (target 30% → drift +12%). Account value $850.

QQQ drift +12% exceeds `panic` threshold 10%. Fire mid-month.

```
delta_usd = +0.12 * 850 = +$102
clamp at ±$85 (10% of $850) → +$85
```

**tick_decision actions:**
```json
[
  {"symbol": "QQQ", "side": "buy", "quantity_type": "notional", "notional_usd": 85.00, "status": "reviewed", "reason": "Drift +12.0% from target 30%"}
]
```

State `last_panic_fire_at` updated. SPY and BND drifts don't matter — only panic-exceeding symbols fire mid-month.

---

## Example 4: Live cron, sell+buy pair placed

**Context:** Same as Example 2 but mode=live and cron context. Executor places both orders.

**tick_decision actions:**
```json
[
  {"symbol": "SPY", "side": "sell", "quantity_type": "notional", "qty": 0.104, "notional_usd": 50.00, "intent_price": 482.07, "realized_review_price": 482.10, "status": "placed", "order_id": "..."},
  {"symbol": "BND", "side": "buy",  "quantity_type": "notional", "qty": 0.412, "notional_usd": 30.00, "intent_price": 72.84,  "realized_review_price": 72.86,  "status": "placed", "order_id": "..."}
]
```

---

## Example 5: Allowlist contraction

**Context:** User removed VTI from `target_weights` but a prior position of 5 shares of VTI exists (perhaps placed manually). First-of-month tick.

Phase 4 sees VTI in `held_symbols - target_symbols`. Emits a sell intent for the full position (clamped at 10% of account).

**tick_decision actions:**
```json
[
  {"symbol": "VTI", "side": "sell", "quantity_type": "notional", "notional_usd": 100.00, "status": "reviewed", "reason": "Drift -X% — symbol no longer in target_weights"}
]
```
