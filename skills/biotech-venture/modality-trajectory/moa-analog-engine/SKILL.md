---
name: moa-analog-engine
description: >
  Place a discovery- or early-clinical-stage drug candidate on the historical
  arc of its mechanism class. Given a target, modality, or mechanism, finds the
  nearest validated analog among twelve matured classes, names the still-pending
  ignition trial to watch, dates its position on the five-phase life-cycle, and
  reads a marquee failure followed by modality re-engineering as a buy signal,
  not a kill. Activate when asking "what does this mechanism become, how long,
  and what proves it" — for a clinician learning the field or an investor
  screening early opportunities.
metadata:
  author: nirav
  version: "1.0"
  parent: modality-trajectory
compatibility: Designed for Claude Code
allowed-tools: Read
---

# MOA Analog Engine — Placing a Mechanism on the Historical Arc

Drug mechanism classes do not mature randomly. Across twelve matured classes — PD-1, GLP-1, PCSK9, KRAS G12C, CD19 CAR-T, siRNA/ASO, ADC, PROTAC/molecular-glue, complement, anti-amyloid, IL-23/IL-17, BTK — development obeys a stable five-phase life-cycle (target ID → tool/platform → first-in-human → first approval → class explosion → maturity) with a remarkably stable clock: **18-30 years from validated target to first approval, then a compressed 2-5 year explosion** once an unambiguous, hard-endpoint pivotal trial reads out in a genetically- or biomarker-defined population. PCSK9 was the speed champion (~12 yr, clean human knockouts); KRAS the slowest (~39 yr, "undruggable" until the 2013 covalent chemistry); PROTAC sits at ~24 yr (2001 concept → vepdegestrant 2025).

The engine's core move is **analogical placement**: a new candidate is never reasoned about de novo. You find the nearest matured class it rhymes with, locate where the candidate sits on that class's arc, and read off what comes next and what would prove it. The single most decisive object is the **ignition event** — one identifiable pivotal readout (KEYNOTE-024, FOURIER, ELIANA, SELECT, CodeBreaK 100, CLARITY-AD, VERITAC-2) that converted skepticism to capital. For a pre-ignition candidate, the entire question reduces to: *which trial is its ignition event, and when does it read out?*

The most counterintuitive — and most valuable — doctrine: **a marquee failure followed by modality re-engineering is a buy signal, not a kill.** Anti-amyloid absorbed ~15 years of failures before lecanemab/donanemab; ADCs died with gemtuzumab's 2010 withdrawal and returned via DXd payloads; siRNA was dead-on-delivery until GalNAc. The discriminating question is whether the failure was in the *biology* (kills the class — CETP/torcetrapib raised mortality) or in the *modality/execution* (re-engineerable — bad linker, bad delivery, wrong dose, wrong amyloid species). This skill serves a clinical-scientist mapping how a field will unfold and an investor timing entry around the next ignition readout — the same arc, read for understanding or for alpha.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Target or mechanism of action | User / emerging-target-radar candidate object | Yes |
| Modality (small molecule, mAb, siRNA, degrader, CAR, etc.) | User | Recommended |
| Indication | User | Recommended |
| Lead asset(s) and sponsor(s) | User / ClinicalTrials.gov | Optional |
| Known false starts / failed predecessors | User / PubMed | Optional |

### Steps

#### Step 1 — Characterize the Candidate

Pin down the four coordinates that determine which analog applies:
- **Target class**: receptor / enzyme / oncogene / scaffold-or-TF / cytokine / cell-surface antigen. Flat-surface, intrinsically-disordered, or pocket-less targets route to the undruggable-cracking pattern.
- **Validation type**: human genetic LOF/GOF carriers (strongest), KO-mouse, biomarker-defined population, or association-only. Query **Open Targets** for the target-disease genetic score and **gnomAD** for human-knockout tolerance.
- **Modality maturity**: is the modality itself proven, or is this a modality-on-novel-target combination? (Hand to `modality-lifecycle` for the deliverability term.)
- **Current development stage**: preclinical / tool compound / first-in-human / registrational. Confirm via **ClinicalTrials.gov** (trial existence, phase, enrollment) and **ChEMBL** (tool-compound and approved-drug MOA annotations).

#### Step 2 — Find the Nearest Validated Analog

Match the candidate to the closest of the twelve arcs in `references/moa-arc-library.md`. Match on the **mechanism of unlock**, not the indication. Heuristics:

