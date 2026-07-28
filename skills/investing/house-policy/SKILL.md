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
  version: "1.1.0"
  policy_version: "investing-house-policy/1.1"
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
- `max_gross_exposure` = **100%** of book value — **no leverage**; cash is the residual with no
  minimum. Position caps alone permit 8 × 15% = 120%, so this constraint is what actually
  bounds total risk. **[executor]**
- Default stop-loss = **−5%** from entry unless the intent states a thesis-invalidation level **[agent]**

### Sleeve allocation

| Sleeve | Class | Share | Strategist max | Effective cap |
|---|---|---:|---:|---:|
| dca-investor | **core** | 55% | 50% | **15.0%** (book cap binds) |
| rebalancer | **core** | 30% | 70% | **15.0%** (book cap binds) |
| swing-trader | **tactical** | 5% | 25% | **1.25%** |
| macro-overlay-trader | **tactical** | 5% | 70% | **3.5%** |
| options-strategist | **tactical** | 5% | 25% | **1.25%** |
| day-trader · earnings-event-trader · reflexivity-trader | — | **0%** | — | **0** (kill-listed) |

**Core** sleeves run systematic processes — scheduled contribution and drift correction back to
committed targets. **Tactical** sleeves open discretionary positions on a view. The distinction
is load-bearing in §6.

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

### Tilt envelope

Regime tilts move a factor by at most **±10 percentage points** from baseline. A factor is
**never** permitted outside this envelope, whatever any drift band would otherwise allow:

| Factor | Baseline | Permitted range |
|---|---:|---|
| Value | 25% | 15–35% |
| Momentum | 20% | 10–30% |
| Quality | 25% | 15–35% |
| Low Vol | 15% | 5–25% |
| Broad Market | 15% | 5–25% |

- Tilts must **fund each other** — weights sum to 100% at all times; a tilt up requires an
  offsetting tilt down.
- Unclear regime signal → revert to baseline.
- Tilts persist until reverted deliberately or by the unclear-signal rule; they do not expire.

### Rebalancing

The **active target** is the current tilted weight (baseline if untilted). Rebalancing restores
the active target — it does not silently undo a tilt.

Trigger fires on whichever comes first:

1. **25% relative drift** from the active target — e.g. untilted Value (25%) outside 18.75–31.25%;
   Value tilted to 35% outside 26.25–43.75%; **or**
2. **exit from the tilt envelope** above.

Rule 2 clips rule 1: a factor tilted to its 35% ceiling has an effective band of 26.25–35%,
because the envelope binds tighter than the drift band on the upside.

Cadence: **quarterly** check; trigger fires only on breach.

## 6. Drawdown gates

Measured peak-to-trough on book equity. **[executor]**

| State | Threshold | Behavior |
|---|---|---|
| Normal | ≥ −10% | unrestricted |
| **Restricted** | < −10% | no new **tactical** positions (§3 class column: swing-trader, macro-overlay-trader, options-strategist); **core sleeves continue** — scheduled contribution and drift correction are not new risk-taking; **policy may not be loosened** |
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
| 2026-07-27 | 1.0.1 | Defined **core** vs **tactical** sleeve classes in §3; §6 Restricted now names which sleeves halt and states that core sleeves continue | clarifying (PATCH) | "tactical" appeared once in §6 and was never defined — a reader could have frozen routine rebalancing during a drawdown, which the gate never intended. Same-day pre-merge correction; treated as completing authorship, not an amendment |
| 2026-07-27 | 1.1.0 | §3 adds `max_gross_exposure` 100%, no leverage. §5 rewritten: tilt envelope is **±10 percentage points** (the "double/halve" language removed as a mis-description of the source's own examples), tilts must fund each other, active target defined, rebalance trigger clipped by the envelope | tightening + clarifying (MINOR) | Three defects found in a self-audit: caps alone permitted 120% gross; the tilt rule carried three incompatible bounds at once; "intended exposure" was undefined under an active tilt. The envelope-clips-band rule resolves an interaction the two fixes would otherwise have created (a tilted band reaching 43.75% past a 35% ceiling) |

## Connections

- `_shared/executor` — the only deterministic gate; enforces §3, §6, §7
- `archon/references/portfolio-rules.md` — runtime profile; must not contradict §3
- `predictions-factory` — supplies the reference probabilities §4 requires
- Track A inventory and Track B (IPS canon + policy-as-code) in vault `skill-lab/`
