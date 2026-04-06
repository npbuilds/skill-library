# Asset Allocation — Regime Matrix Quick Reference

## Tactical Tilt Table (vs Strategic Baseline)

| Asset Class | Goldilocks | Reflation | Deflation | Stagflation |
|-------------|-----------|-----------|-----------|-------------|
| US Equities | +5% | 0% | -5% | -10% |
| Intl Dev Equities | +5% | +5% | -5% | -5% |
| EM Equities | +5% | +5% | -10% | -10% |
| Investment Grade Bonds | -5% | -5% | +5% | -5% |
| Long Treasuries | -5% | -10% | +15% | -10% |
| TIPS | -5% | +5% | -5% | +10% |
| Commodities | -5% | +10% | -10% | +10% |
| Gold | -5% | 0% | +5% | +10% |
| Cash | -5% | -5% | 0% | +10% |

*Tilts expressed as deviation from policy weights. Apply within ±10% guardrails.*

## Framework Selection by Investor Type

| Investor | Framework | Key Advantage |
|----------|-----------|---------------|
| Passive / time-poor | Permanent Portfolio (25/25/25/25) | No regime timing required |
| Balanced / moderate | 60/40 + TIPS sleeve | Familiar, handles Goldilocks/Deflation well |
| Active / systematic | Risk Parity | Regime-agnostic, equal risk contribution |
| Institutional / long-horizon | Endowment model | Illiquidity premium access |

## Rebalancing Decision Tree

```
Portfolio drift > 5% from target?
├── NO → No action needed
└── YES → Is momentum in the drifted direction strong?
          ├── YES → Wait up to 3 months, then rebalance
          └── NO → Rebalance now
                   └── In taxable account?
                       ├── YES → Harvest losses, use new contributions first
                       └── NO → Rebalance directly
```

## Common Allocation Mistakes

| Mistake | Why It Hurts | Fix |
|---------|--------------|-----|
| Using S&P 500 as sole benchmark | Ignores bonds/intl/alts, creates behavioral pressure to de-diversify | Use blended benchmark matching your actual allocation |
| Ignoring correlation regime | 60/40 failed in 2022 because stock-bond correlation flipped positive | Add inflation hedge sleeve (commodities, TIPS) for regime resilience |
| Over-diversifying (>10-12 asset classes) | Complexity without diversification benefit | Consolidate to fewer, more distinct risk premia |
| Tactical drift becoming permanent | Time-limited bets become strategic positions without review | Set explicit time-based or signal-based reversion triggers |
