---
name: endpoint-selection
description: >
  Apply endpoint selection frameworks for clinical trials across therapeutic areas,
  distinguishing validated surrogate endpoints from clinical endpoints and mapping
  FDA/EMA acceptance precedent. Reference when evaluating whether a trial's primary
  endpoint is approvable, comparing endpoint strategies across competitors, or assessing
  the regulatory risk of a novel endpoint.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Endpoint Selection — Where Clinical Science Meets Regulatory Acceptance

Endpoint selection is the single most consequential decision in clinical trial design. Choose a validated surrogate and you get accelerated approval in 2 years. Choose a clinical endpoint that requires 5 years of follow-up and you burn $200M more in development costs. Choose an endpoint the FDA does not accept and you get a Complete Response Letter.

This is where the physician-scientist adds unique value in venture diligence. Most financial analysts can model an rNPV; few can independently assess whether a trial's primary endpoint will satisfy the FDA.

## Key Concepts

### Endpoint Taxonomy

| Category | Definition | Example | Regulatory Implication |
|---|---|---|---|
| **Clinical endpoint** | Measures how a patient feels, functions, or survives | Overall Survival (OS), Major Adverse Cardiac Events (MACE) | Gold standard; supports full approval |
| **Surrogate endpoint** | Lab measurement or physical sign that substitutes for a clinical endpoint | Objective Response Rate (ORR), HbA1c, LDL-C | Can support accelerated approval if "reasonably likely to predict clinical benefit" |
| **Validated surrogate** | Surrogate with established relationship to clinical outcome | LDL-C for CV events, viral load for HIV | Supports full approval |
| **Patient-reported outcome (PRO)** | Patient's own assessment of symptoms, function, quality of life | EORTC QLQ-C30, SF-36, visual analog scale | Increasingly important; FDA has specific PRO guidance |
| **Composite endpoint** | Combines multiple events into a single endpoint | MACE (CV death + MI + stroke) | Increases event rate; components must be clinically meaningful |
| **Digital endpoint** | Measured by wearable/sensor/app | Step count, sleep architecture, voice biomarkers | Emerging; limited regulatory precedent |

### Surrogate Validation Framework (Prentice Criteria)

A valid surrogate endpoint must satisfy:
1. The surrogate is correlated with the clinical endpoint
2. The treatment effect on the surrogate correlates with the treatment effect on the clinical endpoint
3. The entire treatment effect on the clinical endpoint is mediated through the surrogate

In practice, few surrogates satisfy all three Prentice criteria. The FDA uses a pragmatic standard: "reasonably likely to predict clinical benefit" for accelerated approval.

## Endpoint Tables by Therapeutic Area

### Oncology

| Endpoint | Type | FDA Status | Typical Use | Key Considerations |
|---|---|---|---|---|
| **Overall Survival (OS)** | Clinical | Gold standard for full approval | Phase 3 primary | Requires long follow-up; confounded by crossover and subsequent therapy |
| **Progression-Free Survival (PFS)** | Surrogate | Accepted for full approval in some settings | Phase 3 primary or co-primary | RECIST-based; accepted in ovarian, breast, CRC; debated in NSCLC |
| **Objective Response Rate (ORR)** | Surrogate | Supports accelerated approval | Phase 2 primary, Phase 3 secondary | Rapid readout; does not capture durability |
| **Duration of Response (DOR)** | Surrogate | Supports accelerated approval (with ORR) | Phase 2/3 secondary | Context-dependent; median DOR >6 months generally expected |
| **Disease-Free Survival (DFS)** | Surrogate | Accepted in adjuvant settings | Phase 3 primary (adjuvant) | Validated in colon cancer (Stage III), breast cancer |
| **Complete Response (CR) rate** | Surrogate | Supports accelerated in heme malignancies | Phase 2 primary (heme) | MRD-negativity increasingly used alongside CR |
| **Minimal Residual Disease (MRD)** | Surrogate | Under evaluation; FDA guidance draft 2024 | Phase 2/3 (heme) | Highly sensitive; not yet validated as standalone |
| **Patient-Reported Outcomes** | PRO | Supports labeling claims | Phase 3 secondary | EORTC QLQ-C30, FACT scales; must use validated instrument |

