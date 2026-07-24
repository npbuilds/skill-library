# Epidemiology by Indication — Extended Reference

Primary-sourced prevalence, incidence, survival, and treatment-funnel base rates for patient-population sizing. Every figure carries a source and vintage. **Cancer figures refresh annually (SEER/ACS) — re-pull before a diligence memo.** All are model-based estimates with uncertainty; the round-number "lore" versions are flagged where they diverge from observed data.

## Oncology — US Incidence & Survival (SEER Cancer Stat Facts, 2026)

Incidence/mortality estimates from ACS Cancer Facts & Figures 2026 (republished by SEER); 5-yr relative survival from SEER 21 (excl. IL), 2016–2022.

| Indication | New US cases 2026 | % of all new cancers | 5-yr rel. survival | Incidence /100k/yr | Prevalence (living w/ disease) |
|---|---|---|---|---|---|
| Lung & bronchus | 229,410 | 10.8% | 29.5% | — | — |
| Female breast | 321,910 | 15.2% | 91.9% | — | — |
| Multiple myeloma | 36,000 (~10,850 deaths) | 1.7% | 63.7% | 7.4 (2019–2023) | ~202,793 (2023, model est.) |
| AML | 22,720 | 1.1% | 33.4% | 4.4 (2019–2023) | — |

Source: SEER Stat Facts (lungb / breast / mulmy / amyl). Survival vintage SEER 21 excl. IL 2016–2022; mortality 2020–2024.

## Oncology — Global (GLOBOCAN 2022 / IARC; Bray et al. 2024, CA Cancer J Clin)

- **~20 million** new cancer cases and **9.7 million** deaths in 2022 (incl. nonmelanoma skin cancer); projected to **35 million** new cases by 2050.

| Rank | Incidence 2022 | Mortality 2022 |
|---|---|---|
| 1 | Lung ~2.5M (12.4%) | Lung ~1.8M (18.7%) |
| 2 | Female breast (11.6%) | Colorectal (9.3%) |
| 3 | Colorectum (9.6%) | Liver (7.8%) |
| 4 | Prostate (7.3%) | Female breast (6.9%) |
| 5 | Stomach (4.9%) | Stomach (6.8%) |

GLOBOCAN 2022 is the current global cycle as of 2026; revised every ~2–3 years.

## Line-of-Therapy Attrition (real-world funnels)

The prevalence→treated funnel loses most patients across lines — line-compounding attrition is the single biggest reason peak-sales models over-count 2L/3L populations.

**Relapsed/refractory multiple myeloma** (Flatiron Health; Blood Advances 2024;8(19):5062):
- Screening: 12,767 MM patients (Jan 2016–Apr 2022) → 1,455 PI-exposed, lenalidomide-refractory with 1–3 prior lines.
- Of the 561 entering with **only 1 prior line**, cumulative attrition across lines 2–5 was **85%** (25% died, 60% received no further treatment). *Caveat: len-refractory RRMM database cohort, not nationally representative.*

**HER2+ metastatic breast cancer** (European multi-country EMR, n=496; PMC11785661):
- 1L **93.1%** → 2L **51.2%** → 3L **24.8%**. Per-line attrition (treated, no subsequent line) rises 29.6% (1L→2L) → 34.2% (2L→3L); **death is the largest single attrition driver** (37.4% of 1L→2L attrition).

**EGFR-mutant metastatic NSCLC on 1L osimertinib** (US single-center, n=115; medRxiv 2025.10.29.25339070):
- Of the 66 who discontinued 1L, only **~61%** received 2L (**~35% of the full cohort**). *A refuted framing claimed this "matches the FLAURA2 60% control arm" — do not assert that equivalence.*

> **Rule of thumb:** each therapy line loses ~30–35% of the prior line's treated patients, with death the dominant driver. A "3L eligible" population is typically only ~25% of the 1L population.

## Cardiometabolic — US (CDC)

| Indication | Prevalence | Vintage |
|---|---|---|
| Adult obesity | 40.3% (men 39.2%, women 41.3%) | NHANES Aug 2021–Aug 2023 (Data Brief 508) |
| Severe obesity | 9.4% (women 12.1%, men 6.7%) | NHANES 2021–2023 |
| Diabetes (all ages, dx + undx) | 38.4M / 11.6% (29.7M dx + 8.7M undx) | CDC NDSR 2024, 2021 data |
| Prediabetes | 97.6M adults / 38.0% | CDC NDSR, 2017–2020 NHANES |

## CNS — US

