---
name: comics
description: >
  Route comics and graphic-novel collecting questions — age categorization (Golden / Silver /
  Bronze / Copper / Modern), CGC and CBCS grading, pressing economics, key issues and first
  appearances, restoration disclosure, market venues (Heritage, ComicConnect, ComicLink), and
  manga / tankōbon as a distinct sub-discipline. Activate when the question concerns a specific
  issue, a grade decision, a pressing-vs-not decision, a key-issue identification, or any
  Western or Japanese comics topic.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Comics — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope

Comics is one of the deepest collecting domains by population, with the cleanest grading infrastructure (CGC), the clearest key-issue economics (first appearances and origins drive 95% of value), and a rich vocabulary of age categorization. This director routes to four leaf skills covering the substantive sub-domains.

## Routing

| User Signal | Leaf Skill | Cross-Axis Skills (load alongside) |
|---|---|---|
| Age categorization, key-issue identification, "is this important?" | `ages-and-keys` | none required by default |
| Grade decision, pressing decision, crackout decision | `grading-pressing` | `horizontal/grading-condition` |
| Venue, pricing, comp analysis | `comics-market` | `horizontal/market-intelligence` |
| Japanese manga, tankōbon, obi, shikishi, Mandarake/Suruga-ya | `manga-tankobon` | `horizontal/authentication-provenance` |

## The Comics Domain at a Glance

### Age Categories

- **Golden Age** (1938–1956): from Action Comics #1 (Superman's first appearance) through the seductive censorship-era Atlas/Marvel comics. The first-appearance keys here dwarf everything later — Action Comics #1 has exceeded $6M at major auction.
- **Silver Age** (1956–1970): the Marvel renaissance. Amazing Fantasy #15 (Spider-Man), Fantastic Four #1, X-Men #1, Iron Man's first appearance in Tales of Suspense #39, the Avengers' first appearance.
- **Bronze Age** (1970–1985): the maturing market. Incredible Hulk #181 (Wolverine's full first appearance), Amazing Spider-Man #129 (the Punisher's first appearance), Giant-Size X-Men #1 (the new X-Men).
- **Copper Age** (1985–1991): often folded into Bronze or Modern. The Sandman by Neil Gaiman starts here; key Image Comics #1s.
- **Modern Age** (1992–present): The Image Comics founding (Image #1 with Wildcats, Spawn, Youngblood); the modern Marvel/DC reboots; the Walking Dead #1.

### Grading

CGC dominates the slabbing market. CBCS is the credible #2. PGX exists as a distant third with a weak reputation.

**The CGC scale** (10.0 = perfect, 0.5 = Poor): the de facto market standard. Sub-grades are not published in the same way BGS publishes them; CGC produces a single holistic grade.

**The CGC label colors:**
- **Blue (Universal)** — no restoration detected; the premium tier
- **Purple (Restored)** — restoration detected; 50–80% value penalty vs. universal at the same grade
- **Light Blue (Conserved)** — conservation work only (cleaning, dry pressing, simple tear seal) without color additions or piece replacement; trades closer to universal
- **Green (Qualified)** — the grade is conditional on a called-out defect (e.g., missing back cover)
- **Yellow (Signature Series)** — signed by the creator in CGC's presence; witnessed authentication

### Key-Issue Economics

The single most important concept in comics: **first appearances** of major characters drive 95% of value. Origin issues, the first issue of an ongoing series, and major character milestones are the trophy. Many comics with beautiful condition are worthless because they have no "key" status. Many "keys" in mediocre condition outperform pristine non-keys.

### Pressing

Heat + humidity + pressure to remove non-color-breaking ticks, spine roll, and minor surface defects. **Legal, common, value-accretive**, and accepted by CGC and CBCS. The economic logic is in the `grading-pressing` leaf — pressing a 9.4 to a likely 9.6 or possible 9.8 on a Bronze Age key can produce returns of 20-50x the pressing cost.

### Restoration vs. Conservation

The hardest line in comics. Restoration adds material (color touch, piece replacement, tear seals with material added) and triggers the purple CGC label. Conservation does not add material (just removes acidity, flattens warps, seals tears with archival mending) and triggers the light blue label. The 2024 Meyers v. CGC defamation case ($10M jury award) showed even CGC can be wrong about which is which.

## Cross-Axis Connections

Almost every comics question requires loading at least one horizontal skill:

- Grade decisions → `horizontal/grading-condition`
- Authentication of signed copies / classic issues → `horizontal/authentication-provenance`
- Comparable analysis → `horizontal/market-intelligence`
- Storage of a collection → `horizontal/storage-preservation`
- Insurance scheduling → `horizontal/insurance-risk`
- Counterfeit / restoration fraud → `horizontal/fraud-intelligence`

## Sub-Domain Boundaries

- Western comics and graphic novels → `ages-and-keys`, `grading-pressing`, `comics-market`
- Japanese manga / tankōbon / shikishi → `manga-tankobon` (different epistemology entirely; the Japanese tankōbon is canonical and English first editions track differently)
- Limited-edition reprints / box sets → fall under `ages-and-keys` for value framework but the audience is more modern-collector
- Comic art (original pages, splash pages) → cross-link to `vertical/art/` for the gallery/auction-house side

---

Connoisseur ─── A Key Issue in Low Grade Beats a Non-Key in High Grade

The collector who pays $400 for a CGC 5.0 Incredible Hulk #181 over a CGC 9.8 Hulk #182 has made the structurally correct trade. The #181 is the first full appearance of Wolverine; the #182 is the second appearance, the issue *after* the trophy. Over thirty years, the #181 in any grade outperforms the #182 in any grade. This is the discipline that separates serious comic collectors from card-grade chasers: the issue identity matters more than the surface.

Allocator ─── Pop and Comp Discipline on Modern Keys

Modern comic keys (post-2000) often trade with deceptively favorable pop reports because they were grade-submitted en masse at release. Walking Dead #1, Saga #1, modern Marvel/DC key first appearances often have CGC 9.8 populations of 5,000–20,000+. The trophy comps (Heritage Signature realizations) tell one story; the daily realized comps on eBay BIN tell another. For modern keys, weight the daily-traded data more heavily than the Heritage Signature comps when valuing.
