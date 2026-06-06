---
name: emerging-target-radar
description: >
  Fuse literature/preprint velocity, scientific mindshare, and orthogonal data-engine
  convergence into a ranked watchlist of emerging target x modality candidates — each tagged
  with realized/expected literature-to-first-in-human lead time, the responsible NewCo-creation
  events, and which historical pattern it follows (genetics-first, modality-unlock, or
  resistance-ladder). Activate when scanning the discovery frontier for what is inflecting before
  consensus, building or refreshing an early-stage target watchlist, or sourcing candidate objects
  for downstream arc-placement and conviction scoring.
metadata:
  author: nirav
  version: "1.0"
  parent: frontier-intelligence
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Emerging Target Radar — The Pre-Consensus Watchlist Integrator

The single most valuable thing a frontier investor or a clinical scientist entering a new field can know is *what is inflecting before everyone agrees it is*. Scientific mindshare accreting to an emerging target or modality is measurable, with lead times running from ~5-7 years (NIH grant flows) down to near-real-time (conference share-of-voice). The radar's job is to fuse those signals into one ranked, defensible watchlist instead of chasing whatever was loudest at the last JPM.

This skill is the **integrator**. It does not generate raw velocity, attention, or convergence signals itself — three upstream skills do that (signal-scanner, mindshare-tracker, data-generation-monitor). The radar consumes their outputs and produces a single ranked list of `{target × modality}` candidates, each carrying its **lead-time estimate** (the literature-inflection-to-first-in-human gap, typically 3-7 years for a novel target), its **NewCo-creation events** (the sharpest venture signal there is), and its **historical-pattern tag** (genetics-first like PCSK9/GPR75, modality-unlock like KRAS/VAV1, or resistance-ladder like BTK). These candidate objects are the input contract for the downstream analog engine (moa-analog-engine, modality-lifecycle, frontier-conviction-scorer).

The core discipline is anti-hype. Mindshare is reflexive — capital manufactures the attention it claims to detect — so a candidate's rank is a *positioning/timing* instrument, never a measure of biological merit. Every velocity signal must be gated by an evidence-maturity check and normalized against the financing regime (Q1 2025 was the lowest US biotech startup formation in a decade, ~70% off the 2021 peak, so a single NewCo means more in 2025 than it did in 2021).

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Scope (therapeutic area, modality, or "broad frontier scan") | User | Yes |
| Signal-scanner output (velocity + acceleration + breadth per entity) | signal-scanner skill / WebSearch | Recommended |
| Mindshare-tracker output (0-100 momentum + Consensus evidence gate) | mindshare-tracker skill / WebSearch | Recommended |
| Data-generation-monitor output (orthogonal-convergence counts) | data-generation-monitor skill | Recommended |
| Time window for velocity (e.g. trailing 3 yr) | User | Optional (default: 3 yr) |
| Existing watchlist to refresh | User / Read | Optional |
| Financing-regime normalization year | User | Optional (default: current) |

If the three upstream signal streams are unavailable, reconstruct them inline: query PubMed E-utilities for `total_count` velocity, bioRxiv/medRxiv for preprint lead, conference abstract databases for share-of-voice, and EDGAR/press/Crunchbase for NewCo events. The skill degrades gracefully but is strongest when fed clean upstream objects.

### Steps

#### Step 1 — Assemble the Candidate Universe

Pull every `{target × modality}` pair surfacing in the three signal streams within scope. Do not pre-filter on merit — the universe is deliberately broad; ranking happens later.

Seed sources to query directly when upstream streams are thin:
- **PubMed E-utilities** — `total_count` per `target[tiab] AND modality[tiab]` per year; compute YoY velocity and the second derivative (acceleration). Strip review/perspective publication types before counting.
- **bioRxiv / medRxiv** — preprint volume per entity (leads peer-reviewed by 6-18 months); the earliest formal-literature signal.
- **Open Targets** — genetics-to-target associations; flags genetics-first candidates.
- **ClinicalTrials.gov v2** — first IND/Phase-1 entry is the *translation-event ground truth* that closes the lead-time measurement.
- **ChEMBL** — is there tractable chemical matter yet (IC50/EC50/Ki), or is this still a tool-compound gap?

#### Step 2 — Fuse the Three Signal Streams per Candidate

For each candidate, combine the upstream signals into a fused signal profile. The streams are deliberately orthogonal — they catch different false positives:

