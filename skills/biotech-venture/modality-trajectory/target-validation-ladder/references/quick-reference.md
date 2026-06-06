# Target Validation Ladder — Quick Reference

The gradeable human-genetics rubric. Causality and direction-of-effect concordance are the load-bearing variables; predictive power is **flat across effect size, MAF, and discovery year** (Minikel 2024), so rank evidence by *causal-gene confidence*, not by p-value.

## Input

| Parameter | Source | Required? |
|---|---|---|
| Target gene (HGNC symbol) | User | Yes |
| Indication / disease | User | Yes |
| Intended mechanism direction (inhibit / degrade / agonize / replace) | User | Recommended |
| Intended modality | User | Recommended (default: score all) |
| Ancestry / cohort caveats | User | Optional |

## Anchor numbers (cite these)

| Claim | Value | Source |
|---|---|---|
| Relative success with genetic support | **~2.6x** (was ~2x) | Minikel/Nelson, *Nature* 629:624, 2024 |
| Supported-mechanism fraction, preclinical → approved | **2.0% → 8.2%** | Nelson, *Nat Genet* 47:856, 2015 |
| GPS top 0.28% → odds of valid indication | **~9.9x** | Duffy/Do, *Nat Genet* 56:51, 2024 |
| GPS top-bin phase advancement I→II / III / IV | **1.7 / 3.7 / 8.8x** | Duffy/Do 2024 |
| Genes with tolerated two-hit pLoF (human KO) | **~3,421 (18%)** | Minikel, *Nature* 581:459, 2020 |
| Side-effect risk if resembles genetically-assoc. trait | **~2x** | Duffy/Minikel/Nelson, *PLOS Genet* 2025 |
| Open Targets L2G | 0-1, 51 features, 92-tissue QTL coloc, Shapley | Ghoussaini, *NAR* 49:D1311 |
| gnomAD scale | v2 141,456 / v4 ~807,000 | Karczewski, *Nature* 581:434 |
| Biobank scale | FinnGen ~454k/2,447 endpoints; UKB WES 392,814; UKB+FinnGen meta n=653,219/744 endpoints; MVP/UKB/FinnGen >1M | FinnGen / Sun et al. |

## Evidence-tier table (the ladder — TIER | WHAT IT IS | WEIGHT | FAILURE MODE)

| Tier | What it is | Weight (Axis 1) | Characteristic failure mode |
|---|---|---|---|
| **A — Mendelian / rare-variant burden** | Monogenic disease or gene-collapsing LoF/missense burden test; the variant *is* the gene | **4** | Rare; ascertainment toward well-studied genes; absence ≠ evidence against |
| **B — Coding GWAS + colocalization** | Coding lead/credible-set variant OR coloc posterior >0.8 / L2G >0.5; pins causal gene | **3** | Coloc in wrong tissue; QTL ≠ disease-relevant cell type |
| **C — cis-MR (colocalized, robust)** | Cis instruments mimic pharmacological perturbation; gives direction | **2** | Horizontal pleiotropy, LD confounding, wrong/tissue-discordant direction — *only counts if cis + colocalized* |
| **D — Non-coding GWAS, nearest-gene only** | Association with no coding variant, no coloc | **1** | **#1 failure: wrong gene at the locus** (~90% of GWAS hits non-coding) |
| **— None** | No human genetic association | **0** | No prior; 2.6x lift unavailable |

Orthogonal amplifiers (separate axes, beside the ladder):
- **Allelic series / dose-response** (Axis 3): null→partial→GoF monotonic gradient = gold standard; predicts efficacy-curve shape. *PCSK9 paradigm.*
- **Human knockouts** (Axis 4): healthy homozygous LoF ⇒ full inhibition tolerated.

## Six-axis scoring rubric (composite 0-13)

| Axis | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **1. Causal-gene confidence** | No assoc. | Non-coding, nearest-gene, no coloc | cis-MR sig. + colocalized, pleiotropy-robust | Coding lead variant OR coloc >0.8 / L2G >0.5 | Mendelian OR rare-variant burden |
| **2. Direction concordance** | Unknown OR discordant | Inferable, not confirmed | Established (allelic series / LoF-GoF) AND concordant with mechanism | — | — |
| **3. Allelic series / dose-response** | Single variant | ≥2 variants, partial gradient | Graded series, monotonic dose-response | — | — |
| **4. Safety read-across** | Constrained gene + adverse pleiotropy | Mixed / limited | Healthy human KOs AND clean PheWAS | — | — |
| **5. Tractability (per modality)** | No tractable handle | Druggable family / structural plausibility | Clinical precedence or strong pocket/epitope (OT buckets 1–4) | — | — |
| **6. Replication / generalizability** | Single cohort | Replicated ≥2 biobanks/ancestries | — | — | — |

## Composite → tier

