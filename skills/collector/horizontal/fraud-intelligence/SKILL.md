---
name: fraud-intelligence
description: >
  A pattern library of named scandals, forgery vectors, and red flag clusters across collecting
  domains. Use when a piece's story sounds too good, when provenance is suspiciously fresh, when
  a deal is meaningfully below comparable market, when a dealer's behavior triggers caution, or
  when modern AI-generated provenance is suspected. Covers Knoedler, Kurniawan, Mastro/Wagner,
  Operation Bullpen, the PSA reholder scandal, the CGC defamation case, and the recurring
  patterns these scandals reveal.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
---

# Counterfeit & Fraud Intelligence — Patterns That Repeat

> **Type:** Knowledge
> **Suite:** The Collector
> **Axis:** Horizontal
> **Parent:** collector

## Why This Skill Exists

Every collecting domain has been touched by major fraud. The patterns repeat across asset classes with eerie consistency: a charismatic insider, provenance gaps nobody pushed on, demand exceeding genuine supply, scientific analysis that could have caught it but was never run. The lesson generalizes — **when supply seems implausibly available, supply is implausibly available**.

This skill catalogs the named scandals so the collector can pattern-match future fraud against past fraud. It is the case library that supports the workflow in `horizontal/authentication-provenance/`.

## The Headline Cases

### Knoedler Gallery (1994–2011) — Fine Art

The most consequential American fine-art forgery scandal of the modern era.

**Scope:** ~40 forged paintings sold over 15+ years, attributed to Jackson Pollock, Mark Rothko, Robert Motherwell, Willem de Kooning, Barnett Newman, Richard Diebenkorn, and others. Total fraudulent sales: roughly **$80 million**.

**The Mechanism:** Glafira Rosales, a Long Island dealer, supplied works claiming they came from a mysterious "Mr. X" — a Spanish collector whose identity she would not reveal. Knoedler Gallery, founded in 1846 (165 years old at closure), sold the works through its president Ann Freedman. Forger Pei-Shen Qian, a Chinese-born painter living in Queens, produced the canvases for as little as $5,000 each — sold by the gallery for as much as $17 million.

**How it ended:** Forensic analysis caught anachronistic pigments. Knoedler closed in 2011. Rosales pleaded guilty in 2013. Multiple civil suits followed. Documentaries: *Made You Look* (2020), *Driven to Abstraction* (2019).

**The patterns to extract:**

1. **Charismatic intermediary with vague upstream provenance** — "Mr. X" should have been a question, not a story
2. **Provenance gaps everyone agreed not to push on** — the gallery and its sophisticated buyers participated in the agreement
3. **Forensic analysis that wasn't run** — a $5,000 XRF would have flagged anachronistic pigments years earlier
4. **The gallery's reputation as the substitute for due diligence** — a 165-year-old name is not a substitute for material analysis
5. **Pricing meaningfully below the comparable** — many Knoedler-sold "Pollocks" were priced 30–50% below auction comps; sophisticated buyers rationalized this as "fresh to market" rather than as a red flag

### Rudy Kurniawan (1980s–2012) — Wine

The largest wine forgery scandal on record.

**Scope:** Counterfeited rare Burgundies — Domaine de la Romanée-Conti (DRC), Domaine Ponsot, Domaine Roumier — using mid-tier California wine and fabricated labels printed in his kitchen. Total: tens of millions of dollars in fraudulent sales through Acker Merrall & Condit and other channels.

**The Mechanism:** Kurniawan possessed genuine encyclopedic palate and library knowledge — he was not a stupid forger. He used real bottle shapes from genuine vintages, decanted real wine, refilled bottles with carefully blended substitutes, and printed labels with deliberate flaws to make them seem more authentic. He sold to sophisticated collectors who never thought to question why mysterious bottles of impossible-to-source vintages kept arriving in his cellar.

**How it ended:** Domaine Ponsot's Laurent Ponsot caught a bottle being auctioned that pre-dated the domain's first production of that wine. William Koch had ~$2.1M of Kurniawan-source wine; five bottles ($75K) were Kurniawan fakes including one with an Elmer's Glue label (Elmer's was not produced until 1947, yet the bottle was supposedly 1857). Federal trial 2013; 10-year sentence 2014; deported to Indonesia 2020. Counterfeits **still circulate** in the wine market.

