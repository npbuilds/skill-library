# Portfolio Rules

The Archon's paper trading portfolio rules. These are self-modifiable — the Archon can evolve them via `adjust_portfolio_rules()` with documented rationale.

## Current Rules

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Initial capital | $1,000,000 | Standard institutional sizing for tracking |
| Max position size | 15% of capital | Forces diversification while allowing conviction |
| Max positions | 8 | Manageable number for daily thesis review |
| Default stop-loss | -5% from entry | Tudor Jones defense discipline |
| Conviction sizing | Enabled | H = up to max, M = half, L = monitoring only |

## Sizing Rules

| Conviction | Max Size | Rationale |
|------------|----------|-----------|
| HIGH | 15% (max_position_pct) | Multiple frameworks agree, asymmetry clear, risk defined |
| MEDIUM | 7.5% (half of max) | Framework support with caveats, some assumptions uncertain |
| LOW | 0% (monitoring only) | Interesting signal but insufficient evidence — watch, don't trade |

## Entry Criteria

Every position must have:
1. **Thesis source**: Which briefing analysis drove this (contrarian_scorecard, regime_shift, alert, reflexivity_signal, etc.)
2. **Thesis text**: Specific, falsifiable statement of why this trade should work
3. **Confidence**: H/M/L
4. **Regime context**: What regime was active (the thesis may not survive a regime change)
5. **Stop-loss**: Price level that invalidates the thesis
6. **Target** (optional): Price level for profit-taking

## Exit Criteria

Positions are closed for one of these reasons:
- `target_hit`: Profit target reached
- `stop_hit`: Stop-loss triggered
- `thesis_broken`: The underlying premise no longer holds
- `regime_change`: The macro regime shifted, invalidating the thesis context
- `rebalance`: Portfolio-level risk management

## Thesis Outcome Classification

When closing a trade, classify the thesis outcome:
- `correct`: The thesis played out as expected
- `wrong`: The thesis was fundamentally incorrect (but trade may still have been profitable)
- `stopped_out`: The thesis may have been right, but timing was wrong
- `invalidated`: External events made the thesis irrelevant (not right or wrong)

## Rules History

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-04-09 | Initial rules set | Starting point for portfolio tracking. Conservative sizing to build calibration data. |

*The Archon may add entries to this table when it adjusts rules via `adjust_portfolio_rules()`. All changes must be documented with rationale.*
