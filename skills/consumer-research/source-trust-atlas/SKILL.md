---
name: source-trust-atlas
description: >
  Maps consumer review sources to trust tiers and routes product categories to the sources
  worth searching. Use when planning where to research a purchase, deciding how much weight a
  review source deserves, or checking whether a review is too stale to trust. Called by emptor
  during the source-plan phase; also useful standalone when the user asks "which review sites
  can I trust for X?".
metadata:
  author: nirav
  version: "1.0"
type: knowledge
compatibility: Designed for Claude Code
---

# Source Trust Atlas — The Cartographer

Knowledge skill: which consumer review sources to trust, per category, as of 2026 — and how that trust decays. Grounded in `research/consumer-research-landscape-2026.md`.

## Description

Consumer review territory is adversarial. Affiliate SEO farms dominate generic search results, AI-generated reviews grow ~80% month-over-month, and merchants now optimize content specifically to manipulate LLM recommendations. This atlas encodes the defensive map: a four-tier trust model, per-category source routing, freshness decay rules, and site-scoped search strategy.

## Core Content

### The Four Tiers

| Tier | Who | Why | Weight |
|---|---|---|---|
| **1 — Independent testers** | Consumer Reports, Rtings, Which? (UK), America's Test Kitchen, Project Farm | Financial independence (no ads), self-funded/anonymous product purchases, no free samples, published methodology | Primary evidence |
| **2 — Independent but affiliate-funded** | Wirecutter, Good Housekeeping Institute, TechRadar, CNET | Real testing, editorial independence, but affiliate revenue and unpublished rubrics | Strong corroboration |
| **3 — Crowd sources** | Reddit, YouTube reviewers, Capterra | Genuine expertise coexists with documented astroturfing and unverifiable sponsorship | Hypothesis generation; verify before weighting |
| **4 — Adversarial content** | "Best X 2026" affiliate SEO sites, AI content farms, manufacturer/merchant copy | Documented spam takeover of product search; AI-SEO gaming tools target LLM recommendations | Never evidence. Treat as claims to verify |

Full roster with rationale, affiliate-disclosure status, and known caveats: `references/tier-tables.md`.

### Search Strategy

1. **Never run generic "best X" queries** — Google product search is documented as degraded (academic study; ~10% accuracy drop; SEO spam takeover).
2. **Site-scope every scan query** to Tier 1-2 sources for the category, e.g. `site:rtings.com robot vacuum`, `site:consumerreports.org OR site:wirecutter.com <product>`.
3. **Reddit/YouTube only as a second pass** for failure modes and long-term ownership reports — with astroturf checks (account age, posting pattern, cross-thread repetition) before treating any thread as evidence.
4. **Manufacturer/merchant pages**: specs only, every claim tagged unverified until triangulated.

### Category Routing

| Category | First | Then | Caution |
|---|---|---|---|
| TVs / audio / monitors / peripherals | Rtings | Consumer Reports, Wirecutter | enthusiast-forum methodology disputes exist |
| Major appliances | Consumer Reports | Which?, Wirecutter | durability data matters most |
| Kitchen gear | America's Test Kitchen | Wirecutter, GH Institute | ATK scope is narrow but gold |
| Tools / outdoor / hardware | Project Farm | Consumer Reports, Wirecutter | YouTube comparisons vary in rigor |
| Software / SaaS | Capterra + TechRadar | recent hands-on reviews | fastest decay; check test dates |
| Services (trades, repair, local) | No institutional source | Reddit + local reviews with astroturf protocol; word-of-mouth | weakest category — flag low confidence |

Extended routing with per-category query templates: `references/category-routing.md`.

### Freshness Decay

Review credibility decays. Apply these horizons when weighing evidence and stamping briefs:

| Source tier / type | Trust horizon |
|---|---|
| Tier 1 reviews | ~12 months |
| Tier 2 reviews | ~6 months |
| Software/SaaS reviews (any tier) | ~3 months |
| Prices and availability | days — always date-stamp, never carry forward |

Every brief must state when its evidence goes stale. **This atlas decays too**: tiers are a 2026 snapshot — during `deep` runs, re-verify that a source's independence model still holds (ownership changes, ad-model shifts) before leaning on its tier.

## Diagnostic Cues

- Source not in the atlas? Score it on the Tier-1 traits: independent funding, self-purchased products, published methodology, disclosed revenue. Two or fewer → treat as Tier 3 at best.
- A "review" page with affiliate links on every product name, no test photos, and a current-year title is Tier 4 regardless of search rank.
- FTC fake-review rule (effective Oct 2024): documented violations by a seller are a standing reputational red flag.

## Common Mistakes

1. Treating repetition across Tier 3/4 sources as corroboration — affiliate farms syndicate the same content.
2. Using a 2-year-old Tier 1 review for a product line that has since been revised.
3. Letting one charismatic YouTube review outweigh instrumented Tier 1 testing.
4. Trusting merchant spec sheets as evidence rather than claims.

## Related Skills

- `emptor` consumes this atlas in its source-plan phase; `product-verifier` and `review-forensics` apply it when qualifying evidence.
- `source-triangulator` (research domain) handles general source independence; this atlas adds the consumer-specific tier map.

## Learn Block

After internalizing this atlas, learn `review-forensics` — the per-product authenticity check applied once candidate reviews are found.
