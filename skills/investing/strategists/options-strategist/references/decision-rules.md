# Options Strategist — Decision Rules

## Constants

| Constant | Value |
|---|---|
| `target_dte.csp_min` | 21 |
| `target_dte.csp_max` | 45 |
| `target_dte.cc_min` | 14 |
| `target_dte.cc_max` | 30 |
| `target_delta.csp_short` | 0.30 |
| `target_delta.cc_short` | 0.30 |
| `delta_tolerance` | ±0.05 |
| `max_position_pct` | 25 |
| `max_concurrent_positions` | 4 |
| `max_slippage_pct` (per intent) | 5.0 |

## CSP selection

```
1. Filter to allowlist ∩ value-quality.top_picks (only sell puts on quality you'd own).
2. For each chain whose expiration is in [today+21, today+45]:
   a. Get puts whose delta ∈ [-0.35, -0.25]
   b. Compute premium/collateral ratio = bid / (strike * 100)
   c. Pick the highest-ratio contract
3. Check collateral_required = strike * 100 ≤ buying_power * 25%
4. If multiple symbols qualify, prefer ones with higher premium/collateral.
5. Max 4 concurrent short-put positions.
```

## CC selection

```
1. Get equity positions where qty ≥ 100 AND symbol in allowlist.
2. For each, for each chain whose expiration is in [today+14, today+30]:
   a. Get calls whose strike ≥ max(current_price * 1.01, position.avg_buy_price)
      (covers OTM bias AND no forced-loss assignment)
   b. Filter to delta ∈ [0.25, 0.35]
   c. Pick highest-bid (premium income)
3. contracts = floor(qty / 100). One call per 100 shares.
```

## Exit rules

| Trigger | Action | Reason |
|---|---|---|
| `pct_of_max_profit >= 0.50` | Buy-to-close | `50pct_max_profit` |
| `days_to_expiry <= 5` | Buy-to-close | `21_dte_management` |
| Underlying within 1 strike of short strike | Buy-to-close | `assignment_imminent` |
| Underlying assignment received (if held to expiry) | Strategist disables for this symbol for 30 days | (cooldown after assignment) |

## Executor rejection paths (important)

| Scenario | Executor's behavior |
|---|---|
| Loaded from `autotrader` profile | Abort tick: `aborted: profile_compatibility_failed` |
| Account `option_level == "" or option_level_0` | Abort tick: `aborted: capability_gated` |
| Loaded from Claude Code | All intents land `status: reviewed`; never placed |
| Loaded from future `options-trader` profile (cron + live) | Place after review + Greeks/collateral validation |

## Anti-rules

| Refused | Reason |
|---|---|
| Run from `autotrader` profile | Hard rule. |
| Naked calls (no underlying long) | Risk profile incompatible with cash account. |
| CSPs whose collateral > 25% of buying power | Cap. |
| CCs at strikes below cost basis | Prevents forced-loss assignment. |
| Multi-leg structures | MCP doesn't support; would have to use Robinhood app. |
| Long calls/puts (directional bets) | Out of v1 scope. |

## State file shape

`<profile>/state/options-strategist.json` (where `<profile>` is the running profile, e.g. `options-trader` if/when it exists, NOT `autotrader`):

```json
{
  "open_shorts": [
    {
      "symbol": "AAPL",
      "right": "put",
      "strike": 185.00,
      "expiration": "2026-07-31",
      "qty_contracts": 1,
      "entry_credit": 2.85,
      "opened_at": "2026-06-26T14:00:00-04:00",
      "option_id": "..."
    }
  ],
  "assigned_cooldown": {
    "MSFT": "2026-07-26"
  }
}
```
