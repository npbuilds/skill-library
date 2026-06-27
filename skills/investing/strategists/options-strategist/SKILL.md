---
name: options-strategist
type: strategist
description: >
  Single-leg options strategist focused on income generation — cash-secured puts
  (CSP) on quality names you'd be happy to own, and covered calls (CC) against
  existing positions. EXPLICITLY ISOLATED from the autotrader profile (equity-only
  per SOUL); runs only as a Claude Code analyst or in a future dedicated
  options-trader profile with its own SOUL. Capability-gated to option_level_2+.
  Use when user asks "CSP setup on X", "covered call ideas", or "options income".
  Default review-only.
metadata:
  author: nirav
  version: "0.1"
compatibility: Hermes Agent + Claude Code
allowed-tools: Read Skill Bash
strategist:
  mode: review
  asset_class: option-l2
  account_lock: null
  time_window: "10:00-15:55 America/New_York"
  cron_hint: "0 14 * * 5"
  allowlist: [AAPL, MSFT, GOOGL, NVDA, META, AMZN, AVGO, SPY, QQQ]
  max_position_pct: 25
  max_concurrent_positions: 4
  capability_requires: [option_level_2]
  profile_compatibility: [analyst-only, options-trader]
  requires_directors: [risk-architecture, value-quality]
target_dte:
  csp_min: 21
  csp_max: 45
  cc_min: 14
  cc_max: 30
target_delta:
  csp_short: 0.30
  cc_short: 0.30
---

# Options Strategist (Isolated)

A single-leg options strategist that produces income via short premium on quality names. NOT loadable by the `autotrader` profile — its SOUL is equity-only and any attempt to invoke this skill from autotrader will abort in the executor with `aborted: "profile_compatibility_failed"`.

**Where this skill runs:**
- ✅ Claude Code (`analyst-only`) — for research, paper trading, and contract selection. Never places.
- ✅ A future dedicated `options-trader` Hermes profile (to be built) with its own L2-permissive SOUL and a non-Agentic account.
- ❌ The `autotrader` profile. Hard-rejected by the executor.

> Required: `_shared/intent-schema.md` §"option_leg field" and `_shared/circuit-breakers.md`. The MCP supports **single-leg only** — no spreads, condors, butterflies.

## Strategy summary

- **Two setups:** cash-secured puts (CSP) and covered calls (CC). Long calls/puts are explicitly out of v1 scope.
- **Universe:** 9 mega-cap quality names with deep options markets.
- **CSP target:** sell put, target delta ~0.30, 21-45 DTE, on names you'd happily own at the strike.
- **CC target:** sell call against an EXISTING long stock position, target delta ~0.30, 14-30 DTE.
- **Exit:** buy-to-close at 50% of max profit OR within 5 DTE OR if strike is breached (assignment near-certain).
- **Cadence:** weekly Friday afternoon (income-generation discipline).
- **Sizing:** at most 25% of buying power per position. CSP requires full cash collateral.

## 6-phase protocol

### Phase 1 — Pre-flight

The executor's pre-flight will:
1. Reject if current profile is not in `profile_compatibility` → `aborted: profile_compatibility_failed`. Today this always rejects from autotrader.
2. Reject if `account.option_level not in {"option_level_2", "option_level_3"}` → `aborted: capability_gated`.
3. Standard account-lock, portfolio, time-window, circuit-breaker checks.

