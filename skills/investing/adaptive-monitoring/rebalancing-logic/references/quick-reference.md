# Rebalancing Logic — Quick Reference


## Quick Reference

| Asset Class Weight | Suggested Absolute Threshold | Suggested Relative Threshold |
|-------------------|-----------------------------|-----------------------------|
| >30% | 5 percentage points | 15-20% of target |
| 15-30% | 4 percentage points | 20-25% of target |
| 5-15% | 3 percentage points | 25-30% of target |
| <5% | 2 percentage points | 30-50% of target |

## The Tax-Aware Decision Framework

```
IF asset class is overweight AND in a taxable account:
  1. First: Can new contributions fix the drift? → Use contributions
  2. Second: Can dividends be redirected? → Redirect dividends
  3. Third: Are there offsetting losses available? → Harvest losses and rebalance simultaneously
  4. Fourth: Is the overweight position in an asset with long-term gain? → Consider partial rebalance only
  5. Last resort: Sell and accept the tax hit → Only if drift exceeds emergency threshold
```

## Step 1 — Check Drift (Monthly)

```
FOR each asset class:
  drift = |actual_weight - target_weight|
  IF drift > threshold:
    FLAG for review
  ELSE:
    No action needed
```

## Step 2 — Assess the Cause

```
IF flagged positions exist:
  FOR each flagged position:
    IS drift from price movement (passive drift)?
      → Proceed to Step 3 (standard rebalancing)
    IS drift from thesis change (active decision)?
      → Proceed to Thesis Invalidation Triggers above
    IS drift from cash flow (contribution/withdrawal)?
      → Direct cash flow to fix drift (most tax-efficient)
```

## Step 3 — Choose Rebalancing Method

```
IF in a tax-deferred account:
  → Full rebalance to target weights (no tax consequences)

IF in a taxable account:
  IF new contributions can fix drift:
    → Direct contributions to underweight asset classes
  ELIF tax-loss harvesting opportunities exist:
    → Harvest losses and rebalance simultaneously
  ELIF drift is moderate (within 1.5x threshold):
    → Partial rebalance to band edge, not target
  ELIF drift is severe (>2x threshold):
    → Full rebalance — accept tax cost for risk management
```

## Step 4 — Execute and Document

```
1. Calculate exact trade sizes
2. Execute trades (use limit orders, not market orders)
3. Record: date, positions, sizes, rationale, cost estimate
4. Set next review date
5. Update monitoring thresholds if portfolio structure changed
```

## Step 5 — Post-Trade Verification

```
1. Confirm new weights are within tolerance bands
2. Verify no unintended sector/factor concentrations from the trades
3. Recalculate portfolio risk metrics with new weights
4. Update tax lot records for future harvesting opportunities
5. Archive the decision rationale for future attribution reviews
```
