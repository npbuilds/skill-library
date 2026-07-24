# Designation Eligibility & Grant Rates — Extended Reference

This doc holds the eligibility-criteria matrix for FDA expedited/incentive designations (Breakthrough Therapy, Fast Track, Accelerated Approval, Priority Review, Orphan, RMAT) and their EMA equivalents (PRIME, Conditional Marketing Authorization, Accelerated Assessment, Orphan Medicinal Product, ATMP), plus a consolidated grant/conversion summary. It serves the **pathway-analyzer** SKILL. Eligibility criteria are largely statutory; grant-rate detail by therapeutic area lives in the regulatory-precedent approval-precedent-database (referenced, not duplicated here).

**Provenance legend:**
- `statutory` — a stable legal/regulatory constant (eligibility bar, exclusivity term, prevalence threshold, review-clock length).
- `int` — internal consensus estimate carried from the pathway-analyzer SKILL prose / quick-reference; no external citation.
- `ext✓` — externally verified with a real citation. *(No external verified-facts block was supplied for this doc; no figure here carries `ext✓`. Treat every non-statutory number as `int`.)*

---

## FDA Designation Eligibility Matrix

| Designation | Core eligibility bar | Evidence stage required | Provenance | Primary benefit |
|---|---|---|---|---|
| **Breakthrough Therapy (BTD)** | Serious/life-threatening condition **AND** preliminary clinical evidence of *substantial improvement* over available therapy on a clinically significant endpoint | Preliminary clinical (can be Phase 1/2, even single-arm) | statutory (bar); int (stage detail) | Intensive FDA engagement; organizational commitment; usually paired w/ Priority Review |
| **Fast Track** | Serious condition **AND** potential to address an *unmet medical need* (lower bar than BTD — "potential to address") | Nonclinical or clinical data supporting potential | statutory (bar); int (bar-relativity) | Rolling review + frequent FDA meetings |
| **Accelerated Approval** | Serious condition **AND** approval based on a *surrogate endpoint reasonably likely to predict clinical benefit* (or intermediate clinical endpoint) | Surrogate/intermediate endpoint data | statutory | Earlier approval; **confirmatory post-marketing trial required** |
| **Priority Review** | Drug offers *significant improvement* in safety or effectiveness of treatment/diagnosis/prevention | Complete application at filing | statutory (bar); int (grant frequency) | 6-month review vs 10-month standard |
| **Orphan Drug** | Disease/condition affecting **<200,000 US patients** (or no expectation of recovering development cost) | Designation available pre-approval, any stage | statutory | 7-yr market exclusivity; 25% clinical-trial tax credit; PDUFA fee waiver; smaller trials accepted |
| **RMAT** | *Regenerative medicine therapy* (cell therapy, gene therapy, tissue engineering, or combination product) for a serious condition **AND** preliminary clinical evidence of potential to address unmet need | Preliminary clinical | statutory | All BTD benefits **plus** potential accelerated approval; earlier surrogate discussions |

### Serious-condition gate (threshold test for all four expedited programs)

| Bucket | Examples | Provenance |
|---|---|---|
| Clearly serious | Oncology, rare genetic disease, heart failure, ALS, organ transplant | int |
| Context-dependent | Moderate-severe psoriasis (yes) vs mild acne (no); NASH w/ fibrosis (yes) vs simple steatosis (debatable) | int |
| Typically not serious | Seasonal allergies, mild eczema, erectile dysfunction, cosmetic indications | int |

### Orphan quantitative incentives (from SKILL)

| Incentive | Value | Provenance |
|---|---|---|
| US market exclusivity | 7 years upon approval | statutory |
| Clinical-trial tax credit | 25% of clinical trial costs | statutory |
| PDUFA fee waiver | ~$3.4M fee (2025) waived | int (fee amount); statutory (waiver) |
| Trial-size relief | Smaller trials accepted | int |

---

## EMA Equivalents Eligibility Matrix

