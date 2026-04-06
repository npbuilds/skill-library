# Tail Risk Playbook — Quick Reference

## Tail Event Classification

| Type | Trigger | Historical Examples | Hedge |
|------|---------|---------------------|-------|
| Liquidity crisis | Credit seizure, margin calls | 2008 GFC, March 2020 | Long vol, long treasuries, cash |
| Inflation shock | Supply disruption, fiscal excess | 1973-74, 2022 | Commodities, TIPS, gold |
| Growth shock | Demand collapse, credit crunch | 2001, 2008, COVID | Long treasuries, quality equities |
| Geopolitical | War, sanctions, energy disruption | 1973, 1990 Gulf War, 2022 Russia | Gold, energy, defense |
| Financial system | Bank failure, currency crisis | 1997 Asia, 2011 Euro crisis | USD, gold, CDS |

## Hedge Cost-Effectiveness Ranking

| Hedge | Annual Cost (approx) | Convexity | Best Against |
|-------|---------------------|-----------|-------------|
| Long VIX calls (30-60 delta OTM) | 2-4% drag | Very high | Liquidity/vol spikes |
| Long OTM S&P puts (10-20% OTM) | 1-3% drag | High | Equity drawdowns |
| Long gold (5-10% allocation) | 0-0.5% drag | Medium | Inflation, geopolitical |
| Long treasuries (flight-to-quality) | 0-1% drag | Medium | Deflation, growth shocks |
| Trend-following (CTA allocation) | 0.5-1.5% fees | Medium | Extended trends in any direction |
| Cash buffer (3-6 months expenses) | Inflation erosion | Low | Liquidity need, forced selling |

## Portfolio Stress Test Scenarios

### Scenario 1: 2008-Style GFC
- Equities: -55% peak to trough
- HY credit: -35%
- Long treasuries: +25%
- Gold: -10% initially, then +25%
- VIX: 80+ from ~15
- Duration: 18 months peak to trough

### Scenario 2: 2022-Style Inflation Shock
- Equities: -25%
- Long treasuries: -30% (duration losses)
- TIPS: -12% (still hurt by real rate rise)
- Gold: flat to -5%
- Commodities: +40%
- 60/40 portfolio: -17%

### Scenario 3: 2020-Style Liquidity Shock
- Equities: -35% in 5 weeks
- All credit (even IG): -15-20%
- Long treasuries: +8%
- Gold: -12% (margin calls, liquidation)
- VIX: 85+ from ~15
- Recovery: V-shaped, 6 months to new highs

## Tail Risk Budget Framework

```
Total portfolio risk budget = 100%
├── Core positions: 80%
├── Hedges: 15%
│   ├── Structural (permanent): 10%  [gold, trend-following]
│   └── Tactical (regime-based): 5%  [vol, OTM puts when VIX < 15]
└── Cash buffer: 5%
```

Rule: Hedge cost should not exceed expected annual alpha from the core portfolio.
