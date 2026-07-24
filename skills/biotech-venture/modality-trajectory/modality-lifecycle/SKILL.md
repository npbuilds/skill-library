---
name: modality-lifecycle
description: >
  Place a therapeutic modality on its maturity arc and answer "is this deliverable yet?"
  using a live mature-vs-proving map keyed to the delivery unlock as the primary state
  variable. Produces a modality position read with the binding delivery bottleneck, the
  platform fix that converts the class, and a P(modality deliverable) term for the
  conviction scorer. Activate when assessing whether a modality is ready, what gates its
  next stage, or whether a stalled class is about to inflect — for clinicians learning
  the field and investors screening early opportunities alike.
metadata:
  author: nirav
  version: "1.0"
  parent: modality-trajectory
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Modality Lifecycle — The Live Maturity Map of Drug Delivery

Modalities, not just molecules, have life-cycles. A small molecule, a GalNAc-siRNA, and an in-vivo CRISPR editor are at radically different points on the same arc — and the single state variable that determines where a modality sits is not its biology but its **delivery unlock**: what is the delivery problem, and has the fix landed? Get this wrong and you either dismiss a class that just inflected (TPD before vepdegestrant) or over-credit one whose delivery wall is still standing (extrahepatic RNAi, in-vivo CAR in humans).

The core principle: **the platform fix, not new biology, is what converts a stalled class.** siRNA was dead-on-delivery for a decade until GalNAc conjugation gave it the liver; KRAS was "undruggable" until the 2013 covalent switch-II discovery; degraders waited on E3-ligase recruitment; ADCs were left for dead after gemtuzumab until site-specific linkers and DXd payloads. A high-profile failure followed by a modality re-engineering is a buy signal, not a kill signal. And the arc runs both ways: a modality can **regress** — AAV gene therapy slid backward in 2025 after Elevidys was tied to ≥3 deaths and an FDA dosing pause.

This skill is dual-use by design. For a clinician-scientist it is a map of where each modality actually stands and what unlocks the next tissue. For an investor it supplies the **P(modality deliverable)** term that the conviction scorer multiplies against P(biology holds), arc-position, and competitive timing — the discipline that stops a great target from being funded inside an undeliverable modality.

> **Maturity map:** the per-modality S-curve placement, delivery-wall lookup, and platform-fix registry are versioned in `references/modality-maturity-map.md` (a 2026 point-in-time snapshot — the most perishable data in the pillar).

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Modality (e.g., in-vivo CAR, GalNAc-siRNA, base editing, PROTAC) | User | Yes |
| Target tissue / compartment (liver, muscle, CNS, T-cell, tumor) | User | Recommended — delivery is tissue-specific |
| Specific asset / company (if scoring a candidate) | User | Optional |
| Indication | User | Optional (gates which delivery route matters) |
| Use mode: learn (field map) vs screen (conviction input) | User | Optional (default: screen) |

### Steps

#### Step 1 — Locate the Modality on the Four-Stage Maturity Map

Assign one of four stages. The boundary tests are concrete, not vibes:

- **Emerging** — first-in-human to early Ph1; proof-of-mechanism not yet durable or safe at scale. (in-vivo CAR, prime editing, CAR-NK/allogeneic)
- **Proving** — Ph1/2 efficacy signals replicating; ≤1 approval; platform risk still live. (TPD, base editing, in-vivo CRISPR nuclease, TCR-T/TIL, oral biologics, saRNA)
- **Established** — multiple approvals; mechanism de-risked; scaling/access is the remaining work. (ADCs, ASO/siRNA, mRNA vaccines, ex-vivo CAR-T, ex-vivo CRISPR, RLT, lentiviral)
- **Mature** — dozens-to-hundreds of approvals; commoditized; innovation is incremental or in delivery. (small molecules, mAbs, peptides/macrocycles)

Start from the maturity-map table in `references/quick-reference.md`. Do not anchor on hype — anchor on **approvals shipped × mechanism de-risking**.

#### Step 2 — Identify the Binding Delivery Bottleneck

For the modality + target tissue, name the **one** delivery/enabling-technology constraint that gates the next stage. This is the load-bearing analytical step. The universal rate-limiter in 2026 is delivery, not biology:

