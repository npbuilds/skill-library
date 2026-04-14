---
name: pos-calculator
description: >
  Calculate risk-adjusted probability of success for any therapeutic program using
  historical base rates, mechanism-based adjustments, and program-specific modifiers.
  Produce phase-by-phase transition probabilities with explicit adjustment rationale
  and cumulative likelihood of approval. Activate when estimating PoS for an asset,
  comparing programs, or feeding probability inputs into rNPV valuation.
metadata:
  author: nirav
  version: "1.0"
  innovation: "First open-source parameterized PoS calculator with auditable adjustments"
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# PoS Calculator — The Actuarial Engine

No open-source probability-of-success calculator exists for biotech venture diligence. Every VC firm does this on ad-hoc spreadsheets with inconsistent assumptions. This skill changes that. It produces a structured, auditable PoS estimate with explicit adjustment rationale at every step — so when you present an rNPV to an investment committee, every assumption behind the probability weighting can be traced.

## How to Run

### Input

Provide as much of the following as available. The calculator works with partial information but produces wider confidence ranges.

| Parameter | Required? | Example |
|---|---|---|
| Therapeutic area | Yes | Oncology (NSCLC) |
| Current development phase | Yes | Phase 2 |
| Mechanism of action | Yes | PD-1/VEGF bispecific antibody |
| Target | Recommended | PD-1 + VEGF-A |
| Modality | Recommended | Bispecific antibody |
| Biomarker selection | If applicable | PD-L1 CPS >= 1 |
| Regulatory designations | If applicable | Breakthrough Therapy, Orphan |
| Prior clinical data | If available | Phase 1 ORR = 42%, DCR = 78% |
| Competitive context | Recommended | 3 approved IO agents in 1L NSCLC |
| Company capitalization | Optional | $800M market cap, $400M cash |

### Steps

#### Step 1 — Establish Base Rate

Load therapeutic-area-specific base rates from pos-base-rates:

```
Base PTRS = {P(current phase -> next), P(next -> next+1), ..., P(NDA -> Approval)}
Base LOA = Product of all remaining PTRS
```

Example for Phase 2 oncology (NSCLC):
- P2->P3: 24% | P3->NDA: 52% | NDA->Appr: 85%
- Base LOA from Phase 2 = 0.24 x 0.52 x 0.85 = **10.6%**

#### Step 2 — Apply Modality Adjustment

Adjust base rate for drug modality using pos-base-rates modality table:

```
Modality-adjusted LOA = Base LOA x Modality Factor
```

Example: bispecific antibody = 0.9-1.0x → adjusted LOA = 10.6% x 0.95 = **10.1%**

#### Step 3 — Apply Mechanism-Based Adjustments

Route to mechanism-risk-adjuster for target validation assessment. Key adjustment categories:

| Factor | Direction | Magnitude | Evidence Required |
|---|---|---|---|
| Genetic target validation (MR) | Upward | +20-30% relative | Published MR study with significant association |
| Validated target (approved drug in class) | Upward | +10-20% relative | Approved drug hitting same target |
| First-in-class (novel target) | Downward | -10-15% relative | No approved drug or advanced clinical data on target |
| Prior failure in same MOA | Downward | -15-25% relative | Phase 2/3 failure in same mechanism class |
| Strong preclinical-to-clinical translation | Upward | +5-10% relative | Species concordance, validated PK/PD model |
| Known mechanism toxicity | Downward | -5-15% relative | Class-effect safety signal documented |

Apply adjustments multiplicatively to the modality-adjusted LOA. Document each adjustment with evidence.

```
Mechanism-adjusted LOA = Modality-adjusted LOA x (1 + sum of adjustment factors)
```

#### Step 4 — Apply Program-Specific Modifiers

