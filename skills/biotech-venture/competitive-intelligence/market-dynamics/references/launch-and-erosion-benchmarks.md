# Launch Dynamics & Erosion Benchmarks — Extended Reference

Order-of-entry advantage, generic vs biosimilar erosion curves, net-vs-list price dynamics, and named peak-sales analogs for competitive and revenue forecasting. Every figure is primary-sourced with vintage. **Several widely-repeated "lore" figures were adversarially refuted — see the "Do NOT use" box.**

## Order-of-Entry Advantage (and its decay)

Pioneer advantage is large but decays steeply with each entrant (fractional-probit panel, Porath 2018).

| Entry position | Ceteris-paribus share advantage vs later entrants |
|---|---|
| 1st (pioneer) | ~33 points |
| 2nd | 19 points |
| 3rd | 13 points |
| 4th–6th+ | stabilizes at ~6 points |

Time-limited: a **superior** second entrant must launch within **~2 years** of the first-in-class drug to overtake it (Schulze & Ringel 2013, NRDD — treat as directional; this specific window drew a split verification vote).

## Small-Molecule Generic Erosion — Steep and Fast

IQVIA/IMS Institute ("Price Declines after Branded Medicines Lose Exclusivity in the U.S.," 2016; 428 products, first generic entry 2002–2014). These are *generic price declines relative to brand*, i.e. how cheap the generic gets.

| Segment | Year 1 | Year 2 | 5-year |
|---|---|---|---|
| All medicines | −51% | −57% | — |
| Oral medicines | −66% | −74% | −80% |

Erosion has **accelerated**: oral generics entering 2011–2013 fell 79% within 12 months and 90% within 30 months, vs only 44% within 12 months for 2002–2004 entrants — nearly all price reduction now realized within the first ~8 months.

**Competitor-count gradient (FDA, "Generic Competition and Drug Prices," 2019; entry 2015–2017):**

| # generic competitors | Price below brand (AMP) | (invoice) |
|---|---|---|
| 1 | −39% | −31% |
| 2 | −54% | −44% |
| 4 | ~−79% | ~−73% |
| 6+ | >−95% | >−95% |

## Biosimilar Erosion — Slower Volume, Fast Net Price

Biologic brands lose *volume* far more slowly than small molecules, but *net price* can fall fast via defensive rebates even without share loss.

| Metric | Value | Source |
|---|---|---|
| Humira biosimilar Rx share, Y1 (2023) | 0.03% (Q1) → **1.35%** (Q4) | PMC11645644 (IQVIA NPA) |
| Humira biosimilar Rx share by Nov 2024 (~2 yr) | ~23% | AJMC/Samsung Bioepis (IQVIA) |
| Small-molecule generic Y1 volume capture (contrast) | ~80–90% | IQVIA |
| Humira **net price/Rx** change, 2023 | **−43%** ($5,007 → $2,837) | PMC11645644 |
| Humira US net sales, Q4 2023 | **−45%** ($5B → $2.8B) despite <2% biosimilar share | PMC11645644 + AbbVie Q4'23 |
| Humira reference net price, 3-yr (2023–2025) | **>−70%**, 20+ biosimilar competitors | Drug Channels (SSR Health) |
| Biosimilar ASP discount, Q1 2025 | trastuzumab −52%, bevacizumab −49%, rituximab −66% | AJMC |

> **Key insight for erosion modeling:** Humira's net price fell faster than its *volume* — Q4 net price was actually *below* the biosimilars'. Net erosion is driven by **rebate defense of formulary position**, not biosimilar price competition or share capture. Model the two curves separately.

## Net-vs-List Price Erosion (pre-LOE)

Net price erodes broadly via rebates *before* any exclusivity loss.

- Average manufacturer discount from list ≈ **50.0%** (2024, Drug Channels 9-company analysis) — net ≈ half of list.
- US **gross-to-net bubble**: **$356B** (2024, +7%, slowest growth in a decade), up from $334B (2023).
- Illustrative: a brand launched at $100 list/net in 2013 carries a 2024 list of $211 but net of only $102 — a −51% gross-to-net gap.

## Named Peak-Sales Analogs

| Drug | Peak / latest annual revenue | Notes | Source |
|---|---|---|---|
| **Keytruda** (pembrolizumab) | **$25.01B (2023)**, up from $20.94B (2022) | World's #1 drug; 2023 was **not** yet peak (US LOE ~2028) | GEN Top-10 |
| **Humira** (adalimumab) | **~$200B cumulative** since 2002 (through 2022; ~$237–238B through 2024) | Best-seller in pharma history pre-biosimilar; US net −45% in first biosimilar year | BioPharma Dive |

## Do NOT Use — Refuted Lore

Adversarial verification killed these; do not enshrine them:

| Refuted claim | Vote |
|---|---|
| "First three-in-class capture >90% of market value" | 0-3 |
| "Best-in-class 2nd entrant captures ~88% of first-in-class value (12% first-mover premium)" | 1-2 |
| "Humira reached a peak of $20.7B in 2021" (peak-year figure) | 0-3 |
| "~$400B of branded sales lose exclusivity 2025–2030" | 0-3 |

## Source Vintage & Staleness

| Source | Anchors | Vintage | Staleness |
|---|---|---|---|
| Porath 2018 (fractional probit) | Order-of-entry share decay | modeled coefficients | Directional, single study |
| IQVIA 2016 | Generic erosion curves | 2002–2014 data | Canonical but ~10 yr old |
| FDA 2019 | Competitor-count gradient | 2015–2017 | Structurally durable |
| PMC11645644 / AJMC / Drug Channels | Biosimilar + net-price erosion | 2023–2025 | **Fast-moving — refresh <12 mo** |
| GEN / BioPharma Dive | Peak-sales analogs | 2023–2024 | Update annually |

**Usage note.** Feeds `market-dynamics/SKILL.md` (launch sequencing, class saturation, erosion). Pair the order-of-entry decay with the erosion curves: a fast-follower's disadvantage (Porath) and the post-LOE cliff (IQVIA/FDA) are the two ends of a molecule's competitive life. Always separate *volume* erosion from *net-price* erosion for biologics — they diverge sharply.