| FDA analog | EMA mechanism | Core eligibility bar | Provenance | Key structural difference |
|---|---|---|---|---|
| Breakthrough Therapy | **PRIME** (Priority Medicines) | *Substantial treatment advantage* for unmet need; stricter than BTD | statutory (bar); int (relative strictness) | Fewer granted (~50/yr vs FDA's ~100 BTDs/yr) |
| Fast Track | **Accelerated Assessment** | *Major interest for public health* | statutory | Review clock 210 → 150 days |
| Accelerated Approval | **Conditional Marketing Authorization (CMA)** | Positive benefit-risk on incomplete data; obligations to complete | statutory | **Annual renewal**; obligations must be fulfilled within agreed timeline |
| Priority Review | (folded into Accelerated Assessment) | No standalone designation | statutory | Built into accelerated timeline |
| Orphan Drug | **Orphan Medicinal Product** | Prevalence **<5 in 10,000** in EU | statutory | 10-year exclusivity (vs 7 in US) |
| RMAT | **ATMP classification** | Advanced Therapy Medicinal Product | statutory | Separate framework via CAT (Committee for Advanced Therapies) |

---

## Consolidated Grant / Conversion Summary

All figures below are drawn from the pathway-analyzer SKILL prose (`int`) unless tagged otherwise. **For BTD grant rates broken out by therapeutic area, and for BTD-vs-non-BTD development-time impact, do NOT use this doc — see the regulatory-precedent [approval-precedent-database](../../regulatory-precedent/references/approval-precedent-database.md)**, which owns those tables.

| Designation | Grant / prevalence stat | Conversion to approval | Provenance |
|---|---|---|---|
| **BTD** | 634 granted of 1,622 requests (~39% grant rate) | 336 of 634 ultimately approved (~54% conversion) | int |
| **Fast Track** | ~60% of novel drugs receive it | — | int |
| **Accelerated Approval** | ~270 accelerated approvals since 1992 | ~30 withdrawn when confirmatory trials failed | int |
| **Priority Review** | ~50% of novel drugs receive it | Often granted alongside BTD or Fast Track | int |
| **Orphan** | ~5,000 designations granted | ~800 orphan drugs approved | int |
| **RMAT** | ~100 designations granted since 2017 | — (many still in development) | int |
| **PRIME (EMA)** | ~50/year granted | — | int |
| **BTD-by-area, dev-time impact** | *see approval-precedent-database* | *see approval-precedent-database* | pointer |

### Timeline / financial impact (from SKILL — internal estimates)

| Pathway | Standard | With designation | Time saved | Financial impact | Provenance |
|---|---|---|---|---|---|
| BTD | ~10 yrs IND→approval | ~6.9 yrs median | ~3.1 yrs | $300–500M dev-cost savings | int |
| Fast Track (rolling review) | 10-mo review | 6–8 mo effective | 2–4 mo | Modest; value is FDA engagement | int |
| Accelerated Approval | Ph3 OS trial (5+ yrs) | Ph2 surrogate (2–3 yrs) | 2–3 yrs to initial approval | $150–300M; confirmatory trial still needed | int |
| Priority Review | 10-mo PDUFA | 6-mo PDUFA | 4 mo | ~$50–100M earlier revenue | int |
| Orphan | Standard | Often smaller trials | Variable | $50–200M reduced trial cost + 7-yr exclusivity | int |

*Note on internal consistency:* the SKILL's BTD headline (~3.1 yrs / ~6.9 yr median) and the approval-precedent-database's BTD figure (~2.8 yrs / ~6.3 yr median) are independent estimates of the same effect and differ modestly; cite whichever source you are anchoring to and do not average them silently.

---

## Source Vintage & Staleness

- **Eligibility criteria (`statutory`)** — slow-staling. These are set by statute/regulation (FDCA expedited-program provisions, Orphan Drug Act, EU Orphan Regulation, ATMP framework) and change only with legislation or major guidance. The Accelerated Approval confirmatory-trial regime is the most active area (FDAORA-era tightening); re-check if advising on withdrawal risk.
- **Grant/conversion counts (`int`)** — moderate-staling. BTD request/grant tallies, orphan designation counts, and RMAT counts are cumulative and drift upward every cycle; the SKILL snapshot should be refreshed roughly annually against FDA CDER/CBER reporting.
- **Fee amounts (`int`)** — fast-staling. PDUFA fees reset annually (the ~$3.4M figure is 2025); always confirm the current fiscal-year fee.
- **EMA cadence (`int`)** — moderate-staling. PRIME and CMA volumes shift year to year.

When any of these are load-bearing for a diligence conclusion, verify against the primary regulator source rather than this reference.

---

**Usage note.** This doc supports the **pathway-analyzer** SKILL (`skills/biotech-venture/regulatory-strategy/pathway-analyzer/SKILL.md`). It provides the eligibility-criteria matrix and a consolidated grant/conversion summary; it deliberately does **not** reproduce the BTD-by-therapeutic-area grant table or the BTD development-time-impact stats, which are owned by the sibling **regulatory-precedent** [approval-precedent-database](../../regulatory-precedent/references/approval-precedent-database.md). Cross-reference that file for area-level precedent, and the pathway-analyzer SKILL for the decision tree, pathway-stacking logic, and dual-filing strategy.
