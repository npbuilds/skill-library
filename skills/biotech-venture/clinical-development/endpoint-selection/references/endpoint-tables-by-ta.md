# Endpoint Tables — Extended Therapeutic Area Reference

## Oncology Endpoint Decision Tree

```
Is the goal curative / adjuvant?
  YES -> DFS or EFS as primary; OS as secondary
  NO -> Is there an unmet need with no SOC?
    YES -> ORR (accelerated approval eligible)
      -> Is the ORR durable? DOR > 6 months strengthens case
    NO -> Is PFS accepted in this tumor type?
      YES -> PFS as primary; OS as key secondary
      NO -> OS as primary (requires larger trial, longer follow-up)
```

## Endpoint Acceptance Matrix — Oncology by Tumor Type

| Tumor Type | ORR (Accel) | PFS (Full) | OS (Full) | DFS (Adjuvant) | Notes |
|---|---|---|---|---|---|
| NSCLC | Yes | Debated | Yes | Yes (adjuvant IO) | PFS accepted in some settings but OS increasingly expected |
| Breast (HER2+) | Yes | Yes | Yes | Yes (neoadjuvant pCR) | pCR accepted for neoadjuvant setting |
| Breast (TNBC) | Yes | Yes (IO combos) | Yes | Limited | EFS emerging in early-stage |
| CRC | Yes | Yes | Yes | Yes (Stage III DFS) | DFS well-validated in adjuvant |
| Ovarian | Yes | Yes | Yes | N/A | PFS widely accepted |
| RCC | Yes | Yes | Yes | Yes (adjuvant) | PFS + ORR accepted |
| Melanoma | Yes | Yes | Yes | Yes (RFS) | Relapse-free survival in adjuvant |
| AML | Yes (CR+CRh) | N/A | Yes | N/A | Complete remission rate standard |
| MM | Yes (ORR, sCR) | Yes (PFS) | Yes | N/A | PFS well-accepted |
| DLBCL | Yes (CR) | N/A | Yes (EFS) | N/A | CR rate for CAR-T accelerated approvals |

## CNS Endpoint Requirements

### Alzheimer's — Current FDA Expectations (Post-Aducanumab/Lecanemab)

| Component | Required? | Endpoint | Notes |
|---|---|---|---|
| Cognitive | Yes (co-primary) | ADAS-Cog-13 or CDR-SB | CDR-SB preferred post-lecanemab |
| Functional | Yes (co-primary) | ADCS-ADL or CDR-SB | Must show functional benefit, not just cognitive |
| Biomarker | Expected (key secondary) | Amyloid PET, p-tau217 | Biomarker evidence strengthens case |
| Global | Recommended | CIBIC+ or CDR global | Supports clinical meaningfulness |
| Duration | 18 months minimum | — | Shorter for accelerated approval with biomarker |

### Multiple Sclerosis

| Endpoint | Setting | Status |
|---|---|---|
| Annualized Relapse Rate (ARR) | RMS (relapsing) | Standard primary |
| EDSS progression (confirmed 3/6 month) | Progressive MS | Standard primary for PPMS/SPMS |
| New/enlarging T2 lesions (MRI) | RMS | Key secondary; accepted as primary in some settings |
| Brain volume loss | All MS | Exploratory; not accepted as primary |
| MSFC (composite) | All MS | Composite; 9-HPT, T25FW, PASAT |

## Cardiovascular CVOT Requirements

Post-2008 (rosiglitazone), all new diabetes drugs must demonstrate cardiovascular safety.

| Requirement | Details |
|---|---|
| **CVOT design** | Randomized, placebo-controlled, event-driven |
| **Primary endpoint** | 3-point MACE (CV death, nonfatal MI, nonfatal stroke) |
| **Non-inferiority margin** | Upper bound of 95% CI for HR must be <1.3 (pre-approval) or <1.8 (post-approval) |
| **Minimum events** | Typically 600-1,000+ MACE events required |
| **Trial size** | 5,000-17,000 patients typical |
| **Duration** | 2-5+ years of follow-up |

## Rare Disease Endpoint Flexibility

The FDA applies a risk-benefit framework with greater flexibility for rare diseases:

| Population Size | Typical Endpoint Flexibility | Trial Design |
|---|---|---|
| >10,000 patients | Standard clinical endpoints expected | Randomized controlled trial |
| 1,000-10,000 | Functional endpoints, biomarker surrogates acceptable | Randomized; possibly smaller |
| 200-1,000 | Single-arm with external control possible | Natural history comparator |
| <200 | Biomarker-only surrogate may suffice | Single-arm, n-of-1, case series |

## Digital Endpoints — Emerging Landscape

| Digital Endpoint | Disease | Status | Technology |
|---|---|---|---|
| 6-minute walk distance (digital) | Heart failure, PAH | Validated | Wearable accelerometer |
| Step count / activity levels | Neuromuscular, COPD | Exploratory | Wearable |
| Sleep architecture | Insomnia, depression | Exploratory | Wearable/app |
| Voice biomarkers | Depression, Parkinson's | Research | Smartphone |
| Continuous glucose monitoring | Diabetes | Validated (CGM metrics) | Sensor |
| Seizure detection | Epilepsy | Emerging | Wearable EEG |

FDA has not yet accepted a purely digital endpoint as a primary endpoint for pivotal trials, but CGM-derived metrics (time-in-range) are gaining traction for diabetes.
