---
name: house-policy
description: >
  The committed investing parameters — scope, authority, position-cap hierarchy, risk gates,
  factor targets, and the amendment procedure. Use before any sizing, rebalancing, or
  risk-limit decision, and whenever a strategist or Archon proposes an action. This file
  holds decided values, not ranges or advice; where it is silent, no policy exists yet and
  the answer is "unstated", never an improvised default.
metadata:
  author: nirav
  version: "2.0.0"
  policy_version: "investing-house-policy/2.0"
  authored: 2026-07-27
compatibility: Designed for Claude Code
allowed-tools: Read
---

# House Policy — Investing v2.0

Committed parameters for the paper book. Every line is either **[policy]** — a binding
requirement for compliant paper-book behavior — or **[agent]** — guidance honored by judgment.
Neither label claims machine enforcement. The current `_shared/executor` is an LLM-executed
broker-routing skill, not deterministic policy-as-code, and it does not implement the
book-level limits below. Until a paper-book gate enforces them, automated actions must not be
described as policy-compliant merely because this skill was loaded.

## 1. Scope

- Governs the **Archon $1M paper book only**. Real accounts are outside this document's
  binding scope as of v2.0. **[agent]**
- Claude Code is **analyst-only**; live placement never originates here, in any mode. **[policy]**
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

Thesis-book entries (§3) are decided by **Nirav alone**: Archon and strategists may analyze
or draft the thesis note, but the entry intent is authored and signed by Nirav — no other
actor may originate it. **[policy]**

## 3. Position-cap hierarchy

Two layers bind simultaneously; the **tighter always wins**. A downstream layer may be
stricter than this policy, never looser. **[policy]**

```
effective_cap = min( book_max_position_pct ,
                     sleeve_share × per_position_max_pct )
```

- `book_max_position_pct` = **15%** of total book **[policy]**
- `max_concurrent_positions` (book) = **8** **[policy]**
- `max_gross_exposure` = **100%** of book value — **no leverage**; cash is the residual with no
  minimum. Position caps alone permit 8 × 15% = 120%, so this constraint is what actually
  bounds total risk. **[policy]**
- Default stop-loss = **−5%** from entry unless the intent states a thesis-invalidation level **[agent]**

### Sleeve allocation

| Sleeve | Class | Share | Per-position max | Effective cap |
|---|---|---:|---:|---:|
| dca-investor | **core** | 45% | 50% | **15.0%** (book cap binds) |
| rebalancer | **core** | 25% | 70% | **15.0%** (book cap binds) |
| thesis-book | **thesis** | 15% | 33⅓% | **5.0%** |
| swing-trader | **tactical** | 5% | 25% | **1.25%** |
| macro-overlay-trader | **tactical** | 5% | 70% | **3.5%** |
| options-strategist | **tactical** | 5% | 25% | **1.25%** |
| day-trader · earnings-event-trader · reflexivity-trader | — | **0%** | — | **0** (kill-listed) |

**Core** sleeves run systematic processes — scheduled contribution and drift correction back to
committed targets. **Tactical** sleeves open short-horizon discretionary positions on a view.
**Thesis** sleeves hold long-horizon conviction positions against a written thesis note (below).
The class distinction is load-bearing in §6. A discretionary-on-a-view entry may never route
through a core sleeve to obtain size; if no non-core sleeve can host it at workable size, the
answer is "no position", not reclassification. **[policy]**

Kill-listed strategists have sleeve 0 and `do_not_promote: true`; both conditions are
AND-gated at the executor. **[policy]**

### Thesis-book sleeve

The thesis-book sleeve exists because conviction positions are neither systematic (core) nor
short-horizon (tactical). It is funded by reducing core shares (dca-investor 55→45%,
rebalancer 30→25%); total sleeve shares still sum to 100%.

- **Max 3 concurrent thesis positions** (they also count toward the book's
  `max_concurrent_positions` = 8). **[policy]**
- Every entry requires a **written thesis note filed before the intent**, containing: the
  market-implied expectation being disputed, at least one **pre-registered falsifier** that
  would force exit, a catalyst or review window, and a review date. No note → no entry. **[policy]**
- A fired falsifier forces exit or an explicit written amendment of the thesis — silence is
  not an option. **[policy]**
- Stop-loss default in §3 does not apply; the falsifier **is** the thesis position's
  invalidation level, and it must be stated in the note. **[policy]**
- No strategist runs this sleeve; entries are Nirav-signed (§2). **[policy]**

## 4. Sizing basis

Conviction tiers persist, but **size is gated on edge, not confidence**. **[agent]**

Tier size is a **fraction of the §3 effective cap for the sleeve the position lives in** —
never a fraction of the book directly, and never a fraction of a fraction. This supersedes the
v1.1 table, which read two ways an order of magnitude apart ("7.5%" of book vs. of
sleeve-adjusted cap); neither ambiguous reading survives. **[policy]**

| Tier | Size | Requires |
|---|---:|---|
| HIGH | 100% of the sleeve's effective cap | stated probability **vs. a named reference** + payoff asymmetry |
| MEDIUM | 50% of the sleeve's effective cap | reference requirement per sleeve-class scope below |
| LOW | 0% | monitor only |

**Worked example.** A MEDIUM swing-trader position: effective cap 1.25% of book (§3), so size
= 50% × 1.25% = **0.625% of book**. A MEDIUM thesis-book position: effective cap 5.0%, so size
= **2.5% of book**. A HIGH dca-investor allocation may use the full 15% book cap. The tier
never overrides the cap hierarchy — §3's tighter-wins rule already bound before the tier
applied.

### Reference-probability rule — scope

