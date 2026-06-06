# Data Generation Monitor — Quick Reference

## Input

| Parameter | Source | Required? |
|---|---|---|
| Release / dataset / claim to evaluate | User | Yes |
| Target(s) or therapeutic area | User | Recommended |
| Modality lens | User | Optional |
| Time window | User | Optional (default: latest) |
| Prior convergence baseline | User / prior run | Optional (needed for net-new Δ) |

## Data-Engine Catalog

| Engine | Evidence type | Leading generators (scale, 2024–2026) | How to read the release |
|---|---|---|---|
| **Plasma proteomics × genetics (pQTL→MR→coloc)** | Human causal target nomination + directionality (HIGHEST weight; ~2x approval odds) | **UKB-PPP** Olink: pilot ~2,923 proteins × 54,219 (>14k pQTLs); phase 2 ~5,400 proteins × 600k (announced Jan 2025). **deCODE** SomaScan: 4,907 aptamers × 35,559 → 18,084 pQTLs, **938 candidate drug-target genes** | Count *cis*-pQTL MR hits with colocalization (cis > trans). Record direction (lower→Ab/ASO; raise→replacement). Check druggability + cell-type restriction. |
| **Cancer dependency (DepMap)** | Functional "phenotype depends on gene"; selective dependency = oncology prize | DepMap (Broad): genome-wide CRISPR-KO across **1,865+ cell lines**; Oct 2025 +25 screens incl. pediatric/CNS | Scan *newly selective* dependencies in newly-covered subtypes. Chronos score ~0 none, ~−1 pan-essential. Selective (window) = nominate; pan-essential = too toxic. Pull biomarker correlate. |
| **Perturb-seq (mechanism)** | Full transcriptional signature; pathway membership; upstream of disease signature | Replogle 2022 (CRISPRi, all ~19k genes, >2.5M cells). Frontier: **Perturb-DBiT** (spatial+in-vivo, bioRxiv 2024), **Perturb-Multi/FISH** (Cell 2025). TRADE: typical perturbation shifts ~45 genes, essential >500 | Weight spatial/in-vivo heavily for immuno-onc / microenvironment. Identify targets upstream of disease signature. |
| **Variant screens (SGE / prime / base editing)** | VUS → LoF/GoF call → therapeutic direction + patient stratification | Pooled prime editing (Cell Genomics 2025: SMARCB1, MLH1); SGE (BRCA1 clinical gold standard) | Record which variants resolved LoF vs GoF; sets modality direction and stratification. |
| **Expression context (atlases)** | Cell-type restriction (window) vs broad vital-tissue (tox flag) | **Tabula Sapiens v2**: >1.1M cells, 28+ organs, >400 cell types. Human Cell Atlas; spatial (Visium/Xenium/MERFISH) | Restricted to diseased compartment = green flag; broad in vital tissue = tox flag. Re-score existing targets on each new atlas. |
| **Biobanks / cohorts (genetics substrate)** | GWAS + gene-burden; the genetics half of pQTL/MR | **FinnGen R12/DF12**: 500,348 people, 2,502 endpoints, >21M variants (R13–R15 annually 2025–27). **All of Us** >800k diverse (cross-ancestry). UKB ~500k WGS. MVP, Estonian, BBJ | UPSTREAM signal — seeds pQTL/MR papers 6–18mo later. Look for rare-variant hits replicating borderline cis-pQTL MR. Cross-ancestry replication = de-risk. |
| **Druggability / chemistry** | Is there tractable matter matching the required direction? | **ChEMBL** v34 (bioactivity, IC50/Ki, mechanism, ADMET) | Confirm existing chemistry / tractable modality; match to required direction (lower vs raise). |
| **Patient-derived models (validation)** | Does drugging the target move a human-derived system? | PDTO biobanks: CRC ~80% accuracy (sens 63%, spec 94%); brain IPTO; 399-organoid/144-patient liver biobank. Organoid Perturb-seq (emerging) | DepMap dependency + organoid-confirmed vulnerability = high conviction. |
| **Integration hub** | One target-disease prioritization score across all engines | **Open Targets** (NAR 2025): GWAS Catalog, UKB, FinnGen, gene-burden (AZ ~470k exomes), Project Score, literature, mouse | The practical "where to read the convergence" tool; use L2G + Project Score. |

