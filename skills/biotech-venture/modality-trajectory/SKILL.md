---
name: modality-trajectory
description: >
  Direct historical MOA-arc placement, modality-lifecycle assessment, human-genetics target
  validation, and discovery-stage conviction scoring to the appropriate specialist skill. Activate
  when the question is "where will this go?" — given an emerging target×modality, place it on the
  trajectory past mechanism classes followed, find its nearest validated analog, grade how validated
  the target is, and produce an early conviction score. This director is the analog engine: it turns
  a frontier candidate into a placed, graded, scored thesis that hands off to PoS/rNPV once a
  clinical asset exists.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Modality Trajectory Director

A new target×modality is not a blank slate — it is a point on a curve that twelve prior mechanism classes have already traced. Drug classes obey a stable life-cycle (target ID → tool/platform → first-in-human → first approval → class explosion → maturity) with a ~18–30 year clock to first approval and a compressed 2–5 year explosion once one hard-endpoint pivotal readout lands in a genetically- or biomarker-defined population. This director routes the "where will this go, and will it work?" question to specialists that place a candidate on that arc, find its nearest validated analog, grade its human-genetics validation rung, and decompose an early conviction score. It is the analog engine that consumes the radar's (`frontier-intelligence`) watchlist and hands a scored thesis to Asclepius's diligence pillars.

## Child Skills

| Skill | Type | When to Use |
|-------|------|-------------|
| modality-lifecycle | knowledge | Assessing where a modality sits on its own maturity curve, its delivery bottleneck, and what unlocks the next stage — supplies the P(modality deliverable) term |
| moa-analog-engine | knowledge | Placing a target×modality on the historical MOA arc, finding the nearest validated analog, and naming the still-pending ignition trial to watch — the core placement skill |
| target-validation-ladder | knowledge | Grading how validated a target is on the human-genetics evidence ladder (causality + direction-of-effect), earlier-stage than mechanism-risk-adjuster — supplies the P(biology holds) term |
| frontier-conviction-scorer | knowledge | Decomposing a discovery-stage conviction score (biology × modality × arc-position × timing) anchored to empirical base rates, with explicit handoff to rNPV/PoS once a clinical asset exists |

## Routing Logic

| Question Signal | Route To | Examples |
|-----------------|----------|----------|
| Is this modality ready, delivery problem, where is the modality on its curve, what unlocks it | modality-lifecycle | "Is in-vivo CAR ready, or still a delivery problem?" |
| What's the analog, where on the arc, how long until it matters, what trial to watch, has this pattern happened before | moa-analog-engine | "What's the historical analog for oral PCSK9, and where on the arc is it?" |
| How validated is the target, genetic support, is this causal, will the biology hold | target-validation-ladder | "Grade the human-genetics validation for TREM2 in Alzheimer's" |
| What's my conviction, early PoS, is this worth a position, score this candidate | frontier-conviction-scorer | "Give me a discovery-stage conviction score for amylin agonism in obesity" |
| Modality readiness + arc placement | modality-lifecycle then moa-analog-engine | "Is this modality ready and where does the class sit?" |
| Full trajectory thesis | All four, ending in frontier-conviction-scorer | "Place, grade, and score this candidate" |

## Multi-Skill Questions

1. **Where on the arc, and how far will it travel?**: "Where is this class, and what happens next?"
   - Load moa-analog-engine to find the nearest validated analog, place arc-position, and name the ignition trial to watch
   - Load modality-lifecycle to check whether the modality itself is deliverable or still gated by a delivery bottleneck
   - Synthesize: a target on a proven arc with an undeliverable modality stalls until the platform fix arrives (siRNA pre-GalNAc); the ignition trial is the event to watch

2. **Will the biology hold?**: "Is this target real?"
   - Load target-validation-ladder to grade the human-genetics evidence (causality, direction-of-effect, constraint, pleiotropy-as-safety)
   - Load moa-analog-engine to check whether the validation pattern matches a genetics-first analog (PCSK9) vs a modality-unlock analog (KRAS)
   - Synthesize: genetic support with direction-of-effect concordance is the single strongest pre-clinical predictor (~2.6× relative success); a confounded non-coding hit is not

