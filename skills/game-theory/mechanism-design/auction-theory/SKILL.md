---
name: auction-theory
description: >
  Auction theory foundations for understanding and designing competitive allocation mechanisms.
  Reference when analyzing auction formats, computing optimal bidding strategies, evaluating
  revenue properties, or designing new auctions. Use when any analysis involves competitive
  bidding, price discovery, or allocation through auctions.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Auction Theory — The Market Maker

The theory of competitive allocation through bidding. Auctions are the purest form of mechanism design — a set of rules that transforms private valuations into allocations and payments. Grounded primarily in Krishna (2002), Milgrom (2004), and Myerson (1981).

## The Auction Framework

An auction specifies:
- **Bidders**: N = {1, ..., n} with private valuations vᵢ for the item(s)
- **Value model**: Independent Private Values (IPV), correlated, or common values
- **Rules**: How bids are submitted, who wins, and what the winner pays
- **Information**: What bidders know about each other's valuations

### Value Models

**Independent Private Values (IPV)**: Each bidder's valuation is drawn independently from a known distribution. My value for a painting depends only on how much I personally like it.

**Common Values**: The item has an objective value unknown to all bidders, who receive noisy private signals. My value for an oil lease depends on how much oil is actually there — something I estimate but don't know.

**Affiliated Values** (Milgrom & Weber 1982): Generalization where bidders' signals are positively correlated. Higher signals by one bidder make higher signals by others more likely. Most realistic model for many settings.

## Standard Auction Formats

### Single-Item Auctions

| Format | Rules | Winner | Payment |
|--------|-------|--------|---------|
| **English (ascending)** | Price rises; bidders drop out when price exceeds value | Last remaining bidder | Second-highest value (approximately) |
| **Dutch (descending)** | Price falls from high; first bidder to claim wins | First to stop the clock | Their bid (first-price) |
| **First-Price Sealed-Bid** | Submit sealed bids simultaneously; highest wins | Highest bidder | Their bid |
| **Second-Price Sealed-Bid (Vickrey)** | Submit sealed bids; highest wins, pays second-highest bid | Highest bidder | Second-highest bid |

### Optimal Bidding Strategies

**Vickrey (second-price sealed-bid)**: Truthful bidding is a **dominant strategy**. Bid your true valuation — you never gain by overbidding or underbidding. This is the foundational incentive compatibility result in auction theory.

**Why truthful bidding works in Vickrey**: If you win, you pay the second-highest bid regardless of your own bid. Bidding higher than your value risks winning at a loss. Bidding lower risks losing when you would have profited.

**First-price sealed-bid (IPV)**: Bid below your true valuation — **bid shading**. With n bidders uniformly distributed on [0,1], the symmetric equilibrium bid is b(v) = v(n-1)/n. More bidders → less shading → bids approach true values.

**English auction**: Strategically equivalent to Vickrey under IPV — stay in until price reaches your value, drop out when it exceeds. Under affiliated values, the English auction generates strictly more revenue than sealed-bid formats (Milgrom & Weber 1982).

## Revenue Equivalence Theorem

The central unifying result of auction theory (Myerson 1981, Riley & Samuelson 1981):

**Under IPV with risk-neutral bidders**: Any auction that (a) allocates to the highest-valued bidder and (b) gives zero expected surplus to the lowest-type bidder generates the **same expected revenue**.

This means English, Dutch, first-price, and second-price auctions all produce identical expected revenue under IPV. Revenue differences arise from:
- **Risk aversion** → favors first-price (bidders shade less)
- **Affiliated values** → favors English (information revelation during bidding)
- **Reserve prices** → all formats benefit from optimal reserves
- **Asymmetric bidders** → revenue equivalence breaks down

## Optimal Auction Design (Myerson 1981)

The revenue-maximizing auction under IPV:

1. Compute each bidder's **virtual valuation**: ψᵢ(vᵢ) = vᵢ - (1 - F(vᵢ))/f(vᵢ), where F is the CDF and f the density of the value distribution
2. Allocate to the bidder with the highest virtual valuation (if positive)
3. Charge the **minimum bid** that would have still won

**Key results**:
- The optimal reserve price excludes some efficient trades to extract more surplus from high-value bidders
- With symmetric bidders, a second-price auction with an optimal reserve price is optimal
- **Myerson-Satterthwaite impossibility**: In bilateral trade (one buyer, one seller) with private values, no mechanism is simultaneously efficient, individually rational, incentive compatible, and budget-balanced

## Multi-Item and Combinatorial Auctions

Read `references/auction-formats.md` for detailed coverage of multi-item mechanisms.

When multiple items are sold simultaneously, **complementarities** and **substitutabilities** between items create new challenges:
- A spectrum license for New York is worth more if you also have New Jersey (complements)
- Two paintings by the same artist may be substitutes to a collector

**VCG (Vickrey-Clarke-Groves) mechanism**: Extends Vickrey to multiple items. Each bidder pays the externality they impose on others. Truthful bidding is dominant strategy. Achieves efficiency but may generate low revenue and is vulnerable to collusion.

**Combinatorial auctions**: Allow bids on bundles of items. NP-hard winner determination problem. Used for FCC spectrum allocation, industrial procurement, airport landing slots.

## Real-World Auction Applications

| Application | Format | Scale | Key Design Feature |
|-------------|--------|-------|-------------------|
| FCC Spectrum Auctions | Simultaneous Multiple Round (SMR) / Combinatorial Clock | $60B+ since 1994 | Activity rules prevent bid sniping; package bidding handles complements |
| Online Ad Auctions (Google/Bing) | Generalized Second Price (GSP) | ~$200B/year globally | Position auctions; quality score adjustments; real-time bidding |
| Treasury Bond Auctions | Uniform-price or discriminatory | Trillions/year | Multiple units; strategic demand reduction |
| eBay | Proxy ascending (English variant) | Billions of transactions | Proxy bidding ≈ Vickrey; sniping as strategic response |
| Electricity Markets | Uniform-price with complex bids | Daily, regional | Start-up costs, ramping constraints, must-run status |

## The Winner's Curse

In **common-value** settings, winning is bad news — you won because everyone else thought the item was worth less. Rational bidders account for this by shading their bids below their estimate.

**Example**: Oil lease auctions. Your geological survey suggests $10M of oil. But if you win the auction, it's likely because other firms' surveys suggested less — implying the true value is lower than your estimate. Failing to adjust for the winner's curse leads to systematic overpayment.

The winner's curse is most severe with: more bidders, less precise signals, and pure common values. It's mitigated by: affiliated values, information revelation (English format), and experienced bidders.

## Sources

Read `references/sources.md` for the full bibliography — primary texts (Krishna, Milgrom, Myerson), key papers, and applied references.

## When This Applies

- Designing or analyzing any competitive allocation process
- Setting reserve prices or bidding strategies
- Evaluating whether an auction format is revenue-optimal or efficient
- Understanding real-world markets that use auction mechanisms (spectrum, advertising, procurement)
- Choosing between auction formats for a specific application

## Cross-Domain Connections

- **Investing/market-microstructure**: Equity markets are continuous double auctions — bid-ask spreads, price discovery, and market maker rebates are auction theory applied. Consult `market-microstructure/liquidity-topology` for real-world auction dynamics in order books.
- **Investing/special-situations/event-driven**: M&A bidding wars are ascending auctions with affiliated values. Winner's curse applies directly to takeover premiums — acquirers systematically overpay in contested deals.