| Indication | Prevalence | Vintage |
|---|---|---|
| Alzheimer's dementia (65+) | 6.9M (7.2M in 2025 report) | Alzheimer's Assoc. 2024 Facts & Figures (alz.13809) |
| Multiple sclerosis (US) | **~419,000** (GBD 2021, 126/100k) **vs ~1M** claims-based (NMSS/CDC, Wallin 2019) — a real method divergence | GBD 2021 (s44197-025-00353-6) |
| Multiple sclerosis (global) | ~1.89M (GBD 2021, 23.9/100k); Atlas of MS gives 2.8M (2020); >62k new dx/yr | GBD 2021 |
| Parkinson's (US) | ~1.1M (→1.2M by 2030); ~90k new dx/yr (revised up ~50%) | Parkinson's Foundation 2024; Willis 2022; Marras 2018 |
| Parkinson's (global) | ~11.8M (GBD 2021, 138.63/100k) → **25.2M by 2050** (~doubling) | GBD 2021; BMJ 2025 (Su et al.) |

> **Registry vs modeled divergence (important for TAM sizing):** GBD modeled estimates run *well below* national foundation/claims-based figures (US MS: GBD 419k vs NMSS ~1M — a ~2.4× gap). State which basis you use; foundation figures are usually the right anchor for a US addressable market, GBD for global.

## Immunology

- Global RA prevalence 2020: **~17.6M** (95% UI 15.8–20.3M), ASR 208.8/100k (GBD 2021; Lancet Rheumatology 2023).
- Global mean GBD point-prevalence (1990–2018): atopic dermatitis 2.54%, psoriasis 0.74%, RA 0.31%, IBD 0.08%, MS 0.03%.

> **Critical sizing caveat:** these GBD figures are *global all-age point-prevalence* and substantially understate US/EU addressable populations (e.g., psoriasis ~2–3% of Western adults; AD ~15–20% of children). For a US/EU market model, use region-specific clinical/survey prevalence, not the global mean.

## Rare Disease

| Indication | Observed value | Lore figure | Source |
|---|---|---|---|
| Spinal muscular atrophy (SMA) | Birth prevalence **~1 in 14,694** (US newborn screening) | 1:10,000 | PMC11250364 |

> The SMA gap is **partly real reproductive selection**, not just a correction: expanded carrier screening (recommended 2017) reduces affected births. A refuted framing claimed the data "directly confirms the round-number overstates true incidence" — the authors are more careful, so don't assert a clean debunk. (DMD, sickle cell prevalence remain to be sourced.)

## Negative Findings (do not cite)

- **CDC NNCSS May 2020 Interim Report to Congress contains NO numeric MS or Parkinson's prevalence/incidence estimates** — it only states CDC is producing them. Not a citable source for MS/PD figures (use the GBD / NMSS / Parkinson's Foundation figures above instead).

## Source Vintage & Staleness

| Source | Anchors | Vintage | Refresh |
|---|---|---|---|
| SEER Cancer Stat Facts | US onc incidence/survival/prevalence | 2026 (ACS F&F 2026 + SEER 21 2016–2022) | Annual |
| GLOBOCAN 2022 (Bray 2024) | Global onc incidence/mortality | 2022 | ~2–3 yr cycle |
| Flatiron / Blood Advances 2024 | RRMM line-of-therapy funnel | 2016–2022 data | Cohort-specific |
| CDC NHANES / NDSR | Obesity, diabetes | 2021–2023 / 2021 | Periodic NHANES cycles |
| Alzheimer's Assoc. Facts & Figures | AD prevalence | 2024 (→7.2M in 2025) | Annual |
| GBD 2021 / JAAD Intl 2024 | Global immunology prevalence | 2020 / 1990–2018 | GBD cycle |
| GBD 2021 (MS/PD) + foundations | MS/PD prevalence (modeled vs registry) | 2021 / 2024 | Note method divergence |
| PMC11785661 / medRxiv 2025 | Solid-tumor line-of-therapy funnels | 2024–2025 | Cohort-specific |
| PMC11250364 | SMA birth prevalence | 2024 (NBS data) | Reflects post-2017 carrier screening |

**Usage note.** These are epidemiologic base rates — the *top* of the funnel. `patient-population-sizer/SKILL.md` supplies the diagnosis → treatment-seeking → eligibility → biomarker → line-of-therapy → geography multipliers that convert incidence/prevalence into a treatable population. Biomarker *prevalence* is owned by this doc (single source of truth); `biomarker-enrichment` should reference it rather than duplicating prevalence tables.