3. **Score it**: "What's my conviction?"
   - Load target-validation-ladder for P(biology holds), modality-lifecycle for P(modality deliverable), moa-analog-engine for arc-position and competitive timing
   - Load frontier-conviction-scorer to decompose the score against empirical base rates and emit the rNPV handoff trigger
   - Synthesize: the score is qualitative and discovery-stage; it hands off to phase-weighted rNPV the moment a clinical asset and indication exist — it never replaces diligence math

## Curriculum Order

1. **modality-lifecycle** — Foundation. Learn the maturity map and that delivery, not biology, is usually the binding constraint; that modalities can regress; and that an enabling-platform fix converts a stalled class. This is the P(modality deliverable) term.
2. **moa-analog-engine** — Second, and central. Learn the five-phase arc, the 18–30 year time constant, the three sub-patterns (undruggable-cracking, indication-creep, resistance-ladder), and the ignition-event doctrine. This is how a candidate gets placed and its nearest analog found.
3. **target-validation-ladder** — Third. Learn the human-genetics evidence ladder and why causality + direction-of-effect are load-bearing. This is the P(biology holds) term and the most rigorous gate.
4. **frontier-conviction-scorer** — Last. The synthesizer. With modality readiness, arc-position, and target validation in hand, learn to decompose a base-rate-anchored conviction score and to recognize the handoff point to formal PoS/rNPV.

## Conflict Resolution

| Conflict | Resolution | Reason |
|----------|------------|--------|
| target-validation-ladder grades the biology strong but modality-lifecycle says the modality cannot yet reach the target | Conviction is gated by the weaker term; flag as "right target, wrong era — watch for the delivery unlock" | A validated target with an undeliverable modality is a waiting game, not a current bet (siRNA before GalNAc; extrahepatic oligo today) |
| moa-analog-engine places the candidate early on a proven arc but frontier-conviction-scorer's base rates look punishing | Arc-position and analog inform *direction*; base rates anchor *magnitude* — report both, do not let optimism override the base rate | The base rate is the prior; the analog adjusts it. De novo optimism is the most common error in early conviction |
| A marquee clinical failure just occurred in the class | Do not auto-kill; check whether a modality re-engineering follows | Anti-amyloid, ADCs, and siRNA all exploded *after* marquee failures once the modality was re-engineered — failure + re-engineering is a BUY signal |
| target-validation-ladder and mechanism-risk-adjuster disagree | target-validation-ladder governs discovery-stage; mechanism-risk-adjuster governs PoS-stage; hand forward, do not double-count | They are sequential stages of the same evidence, not competing estimates |

## Scope Boundaries

**This director handles**: all questions about placing a target×modality on the historical MOA arc, finding validated analogs, assessing modality maturity and delivery readiness, grading human-genetics target validation, and producing discovery-stage conviction scores.

**Route to Asclepius when**:
- A clinical asset and indication exist and the question is formal PoS (route to `probability-of-success/pos-calculator`) or valuation (route to `asset-valuation/rnpv-modeler`)
- The mechanism needs PoS-stage risk adjustment rather than discovery-stage validation (route to `probability-of-success/mechanism-risk-adjuster`)
- The question is which emerging targets to scout in the first place (route to `frontier-intelligence`)
- The question is manufacturing feasibility/COGS for a specific program rather than modality-class readiness (route to `manufacturing-ip`)

## Cross-Domain Connections

- **Biotech-venture/frontier-intelligence**: the radar that feeds this engine — ranked candidates flow in from emerging-target-radar
- **Biotech-venture/probability-of-success (pos-base-rates, pos-calculator, mechanism-risk-adjuster)**: the diligence-stage successors; frontier-conviction-scorer anchors to pos-base-rates and hands off to pos-calculator; target-validation-ladder hands off to mechanism-risk-adjuster
- **Biotech-venture/asset-valuation/rnpv-modeler**: the conviction score becomes an rNPV input once a clinical asset and indication exist
- **Biotech-venture/manufacturing-ip/modality-manufacturing**: modality-lifecycle's delivery-readiness view complements modality-specific manufacturing/COGS analysis
- **Research/spelunker**: deep verification of a historical arc, an analog claim, or a target's genetic support
- **Probability-of-success base rates**: the empirical anchor that keeps conviction scores honest against de novo optimism
- **Dual use**: serves a clinical-scientist learning how mechanism classes mature *and* an investor sizing early conviction before a clinical readout prices it in
