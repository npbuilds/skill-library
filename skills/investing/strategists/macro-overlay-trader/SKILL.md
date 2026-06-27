---
name: macro-overlay-trader
type: strategist
description: >
  Dalio-quadrant macro overlay. Asks regime-intelligence which growth×inflation
  quadrant we're in and rotates a small SPY/TLT/IEF/GLD basket to the
  corresponding target weights. Monthly cadence, plus off-cadence on regime
  shift. Composes both regime-intelligence and asset-universe. Use when user
  asks "what regime are we in for positioning", "macro overlay view", or "how
  should I tilt the book". Default review-only.
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash
strategist:
  mode: review
  asset_class: equity
  account_lock: "619508153"
  time_window: "10:00-15:55 America/New_York"
  cron_hint: "0 15 1 * *"
  allowlist: [SPY, TLT, IEF, GLD]
  max_position_pct: 70
  max_concurrent_positions: 4
  capability_requires: []
  assumes:
    fractional_shares: true   # cash individual accounts on Robinhood; not a capability the broker reports
  profile_compatibility: [autotrader]
  requires_directors: [regime-intelligence, asset-universe]
quadrant_targets:
  q1_growth_up_inflation_up:    {SPY: 0.50, GLD: 0.30, TLT: 0.00, IEF: 0.20}
  q2_growth_up_inflation_down:  {SPY: 0.60, GLD: 0.00, TLT: 0.30, IEF: 0.10}
  q3_growth_down_inflation_up:  {SPY: 0.20, GLD: 0.50, TLT: 0.00, IEF: 0.30}
  q4_growth_down_inflation_down: {SPY: 0.30, GLD: 0.10, TLT: 0.50, IEF: 0.10}
drift_thresholds:
  normal: 0.05
  panic: 0.15
per_tick_clamp_pct: 0.15
---

# Macro Overlay Trader

A regime-aware target-weight strategist. Same mechanism as `rebalancer`, different target. The targets come from the current Dalio quadrant (growth direction × inflation direction), which the `regime-intelligence` director returns. When the quadrant flips, the strategist rotates — but uses the `per_tick_clamp` to spread the rotation over multiple ticks (avoids whipsaws on regime ambiguity).

> Required: `_shared/intent-schema.md`, `_shared/position-sizing.md` §"Target-weight rebalance". Cross-reference with `rebalancer/SKILL.md` — the protocols are siblings.

## Strategy summary

- **Universe:** SPY (equities), TLT (long bonds), IEF (intermediate bonds), GLD (gold).
- **Quadrants:** four target-weight presets keyed on growth direction and inflation direction.
- **Cadence:** monthly first-trading-day, plus off-cadence ticks when regime director reports a quadrant change.
- **Per-tick clamp:** 15% of account value per tick (slower than `rebalancer` because regime shifts are noisier than drift).
- **Drift threshold:** 5% from quadrant target before trading.

## 6-phase protocol

### Phase 1 — Pre-flight

Strategist-side: read state file. If this month's normal-cadence tick already ran AND the last detected quadrant matches the current one → skip. Otherwise proceed.

### Phase 2 — Compose context (load-bearing)

Invoke `regime-intelligence` with this exact prompt:

> "Classify the current macro regime as a Dalio quadrant. Respond ONLY with a JSON object:
>
> ```json
> {
>   "quadrant": "q1_growth_up_inflation_up | q2_growth_up_inflation_down | q3_growth_down_inflation_up | q4_growth_down_inflation_down",
>   "confidence": <float 0.0-1.0>,
>   "transition_risk": "<string>",
>   "one_line_justification": "<string>"
> }
> ```"

Also invoke `asset-universe` briefly with: *"Are TLT/IEF/GLD behaving as risk-off proxies right now, or is correlation breaking down? One line."*

If `confidence < 0.5`: skip new rebalance trades; treat as if quadrant is unknown. Existing positions stay where they are.

### Phase 3 — Signal gather

- `get_equity_positions(account_number=619508153)` — current shares.
- `get_portfolio(account_number=619508153)` — `total_value`.
- `get_equity_quotes(symbols=allowlist)` — current prices.

Compute `current_weight[s]` per symbol.

### Phase 4 — Decide

Lookup target weights from `quadrant_targets[director.quadrant]`. Apply the same drift-trigger + clamp logic as `rebalancer`:

```
for symbol in allowlist:
    target = quadrant_targets[director.quadrant][symbol]
    delta_pct = target - current_weight[symbol]
    if abs(delta_pct) < drift_thresholds.normal: skip
    delta_usd = delta_pct * total_value
    delta_usd = clamp(delta_usd, -total_value*0.15, +total_value*0.15)
    side = "buy" if delta_usd > 0 else "sell"
    notional = abs(delta_usd)
    emit notional intent with reason: f"Quadrant {director.quadrant}: drift {delta_pct*100:+.1f}% from target {target*100:.0f}%"
```

Sells listed first.

### Phase 5 — Hand off to executor

### Phase 6 — Emit & persist

State file:
```json
{
  "last_normal_cadence_at": "<ISO>",
  "last_quadrant_at": {"quadrant": "q2_growth_up_inflation_down", "first_seen": "<ISO>", "confidence": 0.7},
  "rotation_count": 4
}
```

Quadrant change detection compares `director.quadrant` to `last_quadrant_at.quadrant`. Mismatch → quadrant changed → off-cadence tick allowed.

## Interactive mode

- "What quadrant are we in?" — just phase 2; report director's response.
- "Should I rotate?" — run phases 1-4 in review mode, show what intents would fire.
- "Force rotation to q3" — refuse. Quadrants come from the director, not the user.

## What this strategist will never do

- Decide its own quadrant. Director's word is final.
- Trade above 15% of account in a single tick. Regime shifts get smoothed.
- Hold positions outside the 4-asset universe.
- Run with `confidence < 0.5` from the director (treats regime as unknown — no action).
- Override quadrant targets at runtime.