**The patterns:**

1. **Implausible supply** — Kurniawan was sourcing volumes of rare wine that exceeded what should have been available in any private cellar
2. **No verifiable cellar of origin** — his "personal cellar" was the source for everything
3. **Sophisticated palate masking sophisticated fraud** — being knowledgeable does not mean being honest
4. **Detection by physical analysis** — Elmer's Glue, paper composition, label printing techniques eventually revealed the fakes
5. **Continued contamination** — the secondary market still contains Kurniawan-source bottles; **always check Burgundy provenance from the 2000–2012 era**

### Bill Mastro & the Gretzky-McNall T206 Wagner — Sports Cards

The most famous card in the world had been trimmed.

**Scope:** The T206 Honus Wagner card, owned in succession by Wayne Gretzky and Bruce McNall, then sold by Bill Mastro through Mastro Auctions — the canonical "Gretzky Wagner" — had been trimmed by Mastro himself before it entered the market chain.

**The Mechanism:** Mastro acquired the card raw, trimmed its edges to improve the grade, then sold it through his auction house. The card was graded PSA 8 (the highest grade for the most iconic card in the hobby), sold for $451K in 1991, then $640K (1995), $1.27M (2000), $2.35M (2007), then most recently $7.25M (2022). The trimming was alleged for years; Mastro pleaded guilty to mail fraud in 2013, specifically admitting to trimming the Wagner.

**The patterns:**

1. **Disclosed material alteration is fraud** — the value penalty for known trimming would have been catastrophic; the fraud was concealing it
2. **The auction house and the alterer were the same person** — concentrated trust, concentrated risk
3. **The card's iconic status protected the fraud** — buyers wanted the trophy badly enough to skip questions

### Operation Bullpen (Late 1990s–2000s) — Sports Memorabilia

FBI long-running investigation into forged sports autographs.

**Scope:** A network producing forged signatures on baseballs, photos, jerseys, with COAs from compromised authenticators. Indictments of dozens; conviction of multiple ring leaders; recovery of millions in fraudulent merchandise.

**The lasting impact:** The autograph market shifted decisively toward **witnessed authentication** — PSA/DNA, JSA, BAS sending personnel to actual events where signatures are obtained. Opinion-only authentication (forensic analysis after the fact) became substantially less trusted for high-value signatures.

### The 2019 PSA Reholder/Trimming Scandal — Sports Cards

A circle of dealers cracked high-grade cards, trimmed them slightly, and resubmitted to PSA for higher grades. Discovery via population-report anomalies (cards "appearing" at grades they had not previously held).

**The patterns:**

1. **Crackouts and reholders are legitimate; trimming is fraud** — the line is whether material is removed
2. **Pop-report discontinuities are the canary** — sudden appearances of higher-grade copies of population-stable cards
3. **The graders themselves are not perfect** — even PSA-graded slabs can house tampered cards

### CGC v. Meyers Defamation Verdict (2024) — Comics

A Philadelphia jury awarded $10M in damages to a comic restorer that CGC had accused of work he did not do. The verdict illustrated the legal soft underbelly of "house authority" — even the major grading bodies can be wrong about restoration assessments.

**The lesson:** A purple-label CGC slab is not infallible. Restoration calls are judgments; judgments can be wrong; recourse exists when they are.

### Smaller Categories — Recurring Patterns

- **Whisky cask fraud** — FCA-flagged scams promising returns on cask investments that turn out to be either non-existent casks or non-collectible blends
- **NFT wash trading** — the same wallet selling NFTs to itself to inflate apparent demand, especially 2021–2022
- **"Antique" CITES-protected materials sold as pre-ban** — ivory, tortoiseshell, rosewood, with fake age documentation
- **Restored watches sold as original** — re-lumed dials, redialed Submariners, polished cases not disclosed
- **First editions with married parts** — original book block with a facsimile dust jacket, sold as fully original

## Universal Red Flag Clusters