```
ANALOG-MATCHING HEURISTICS

If target is "undruggable" (flat/disordered/no pocket) and unlock is chemistry
   → KRAS G12C arc (covalent switch-II) or PROTAC/glue arc (E3 recruitment)
If validation is healthy human LOF carriers mirroring drug effect
   → PCSK9 arc (the genetics-first speed playbook)
If one mechanism keeps expanding into new indications on a dose-response signal
   → GLP-1 arc (indication-creep explosion)
If progress is gated by a delivery/conjugation problem, not biology
   → siRNA/GalNAc arc or ADC/linker arc
If each new agent is triggered by a defined resistance mutation
   → BTK arc (generational resistance ladder)
If the class is absorbing repeated high-profile failures
   → anti-amyloid arc (false-start-as-penultimate-stage)
If an n-of-1 durable response in terminal disease appeared
   → CAR-T arc or PD-1 arc (durable-tail signal)
If a long-monopoly first agent leaves a clear unmet need inside treated patients
   → complement arc (unmet-need-wedge second wave)
If pathway dissection spawns adjacent cleaner sub-classes
   → IL-23/IL-17 arc
```

Name the analog explicitly and state *why* it is the nearest rhyme. A candidate may match a **primary arc** (mechanism shape) and a **sub-pattern** (how it explodes) from different classes — record both.

#### Step 3 — Classify the Sub-Pattern

Assign one of the three named templates (full profiles in the library):

- **Undruggable-cracking** — a pocket-less / disordered / flat-surface target unlocked by a *modality* innovation (covalent trapping, tri-complex/glue, degradation). The unlock is chemistry, not biology. Index case: KRAS (single 2013 *Nature* paper → pan-RAS franchise). Leading indicator: the first co-crystal structure of a covalent/ternary ligand — once it generalizes beyond the index target, the class is real.
- **Indication-creep explosion** — one mechanism expands across indications on a dose-dependent signal visible years early (GLP-1: T2D → obesity → CV outcomes → MASH/CKD). Leading indicator: a hard-surrogate effect (weight, LDL) legible in early trials a decade before the marquee approval.
- **Generational resistance-ladder** — each rung triggered by a defined resistance/tolerability problem (BTK: covalent → cleaner covalent → non-covalent for C481S → degraders). Leading indicator: a dominant, recurrent escape mutation *guarantees* the next sub-class forms.

#### Step 4 — Place Arc-Position and Estimate the Clock

Locate the candidate on the five phases (0 Target ID → 1 Tool → 2 FIH → 3 First approval → 4 Explosion → 5 Maturity). Then estimate the remaining clock by subtracting elapsed years from the analog's observed time constant:

```
TIME-CONSTANT REFERENCE (target ID → first approval)

PCSK9  ~12 yr  (fastest — clean human LOF carriers)
IL-23/17 ~8-15 yr
BTK    ~20 yr
PD-1   ~22 yr
GLP-1  ~20-23 yr
PROTAC ~24 yr
CAR-T  ~25+ yr
anti-amyloid ~31-32 yr
KRAS   ~39 yr  (slowest — undruggable until 2013 chemistry)

Median ~18-25 yr. Explosion window (first approval → crowded field): 2-5 yr.
Rate-limiter is the SLOWEST of: modality/druggability, validation, or biology.
```

Flag the rate-limiter explicitly — a validated-biology / no-modality candidate (KRAS 1982-2013) idles until the platform fix arrives.

#### Step 5 — Name the Ignition Trial to Watch

This is the engine's highest-value output. For a pre-ignition candidate, identify the **single still-pending pivotal readout** that would convert the class. The ignition event is always a hard-endpoint trial in a genetically- or biomarker-defined population. Query **ClinicalTrials.gov** for the registrational trial (NCT#, phase, enrollment, estimated primary completion), name the hard endpoint, and date the readout window.

```
IGNITION-EVENT TEMPLATE (per matured analog)

PD-1          → KEYNOTE-024 (1L NSCLC, PD-L1≥50%, 2016)
PCSK9         → FOURIER (CV MACE, 2017)
CAR-T         → ELIANA / ZUMA-1 (2017)
GLP-1 obesity → SELECT (CV outcomes in non-diabetic obesity, 2023)
KRAS G12C     → CodeBreaK 100 (2021)
ADC redemption→ DESTINY-Breast / T-DXd (2019-2022)
anti-amyloid  → CLARITY-AD (lecanemab, 2023)
PROTAC        → VERITAC-2 (vepdegestrant ESR1m, 2025)
```

For the candidate, state: "Its ignition analog is [trial]; the pending equivalent is [NCT#/program], reading [endpoint] in [window]. A positive hard-endpoint readout in the defined population would ignite; a soft-surrogate or all-comers readout would not."

#### Step 6 — Run the False-Start Diagnostic

