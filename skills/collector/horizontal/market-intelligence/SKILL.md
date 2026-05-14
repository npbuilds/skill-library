---
name: market-intelligence
description: >
  Price illiquid collectibles using completed-sales data, named indices, and auction-house math.
  Use when valuing a piece for purchase, sale, insurance, or donation; reading auction comps;
  computing all-in cost from hammer price; or interpreting cross-asset indices (Liv-ex, PWCC 500,
  Mei Moses, Knight Frank Luxury Investment Index). Covers buyer's premium tables, liquidity
  tiers, the bid-ask spread on illiquid assets, and the "sold not asking" discipline that
  separates real comps from noise.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Market Intelligence & Valuation — Pricing the Illiquid

> **Type:** Knowledge
> **Suite:** The Collector
> **Axis:** Horizontal
> **Parent:** collector

## The Three Pricing Signals

Every collectible price comes from one of three sources, in descending order of trustworthiness:

1. **Auction comparables** — completed sales at named auction houses, with full hammer + buyer's premium + lot detail.
2. **Dealer markup math** — wholesale-to-retail spreads typically 2× at major dealers, with negotiation room of 5–15% on most pieces.
3. **Private treaty** — off-market negotiated sales. Highest information asymmetry; weakest as a public comp.

**The "sold not asking" rule:** eBay asking prices, dealer-listed asking prices, and "I heard one went for…" are noise. Only completed transactions count, and only completed transactions at named venues with auditable records produce a trustworthy comp.

## Buyer's Premium Math

Headline auction prices are deceptive. The buyer's premium (BP) is paid on top of the hammer price; sales tax is paid on top of the hammer+BP combination; shipping and insurance are paid on top of that. The all-in number is what the buyer actually writes a check for.

### Current BP Tables (2026)

| Auction House | Tier 1 (up to ~$1M hammer) | Tier 2 (~$1M–6M) | Tier 3 (above ~$6M) |
|---|---|---|---|
| Christie's NY | 26% | 21% | 15% |
| Sotheby's NY | 27% | 22% | 15% |
| Phillips NY | 27% | 21% | 15% |
| Bonhams | 27.5% (up to $50K) | declining tiers | varies |
| Heritage Auctions | 25% (flat or near-flat in most categories) | — | — |

(These rates shift over time; check the current Conditions of Sale before bidding.)

### Worked Example — $100,000 Hammer at Sotheby's NY

- Hammer: $100,000
- BP at 27%: +$27,000
- Subtotal: $127,000
- NY sales tax (8.875% on hammer + BP, if ship-to-NY): +$11,266
- Shipping + insurance: +$1,500–3,000
- **All-in total: $139,766 – $141,266**

The $100K headline is 40% below the buyer's real outlay.

### Worked Example — $1,000,000 Hammer at Sotheby's NY

- Hammer: $1,000,000
- BP at 27% on first $1M: +$270,000
- Wait — the tier breakpoint is $1M, so this is the borderline. Some houses charge the higher rate on the first $1M and the lower rate above. Check the specific Conditions of Sale.
- Effective BP at this exact point: ~$270,000
- Subtotal: $1,270,000
- Sales tax in many jurisdictions, freeport-shipping mechanics, ITAR/CITES for certain materials
- **All-in total: $1.30M+ depending on jurisdiction**

The headline-to-all-in math shifts by ~25–30% across most major-house categories. Always quote the all-in.

## The Major Indices

Cross-asset indices serve two purposes: smoothing noise in any single category, and providing a benchmark against which a collector can ask "did I do better or worse than the asset class?"

### Liv-ex (Wine)

The London International Vintners Exchange — the closest thing to a real-time price-discovery system in collectibles.

- **Liv-ex 100** — the 100 most-traded wines, weighted by liquidity
- **Liv-ex 1000** — broader benchmark, 1,000 wines across regions
- **Bordeaux 500** — Bordeaux-specific
- **Burgundy 150** — Burgundy-specific
- **Champagne 50, Italy 100, Rest of World 60** — regional indices

Liv-ex is a members-only dealer exchange; published indices are public. Read the indices for asset-class trajectory; read the order book (members-only) for live price discovery.

### PWCC 500 (Sports Cards)

The PWCC 500 tracks the top 500 trading-card investment assets. It outperformed the S&P 500 by 680 percentage points between January 2008 and August 2022 — a result that drove much of the 2020–2022 retail enthusiasm. After the 2022 peak, the index has declined; the long-horizon Sharpe ratio is competitive with equities but the friction (slabbing, storage, sale costs) eats meaningfully into realized return.

