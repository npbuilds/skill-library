---
name: risk-architecture
description: >
  Direct the risk architecture subdomain — route questions about position sizing, tail risk,
  correlation regimes, and drawdown psychology to the right specialist skill. Use when managing
  portfolio risk, sizing positions, hedging tail events, or navigating drawdowns.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Glob
---

# Risk Architecture Director

The department head for portfolio risk management within the investing domain. Routes questions to the right specialist, defines the learning order, and resolves conflicts between risk frameworks.

## Routing Logic

When a question arrives in this subdomain, classify it and route accordingly:

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

### Multi-Skill Questions

Some questions need more than one skill. Load them in this priority:

1. `position-sizing` — establish how large each position should be
2. `tail-risk` — evaluate whether the portfolio survives extreme events
3. `correlation-regimes` — assess whether diversification assumptions hold
4. `drawdown-psychology` — plan for behavioral response to losses

This order ensures sizing is grounded first, then stress-tested for tails, validated for correlation assumptions, and finally checked against psychological tolerance.

**Example multi-skill question**: "I want to build a concentrated portfolio of 8 positions — how do I size them and protect against a crash?"
1. `position-sizing` — Use Kelly/risk-budget framework to size each position based on conviction and volatility
2. `tail-risk` — Apply barbell logic: allocate a portion to convex tail hedges (OTM puts or long vol)
3. `correlation-regimes` — Stress-test the 8 positions under crisis correlation (do they all sell together?)
4. `drawdown-psychology` — Define the uncle point and stop-loss discipline before entry

**Example multi-skill question**: "My portfolio is down 25% — should I cut losses or add?"
1. `drawdown-psychology` — Apply the thesis-intact vs price-changed framework; check against pre-defined drawdown budget
2. `position-sizing` — If adding, recalculate position size given reduced capital and current volatility
3. `correlation-regimes` — Assess whether the drawdown is idiosyncratic or a regime shift affecting all positions

## Curriculum Order

For learning or progressive loading:

1. **Position Sizing** (foundation) — The most consequential risk decision. Getting the size right matters more than getting the entry right. Kelly criterion, risk budgets, and volatility-adjusted sizing provide the mathematical backbone. Without this, all other risk management is built on sand.

2. **Tail Risk** (extension) — Once you know how to size positions, you need to understand what can destroy them. Taleb's framework for fragility, antifragility, and convexity teaches you to survive the events that standard risk models miss. Builds on position sizing by reframing risk as non-linear.

3. **Correlation Regimes** (extension) — Diversification is the most overused word in finance. This skill teaches when diversification works, when it fails, and what truly diversifies. Builds on tail risk by explaining why "everything goes down together" in crises.

4. **Drawdown Psychology** (capstone) — The human element. Knowing the math of position sizing, tail risk, and correlation is worthless if you panic at -30% and sell everything. This skill integrates the technical framework with behavioral discipline. Requires all three prior skills as context.

### Level Progression
- **Foundational**: Position Sizing
- **Intermediate**: Tail Risk, Correlation Regimes
- **Advanced**: Drawdown Psychology (integrates all prior skills)

## Conflict Resolution

When child skills give contradictory guidance:

| Conflict | Resolution | Reason |
|----------|-----------|--------|
| Kelly says size big but tail-risk analysis shows fragility | Reduce to fractional Kelly and add tail hedges | Survival trumps growth; Kelly assumes known distributions, reality has fat tails |
| Position sizing says add to a winner but drawdown psychology says honor the stop | Honor the stop if the pre-defined level is hit | Pre-commitment > in-the-moment optimization; rules exist for when judgment is impaired |
| Correlation analysis says diversified but tail-risk audit finds shared fragilities | Trust the tail-risk audit over historical correlations | Historical correlations understate crisis dependence; fragility analysis is forward-looking |
| Druckenmiller concentration conflicts with risk parity equal-sizing | Depends on edge quality — high-conviction, high-edge ideas warrant concentration; uncertain ideas warrant equal risk | Match sizing method to information quality; concentration requires genuine edge |

**General rule**: Survival > returns. When frameworks disagree, the more conservative risk assessment takes priority. Position sizing optimizes growth; tail risk and drawdown psychology impose constraints. Constraints always override optimization.

## Scope Boundaries

**This director handles**: All portfolio risk management — position sizing, tail risk hedging, correlation analysis, drawdown planning, and the integration of these frameworks into a coherent risk architecture.

**Escalate to the orchestrator when**:
- The question involves security selection or valuation (not risk management)
- The question involves macroeconomic regime identification (Regime Intelligence)
- The question involves portfolio construction beyond risk (asset allocation, factor exposure)
- The question spans multiple investing subdomains and needs orchestrator-level coordination
