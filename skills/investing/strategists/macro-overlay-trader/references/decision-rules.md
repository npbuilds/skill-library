# Macro Overlay Trader — Decision Rules

## Constants

| Constant | Value |
|---|---|
| `drift_thresholds.normal` | 0.05 (5%) |
| `drift_thresholds.panic` | 0.15 (15%, currently unused — kept for symmetry) |
| `per_tick_clamp_pct` | 0.15 |
| `confidence_floor` | 0.5 |
| `max_slippage_pct` (per intent) | 0.5 |

## Quadrant target weights

| Quadrant | SPY | GLD | TLT | IEF | Thesis |
|---|---|---|---|---|---|
| q1 — growth↑ inflation↑ | 0.50 | 0.30 | 0.00 | 0.20 | Reflation: equities + gold; avoid long duration. |
| q2 — growth↑ inflation↓ | 0.60 | 0.00 | 0.30 | 0.10 | Goldilocks: equities + long duration; no gold need. |
| q3 — growth↓ inflation↑ | 0.20 | 0.50 | 0.00 | 0.30 | Stagflation: gold-heavy; equities tactical-light. |
| q4 — growth↓ inflation↓ | 0.30 | 0.10 | 0.50 | 0.10 | Deflation: long duration leads; equities defensive. |

These are starting weights. Future versions may layer in additional signals (yield-curve shape, dollar trend, energy prices) for sub-quadrant tilts.

## Director response contract

`regime-intelligence` MUST respond with valid JSON matching:

```json
{
  "quadrant": "q1_growth_up_inflation_up | q2_growth_up_inflation_down | q3_growth_down_inflation_up | q4_growth_down_inflation_down",
  "confidence": 0.0-1.0,
  "transition_risk": "<string>",
  "one_line_justification": "<string>"
}
```

If response is not valid JSON or quadrant value is outside the enum: `data_anomaly`, skip the tick.

## Trigger rules

| Condition | Action |
|---|---|
| First-of-month + confidence ≥ 0.5 | Run rebalance |
| Mid-month + quadrant changed since last tick + confidence ≥ 0.5 | Run rebalance |
| confidence < 0.5 | Skip (regime ambiguous) |
| Director's quadrant matches state's last quadrant + within month | Skip (already aligned) |

## Anti-rules

| Refused | Reason |
|---|---|
| Trade above 15% of account per tick | Smooth regime shifts. |
| Hold non-allowlist symbols | Hard rule. |
| Run with director confidence < 0.5 | Regime unknown ≠ act blindly. |
| Override quadrant at runtime | Director's word is final. |

## State file shape

`~/.hermes/profiles/autotrader/state/macro-overlay-trader.json`:

```json
{
  "last_normal_cadence_at": "2026-06-01T15:00:00-04:00",
  "last_quadrant_at": {
    "quadrant": "q2_growth_up_inflation_down",
    "first_seen": "2026-05-01T15:00:00-04:00",
    "confidence": 0.7
  },
  "rotation_count": 4,
  "current_holdings_snapshot": {"SPY": 0.55, "TLT": 0.28, "GLD": 0.00, "IEF": 0.12, "CASH": 0.05}
}
```
