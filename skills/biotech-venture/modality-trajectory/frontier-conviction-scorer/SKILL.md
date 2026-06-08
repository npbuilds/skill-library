---
name: frontier-conviction-scorer
description: >
  Score a discovery-stage target × modality candidate before any clinical PoS exists, decomposing
  conviction into P(biology holds) × P(modality deliverable) × position-on-arc × competitive-timing,
  anchored to empirical phase/modality/therapeutic-area base rates rather than management optimism.
  Activate when ranking pre-clinical programs, sizing the binding risk (biology vs platform vs timing),
  benchmarking a frontier asset against its class prior, or deciding what to advance — then hand off
  to rNPV the moment a clinical asset and indication exist.
metadata:
  author: nirav
  version: "1.0"
  parent: modality-trajectory
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Frontier Conviction Scorer — Discovery-Stage Trajectory Conviction, Anchored to Base Rates

Most early-stage biology is scored on narrative. A founder pitches a "bulletproof" target, a novel modality, a paradigm shift — and the listener's prior quietly drifts toward the optimism in the room. This skill exists to refuse that drift. Drug-development success is mostly priced by a small set of observable, discovery-stage features — therapeutic area, modality maturity, human genetic support, biomarker strategy, orphan status — and the base rates for those features have been stable across fifteen years of meta-analyses. The honest answer at discovery is never "model the cash flows"; it is "borrow a base rate and adjust it explicitly."

The core object is a **Trajectory Conviction score = P(biology holds) × P(modality deliverable) × position-on-arc × competitive-timing**, each factor on 0–1, every factor calibrated against an empirical anchor. The decomposition is the value: it localizes *where the binding risk sits* (the target, the platform, the arc position, or the clock) so a reader knows what to diligence next. The number is ordinal and relative — it ranks programs and flags risk; it is not an rNPV and must never be sold as one.

This skill is **dual-use by construction.** A clinical scientist learning the field uses it as a falsification discipline: it forces them to separate "is the target causal?" (biology) from "can this modality reach it?" (platform), and to confront that a genetically bulletproof target delivered by an unproven modality still fails on delivery. An investor screening early opportunities uses the same machinery to triage a deal flow against the class prior, anchor a term sheet to a defensible LOA, and know exactly when to retire the qualitative score for a phase-weighted rNPV. The base rates are the shared backbone of both readings.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Target / gene / pathway | User | Yes |
| Modality (small molecule, mAb, ADC, siRNA, AAV, CAR-T, PROTAC, in vivo CRISPR, etc.) | User | Yes |
| Lead indication / therapeutic area | User | Recommended |
| Development stage (lead-opt, IND-enabling, IND-ready, Phase 1 cleared) | User | Recommended |
| Human genetic support evidence | Open Targets Genetics, GWAS Catalog, gnomAD | Recommended |
| Biomarker / patient-selection strategy | User, ClinicalTrials.gov | Optional |
| Orphan / rare-disease status | User, Drugs@FDA designations | Optional |
| Competitive set & order-of-entry | ClinicalTrials.gov, EDGAR/S-1, patents (PCT/WO) | Optional |

### Steps

#### Step 1 — Fix the Measurement Convention (do this first or every number is wrong)

Before quoting any base rate, decide the unit of analysis and never mix conventions:

- **CDP / program-indication based** (BIO/Informa/QLS) → overall ~7.9% LOA from Phase 1. Use when scoring a *specific target-indication pair*.
- **Molecule based (ME)** (Wong/Lo, DiMasi) → overall ~13.8%. Runs roughly **2x** the CDP rate because one molecule can rescue a failed indication.

A discovery-stage candidate is a program-indication, so **default to CDP** (~7.9% as the general anchor; ~5% for the most recent 2015–2023 novel-modality-heavy window). Pick one and label it in the output. Silent conflation is the most common error in secondary citations.

#### Step 2 — Score P(biology holds) — is the target causal for the disease?

This factor speaks to the *target*, not the platform. Grade it on the human-genetics and validation evidence (hand off the genetic grading to **target-validation-ladder** when a graded rung exists):

