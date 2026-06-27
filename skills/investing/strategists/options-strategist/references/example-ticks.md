# Options Strategist — Example Ticks

## Example 1: Loaded from autotrader (hard reject)

**Context:** Misconfiguration — someone loads `options-strategist` from `autotrader` profile.

**Executor pre-flight 1.4 (profile_compatibility):**
```
current_profile = "autotrader"
strategist.profile_compatibility = ["analyst-only", "options-trader"]
"autotrader" not in [...] → abort
```

**tick_decision:**
```json
{
  "tick_utc": "...",
  "strategy": "options-strategist",
  "mode": "review",
  "account_value": 0,
  "buying_power": 0,
  "actions": [],
  "circuit_breaker_tripped": false,
  "aborted": "profile_compatibility_failed",
  "notes": "options-strategist is not loadable in autotrader profile (equities-only per SOUL)"
}
```

No broker call was made. Validates Codex finding 1's fix.

---

## Example 2: Loaded from Claude Code on Agentic account (capability_gated)

**Context:** Claude Code analyst session. The Agentic account `619508153` has `option_level == ""`.

**Executor pre-flight 1.3 (capability_gated):**
```
required: account.option_level in {option_level_2, option_level_3}
got: ""
→ abort
```

**tick_decision:**
```json
{
  "actions": [],
  "aborted": "capability_gated",
  "notes": "Agentic account option_level is empty; options-strategist requires option_level_2+"
}
```

User can target a different account by changing the loaded profile (none exists yet for options).

---

## Example 3: CSP analyst tick on AAPL (Claude Code, no L2 issue assumed)

**Context:** Claude Code analyst session against an L2-enabled paper account (hypothetical). Phase 2 returns vol regime "moderate IV". value-quality picks AAPL and MSFT as top quality.

Phase 3 gets AAPL chains, finds 35-DTE put chain. Strikes near Δ-0.30 are around $182.50 (current price $189). Premium $2.85. Collateral = $18250.

But: $18250 > 25% of buying_power (say buying_power is $50k) → $12500 cap → AAPL fails sizing check at 35 DTE.

Alternative: shorter DTE, lower strike. The strategist iterates within tolerance. Suppose 21 DTE at strike $180 with Δ-0.28 and premium $1.65: collateral $18000, still over.

If buying_power were $100k: $25k cap → AAPL fits. Emit:
```json
{
  "symbol": "AAPL",
  "side": "sell",
  "asset_class": "option-l2",
  "option_leg": {"option_id": "<UUID>", "position_effect": "open", "ratio_quantity": 1},
  "qty": 1,
  "order_type": "limit",
  "limit_price": 2.85,
  "status": "reviewed",
  "reason": "CSP AAPL 182.50P 35DTE Δ-0.30; premium $285 on $18250 collateral (1.56%)"
}
```

Status is `reviewed` because Claude Code never places. The user inspects and may execute manually via Robinhood app.

---

## Example 4: Covered call against held NVDA position

**Context:** Future `options-trader` profile (hypothetical). Account holds 100 NVDA shares at cost basis $80. NVDA at $122.

CC selection: 21-DTE call chain, strike ≥ max($122 * 1.01 = $123.22, $80 cost basis) = $123.22. Δ ~0.30. Pick $130 strike with Δ 0.28, bid $2.40.

```
contracts = floor(100 / 100) = 1
```

```json
{
  "symbol": "NVDA",
  "side": "sell",
  "asset_class": "option-l2",
  "option_leg": {"option_id": "<UUID>", "position_effect": "open"},
  "qty": 1,
  "limit_price": 2.40,
  "status": "placed" (if options-trader cron + live),
  "reason": "CC NVDA 130C 21DTE Δ0.28; premium $240; strike 6.4% above cost"
}
```

---

## Example 5: Exit on 50% max profit

**Context:** Held short put AAPL 185P entry credit $2.85. Current bid $1.40.

```
pct_of_max_profit = (2.85 - 1.40) / 2.85 = 51%
```

Exits at ≥ 50%.

```json
{
  "symbol": "AAPL",
  "side": "buy",
  "asset_class": "option-l2",
  "option_leg": {"option_id": "<same UUID>", "position_effect": "close"},
  "qty": 1,
  "limit_price": 1.45,
  "status": "reviewed",
  "reason": "50pct_max_profit; locked $145 of $285 max"
}
```