```
FUSED SIGNAL PROFILE — {target × modality}

  Velocity  (signal-scanner):   accel of PubMed total_count + bioRxiv preprint vol; author-affiliation
                                 breadth (Herfindahl — high concentration = single-lab artifact, discount)
  Attention (mindshare-tracker): 0-100 momentum from conference share-of-voice (AACR/ASCO/ASH/ESMO/JPM);
                                 GATED by Consensus evidence-maturity (volume high + quality low = HYPE flag)
  Convergence (data-gen-monitor): count of net-new ORTHOGONAL data-engine convergences
                                 (cis-pQTL+MR AND selective DepMap dependency AND clean Perturb-seq AND
                                  druggable ChEMBL matter AND cell-type-restricted expression)
```

A candidate with high velocity but a HYPE flag and zero orthogonal convergences is froth. A candidate with moderate velocity, multi-lab breadth, and 3+ convergences is a durable inflection. Rank rewards the second, not the first.

#### Step 3 — Estimate Lead Time (Literature-Inflection → First-in-Human)

For each candidate, locate the literature-velocity inflection year and the first-in-human (FIH) entry, or project the FIH if not yet reached.

```
LEAD-TIME ESTIMATE

  Inflection year   = year the second derivative of publication/preprint volume turned sharply positive
  FIH year          = first Phase-1 entry on ClinicalTrials.gov v2 (REALIZED) — or projected from arc position
  Realized lead     = FIH year − Inflection year         (only if FIH has occurred)
  Expected lead     = 3-7 yr from inflection for a novel target (use 3 yr if tool compound + chemical matter
                      already exist; 7 yr if still target-ID/biology stage with no tractable handle)
```

The realized/expected lead time is what tells an investor *how much runway remains before consensus prices it* and tells a scientist *how mature the field is*. A candidate already past FIH with a short realized lead (PCSK9 ~12 yr target-to-approval) is late-stage radar; a candidate at tool-compound stage with a 5-7 yr expected lead is the earliest actionable read.

#### Step 4 — Capture NewCo-Creation Events (the Sharpest Venture Signal)

A venture builder spinning out a NewCo around a *specific* target/modality front-runs consensus by 1-2 years — far more informative than aggregate sector financing. Record each event and **normalize against the financing regime**:

```
NEWCO SIGNAL

  Events: [company, round/$ , date, builder (Flagship/ARCH/etc.), specific target×modality]
  Big-pharma deal proxy: large licensing/M&A on the exact mechanism counts as a confirmation NewCo-equivalent
    (e.g. Novartis × Monte Rosa VAV1 degrader up to $2.1B; Sanofi × Vigil TREM2 $470M+; AbbVie × Capstan ~$2.1B)
  Regime normalization: weight each event UP in a contractionary year. Q1 2025 = decade-low US startup
    formation (~70% off 2021 peak), so a 2025 NewCo carries more conviction than a 2021 one.
```

#### Step 5 — Tag the Historical Pattern

Assign each candidate exactly one of three named patterns (the analog engine keys off this tag). The pattern predicts *how* the class will explode and *what* the ignition event will be:

```
PATTERN TAG

  genetics-first    — human-genetics (esp. LoF-protective) validation came BEFORE the drug.
                      Ignition = CV/hard-outcome trial. Analogs: PCSK9, GPR75, INHBE/ALK7, TL1A.
  modality-unlock   — a flat/disordered/pocketless target made tractable by a CHEMISTRY/PLATFORM fix,
                      not new biology. Analogs: KRAS (covalent switch-II), VAV1 (molecular glue),
                      in vivo CAR (tLNP), siRNA targets (GalNAc). Ignition = first-in-class pivotal readout.
  resistance-ladder — each new sub-class triggered by a defined resistance mutation. Analogs: BTK
                      (ibrutinib → acalabrutinib → pirtobrutinib C481S → BTK degraders). Ignition =
                      the resistance mechanism itself is the leading indicator of the next rung.
```

#### Step 6 — Rank and Emit the Watchlist

Score each candidate and sort. The composite rank is a positioning score, not a PoS:

```
RADAR RANK (0-100) =
    0.35 × fused_signal_strength      (velocity accel + breadth + convergence count, gated by evidence-maturity)
  + 0.25 × newco_signal               (count × regime-normalization weight)
  + 0.25 × lead_time_actionability    (more remaining runway before consensus = higher; penalize already-crowded)
  + 0.15 × pattern_clarity            (clean genetics-first or post-ignition modality-unlock ranks above ambiguous)

  HARD GATES (apply before scoring):
    — HYPE flag (high volume, low Consensus evidence quality) → cap rank at 40, route to "watch, don't underwrite"
    — Single-lab artifact (Herfindahl breadth fail) → cap rank at 40
    — "AI-discovered target" claim with no independent wet-lab/clinical validation → discount; AI moving
      molecular DESIGN is credible, AI "finding a novel target" usually is not (targets were already implicated)
```

