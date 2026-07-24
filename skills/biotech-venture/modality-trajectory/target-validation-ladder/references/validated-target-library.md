# Validated Target Library — Extended Reference

A corpus of real drug targets graded by human-genetics evidence and matched against clinical outcome — the grading-by-analogy corpus for `target-validation-ladder` (structural analog of `moa-analog-engine`'s `moa-arc-library.md`). Grade a new target by finding its nearest analog here. Every row is primary-sourced and adversarially verified.

## Ladder Calibration — Why Tier Beats a Flat Multiplier

Human genetic support raises probability of success, but **not uniformly** — the multiplier is tier-dependent, which is the entire justification for a ladder rather than a flat 2×.

| Evidence tier | Relative success / odds ratio | Source |
|---|---|---|
| Any genetic support (aggregate) | **2.6× PoS** (refined up from Nelson 2015's "2×") | Minikel et al. 2024, Nature (s41586-024-07316-0) |
| Mendelian / OMIM | **RS = 3.7** (highest) | Minikel 2024 |
| All evidence sources | RS > 2 for *every* source examined | Minikel 2024 |
| Mendelian + GWAS-linked-to-coding | > 2× approval, holds prospectively | King et al. 2019, PLOS Genetics (pgen.1008489) |
| Common-variant (noncoding) GWAS | Smaller, often **not distinguishable from zero** | King 2019 |

Dose-response as confidence tightens (Open Targets genetic-association score): **>0 → OR 3.25; >0.5 → OR 4.47; >0.8 → OR 5.06**. Confidence in *causal-gene assignment* is what drives the tier — Mendelian/coding-LoF assigns the gene cleanly; noncoding GWAS does not.

> The multiplier is a portfolio **base-rate enrichment**, not a per-program guarantee. A Tier-1 target can still fail on trial execution, dose, or a divergence like LRRK2 (below).

## Cardiovascular / Lipid — Genetics and Clinic Converge Cleanly

| Target | Genetic evidence | Effect | Drug / outcome | Tier |
|---|---|---|---|---|
| **PCSK9** | Allelic series + MR (LoF protective, GoF harmful) | OR 0.81 per 10 mg/dL LDL (MR, n=112,772) | evolocumab / alirocumab / inclisiran — **approved** | 1 |
| **HMGCR** (statin target) | MR, coding/regulatory variants | OR 0.81 per 10 mg/dL LDL | statins — **approved** (archetype) | 1 |
| **NPC1L1** | Rare inactivating LoF (nonsense/splice/frameshift) | OR 0.47 (53% ↓ CHD), ~12 mg/dL ↓ LDL | ezetimibe — **approved**, IMPROVE-IT positive | 1 |
| **ASGR1** | Rare LoF del12 haploinsufficiency (1 in 120) | 34% ↓ CAD (CI 21–45), 15.3 mg/dL ↓ non-HDL | AMG 529 — **early-stage**, no drug yet | 2 |
| **APOC3** | MR (LoF protective) | OR ~0.83–0.90 CAD; benefit via remnant cholesterol | olezarsen and antisense — **advancing** | 2 |
| **ANGPTL4** | LoF E40K | OR 0.57 CAD | early programs | 2 |
| **ANGPTL3** | Split signal | Common variants **not** CAD-associated; **PTVs** protective via TG (OR 0.42/mmol/L) | evinacumab (HoFH) — nuance matters for tiering | 2 |
| **LPA / Lp(a)** | MR — directional causal | OR 0.942 per 10 mg/dL; **low per-mg/dL potency** (~100 mg/dL absolute drop needed) | pelacarsen / olpasiran — **pending** event trials | 2 |

Sources: Ference NEJM 2016 (NEJMoa1604304); Stitziel NEJM 2014 (NPC1L1, NEJMoa1405386); Nioi NEJM 2016 (ASGR1, NEJMoa1508419); Burgess/Lp(a) MR (PMID 29926099); APOC3/ANGPTL MR (EHJ Open oeae035, PMC11951255).

## Immunology

| Target | Genetic evidence | Effect | Drug / outcome | Tier |
|---|---|---|---|---|
| **TYK2** | Coding partial-LoF MR (P1104A, rs34536443) | Protective across autoimmune: psoriasis OR 0.79, RA 0.73, T1D 0.77, UC 0.83, PBC 0.46 | deucravacitinib (Sotyktu) — **approved** (psoriasis) | 1 |
| **TL1A / TNFSF15** | GWAS risk locus + prospective genetic CDx | Phase 2 UC remission 26% vs 1% placebo (n=135) | tulisokibart — **Phase 2 positive** (later-stage status not independently verified here) | 2 |
| **IL6R** | *Not yet researched* (Asp358Ala/rs2228145 MR signal + tocilizumab) | — | — | pending |

Sources: TYK2 MR (PMC9988426); tulisokibart ARTEMIS-UC (NEJMoa2314076).

## Neurology — Directional Complexity & a Divergence Watch

| Target | Genetic evidence | Effect | Drug / outcome | Tier |
|---|---|---|---|---|
| **TREM2** | Rare coding **LoF** R47H (risk allele) | Pooled OR 3.88 AD risk; ↓ soluble TREM2 | **Direction inverted** — LoF is *harmful*, so therapeutics pursue TREM2 **agonism** (AL002/AL044, pending) | 2 |
| **LRRK2** | **Gain-of-function** Mendelian (G2019S, kinase-hyperactivating) | Rational target for **inhibition** | BIIB122/DNL151 kinase inhibitor — **⚠ possible divergence** | 2 |

Sources: TREM2 R47H meta-analysis (PMC7903442); LRRK2 BIIB122 (Mov Disord, mds.29297).

> **Divergence watch — LRRK2.** Genetics is strong and the modality (kinase inhibition) is mechanistically rational, but a verifier flagged a **May 2026 Phase 2b LUMA failure and terminated Phase 3 LIGHTHOUSE** for BIIB122 — a potential "genetics-strong / clinical-disappointing" divergence. **This was not confirmable from the surviving verified claim set — treat as a flag to run down against primary sources, not an established fact.** It is exactly the kind of case the ladder must be able to represent: strong target validation does not immunize a program against clinical failure.
>
> **Directional lesson — TREM2.** The clean "LoF-protective → inhibit the target" logic (PCSK9/NPC1L1/ASGR1/TYK2) **inverts** when the LoF allele is *harmful*: TREM2 loss raises AD risk, so the drug direction is agonism. Always read the *direction* of the genetic effect before assuming the modality.

## Pending Targets (uncovered — do not treat absence as evidence)

The following were requested but produced no verified rows; they are **unresearched**, not disproven: **IL6R, GPR75 (obesity LoF), INHBE (metabolic LoF), PNPLA3 (MASH I148M), APOB, GLP1R**. A follow-up pass should grade each on the same axes (evidence type → effect direction → drug outcome), flagging divergences.

## Source Vintage & Staleness

The genetics literature is stable (Mendelian variants don't change); **the drug-outcome column is the perishable part** — re-check clinical status (especially pending/early-stage and the LRRK2 flag) before a memo. Headline multiplier lineage: Nelson 2015 → King 2019 → Minikel 2024, a self-consistent same-group refinement; cite the 2.6× / RS-by-source (2024) as current and "2×" as the historical origin.

**Usage note.** This corpus feeds `target-validation-ladder/SKILL.md` (grade a candidate by its nearest analog here) and is the shared genetic-evidence source for `probability-of-success/mechanism-risk-adjuster` — reference it rather than duplicating rows. The tier a target lands on should reflect *both* genetic strength (causal-gene confidence) and how far the clinical program has confirmed the thesis.
