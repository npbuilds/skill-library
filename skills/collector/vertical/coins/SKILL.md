---
name: coins
description: >
  Route numismatic questions — US coins (Sheldon 1-70 scale, RD/RB/BN designations, FS/FBL/FH
  strike designations), world coins (broader category, region-specific markets), and die
  varieties (1955 DDO, 1969-S DDO, the specialist subfield where die identity matters more
  than grade). The most codified condition system in collecting via the Sheldon scale.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Coins — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope

Numismatics is the most rigorously codified collecting domain. The **Sheldon scale (1-70)**, developed by William Sheldon in 1949, provides the most precise condition vocabulary in any collecting category. PCGS and NGC are the duopoly grading services; ANACS is a credible third. The market is mature, the data is deep, and the trophy tier is well-defined.

## Routing

| Signal | Leaf | Cross-Axis |
|---|---|---|
| US coins, Sheldon scale, mint marks, RD/RB/BN, US numismatics | `us-coins` | `horizontal/grading-condition` |
| British, European, Asian, ancient coins, gold sovereigns | `world-coins` | `horizontal/authentication-provenance` |
| Doubled-die varieties, mint errors, the variety-specialist subfield | `die-varieties` | `horizontal/grading-condition` |

## The Sheldon Scale in One Table

| Grade | Designation | Description |
|---|---|---|
| P-1 | Poor | Identification just possible |
| FR-2 | Fair | Partial outline visible |
| AG-3 | About Good | Rims worn into design |
| G-4, G-6 | Good | Heavy wear; design outline visible |
| VG-8, VG-10 | Very Good | More details than Good; minor surface preservation |
| F-12, F-15 | Fine | Major details clear; minor wear |
| VF-20 to VF-35 | Very Fine | Most details preserved; light wear on highest points |
| EF-40, EF-45 | Extremely Fine | Slight wear only on highest points |
| AU-50 to AU-58 | About Uncirculated | Friction wear traces only |
| MS-60 to MS-70 | Mint State | Uncirculated; MS-65 = Gem; MS-70 = perfect |
| PF-60 to PF-70 | Proof | Proof coins; PF/PR prefix |

The MS-60 to MS-70 range is where most collector value lives. The spread between MS-65 and MS-67 on a key date can be 10-50×; between MS-67 and MS-70 on rare issues can be 100×.

## Cross-Axis

- Authentication → `horizontal/authentication-provenance` (counterfeit coins are sophisticated; PCGS/NGC slab provides authentication)
- Pricing → `horizontal/market-intelligence` (Heritage / Stack's Bowers / Great Collections; PCGS CoinFacts; NGC Coin Explorer)
- Storage → `horizontal/storage-preservation` (Air-tite holders; anti-tarnish strips; dry storage)
- Insurance → `horizontal/insurance-risk` (graded coins above $5K scheduled separately)
- Tax / estate → `horizontal/tax-estate-legal` (28% collectibles cap gains; step-up at death; reportable transactions over $10K under Form 8300)
- Buying mechanics → `horizontal/buying-mechanics` (Heritage signature sales; weekly online events)

## What Makes Coins Distinct

- **Cleaning is catastrophic** — "Details" graded coins (PCGS Genuine, NGC Details) trade at 30-70% of problem-free graded coins. A cleaned coin is permanently damaged in value.
- **Strike vs preservation are separate considerations** — a perfectly preserved coin may have a weak strike (incomplete details on the die's deepest cuts); a sharply struck coin may have surface marks. Both affect grade.
- **Die varieties can dominate date and mintmark** — a common 1955 Lincoln cent is $1; the 1955 Doubled Die Obverse (DDO) is $1,000-$50,000+ depending on grade. The variety, not the date, is the asset.
- **CAC sticker** — the Certified Acceptance Corporation (founded by John Albanese) reviews PCGS and NGC slabs and applies a green sticker to coins that meet CAC's stricter standard, or a gold sticker for the highest tier. CAC-stickered coins trade at 5-30% premium to non-stickered slabs.

---

Connoisseur ─── A Coin Without Original Surfaces Is a Different Coin

The single largest mistake in numismatics is cleaning. A coin's original surfaces — the toning that has developed over decades or centuries — are part of the coin's identity. Removing them with abrasion, dipping, or chemical treatment may make the coin look brighter but destroys the original surfaces forever. The trained eye distinguishes original surfaces from cleaned in seconds; the market punishes cleaned coins severely.

Allocator ─── CAC Stickers Compound Modest Premiums Into Meaningful Differentials

A PCGS MS-65 Morgan dollar without CAC trades at price X. The same grade with green CAC trades 5-15% above X; with gold CAC, 15-40% above X. The CAC review is essentially a second-opinion overlay that the market rewards. For long-hold coin investment, CAC-stickered slabs preserve the premium and are more liquid in secondary sale. Specify CAC stickers in your acquisitions when premium-tier holding is the goal.
