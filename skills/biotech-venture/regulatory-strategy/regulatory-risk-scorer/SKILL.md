---
name: regulatory-risk-scorer
description: >
  Score regulatory risk across six clinical-regulatory dimensions using a structured
  framework, producing a quantitative risk profile with radar chart scores, aggregate
  risk rating, and prioritized mitigation strategies. Reference when performing
  diligence on a biotech asset's regulatory risk profile or comparing risk across
  multiple assets in a portfolio context.
metadata:
  author: nirav
  version: "1.0"
  parent: regulatory-strategy
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Regulatory Risk Scorer — Quantifying the Probability That the FDA Says Yes

Regulatory risk is the most frequently underestimated variable in biotech venture models. A company can have a drug that works biologically, demonstrate statistical significance in a pivotal trial, and still receive a Complete Response Letter. The FDA evaluates benefit-risk holistically, and dimensions that financial analysts overlook — manufacturing complexity, endpoint validation strength, competitive context — regularly determine approval outcomes.

This skill provides a structured, six-dimension scoring framework that translates qualitative clinical-regulatory judgment into a quantitative risk profile. Each dimension is scored 1-5, weighted by its empirical contribution to approval outcomes, and aggregated into an overall risk rating.

## The Six Dimensions of Regulatory Risk

### Dimension 1: Endpoint Validation Strength (Weight: 25%)

How well-established is the primary endpoint for this indication at the FDA?

| Score | Definition | Examples |
|---|---|---|
| **5 (Very Low Risk)** | Gold standard endpoint with extensive FDA precedent | OS in oncology, MACE in cardiovascular, HbA1c in diabetes |
| **4 (Low Risk)** | Validated surrogate accepted for full approval | LDL-C in cardiovascular, viral load in HIV, PFS in ovarian cancer |
| **3 (Moderate Risk)** | Surrogate accepted for accelerated approval with precedent | ORR in oncology, FEV1 in COPD, MRD in hematologic malignancies |
| **2 (High Risk)** | Surrogate with limited or contested FDA precedent | Digital endpoints, composite biomarkers, novel PROs without qualification |
| **1 (Very High Risk)** | Novel endpoint with no FDA precedent | First-in-class endpoints, unvalidated surrogates, AI-derived endpoints |

**Scoring guidance**: Check the regulatory-precedent skill for FDA endpoint acceptance history in the target indication. If the endpoint has been the basis for >=3 approvals in the same disease, score 4-5. If the endpoint has never been accepted, score 1-2.

### Dimension 2: Safety Signal Severity (Weight: 20%)

What is the severity and manageability of the known safety profile?

| Score | Definition | Examples |
|---|---|---|
| **5 (Very Low Risk)** | Clean safety profile; AEs mild and manageable | Most oral small molecules with well-known target |
| **4 (Low Risk)** | Known class-effect AEs that are manageable with standard monitoring | CRS with CAR-T (manageable with tocilizumab), hepatotoxicity with ALT monitoring |
| **3 (Moderate Risk)** | Significant AEs requiring REMS or restricted distribution | Thalidomide analogs (REMS), clozapine (REMS), isotretinoin (iPLEDGE) |
| **2 (High Risk)** | Serious AEs observed: cardiotoxicity, severe hepatotoxicity, opportunistic infections | Novel immunomodulators, targeted therapies with on-target toxicity |
| **1 (Very High Risk)** | Treatment-related deaths, black box warning-level events, clinical hold history | Gene therapies with insertional mutagenesis risk, drugs with clinical holds |

**Scoring guidance**: Review safety data from all available phases. Clinical holds are automatic score 1. Any treatment-related deaths in a non-life-threatening indication are score 1-2. Known class effects with established management protocols score 3-4.

### Dimension 3: Manufacturing Complexity (Weight: 15%)

How difficult is it to consistently manufacture the product at commercial scale?

