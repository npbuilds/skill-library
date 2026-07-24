---
name: target-validation-ladder
description: >
  Grade the human-genetic validation of a drug target on a causality-ranked evidence
  ladder (Mendelian/rare-variant > coding GWAS+colocalization > Mendelian randomization >
  non-coding GWAS), scoring direction-of-effect concordance, tractability, and on-target
  safety read-across. Produces a 0-13 composite tier from Open Targets, the Genetic
  Priority Score, gnomAD constraint, and a cis-MR/PheWAS scan. Activate when assessing
  whether a target hypothesis is genetically supported, before mechanism-risk or PoS
  modeling, when screening an early-discovery asset, or when learning what separates a
  PCSK9-class target from a hopeful GWAS hit.
metadata:
  author: nirav
  version: "1.0"
  parent: modality-trajectory
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Target Validation Ladder — Grading the Human-Genetics Prior

Target choice is the highest-leverage decision in drug development: roughly 90% of clinical programs fail, and the largest share of Phase II/III failures is lack of efficacy — the *target hypothesis was wrong*, not the molecule. Human genetics is the only widely-validated tool that shifts the prior on efficacy *before* any clinical data exist, because a genetic variant is a natural, lifelong, randomized perturbation of the target in humans. Targets with genetic support have ~2.6x higher relative success across the pipeline (Minikel, Painter, Dong & Nelson, *Nature* 629:624, 2024), refining the original ~2x estimate (Nelson et al., *Nature Genetics* 2015).

The headline 2.6x is an average that hides the structure. The multiplier concentrates where two things hold: (1) the **causal gene** at the locus is unambiguous, and (2) the **genetic direction of effect** matches the drug's intended direction. Predictive power is *flat* across genetic effect size, minor allele frequency, and year of discovery (Minikel 2024) — so a clean common-variant signal can be as informative as a rare large-effect one, provided causality is established. A program citing "GWAS support" without naming the causal gene and stating a concordant direction is claiming far less than it sounds.

This skill turns that into a gradeable rubric. It is the **earliest-stage** validation check in the suite — it asks "does the human evidence say this target matters, in the right direction, with confidence in the gene?" before any clinical asset exists, then hands the graded prior forward to `probability-of-success/mechanism-risk-adjuster`, which converts it into a phase-weighted PoS multiplier. The #1 failure mode it exists to prevent: **crediting the wrong gene at a locus** (~90% of GWAS hits are non-coding; the nearest gene is often not causal).

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Target gene (HGNC symbol) | User | Yes |
| Indication / disease | User | Yes |
| Intended mechanism direction (inhibit / degrade / agonize / replace) | User | Recommended |
| Intended modality (small molecule / antibody / PROTAC / oligo / gene therapy) | User | Recommended (default: score all) |
| Ancestry / cohort caveats | User | Optional |

### Steps

> **Grading corpus:** Grade a candidate by its nearest analog in `references/validated-target-library.md` — 9+ primary-sourced targets (PCSK9, HMGCR, NPC1L1, ASGR1, Lp(a), TYK2, TL1A, TREM2, LRRK2…) with evidence type, effect direction, drug outcome, and tier, plus the ladder-calibration multipliers (Nelson 2× → Minikel 2.6×, OMIM RS 3.7, Open Targets dose-response) and a genetics-vs-clinical divergence watch.

#### Step 1 — Pull the genetics-only association and the pre-computed rank

Establish the prior before grading by hand:

- **Open Targets Platform** (platform.opentargets.org / Open Targets MCP): pull the target-disease association. Use the 2025 "Associations on the Fly" weighting to **zero out non-genetic data sources** and read a *genetics-only* score — non-genetic evidence (literature, pathways) inflates the headline and is not what predicts approval.
- **Genetic Priority Score** (Mount Sinai / Do lab portal): look up the GPS and GPS-with-direction for the gene × indication (19,365 genes × 399 indications). Anchor: the **top 0.28% of GPS conferred ~9.9x odds** of being a valid indication and were **1.7 / 3.7 / 8.8x** more likely to advance Phase I→II / III / IV (Duffy/Do, *Nature Genetics* 56:51, 2024).

These two reads give a fast prior. The rest of the workflow confirms *why* the score is what it is — never trust the number without auditing the causal gene and direction.

#### Step 2 — Place the evidence on the causality ladder (Axis 1)

The ladder is ordered by **causal-gene confidence**, not statistical significance. Climb to the highest tier the evidence supports:

```
EVIDENCE LADDER (highest causal confidence → lowest)

Tier A  Mendelian / rare-variant burden     → OMIM, ClinVar, gene-collapsing
        The variant IS the gene; no ambiguity.   (Regeneron/AZ exome, UKB WES
                                                   + FinnGen 744-endpoint meta, n=653,219)
Tier B  Coding GWAS hit OR colocalization    → Open Targets L2G (0-1, 51 features,
        (coloc posterior >0.8 / L2G >0.5)        92-tissue QTL coloc, Shapley
        Pins the causal gene.                     explanations); coloc/SuSiE; GWAS Catalog
Tier C  cis-MR, colocalized, pleiotropy-robust → cis-MR (Nat Commun 2024); mimics
        Direction + causality, method-dependent   pharmacological perturbation
Tier D  Non-coding GWAS, nearest-gene only    → weakest; the wrong-gene failure mode
```

