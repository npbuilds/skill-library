# Portfolio Construction Benchmarks — Extended Reference

Fund-level calibration constants for the `portfolio-analyzer` skill (`skills/biotech-venture/deal-synthesis/portfolio-analyzer/`): the target multiples, viability thresholds, concentration bands, correlation coefficients, phase-distribution ranges, and reserve ratios used to score whether a portfolio of individually strong assets adds up to a viable fund. Every number below is an internal fund-construction heuristic drawn from the parent SKILL's own prose — none carry external citations.

**Provenance legend.** `int` = internal consensus estimate (from the skill's own quick-reference / prose, no external source). `ext✓` = externally verified with a real citation (none appear in this doc). `statutory` = a stable legal/regulatory constant. All benchmarks in this reference are tagged `int`.

**On LOA / PoS base rates.** This doc deliberately does **not** restate loss-of-approval-by-phase transition probabilities. For authoritative LOA base rates by phase, see `skills/biotech-venture/probability-of-success/pos-base-rates/references/transition-probability-tables.md`. The phase table below shows only the *capital-allocation* ranges the portfolio-analyzer uses; it points to that reference for the underlying success rates.

## Return & Viability Targets

| Metric | Threshold / range | Meaning | Provenance |
|---|---|---|---|
| Top-quartile gross MOIC | 3–4x | Return target for top-quartile biotech venture funds | int |
| Portfolio expected multiple (floor) | > 3x | Expected portfolio multiple should exceed 3x to absorb losses on failed programs | int |
| P(≥1 success) — viable | > 70% | Portfolio probability that at least one asset reaches approval / meaningful return | int |
| P(≥1 success) — danger zone | < 50% | Below this, the fund has meaningful probability of total loss | int |

## Concentration Bands (Herfindahl–Hirschman Index)

HHI = Σ (share_i)², where share_i = investment in a category / total portfolio investment. Compute across therapeutic area, modality, mechanism class, and geography for multi-dimensional concentration.

| HHI range | Label | Interpretation | Provenance |
|---|---|---|---|
| < 0.15 (1,500) | Diversified | No single TA dominates | int |
| 0.15–0.25 | Moderate concentration | Acceptable for focused funds | int |
| 0.25–0.40 | High concentration | Deliberate strategy required | int |
| > 0.40 | Very high concentration | Single-TA risk | int |

## Correlation by Shared Risk Source

Biotech assets are not independent; correlation reduces effective diversification. Pairwise ρ ranges by source of shared risk:

| Correlation source | Description | ρ range | Impact | Provenance |
|---|---|---|---|---|
| Therapeutic area | Same TA → correlated regulatory and market risk | 0.2–0.4 | Moderate | int |
| Mechanism class | Same pathway → correlated scientific risk | 0.3–0.6 | High | int |
| Platform | Same platform (mRNA, AAV, etc.) → shared technology risk | 0.4–0.7 | Very high | int |
| Regulatory | FDA policy changes hit multiple assets at once | 0.1–0.3 | Low–Moderate | int |
| Payer / commercial | TA-level market-access decisions affect all assets in that TA | 0.2–0.4 | Moderate | int |

**Correlation-adjusted portfolio PoS (portfolio-level simplification):**

```
Effective PoS = Independent PoS × (1 − average_ρ / 2)
```

Worked implication from the SKILL: a portfolio of 5 oncology assets at average pairwise ρ = 0.3 delivers the diversification equivalent of ~3.5 independent assets, not 5. `int`

## Phase Distribution — Optimal Capital Allocation

Capital-allocation ranges for a balanced biotech fund. LOA/PoS ranges by phase are **not** reproduced here — see `probability-of-success/pos-base-rates/references/transition-probability-tables.md`.

| Phase bucket | Target % of capital | Role | Provenance |
|---|---|---|---|
| Preclinical + Phase 1 | 20–35% | High risk, high multiple | int |
| Phase 2 | 35–45% | Core portfolio | int |
| Phase 3+ | 20–35% | De-risked, lower multiple | int |

**J-curve note (`int`).** Early-stage-heavy portfolios carry longer J-curves (3–5 years to first positive cash event); late-stage-heavy portfolios shorten the J-curve but cap return potential. Balance against fund LP expectations and fund life.

## Reserve Allocation for Follow-On

| Parameter | Value | Note | Provenance |
|---|---|---|---|
| Top-quartile follow-on reserve | 40–60% of capital | Share of fund held for follow-on in winners | int |
| Reserve coverage ratio (target) | > 1.5x | Reserves ÷ expected total follow-on demand | int |
| Default modeling assumption | 50% reserve ratio | Used when reserve allocation is unspecified | int |
| Sensitivity band | 40% and 60% | Stress-test around the 50% default | int |

**Critical rule (`int`).** Under-reserved funds are forced to dilute in winning positions (selling winners early) or let pro-rata lapse — both destroy fund-level return.

## Small-N and Data-Gap Defaults

| Scenario | Analyzer behavior | Provenance |
|---|---|---|
| Fewer than 3 assets | Concentration metrics flagged as less meaningful | int |
| No correlation data | Fall back to TA-based ρ estimates; label "estimated correlations" | int |
| Reserve allocation unspecified | Model at 50%, sensitivity-test 40% / 60% | int |
| Mixed (biotech + non-biotech) fund | Analyze biotech sub-portfolio separately; note cross-asset correlations | int |

## Source Vintage & Staleness

These are structural fund-construction heuristics, not market prints, so they stale slowly — but not never:

- **Return targets (3–4x MOIC, >3x floor)** track the venture cycle. They drift with fundraising conditions and vintage-year expectations; re-check every fund cycle (~2–3 years) or after a market regime shift.
- **HHI bands and phase-distribution ranges** are the most durable here (definitional / strategy heuristics); revisit only if the fund's mandate changes.
- **Correlation coefficients by risk source** are the softest inputs — they are estimates, are labeled as such in the SKILL, and should be re-derived from realized portfolio outcomes as evidence accumulates; treat platform/mechanism ρ as directional, not precise.
- **Reserve ratios (40–60%, >1.5x coverage)** shift with average follow-on check sizes and round dynamics; re-check when deployment pace or round sizing changes materially.
- **LOA/PoS base rates** (referenced, not restated) stale on their own cadence — governed by `transition-probability-tables.md`, not this doc.

**Usage note.** This reference serves the `portfolio-analyzer` SKILL (`skills/biotech-venture/deal-synthesis/portfolio-analyzer/SKILL.md`). For the authoritative LOA-by-phase transition probabilities that feed portfolio PoS and expected-value math, always defer to `skills/biotech-venture/probability-of-success/pos-base-rates/references/transition-probability-tables.md`. Related inputs come from `asset-valuation/rnpv-modeler` (per-asset rNPV), `probability-of-success/pos-calculator` (per-asset PoS), `deal-synthesis/diligence-scorecard` (asset scores), and `competitive-intelligence/market-dynamics` (TA correlation assumptions).