| Composite | Tier | Read |
|---|---|---|
| **11–13** | Tier 1 — de-risked | PCSK9-class; genetics ~maximally predictive; expect top-bin RS multiplier |
| **8–10** | Tier 2 — strong | Solid causal gene + direction; minor gaps (tractability or replication) |
| **5–7** | Tier 3 — emerging | Real signal, one load-bearing weakness (usually direction or causal-gene ambiguity); needs orthogonal work |
| **2–4** | Tier 4 — hypothesis | Association-grade only; treat as unvalidated |
| **0–1** | Tier 5 — none | No human genetic prior |

## Hard gates (override the composite)

- Discordant direction of effect → **cap at Tier 3** regardless of other axes.
- Non-coding-only with no coloc → **cap causal confidence (Axis 1) at 1**.
- Intractable in *all* plausible modalities → **flag undevelopable** even if genetically pristine.

## Failure-mode checklist (subtract before scoring)

| Failure mode | Mitigation |
|---|---|
| Wrong gene at locus | Require coding variant or coloc/L2G > threshold |
| Wrong direction of effect | Steiger filtering, allelic series, explicit direction statement |
| Horizontal pleiotropy (MR) | cis-only instruments, colocalization, MR-Egger / CAUSE, multiple methods |
| LD / cross-ancestry confounding | Matched-ancestry colocalization |
| Tissue-discordant QTLs | Use disease-relevant tissue |
| Reverse causation | Confirm trait doesn't cause the molecular phenotype |
| Indication mismatch | Genetic support for trait X vs. program targeting Y |
| Mechanism mismatch | Variant may model one isoform/domain only |

## Modality tractability buckets (Axis 5, grade per modality)

- **Small molecule (8):** approved SM → Ph2/3 → Ph1 → co-crystal w/ ligand → high-quality ligand (PFI ≤7) → DrugEBIlity pocket ≥0.7 → DrugEBIlity 0–0.7 → druggable-genome family.
- **Antibody:** clinical precedence → membrane/secreted localization → predicted signal peptide/TM → HPA membrane evidence.
- **PROTAC:** clinical precedence → literature → ubiquitination sites → protein half-life → ChEMBL binder ≤10 µM.
- **Oligo / gene therapy:** escape hatch for high-genetic-confidence / low-classical-tractability targets (e.g., *LPA* siRNA).

## Data sources to query

Open Targets Platform (genetics-only weighting) · Open Targets Genetics / Gentropy (L2G, coloc, Shapley) · Genetic Priority Score portal (Mount Sinai/Do) · gnomAD v2/v4 (pLI, LOEUF, human-KO catalog) · OMIM / ClinVar (Tier A) · GWAS Catalog · ChEMBL v34 (tractability, bioactivity) · ClinicalTrials.gov v2 (pipeline/phase per target) · PubMed + Consensus (MR methodology, genetic-support claims) · bioRxiv/medRxiv (biobank target-discovery preprints) · UK Biobank / FinnGen / All of Us / MVP (burden tests, cis-MR, PheWAS).

## Worked grading example — PCSK9 (LDL-C lowering / cardiovascular)

Intended mechanism: **inhibit** (small molecule, antibody, siRNA all relevant).

| Axis | Evidence | Score |
|---|---|---|
| 1. Causal-gene confidence | GoF causes autosomal-dominant hypercholesterolemia; LoF allelic series — Tier A | **4** |
| 2. Direction concordance | Heterozygous LoF carriers ~28% lower LDL-C, ~88% lifetime CHD reduction (Cohen 2006); LoF protective ⇒ inhibit — concordant | **2** |
| 3. Allelic series | Full LoF nonsense → ~28% drop; partial variants intermediate; monotonic | **2** |
| 4. Safety read-across | Healthy living compound-het knockout woman de-risks complete inhibition; clean phenome | **2** |
| 5. Tractability | Approved antibodies (evolocumab/alirocumab) + siRNA (inclisiran) + oral in development — OT bucket 1 | **2** |
| 6. Replication | Replicated across multiple ancestries (original LoF in African-American cohort + European) | **1** |

**Composite: 13 / 13 → Tier 1 (de-risked).** No hard gates tripped; no failure-mode flags. The healthy human knockout is what converts "inhibit PCSK9" from a hypothesis into a near-certainty of on-target tolerability — this is why PCSK9 went gene→approval in ~12 years, the speed champion. **Hand-forward to mechanism-risk-adjuster:** Tier 1, direction-concordant Y, safety flag clean, implied ~2.6x (top-bin) relative-success multiplier.

## Counter-example — generic non-coding GWAS hit

A locus reaches genome-wide significance for the indication; the lead variant is intergenic, no coding variant in the credible set, no QTL colocalization run, direction unknown. Axis 1 = 1 (hard gate: non-coding-only caps it), Axis 2 = 0 (direction unknown → caps composite at Tier 3), Axes 3–6 thin. **Composite ~2–3 → Tier 4 (hypothesis), and even a generous read is gated to Tier 3.** The brief's warning applies: this is the most common "genetically supported" target that fails — the wrong gene at the locus was credited.
