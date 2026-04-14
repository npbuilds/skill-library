---
name: regulatory-precedent
description: >
  Catalog FDA and EMA regulatory precedents by therapeutic area, including expedited
  pathway statistics, approval basis, endpoint acceptance, advisory committee outcomes,
  and Complete Response Letter patterns. Reference when assessing regulatory pathway
  feasibility, predicting FDA behavior, or evaluating the regulatory risk of a novel
  approach to approval.
metadata:
  author: nirav
  version: "1.0"
  sources: "FDA CDER Annual Reports, FDA Expedited Programs Guidance, EMA PRIME data"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Regulatory Precedent — The Case Law of Drug Approval

Regulatory precedent is the strongest predictor of future regulatory outcomes. The FDA is a precedent-driven agency — knowing that the FDA accepted PFS as a primary endpoint in ovarian cancer, or rejected a particular PRO instrument in depression, directly informs what they will likely accept for a new drug in the same space.

This skill is the case law library. The pathway-analyzer uses it to recommend strategies; the regulatory-risk-scorer uses it to quantify risk.

## Key Concepts

### FDA Expedited Pathways

The FDA offers four expedited programs plus two special designations. Understanding which apply — and their actual statistics — is essential for biotech venture diligence.

| Pathway | Criteria | Benefit | Statistics (as of Sep 2025) |
|---|---|---|---|
| **Breakthrough Therapy (BTD)** | Serious condition + preliminary clinical evidence of substantial improvement over existing therapies | Intensive FDA guidance, organizational commitment, rolling review eligible | 1,622 requests, 634 granted (39%), 336 approved (54% of granted) |
| **Fast Track** | Serious condition + potential to address unmet medical need | Rolling review, more frequent FDA meetings | ~60% of novel drugs receive Fast Track |
| **Accelerated Approval** | Serious condition + surrogate endpoint reasonably likely to predict clinical benefit | Earlier approval based on surrogate; requires confirmatory trial | ~270 accelerated approvals since 1992; ~30 withdrawn/voluntarily withdrawn |
| **Priority Review** | Significant improvement in safety or effectiveness over available therapy | 6-month review (vs 10-month standard) | ~50% of novel drug approvals receive Priority Review |
| **Orphan Drug Designation** | Disease affecting <200,000 patients in US | 7-year market exclusivity, tax credits, fee waivers, smaller trials | ~5,000 designations granted; ~800 orphan drugs approved |
| **RMAT (Regenerative Medicine Advanced Therapy)** | Cell therapy, gene therapy, tissue engineering, or combination for serious condition | All BTD benefits plus potential for accelerated approval | ~100 designations granted since 2017 |

### EMA Equivalents

| FDA Pathway | EMA Equivalent | Key Difference |
|---|---|---|
| Breakthrough Therapy | PRIME (Priority Medicines) | Similar but fewer granted; requires "substantial treatment advantage" |
| Fast Track | Accelerated Assessment | Reduces review from 210 to 150 days |
| Accelerated Approval | Conditional Marketing Authorization (CMA) | Annual renewal required until full data submitted |
| Priority Review | (Included in Accelerated Assessment) | No separate designation |
| Orphan Drug | Orphan Medicinal Product | 10-year exclusivity (vs 7 in US); stricter criteria |

### Accelerated Approval Track Record

Accelerated approval is both an opportunity and a risk. Key patterns:

- **Oncology dominates**: ~65% of all accelerated approvals are in oncology
- **Surrogate endpoints used**: ORR (~40%), PFS (~25%), biomarker (~15%), other (~20%)
- **Confirmatory trial conversion**: ~60% of accelerated approvals have completed confirmatory trials successfully
- **Withdrawals increasing**: FDA has become more aggressive about withdrawing approvals when confirmatory trials fail (Makena, Aduhelm voluntary withdrawal, multiple oncology withdrawals 2021-2024)
- **Time to confirmatory data**: Median ~3-4 years; some programs exceed 10 years without confirmation

### Complete Response Letters (CRLs)

CRLs signal FDA rejection. Common CRL patterns:

| CRL Reason | Frequency | Implication for Diligence |
|---|---|---|
| Insufficient efficacy data | ~35% | Trial design or endpoint issue |
| Safety concerns | ~25% | May require REMS or additional studies |
| Manufacturing/CMC issues | ~20% | Often fixable but delays 12-18 months |
| Labeling/clinical pharmacology | ~10% | Usually resolvable |
| Inspection findings (GMP/GCP) | ~10% | Site or facility issues |

## Approval Precedent by Therapeutic Area

### Oncology Regulatory Patterns

- **IO combinations**: FDA has accepted PFS and ORR as primary endpoints for IO combos; OS increasingly expected for confirmatory
- **Tumor-agnostic approvals**: Precedent set by pembrolizumab (MSI-H/dMMR), larotrectinib (NTRK), entrectinib (NTRK/ROS1) — requires biomarker-defined population
- **Accelerated to full conversion**: Increasing scrutiny; several oncology accelerated approvals withdrawn when confirmatory trials failed
- **ctDNA/MRD**: FDA draft guidance (2024) exploring MRD as potential endpoint in heme malignancies; not yet accepted as standalone primary

### Rare Disease Regulatory Patterns

- **Single-arm trials**: FDA increasingly willing to accept single-arm trials with natural history comparators for ultra-rare diseases (<1,000 patients)
- **Biomarker endpoints**: Enzyme replacement therapies approved based on substrate reduction (Fabry, Gaucher, MPS)
- **Genetic therapies**: Gene therapy approvals based on durable biomarker response (Zolgensma, Luxturna, Casgevy)
- **Pediatric extrapolation**: FDA guidance allows extrapolation from adult data in some rare disease settings

### CNS Regulatory Patterns

- **Alzheimer's**: FDA accepted amyloid PET as surrogate for aducanumab (accelerated approval); lecanemab converted to full approval based on CDR-SB. FDA now expects both biomarker AND clinical endpoint
- **Neurodegeneration**: Functional endpoints (EDSS, UPDRS) remain standard; NfL biomarker gaining acceptance as secondary/exploratory
- **Psychiatry**: High placebo response rates make Phase 3 challenging; centralized rating and MMRM analysis becoming standard

## Advisory Committee (AdCom) Patterns

- ~75% of products with positive AdCom vote receive approval
- ~25% of products with negative AdCom vote still receive approval (FDA is not bound by AdCom)
- Controversial mechanisms of action are more likely to go to AdCom
- First-in-class drugs go to AdCom more frequently than follow-on drugs

## When This Applies

- When pathway-analyzer needs to recommend a regulatory strategy
- When assessing whether a surrogate endpoint has FDA precedent in a specific indication
- When evaluating CRL risk for a pending NDA
- When comparing US vs EU regulatory feasibility
- When regulatory-risk-scorer needs precedent data for scoring dimensions

## Cross-Domain Connections

- **Biotech-venture/pathway-analyzer**: Uses precedent data to recommend optimal regulatory strategy
- **Biotech-venture/regulatory-risk-scorer**: Uses precedent as a scoring dimension (more precedent = lower risk)
- **Biotech-venture/endpoint-selection**: Endpoint acceptance is fundamentally a precedent question
- **Biotech-venture/pos-calculator**: Regulatory designation (BTD, orphan) modifies PoS
- **Investing/macro-cycles**: Regulatory regimes have cycles — permissive vs restrictive phases
- **Research/spelunker**: Deep research on specific regulatory precedents for novel endpoints