If the class has absorbed a high-profile failure, classify it:
- **Biology failure** (kills the class): effect on a soft/unvalidated surrogate with no genetic tie to outcomes (CETP/torcetrapib); hitting the wrong molecular species or disease stage with confirmed mechanism harm (γ-secretase worsened cognition).
- **Modality/execution failure** (re-engineerable → buy signal): bad linker (first-gen ADC), bad delivery (pre-GalNAc siRNA), wrong dose, wrong amyloid species, bad oral PK (early PROTAC). If a re-engineered asset with the fix is now advancing, treat the prior failure as the *penultimate stage* and the class as pre-explosion.

State the verdict: **biology-killed (avoid)** vs **modality-redeemable (watch the re-engineered asset's ignition readout)**.

### Output

```
MOA ARC PLACEMENT — [Target × Modality, Indication]
Date: [assessment date]

Candidate coordinates:
  Target class: [receptor/enzyme/oncogene/scaffold/cytokine/antigen]
  Validation:   [human LOF | KO mouse | biomarker pop | association]
  Modality:     [type] (maturity: [proven | novel-on-target] — see modality-lifecycle)
  Stage:        [Phase 0-5], lead asset [name/NCT#], sponsor [co.]

Nearest validated analog: [arc name]
  Why: [the shared unlock mechanism — chemistry/genetics/delivery/resistance]
  Sub-pattern: [undruggable-cracking | indication-creep | resistance-ladder]

Arc-position: Phase [N] — [phase name]
  Elapsed since target ID: ~[X] yr
  Analog time constant: ~[Y] yr  →  est. remaining to first approval: ~[Y-X] yr
  Rate-limiter: [modality | validation | biology]

IGNITION EVENT TO WATCH:
  Analog ignition: [trial, year]
  Pending equivalent: [NCT# / program], [hard endpoint], readout [window]
  Verdict if positive: [class ignites — explosion in 2-5 yr]
  Verdict if soft/negative: [stalls — re-engineering or re-validation needed]

False-start diagnostic: [none | biology-killed (AVOID) | modality-redeemable (BUY-on-re-engineering)]
  Prior failure: [asset, year, cause]
  Re-engineered fix now advancing: [asset/platform]

Leading indicators present: [LOF carriers | n-of-1 durable response | recurrent
  resistance mutation | generalizing platform | off-target-population efficacy |
  early hard-surrogate signal | unmet-need-inside-treated-population]

Bottom line: [1-2 sentences — where it is, what proves it, when, buy/watch/avoid]
```

## Error Handling

| Scenario | Response |
|---|---|
| No clean analog among the twelve | Match on sub-pattern (unlock mechanism) even if indication differs; flag as "novel — borrow nearest pattern, widen uncertainty" |
| Candidate is a modality on an already-validated target | Split the analysis: biology rides the validated arc; modality risk routes to `modality-lifecycle`. Do not double-count target risk |
| Multiple plausible analogs | Report primary (mechanism shape) and secondary (explosion pattern); state which time constant dominates |
| Ignition trial not yet registered | Note the gap; name the endpoint/population the future pivotal *must* hit; monitor ClinicalTrials.gov and congress abstracts |
| Class has a failure but no re-engineered successor yet | Hold as "biology-vs-modality unresolved"; do not call buy until the fix is identifiable and advancing |
| Pre-IND / tool-compound stage | Place at Phase 1-2; emphasize the time-constant estimate over the ignition trial (which doesn't exist yet) |
| User conflates target validation with class validation | Separate them: a validated target with no validated modality still idles (KRAS 1982-2013) |

## Cross-Domain Connections

- **research/spelunker** (depends_on): supplies the deep primary-literature dives that establish target ID dates, the enabling-platform paper, and the false-start record an arc placement rests on. The engine is only as good as the dated history the spelunker recovers.
- **probability-of-success/pos-base-rates** (depends_on): the qualitative arc-position must hand off to quantitative phase-transition base rates the moment a clinical asset and indication exist. Arc-position tells you *which* transition matters next; pos-base-rates tells you the *odds* of clearing it (e.g., biomarker-selected ~3x LOA, oncology ~5% vs hematology ~26%).
- **modality-trajectory/modality-lifecycle**: supplies the P(modality deliverable) term and the "has the delivery unlock landed?" state variable that gates whether a class can explode at all.
- **competitive-intelligence/pipeline-mapper**: once arc-position says "explosion imminent," pipeline-mapper enumerates the fast-followers crowding in during the 2-5 year window.
- **emerging-target-radar** (upstream): feeds the candidate objects {target, modality, indication, signals} this engine places on the arc.
- **frontier-conviction-scorer** (downstream): consumes arc-position and ignition-event timing as the position-on-arc and competitive-timing terms of the decomposed conviction score.
- **Dual use:** a clinical-scientist uses the arc to learn how a mechanism field will unfold and what evidence to trust; an investor uses the identical arc to time entry around the next ignition readout and to treat a re-engineered comeback as alpha rather than a falling knife.
