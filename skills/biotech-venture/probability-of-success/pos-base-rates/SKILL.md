---
name: pos-base-rates
description: >
  Provide historical clinical trial success rates by phase, therapeutic area, modality,
  and endpoint type, sourced from BIO/Informa/QLS databases with vintage-year adjustments.
  Reference when calculating probability of success, calibrating mechanism-based risk
  adjustments, or benchmarking a specific program against historical base rates.
metadata:
  author: nirav
  version: "1.0"
  sources: "BIO/Informa/QLS 2011-2020, VisionLifeSciences 2024, Nature Communications 2025"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# PoS Base Rates — The Actuarial Tables of Drug Development

Historical phase transition probabilities are the foundation of every probability-of-success estimate. They represent the prior — what happens to the average drug in the average program before you apply any program-specific adjustments. Getting the base rate wrong by even a few percentage points compounds multiplicatively across phases and can distort an rNPV by 2-5x.

These tables are reference data, not calculations. The pos-calculator consumes them as inputs and applies adjustments. Keep them separate so the data can be updated independently as new meta-analyses publish.

## Key Concepts

### Likelihood of Approval (LOA)

LOA is the cumulative probability that a drug currently in a given phase will eventually receive regulatory approval. It is calculated as the product of all remaining phase transition probabilities:

```
LOA from Phase N = P(N->N+1) x P(N+1->N+2) x ... x P(NDA->Approval)
```

### Phase Transition Probability (PTRS)

Probability of Technical and Regulatory Success at each individual phase gate. This is the probability of advancing from one phase to the next, NOT the cumulative probability of reaching approval.

### Why Base Rates Matter for Venture

- A Phase 1 oncology asset has ~4.7% LOA. Most venture analysts use "~10%" as a generic figure, overestimating by 2x.
- A rare disease asset has ~16.3% LOA from Phase 1 — 3.5x higher than oncology. This difference alone can flip an rNPV from negative to positive.
- Modality matters: biologics have higher Phase 1 PoS than small molecules, but gene therapy has higher late-stage attrition due to manufacturing.

## Phase Transition Probabilities by Therapeutic Area

Source: BIO/Informa/QLS 2011-2020 report, supplemented by VisionLifeSciences 2024 update.

| Therapeutic Area | P1->P2 | P2->P3 | P3->NDA | NDA->Appr | LOA (P1) |
|---|---|---|---|---|---|
| **All Indications** | 52% | 29% | 58% | 88% | **7.9%** |
| **Oncology** | 45% | 24% | 52% | 85% | **4.7%** |
| **Rare / Orphan** | 65% | 42% | 65% | 92% | **16.3%** |
| **Hematology** | 55% | 35% | 60% | 90% | **10.4%** |
| **Immunology / Inflammation** | 50% | 25% | 55% | 87% | **6.0%** |
| **CNS / Neurology** | 48% | 20% | 50% | 85% | **4.1%** |
| **Cardiovascular** | 55% | 28% | 55% | 88% | **7.5%** |
| **Metabolic / Endocrine** | 58% | 32% | 60% | 90% | **10.0%** |
| **Infectious Disease** | 55% | 33% | 62% | 88% | **9.9%** |
| **Respiratory** | 50% | 26% | 52% | 85% | **5.7%** |
| **Ophthalmology** | 55% | 30% | 58% | 88% | **8.5%** |
| **Dermatology** | 52% | 30% | 60% | 88% | **8.3%** |
| **GI / Hepatology** | 50% | 27% | 55% | 87% | **6.5%** |

## Modality Adjustments

Not all drug types have equal success rates. Apply these multipliers to the therapeutic-area base rate.

| Modality | Adjustment Factor | Rationale |
|---|---|---|
| Small molecule | 1.0x (baseline) | Well-characterized development pathway |
| Monoclonal antibody | 1.1-1.2x | Higher Phase 1 safety, better target selectivity |
| Bispecific antibody | 0.9-1.0x | Newer modality, less historical data |
| ADC (antibody-drug conjugate) | 0.8-0.9x | Complex manufacturing, narrow therapeutic window |
| Gene therapy | 0.7-0.8x | High Phase 3 attrition due to manufacturing, durability uncertainty |
| Cell therapy (autologous) | 0.6-0.7x | Vein-to-vein logistics, manufacturing variability |
| Cell therapy (allogeneic) | 0.7-0.8x | Off-the-shelf advantage, but less clinical validation |
| mRNA/LNP | 0.9-1.0x | COVID validation improved platform confidence |
| Oligonucleotide (ASO/siRNA) | 0.8-0.9x | Delivery challenges, but improving with GalNAc |
| Peptide | 1.0-1.1x | Well-understood PK, GLP-1 success boosted class |

## Program-Specific Modifiers

These adjust the base rate up or down based on characteristics of the specific program being evaluated.

| Modifier | Effect on PoS | Evidence |
|---|---|---|
| **Genetic target validation (MR evidence)** | +20-30% | Targets with Mendelian randomization support have 2x higher LOA (Nature Genetics 2015) |
| **Biomarker-selected population** | +15-25% | Enriched trials have higher effect sizes and lower NNT |
| **First-in-class mechanism** | -10-15% | Novel mechanisms have higher attrition than validated targets |
| **Breakthrough Therapy Designation** | +15-20% (time) | 30% reduction in development time; 54% of granted BTDs approved |
| **Orphan Drug Designation** | +10-15% | Smaller trials, lower regulatory bar, 7-year exclusivity |
| **Prior Phase 2 failure in same MOA** | -15-25% | Mechanism may be flawed, not just the molecule |
| **Competitive validation (same-class approval)** | +10-20% | Validates mechanism; reduces regulatory uncertainty |
| **Large unmet need / no SOC** | +5-10% | FDA more willing to accept surrogate endpoints |

## Historical Trends

- **Overall LOA is declining**: BioMedTracker analysis (2014-2023) shows falling success rates, driven by increasing complexity of remaining targets
- **Oncology improving slightly**: Biomarker selection and immunotherapy have modestly improved oncology Phase 2 success rates since 2015
- **CNS remains hardest**: Blood-brain barrier, endpoint validation challenges, and placebo response keep CNS at ~4% LOA
- **Rare disease accelerating**: Orphan drug incentives, smaller trials, and genetic target clarity drive 2-3x higher LOA than non-orphan

## When This Applies

- **Always** as the starting point for any PoS calculation via pos-calculator
- When benchmarking a specific program: "Is this Phase 2 oncology result better or worse than the base rate?"
- When comparing therapeutic areas: "Should we invest in rare disease vs oncology?"
- When evaluating modality risk: "How does gene therapy attrition compare to mAb?"

## Cross-Domain Connections

- **Biotech-venture/pos-calculator**: Primary consumer — takes base rates and applies program-specific adjustments
- **Biotech-venture/mechanism-risk-adjuster**: Uses base rates as the denominator for mechanism-based adjustment calculations
- **Biotech-venture/rnpv-modeler**: PoS feeds directly into the probability-weighted cash flow model
- **Investing/risk-architecture**: Structural parallel — both map risk factors to probability-weighted outcomes
