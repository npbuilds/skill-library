# Data-Engine Catalog — Extended Reference

Dated, versioned snapshot of the target-discovery data engines the **data-generation-monitor** skill watches (UKB-PPP, deCODE, DepMap, FinnGen, Tabula Sapiens, ChEMBL, Open Targets, PDTO, etc.), with scales/versions and how-to-read notes. Split out of the parent `quick-reference.md` so dataset-version churn (FinnGen R12→R15, UKB-PPP pilot→phase 2) versions cleanly here without touching the skill body.

**Snapshot date:** 2026-07-23. **Coverage window:** 2024–2026 releases as characterized in the parent skill.

**Provenance:** every figure below is tagged.
- `int` = internal consensus estimate carried from the skill's own quick-reference/SKILL prose; no external citation attached.
- `ext✓` = externally verified with a real citation (none in this doc — no VERIFIED FACTS block was supplied).
- `statutory` = stable legal/regulatory constant (none appear in this catalog).

**This entire catalog is tagged `int`.** The scales, versions, and CV figures were transcribed from skill prose, not re-verified against source releases. Treat them as directional until confirmed against the primary release.

## Data-Engine Catalog (`int`)

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

## Version / Release Tracking (`int`)

Fast-moving version pointers pulled out of the catalog for at-a-glance churn tracking. Update the "current" column as new releases land; the "next expected" is the skill's stated cadence.

| Engine | Current pin (2024–2026) | Next expected | Cadence note |
|---|---|---|---|
| UKB-PPP (Olink) | pilot ~2,923 proteins × 54,219; phase 2 ~5,400 × 600k announced Jan 2025 | phase 2 full data release | pilot → phase 2 is the version step to watch |
| deCODE (SomaScan) | 4,907 aptamers × 35,559 → 18,084 pQTLs | — | single major release characterized |
| DepMap (Broad) | 1,865+ cell lines; Oct 2025 +25 screens (pediatric/CNS) | rolling quarterly screen adds | new subtypes = new selective-dependency windows |
| FinnGen | R12 / DF12 (500,348 people, 2,502 endpoints, >21M variants) | R13–R15, annually 2025–27 | annual release train; each seeds pQTL/MR 6–18mo later |
| All of Us | >800k diverse (cross-ancestry) | WGS expansions | cross-ancestry replication engine |
| UK Biobank | ~500k WGS | — | genetics substrate |
| Tabula Sapiens | v2: >1.1M cells, 28+ organs, >400 cell types | future atlas versions | re-score targets on each new atlas |
| ChEMBL | v34 | v35+ | druggability/chemistry reference |
| Open Targets | NAR 2025 release; AZ ~470k exomes gene-burden | annual platform release | integration hub; L2G + Project Score |
| Perturb-seq frontier | Replogle 2022 (~19k genes, >2.5M cells); Perturb-DBiT (bioRxiv 2024); Perturb-Multi/FISH (Cell 2025) | spatial/in-vivo scale-up | spatial/in-vivo is the emerging axis |

## Platform-Precision Notes for Proteomics Engines (`int`)

Measurement-quality caveats that gate how much weight a proteomics hit earns. Carried from the parent haircut rubric because they are engine-intrinsic.

| Platform / risk | Figure | How to read it |
|---|---|---|
| SomaScan precision | CV ~6.8%, ~11k analytes | Higher multiplex, lower CV; epitope/aptamer artifacts are the failure mode |
| Olink HT precision | CV ~35.7%, ~5.4k analytes | Noisier at HT scale; single-platform-only hit → check measurability on the other platform → confidence haircut, mark WATCH |
| Cross-platform concordance | bimodal (r≈0 or r≈0.8) | Agreement is all-or-nothing per protein; a hit on one platform is not automatically portable |

## Source Vintage & Staleness

- **Fastest-staling (quarterly to annual):** FinnGen (R12→R15, annual 2025–27), DepMap (rolling screen adds, e.g. Oct 2025 +25), UKB-PPP (pilot→phase 2 full release). Re-check these columns each quarter; the version pin is the first thing that goes out of date.
- **Medium (annual platform releases):** Open Targets, ChEMBL (v34→v35+), Tabula Sapiens atlas versions, All of Us WGS expansions.
- **Slow (structural methods, multi-year):** the *evidence-type* and *how-to-read* columns — pQTL→MR→coloc logic, Chronos-score interpretation, LoF/GoF variant calls — are method-level and change on a multi-year horizon, not per release.
- **CV / precision figures** are platform-generation-specific; a new Olink or SomaScan panel generation invalidates the numbers in the platform-precision table.
- Because everything here is `int` (transcribed from skill prose, no external citation), any figure should be re-verified against the primary release before it drives a nomination decision. The parent skill scores the *delta in convergence* a release creates, not raw dataset size, so a stale scale number degrades gracefully.

**Usage note.** Serves the parent SKILL `data-generation-monitor` (frontier-intelligence). Read alongside the parent `references/quick-reference.md`, which holds the Orthogonal-Convergence Scoring primitive, the full Haircut/Discount rubric, and the Forward-Signal Translation guidance that consume this catalog. When a new release lands, update the Version/Release Tracking table here first, then re-run the convergence delta in the parent skill.
