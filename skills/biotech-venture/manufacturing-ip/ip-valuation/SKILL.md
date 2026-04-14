---
name: ip-valuation
description: >
  IP valuation frameworks for biotech assets including cost approach, market approach
  (comparable royalty rates), and income approach (relief-from-royalty). Covers royalty
  rate benchmarks by patent type, IP contribution analysis, trade secret valuation, and
  regulatory exclusivity value quantification. Activate when translating patent strength
  into financial value or modeling the impact of IP on asset economics.
metadata:
  author: nirav
  version: "1.0"
  parent: manufacturing-ip
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# IP Valuation — Translating Patent Strength into Financial Value

IP valuation bridges the gap between legal analysis ("the patent expires in 2034") and financial analysis ("the patent is worth $400M"). For biotech venture investors, IP value manifests in two ways: the duration and magnitude of premium-priced revenue before generic/biosimilar erosion, and the licensing economics when IP is transacted between parties. This skill provides the frameworks for both.

## Three Approaches to IP Valuation

### Approach 1 — Cost Approach

**What it measures:** The cost to recreate the IP from scratch.

**Methodology:**
- Reproduction cost: What would it cost to generate the same patent estate today?
- Replacement cost: What would it cost to develop equivalent (not identical) IP?

**Components:**
- R&D investment to discover the compound: $50M-$500M (modality-dependent)
- Patent prosecution costs: $50K-$200K per patent family
- Clinical data package (if data exclusivity is part of IP value): $100M-$2B
- Opportunity cost of time: 5-15 years of development

**When to use:** Floor valuation. The cost approach sets the minimum value — IP is worth at least what it cost to create. Useful for early-stage assets where income projections are speculative.

**Limitations:** Cost does not equal value. A $500M R&D program that produces a failed drug has zero IP value regardless of investment. Cost approach ignores market potential.

### Approach 2 — Market Approach (Comparable Royalty Rates)

**What it measures:** What similar IP transacts for in the market.

**Methodology:** Identify comparable licensing deals and extract implied royalty rates. Apply comparable rates to the subject IP based on similarity of patent type, therapeutic area, development stage, and exclusivity strength.

**Royalty Rate Benchmarks by Patent Type:**

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

**Royalty Rate Adjustments:**

| Factor | Adjustment |
|---|---|
| Strong CoM with no design-around | +2-5% above benchmark |
| Weak patent estate (method-of-use only) | -2-3% below benchmark |
| Multiple overlapping patents (thicket) | +1-2% (enforcement advantage) |
| Patent challenged (IPR pending) | -2-5% (uncertainty discount) |
| Orphan drug exclusivity stacking | +1-3% (regulatory moat) |
| Blockbuster potential (>$1B peak sales) | Rate at lower end of range (absolute dollars are large) |
| Niche indication (<$200M peak sales) | Rate at higher end of range (licensor needs adequate return) |

**Comparable deal sources:**
- SEC filings (10-K, 8-K) for disclosed deal terms
- Pharma licensing databases (evaluate publicly available deal summaries)
- Royalty monetization transactions (royalty trusts disclose rates)

### Approach 3 — Income Approach (Relief-from-Royalty)

**What it measures:** The present value of royalty payments the company avoids by owning the IP rather than licensing it.

**Methodology:**
```
IP Value = Σ [ (Net Revenue_t x Royalty Rate) x PoS_t ] / (1 + r)^t

Where:
  Net Revenue_t  = Projected net sales in year t
  Royalty Rate    = Appropriate rate from market approach benchmarks
  PoS_t          = Probability of reaching year t (from pos-calculator)
  r              = Discount rate (WACC)
  t              = Years over patent protection period only
```

**Key distinction from rNPV:** Relief-from-royalty values only the IP contribution to revenue, not the entire asset. It answers: "What is the patent worth?" rather than "What is the drug worth?"

**IP contribution percentage:**
- Composition of matter patents: 60-80% of total asset value
- Method of use only: 20-40% of total asset value
- Formulation only: 15-30% of total asset value
- No patent (regulatory exclusivity only): 10-20% of total asset value

## Regulatory Exclusivity Valuation

Regulatory exclusivity provides IP-like protection independent of patents. Value each exclusivity type:

### NCE Exclusivity (5 Years)

**What it protects:** No ANDA (generic) application can be filed for 5 years from NDA approval for a new chemical entity.

**Value:** Guarantees 5 years of generic-free revenue regardless of patent status. Most valuable when patent protection is weak or challenged.

**Quantification:**
```
NCE Value = Σ Revenue_t for t = Year 1 through Year 5 post-approval
            (discounted, probability-weighted)
            MINUS revenue that patents alone would have protected
```

If patents extend beyond 5 years, NCE exclusivity has zero incremental value (it is fully overlapping). If patents expire before 5 years post-approval, NCE exclusivity value = revenue in the gap period.