## Orthogonal-Convergence Scoring Primitive

```
PER-TARGET CONVERGENCE SCORE

Engine                          Present?   Weight   Modifier
─────────────────────────────────────────────────────────────────
[1] cis-pQTL + MR + coloc        [Y/N]      3        cross-ancestry replicated → +1
[2] Selective DepMap dependency  [Y/N]      2        must be selective, not pan-essential
[3] Clean Perturb-seq signature  [Y/N]      2        in vivo / spatial → +1
[4] Variant-resolved LoF/GoF     [Y/N]      1        sets therapeutic direction
[5] Druggable in ChEMBL          [Y/N]      2        must match required direction
[6] Cell-type-restricted         [Y/N]      1        restricted = window; broad-in-vital → −1 (tox)
[7] Organoid / in-vivo validated [Y/N]      1
─────────────────────────────────────────────────────────────────
RAW CONVERGENCE = count of independent engines (Y)
WEIGHTED        = Σ (weight × present)
NET-NEW Δ       = engines THIS release adds vs prior baseline

CONVICTION TIERS
  ≥4 engines incl. [1] genetics → HIGH (nominate)
  2–3 engines, genetics present → WATCH (needs one more orthogonal line)
  1 engine only                 → SINGLE-SOURCE (artifact risk — do NOT nominate)

The skill computes the DELTA in convergence a release creates, not raw dataset size.
Exemplar HIGH target: cis-pQTL+MR hit that is ALSO selective DepMap dependency
AND clean Perturb-seq signature AND druggable in ChEMBL AND cell-type-restricted.
```

## Haircut / Discount Rubric

| Risk | Trigger | Action |
|---|---|---|
| **Platform precision** | SomaScan (CV ~6.8%, 11k) vs Olink HT (CV ~35.7%, 5.4k); cross-platform bimodal (r≈0 / r≈0.8) | Single-platform-only hit → check measurability on other platform → confidence haircut, mark WATCH |
| **trans-pQTL** | MR signal is trans-only | Do not nominate; causally ambiguous |
| **Ancestry** | EUR/Finnish-only (UKB/FinnGen) | Flag ancestry-specific-artifact risk; require All of Us / cross-ancestry replication |
| **Cell-line generalization** | DepMap/Perturb-seq hit, no primary-tissue confirmation | Organoid/in-vivo upgrades; absence = caveat not kill |
| **AI-discovery** | "AI-discovered" claim | Weight by funnel position: design (credible, e.g. Chai-2 ~16% Ab hits) vs novel target-ID (discount — usually already literature-implicated). AI moves Ph1 (~80–90%) not Ph2 (~40%). Demand wet-lab/clinical validation. |
| **Virtual-cell** | "virtual cell will design drugs" | Discount to 5–10yr bet; unseen-perturbation prediction unsolved (Virtual Cell Challenge) |

## Forward-Signal Translation

- **Upstream releases** (biobank: FinnGen R13, UKB-PPP ph2, All of Us WGS) → seed pQTL/MR target papers **6–18 months** later. Release date = leading indicator; cross-ancestry replication = de-risk event.
- **Translation ground truth**: first IND/Phase-1 on ClinicalTrials.gov. Literature-inflection → FIH gap is typically **3–7 years** for a novel target (the realized lead time).
- **Established vs emerging vs hyped (2026):**
  - Established: pQTL+MR nomination; DepMap selective dependencies; genome-scale CRISPRi Perturb-seq; SGE clinical variant calls; PDTO drug-response (CRC/liver).
  - Emerging: spatial/in-vivo Perturb-seq; pooled prime-editing screens; Olink↔SomaScan harmonization; optical pooled morphology screens; organoid Perturb-seq.
  - Hyped: SomaScan epitope artifacts / Olink HT noise; trans-pQTL causal claims; cell-line→patient generalization; AI "virtual cell" prospective target nomination.