### Mei Moses (Fine Art)

Acquired by Sotheby's in 2016. Uses a repeat-sale methodology (compares the same painting selling in two different years), avoiding the heterogeneity bias of "average price" indices. Coverage extends to ~200 years of repeat-sale data. Mei Moses art correlation to S&P is reported at ~0.04 — genuine diversification, though the friction is also real.

### Knight Frank Luxury Investment Index (KFLII)

The multi-asset basket. Tracks 10 luxury collectibles: art, classic cars, coins, coloured diamonds, fine wine, furniture, handbags, jewellery, rare whisky, watches. The index returned ~7% in the 12 months ending June 2023; longer-horizon (10-year) returns have been competitive with public equities on a pre-friction basis.

### Other Indices to Know

- **Mei Moses All Art** sub-indices by category
- **Artprice / Artnet Price Database** — auction-level, deep historical data
- **Wine-Searcher** — aggregator for wine prices across the global market (asking + completed)
- **CardLadder, GoCollect** — index layers for cards and comics
- **Chrono24** — watch marketplace data; useful for current-market estimates but not a true index
- **Rare Whisky 101 Apex 1000 / Icon 100** — whisky indices, the "Liv-ex of whisky"

## Liquidity Tiers

Every collectible category has a tier structure. Knowing where a specific piece sits affects everything from bid-ask expectations to sale timing.

| Tier | Description | Bid-Ask | Example |
|---|---|---|---|
| **Tier 1** — Always-bid | Daily transactions, multiple ready buyers at any time | 5–15% | PSA 10 Charizard Base Set; Rolex Daytona ref. 116500LN; PSA 10 1986 Fleer Jordan |
| **Tier 2** — Auction-only | Liquidity exists but only at major-house sales every 3–6 months | 20–40% | Mid-tier vintage Patek; specific high-grade comics with population <50; second-tier blue-chip art |
| **Tier 3** — Need-a-finder | Liquidity requires actively cultivated dealer network or specialist auction | 40–70% | Niche category items; restored or qualified-grade examples; obscure regional art |

The tier structure is asymmetric to size. A $5K item in Tier 3 may take 12 months to sell. A $5M item in Tier 1 (a major blue-chip painting) can transact in 60–90 days at a major-house evening sale.

## The "Fresh to Market" Premium

Items emerging from a 30+ year private collection price 20–40% above the same item that has been in regular auction rotation. The premium is informational: a piece that has been "shopped" extensively in recent years is presumed to have been passed on by sophisticated buyers; a piece that has been untouched for decades has not been priced by recent market sophistication and may be undervalued or simply hasn't been measured.

The trade: buy fresh-to-market when you can; understand that the premium you pay is for the absence of negative selection.

## Reading Comps

When the user is buying or selling, comp analysis follows a discipline:

1. **Same item, same grade.** Not "similar." A PSA 10 1986 Fleer Jordan rookie comps against other PSA 10 1986 Fleer Jordan rookies — not against PSA 9.5s, not against unrelated rookies.
2. **Same time horizon.** Comps from >12 months ago are stale in volatile markets. Comps from <30 days ago are the most actionable.
3. **Same venue tier.** Heritage Signature comps are stronger than eBay BIN. Sotheby's evening sale comps are stronger than dealer treaty.
4. **At least 3 comps.** One comp is anecdote. Two are coincidence. Three are a trend.
5. **Excluded extremes.** Drop the highest and lowest from the comp set; the central tendency is the price; the extremes are the variance.

---

Connoisseur ─── A Comp Is a Story About a Specific Object

Two PSA 10 cards never sell for the same price for the same reason. One was a Heritage Signature lot with a five-figure underbidder duel; the other was a Goldin marketplace fixed price. The headline numbers may be identical but the meaning is different. The Connoisseur reads what the comp does not say — the auction sequence (lot #3 sells differently than lot #47), the room dynamic, who consigned it, who bid. The number is the tip of an iceberg.

Allocator ─── The Index Is Not the Asset

The PWCC 500 may have beaten the S&P by 680 percentage points to August 2022. Your specific card has not. Indices report the median liquid path; your asset is a single observation on a different distribution. Treat indices as macro signal — what the asset class is doing — and individual comp sets as micro signal — what your asset is worth. Confusing the two leads to bad portfolio decisions and worse exit timing.