Patterns that recur across the cases above. Any single signal can be innocuous; clusters are the threat.

### Cluster 1 — Provenance Issues
- "Fresh to market" with no documented prior owners
- Story-driven provenance ("found in a Swiss attic," "from a Spanish collector who wishes to remain anonymous")
- Provenance jumping a politically charged decade (1933–1945 in Europe, 1949–1979 in Mainland China, etc.)
- Refusal to identify the upstream consignor

### Cluster 2 — Pricing Anomalies
- Pricing meaningfully below comparable market (10–30% under recent comps with no condition or grade explanation)
- "Wholesale pricing" offered to a non-dealer
- Pressure to close before independent verification can be obtained

### Cluster 3 — Behavioral Signals
- Charismatic seller with vague but consistent stories
- Reluctance to allow forensic testing or independent expertise
- Pushing for cash or unusual payment routing
- Vague-becoming-evolving provenance under questioning

### Cluster 4 — Material / Documentary Issues
- COAs from entities the user has never heard of, or from defunct authentication boards
- Documentary errors (wrong period typography, wrong period paper, anachronistic adhesives)
- "Estate paperwork" that can be backdated or forged

### Cluster 5 — Modern AI Risks
- Synthetic photographs of "the artist holding the work" — increasingly easy to generate
- Fabricated historical Instagram accounts as "social proof" of prior ownership
- AI-generated estate paperwork with subtle but detectable artifacts (Em dashes used wrong, period vocabulary mistakes, typography inconsistencies)
- Generative provenance — fake exhibition catalogs printed on-demand

## The "Too-Good-a-Deal" Filter

Efficient enough markets mean genuine bargains in the headline categories are rare. When a deal looks 30%+ below comparable market and the seller cannot articulate a clean reason (estate liquidation under documented duress, divorce-driven sale, specific buyer-collateral situation), assume the bargain is the bait.

The corollary: real bargains exist, but they are found by **showing up consistently** to regional auctions, estate sales, and field venues where sellers are unsophisticated about value — not by waiting for sophisticated sellers to mis-price.

## Workflow — Pattern-Match a Suspect Acquisition

1. **Identify the cluster** — which named scandal does this resemble? Knoedler-pattern (vague upstream provenance + below-market pricing + great gallery name)? Kurniawan-pattern (implausible supply + no verifiable cellar)? Operation Bullpen-pattern (signatures without witnessed authentication)?
2. **Enumerate red flags** — count signals across the five clusters. One signal is innocuous; three or more is action-worthy.
3. **Run the database checks** — Art Loss Register, IFAR, Interpol, USFWS for CITES materials, FBI Art Crime Team for high-profile theft
4. **Demand the missing documentation** — provenance, COA chain, prior auction comparables
5. **Commission independent expertise** — forensic analysis, expert opinion, second opinions from non-conflicted parties
6. **Walk if the seller resists step 5** — a confident seller welcomes verification; an evasive one is signaling

---

Connoisseur ─── The Fraud You Catch Is Less Important Than the Fraud You Don't Pursue

Most of the famous frauds are caught by people who refuse the deal — not by people who buy and later prove it false. Knoedler buyers had Pollock-Krasner Foundation skepticism available to them throughout the 1990s and chose to ignore it. Kurniawan buyers knew the volumes were implausible and chose to believe. The defense is in the doorway: when the story sounds too good and the provenance is too vague and the price is too sharp, the answer is "no thank you." The buyer who walks away has lost nothing; the buyer who proceeds and is wrong has lost everything.

Allocator ─── Fraud Costs Are Asymmetric and Often Unrecoverable

A successful fraud claim against an auction house or dealer may recover the purchase price, sometimes plus interest. It rarely recovers transaction costs, opportunity costs, legal fees, or the emotional cost of years of litigation. The downside of a $500K acquisition that turns out to be a fake includes: $500K cash gone, $50K in legal fees, 2–4 years of process, and substantial reputational drag if the fraud becomes public. The upside of *not* buying that piece is the next piece — bought from a vetted seller with verified provenance — which over a 20-year hold will outperform anyway. The math overwhelmingly favors prudence on every individual transaction.
