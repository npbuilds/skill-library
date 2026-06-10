# Peak Sales Forecaster — Quick Reference


## Input

| Parameter | Required? | Example |
|---|---|---|
| Treatable patient population | Yes | 19,000 (from patient-population-sizer) |
| Geography | Yes | US, US + EU5, Global |
| Pricing estimate or range | Recommended | $150,000-$200,000/yr (oncology IV) |
| Competitive landscape | Recommended | 3 approved competitors, 2 Phase 3 |
| Expected launch year | Recommended | 2029 |
| Product differentiation | Recommended | Superior efficacy, better safety, oral formulation |
| Line of therapy | Yes | 1L metastatic |
| Modality | Recommended | Monoclonal antibody |

## Quick Reference

| Factor | Annual Growth Rate | Driver |
|---|---|---|
| Incidence/prevalence growth | +1-3%/yr | Aging population, improved diagnosis |
| Biomarker testing adoption | +3-8%/yr (if relevant) | NGS penetration, companion diagnostic uptake |
| Line expansion (label broadening) | Step-change | New indications add discrete patient pools |
| Geographic expansion | Step-change | EU, Japan launches typically 1-2yr post-US |

## Quick Reference

| Launch Profile | Time to Peak Share | Peak Share Range | Analog Examples |
|---|---|---|---|
| **Best-in-class, high unmet need** | 2-3 years | 40-60% | Keytruda 1L NSCLC, Humira RA |
| **Differentiated entrant, competitive market** | 3-5 years | 15-30% | Opdivo 2L melanoma post-Keytruda |
| **Me-too, crowded market** | 4-6 years | 5-15% | Late PD-1 entrants in NSCLC |
| **First-in-class, novel mechanism** | 3-4 years | 30-50% | Ibrutinib in CLL, semaglutide in obesity |
| **Rare disease, limited competition** | 1-2 years | 60-80% | Spinraza in SMA (before gene therapy) |

## Quick Reference

| Category | US Annual Price Range | EU5 Discount | Japan Discount |
|---|---|---|---|
| Oncology (IV, solid tumor) | $150,000-$250,000 | 30-50% | 20-40% |
| Oncology (oral, targeted) | $100,000-$180,000 | 30-50% | 20-40% |
| Rare disease (enzyme replacement) | $200,000-$500,000 | 10-30% | 10-20% |
| Rare disease (gene therapy, one-time) | $1,000,000-$3,500,000 | 20-40% | 20-30% |
| Immunology (biologic, chronic) | $30,000-$80,000 | 40-60% | 30-50% |
| Obesity (GLP-1 RA, chronic) | $12,000-$20,000 | 40-60% | 30-50% |
| Large-population chronic disease | $5,000-$30,000 | 40-60% | 30-50% |

## Quick Reference

| Modality/Setting | Annual Compliance Rate | Key Drivers |
|---|---|---|
| IV infusion (clinic-administered) | 85-95% | Physician-directed, high adherence |
| Oral daily (oncology) | 70-85% | Pill fatigue, side effects |
| Subcutaneous self-injection (weekly) | 75-85% | Injection burden, refrigeration |
| Subcutaneous self-injection (monthly) | 85-90% | Less frequent, better persistence |
| Gene therapy (one-time) | 100% | Single administration |

## Quick Reference

| Category | Peak Sales Range | Benchmark Drug(s) |
|---|---|---|
| Oncology (solid tumor, single indication) | $1-5B | Tagrisso ($5.8B), Imbruvica ($4.5B peak) |
| Oncology (pan-tumor/multi-indication) | $5-25B | Keytruda ($25B), Opdivo ($9B) |
| Rare disease | $500M-$3B | Spinraza ($2B peak), Trikafta ($8.9B — CF is borderline rare) |
| Immunology (biologic) | $3-15B | Humira ($21B peak), Dupixent ($13B+) |
| Obesity / metabolic (GLP-1) | $5-30B+ | Wegovy ($8B+ and growing), Mounjaro ($12B+) |
| Gene therapy (single indication) | $200M-$1B | Zolgensma ($1.4B peak) |

## Error Handling

| Scenario | Response |
|---|---|
| No clear launch analog | Use therapeutic-area averages for S-curve parameters; widen confidence range; present multiple penetration scenarios |
| First-in-class with no pricing precedent | Benchmark against nearest therapeutic analog by value delivered; apply ICER threshold analysis ($100-150K/QALY); present price sensitivity table |
| Rapidly evolving competitive landscape | Model multiple competitive scenarios (current, expected, worst-case); assign probabilities to each; present expected-value weighted forecast |
| Indication too new for prevalence data | Use bottom-up clinical trial screening data to estimate eligible population; flag as high-uncertainty input |
| Global forecast requested but limited data outside US | Model US in detail; apply regional multipliers from Step 7 of patient-population-sizer; clearly state which geographies are extrapolated vs. modeled |
