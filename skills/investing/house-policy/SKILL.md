---
name: house-policy
description: >
  The committed investing parameters — scope, authority, position-cap hierarchy, risk gates,
  factor targets, and the amendment procedure. Load before any sizing, rebalancing, or
  risk-limit decision, and whenever a strategist or Archon proposes an action. This file
  holds decided values, not ranges or advice; where it is silent, no policy exists yet and
  the answer is "unstated", never an improvised default.
metadata:
  author: nirav
  version: "1.0.0"
  policy_version: "investing-house-policy/1.0"
  authored: 2026-07-27
compatibility: Designed for Claude Code
allowed-tools: Read
---

# House Policy — Investing v1.0

Committed parameters for the paper book. Every line is either **[executor]** — enforced by a
deterministic gate outside the model — or **[agent]** — honored by judgment and therefore
advisory. LLM-read policy is not enforcement; treat **[agent]** lines as intent that a
sufficiently confused session could violate, and **[executor]** lines as invariants.

## 1. Scope

- Governs the **Archon $1M paper book only**. Real accounts are outside this document's
  binding scope as of v1.0. **[agent]**
- Claude Code is **analyst-only**; live placement never originates here, in any mode. **[executor]**
- Factor targets (§5) describe intended allocation policy; enforcement applies to the paper
  book. Real-account adherence is by intention, not gate. **[agent]**

## 2. Authority

| Actor | May decide | May not |
|---|---|---|
| Nirav | everything; sole amender | — |
| Archon | analysis, routing, recommendations | size above §4; override risk directors |
| Strategists | intents within their sleeve | exceed §3 caps; place from Claude Code |
| `_shared/executor` | reject, downsize, pass through | invent or substitute intents |

Archon never overrides Risk Architecture to chase returns. **[agent]**

## 3. Position-cap hierarchy

Two layers bind simultaneously; the **tighter always wins**. A downstream layer may be
stricter than this policy, never looser. **[executor]**

```
effective_cap = min( book_max_position_pct ,
                     sleeve_share × strategist_max_position_pct )
```

- `book_max_position_pct` = **15%** of total book **[executor]**
- `max_concurrent_positions` (book) = **8** **[executor]**
- Default stop-loss = **−5%** from entry unless the intent states a thesis-invalidation level **[agent]**

### Sleeve allocation

| Sleeve | Share | Strategist max | Effective cap |
|---|---:|---:|---:|
| dca-investor | 55% | 50% | **15.0%** (book cap binds) |
| rebalancer | 30% | 70% | **15.0%** (book cap binds) |
| swing-trader | 5% | 25% | **1.25%** |
| macro-overlay-trader | 5% | 70% | **3.5%** |
| options-strategist | 5% | 25% | **1.25%** |
| day-trader · earnings-event-trader · reflexivity-trader | **0%** | — | **0** (kill-listed) |

Kill-listed strategists have sleeve 0 and `do_not_promote: true`; both conditions are
AND-gated at the executor. **[executor]**

## 4. Sizing basis

Conviction tiers persist, but **size is gated on edge, not confidence**. **[agent]**

| Tier | Size | Requires |
|---|---:|---|
| HIGH | 15% of sleeve-adjusted cap | stated probability **vs. a named reference** + payoff asymmetry |
| MEDIUM | 7.5% | same, weaker edge |
| LOW | 0% | monitor only |

**No stated edge versus a reference → no size.** Confidence alone never establishes
attractiveness: a 90% event can be fully priced, a 35% event can be attractive. Recommendations
that cannot name their reference probability are LOW by definition.

## 5. Factor targets and rebalancing

Committed weights: **Value 25% · Momentum 20% · Quality 25% · Low Vol 15% · Broad Market 15%.** **[agent]**

- Regime tilts: within **±10%** of baseline; maximum tilt doubles a favored factor, minimum
  halves a challenged one; unclear signal → revert to baseline.
- Rebalance trigger: **25% relative drift** from intended exposure (Value outside 18.75–31.25%,
  Momentum outside 15–25%, Low Vol outside 11.25–18.75%).
- Cadence: **quarterly** check; trigger fires only on breach.

## 6. Drawdown gates

Measured peak-to-trough on book equity. **[executor]**

| State | Threshold | Behavior |
|---|---|---|
| Normal | ≥ −10% | unrestricted |
| **Restricted** | < −10% | no new tactical positions; **policy may not be loosened** |
| **Halt** | < −20% | no new positions of any kind; written review required to exit |

## 7. Negative constraints

Not authorized under v1.0, regardless of apparent opportunity: **[executor]**

- live placement from Claude Code, in any mode
- options intents outside an `options-trader` profile (which does not exist)
- any position from a kill-listed strategist
- any intent the executor did not receive from a strategist

## 8. Amendment procedure

Asymmetric by design — pre-commitment binds only when changing the policy is slower than the
impulse to change it. **[agent]**

- **Tightening** takes effect immediately.
- **Loosening** requires written rationale **plus a 7-day cooling-off period**.
- Loosening is **forbidden** while §6 Restricted or Halt is active, and within **30 days of a
  stop-out**.
- Every change records date, rationale, and whether it tightened or loosened. MAJOR version
  bump on any loosening; MINOR on tightening or addition; PATCH on wording.
- No calibration or backtest result may mutate a parameter automatically. Human approval,
  always.

### Reasons that are **not** grounds for amendment

Recent underperformance of a factor · a compelling single idea that exceeds a cap · a
strategist requesting more room · short-horizon market moves.

## 9. Review cadence

Quarterly review against: book drawdown state, factor drift, cap breaches (should be zero —
any breach is an executor bug, not a policy question), and the conversion gap once the
predictions factory reports it.

## Change log

| Date | Version | Change | Direction | Rationale |
|---|---|---|---|---|
| 2026-07-27 | 1.0.0 | Initial authorship | — | Track A found policy scattered across five conflicting layers; this consolidates and supplies the six missing committed values |

## Connections

- `_shared/executor` — the only deterministic gate; enforces §3, §6, §7
- `archon/references/portfolio-rules.md` — runtime profile; must not contradict §3
- `predictions-factory` — supplies the reference probabilities §4 requires
- Track A inventory and Track B (IPS canon + policy-as-code) in vault `skill-lab/`
