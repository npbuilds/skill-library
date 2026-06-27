# Swing Trader — Example Ticks

## Example 1: No-op (no oversold names, no positions to exit)

**Context:** RSI(14) values across allowlist: SPY 52, QQQ 55, AAPL 48, MSFT 50, NVDA 65, GOOGL 49, META 58, AMZN 53. No open positions.

**Phase 4:** All RSI > oversold → no entries. No positions → no exits.

```json
{
  "tick_utc": "...",
  "strategy": "swing-trader",
  "mode": "review",
  "account_value": 1000.00,
  "buying_power": 1000.00,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": null,
  "notes": "8/8 above oversold; lowest RSI: AAPL 48"
}
```

---

## Example 2: New entry on deep-oversold name

**Context:** AAPL RSI 18 (deep oversold). AAPL quote $182. Buying power $1000. No microstructure regime warning.

```
conviction = (30-18)/30 = 0.4
target_notional = 1000 * 0.25 * 0.4 = $100
qty = floor(100 / 182) = 0  → too small
```

Skip with `notes: "AAPL deep oversold but position size < 1 share at current price"`.

---

## Example 3: Successful entry on mid-cap oversold

**Context:** Hypothetical NVDA at $80, RSI 16, buying power $500.

```
conviction = clamp((30-16)/30, 0.3, 1.0) = 0.467
target_notional = 500 * 0.25 * 0.467 = $58
qty = floor(58 / 80) = 0  → too small
```

Still too small. This strategist is constrained for $1k accounts. In production, it would need larger account_value to be useful.

For example purposes assume account $5000, NVDA $80, RSI 16:
```
target_notional = 5000 * 0.25 * 0.467 = $584
qty = floor(584 / 80) = 7
```

**tick_decision action:**
```json
{
  "symbol": "NVDA",
  "side": "buy",
  "quantity_type": "shares",
  "qty": 7,
  "intent_price": 80.10,
  "realized_review_price": 80.12,
  "order_type": "limit",
  "limit_price": 80.18,
  "status": "reviewed",
  "reason": "RSI(14)=16, conviction 0.47"
}
```

---

## Example 4: Exit on RSI revert

**Context:** AAPL position opened 4 trading days ago at RSI 22, current RSI 73, qty=2 shares.

**Phase 4 exit check:** `current_rsi >= overbought` → sell.

```json
{
  "symbol": "AAPL",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 2,
  "status": "reviewed",
  "reason": "rsi_revert"
}
```

State updated: AAPL removed from `open_positions`, `closed_count_30d` incremented.

---

## Example 5: Force exit on max age

**Context:** NVDA position opened 10 trading days ago, current RSI 45 (not yet overbought).

**Phase 4 exit check:** `age_days >= max_days` → sell regardless of RSI.

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "quantity_type": "shares",
  "qty": 7,
  "status": "reviewed",
  "reason": "max_age"
}
```

The strategy doesn't second-guess: hitting 10 days means exit.
