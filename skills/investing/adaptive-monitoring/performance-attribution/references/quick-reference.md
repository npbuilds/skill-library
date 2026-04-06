# Performance Attribution — Quick Reference


## Benchmark Selection Guide

| Portfolio Type | Appropriate Benchmark |
|---------------|----------------------|
| US large cap equity | S&P 500 or Russell 1000 |
| US total equity | Russell 3000 or CRSP Total Market |
| Global equity | MSCI ACWI or FTSE All-World |
| US aggregate bonds | Bloomberg US Aggregate Bond Index |
| 60/40 balanced | 60% MSCI ACWI / 40% Bloomberg Global Agg |
| Multi-asset with alts | Custom blend reflecting target allocation |
| Absolute return / hedge fund | Cash + spread (e.g., T-bills + 300bps) |
| Private equity | Public market equivalent (PME) with illiquidity premium |

## Formula / Pseudocode

```
Total Return:          +12.0%
  Market Beta:          +8.5%  (70.8%)
  Size (SMB):           +0.5%  ( 4.2%)
  Value (HML):          -0.3%  (-2.5%)
  Momentum (MOM):       +2.1%  (17.5%)
  Alpha (residual):     +1.2%  (10.0%)
```

## Formula / Pseudocode

```
Max Drawdown = Largest peak-to-trough decline
Calmar = Annualized Return / |Max Drawdown|
```

## Formula / Pseudocode

```
Years needed for 95% confidence that alpha > 0:
  n = (1.96 * TE / a)^2
```