**No stated edge versus a reference → no size** applies to **tactical sleeves as written**:
a tactical recommendation that cannot name its reference probability is LOW by definition.
Confidence alone never establishes attractiveness: a 90% event can be fully priced, a 35%
event can be attractive. **[policy]**

The rule's intent is to force the question "what does the market already believe?" — not to
zero every honest long-horizon view. Scope by sleeve class:

- **Core** — not applicable; systematic entries carry no per-position view.
- **Tactical** — applies in full. HIGH and MEDIUM both require a named reference probability;
  the tiers differ by strength of edge.
- **Thesis** — HIGH requires a named reference probability plus payoff asymmetry, same as
  tactical. **MEDIUM is available without a point probability** when the §3 thesis note is
  complete: it must still name the market-implied expectation it disputes (a qualitative
  reference), a pre-registered falsifier, and a review date. An incomplete note is LOW. Honest
  "I cannot name a point probability" therefore caps a thesis position at MEDIUM (2.5% of
  book); it no longer zeroes it. **[policy]**

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

Measured peak-to-trough on book equity. **[policy]**

| State | Threshold | Behavior |
|---|---|---|
| Normal | ≥ −10% | unrestricted |
| **Restricted** | < −10% | no new **tactical or thesis** positions and no adds to existing ones (§3 class column: thesis-book, swing-trader, macro-overlay-trader, options-strategist); **core sleeves continue** — scheduled contribution and drift correction are not new risk-taking; **policy may not be loosened**. Thesis exits on a fired falsifier remain mandatory — the gate blocks entries, never exits |
| **Halt** | < −20% | no new positions of any kind; written review required to exit |

## 7. Negative constraints

Not authorized under v2.0, regardless of apparent opportunity: **[policy]**

- live placement from Claude Code, in any mode
- options intents outside an `options-trader` profile (which does not exist)
- any position from a kill-listed strategist
- any intent the executor did not receive from a strategist — except thesis-book intents,
  which it accepts **only** when Nirav-signed per §2
- any thesis-book entry without a filed thesis note, or any discretionary entry routed
  through a core sleeve

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

Quarterly review against: book drawdown state, factor drift, gross exposure, and cap breaches.
Until a deterministic paper-book gate exists, any breach is an enforcement gap to close, not
evidence that the policy parameter should be loosened.

## Change log

| Date | Version | Change | Direction | Rationale |
|---|---|---|---|---|
| 2026-07-27 | 1.0.0 | Initial authorship | — | Track A found policy scattered across five conflicting layers; this consolidates and supplies the six missing committed values |
| 2026-07-27 | 1.0.1 | Defined **core** vs **tactical** sleeve classes in §3; §6 Restricted now names which sleeves halt and states that core sleeves continue | clarifying (PATCH) | "tactical" appeared once in §6 and was never defined — a reader could have frozen routine rebalancing during a drawdown, which the gate never intended. Same-day pre-merge correction; treated as completing authorship, not an amendment |
| 2026-07-27 | 1.1.0 | §3 adds `max_gross_exposure` 100%, no leverage. §5 rewritten: tilt envelope is **±10 percentage points** (the "double/halve" language removed as a mis-description of the source's own examples), tilts must fund each other, active target defined, rebalance trigger clipped by the envelope | tightening + clarifying (MINOR) | Three defects found in a self-audit: caps alone permitted 120% gross; the tilt rule carried three incompatible bounds at once; "intended exposure" was undefined under an active tilt. The envelope-clips-band rule resolves an interaction the two fixes would otherwise have created (a tilted band reaching 43.75% past a 35% ceiling) |
| 2026-07-28 | 1.1.1 | Replaced the misleading `[executor]` label with `[policy]`, documented the current enforcement gap, aligned visible version text, and removed the unavailable predictions-factory dependency | clarifying (PATCH) | Registry dependency edges and LLM instructions are not deterministic enforcement. The policy must distinguish committed requirements from implemented controls. |
| 2026-08-10 | 2.0.0 | **PROPOSED — pending Nirav sign-off (merge = sign-off).** §3 adds a **thesis** sleeve class and `thesis-book` sleeve (15% share funded from core: dca 55→45%, rebalancer 30→25%; per-position ⅓ of sleeve → 5.0% effective cap; max 3 concurrent; thesis-note + falsifier required). §4 rewritten: tier = fraction of the sleeve's effective cap (HIGH 100%, MEDIUM 50%), one worked example, and the reference-probability rule scoped by sleeve class — tactical unchanged, thesis MEDIUM available on a complete note without a point probability. §6 Restricted now also blocks new thesis entries. §7 extended | loosening + clarifying (MAJOR) | Orchestration rep 4 (vault `skill-lab/`, 2026-08-11 record): three independent draft overlays all routed through core sleeves because the tactical path sized a committed view to ~0.09% of book — economically meaningless — and the structural gate correctly rejected every one. The policy could not host the position class it was written to govern. This is a structural gap, not "a compelling single idea exceeding a cap": no specific position motivates the numbers. **Cooling-off: the loosening component (new sleeve) takes effect 7 days after sign-off; sign-off itself requires the book not in §6 Restricted/Halt and no stop-out within 30 days. The §4/§6 clarifications and tightenings are effective at sign-off.** |

## Connections

- `_shared/executor` — current broker-routing skill; it does **not** yet enforce the paper-book
  limits in §3 or §6 and is outside this policy's binding real-account scope
- `archon/references/portfolio-rules.md` — runtime profile; must not contradict §3
- Named references in §4 are recorded at decision time; no prediction runtime is required
- Track A inventory and Track B (IPS canon + policy-as-code) in vault `skill-lab/`
