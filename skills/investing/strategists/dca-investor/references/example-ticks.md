# DCA Investor — Example Ticks

Five worked examples covering the main outcomes. Each shows pre-flight result, intent set, executor return, and the final `tick_decision`.

---

## Example 1: Healthy review tick (mode=review, Monday)

**Context:** Monday 10:00 ET, mode=review, $1,000 buying power, last placement 7 days ago, no circuit breaker.

**Pre-flight (strategist-side cadence):** PASS — 7 days since last tick.

**Intents emitted:**
```json
[
  {"symbol": "SPY", "side": "buy", "quantity_type": "notional", "notional_usd": 25.00, "order_type": "market", "intent_price": 482.15, "max_slippage_pct": 1.0, "reason": "DCA weekly tranche — SPY 50% of $50 = $25", ...},
  {"symbol": "QQQ", "side": "buy", "quantity_type": "notional", "notional_usd": 15.00, "order_type": "market", "intent_price": 415.30, "max_slippage_pct": 1.0, "reason": "DCA weekly tranche — QQQ 30% of $50 = $15", ...},
  {"symbol": "BND", "side": "buy", "quantity_type": "notional", "notional_usd": 10.00, "order_type": "market", "intent_price": 72.85, "max_slippage_pct": 1.0, "reason": "DCA weekly tranche — BND 20% of $50 = $10", ...}
]
```

**Executor:** runs full pre-flight (passes), validates each intent (passes), calls `review_equity_order` × 3, no anomalies, no slippage breach. Returns three RealizedActions with `status: reviewed`.

**State file:** NOT updated (review-only).

**tick_decision:**
```json
{
  "tick_utc": "2026-06-29T14:00:00Z",
  "strategy": "dca-investor",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 1000.00,
  "actions": [
    {"symbol": "SPY", "side": "buy", "quantity_type": "notional", "qty": 0.052, "notional_usd": 25.00, "intent_price": 482.15, "realized_review_price": 482.07, "status": "reviewed", "reason": "...", "order_id": null, "alerts": []},
    {"symbol": "QQQ", "side": "buy", "quantity_type": "notional", "qty": 0.036, "notional_usd": 15.00, "intent_price": 415.30, "realized_review_price": 415.22, "status": "reviewed", "reason": "...", "order_id": null, "alerts": []},
    {"symbol": "BND", "side": "buy", "quantity_type": "notional", "qty": 0.137, "notional_usd": 10.00, "intent_price": 72.85, "realized_review_price": 72.84, "status": "reviewed", "reason": "...", "order_id": null, "alerts": []}
  ],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "regime: late-cycle, disinflation, easing bias"
}
```

---

## Example 2: Cadence-not-due skip

**Context:** Monday 10:00 ET, last successful tick was 4 days ago (someone ran the cron manually).

**Strategist-side cadence check:** FAIL — only 4 days elapsed.

**Executor not invoked.**

**tick_decision:**
```json
{
  "tick_utc": "2026-06-26T14:00:00Z",
  "strategy": "dca-investor",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 950.00,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "cadence_not_due; last placement 2026-06-22T14:00Z; next eligible 2026-06-28T14:00Z"
}
```

Note `account_value` and `buying_power` are populated even though the executor wasn't invoked — the strategist makes a quick `get_portfolio` call for the snapshot. This is fine; it's read-only and cheap.

---

## Example 3: Account-lock failure (Codex finding 3 verification)

**Context:** Frontmatter `account_lock` has been changed to `"999999"` (wrong number — for a test). Otherwise normal Monday.

**Strategist-side cadence:** PASS.

**Executor pre-flight 1.1:** `get_accounts()` returns Nirav's 5 accounts. None match `"999999"`. Abort.

**Executor returns:**
```json
{"aborted": "account_lock_failed", "circuit_breaker_tripped": false, "account_value": 0, "buying_power": 0, "actions": []}
```

