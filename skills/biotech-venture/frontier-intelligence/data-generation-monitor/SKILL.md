---
name: data-generation-monitor
description: >
  Read each new functional-genomics data-engine release as a forward signal of pre-validated
  drug targets. Tracks pQTL/MR/colocalization atlases (UKB-PPP, deCODE), DepMap dependency
  updates, genome-scale and spatial Perturb-seq, prime-editing/SGE variant screens, optical
  pooled screens, biobank releases (FinnGen, All of Us, MVP), and organoid biobanks. Activate
  when a new dataset, atlas, or AI-discovery claim drops and you need to know which targets just
  gained orthogonal causal support — for a scientist learning the field or an investor screening
  early opportunities.
metadata:
  author: nirav
  version: "1.0"
  parent: frontier-intelligence
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Data Generation Monitor — Reading Data Engines as a Pipeline of Pre-Validated Targets

Target discovery has shifted from hypothesis-first biology to **data-engine-first triangulation**. A modern target is "real" not when one assay points at it but when several independent engines — human genetics, functional perturbation, cancer dependency, expression context, and chemistry — converge on the same gene. The single most consequential 2024–2026 development is that plasma proteomics fused with human genetics (cis-pQTL → Mendelian randomization → colocalization) has become the dominant causal-target-nomination machine, because it most closely mimics a randomized trial of a drug acting on a druggable protein. Open Targets quantifies the payoff: a target with human genetic support for its disease is **~2x more likely to win approval**.

The core insight this skill encodes: **a new data-engine release is not "more data" — it is a fresh batch of pre-validated targets.** When UKB-PPP phase 2 adds 2,400 proteins, or DepMap adds 25 genome-wide screens, or FinnGen R13 releases, the analytically useful question is never "how big is this dataset" but **"how many net-new *orthogonal convergences* does it create?"** A protein only matters where it is *also* a selective dependency, *also* druggable, *also* cell-type-restricted. The skill's job is to compute the delta in convergence, not to catalog raw data.

The discipline cuts both ways. The same release can be inflated by platform noise (Olink Explore HT median CV ~35.7% vs SomaScan 11k ~6.8% — platform choice changes which targets even get nominated) and by AI-discovery hype (AI compresses *design*, not Phase 2/3 biology). This skill nominates targets *and* applies the haircuts that separate a durable convergence from an artifact.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Release / dataset / claim to evaluate | User (e.g. "UKB-PPP phase 2", "the new DepMap drop", "Insilico's TNIK paper") | Yes |
| Target(s) or therapeutic area of interest | User | Recommended (else scan the whole release) |
| Modality lens (small molecule, antibody, ASO/siRNA, degrader, gene therapy) | User | Optional |
| Time window (e.g. "releases since Q1 2026") | User | Optional (default: latest release) |
| Prior convergence baseline (what was already known) | User or prior run | Optional — needed to compute *net-new* delta |

### Steps

#### Step 1 — Classify the Engine and the Evidence It Produces

Identify which engine the release belongs to, because each produces a *different kind* of evidence and sits at a different weight in the convergence stack. Map the release to the engine catalog (see `references/quick-reference.md` for the full table):

- **Human genetic causal** (pQTL+MR+coloc atlases: UKB-PPP, deCODE; biobank GWAS/gene-burden: FinnGen, All of Us, MVP) — highest weight; the ~2x approval-odds evidence.
- **Functional dependency** (DepMap CRISPR KO; CRISPRi/a screens) — causal "this phenotype depends on this gene"; selective dependency is the oncology prize.
- **Mechanism / pathway** (genome-scale & spatial Perturb-seq: Replogle, Perturb-DBiT/Multi/FISH) — transcriptional signature, pathway membership.
- **Variant resolution** (SGE, pooled prime-editing, base-editing screens) — turns VUS into LoF/GoF calls → therapeutic direction.
- **Expression context** (Tabula Sapiens / Human Cell Atlas, spatial) — cell-type restriction (window) vs broad vital-tissue expression (tox flag).
- **Druggability / chemistry** (ChEMBL bioactivity, tractable modality) — is there matter, and does it match the required direction?
- **Model validation** (patient-derived organoid biobanks; organoid Perturb-seq) — does drugging the target move a human-derived system?

