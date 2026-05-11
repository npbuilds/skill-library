# Domain Taxonomy — The Collector

## Question Classification

Every incoming question is classified along three dimensions before routing.

### Dimension 1 — Axis

| Signal in question | Axis |
|---|---|
| Specific asset class named (comic, card, painting, watch, bottle, coin, book, etc.) | Vertical-anchored |
| Discipline named without asset class (insurance, tax, storage, authentication, grading) | Horizontal-anchored |
| Question would change meaning if either axis were missing | Dual-axis (load both primary skills) |

### Dimension 2 — Lens

| Signal in question | Lens |
|---|---|
| "Is this real?" "Is this great?" "Should I press it?" "What's the eye-test?" "What would a master see?" | Connoisseur |
| "What's the comp?" "What does it cost all-in?" "What's the tax impact?" "What's the illiquidity premium?" "Should I hold or sell?" | Allocator |
| User combines both signals; user is a serious collector who treats collection as portfolio | Dual-lens (both blocks at the end) |

### Dimension 3 — Intent

| Signal | Intent | Routing implication |
|---|---|---|
| "How does X work?" / "Explain Y" | Learn | Calibrate to user level; teaching block is the deliverable |
| "Should I buy / press / consign?" | Decide | Show dual-track analysis with explicit recommendation |
| "Is this authentic / correct / real?" | Authenticate | `horizontal/authentication-provenance/` + asset vertical + `fraud-intelligence/` |
| "What's it worth?" | Value | `horizontal/market-intelligence/` + asset vertical |
| "How do I find / buy / sell?" | Transact | `horizontal/buying-mechanics/` or `horizontal/selling-deaccessioning/` + `horizontal/discovery-sourcing/` |

---

## Full Skill Map

### Orchestrator (1)

- `collector` — The Collector — top-level router

### Horizontal Disciplines (12)

| Skill | Type | Primary domain |
|---|---|---|
| `authentication-provenance` | knowledge + workflow | Chain-of-custody, forensic methods, COA hierarchy |
| `grading-condition` | knowledge | CGC/PSA/BGS/Sheldon, pressing/cleaning ethics |
| `market-intelligence` | knowledge | Liv-ex, PWCC 500, Mei Moses, Knight Frank, BP math |
| `storage-preservation` | knowledge | Temp/RH, Mylar, Oddy test, UV limits, conservation |
| `insurance-risk` | knowledge + workflow | Agreed-value, freeports, scheduled riders, transit |
| `tax-estate-legal` | knowledge + workflow | 28% collectibles cap gains, Form 8283, step-up, CITES |
| `portfolio-allocation` | knowledge | Illiquidity premium, concentration risk, deaccessioning calendar |
| `vetting-services` | knowledge | USPAP, AAA/ASA/ISA, catalog hedge-language, associations |
| `fraud-intelligence` | knowledge | Knoedler, Kurniawan, Mastro/Wagner, PSA reholder, red flags |
| `buying-mechanics` | action | Auction protocol, max bids, increments, allocations |
| `selling-deaccessioning` | action | Channel choice, reserves, irrevocable bids, tax-loss |
| `discovery-sourcing` | action | Estate sales, regionals, eBay/WhatNot, Discord/IG, picker networks |

### Vertical Directors — Tier 1 (7) and their leaf skills

| Director | Leaf skills |
|---|---|
| `comics` | ages-and-keys, grading-pressing, comics-market, manga-tankobon |
| `cards` | sports-cards, pokemon-cards, mtg-collecting, tcg-other |
| `art` | paintings, prints-multiples, contemporary, old-masters, photography |
| `wine-collecting` | en-primeur, cellar-strategy, wine-provenance, wine-as-asset |
| `watches` | vintage-watches, modern-watches, watch-references |
| `coins` | us-coins, world-coins, die-varieties |
| `memorabilia` | autographs, game-used, pop-culture |

### Vertical Standalones — Tier 2 (8)

`books-rare`, `vinyl-records`, `whiskey-collecting`, `luxury-handbags`, `video-games-sealed`, `movie-posters`, `sealed-toys-lego`, `stamps-philately`

---

## Curriculum Progression (for users who want to learn collecting as a discipline, not just answer one question)

**Foundational layer** — anyone serious about collecting needs these regardless of asset class:

1. `horizontal/authentication-provenance` — the meta-skill that makes every other skill load-bearing
2. `horizontal/grading-condition` — the second-order discipline that sits on top of authentication
3. `horizontal/storage-preservation` — the discipline that prevents already-acquired value from being destroyed
4. `horizontal/insurance-risk` — the discipline that catches the tail risk most collectors ignore until it bites
5. `horizontal/market-intelligence` — the discipline that prices everything else

**Asset-class specialization** — choose 1–3 verticals that match the user's actual interest. Going wide too fast erodes depth. The Lauder "three categories — Oh, Oh my, Oh My God" doctrine applies to categories too.

**Allocator layer** — for users who treat their collection as part of their balance sheet:

6. `horizontal/portfolio-allocation`
7. `horizontal/tax-estate-legal`
8. `horizontal/selling-deaccessioning`

**Transactional layer** — once the user is buying actively:

9. `horizontal/buying-mechanics`
10. `horizontal/discovery-sourcing`

**Defensive layer** — once the collection has accumulated meaningful value:

11. `horizontal/fraud-intelligence`
12. `horizontal/vetting-services`

A new collector who absorbs these 12 horizontals will have stronger collecting infrastructure than 90% of people who have spent decades in any single vertical. The infrastructure is the moat.