When `account_lock` is `null` (this skill's frontmatter), the executor uses whichever account is the loaded profile's default — i.e., it does NOT pin to 619508153. Future `options-trader` profile will set its own account number.

### Phase 2 — Compose context

`risk-architecture` with: *"What's the current vol regime — high/low IV, term structure? One line."* (High IV = more income; low IV = less attractive premium.)

`value-quality` with: *"Of [allowlist], which 2-3 names are highest quality at current prices?"* (Used to filter CSP candidates — only sell puts on names you'd own.)

### Phase 3 — Signal gather

For each allowlist symbol:
- `get_equity_quotes([symbol])` — current price.
- `get_option_chains(underlying_symbol=symbol)` — chain UUIDs and expiration dates.
- For matching expirations (within target DTE windows), `get_option_instruments(chain_id=..., expiration_dates=..., type="put" or "call")` — strikes.
- For candidate strikes (around target delta), `get_option_quotes(instrument_ids=[...])` — premium and Greeks.

Also `get_equity_positions(account_number=<resolved>)` to find covered-call candidates (symbols held with qty ≥ 100).

### Phase 4 — Decide

**CSP candidates:**
```
for symbol in allowlist:
    if symbol not in value-quality.top_picks: skip (only sell puts on names you'd own)
    for chain whose expiration is target_dte.csp_min ≤ DTE ≤ csp_max:
        candidate strikes = puts whose delta in [-target_delta.csp_short - 0.05, -target_delta.csp_short + 0.05]
        pick the one with highest premium / collateral ratio
        collateral_required = strike * 100
        if collateral_required > buying_power * max_position_pct/100: skip
        emit intent: sell-to-open put, asset_class: option-l2
```

**CC candidates:**
```
for pos in positions where qty ≥ 100:
    if pos.symbol not in allowlist: skip
    for chain whose expiration is target_dte.cc_min ≤ DTE ≤ cc_max:
        candidate strikes = calls whose strike > current_price AND delta in [target_delta.cc_short ± 0.05]
        pick highest premium with strike ≥ pos.avg_buy_price (prevent forced-loss assignment)
        contracts = floor(pos.qty / 100)
        emit intent: sell-to-open call, asset_class: option-l2
```

**Exits** (existing short positions):
```
for short_pos in open_options_short:
    bid_to_close = quote.bid_price
    pct_of_max_profit = (entry_credit - bid_to_close) / entry_credit
    days_to_expiry = expiration - today
    if pct_of_max_profit >= 0.50: emit buy-to-close intent; reason: "50pct_max_profit"
    elif days_to_expiry <= 5: emit buy-to-close intent; reason: "21_dte_management"
    elif current_underlying in danger zone (within 1 strike of short): emit buy-to-close; reason: "assignment_imminent"
```

### Phase 5 — Hand off to executor

The executor enforces the options-from-wrong-profile rejection. When running from Claude Code, the executor will never place (analyst-only).

### Phase 6 — Emit & persist

State file format mirrors equity strategists, with `option_id`, `expiration`, `strike`, `right`, `credit`, etc.

## Intent shape (option-l2)

```json
{
  "symbol": "AAPL",
  "side": "sell",
  "asset_class": "option-l2",
  "option_leg": {
    "option_id": "<UUID from get_option_instruments>",
    "position_effect": "open",
    "ratio_quantity": 1
  },
  "quantity_type": "shares",
  "qty": 1,
  "order_type": "limit",
  "limit_price": 2.85,
  "intent_price": 2.85,
  "max_slippage_pct": 5.0,
  "time_in_force": "gfd",
  "reason": "CSP AAPL 185P 35DTE Δ-0.30; premium $285 on $18500 collateral (1.5%)"
}
```

Notes:
- `qty` in `option_leg` context = contract count (each contract = 100 shares of underlying).
- `quantity_type: "shares"` is the only valid value for options (notional doesn't apply).
- `max_slippage_pct` is much higher (5%) because options spreads are wider than equities.

## Interactive mode

- "CSP setup on AAPL?" — run phases 2-4 for AAPL only; report candidates.
- "Should I sell a covered call on my NVDA?" — check if held ≥ 100 shares; if yes, find candidates; if no, explain.
- "What options positions do I have?" — return state file contents + `get_option_positions`.

## What this strategist will never do

- Trade in the `autotrader` profile. Executor enforces.
- Sell naked calls. CC requires the underlying long.
- Sell options below your CSP cash-collateral capacity.
- Sell options below your cost basis (forced-loss assignment).
- Trade multi-leg strategies. MCP doesn't support them.
- Trade options on tickers outside the allowlist.