### Output

```
EMERGING TARGET RADAR — {Scope}
Date: [assessment date]   |   Velocity window: [window]   |   Regime year: [year]

RANKED WATCHLIST

| Rank | Target × Modality | Pattern Tag | Arc Position | Lead Time (R/E) | NewCo / Deal Signal | Fused Signal | Evidence Gate |
|------|-------------------|-------------|--------------|-----------------|---------------------|--------------|---------------|
| 1    | RAS(ON) tri-cplx  | modality-unlock | FIH→1st-appr (Ph3) | realized ~8 yr | RevMed (public) | accel↑↑ / conv 4 | PASS |
| 2    | GPR75/INHBE × siRNA | genetics-first | tool→FIH | expected 4-6 yr | Arrowhead/Regeneron | accel↑ / conv 5 | PASS |
| ...  |                   |             |              |                 |                     |              |               |

CANDIDATE OBJECTS (handoff to analog engine) — one per row:
  { target, modality, indication, arc_position, pattern_tag, lead_time, newco_events,
    supporting_signals: {velocity, mindshare, convergence}, evidence_gate, radar_rank }

TOP-OF-RADAR NARRATIVE:
1. [Highest-conviction pre-consensus read and why now]
2. [Steepest adoption curve this cycle]
3. [The one to "watch, don't underwrite" — high mindshare, evidence gap]

DEPRIORITIZED (gated out):
  - [Candidate] — [HYPE flag / single-lab / AI-novelty discount]
```

## Error Handling

| Scenario | Response |
|---|---|
| Upstream signal streams unavailable | Reconstruct inline via PubMed E-utilities, bioRxiv/medRxiv, conference abstracts, EDGAR/press — flag as lower-fidelity |
| High velocity but no convergence and HYPE flag | Hard-gate to "watch, don't underwrite"; do not let loud literature inflate rank |
| Single-lab dominates the literature (Herfindahl fail) | Discount as artifact (>50% of preclinical findings irreproducible); require multi-lab breadth before ranking |
| No FIH yet (no ClinicalTrials.gov entry) | Use *expected* lead time from arc position (3 yr if tractable chemical matter exists, 7 yr if still biology-stage) |
| NewCo events sparse | Check big-pharma licensing/M&A on the exact mechanism as a confirmation-equivalent; do not treat absence as a kill |
| "AI-discovered target" claim | Down-weight unless AI acted in molecular *design* with independent validation; AI does not yet move Phase 2/3 odds |
| Crowded/post-explosion class | Lower lead-time actionability; flag that alpha has likely left (convenience/cadence reformulation = maturity) |
| Contractionary financing year | Up-weight each NewCo event; one 2025 spinout > one 2021 spinout for conviction purposes |

## Cross-Domain Connections

This skill is explicitly **dual-use**: a clinical-scientist entering a field reads the watchlist as a map of *where the science is inflecting and how mature each frontier is*; an investor reads the identical output as a *screen of early opportunities with remaining runway before consensus pricing*. Lead-time and pattern-tag serve both readers.

- **frontier-intelligence/signal-scanner** *(depends_on)*: supplies the velocity/acceleration/breadth primitive the radar fuses — the literature inflection that starts the lead-time clock
- **frontier-intelligence/mindshare-tracker** *(depends_on)*: supplies the 0-100 attention momentum and the Consensus evidence-maturity gate that powers the anti-hype hard gate
- **frontier-intelligence/data-generation-monitor** *(depends_on)*: supplies the orthogonal-convergence count — the strongest durable-merit signal that separates inflection from froth
- **frontier-intelligence/moa-analog-engine**: primary consumer — takes each candidate object, finds its nearest validated analog, and names the still-pending ignition trial to watch
- **frontier-intelligence/modality-lifecycle**: consumes the modality half of each candidate to supply the P(modality deliverable) term and confirm the delivery unlock has landed
- **frontier-intelligence/frontier-conviction-scorer**: ultimate consumer — converts the ranked candidate into a decomposed conviction score, handing off to phase-weighted rNPV once a clinical asset exists
- **competitive-intelligence/pipeline-mapper** *(depends_on)*: once a candidate crosses into the clinic, pipeline-mapper enumerates the competitive set and confirms the "pre-explosion crowding" signal (e.g. every major immunology pharma owning a TL1A asset)
- **product/frontier-antenna** *(depends_on)*: shares the cross-domain frontier-scanning methodology; the radar is the biotech-specialized instance feeding product-level frontier signals
- **neocortex/foresight** *(depends_on)*: the radar's lead-time + pattern-tag output is a structured foresight signal — second-derivative detection of an emerging trend before consensus