| Modifier | Direction | Magnitude | Rationale |
|---|---|---|---|
| Breakthrough Therapy Designation | Upward | +10-15% relative | 54% of granted BTDs approved; 30% time savings |
| Orphan Drug Designation | Upward | +10-15% relative | Smaller trials, regulatory flexibility, 7yr exclusivity |
| Biomarker-selected population | Upward | +15-25% relative | Higher effect size, enriched responder population |
| Large unmet need (no approved SOC) | Upward | +5-10% relative | FDA more willing to accept surrogate endpoints |
| Positive Phase 2 data (above expectations) | Upward | +10-20% relative | Data de-risks efficacy hypothesis |
| Crowded indication (5+ competitors) | Downward | -5-10% relative | Higher bar for differentiation, enrollment challenges |
| Small/undercapitalized sponsor | Downward | -5-10% relative | Execution risk, may not fund pivotal trial adequately |

#### Step 5 — Apply Reflexivity Adjustment (Innovation)

This step captures the insight from Soros's reflexivity theory applied to biotech:

**PoS is path-dependent.** A well-capitalized company with positive market sentiment has genuinely higher PoS than the base rate suggests — not because the drug is different, but because:
- Better-funded Phase 3 trials (more sites, faster enrollment, better CRO)
- Ability to run adaptive trials and add arms
- Stronger regulatory interactions (can afford experienced regulatory teams)
- Better manufacturing scale-up execution

| Capital Position | Reflexivity Adjustment |
|---|---|
| Well-capitalized (>3yr runway, >$500M cash) | +5-10% relative |
| Adequately capitalized (1-3yr runway) | 0% (neutral) |
| Under-capitalized (<1yr runway without raise) | -10-15% relative |
| Pre-data capital raise completed | +5% relative (runway secured) |

```
Reflexivity-adjusted LOA = Program-adjusted LOA x (1 + reflexivity factor)
```

#### Step 6 — Produce Output

### Output

```
POS ESTIMATE — [Asset Name]
Indication: [therapeutic area + specific indication]
Current Phase: [phase]
Date: [date of assessment]

Phase-by-Phase PTRS:
  P[current] -> P[next]:  [%] (base: [%], adjusted: [%])
  P[next] -> P[next+1]:   [%] (base: [%], adjusted: [%])
  ...
  NDA -> Approval:         [%] (base: [%], adjusted: [%])

Cumulative LOA: [%]

Adjustment Audit Trail:
  Base rate (TA):          [%]  Source: BIO/Informa 2024
  + Modality ([type]):     [+/- x%]  Reason: [rationale]
  + Target validation:     [+/- x%]  Evidence: [MR study / competitive validation / novel]
  + [Modifier 1]:          [+/- x%]  Reason: [rationale]
  + [Modifier 2]:          [+/- x%]  Reason: [rationale]
  + Reflexivity:           [+/- x%]  Capital position: [status]
  ─────────────────────────
  Final LOA:               [%]

Confidence Range: [low% - high%]
  Low: Conservative (all adjustments at lower bound)
  High: Optimistic (all adjustments at upper bound)

Key Assumptions:
  1. [Most impactful assumption]
  2. [Second most impactful]
  3. [Third most impactful]

Key Risks to PoS:
  1. [Risk that could materially lower PoS]
  2. [Risk that could materially lower PoS]

Comparison to Naive Estimate:
  Generic Phase 2 LOA: [%]
  This program's LOA: [%]
  Difference: [+/- x%] ([reason for divergence])
```

## Error Handling

| Scenario | Response |
|---|---|
| Insufficient information for base rate | Use "All Indications" base rate with wider confidence range |
| No MR data available for target | Skip genetic validation adjustment; note as limitation |
| Conflicting adjustment factors | Apply both; net effect may partially cancel; document both |
| Ultra-rare disease (<200 patients) | Base rates unreliable; use rare disease rates with high uncertainty band |
| Platform technology (multiple indications) | Calculate PoS per indication; note that platform success in one indication may de-risk others |

## Cross-Domain Connections

- **Biotech-venture/pos-base-rates**: Source of all base rate data
- **Biotech-venture/mechanism-risk-adjuster**: Provides mechanism-based adjustment factors
- **Biotech-venture/rnpv-modeler**: Primary consumer — PoS feeds into probability-weighted cash flows
- **Biotech-venture/diligence-scorecard**: PoS is the clinical strength pillar score
- **Investing/reflexivity-theory**: Source of the reflexivity adjustment concept
- **Investing/risk-architecture**: Structural parallel — both quantify multi-factor risk
