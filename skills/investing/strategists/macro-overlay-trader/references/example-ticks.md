# Macro Overlay Trader — Example Ticks

## Example 1: First-of-month, quadrant stable, already aligned

**Context:** Director returns q2 with confidence 0.7. State already has q2. Current allocation: SPY 60%, TLT 30%, IEF 10% — exactly target.

```json
{
  "actions": [],
  "notes": "quadrant=q2 (confidence 0.7); allocation within drift threshold"
}
```

State `last_normal_cadence_at` updated.

---

## Example 2: First-of-month rotation (newly-funded $1k account, all cash)

**Context:** $1000 in cash, no positions. Director: q2, confidence 0.7.

```
Target = SPY 60%, TLT 30%, GLD 0%, IEF 10%
Current = SPY 0%, TLT 0%, GLD 0%, IEF 0% (all cash)

delta_pct: SPY +60%, TLT +30%, IEF +10%
delta_usd: SPY +$600, TLT +$300, IEF +$100
clamp at ±$150 (15% of $1000)
```

Three intents, each clamped to $150 max:

```json
[
  {"symbol": "SPY", "side": "buy", "notional_usd": 150.00, "reason": "Quadrant q2_growth_up_inflation_down: drift +60.0% from target 60%"},
  {"symbol": "TLT", "side": "buy", "notional_usd": 150.00, "reason": "Quadrant q2_growth_up_inflation_down: drift +30.0% from target 30%"},
  {"symbol": "IEF", "side": "buy", "notional_usd": 100.00, "reason": "Quadrant q2_growth_up_inflation_down: drift +10.0% from target 10%"}
]
```

The strategist will keep firing each first-of-month until aligned (~3 months at clamp speed).

---

## Example 3: Quadrant change triggers off-cadence rebalance

**Context:** Mid-month. Last state's quadrant: q2. Director now reports: q4 (growth↓ inflation↓), confidence 0.6.

Quadrant flipped → off-cadence allowed.

```
Target q4 = SPY 30%, GLD 10%, TLT 50%, IEF 10%
Current  = SPY 60%, GLD 0%,  TLT 30%, IEF 10%

delta: SPY -30%, GLD +10%, TLT +20%, IEF 0%
delta_usd (account $1000): SPY -$300, GLD +$100, TLT +$200, IEF 0
clamp at ±$150
```

```json
[
  {"symbol": "SPY", "side": "sell", "notional_usd": 150.00, "reason": "Quadrant q4_growth_down_inflation_down: drift -30.0% from target 30%"},
  {"symbol": "GLD", "side": "buy",  "notional_usd": 100.00, "reason": "Quadrant q4_growth_down_inflation_down: drift +10.0% from target 10%"},
  {"symbol": "TLT", "side": "buy",  "notional_usd": 150.00, "reason": "Quadrant q4_growth_down_inflation_down: drift +20.0% from target 50%"}
]
```

State `last_quadrant_at` updated. Subsequent ticks continue closing the gap.

---

## Example 4: Low confidence — skip

**Context:** Director: `{"quadrant": "q3_growth_down_inflation_up", "confidence": 0.4, ...}`.

Confidence < 0.5 → skip rebalance.

```json
{
  "actions": [],
  "notes": "regime ambiguous: confidence 0.4 < 0.5; allocation unchanged"
}
```

---

## Example 5: Director response invalid (data anomaly)

**Context:** Director returns prose instead of JSON. Strategist can't parse `quadrant`.

```json
{
  "actions": [],
  "aborted": null,
  "notes": "data_anomaly: regime-intelligence response not valid JSON; quadrant unknown"
}
```

Note: not aborted — pre-flight passed, the strategist just couldn't get usable signal. Healthy no-op.
