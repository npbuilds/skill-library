# Auction Formats — Multi-Item and Specialized Mechanisms

## Multi-Item Auction Theory

### Sequential vs. Simultaneous

**Sequential auctions**: Items sold one at a time. Simpler but creates strategic complications — bidders must guess future prices and decide when to bid aggressively. Declining price anomaly: empirically, prices tend to fall in sequential auctions of identical items (contradicting the theoretical prediction of constant prices under risk-neutrality).

**Simultaneous auctions**: All items available at once. Allows bidders to express preferences over combinations. More informationally demanding for bidders but better for efficiency when items are related.

### Simultaneous Multiple Round (SMR) Auction

Designed by Milgrom, Wilson, and McAfee for the FCC (1994):

1. All licenses are auctioned simultaneously
2. Multiple rounds with increasing bids
3. **Activity rules**: bidders must be active on a minimum number of licenses proportional to their eligibility, increasing over time. Prevents "snake in the grass" strategies
4. Auction ends when no new bids on any license

**Strengths**: Allows bidders to assemble efficient packages across related licenses. Price discovery through iterative bidding.
**Weaknesses**: Exposure problem — bidders wanting a package may win only some items and overpay. Demand reduction — large bidders may reduce demand to lower prices.

### Combinatorial Clock Auction (CCA)

Evolution of SMR used in recent spectrum auctions (UK 4G, Australian digital dividend):

1. **Clock phase**: Ascending clock prices for abstract blocks; bidders indicate demand at each price
2. **Supplementary round**: Sealed bids on specific packages, constrained by clock phase behavior
3. **Allocation and pricing**: VCG-based pricing (or nearest VCG) applied to supplementary bids

Addresses the exposure problem of SMR by allowing package bidding.

### Generalized Second Price (GSP) Auction

The mechanism behind search advertising (Google, Bing):

- Advertisers bid on keywords
- Positions allocated by bid × quality score
- Each advertiser pays the minimum bid to maintain their position (price of the position below them, adjusted by quality ratio)

**Key result**: GSP is NOT truthful (unlike Vickrey). The set of Nash equilibria corresponds to stable matchings in a two-sided market. The lowest-revenue equilibrium coincides with the VCG outcome (Edelman, Ostrovsky & Schwarz 2007).

**Quality score**: Google's innovation — adjusts ranking by estimated click-through rate, ad quality, and landing page relevance. Aligns platform incentives (revenue per impression) with user experience.

## Specialized Auction Types

### All-Pay Auction

All bidders pay their bids; only the highest bidder wins. Models lobbying, patent races, political campaigns, and R&D contests.

**Expected revenue**: Higher than standard auctions for risk-neutral bidders (all bidders pay, not just the winner). But often leads to overbidding and dissipation of rents.

**War of attrition**: A continuous-time all-pay auction. Two firms in a price war: both lose money every period, the first to exit loses. Mixed-strategy equilibrium involves random exit times.

### Double Auction

Both buyers and sellers submit bids. A market-clearing price is determined where supply meets demand.

**k-double auction**: Price set at k × (lowest rejected ask) + (1-k) × (highest rejected bid). At k = 1/2, approximates the competitive equilibrium for large markets.

**Chatterjee-Samuelson result**: In bilateral double auctions with uniform priors, the k = 1/2 mechanism maximizes ex ante surplus among all incentive-compatible, individually rational, budget-balanced mechanisms. But it's still not fully efficient — some profitable trades are missed (echoing Myerson-Satterthwaite).

### Ascending Proxy Auction (Ausubel, Milgrom & others)

Bidders report preferences to a proxy agent that bids on their behalf in an ascending auction. The proxy bids for the package that maximizes the bidder's profit at current prices.

Achieves VCG-like outcomes when goods are substitutes. Addresses the computational complexity of direct combinatorial bidding.

### Position Auctions

Multiple positions of decreasing value (search results, display ad slots). Bidders compete for positions; higher positions get more clicks/views.

Standard model: positions have click-through rates α₁ > α₂ > ... > αₖ. Values per click are private. GSP and VCG are the two main pricing rules.

## Revenue Comparison Across Formats

Under IPV with risk-neutral symmetric bidders (revenue equivalence holds):

| Format | Expected Revenue | Strategic Complexity | Truthful? |
|--------|-----------------|---------------------|-----------|
| English | E[2nd highest value] | Low | Yes (approx.) |
| Vickrey | E[2nd highest value] | Low | Yes (dominant) |
| First-price | E[2nd highest value] | Medium (must shade) | No |
| Dutch | E[2nd highest value] | Medium (must shade) | No |
| All-pay | E[2nd highest value] | High | No |

Revenue equivalence breaks when we relax IPV:
- **Risk aversion** → First-price > Second-price (less shading under risk aversion)
- **Affiliated values** → English > Second-price > First-price (Milgrom & Weber 1982 revenue ranking)
- **Asymmetric bidders** → No general ranking; depends on the asymmetry structure

## Reserve Prices

Setting an optimal reserve price is often more important than choosing the auction format:

- **Optimal reserve under IPV**: Solve ψ(r) = 0, where ψ is the virtual valuation. For uniform [0,1] values, optimal reserve = 1/2 regardless of number of bidders
- **The reserve price trades off**: excluding some efficient sales (lost surplus) vs. extracting more from high-value bidders (increased revenue per sale)
- **With entry effects**: too-high reserves deter participation, reducing competition. The optimal reserve balances extraction against participation

## Auction Design Checklist

When designing an auction for a specific application:

- [ ] **Value model**: IPV, common value, or affiliated? Determines bidding behavior and winner's curse risk
- [ ] **Number of items**: Single → standard formats. Multiple → consider complementarities and combinatorial bidding
- [ ] **Bidder symmetry**: Symmetric → standard theory applies. Asymmetric → consider handicapping or set-asides
- [ ] **Budget constraints**: If bidders are budget-constrained, Vickrey/VCG may not be optimal; consider all-pay or clinching variants
- [ ] **Collusion risk**: More transparent formats (English) are more vulnerable to collusion. Consider sealed-bid or anonymous bidding
- [ ] **Revenue vs. efficiency**: Can't always have both (Myerson-Satterthwaite). Choose the primary objective
- [ ] **Computational burden**: Combinatorial auctions impose computational costs on bidders. Simpler formats may attract more participation