### Orphan Drug Exclusivity (7 Years)

**What it protects:** No approval of the same drug for the same rare disease indication for 7 years.

**Value:** Extremely high in rare diseases where the market is small and a single competitor can destroy economics. The 7-year window often exceeds patent protection for repurposed compounds.

**Key nuance:** Orphan exclusivity blocks the same drug, not different drugs for the same indication. A competitor with a different molecule can still be approved. The exclusivity protects against generics/biosimilars, not against new mechanisms.

### Pediatric Exclusivity (+6 Months)

**What it protects:** Extends all existing patents and exclusivities by 6 months in exchange for conducting pediatric studies.

**Value calculation:**
```
Pediatric Exclusivity Value = 6 months of peak revenue (net, discounted)
```

At $2B peak sales, 6 months = ~$1B in gross revenue, ~$600-700M net. One of the highest-ROI regulatory incentives — pediatric studies cost $10-50M but can generate hundreds of millions in extended exclusivity.

### Biologic Exclusivity (12 Years)

**What it protects:** No biosimilar approval for 12 years from BLA approval; no biosimilar application for 4 years.

**Value:** The 12-year window is the primary competitive moat for biologics (often more protective than patents). For biologics with patents expiring before the 12-year mark, this exclusivity IS the IP.

### QIDP Exclusivity (+5 Years)

**What it protects:** Adds 5 years to existing exclusivity for Qualified Infectious Disease Products.

**Value:** Transformative for anti-infectives where development costs are high but market size is limited. Can make economically marginal programs viable.

## Trade Secret Valuation

Some biotech IP is protected through trade secrets rather than patents:

**Trade secret advantages:**
- No expiration (protection lasts as long as the secret is maintained)
- No disclosure requirement (unlike patents, which require public disclosure)
- Protects know-how that is difficult to patent (cell culture conditions, purification parameters)

**Trade secret risks:**
- No protection against independent discovery or reverse engineering
- Employee departure can compromise secrets
- No injunctive relief framework as robust as patent law

**Valuation approach:** Value trade secrets as a perpetuity of the cost advantage or competitive advantage they provide, discounted by the probability of loss (employee turnover, reverse engineering).

**Common trade secrets in biotech:**
- Cell line development conditions and selection criteria
- Purification process parameters and optimization
- Analytical method details beyond what is filed with regulators
- Manufacturing yield optimization techniques
- Formulation know-how for complex delivery systems

## IP Contribution Analysis Framework

To determine what fraction of total asset value is attributable to IP:

```
IP CONTRIBUTION ANALYSIS

Total Asset rNPV: $[X]M (from rnpv-modeler)

Revenue Components:
  Patent-protected revenue period: Year [A] to Year [B]
  Post-patent revenue (brand loyalty/authorized generic): Year [B] to Year [C]
  Revenue during exclusivity-only period: Year [X] to Year [Y]

IP Value Components:
  Patent contribution:       $[X]M  ([X]% of total rNPV)
  Regulatory exclusivity:    $[X]M  ([X]% of total rNPV)
  Trade secret contribution: $[X]M  ([X]% of total rNPV)
  Total IP contribution:     $[X]M  ([X]% of total rNPV)

Non-IP Value:
  Post-LOE branded revenue:  $[X]M
  Clinical data value:       $[X]M (regulatory data package)
  Brand/franchise value:     $[X]M

IP as % of Total Value: [X]%
```

**Benchmark:** For innovative drugs with strong CoM patents, IP typically represents 60-85% of total asset value. For biologics with strong regulatory exclusivity, the split may be 40% patent / 30% regulatory exclusivity / 30% other.

## Error Handling

| Scenario | Response |
|---|---|
| No comparable licensing deals available | Use royalty rate benchmarks by patent type; note as "benchmark estimate — limited comparables" |
| Patent life shorter than development timeline | Value shifts to regulatory exclusivity; model NCE/orphan/biologic exclusivity explicitly |
| IP encumbered by third-party royalties | Net the existing royalty obligation from IP value; adjust relief-from-royalty accordingly |
| Multiple indications with different IP coverage | Value IP per indication; some indications may have stronger protection than others |

## Cross-Domain Connections

- **manufacturing-ip/patent-analyzer**: Patent landscape is the input; IP valuation is the financial translation
- **asset-valuation/rnpv-modeler**: IP value is a component of total rNPV; patent expiry sets the revenue tail
- **manufacturing-ip/cmc-risk-assessor**: Trade secret value in manufacturing know-how
- **competitive-intelligence/market-dynamics**: Biosimilar/generic erosion patterns post-LOE
- **deal-synthesis/diligence-scorecard**: IP valuation feeds Pillar 5 (IP Fortress) of the 8-pillar scorecard