| Score | Definition | Examples |
|---|---|---|
| **5 (Very Low Risk)** | Simple manufacturing, well-established processes | Oral small molecules, standard mAbs (CHO expression) |
| **4 (Low Risk)** | Moderately complex but established platform | ADCs (linker-payload chemistry established), bispecifics on proven platform |
| **3 (Moderate Risk)** | Complex manufacturing with known challenges | AAV gene therapy (yield, potency assays), allogeneic cell therapy |
| **2 (High Risk)** | Highly complex, limited commercial-scale experience | Autologous cell therapy (patient-specific), in vivo gene editing |
| **1 (Very High Risk)** | Novel manufacturing with no commercial precedent | Novel delivery platforms, synthetic biology-derived products |

**Scoring guidance**: FDA increasingly issues CRLs for manufacturing deficiencies. Key questions: Is the CMC package complete? Has the manufacturing process been validated at commercial scale? Are analytical methods for potency, purity, and identity established?

### Dimension 4: Competitive Context / Standard of Care (Weight: 15%)

How does the drug compare to existing approved therapies?

| Score | Definition | Examples |
|---|---|---|
| **5 (Very Low Risk)** | No approved therapy exists; true unmet need | First-in-disease therapy for rare genetic disorder |
| **4 (Low Risk)** | Existing therapies are inadequate; clear step-change improvement | Substantially better efficacy or safety vs current SOC |
| **3 (Moderate Risk)** | Competitive landscape with room for differentiation | Me-better with clinically meaningful advantage in a subpopulation |
| **2 (High Risk)** | Crowded space, marginal differentiation | Multiple approved therapies with similar efficacy; convenience-only advantage |
| **1 (Very High Risk)** | SOC is highly effective; new entrant adds minimal value | Generic-dominated space, biosimilar competition imminent |

**Scoring guidance**: FDA's benefit-risk framework explicitly considers available alternatives. A marginal improvement over a highly effective SOC is a harder regulatory path than a moderate improvement over no SOC. Check the clinical-differentiator skill for competitive positioning.

### Dimension 5: Unmet Need Magnitude (Weight: 15%)

How severe is the disease and how great is the unmet need?

| Score | Definition | Examples |
|---|---|---|
| **5 (Very Low Risk)** | Fatal disease with no treatment, rapid progression | Pancreatic cancer, ALS, GBM, pediatric cancers with no approved therapy |
| **4 (Low Risk)** | Serious disease with inadequate treatment options | Relapsed/refractory multiple myeloma, treatment-resistant depression |
| **3 (Moderate Risk)** | Chronic disease with existing but imperfect therapies | Moderate-to-severe psoriasis, NASH, moderate Alzheimer's |
| **2 (High Risk)** | Non-serious condition or well-managed chronic disease | Mild-moderate allergic rhinitis, GERD with PPIs available |
| **1 (Very High Risk)** | Cosmetic or lifestyle indication with no serious morbidity | Hair loss, wrinkle reduction, mild acne |

**Scoring guidance**: High unmet need provides regulatory tailwind — FDA grants more flexibility on endpoint, safety tolerance, and trial size. Conversely, low unmet need means the FDA demands more rigorous evidence of benefit.

### Dimension 6: Regulatory Precedent Depth (Weight: 10%)

How many prior approvals has the FDA granted in this indication using a similar approach?

| Score | Definition | Examples |
|---|---|---|
| **5 (Very Low Risk)** | >=5 prior approvals with same modality in same indication | PD-1 inhibitors in melanoma, TNF inhibitors in RA |
| **4 (Low Risk)** | 2-4 prior approvals; clear regulatory path established | PARP inhibitors in ovarian cancer, JAK inhibitors in MF |
| **3 (Moderate Risk)** | 1 prior approval; some precedent but not deep | First biosimilar in a new indication, second gene therapy in a disease |
| **2 (High Risk)** | No prior approval but advisory committee has reviewed similar programs | First-in-class with analogous mechanism reviewed by AdCom |
| **1 (Very High Risk)** | No precedent; entirely novel regulatory territory | First gene editing therapy, first AI-derived NME, first microbiome therapeutic |

**Scoring guidance**: Cross-reference with the regulatory-precedent skill for approval history. Count approvals of the same modality in the same indication within the last 10 years.

