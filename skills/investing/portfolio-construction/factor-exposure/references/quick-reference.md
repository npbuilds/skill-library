# Factor Exposure — Quick Reference


## Factor-Regime Matrix

| Factor | Best Environment | Worst Environment | Regime Sensitivity |
|--------|-----------------|-------------------|-------------------|
| Value | Early recovery, cheap valuations, rising rates | Late expansion, growth dominance, falling rates | High — strongly cyclical |
| Momentum | Trending markets (sustained up or down), low vol | Sharp reversals, high vol, regime transitions | Moderate — crashes are the risk |
| Quality | Late cycle, recession, high uncertainty | Early recovery (junk rally), risk-on euphoria | Low — works almost always |
| Low Vol | Corrections, bear markets, high uncertainty | Strong bull markets, risk-on rallies | Moderate — anti-cyclical |
| Size | Early recovery, high risk appetite, credit easing | Late cycle, tightening, flight to quality | High — pro-cyclical |
| Carry | Low vol, stable growth, "Goldilocks" | Risk-off events, sudden regime shifts, vol spikes | High — crashes in risk-off |

## Implementation Options

| Vehicle | Annual Cost | Factor Purity | Liquidity | Tax Efficiency |
|---------|-------------|---------------|-----------|----------------|
| Cap-weighted index ETF | 0.03-0.10% | None (market beta only) | Highest | Highest |
| Single-factor ETF | 0.15-0.35% | Moderate | High | High |
| Multi-factor ETF | 0.20-0.40% | Moderate | High | High |
| Factor mutual fund | 0.30-0.80% | Moderate-High | Daily | Moderate |
| Systematic hedge fund | 1-2% + performance fee | Highest | Quarterly-Annual | Low |
| Direct indexing | 0.25-0.45% platform fee | Customizable | Daily | Highest (tax harvesting) |

## Quick Reference

| Factor | Baseline Weight | Vehicle |
|--------|----------------|---------|
| Value | 25% | AVUV (small-cap value) + VLUE or RPV (large-cap value) |
| Momentum | 20% | MTUM or individual momentum strategy |
| Quality | 25% | QUAL or DFA/Avantis quality-integrated funds |
| Low Vol | 15% | USMV or EFAV (international) |
| Broad Market | 15% | VTI or ITOT (market beta as anchor) |

## Formula / Pseudocode

```
Pure Passive (cap-weighted index) ← Smart Beta → Active Management
   Market return                    Factor premia     Alpha (skill)
   Lowest cost                     Moderate cost      Highest cost
   No skill required               Rules-based        Skill-dependent
```