Two orthogonal amplifiers sit beside the ladder, not on it:
- **Allelic series / dose-response** (Tier D in the brief's lettering, Axis 3 here): a graded null→partial→GoF set with monotonic effect is the *gold standard* — it predicts the shape of the efficacy curve. PCSK9 is the canonical case.
- **Human knockouts / LoF tolerance** (Axis 4 safety): healthy homozygous/compound-het LoF carriers prove full inhibition is tolerated.

#### Step 3 — Establish direction-of-effect concordance (Axis 2)

The single most underweighted variable. Association says the gene matters; **direction** says whether to agonize or antagonize.

```
LoF protective       ⇒ inhibit / degrade   (PCSK9, ANGPTL3, APOC3, LPA)
LoF causes disease   ⇒ activate / replace  (enzyme replacement, agonism)
Direction discordant ⇒ COLLAPSES the genetic premium — hard gate
```

Confirm direction with: allelic series, LoF-vs-GoF contrast, and **Steiger filtering** in MR (orients cause→effect). Demand the direction be *stated* and *concordant* with the intended mechanism. Use the **GPS-with-direction** variant where available. Discordant or unknown direction is the second-most-common reason a "genetically supported" target fails.

#### Step 4 — Run the safety read-across (Axis 4)

Human genetics predicts harm, not just efficacy:

- **gnomAD constraint** (v4 ~807,000; v2 141,456): read **pLI** and **LOEUF** (LOFTEE-based). Highly constrained genes (pLI~1, low LOEUF) flag that strong/complete perturbation may be poorly tolerated — a caution on full inhibition, not a disqualifier (essential genes can be fine inhibitor targets at sub-maximal engagement).
- **Human-knockout catalog**: ~3,421 genes (**18%**) have tolerated two-hit pLoF "human-knockout" genotypes in gnomAD (Minikel et al., *Nature* 581:459, 2020) — positive evidence of dispensability for inhibitor/degrader programs. Absence is ambiguous (lethality vs. rarity), not disqualifying.
- **Pleiotropy as a side-effect predictor**: a side effect is **~2x more likely** when it resembles a trait genetically associated with the target gene (Duffy/Minikel/Nelson, *PLOS Genetics* 2025). Operationalize by scanning the gene's full phenome (PheWAS / cis-MR across UKB, FinnGen, MVP — >1M combined) for adverse phenotypes *before* first-in-human.

#### Step 5 — Grade modality tractability (Axis 5)

A Tier-A genetically validated target can be small-molecule-intractable; the right read is "validated, needs an antibody/oligo," not "fail." Grade *per modality* using Open Targets tractability buckets (ChEMBL v34 pipeline):

- **Small molecule (8 buckets):** approved SM drug → Phase 2/3 → Phase 1 → co-crystal with ligand → high-quality ligand (PFI ≤7) → DrugEBIlity pocket ≥0.7 → DrugEBIlity 0–0.7 → druggable-genome family (Finan 2017).
- **Antibody:** clinical precedence → high-confidence membrane/secreted localization → predicted signal peptide/TM → Human Protein Atlas membrane evidence.
- **PROTAC/degrader:** clinical precedence → literature → ubiquitination sites → protein half-life → ChEMBL binder ≤10 µM.
- **Oligo / gene therapy (escape hatch):** the modern route for high-genetic-confidence / low-classical-tractability targets (e.g., *LPA* siRNA).

#### Step 6 — Subtract the failure modes, then score

Before assigning the composite, run the failure-mode checklist (each is a documented reason "genetically supported" targets still fail):

```
FAILURE-MODE AUDIT
[ ] Wrong gene at locus        → require coding variant or coloc/L2G > threshold
[ ] Wrong direction of effect  → Steiger filter, allelic series, explicit direction
[ ] Horizontal pleiotropy (MR) → cis-only instruments, coloc, MR-Egger/CAUSE
[ ] LD / cross-ancestry confound → matched-ancestry coloc
[ ] Tissue-discordant QTLs     → use disease-relevant tissue
[ ] Reverse causation          → trait causes molecular phenotype, not vice versa
[ ] Indication mismatch        → genetic support for trait X, program targets Y
[ ] Mechanism mismatch         → variant models one isoform/domain only
```

Then score the six axes (full rubric in `references/quick-reference.md`) and apply the hard gates.

### Output

```
TARGET VALIDATION LADDER — [GENE] in [Indication]
Date: [assessment date]    Intended mechanism: [inhibit/agonize/...]    Modality: [...]

Prior reads:
  Open Targets genetics-only score: [0-1]
  Genetic Priority Score percentile: [%]  (top 0.28% ⇒ ~9.9x indication odds)

Axis scores:
  1. Causal-gene confidence (0-4):        [n]  — [ladder tier + evidence]
  2. Direction concordance (0-2):         [n]  — [LoF protective ⇒ inhibit, etc.]
  3. Allelic series / dose-response (0-2):[n]  — [series / partial / single variant]
  4. Safety read-across (0-2):            [n]  — [pLI/LOEUF; KO tolerance; PheWAS pleiotropy]
  5. Tractability (0-2, per modality):    [n]  — [OT bucket]
  6. Replication / generalizability (0-1):[n]  — [biobanks / ancestries]

  COMPOSITE: [0-13]  →  TIER [1-5]: [de-risked / strong / emerging / hypothesis / none]

Hard gates applied:
  [ ] Discordant direction → capped at Tier 3
  [ ] Non-coding-only, no coloc → causal confidence capped at 1
  [ ] Intractable in all modalities → flag undevelopable

Failure-mode flags: [list any tripped]

Verdict: [PCSK9-class de-risked / strong with gaps / emerging needs orthogonal work /
          association-grade hypothesis / no human prior]

Hand-forward to mechanism-risk-adjuster:
  Genetic-support tier: [Tier 1-5]
  Implied relative-success multiplier: [~2.6x top-bin → ~1.0x for Tier 5]
  Direction-concordant: [Y/N]    On-target safety flag: [clean / caution / adverse]
```

## Error Handling

| Scenario | Response |
|---|---|
| No human genetic association found | Score Axis 1 = 0, composite Tier 5. State explicitly there is no genetic prior — not a kill, but the 2.6x lift is unavailable; lean on functional genomics (weakest predictor of human success). |
| Strong GWAS signal but no coding variant / no colocalization | Cap causal-gene confidence at 1 (hard gate). Do not credit the nearest gene. Flag "wrong gene at locus" risk; recommend L2G + coloc before crediting. |
| Direction of effect unknown or discordant | Cap composite at Tier 3 regardless of other axes. Demand allelic series or Steiger-filtered MR before upgrading. |
| MR result is the only support, un-colocalized | Treat as Tier C *only if* cis-instruments + colocalization hold; otherwise discount heavily — un-colocalized druggable-genome MR over-claims novel targets (critiqued 2024-25). |
| Genetically pristine but no tractable handle in any modality | Flag undevelopable (hard gate); note the oligo/gene-therapy escape hatch before concluding. |
| No healthy human knockouts exist | Treat as no-information for safety (could be lethality OR rarity), not as evidence against. Lean on pLI/LOEUF and PheWAS instead. |
| Predominantly European cohort, target may not generalize | Note ancestry caveat; downgrade Axis 6 replication; flag for All of Us / MVP re-check. |
| GPS / Open Targets disagree with hand-graded ladder | The hand audit (causal gene + direction) overrides the pre-computed score; the score is a prior, not a verdict. |

## Cross-Domain Connections

This skill is deliberately **dual-use** — the same rubric serves two readers:
- **A clinical scientist learning the field** uses it as a teaching ladder: it makes explicit *why* PCSK9 (Tier A allelic series + healthy human knockout) is a different class of evidence from a non-coding GWAS hit, and *why* direction-of-effect is the variable that separates a real agonist/antagonist call from a coin flip.
- **An investor screening early opportunities** uses it as a diligence gate: a weak rung on this stack is a red flag even when the preclinical data are pretty, and the composite tier becomes the genetic-support input to the conviction stack — applied *before* a clinical asset exists, when the cheapest de-risking decision is made.

- **probability-of-success/mechanism-risk-adjuster** *(depends_on — primary hand-forward)*: This skill runs *earlier*. It grades the human-genetics prior; the risk-adjuster consumes the graded tier and converts it into the PoS multiplier (genetic target validation ≈ +20-30% / ~2.6x relative success). The clean contract: this skill outputs {genetic-support tier, direction-concordant Y/N, safety flag}; the adjuster turns it into a phase-weighted number. Never let the adjuster apply a genetic premium this skill has not graded.
- **probability-of-success/pos-base-rates**: supplies the therapeutic-area / modality base rate that the 2.6x genetic multiplier scales.
- **modality-trajectory/modality-lifecycle** *(sibling)*: when a Tier-A target is intractable by small molecule/antibody, the lifecycle map says whether the rescuing modality's delivery unlock has landed (oligo, degrader, gene therapy).
- **modality-trajectory/moa-analog-engine** *(sibling)*: a genetics-first target (PCSK9/GPR75 pattern) is one of three arc templates; this skill confirms the "genetics-first" classification with graded evidence.
- **frontier-discovery/frontier-conviction-scorer**: the composite tier is the P(biology holds) term in the discovery-stage trajectory score.
- **competitive-intelligence/pipeline-mapper**: a high-tier target with thin clinical competition is white space; pipeline crowding around a Tier-A target is mechanism validation.
