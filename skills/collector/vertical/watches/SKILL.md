---
name: watches
description: >
  Route timepiece collecting questions — vintage watches (tropical dials, ghost bezels,
  originality discipline), modern watches (Rolex/Patek/AP allocations, gray market dynamics),
  and reference-number discipline (double-signed, papers, "full set"). Activate when the
  question touches authentication of originality, polishing risk, allocation strategy, or any
  watch identification or valuation.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Watches — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope

Timepiece collecting is the asset class where **originality** matters more than any other single concept. There is no grading scale (no PSA/CGC equivalent); instead the market relies on full-set documentation, reference-number precision, and the dealer/auction-house attribution.

## Routing

| Signal | Leaf | Cross-Axis |
|---|---|---|
| Vintage Rolex, Patek, AP; tropical dials, ghost bezels, originality | `vintage-watches` | `horizontal/authentication-provenance` |
| Modern Rolex Daytona, Patek 5711, AP Royal Oak; waitlist; gray market | `modern-watches` | `horizontal/buying-mechanics` |
| Reference numbers, "full set," double-signed, papers / box / receipts | `watch-references` | `horizontal/vetting-services` |

## The Originality Doctrine

A watch's value is anchored to whether its parts are **all original** to its production year. The hierarchy:

- **All original** — case, dial, hands, bezel, crown, bracelet, movement all as-shipped (premium)
- **Service-replaced parts** — components replaced during authorized service (acceptable for daily wearers; major penalty on vintage trophies)
- **Re-dialed** — dial refinished or replaced (significant penalty, 30-50% on vintage)
- **Polished case** — case material removed (major penalty on vintage Rolex; sharp shoulders erased)
- **Frankenwatch** — assembled from parts of multiple watches (always a value penalty)

The 2017 Phillips sale of Paul Newman's own Daytona (ref. 6239) at $17.75M was driven specifically by the unpolished case.

## "Full Set" Documentation

The **full set** designation — watch + box + papers (warranty card / certificate of origin) + service records + receipts — adds significant value to vintage and modern alike. For modern Rolex Daytona or Patek 5711, "full set" is the standard for liquidity; for vintage, "full set" can double the value.

## Cross-Axis

- Authentication → `horizontal/authentication-provenance` + `horizontal/fraud-intelligence` (relume scams, redialed-as-original)
- Pricing → `horizontal/market-intelligence` (Phillips Watches as the canonical comp; Chrono24 as marketplace data)
- Buying mechanics → `horizontal/buying-mechanics` (auction vs allocation vs gray market)
- Insurance → `horizontal/insurance-risk` (scheduled separately; some carriers require recent appraisals)
- Selling → `horizontal/selling-deaccessioning` (Phillips Watches under Aurel Bacs is the premier consignment venue)

---

Connoisseur ─── Read the Case Lines Before the Dial

The first thing the trained watch eye looks at on a vintage Rolex is the case. The sharpness of the lugs, the integrity of the bevels, the way light catches the shoulders — these tell you whether the watch has been polished. A polished Submariner has rounded shoulders where it should have sharp ones; the case is the watch's first sentence and the dial is the second.

Allocator ─── Polished Cases Cost 30-50 Percent on Vintage Trophies

A 1960s Submariner with sharp unpolished case in original configuration trades 30-50% above the same reference with polished case in similar otherwise-original condition. The discount is not recoverable — polishing is irreversible. The collector who buys vintage Rolex without inspecting the case (or having a trusted dealer inspect) is exposed to the single largest preventable value loss in the category. Use Phillips, Christie's, or a CINOA member dealer; never buy vintage trophies from sellers who cannot or will not allow case inspection.
