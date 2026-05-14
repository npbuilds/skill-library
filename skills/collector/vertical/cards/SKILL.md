---
name: cards
description: >
  Route trading-card collecting questions across the four major sub-disciplines — sports cards
  (PSA/BGS/SGC ecosystem, vintage T206 through junk-wax through modern), Pokémon (1st Ed /
  Shadowless, JP trophy cards), Magic: The Gathering (Reserved List, NM/LP/MP/HP scale,
  Alpha/Beta/Unlimited), and other TCGs (Yu-Gi-Oh, Lorcana, Flesh & Blood). Activate when the
  question touches any trading-card domain. The four sub-skills share grading infrastructure
  but each has distinct irreducible knowledge.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Cards — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope

Trading cards are the largest collectibles category by transaction volume — PSA alone grades roughly 14 million cards a year. The grading infrastructure (PSA, BGS, SGC, CGC) is shared across sub-disciplines but the irreducible knowledge differs: sports cards have era-specific economics; Pokémon has the 1st Edition Shadowless distinction; MTG has the Reserved List and a separate condition vocabulary; Yu-Gi-Oh and modern TCGs have their own dynamics.

## Routing

| User Signal | Leaf Skill | Cross-Axis Skills |
|---|---|---|
| Baseball, basketball, football, hockey cards; vintage to modern; PSA/BGS/SGC | `sports-cards` | `horizontal/grading-condition`, `horizontal/market-intelligence` |
| Pokémon; 1st Ed / Shadowless; Japanese trophy cards; PSA / CGC | `pokemon-cards` | `horizontal/authentication-provenance` for Japanese trophy material |
| Magic: The Gathering; Alpha/Beta/Unlimited; Reserved List; NM/LP/MP/HP | `mtg-collecting` | `horizontal/grading-condition` |
| Yu-Gi-Oh prize cards; Lorcana; Flesh & Blood; other TCGs | `tcg-other` | `horizontal/market-intelligence` |

## Shared Infrastructure

All four sub-disciplines use a 1–10 grading scale when slabbed by PSA, BGS, SGC, or CGC:

- **PSA** dominates for liquidity across sports / Pokémon / Yu-Gi-Oh. A PSA 10 typically commands 10–30% over a CGC 10 or BGS 9.5 in most markets.
- **BGS (Beckett)** publishes **subgrades** (centering, corners, edges, surface). A BGS 10 "Black Label" or "Pristine" (all four subgrades = 10) trades at 2–3× PSA 10 for the same card.
- **SGC** is preferred for **raw vintage** (pre-1970) cards — perceived as less punitive on era-appropriate artifacts.
- **CGC** entered cards more recently; has clawed market share with cleaner slabs and competitive turnaround. Strong in Pokémon especially.

**Population reports** (PSA Pop Report, GemRate Universal Pop Report) are the price-discovery substrate across all sub-disciplines. CardLadder provides index-style pricing on top of pop data.

## Cross-Axis Connections

- **Grading decisions** → `horizontal/grading-condition` (crackout ROI, pressing-where-applicable, subgrade economics)
- **Authentication** → `horizontal/authentication-provenance` (especially for high-end vintage, trimmed-card fraud, signed cards)
- **Pricing and comp analysis** → `horizontal/market-intelligence` (PWCC 500 context, comp discipline)
- **Storage** → `horizontal/storage-preservation` (Mylar / top-loader / slab-storage discipline)
- **Insurance** → `horizontal/insurance-risk` (cards above ~$5K should be scheduled separately)
- **Fraud patterns** → `horizontal/fraud-intelligence` (the 2019 PSA reholder/trimming scandal, the Mastro/Wagner case)

## Sub-Discipline Boundaries

Each leaf is a distinct collecting domain with its own community, venues, and economics. The director routes; the leaf delivers.

---

Connoisseur ─── The Four Card Markets Are Four Different Communities

A vintage sports card collector and a modern Pokémon collector use the same graders, the same slabs, the same population reports — and almost nothing else. The vocabulary of "centering" is universal; the canonical issues, the cultural moments, the auction venues, and the social communities are entirely separate. A serious cards collector picks one sub-discipline and goes deep; the breadth-first collector spreads thin and tends to underperform across all four.

Allocator ─── The PWCC 500 Is the Top-Tier Composite; Most Cards Sit Below It

The PWCC 500 tracks the top 500 trading-card investment assets. Most cards are not in the top 500. The asset-class return story (PWCC 500 beat S&P by 680 percentage points to August 2022) does not apply to junk-wax 1990s baseball, modern parallel cards with high populations, or any card not in the trophy tier. The asset class includes both Picasso-equivalent trophy cards and Etsy-equivalent volume cards. Allocate to the trophy tier or accept that the asset-class return is not the user's return.