## Aggregate Scoring System

### Weighted Score Calculation

```
Aggregate Score = (Endpoint * 0.25) + (Safety * 0.20) + (Manufacturing * 0.15)
                + (Competitive * 0.15) + (Unmet Need * 0.15) + (Precedent * 0.10)
```

### Risk Rating Translation

| Aggregate Score | Risk Rating | Interpretation | Approval Probability Estimate |
|---|---|---|---|
| 4.0 - 5.0 | **Low Risk** | Strong precedent, validated path, manageable safety | >70% PoS at regulatory stage |
| 3.0 - 3.9 | **Moderate Risk** | Some uncertainties but navigable path | 50-70% PoS at regulatory stage |
| 2.0 - 2.9 | **Elevated Risk** | Material concerns in >=2 dimensions | 30-50% PoS at regulatory stage |
| 1.0 - 1.9 | **High Risk** | Fundamental uncertainties across multiple dimensions | <30% PoS at regulatory stage |

## Mitigation Strategy Framework

For each dimension scoring <=2, generate specific mitigations:

| Dimension | Common Mitigations |
|---|---|
| **Endpoint** | FDA Type B/C meeting to align on endpoint; EMA Scientific Advice; use co-primary endpoints |
| **Safety** | REMS proposal preemptively; independent DSMB with pre-specified stopping rules; long-term safety registry commitment |
| **Manufacturing** | Pre-Approval Inspection readiness; backup CMO; process validation at commercial scale before filing |
| **Competitive** | Head-to-head trial vs SOC; focus on underserved subpopulation; combination strategy |
| **Unmet Need** | Patient advocacy engagement; FDA rare disease programs; natural history study to document disease burden |
| **Precedent** | Pre-IND meeting; request FDA feedback on development plan; advisory committee simulation |

## Structured Output Format

```
REGULATORY RISK SCORECARD
============================
Program: [drug name / mechanism]
Indication: [target indication]

DIMENSION SCORES (1-5, higher = lower risk):
  1. Endpoint Validation:      [X/5] — [one-sentence rationale]
  2. Safety Signal Severity:   [X/5] — [one-sentence rationale]
  3. Manufacturing Complexity:  [X/5] — [one-sentence rationale]
  4. Competitive Context:       [X/5] — [one-sentence rationale]
  5. Unmet Need Magnitude:      [X/5] — [one-sentence rationale]
  6. Regulatory Precedent:      [X/5] — [one-sentence rationale]

AGGREGATE SCORE: [X.X / 5.0]
RISK RATING: [Low / Moderate / Elevated / High]
ESTIMATED REGULATORY PoS: [X-Y%]

RADAR CHART DATA:
  [Endpoint, Safety, Manufacturing, Competitive, Unmet Need, Precedent]
  [scores as array for visualization]

TOP 3 RISK FACTORS:
  1. [Dimension]: [specific risk description]
  2. [Dimension]: [specific risk description]
  3. [Dimension]: [specific risk description]

MITIGATION PRIORITIES:
  1. [Mitigation action] — Impact: [high/moderate] — Timeline: [months]
  2. [Mitigation action] — Impact: [high/moderate] — Timeline: [months]
  3. [Mitigation action] — Impact: [high/moderate] — Timeline: [months]

COMPARISON NOTE: [How this program's risk profile compares to typical
programs in this therapeutic area]
```

## Cross-Domain Connections

- **Biotech-venture/regulatory-precedent**: Precedent depth is a scoring dimension — the number of prior approvals with the same modality and endpoint directly determines the regulatory precedent score
- **Biotech-venture/endpoint-selection**: Endpoint validation strength is the highest-weighted scoring dimension (25%) — endpoint acceptance risk is the primary driver of regulatory risk
- **Biotech-venture/cmc-risk-assessor**: Manufacturing complexity is a scoring dimension (15% weight) — CMC readiness and process validation status feed directly into the manufacturing risk score
- **Biotech-venture/diligence-scorecard**: The aggregate regulatory risk score feeds the regulatory positioning pillar of the 8-pillar diligence scorecard