```
DELIVERY-WALL LOOKUP
  siRNA / ASO            → extrahepatic reach (CNS, muscle, lung, immune cells)
  in-vivo CRISPR/base    → LNP tropism beyond liver
  in-vivo CAR            → T-cell- (or HSC/NK-) tropic LNP / retargeted vector
  AAV                    → pre-existing immunity, no redosing, liver-detargeting capsids
  mRNA therapeutics      → repeat-dose tolerability, extrahepatic LNP
  oral peptides/biologics→ gut proteolysis + epithelial permeability (often <2% F)
  radioligand therapy    → isotope supply chain (Ac-225) + radiopharmacy sites
  cell therapies         → "delivery" = manufacturing logistics + persistence/rejection
  prime editing          → editor payload size (hard to package)
```

Verify the current state of the wall against live data:
- **ClinicalTrials.gov** (c-trials MCP) — confirm phase/status/enrollment of the proof-point trials (e.g., HAELO for lonvo-z; CPTX2309 Ph1; RAG-17 NCT06556394 for SCAD/intrathecal siRNA).
- **bioRxiv/medRxiv** — delivery-platform preprints (tLNP, antibody-siRNA conjugates, novel capsids) lead approvals by 6-18 months; this is where the next unlock surfaces first.
- **ChEMBL** — bioactivity for the enabling chemistry (covalent KRAS warheads, E3-recruiting glues, payload IC50s).
- **PubMed/PMC + Consensus** — mechanism/review literature and evidence synthesis on whether the delivery claim actually replicates.

#### Step 3 — Determine Whether the Platform Fix Has Landed

Convert "delivery wall" into a binary-with-evidence: **has the enabling-platform fix landed, partially landed, or not?** The known fixes that convert a stalled class:

```
PLATFORM-FIX REGISTRY (fix, not biology, converts the class)
  GalNAc conjugation        → siRNA/ASO to liver (LANDED — inclisiran, vutrisiran)
  covalent switch-II        → KRAS druggability (LANDED — sotorasib 2021)
  tri-complex / RAS(ON)     → pan-RAS beyond G12C (LANDING — daraxonrasib Ph3/BTD)
  E3-ligase recruitment     → targeted degradation (LANDED — vepdegestrant 2025)
  site-specific linker + DXd → ADC redemption (LANDED — T-DXd, Datroway, Emrelis)
  T-cell-tropic LNP (tLNP)  → in-vivo CAR (PARTIAL — CPTX2309 Ph1, NHP data only)
  C16/antibody-siRNA conj.  → extrahepatic RNAi (PARTIAL — muscle AOCs, SCAD preclinical)
  low-seroprevalence capsid → AAV redosing (NOT LANDED — class regressed post-Elevidys)
  multiplexed HLA editing   → allogeneic persistence/rejection (NOT LANDED)
```

If the fix has LANDED → modality clears for that tissue. If PARTIAL → flag the specific trial whose readout closes it. If NOT LANDED → the modality is gated regardless of target merit.

#### Step 4 — Check for Regression and Maturity Signals

The arc is bidirectional and the late-arc tells matter:

- **Regression flag** — a marquee safety event reversing a class. AAV is the index case: Elevidys (DMD) tied to ≥3 liver-injury deaths and an FDA dosing pause in 2025, with Sarepta itself pivoting toward siRNA for redosing. A regressed modality borrows a *worse* transition matrix, not its pre-event one.
- **Maturity / commoditization flag** — convenience/cadence reformulation. When a class competes on **route and dosing cadence rather than efficacy**, the alpha has left: subcutaneous nivolumab/pembrolizumab (Keytruda Qlex, Sept 2025), oral GLP-1 orforglipron, oral PCSK9 enlicitide, twice-yearly inclisiran. Note this for the investor read — mature ≠ attractive entry.

#### Step 5 — Emit the P(modality deliverable) Term

Translate the position into a deliverability probability for the conviction scorer. Anchor to modality LOA base rates and apply delivery/CMC/novelty haircuts:

```
P(modality deliverable) = base_modality_LOA_proxy × delivery_state_multiplier × regression_penalty

base proxies (LOA, BIO/Informa class reads):
  vaccines ~9.7% | biologics ~9.1% > small molecules ~5.7% | CGT ~5.3% bimodal
  (CAR-T / AAV historically 13.6% in their validated indications)

delivery_state_multiplier:
  LANDED for this tissue        = 1.0
  PARTIAL (proof in NHP/Ph1)    = 0.6-0.8
  NOT LANDED (wall standing)    = 0.3-0.5
  zero-clinical-history class   = borrow nearest validated class matrix, never de novo optimism

regression_penalty:
  active safety reversal        = ×0.5-0.7 (AAV post-Elevidys)
  none                          = ×1.0
```

For a zero-clinical-history modality, **borrow the nearest validated class's transition matrix and apply explicit delivery/CMC/regulatory-novelty haircuts** — never an optimistic de novo estimate. Platform risk concentrates in Phase 1→2.

### Output

```
MODALITY LIFECYCLE READ — [Modality] × [Target tissue]
Date: [assessment date]   |   Mode: [learn / screen]

Maturity stage: [Emerging / Proving / Established / Mature]
  Representative drugs: [examples]
  Lead players: [companies]

Binding delivery bottleneck: [the one constraint gating next stage]
  Current state: [wall standing / partially breached / breached]
  Proof-point trial(s): [NCT# / readout + date]   Source: [ClinicalTrials.gov / preprint]

Platform-fix status: [LANDED / PARTIAL / NOT LANDED]
  The fix: [GalNAc / tLNP / E3-recruitment / capsid / etc.]
  What closes it: [specific pending readout if PARTIAL]

Arc-direction flags:
  Regression: [none / active — describe safety event]
  Maturity/commoditization: [none / reformulation underway — route+cadence competition]

P(modality deliverable): [0.00-1.00]
  = base [%] × delivery_multiplier [x] × regression_penalty [x]
  Borrowed matrix (if zero-history): [nearest validated class + haircuts applied]

Bottom line:
  Clinician read: [where it stands, what unlocks the next tissue]
  Investor read: [deliverable enough to fund? entry attractive or commoditized?]
```

## Error Handling

| Scenario | Response |
|---|---|
| Modality not on the map | Place it by analogy to the nearest mapped class; flag as zero-clinical-history and borrow that class's matrix with novelty haircuts |
| Conflicting stage signals (approval but class regressing) | Maturity stage = approvals shipped; apply regression_penalty separately. Record both — an Established class can still be a bad entry (AAV) |
| Delivery claim only in preprint / NHP | Mark PARTIAL; do not credit as LANDED until a human Ph1 dose-response confirms; name the trial that would close it |
| "AI-discovered" / novel-platform framing | Down-weight unless the platform has independent wet-lab + clinical validation; AI compresses discovery, not Phase 2/3 attrition |
| Tissue not specified | Default to the validated tissue (usually liver for oligo/LNP); flag that extrahepatic asks carry a separate, harder delivery state |
| Single company / single asset = the whole class | Treat as Emerging regardless of hype; one Ph1 asset is not a de-risked modality |

## Cross-Domain Connections

- **manufacturing-ip/modality-manufacturing** (depends_on): The CMC/COGS counterpart — where this skill asks "can it reach the tissue?", that skill asks "can it be made at scale and cost?" Autologous CAR-T COGS ~$100-220K/dose and ex-vivo CRISPR's ~$2.2M price are manufacturing walls that cap an otherwise-deliverable modality. The two terms multiply.
- **mechanism-risk-adjuster** (depends_on): Supplies the modality-deliverability haircut that adjusts a target's base PoS. A genetically-clean target inside a NOT-LANDED modality must be discounted for platform risk, not credited at face value.
- **frontier-discovery/frontier-conviction-scorer**: Primary consumer — this skill emits the **P(modality deliverable)** term in the decomposition P(biology holds) × P(modality deliverable) × arc-position × competitive-timing.
- **frontier-discovery/moa-analog-engine**: Complementary — moa-analog-engine places the *mechanism* on its historical arc; this skill places the *modality*. A candidate needs both reads (KRAS the mechanism × small-molecule the modality).
- **probability-of-success/pos-base-rates**: Shares the modality LOA base rates; this skill is where the qualitative delivery state turns those rates into a program-specific deliverability probability.
- **Dual use**: A clinician-scientist runs this in *learn* mode to understand what gates each modality's next tissue; an investor runs it in *screen* mode to gate early opportunities before a clinical asset exists, then hands off to phase-weighted rNPV once one does.