**tick_decision:**
```json
{
  "tick_utc": "2026-06-29T14:00:00Z",
  "strategy": "dca-investor",
  "mode": "review",
  "account_value": 0,
  "buying_power": 0,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": "account_lock_failed",
  "notes": "no account with account_number=999999 (or agentic_allowed=false on match)"
}
```

State file NOT updated. The operator sees the abort and fixes the frontmatter.

---

## Example 4: Circuit breaker tripped (mid-week drawdown scenario)

**Context:** Monday 10:00 ET. The autotrader had a bad week — realized P&L for today is −$60 against a day-start portfolio value of $1,000. That's −6%, beyond the 5% threshold.

**Executor pre-flight 1.6:** `get_realized_pnl(span=day).total_realized_gain == -60.00`. `loss_pct = -0.06`. Trip the breaker.

**Phase 2 intent validation:** All three intents are `side: buy`. Each gets dropped with `status: skipped, reason: "circuit_breaker_tripped"`.

**tick_decision:**
```json
{
  "tick_utc": "2026-06-29T14:00:00Z",
  "strategy": "dca-investor",
  "mode": "review",
  "account_value": 940.00,
  "buying_power": 940.00,
  "actions": [
    {"symbol": "SPY", "side": "buy", "quantity_type": "notional", "notional_usd": 25.00, "intent_price": 482.15, "status": "skipped", "reason": "circuit_breaker_tripped", "order_id": null, "alerts": []},
    {"symbol": "QQQ", "side": "buy", "quantity_type": "notional", "notional_usd": 15.00, "intent_price": 415.30, "status": "skipped", "reason": "circuit_breaker_tripped", "order_id": null, "alerts": []},
    {"symbol": "BND", "side": "buy", "quantity_type": "notional", "notional_usd": 10.00, "intent_price": 72.85, "status": "skipped", "reason": "circuit_breaker_tripped", "order_id": null, "alerts": []}
  ],
  "circuit_breaker_tripped": true,
  "aborted": null,
  "notes": "daily realized P&L -6.00% exceeds -5.00% threshold; only sells permitted"
}
```

Note `aborted == null` even though every action was skipped — the *tick* ran successfully; the *actions* were gated. State file NOT updated.

---

## Example 5: Live tick with placement (post-promotion, weekly Monday)

**Context:** User has promoted `mode: review` → `mode: live`. Monday 10:00 ET, cron run, $1,000 buying power, no circuit breaker, fresh quotes.

**Pre-flight:** PASS.
**Phase 2:** All three intents pass validation.
**Phase 3 review:** All three pass slippage (realized within 0.02% of intent).
**Phase 4 routing:** context=cron, mode=live → place. Three `place_equity_order` calls; three filled orders.

**State file UPDATED.**

**tick_decision:**
```json
{
  "tick_utc": "2026-06-29T14:00:05Z",
  "strategy": "dca-investor",
  "mode": "live",
  "account_value": 1000.00,
  "buying_power": 950.00,
  "actions": [
    {"symbol": "SPY", "side": "buy", "quantity_type": "notional", "qty": 0.052, "notional_usd": 25.00, "intent_price": 482.15, "realized_review_price": 482.07, "status": "placed", "reason": "DCA weekly tranche — SPY 50% of $50 = $25", "order_id": "f3a8...", "alerts": []},
    {"symbol": "QQQ", "side": "buy", "quantity_type": "notional", "qty": 0.036, "notional_usd": 15.00, "intent_price": 415.30, "realized_review_price": 415.22, "status": "placed", "reason": "DCA weekly tranche — QQQ 30% of $50 = $15", "order_id": "9b1c...", "alerts": []},
    {"symbol": "BND", "side": "buy", "quantity_type": "notional", "qty": 0.137, "notional_usd": 10.00, "intent_price": 72.85, "realized_review_price": 72.84, "status": "placed", "reason": "DCA weekly tranche — BND 20% of $50 = $10", "order_id": "2d4e...", "alerts": []}
  ],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "regime: late-cycle, disinflation, easing bias"
}
```
