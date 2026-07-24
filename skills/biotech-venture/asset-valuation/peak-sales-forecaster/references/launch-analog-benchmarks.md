# Launch Analog Benchmarks — Extended Reference

Uptake/peak-sales reference for the **peak-sales-forecaster** SKILL: S-curve launch archetypes, pricing-by-category, compliance/adherence, and peak-sales analogs used to parameterize a bottom-up forecast. This doc owns the **uptake and peak** side; the erosion tail, order-of-entry detail, and refuted-lore list live in the market-dynamics reference (cross-ref below).

**Provenance legend.** `int` = internal consensus estimate (from this skill's own quick-reference prose; no external source). `ext✓` = externally verified against a real citation (VERIFIED FACTS block). `statutory` = stable legal/regulatory constant. Tables carried over verbatim from the quick-reference are internal estimates and are tagged `int` at the section level; treat their analog names as illustrative, not audited financials.

## Uptake Drivers — Underlying Population Growth (int)

| Factor | Annual Growth Rate | Driver |
|---|---|---|
| Incidence/prevalence growth | +1-3%/yr | Aging population, improved diagnosis |
| Biomarker testing adoption | +3-8%/yr (if relevant) | NGS penetration, companion diagnostic uptake |
| Line expansion (label broadening) | Step-change | New indications add discrete patient pools |
| Geographic expansion | Step-change | EU, Japan launches typically 1-2yr post-US |

## S-Curve Launch Archetypes (int)

Time-to-peak and peak-share ranges are internal estimates; analog names are illustrative anchors, not verified share figures.

| Launch Profile | Time to Peak Share | Peak Share Range | Analog Examples |
|---|---|---|---|
| Best-in-class, high unmet need | 2-3 years | 40-60% | Keytruda 1L NSCLC, Humira RA |
| Differentiated entrant, competitive market | 3-5 years | 15-30% | Opdivo 2L melanoma post-Keytruda |
| Me-too, crowded market | 4-6 years | 5-15% | Late PD-1 entrants in NSCLC |
| First-in-class, novel mechanism | 3-4 years | 30-50% | Ibrutinib in CLL, semaglutide in obesity |
| Rare disease, limited competition | 1-2 years | 60-80% | Spinraza in SMA (before gene therapy) |

**Order-of-entry anchor (ext✓, Porath 2018).** Empirically, share advantage decays with entry order: pioneer ~+33pt, 2nd ~19pt, 3rd ~13pt, stabilizing near ~6pt for late entrants. Use this to sanity-check the peak-share ranges above when several competitors are modeled — the "me-too, crowded market" band is consistent with the late-entry stabilization level. Full order-of-entry detail is in the market-dynamics reference.

## Pricing by Category (int)

US annual price ranges with regional discounts; internal estimates.

| Category | US Annual Price Range | EU5 Discount | Japan Discount |
|---|---|---|---|
| Oncology (IV, solid tumor) | $150,000-$250,000 | 30-50% | 20-40% |
| Oncology (oral, targeted) | $100,000-$180,000 | 30-50% | 20-40% |
| Rare disease (enzyme replacement) | $200,000-$500,000 | 10-30% | 10-20% |
| Rare disease (gene therapy, one-time) | $1,000,000-$3,500,000 | 20-40% | 20-30% |
| Immunology (biologic, chronic) | $30,000-$80,000 | 40-60% | 30-50% |
| Obesity (GLP-1 RA, chronic) | $12,000-$20,000 | 40-60% | 30-50% |
| Large-population chronic disease | $5,000-$30,000 | 40-60% | 30-50% |

## Compliance / Adherence by Modality (int)

Annual compliance drives the gap between eligible-and-treated patients and realized revenue.

| Modality/Setting | Annual Compliance Rate | Key Drivers |
|---|---|---|
| IV infusion (clinic-administered) | 85-95% | Physician-directed, high adherence |
| Oral daily (oncology) | 70-85% | Pill fatigue, side effects |
| Subcutaneous self-injection (weekly) | 75-85% | Injection burden, refrigeration |
| Subcutaneous self-injection (monthly) | 85-90% | Less frequent, better persistence |
| Gene therapy (one-time) | 100% | Single administration |

## Peak-Sales Analogs by Category (int)

Peak-sales ranges and benchmark figures below are internal estimates from the quick-reference. Where a category benchmark can be checked against a real source, the verified figure is noted separately (see next section) — do not treat the parenthetical peak figures here as audited.

| Category | Peak Sales Range | Benchmark Drug(s) |
|---|---|---|
| Oncology (solid tumor, single indication) | $1-5B | Tagrisso ($5.8B), Imbruvica ($4.5B peak) |
| Oncology (pan-tumor/multi-indication) | $5-25B | Keytruda ($25B), Opdivo ($9B) |
| Rare disease | $500M-$3B | Spinraza ($2B peak), Trikafta ($8.9B — CF is borderline rare) |
| Immunology (biologic) | $3-15B | Humira ($21B peak — int), Dupixent ($13B+) |
| Obesity / metabolic (GLP-1) | $5-30B+ | Wegovy ($8B+ and growing), Mounjaro ($12B+) |
| Gene therapy (single indication) | $200M-$1B | Zolgensma ($1.4B peak) |

## Verified Analog Figures (ext✓)

Use these in place of the internal parentheticals above when citing to a diligence audience.

| Drug (INN) | Verified figure | Notes | Source |
|---|---|---|---|
| Keytruda (pembrolizumab) | 2023 revenue **$25.011B** (up from $20.937B in 2022) | World's #1 drug in 2023; 2023 is **not yet peak** — US LOE ~2028, so the S-curve is still rising | GEN Top-10 |
| Humira (adalimumab) | **~$200B cumulative** since 2002 (through 2022; ~$237-238B through 2024) | US net revenue fell **-45%** in the first biosimilar year (2023). Do **not** assert a precise peak-year figure — the "$21B peak" in the table is an internal approximation (`int`) | BioPharma Dive |

**Refuted-lore caution.** A specific "Humira $20.7B peak in 2021" claim was adversarially refuted (0-3). The immunology-biologic table's "$21B peak" is an internal round-number placeholder, not a sourced peak. When a Humira peak number is load-bearing, cite the cumulative and the -45% first-year erosion instead, and defer to the market-dynamics refuted-lore list.

## Error Handling (int)

| Scenario | Response |
|---|---|
| No clear launch analog | Use therapeutic-area averages for S-curve parameters; widen confidence range; present multiple penetration scenarios |
| First-in-class with no pricing precedent | Benchmark against nearest therapeutic analog by value delivered; apply ICER threshold analysis ($100-150K/QALY); present price sensitivity table |
| Rapidly evolving competitive landscape | Model multiple competitive scenarios (current, expected, worst-case); assign probabilities to each; present expected-value weighted forecast |
| Indication too new for prevalence data | Use bottom-up clinical trial screening data to estimate eligible population; flag as high-uncertainty input |
| Global forecast requested but limited data outside US | Model US in detail; apply regional multipliers from patient-population-sizer; state which geographies are extrapolated vs. modeled |

## Statutory Anchors (statutory)

Stable constants worth holding fixed while the estimates above drift.

| Constant | Value | Use |
|---|---|---|
| US orphan-disease threshold | <200,000 US patients | Caps the addressable population for rare-disease pricing bands |
| NCE market exclusivity | 5 years | Floor on the pre-erosion revenue window regardless of patent estate |

## Source Vintage & Staleness

- **Verified analog revenues (ext✓)** are 2022-2024 annual figures. Keytruda in particular is still pre-LOE (US ~2028), so its number climbs year over year — re-pull each annual report cycle; a figure more than one reporting year old understates it.
- **Pricing bands (int)** stale on the order of 1-2 years: US net pricing moves with IRA Medicare negotiation, biosimilar entry, and PBM rebate dynamics. GLP-1/obesity pricing is the fastest-moving row here.
- **S-curve archetypes and compliance rates (int)** are the most durable — structural, not tied to a single asset — but the named analogs age as new launches reset the "best-in-class" bar.
- **Peak-sales analog table (int)** is the fastest to go stale on the parentheticals: growing franchises (Wegovy, Mounjaro) are explicitly still climbing, and any "peak" label on a pre-LOE drug is provisional.

**Usage note.** This reference serves the **peak-sales-forecaster** SKILL (asset-valuation) as the uptake/peak-sales side of launch modeling. For the erosion tail, full order-of-entry share detail, and the refuted-lore list, cross-reference `skills/biotech-venture/competitive-intelligence/market-dynamics/references/launch-and-erosion-benchmarks.md`. Population inputs come from `patient-population-sizer`; only figures tagged `ext✓` or `statutory` should be cited as fact to a diligence audience — everything tagged `int` is an internal planning estimate.
