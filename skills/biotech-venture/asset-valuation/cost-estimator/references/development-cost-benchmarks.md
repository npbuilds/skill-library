# Development Cost Benchmarks — Extended Reference

Capitalized and out-of-pocket drug development cost anchors, by method, therapeutic area, and phase. **The headline "cost per drug" is a wide, methodology-driven range — never quote a single point estimate without stating (a) the method/source, (b) the base year, and (c) whether it is out-of-pocket or capitalized.**

## Cost Per Approved Drug — The Range, Not a Point

The three authoritative estimates disagree by ~15× at the out-of-pocket end because they differ in sample, discount rate, failure-cost treatment, and preclinical allocation — this is genuine methodological disagreement, not measurement noise.

| Estimate | Out-of-pocket (cash) | Capitalized | Base year | Sample / method | Source |
|---|---|---|---|---|---|
| **DiMasi et al. 2016** (the "$2.6B") | $1,395M | **$2,558M** | 2013$ | Confidential industry survey, primarily large pharma; 10.5% real discount rate | J Health Econ (S0167629616000291) |
| **Wouters et al. 2020** | — | median $985.3M / $1,141.7M; mean $1,335.9M / $1,559.1M (≈$1.3B vs DiMasi's inflation-adj $2.8B) | 2018$ | n=63 of 355 FDA approvals 2009–2018, 47 companies, public SEC filings; 10.5% cost of capital, incl. failed trials | JAMA 2020 (PMC7054832) |
| **ASPE/ERG 2024** (govt model) | **$172.7M** | $879.3M | 2018$ | ERG model; ASPE notes DiMasi is based on primarily large-pharma data | HHS ASPE report |

> **The "$2.6B" decomposed:** DiMasi's $2,558M is the *capitalized pre-approval* cost. Its *cash out-of-pocket* component is only $1,395M — roughly half. Diligence must preserve that distinction.
>
> **Wouters caveat:** its estimate relied on a phase-2 success rate later corrected *downward* — aggregate probability that a drug entering Phase 2 is ultimately approved was revised from **35.1% → 21.0%** (JAMA 2022 correction), which would raise the true per-approval cost.

## Where the Money Goes

| Component | Share of out-of-pocket R&D | Source |
|---|---|---|
| Clinical trials (Phases 1–3) | **~68%** ($117.4M in the ASPE/ERG model) — the single largest component | ASPE/ERG 2024 |

## Cost Varies 3.6×–4.6× by Therapeutic Area

Any single "cost per drug" hides area variation on the order of 4×. Oncology sits at the top; nervous-system and anti-infective at the bottom.

| Study | Highest TA | Lowest TA | Spread | Base year |
|---|---|---|---|---|
| Wouters 2020 | Oncology / immunomodulating median $2,771.6M | Nervous system $765.9M | **3.6×** (non-overlapping CIs) | 2018$ |
| ASPE/ERG 2024 | Pain & anesthesia $1,756.2M | Anti-infective ~$378.7M | **>4×** | 2018$ |

## Per-Study US Trial Cost by Phase (directional only)

Sertkaya et al. 2016 — includes site overhead and sponsor monitoring. **Vintage warning: built on 2004–2012 data and NOT inflation-adjusted, so materially understated for 2026. Use the therapeutic-area PATTERN, not the absolute dollars.**

| Phase | Low (TA) | High (TA) |
|---|---|---|
| Phase 1 | $1.4M (pain/anesthesia) | $6.6M (immunomodulation) |
| Phase 2 | $7.0M (cardiovascular) | $19.6M (hematology) |
| Phase 3 | $11.5M (dermatology) | $52.9M (pain/anesthesia) |

## Success Rate — Context for Cost-of-Failure

| Metric | Value | Source |
|---|---|---|
| Overall Phase I → approval LOA | **7.9%** (≈1-in-13, not "1-in-10") | BIO/Informa Clinical Development Success Rates 2011–2020 |
| Largest single hurdle | **Phase II** | BIO 2011–2020 |

## Source Vintage & Staleness

| Source | Anchors | Vintage | Notes |
|---|---|---|---|
| DiMasi 2016 (J Health Econ) | Capitalized cost per drug | 2013$ | Rests on unpublished confidential survey (standing critique) |
| Wouters 2020 (JAMA) | Independent lower estimate + TA spread | 2018$ | Only 18% of approvals, skewed to smaller firms; corrected phase-2 input |
| ASPE/ERG 2024 (HHS) | Lowest-end govt model + clinical-share | 2018$ | Broad ERG model |
| Sertkaya 2016 | Per-study trial dollars by phase/TA | 2004–2012 data | Understated for 2026 — pattern only |
| BIO/Informa 2011–2020 | LOA / success rates | 2011–2020 | Feeds `pos-base-rates`; cross-reference `transition-probability-tables.md` |

**Usage note.** Pair this doc with `pos-base-rates/references/transition-probability-tables.md` (the failure side) — cost-of-capital in an rNPV is meaningless without the phase-conditioned probability of paying it. Cross-reference `cost-estimator/SKILL.md` for the phase/modality/complexity multiplier methodology that consumes these anchors.