### CNS / Neurology

| Endpoint | Type | FDA Status | Disease | Key Considerations |
|---|---|---|---|---|
| **ADAS-Cog** | Clinical | Accepted (with functional co-primary) | Alzheimer's | Must be paired with ADCS-ADL or CDR-SB |
| **CDR-SB** | Clinical | Accepted as primary | Alzheimer's | Clinical Dementia Rating Sum of Boxes; used by lecanemab |
| **EDSS** | Clinical | Accepted | Multiple Sclerosis | Expanded Disability Status Scale; insensitive to change |
| **Annualized Relapse Rate** | Clinical | Accepted | Multiple Sclerosis | More sensitive than EDSS; standard primary |
| **UPDRS** | Clinical | Accepted | Parkinson's | Unified Parkinson's Disease Rating Scale |
| **Amyloid PET** | Surrogate | Supported accelerated approval (aducanumab) | Alzheimer's | Highly controversial; amyloid clearance ≠ clinical benefit is debated |
| **NfL (neurofilament light)** | Biomarker | Exploratory / emerging | Multiple diseases | Promising fluid biomarker; not yet validated surrogate |

### Cardiovascular

| Endpoint | Type | FDA Status | Key Considerations |
|---|---|---|---|
| **MACE (3-point)** | Clinical composite | Gold standard | CV death + nonfatal MI + nonfatal stroke |
| **MACE (4-point)** | Clinical composite | Accepted | Adds hospitalization for unstable angina |
| **Heart failure hospitalization** | Clinical | Accepted (with CV death) | Co-primary in HF trials |
| **LDL-C reduction** | Validated surrogate | Supports full approval | Validated by statin trials; accepted for PCSK9, ezetimibe |
| **HbA1c** | Validated surrogate | Supports approval (diabetes) | Must also show CV safety (CVOT requirement post-2008) |
| **eGFR slope** | Surrogate | Accepted in CKD | FDA guidance 2023; validates for CKD progression |

### Rare Disease

| Approach | Description | FDA Attitude |
|---|---|---|
| **Functional endpoints** | Disease-specific scales (6MWT, FVC, motor function) | Accepted when validated for the condition |
| **Biomarker surrogates** | Enzyme levels, substrate reduction, genetic correction | Often accepted for accelerated approval given small populations |
| **Natural history comparison** | Single-arm trial vs external natural history data | Increasingly accepted for ultra-rare (<1,000 patients) |
| **Composite endpoints** | Combine rare events to increase statistical power | Acceptable if components are clinically meaningful |

### Immunology / Inflammation

| Endpoint | Disease | Type | FDA Status |
|---|---|---|---|
| **ACR20/50/70** | Rheumatoid Arthritis | Clinical composite | Standard primary |
| **DAS28-CRP** | RA | Clinical composite | Co-primary or secondary |
| **PASI 75/90/100** | Psoriasis | Clinical | Standard primary; PASI 90 increasingly expected |
| **EASI-75** | Atopic Dermatitis | Clinical | Standard primary |
| **Mayo Score** | Ulcerative Colitis | Clinical composite | Standard primary; endoscopic subscore critical |
| **CDAI / SES-CD** | Crohn's Disease | Clinical + endoscopic | PRO2 (patient-reported) emerging as co-primary |

## When This Applies

- Evaluating whether a company's trial has the right primary endpoint for FDA approval
- Comparing endpoint strategies across competitors in the same indication
- Assessing whether an accelerated approval pathway is viable based on endpoint choice
- Identifying regulatory risk: "Has the FDA ever accepted this endpoint in this indication?"
- Informing trial-design-optimizer about endpoint feasibility and regulatory precedent

## Cross-Domain Connections

- **Biotech-venture/trial-design-optimizer**: Endpoint choice drives trial design (sample size, duration, cost)
- **Biotech-venture/regulatory-precedent**: Approval precedent by endpoint informs pathway-analyzer
- **Biotech-venture/clinical-differentiator**: Comparing endpoints across competitors reveals differentiation
- **Biotech-venture/pos-calculator**: Endpoint type affects PoS (validated surrogate → higher Phase 3 success)
- **Biotech-venture/regulatory-risk-scorer**: Endpoint validation strength is a scoring dimension
