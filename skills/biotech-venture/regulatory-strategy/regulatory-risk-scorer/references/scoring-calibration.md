# Regulatory Risk Scorer — Scoring Calibration Extended Reference

This doc consolidates the six-dimension scoring rubric, 1–5 anchor definitions, dimension weights, and the aggregate-score → regulatory-PoS mapping used by the `regulatory-risk-scorer` SKILL. It is the calibration companion to that skill's inline framework.

> **PROVENANCE — READ FIRST.** Every number and anchor in this document is an **internal / expert-judgment rubric** authored inside the parent SKILL. The dimension weights (stated in the SKILL as set "by empirical contribution to approval outcomes") and the aggregate-score → PoS bands (e.g. 4.0–5.0 → ">70% PoS") are **NOT externally sourced or empirically validated**. Treat them as a structured elicitation scaffold for organizing regulatory judgment — not as a calibrated statistical model. Empirical sourcing is pending. Do not present the PoS outputs as validated approval probabilities.

**Provenance legend:**
- `int` = internal consensus estimate — originates in the parent SKILL's own prose/quick-reference; no external citation.
- `ext✓` = externally verified against a real citation. *(None appear in this doc — no verified-facts block was available at drafting.)*
- `statutory` = stable legal/regulatory constant (e.g. orphan < 200k US patients, NCE 5-yr exclusivity). *(None asserted here; the rubric references regulatory programs by name only.)*

Unless a row is tagged otherwise, assume **`int`**.

## The Six Dimensions & Weights (all `int`)

| # | Dimension | Weight | Core question |
|---|---|---|---|
| 1 | Endpoint Validation Strength | 25% | How well-established is the primary endpoint for this indication at the FDA? |
| 2 | Safety Signal Severity | 20% | How severe and manageable is the known safety profile? |
| 3 | Manufacturing Complexity | 15% | How hard is consistent manufacture at commercial scale? |
| 4 | Competitive Context / Standard of Care | 15% | How does the drug compare to existing approved therapies? |
| 5 | Unmet Need Magnitude | 15% | How severe is the disease and how great is the unmet need? |
| 6 | Regulatory Precedent Depth | 10% | How many prior approvals used a similar approach in this indication? |

Higher score = **lower** risk throughout.

## Dimension 1 — Endpoint Validation Strength (25%, `int`)

| Score | Definition | Examples |
|---|---|---|
| 5 (Very Low Risk) | Gold-standard endpoint with extensive FDA precedent | OS in oncology, MACE in cardiovascular, HbA1c in diabetes |
| 4 (Low Risk) | Validated surrogate accepted for full approval | LDL-C in CV, viral load in HIV, PFS in ovarian cancer |
| 3 (Moderate Risk) | Surrogate accepted for accelerated approval with precedent | ORR in oncology, FEV1 in COPD, MRD in heme malignancies |
| 2 (High Risk) | Surrogate with limited or contested FDA precedent | Digital endpoints, composite biomarkers, novel PROs without qualification |
| 1 (Very High Risk) | Novel endpoint with no FDA precedent | First-in-class endpoints, unvalidated surrogates, AI-derived endpoints |

*Scoring guidance:* if the endpoint has been the basis for ≥3 approvals in the same disease, score 4–5; if never accepted, score 1–2.

## Dimension 2 — Safety Signal Severity (20%, `int`)

| Score | Definition | Examples |
|---|---|---|
| 5 (Very Low Risk) | Clean profile; AEs mild and manageable | Most oral small molecules with well-known target |
| 4 (Low Risk) | Known class-effect AEs manageable with standard monitoring | CRS with CAR-T (tocilizumab), hepatotoxicity with ALT monitoring |
| 3 (Moderate Risk) | Significant AEs requiring REMS or restricted distribution | Thalidomide analogs, clozapine, isotretinoin (iPLEDGE) |
| 2 (High Risk) | Serious AEs: cardiotoxicity, severe hepatotoxicity, opportunistic infections | Novel immunomodulators, targeted therapies with on-target toxicity |
| 1 (Very High Risk) | Treatment-related deaths, black-box-level events, clinical-hold history | Gene therapies with insertional-mutagenesis risk; drugs with clinical holds |

