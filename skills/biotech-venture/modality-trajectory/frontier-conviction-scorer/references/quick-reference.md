# Frontier Conviction Scorer — Quick Reference

Dense, scannable base-rate tables, the score-decomposition worksheet, and the rNPV handoff trigger. Anchor every claim; never quote a generic "~10% PoS."

## The core formula

```
TRAJECTORY CONVICTION = P(biology holds) × P(modality deliverable) × position-on-arc × competitive-timing
                        [0–1]            [0–1]                     [0–1]            [0–1]
Ordinal & relative. Ranks programs, localizes binding risk. NOT a cash-flow estimate.
```

## Convention first (fix one, label it)

| Convention | Overall LOA from P1 | Use for |
|---|---|---|
| CDP / program-indication (BIO/Informa/QLS) | **~7.9%** (2011–2020); ~5% (2015–2023) | A specific target-indication pair — **default** |
| Molecule (ME) (Wong/Lo, DiMasi) | ~13.8% | A molecule across all indications; runs ~2x CDP |

Never mix. ME ≈ 2x CDP.

## Phase-transition base rates (the kill-zone map)

| Transition | BIO 2011–2020 | 2015–2023 | rNPV handoff band |
|---|---|---|---|
| Phase 1 → 2 | ~52% | ~50% | 50–65% |
| **Phase 2 → 3** | **~28.9%** | **~28%** | **25–35% (KILL ZONE)** |
| Phase 3 → NDA/BLA | ~57.8% | ~53% | 50–60% |
| NDA/BLA → Approval | ~90.6% | high | 85–90% |
| Preclinical → P1 | — | — | 40–50% |
| **Cumulative P1 → approval** | **7.9%** | **~5%** | 7–12% |

Discount rate: 15–20% early-stage biotech (10–15% mid-cap, 8–10% large pharma). Phase 2 is where biology gets falsified — spend the marginal diligence dollar on PoM/dose/endpoint risk.

## Modality LOAs (from Phase 1, CDP)

| Modality | LOA | Note |
|---|---|---|
| Vaccine | 9.7% | highest |
| Biologic (mAb) | 9.1% | antibody programs ~9%+ |
| Small molecule (NME) | 5.7% | baseline |
| CGT (all) | 5.3% | **bimodal — do NOT use blend** |
| — CAR-T | 13.6% | front-loaded; P3→sub 90% |
| — AAV gene therapy | 13.6% | front-loaded; *can regress* (Elevidys) |
| — Ex vivo / In vivo GT | 5.9% / 4.4% | |
| ASO / siRNA | no clean LOA | borrow biologic back-end + delivery haircut |

**CGT rule:** durable rare/inherited CGT shows P2/3 success 68–75%, submission→approval 81–90% — risk concentrated EARLY (delivery/CMC/dose). Weight P1→2 heavily, back end lightly. Opposite of SM oncology.

## Therapeutic-area spread (>5x)

| Area | LOA from P1 |
|---|---|
| Hematology | ~26% (highest) |
| Cardiovascular / metabolic / infectious | mid-teens–low 20s |
| CNS / neurology / psychiatry | ~7–8% (structurally hard) |
| Oncology | ~5% (lowest; Wong/Lo 3.4%) |
| Ophthalmology / vaccines (Wong/Lo) | ~33% |

## Discovery-stage levers (what moves the base rate)

| Lever | Effect | Stacking rule |
|---|---|---|
| Human genetic support | **2.6x** (Minikel/Nelson 2024; 2.0x Nelson 2015) | grade by causal-gene CONFIDENCE, not effect size/allele freq; apply to P(biology) |
| Biomarker selection | **25.9% vs 8.4% (~3x)**; P3 76.5% vs 55.0% | strongest *design* lever; apply once |
| Orphan / rare | ~17% LOA; CGT orphan 9.4% vs 3.2%; approval 46% vs 34% (OR 2.3) | partly selection — don't double-count w/ biomarker |
| Expedited (BTD/Fast Track) | elevated transitions | confirmatory tier-bump only, NOT a stackable multiplier |