#### Step 2 — Extract the Candidate Targets from the Release

Pull the gene-level nominations the release actually makes. For each engine type:

- **pQTL/MR releases** — query the source (UKB-PPP, deCODE) or the paper for *cis*-pQTL MR hits with colocalization. Prioritize **cis over trans** (cis = direct genetic perturbation of the protein's own dose; trans is causally ambiguous, often mediated). Record directionality (lower vs raise the protein — this dictates modality). Example outputs to expect: CAVD targets ANGPTL4, ITGAV, PCSK9, FURIN; sepsis targets CD33, LY9.
- **DepMap releases** — scan for *newly selective* dependencies in subtypes that just gained cell-line coverage. Use gene-effect (Chronos) score: ~0 = no effect, ~ −1 ≈ pan-essential. Selective = strongly negative in one subtype, near-zero elsewhere (the therapeutic window); pan-essential = usually too toxic. Pull the biomarker association (mutation/expression correlate) for patient selection. Query the DepMap portal or Open Targets Project Score.
- **Perturb-seq releases** — identify which targets sit upstream of a disease-relevant transcriptional signature; weight spatial/in-vivo (Perturb-DBiT) heavily for immuno-oncology / microenvironment targets.
- **Variant screens (SGE/prime)** — record which variants resolved to LoF vs GoF (sets therapeutic direction and patient stratification).
- **Biobank releases** — treat as *upstream*: a FinnGen R13 or All of Us WGS release seeds a wave of pQTL/MR papers 6–18 months later. Look for rare-variant hits that *replicate* a borderline cis-pQTL MR signal.

Use the source-specific MCP/data tools where available: **bioRxiv/medRxiv** (methods frontier, preprints), **ClinicalTrials.gov** (downstream IND/Phase-1 entries for nominated targets — the translation-event ground truth), **ChEMBL** (druggability/bioactivity), **PubMed/Consensus** (peer-reviewed validation and evidence maturity), **Open Targets** (the integration hub — aggregates GWAS Catalog, UKB, FinnGen, gene-burden on ~470k exomes, Project Score, literature into one prioritization score).

#### Step 3 — Score Net-New Orthogonal Convergences (the core primitive)

For each candidate target, count how many *independent* engines now point at it. **The convergence count is the conviction increment.** A target gains real conviction when independent lines stack — and the release's value is the *delta* it adds, not the absolute count.

```
ORTHOGONAL CONVERGENCE SCORE — per target

Engine                          Present?   Weight   Notes
─────────────────────────────────────────────────────────────────
[1] cis-pQTL + MR + coloc        [Y/N]      3        replicated cross-ancestry = +1
[2] Selective DepMap dependency  [Y/N]      2        selective (not pan-essential)
[3] Clean Perturb-seq signature  [Y/N]      2        in vivo/spatial = +1
[4] Variant-resolved LoF/GoF     [Y/N]      1        sets therapeutic direction
[5] Druggable in ChEMBL          [Y/N]      2        matches required direction
[6] Cell-type-restricted         [Y/N]      1        Tabula Sapiens: restricted = window
     (broad in vital tissue)                          → flip to −1 (tox flag)
[7] Organoid / in-vivo validated [Y/N]      1
─────────────────────────────────────────────────────────────────
RAW CONVERGENCE  = count of independent engines (Y)
WEIGHTED SCORE   = Σ (weight × present)
NET-NEW DELTA    = engines this release ADDS that were not present before

Conviction read:
  ≥4 independent engines, including [1] genetics → HIGH-conviction nomination
  2–3 engines, genetics present                  → WATCH (needs one more orthogonal line)
  1 engine only                                  → SINGLE-SOURCE (artifact risk — do not nominate)
```

The exemplar high-conviction target: a cis-pQTL+MR causal hit that is **also** a selective DepMap dependency **and** has a clean Perturb-seq signature **and** is druggable in ChEMBL **and** is cell-type-restricted in Tabula Sapiens. PCSK9 is the canonical realized case; GPR75 / INHBE / ACVR1C are current genetics-first obesity examples climbing this stack.

#### Step 4 — Apply the Platform-Precision and Anti-Hype Haircuts

A convergence is only as good as the assays underneath it. Discount before nominating:

- **Platform precision (pQTL)** — SomaScan (aptamer, ~11k proteins, median CV ~6.8%) vs Olink Explore HT (PEA antibody, ~5,400 proteins, median CV ~35.7%); cross-platform agreement is **bimodal** (peaks at r≈0 and r≈0.8). A target nominated on one platform should be checked for whether it is even *measurable* on the other. Aptamer hits can be epitope/binding artifacts; antibody hits can be noise below LOD. Single-platform-only hits get a confidence haircut.
- **trans-pQTL** — causally ambiguous; never nominate on a trans-only MR signal.
- **Ancestry** — UKB/FinnGen are European/Finnish-skewed; a nomination that has *not* replicated in All of Us or a cross-ancestry cohort carries an "ancestry-specific artifact" risk flag.
- **Cell-line generalization** — DepMap/cell-line Perturb-seq hits may not transfer to primary patient tissue; an organoid or in-vivo Perturb-seq confirmation upgrades; absence is a caveat, not a kill.
- **AI-discovery down-weight** — for any "AI-discovered target/molecule" claim, weight by **where in the funnel the AI acted**: a 10x speed/cost claim in molecular *design* (de novo binders — Chai-2 ~16% antibody hit rate, BindCraft 10–100%) is credible; a "novel target found by AI" claim usually is **not** (in nearly all ~24 surveyed AI candidates the target was already literature-implicated). AI improves Phase 1 (~80–90%) but **not** Phase 2 (~40%, industry-average) — it does not de-risk the biology. Demand independent wet-lab/clinical validation and per-target success rates, not benchmark numbers. Discount virtual-cell "will design drugs" claims to a 5–10 year bet.

#### Step 5 — Tag the Translation State and Forward Signal

Locate each nominated target on the discovery-to-clinic timeline so the release reads as a *forward* signal:

- Query **ClinicalTrials.gov** for any IND/Phase-1 entry on the target — the moment mindshare converts to clinical reality. The gap between a data-engine nomination and first-in-human (typically 3–7 years for a novel target) is the realized lead time the skill exists to capture.
- Note whether the release is **upstream** (biobank → pQTL papers 6–18 months out) or **terminal** (a clinical readout). Upstream releases are the earliest-mover signal.
- Flag the de-risking event still pending (cross-ancestry replication; organoid confirmation; first-in-human).

### Output

```
DATA-ENGINE RELEASE BRIEF — [release name / date]
Engine class: [genetic causal | dependency | mechanism | variant | expression | chemistry | model]
Upstream / terminal: [seeds papers in 6–18mo | clinical readout]
Scope evaluated: [target / TA / whole release]

NET-NEW NOMINATIONS (this release's delta)
| Target | Direction | Convergences (engines) | Net-new Δ | Weighted | Platform/ancestry flags | Translation state | Conviction |
|--------|-----------|------------------------|-----------|----------|-------------------------|-------------------|------------|
| PCSK9  | lower     | genetics+DepMap+ChEMBL+restricted (4) | +1 (coloc) | 8 | SomaScan+Olink concordant | approved class | HIGH |
| GPR75  | lower     | genetics+restricted (2) | +1 | 4 | EUR-only — needs AoU rep | preclinical | WATCH |
| [gene] | [raise]   | [engines] (n)          | [+n]      | [n]      | [flags]                 | [no trial yet]    | [tier]    |

HIGH-CONVICTION (≥4 orthogonal engines incl. genetics):
  1. [target] — [why; nearest validated analog; pending de-risk event]

WATCHLIST (2–3 engines — needs one more orthogonal line):
  1. [target] — [missing engine to confirm]

SINGLE-SOURCE / ARTIFACT RISK (1 engine — not nominated):
  - [target] — [why discounted: trans-only / single-platform / EUR-only / AI-novel-target claim]

HAIRCUTS APPLIED:
  - Platform precision: [SomaScan vs Olink concordance notes]
  - Ancestry: [replication status]
  - AI-discovery: [funnel position of any AI claim; validation present?]

FORWARD SIGNAL:
  - This release is upstream of [expected wave / target class] in ~[6–18mo].
  - Realized lead time to FIH for [target]: ~[N] years.
  - Next de-risking catalyst to watch: [cross-ancestry rep / organoid / FIH IND].
```

## Error Handling

| Scenario | Response |
|---|---|
| Release names no specific gene targets (pure methods paper) | Classify the engine and note what target *type* it will enable; flag as upstream-tooling, not a nomination event |
| Only trans-pQTL signals available | Do not nominate; record as causally ambiguous; await cis confirmation or orthogonal engine |
| Single-platform pQTL hit (SomaScan- or Olink-only) | Apply platform haircut; check measurability on the other platform before nominating; mark as WATCH |
| Target is pan-essential in DepMap (negative everywhere) | Flag as likely too toxic for a therapeutic window; do not nominate as a selective target |
| European-only biobank/pQTL nomination | Tag ancestry-specific-artifact risk; require All of Us / cross-ancestry replication as the de-risk event |
| "AI-discovered novel target" claim with no genetic/functional backing | Down-weight heavily (literature-implicated bias); require orthogonal human validation; do not treat as novel biology |
| No prior baseline supplied | State that net-new Δ cannot be computed; report absolute convergence counts and request the prior baseline |
| Conflicting platforms disagree on a target | Surface the conflict explicitly (aptamer artifact vs noise-below-LOD); weight toward the engine with replication, not the louder headline |

## Cross-Domain Connections

This skill is explicitly **dual-use**. For a **clinical scientist learning the field**, it is a guided reading lens — it teaches *what each data engine actually proves* and *why convergence (not any single assay) is what makes a target real*, turning a flood of preprints and atlas releases into an interpretable map of where the biology is solidifying. For an **investor screening early opportunities**, it is a pre-consensus radar — it converts a dataset release into a ranked list of pre-validated targets with conviction tiers and lead-time estimates, and applies the platform/ancestry/AI-hype haircuts that separate a durable bet from a narrative.

- **data-science/statistical-analysis** (depends_on): supplies the inference machinery underneath every nomination — MR assumptions and pitfalls (horizontal pleiotropy, LD confounding, Steiger filtering for direction), colocalization, CV/precision comparison across proteomics platforms, and the convergence-scoring arithmetic. Convergence counting is only valid if the underlying statistical tests are sound.
- **frontier-intelligence/signal-scanner**: the literature/preprint velocity primitive — a data-engine release often *follows* a citation burst on the landmark mechanism paper; the two signals corroborate.
- **frontier-intelligence/emerging-target-radar**: the integrator that consumes this skill's convergence nominations alongside velocity and mindshare signals to produce the ranked target × modality watchlist.
- **frontier-intelligence/target-validation-ladder**: takes a nominated target and grades its human-genetics rung (Mendelian > coding GWAS+coloc > MR > non-coding), tractability bucket, and on-target safety read — the qualitative depth behind engine [1].
- **frontier-intelligence/modality-lifecycle**: the pQTL directionality (lower vs raise the protein) maps to a modality (antibody/ASO to lower, replacement to raise); this skill hands off the required direction.
- **frontier-intelligence/frontier-conviction-scorer**: the convergence count feeds the P(biology holds) term of the decomposed discovery-stage trajectory score.
- **probability-of-success/pos-base-rates**: genetic support is the ~2.6x relative-success multiplier; this skill detects *when* a target earns that multiplier.
