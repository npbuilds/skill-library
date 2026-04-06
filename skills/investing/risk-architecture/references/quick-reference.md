# Risk Architecture — Quick Reference


## Quick Reference

| Question Pattern | Route To | Why |
|-----------------|----------|-----|
| Kelly criterion, position size, how much to buy, risk budget, conviction sizing | `position-sizing` | Core position sizing methodology |
| Volatility targeting, equal risk contribution, risk parity at position level | `position-sizing` | Volatility-adjusted sizing |
| Portfolio heat, total risk, when to stop adding positions | `position-sizing` | Aggregate position risk |
| Concentration vs diversification, Druckenmiller sizing, anti-martingale | `position-sizing` | Conviction-based sizing |
| Fat tails, black swans, antifragility, Taleb, barbell strategy | `tail-risk` | Tail risk and convexity |
| Tail hedging, OTM puts, Universa, long volatility, convexity | `tail-risk` | Tail protection mechanics |
| Via negativa, hidden fragilities, portfolio audit for risk | `tail-risk` | Fragility identification |
| Correlation breakdown, crisis correlations, regime change | `correlation-regimes` | Correlation regime analysis |
| Stocks/bonds correlation, 2022 anomaly, inflation regime | `correlation-regimes` | Cross-asset correlation |
| Diversification illusion, true diversifiers, stress testing correlations | `correlation-regimes` | Diversification validity |
| Drawdown management, loss psychology, stop-loss discipline | `drawdown-psychology` | Drawdown planning and response |
| When to cut losses vs add, Howard Marks cycle positioning | `drawdown-psychology` | Loss decision framework |
| Recovery math, uncle point, drawdown budget | `drawdown-psychology` | Drawdown mechanics and limits |

## Quick Reference

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Kelly says size big but tail-risk analysis shows fragility | Reduce to fractional Kelly and add tail hedges | Survival trumps growth; Kelly assumes known distributions, reality has fat tails |
| Position sizing says add to a winner but drawdown psychology says honor the stop | Honor the stop if the pre-defined level is hit | Pre-commitment > in-the-moment optimization; rules exist for when judgment is impaired |
| Correlation analysis says diversified but tail-risk audit finds shared fragilities | Trust the tail-risk audit over historical correlations | Historical correlations understate crisis dependence; fragility analysis is forward-looking |
| Druckenmiller concentration conflicts with risk parity equal-sizing | Depends on edge quality — high-conviction, high-edge ideas warrant concentration; uncertain ideas warrant equal risk | Match sizing method to information quality; concentration requires genuine edge |
