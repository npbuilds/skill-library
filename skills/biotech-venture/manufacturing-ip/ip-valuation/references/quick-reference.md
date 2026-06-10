# Ip Valuation — Quick Reference


## Quick Reference

| Patent Type | Typical Royalty Range | Rationale |
|---|---|---|
| Composition of Matter (novel compound) | 5-15% of net sales | Strongest protection; covers the product itself |
| Composition of Matter (analog/derivative) | 3-8% of net sales | Narrower scope; design-around possible |
| Formulation / Drug Delivery | 2-5% of net sales | Protects the delivery, not the compound |
| Method of Use (new indication) | 2-6% of net sales | Limited enforcement; off-label generic use |
| Dosing Regimen | 1-3% of net sales | Weakest; difficult to enforce |
| Platform Technology | 3-8% of net sales + milestones | Value depends on platform breadth |
| Target Biology (antibody to validated target) | 2-5% of net sales | Often combined with CoM royalty |
| Manufacturing Process | 1-3% of net sales | Alternative processes usually exist |

## Quick Reference

| Factor | Adjustment |
|---|---|
| Strong CoM with no design-around | +2-5% above benchmark |
| Weak patent estate (method-of-use only) | -2-3% below benchmark |
| Multiple overlapping patents (thicket) | +1-2% (enforcement advantage) |
| Patent challenged (IPR pending) | -2-5% (uncertainty discount) |
| Orphan drug exclusivity stacking | +1-3% (regulatory moat) |
| Blockbuster potential (>$1B peak sales) | Rate at lower end of range (absolute dollars are large) |
| Niche indication (<$200M peak sales) | Rate at higher end of range (licensor needs adequate return) |

## Error Handling

| Scenario | Response |
|---|---|
| No comparable licensing deals available | Use royalty rate benchmarks by patent type; note as "benchmark estimate — limited comparables" |
| Patent life shorter than development timeline | Value shifts to regulatory exclusivity; model NCE/orphan/biologic exclusivity explicitly |
| IP encumbered by third-party royalties | Net the existing royalty obligation from IP value; adjust relief-from-royalty accordingly |
| Multiple indications with different IP coverage | Value IP per indication; some indications may have stronger protection than others |

## Formula / Pseudocode

```
IP Value = Σ [ (Net Revenue_t x Royalty Rate) x PoS_t ] / (1 + r)^t

Where:
  Net Revenue_t  = Projected net sales in year t
  Royalty Rate    = Appropriate rate from market approach benchmarks
  PoS_t          = Probability of reaching year t (from pos-calculator)
  r              = Discount rate (WACC)
  t              = Years over patent protection period only
```

## Formula / Pseudocode

```
NCE Value = Σ Revenue_t for t = Year 1 through Year 5 post-approval
            (discounted, probability-weighted)
            MINUS revenue that patents alone would have protected
```