- **Human genetic support** is the deepest signal: **2.6x relative success** (Minikel/Nelson, *Nature* 2024; 9,704 programs; refining Nelson 2015's 2.0x). The lift *rises with confidence in the causal gene* and is **independent of effect size, allele frequency, and discovery year** — so grade the *quality of the genetic link, not its magnitude*. A clean coding variant or allelic series scores high; a confounded non-coding GWAS hit does not. Query Open Targets Genetics for L2G causal-gene confidence, gnomAD for constraint (pLI/LOEUF), Consensus/PubMed for replication.
- **Biomarker availability / mechanistic clarity** — a confident causal-gene target *with* a selection biomarker sits near the top of this factor (biomarker selection is itself a ~3x LOA lever, see Step 3).
- **Orthogonal convergence** — human genetics + animal model + tissue/expression + a selective dependency raises the score; a phenotypic-screen hit with no genetic anchor sits low.

Anchor scoring: confident causal gene + biomarker → 0.8–1.0; moderate association, plausible mechanism → 0.4–0.6; phenotypic hit, no genetic anchor → 0.1–0.3.

#### Step 3 — Score P(modality deliverable) — can it reach the target, at dose, safely, manufacturably?

Genetic support de-risks **biology, not platform** — keep them orthogonal. Anchor each modality to its empirical LOA, then haircut for delivery/CMC/regulatory novelty:

| Modality | LOA from P1 (CDP) | Scoring note |
|---|---|---|
| Vaccine | 9.7% | Highest |
| Biologic (mAb-dominated) | 9.1% | Antibody programs ~9%+ |
| Small molecule (NME) | 5.7% | Baseline |
| Cell & gene therapy (all) | 5.3% | **Bimodal — do not use the blended number** |
| — CAR-T | 13.6% | Front-loaded risk; P3→submission 90% |
| — AAV gene therapy | 13.6% | Front-loaded; *can regress* (Elevidys safety wall) |
| — Ex vivo / In vivo gene therapy | 5.9% / 4.4% | |
| ASO / siRNA | No clean LOA | Borrow biologic back-end + delivery haircut |

**The CGT structural insight:** the 5.3% blend hides bimodality. Durable CGT in rare/inherited disease shows Phase 2/3 success of 68–75% and submission→approval 81–90% ("no durable-CGT BLA has failed to eventually gain approval"). Risk is concentrated *early* (delivery, manufacturing, dose-finding). For a CGT program, **weight Phase 1→2 and CMC risk heavily, the back end lightly** — the opposite of a small-molecule oncology asset.

Full credit (0.8–1.0) only if the platform has prior human proof-of-concept. New modality, no clinical history → discount hard (see Step 4). Cross-reference **modality-lifecycle** for whether the delivery unlock has landed.

#### Step 4 — Handle a Zero-Clinical-History Modality (the hardest, most decision-relevant case)

Never start from an optimistic de novo number. The disciplined procedure:

1. **Identify the nearest validated class** and adopt its transition matrix as the prior (novel covalent SM → small-molecule matrix; new viral-vector → AAV 13.6%, front-loaded; novel-conjugate oligo → ASO/biologic blend; engineered cell → CAR-T matrix).
2. **Split risk into biology vs modality.** Genetic/biomarker support credits biology only.
3. **Apply explicit haircuts to the analog's early transitions** for (a) unproven delivery/biodistribution, (b) CMC/manufacturing novelty, (c) regulatory pathway novelty, (d) unknown chronic tolerability. **Concentrate the haircut on Phase 1→2**, where platform risk resolves.
4. **Watch the de-risking inflection:** platform risk collapses the moment *any* asset on the platform clears proof-of-mechanism in humans. Before that, weight platform dominant; after, revert toward the analog matrix.
5. **Down-weight "AI-discovered" novelty** unless the AI acted in molecular *design* with independent wet-lab/clinical validation — AI compresses discovery/preclinical but does **not** yet move Phase 2/3 attrition.

#### Step 5 — Score position-on-arc — the literal base-rate gate

Multiply by cumulative survival to date. This is where the empirical LOA enters as a hard floor:

| Stage | Unconditional P(approval) anchor |
|---|---|
| Lead-opt (no IND) | ~0.4–1% (screening→candidate ~0.1–1%; preclinical stage success ~10.5%; ~1 in 250 cumulative) |
| IND-enabling / IND-ready | ~10% (preclinical gate cleared) |
| Phase 1 cleared | the class P1→approval LOA (e.g., oncology ~5%, hematology ~26%) |

This is why discovery-stage conviction must be *relative* — this program vs. the base rate for its class — not absolute. Cross-reference **moa-analog-engine** for where the candidate sits on the historical five-phase arc.

#### Step 6 — Score competitive-timing — will it matter when it arrives?

Order-of-entry, IP runway, standard-of-care drift, crowding. Query ClinicalTrials.gov and EDGAR/S-1 for the competitive set; patents (PCT/WO, 18-month lag) for undisclosed programs. A 4th-in-class asset entering an area where SoC will have moved gets discounted even if the science scores well. First-in-class to a validated, biomarker-defined population with IP runway scores high.

#### Step 7 — Apply the Therapeutic-Area & Lever Adjustments

Overlay the area base rate and the discovery-knowable levers onto the composite. **Do not naively stack** selection-biased designations onto genetic + biomarker effects (double-counting):

| Lever | Effect | Stacking rule |
|---|---|---|
| Therapeutic area | Hematology ~26% → oncology ~5% (>5x spread); CNS/psychiatry ~7–8% | Sets the base; always apply |
| Human genetic support | 2.6x relative success | Apply to P(biology); grade by causal-gene confidence |
| Biomarker selection | 25.9% vs 8.4% LOA (~3x); P3 76.5% vs 55.0% | Strongest *design* lever; apply once |
| Orphan / rare disease | ~17% LOA; CGT orphan 9.4% vs 3.2% | Apply; partly selection — don't double-count with biomarker |
| Expedited designation (BTD/Fast Track) | Elevated transitions, contaminated by selection | Confirmatory tier-bump only, not a stackable multiplier |

#### Step 8 — Trigger the rNPV Handoff

**The moment a clinical asset and a defined lead indication exist, retire the trajectory score.** Switch to a phase-weighted rNPV (hand off to **asset-valuation/rnpv-modeler** and **probability-of-success/pos-calculator**). The handoff PoS ladder:

| Stage | PoS band |
|---|---|
| Preclinical → Phase 1 | 40–50% |
| Phase 1 → Phase 2 | 50–65% |
| Phase 2 → Phase 3 | 25–35% (the kill zone — diligence hardest here) |
| Phase 3 → NDA/BLA | 50–60% |
| NDA/BLA → Approval | 85–90% |
| Cumulative P1 → approval | 7–12% (oncology ~5–8%; rare ~15–25%) |

Discount at 15–20% for early-stage biotech (10–15% mid-cap, 8–10% large pharma). Adjust each base PoS up/down for the Step 7 levers.

### Output

```
FRONTIER CONVICTION SCORE — [Target] × [Modality] in [Indication]
Date: [assessment date]
Convention: [CDP / ME — labeled]   Stage: [lead-opt / IND-ready / P1 cleared]

TRAJECTORY CONVICTION = P(biology) × P(modality) × position-on-arc × competitive-timing
                      = [0.x] × [0.x] × [0.x] × [0.x] = [composite, ordinal]

Score decomposition:
  P(biology holds):        [0.x]  — [genetic rung; causal-gene confidence; biomarker; orthogonal convergence]
  P(modality deliverable): [0.x]  — [nearest validated class + LOA anchor; delivery unlock landed? Y/N; haircuts]
  Position-on-arc:         [0.x]  — [stage → unconditional P(approval) gate; arc phase from moa-analog-engine]
  Competitive-timing:      [0.x]  — [order-of-entry; IP runway; SoC drift; crowding]

Base-rate anchors used:
  Therapeutic area LOA:    [x]% ([area])
  Modality LOA:            [x]% ([class]; bimodality noted if CGT)
  Levers applied:          [genetic 2.6x / biomarker 3x / orphan 17% — list, no double-count]

BINDING RISK (where to diligence next):
  [Biology | Platform/delivery | Arc position | Competitive timing] — [one-line rationale]

For zero-clinical-history modality:
  Borrowed matrix:         [class] | Haircut concentrated on: P1→P2 | De-risking inflection to watch: [first platform PoC event]

rNPV HANDOFF:
  Trigger met? [Yes — clinical asset + indication exist / No — pre-clinical, stay ordinal]
  If yes → hand to rnpv-modeler + pos-calculator with PoS ladder anchored above.

Caveats:
  - Score is ORDINAL and RELATIVE — not a cash-flow estimate.
  - Genetic support de-risks biology, NOT platform.
  - [recency: 5% vs 7.9% anchor choice rationale]
```

## Error Handling

| Scenario | Response |
|---|---|
| User quotes "~10% PoS" generically | Replace with the area- and modality-specific CDP rate; a Phase 1 oncology asset is ~5%, not 10% — generic figures overestimate ~2x |
| CDP and ME rates mixed in one analysis | Stop; fix one convention (default CDP); ME runs ~2x CDP and silently double-counts |
| Modality has no clinical history | Run Step 4: borrow nearest validated class matrix, haircut Phase 1→2 for delivery/CMC/regulatory novelty; never a de novo optimistic number |
| CGT blended 5.3% applied to a CAR-T or AAV asset | Use the bimodal sub-rate (CAR-T/AAV 13.6%, front-loaded risk), not the blend |
| Strong genetics cited to justify a risky platform | Reject the credit transfer; genetic support de-risks biology only — platform risk is orthogonal and resolves at first human PoC |
| Designations stacked multiplicatively (orphan × biomarker × BTD) | Apply the dominant lever; treat designations as confirmatory tier-bumps, not stackable multipliers — selection bias inflates raw lifts |
| Clinical asset + indication now exist | Retire the trajectory score; trigger rNPV handoff (rnpv-modeler + pos-calculator) |
| "AI-discovered target" claimed as de-risking | Down-weight unless AI acted in molecular design with independent wet-lab/clinical validation; AI does not move Phase 2/3 attrition |

## Cross-Domain Connections

This skill is the synthesizer at the bottom of the Frontier Discovery analog engine; it depends on four PoS/valuation skills and serves both a learning clinical scientist and a screening investor.

- **probability-of-success/pos-base-rates** (depends_on): supplies the actuarial tables — the CDP/ME conventions, the by-area and by-modality LOAs, the genetic/biomarker/orphan multipliers. This skill is the discovery-stage *front end* to those base rates; pos-base-rates is the canonical data source both readings cite.
- **probability-of-success/pos-calculator** (depends_on): the rNPV-handoff target. When a clinical asset exists, the ordinal trajectory factors retire and pos-calculator applies the phase-weighted PoS ladder. The clinical scientist uses it to formalize a hunch; the investor uses it to anchor a term sheet.
- **asset-valuation/rnpv-modeler** (depends_on): consumes the handoff PoS ladder to produce the absolute, cash-flow-anchored, deal-ready valuation. Trajectory conviction decides *what to advance*; rNPV decides *what it's worth* once advancing.
- **probability-of-success/mechanism-risk-adjuster** (depends_on): refines P(biology holds) — applies mechanism-class and first-in-class penalties on top of the genetic-support credit so the biology factor reflects mechanism risk, not just target causality.
- **modality-trajectory/modality-lifecycle**: supplies P(modality deliverable) — whether the delivery unlock has landed and whether the modality is maturing or regressing on the arc.
- **modality-trajectory/moa-analog-engine**: supplies position-on-arc — the nearest validated analog and the still-pending ignition readout to watch.
- **frontier-discovery/target-validation-ladder**: supplies the graded genetic rung that feeds P(biology holds) directly.
- **competitive-intelligence/pipeline-mapper**: supplies the competitive set and order-of-entry feeding competitive-timing.