Key: genetic support de-risks BIOLOGY, not platform. The 2.6x is independent of effect size, allele frequency, discovery year.

## Position-on-arc gate (cumulative survival to date)

| Stage | Unconditional P(approval) |
|---|---|
| Lead-opt (no IND) | ~0.4–1% (screen→candidate 0.1–1%; preclinical stage success ~10.5%; ~1 in 250) |
| IND-enabling / ready | ~10% |
| Phase 1 cleared | class P1→approval LOA (e.g. onc ~5%, heme ~26%) |

## Zero-clinical-history modality procedure

```
1. Borrow nearest validated class transition matrix as prior.
   covalent SM → SM | viral vector → AAV 13.6% front-loaded
   novel-conjugate oligo → ASO/biologic blend | engineered cell → CAR-T
2. Split risk: biology (genetic/biomarker) vs modality (delivery/CMC). Keep ORTHOGONAL.
3. Haircut the analog's EARLY transitions (concentrate on P1→2) for:
   (a) unproven delivery/biodistribution  (b) CMC novelty
   (c) regulatory pathway novelty         (d) unknown chronic tolerability
4. De-risking inflection: platform risk collapses at FIRST human PoC on the platform.
5. NEVER a de novo optimistic number. "This time is different" is the failure mode.
6. AI-discovered? down-weight unless AI acted in molecular DESIGN w/ independent wet-lab/clinical validation.
   AI does not move P2/3 attrition.
```

## Score-decomposition worksheet

```
P(biology holds):        ___   genetic rung (causal-gene confidence) | biomarker | orthogonal convergence
                               0.8–1.0 confident causal gene + biomarker
                               0.4–0.6 moderate association, plausible mechanism
                               0.1–0.3 phenotypic hit, no genetic anchor
P(modality deliverable): ___   nearest validated class LOA | delivery unlock landed? | haircuts
                               0.8–1.0 only if prior human PoC on platform
position-on-arc:         ___   stage gate above × arc phase (moa-analog-engine)
competitive-timing:      ___   order-of-entry | IP runway | SoC drift | crowding
                       --------
COMPOSITE = product       ___   (ordinal — rank, don't price)

BINDING RISK = the lowest factor → that's what to diligence next.
```

## rNPV handoff trigger

```
IF (clinical asset exists) AND (lead indication defined):
    RETIRE trajectory score.
    HAND OFF → asset-valuation/rnpv-modeler + probability-of-success/pos-calculator
    APPLY phase-weighted PoS ladder (above) × peak-sales model, discount 15–20%.
    ADJUST each base PoS for area/modality/genetic/biomarker/orphan levers (no double-count).
ELSE:
    STAY ordinal. Trajectory score decides WHAT to advance; rNPV decides WHAT IT'S WORTH.
```

## Error handling

| Scenario | Response |
|---|---|
| Generic "~10% PoS" | Replace with area+modality CDP rate; P1 oncology ~5%, not 10% |
| CDP/ME mixed | Fix one (default CDP); ME ≈ 2x → double-counts |
| No clinical history | Step 4: borrow class matrix, haircut P1→2; never de novo optimism |
| CGT 5.3% on CAR-T/AAV | Use 13.6% bimodal sub-rate, front-loaded risk |
| Genetics → justify platform | Reject; genetics de-risks biology only |
| Designations stacked | Dominant lever only; confirmatory bump, not multiplier |
| Clinical asset + indication exist | Retire score; trigger rNPV handoff |
| "AI-discovered" de-risking claim | Down-weight unless molecular design + independent validation |

## Sources

BIO/Informa/QLS 2011–2020 (9,704 programs); Wong/Siah/Lo Biostatistics 2019 (185,994 trials); Minikel/Nelson *Nature* 2024 (genetic support 2.6x); Nelson *Nat Genet* 2015 (2.0x); CGT Trajectory PMC12447590 2023; Dynamic success rates PMC12572394 2024; rNPV ladder Vision Lifesciences 2026.
