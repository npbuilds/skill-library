# IP Valuation — Extended Reference

Consolidated royalty-rate benchmarks, adjustment factors, and IP/NCE valuation formulas for the `ip-valuation` SKILL under `manufacturing-ip`. All royalty and formula figures here are the skill's own internal consensus estimates, not market-observed comps.

**Provenance legend.**
- `int` — internal consensus estimate (drawn from the skill's own quick-reference prose; no external source attached).
- `ext✓` — externally verified with a real citation (none appear in this doc; see the cross-referenced deal-comps doc for sourced data).
- `statutory` — a stable legal/regulatory constant.

> **Sanity-check against real deals.** Every royalty range and dollar threshold below is an internal benchmark, useful only when comparable licensing deals are unavailable. Before relying on them, cross-check against market-observed royalty and deal comps — which ARE externally sourced — in `asset-valuation/deal-economics/references/deal-comps-benchmarks.md`.

## Royalty Rate by Patent Type (int)

| Patent Type | Typical Royalty Range | Rationale |
|---|---|---|
| Composition of Matter (novel compound) | 5–15% of net sales | Strongest protection; covers the product itself |
| Composition of Matter (analog/derivative) | 3–8% of net sales | Narrower scope; design-around possible |
| Formulation / Drug Delivery | 2–5% of net sales | Protects the delivery, not the compound |
| Method of Use (new indication) | 2–6% of net sales | Limited enforcement; off-label generic use |
| Dosing Regimen | 1–3% of net sales | Weakest; difficult to enforce |
| Platform Technology | 3–8% of net sales + milestones | Value depends on platform breadth |
| Target Biology (antibody to validated target) | 2–5% of net sales | Often combined with CoM royalty |
| Manufacturing Process | 1–3% of net sales | Alternative processes usually exist |

## Royalty Adjustment Factors (int)

Applied to the benchmark rate above once patent-estate strength and commercial context are known.

| Factor | Adjustment |
|---|---|
| Strong CoM with no design-around | +2–5% above benchmark |
| Weak patent estate (method-of-use only) | −2–3% below benchmark |
| Multiple overlapping patents (thicket) | +1–2% (enforcement advantage) |
| Patent challenged (IPR pending) | −2–5% (uncertainty discount) |
| Orphan drug exclusivity stacking | +1–3% (regulatory moat) |
| Blockbuster potential (>$1B peak sales) | Rate at lower end of range (absolute dollars are large) |
| Niche indication (<$200M peak sales) | Rate at higher end of range (licensor needs adequate return) |

## Valuation Formulas (int)

**Relief-from-royalty (market approach) IP value:**

```
IP Value = Σ [ (Net Revenue_t x Royalty Rate) x PoS_t ] / (1 + r)^t

Where:
  Net Revenue_t  = Projected net sales in year t
  Royalty Rate   = Appropriate rate from the benchmarks above
  PoS_t          = Probability of reaching year t (from pos-calculator)
  r              = Discount rate (WACC)
  t              = Years over patent protection period only
```

**Incremental value of NCE (regulatory) exclusivity:**

```
NCE Value = Σ Revenue_t for t = Year 1 through Year 5 post-approval
            (discounted, probability-weighted)
            MINUS revenue that patents alone would have protected
```

The NCE formula isolates the value regulatory exclusivity adds *beyond* patent protection over the 5-year new-chemical-entity window (statutory: US NCE exclusivity = 5 years). When patent life is shorter than the development timeline, value shifts to regulatory exclusivity and NCE/orphan/biologic exclusivity should be modeled explicitly. Orphan-drug status (statutory: US orphan designation requires an indication of <200,000 US patients) stacks its own exclusivity per the adjustment table above.

## Error-Handling Rules (int)

| Scenario | Response |
|---|---|
| No comparable licensing deals available | Use royalty benchmarks by patent type; label "benchmark estimate — limited comparables" |
| Patent life shorter than development timeline | Value shifts to regulatory exclusivity; model NCE/orphan/biologic exclusivity explicitly |
| IP encumbered by third-party royalties | Net the existing royalty obligation from IP value; adjust relief-from-royalty accordingly |
| Multiple indications with different IP coverage | Value IP per indication; some may have stronger protection than others |

## Source Vintage & Staleness

- **Royalty ranges and adjustment factors (int):** these are structural rules of thumb keyed to patent type, not point-in-time market prices. They drift slowly but should be re-anchored against fresh deal comps roughly annually, and immediately whenever a directly comparable licensing deal surfaces — at which point the market comp supersedes the internal benchmark.
- **Statutory constants (NCE 5-year exclusivity, orphan <200k US patients):** stable across years; change only on legislative/regulatory reform.
- **Peak-sales thresholds (>$1B blockbuster, <$200M niche):** nominal-dollar bands that erode with inflation over multi-year horizons; treat as approximate tiers, not hard cutoffs.
- Because none of the royalty figures here carry an external citation, they are the weakest-provenance inputs in any valuation and should always be triangulated against the sourced comps before use.

**Usage note.** This document serves the `ip-valuation` SKILL (`skills/biotech-venture/manufacturing-ip/ip-valuation/`). Every royalty range, adjustment, and threshold is an internal estimate (`int`) — validate against externally sourced, market-observed royalty and deal comps in `asset-valuation/deal-economics/references/deal-comps-benchmarks.md`. PoS inputs to the IP-value formula come from the `pos-calculator` skill.