*Scoring guidance:* clinical holds are automatic score 1; treatment-related deaths in a non-life-threatening indication score 1–2; established class effects with management protocols score 3–4.

## Dimension 3 — Manufacturing Complexity (15%, `int`)

| Score | Definition | Examples |
|---|---|---|
| 5 (Very Low Risk) | Simple, well-established processes | Oral small molecules, standard mAbs (CHO expression) |
| 4 (Low Risk) | Moderately complex but established platform | ADCs (established linker-payload chemistry), bispecifics on proven platform |
| 3 (Moderate Risk) | Complex with known challenges | AAV gene therapy (yield, potency assays), allogeneic cell therapy |
| 2 (High Risk) | Highly complex, limited commercial-scale experience | Autologous cell therapy (patient-specific), in vivo gene editing |
| 1 (Very High Risk) | Novel manufacturing, no commercial precedent | Novel delivery platforms, synthetic-biology-derived products |

*Scoring guidance:* is the CMC package complete? Has the process been validated at commercial scale? Are potency/purity/identity methods established?

## Dimension 4 — Competitive Context / Standard of Care (15%, `int`)

| Score | Definition | Examples |
|---|---|---|
| 5 (Very Low Risk) | No approved therapy; true unmet need | First-in-disease therapy for rare genetic disorder |
| 4 (Low Risk) | Existing therapies inadequate; clear step-change | Substantially better efficacy or safety vs current SOC |
| 3 (Moderate Risk) | Competitive landscape with room for differentiation | Me-better with meaningful advantage in a subpopulation |
| 2 (High Risk) | Crowded space, marginal differentiation | Multiple similar-efficacy therapies; convenience-only advantage |
| 1 (Very High Risk) | Highly effective SOC; new entrant adds minimal value | Generic-dominated space, biosimilar competition imminent |

*Scoring guidance:* FDA's benefit-risk framework explicitly weighs available alternatives — a marginal gain over a highly effective SOC is a harder path than a moderate gain over no SOC.

## Dimension 5 — Unmet Need Magnitude (15%, `int`)

| Score | Definition | Examples |
|---|---|---|
| 5 (Very Low Risk) | Fatal disease, no treatment, rapid progression | Pancreatic cancer, ALS, GBM, pediatric cancers with no approved therapy |
| 4 (Low Risk) | Serious disease with inadequate options | R/R multiple myeloma, treatment-resistant depression |
| 3 (Moderate Risk) | Chronic disease with imperfect therapies | Moderate-to-severe psoriasis, NASH, moderate Alzheimer's |
| 2 (High Risk) | Non-serious or well-managed chronic disease | Mild-moderate allergic rhinitis, GERD with PPIs available |
| 1 (Very High Risk) | Cosmetic/lifestyle indication, no serious morbidity | Hair loss, wrinkle reduction, mild acne |

*Scoring guidance:* high unmet need is a regulatory tailwind (more flexibility on endpoint, safety tolerance, trial size); low unmet need raises the evidentiary bar.

## Dimension 6 — Regulatory Precedent Depth (10%, `int`)

| Score | Definition | Examples |
|---|---|---|
| 5 (Very Low Risk) | ≥5 prior approvals, same modality, same indication | PD-1 inhibitors in melanoma, TNF inhibitors in RA |
| 4 (Low Risk) | 2–4 prior approvals; clear path established | PARP inhibitors in ovarian cancer, JAK inhibitors in MF |
| 3 (Moderate Risk) | 1 prior approval; some but not deep precedent | First biosimilar in a new indication, second gene therapy in a disease |
| 2 (High Risk) | No prior approval, but AdCom has reviewed similar programs | First-in-class with analogous mechanism reviewed by AdCom |
| 1 (Very High Risk) | No precedent; entirely novel territory | First gene-editing therapy, first AI-derived NME, first microbiome therapeutic |

