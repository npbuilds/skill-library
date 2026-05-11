---
name: art
description: >
  Route fine-art collecting questions — paintings, prints and multiples, contemporary, Old
  Masters, photography. Activate when the question touches authentication via catalogue
  raisonné, attribution hierarchy ("Attributed to" / "Studio of" / "Circle of"), primary vs
  secondary market dynamics, edition fractions for prints, condition reports for paintings, or
  the major auction venues (Christie's, Sotheby's, Phillips, Bonhams, Heritage). The most
  complex of the verticals, requiring discipline across five sub-domains.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Art — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope

Fine art is the most complex domain in collecting — no grading scale, no slabbing, deeply variable per-artist economics, and a vocabulary refined over five centuries. This director routes to five leaf skills, each covering a distinct sub-domain with its own authentication frameworks, market venues, and collector communities.

## Routing

| User Signal | Leaf Skill | Cross-Axis Skills |
|---|---|---|
| Oil/canvas/panel paintings, condition reports, primary vs secondary market | `paintings` | `horizontal/authentication-provenance`, `horizontal/market-intelligence` |
| Prints, multiples, edition fractions (AP/HC/EA/PP/BAT), lithographs, etchings, silkscreens | `prints-multiples` | `horizontal/grading-condition` |
| Contemporary art, gallery waiting lists, primary access, blue-chip living artists | `contemporary` | `horizontal/buying-mechanics`, `horizontal/discovery-sourcing` |
| Old Masters, attribution hierarchy, panel paintings, dendrochronology, provenance research | `old-masters` | `horizontal/authentication-provenance`, `collector/references/attribution-hierarchy` |
| Photography, edition sizes, vintage vs lifetime print, signed-mat vs verso | `photography` | `horizontal/authentication-provenance` |

## What Makes Art Different

### No Grading Scale

Unlike comics, cards, or coins, paintings have no codified condition number. Instead, condition is described in a **condition report** — a prose document by a trained conservator covering structural integrity, paint film stability, restoration history, varnish age, frame condition, and any specific concerns.

The implication: the user must read condition reports carefully, understand the vocabulary, and ask follow-up questions. "Minor restorations consistent with age" can hide major work.

### Catalogue Raisonné as Authentication

For artists with a published **catalogue raisonné** (a scholarly complete-works catalog), inclusion is the gold standard of attribution. Exclusion is not conclusive evidence against authenticity — many pieces are unknown at the time of cataloging — but it is a meaningful signal.

Major raisonné committees historically included the Pollock-Krasner Foundation, the Warhol Authentication Board, the Calder Foundation — **most of these committees have disbanded due to litigation risk**, leaving authentication in a difficult state for those artists.

### Attribution Hierarchy

The catalog-language ladder (see `collector/references/attribution-hierarchy.md`):

- **Artist name with no qualifier** → full attribution, with 5-year limited authenticity warranty from major houses
- **"Attributed to"** → warranty withdrawn; 30-50% value reduction
- **"Studio of"** → produced in artist's studio, possibly with their involvement; 50-70% reduction from full attribution
- **"Circle of"** → unidentified hand of the period working closely in the style
- **"Follower of"** → in the style, by someone working from the example
- **"Manner of"** → in the style, possibly much later imitator
- **"After"** → direct copy of a known work by an unidentified hand

Each step downward halves or quarters value.

### Primary vs Secondary Market

- **Primary market** — gallery sales of new work by living artists. Fixed price (no auction). Waiting lists for blue-chip living artists. Allocation depends on collector relationship and institutional credibility.
- **Secondary market** — auction and dealer resale. Public price discovery. Buyer's premium adds 21-27% on top of hammer at major houses.

For contemporary work, the gap between primary (gallery) price and secondary (auction) price can be enormous — and the **flipping ethics** matter. Flipping a primary-market acquisition immediately at auction can damage relationships with the gallery and the artist's estate.

### Provenance Critical for Pre-1945 European Art

Any European work that traded between 1933 and 1945 with documented Jewish ownership and unexplained gaps may be subject to **restitution litigation** under the Holocaust Era Assets and Washington Conference Principles. The Art Loss Register and IFAR are critical pre-purchase databases. A gap in provenance during this period is a major red flag.

## Cross-Axis Connections

Almost every art question requires loading multiple horizontal skills:

- Authentication → `horizontal/authentication-provenance` (forensic methods, COA hierarchy, scientific analysis)
- Attribution language → `collector/references/attribution-hierarchy`
- Pricing → `horizontal/market-intelligence` (Mei Moses, Artnet, hammer + BP math)
- Storage → `horizontal/storage-preservation` (climate, UV, conservation)
- Insurance → `horizontal/insurance-risk` (fine arts policies, scheduling)
- Tax / charitable / estate → `horizontal/tax-estate-legal` (28% cap gains, FMV deduction, step-up)
- Counterfeit / fraud → `horizontal/fraud-intelligence` (Knoedler case, attribution disputes)
- Vetting dealers → `horizontal/vetting-services` (ADAA, CINOA, USPAP)
- Buying at auction → `horizontal/buying-mechanics`
- Selling / consignment → `horizontal/selling-deaccessioning`

## Sub-Domain Boundaries

The five sub-domains overlap but have distinct epistemologies:

- **Paintings** is the broadest — covers oil, acrylic, watercolor, gouache, mixed-media on canvas, panel, paper
- **Prints and Multiples** is structurally different — limited editions with fractional numbering, defined techniques (lithograph, etching, silkscreen, woodcut, photogravure)
- **Contemporary** is a primary-market-driven sub-domain with gallery relationships rather than auction-house-driven secondary economics
- **Old Masters** has the highest discipline requirements — attribution work, panel-painting science, multi-century provenance research
- **Photography** is its own discipline — edition sizes, the vintage-print distinction, signature placement conventions

---

Connoisseur ─── The Catalogue Raisonné Is the First Filter

Before any other due diligence on a major work, the question is: is this work in the catalogue raisonné? For Picasso, Matisse, Pollock, Calder, Lichtenstein, Warhol — the major artists have or had raisonné committees, and inclusion is the foundation of authenticity. A work claiming attribution to one of these artists but not in the raisonné is not necessarily a forgery — but it is a major question that requires explanation. The collector who treats raisonné inclusion as the first filter avoids the largest single class of attribution disputes.

Allocator ─── Provenance Adds 30 Percent; Provenance Gaps Subtract 40+

A clean documented provenance — gallery to first collector to second collector to consignor, with exhibition history and raisonné inclusion — can add 30-60% to a piece's auction estimate. A 1933-1945 European provenance gap can subtract 40% — or, if restitution litigation is triggered, can subtract 100%. The cost of pre-purchase provenance research (Art Loss Register, IFAR, raisonné committee consultation) is typically $1-5K against the scale of the asset. Do the work; price the certainty.