*Scoring guidance:* count same-modality, same-indication approvals within the last 10 years.

## Aggregate Score → Regulatory Risk & PoS (`int`)

Weighted formula (from the SKILL):

```
Aggregate = Endpoint×0.25 + Safety×0.20 + Manufacturing×0.15
          + Competitive×0.15 + UnmetNeed×0.15 + Precedent×0.10
```

| Aggregate Score | Risk Rating | Interpretation | Approval Probability Estimate |
|---|---|---|---|
| 4.0 – 5.0 | Low Risk | Strong precedent, validated path, manageable safety | > 70% PoS at regulatory stage |
| 3.0 – 3.9 | Moderate Risk | Some uncertainties, navigable path | 50–70% PoS at regulatory stage |
| 2.0 – 2.9 | Elevated Risk | Material concerns in ≥2 dimensions | 30–50% PoS at regulatory stage |
| 1.0 – 1.9 | High Risk | Fundamental uncertainties across dimensions | < 30% PoS at regulatory stage |

> The PoS column is the least-defensible part of this rubric: the mapping from a weighted 1–5 average to a percentage approval probability is an unvalidated internal heuristic. Report it as a directional risk tier, not a point estimate, until it is empirically anchored.

## Mitigation Framework — for any dimension scoring ≤ 2 (`int`)

| Dimension | Common Mitigations |
|---|---|
| Endpoint | FDA Type B/C meeting to align on endpoint; EMA Scientific Advice; co-primary endpoints |
| Safety | Preemptive REMS proposal; independent DSMB with pre-specified stopping rules; long-term safety registry |
| Manufacturing | Pre-Approval Inspection readiness; backup CMO; commercial-scale process validation before filing |
| Competitive | Head-to-head trial vs SOC; underserved-subpopulation focus; combination strategy |
| Unmet Need | Patient-advocacy engagement; FDA rare-disease programs; natural-history study to document burden |
| Precedent | Pre-IND meeting; request FDA feedback on development plan; advisory-committee simulation |

## Source Vintage & Staleness

| Element | Staleness rate | Why |
|---|---|---|
| Dimension structure & weights | Slow (years) | Framework-level; changes only if the rubric is re-authored or empirically recalibrated |
| Anchor examples (endpoints, modalities, drugs) | Moderate (12–24 mo) | New approvals continually shift what counts as "precedented"; e.g. a novel endpoint can migrate from score 1 toward 3–4 as approvals accumulate |
| Precedent counts (Dim 6) | Fast (per approval cycle) | The ≥5 / 2–4 / 1 / 0 thresholds are re-crossed every time FDA approves in a class; re-check the same-indication, same-modality tally at each use |
| Aggregate → PoS bands | Unknown / unvalidated | Not empirically fit; will need wholesale replacement once real base rates are sourced, not incremental refresh |

All figures should be re-derived against current FDA approval history at the time of each diligence run — this rubric encodes structure, not a live database.

**Usage note.** This calibration doc serves the `regulatory-risk-scorer` SKILL (`skills/biotech-venture/regulatory-strategy/regulatory-risk-scorer/SKILL.md`). Its output feeds the Regulatory Positioning pillar of the 8-pillar `diligence-scorecard` (see `skills/biotech-venture/deal-synthesis/diligence-scorecard/references/scoring-calibration.md`, whose format this doc mirrors). Cross-reference the `regulatory-precedent`, `endpoint-selection`, and `cmc-risk-assessor` skills when scoring dimensions 6, 1, and 3 respectively. Every quantitative claim here is internal (`int`) and pending empirical sourcing — do not represent the PoS bands as validated.
