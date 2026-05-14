---
name: wine-collecting
description: >
  Route wine-collecting questions — en primeur futures, cellar strategy and storage, provenance
  and ullage assessment, and wine as an asset class (Liv-ex indices, blue-chip producers,
  illiquidity premium). This is the **collector** view of wine; the **tasting and sensory**
  view of wine lives in Bacchus. Both suites stay self-contained — this director mirrors
  Bacchus's wine-market structure rather than cross-linking, by the user's design choice.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Wine Collecting — Director

> **Type:** Director
> **Suite:** The Collector
> **Axis:** Vertical
> **Parent:** collector

## Scope and Relationship to Bacchus

Wine collecting is the asset-class view of wine — building, holding, and deaccessioning a wine cellar with intention. The skills here cover futures markets, storage strategy, provenance assessment, and wine as an investment.

**This director is parallel to Bacchus's wine-market director.** The user has chosen to mirror rather than cross-link — both suites remain self-contained. Some intentional content redundancy exists (the Liv-ex indices, the First Growth producers, the en primeur mechanism) because the two suites serve different routing contexts:

- **Bacchus** handles wine as **sensory experience** — tasting, blind evaluation, food pairing, terroir, winemaking, service, and the **sommelier-grade investment** view (collecting-investment leaf). Activate Bacchus when the question is about drinking, identifying, pairing, or understanding a specific wine.
- **The Collector / wine-collecting** handles wine as an **asset class** — building a cellar as part of a portfolio, comparing wine to other alternative assets, asset-class allocation, and the financial-frame view of wine. Activate The Collector when the question treats wine as a balance-sheet line.

For users who want **both views** (which is most serious wine collectors), both suites can be loaded; the directors are compatible.

## Routing

| User Signal | Leaf Skill | Cross-Axis Skills |
|---|---|---|
| Bordeaux en primeur, futures purchase, La Place de Bordeaux | `en-primeur` | `horizontal/market-intelligence` |
| Cellar building, bonded storage, OWC vs loose, drinking windows | `cellar-strategy` | `horizontal/storage-preservation`, `horizontal/insurance-risk` |
| Ullage, capsule integrity, ex-château vs European-collection, provenance chain | `wine-provenance` | `horizontal/authentication-provenance`, `horizontal/fraud-intelligence` (Kurniawan) |
| Liv-ex indices, blue-chip producers, illiquidity premium, asset allocation | `wine-as-asset` | `horizontal/portfolio-allocation`, `horizontal/market-intelligence` |

## What's Distinctive About Wine

### Wine Is the Only Major Collectible That Improves and Then Declines

Most collectibles have a value curve driven by scarcity and demand over time. Wine has an additional dimension: the wine itself changes. A 1982 Lafite drunk in 1985 is unrecognizable from the same bottle drunk in 2010 or 2024. The wine has a peak window — too young, perfect, too old. This creates a "drink it or die" pressure that makes wine collecting structurally different from comics or watches.

The implication: **storage and timing matter more in wine than in any other collectible**. A poorly stored wine is functionally a different asset than the same wine in pristine cellar conditions.

### Provenance Is a Sensory and Chemical Question

For wine, provenance is not abstract documentation — it is the **physical history of the bottle's storage conditions**. Was it always at 50-59°F? Was it humid enough that the cork stayed wet? Was it light-protected? Was it horizontal? Did it ever cross a hot warehouse?

The market formalizes this through:

- **Ullage** (fill level) — into-neck (best), top-shoulder, upper-shoulder, mid-shoulder (significant deduction), low-shoulder (avoid)
- **Capsule integrity** — intact and not raised; raised capsules signal heat exposure
- **Label condition** — pristine vs water-stained vs torn
- **Cellar source** — ex-château (best), ex-cellar of named collector, "private European collection" (often a warning flag)

### The Kurniawan Legacy

The 2014 Rudy Kurniawan conviction (10 years for counterfeiting rare Burgundies) has not removed his fakes from the market. Bottles from his network continue to surface — and many of them are extremely convincing. Burgundy provenance from the 2000-2012 era requires elevated scrutiny.

## Cross-Axis Connections

- **Authentication and counterfeit risk** → `horizontal/authentication-provenance` + `horizontal/fraud-intelligence`
- **Storage and conservation** → `horizontal/storage-preservation` (climate, humidity, light)
- **Insurance and bonded storage** → `horizontal/insurance-risk` (wine-specific policies, bond houses)
- **Tax** → `horizontal/tax-estate-legal` (28% collectibles cap gains; bonded storage VAT deferral; CITES not applicable but state-by-state wine shipping regs matter)
- **Pricing** → `horizontal/market-intelligence` (Liv-ex indices)
- **Portfolio allocation** → `horizontal/portfolio-allocation`
- **Selling** → `horizontal/selling-deaccessioning` (Sotheby's Wine, Acker, Hart Davis, Zachys)
- **For sensory / tasting / blind / pairing / regional / winemaking** → `bacchus` (cross-suite)

## Major Producers — Quick Reference

(Detailed coverage in leaf skills; this is the director-level orientation.)

### Bordeaux

- **First Growths** (Premiers Crus, 1855 classification): Lafite Rothschild, Latour, Margaux, Haut-Brion, Mouton Rothschild (elevated 1973)
- **Right Bank trophies**: Pétrus, Cheval Blanc, Ausone
- **Super-Seconds**: Pichon Lalande, Léoville Las Cases, Cos d'Estournel, Pichon Baron, Ducru-Beaucaillou

### Burgundy

- **Domaine de la Romanée-Conti (DRC)** — the trophy producer; smallest production volumes among trophy estates
- **Domaine Leroy** — Lalou Bize-Leroy's domaine
- **Domaine Armand Rousseau** — Gevrey-Chambertin
- **Domaine Coche-Dury** — Meursault white Burgundy
- **Domaine Leflaive** — Puligny-Montrachet
- **Domaine Comte de Vogüé** — Chambolle-Musigny

### Champagne

- **Krug** — Grande Cuvée and Clos d'Ambonnay
- **Salon** — Le Mesnil; vintage-only
- **Dom Pérignon** — Plenitude P2, P3 late-disgorgement
- **Bollinger** — Vieilles Vignes Françaises; R.D.
- **Cristal** (Roederer); **Comtes de Champagne** (Taittinger)

### Italy

- **Sassicaia, Masseto, Ornellaia, Tignanello, Solaia, Gaja Barbaresco/Barolo, Conterno Monfortino**

### Napa

- **Screaming Eagle, Harlan Estate, Bryant Family, Colgin Cellars, Dominus, Opus One**

### Spain, Portugal, Australia

- **Vega Sicilia Único, Pingus, Quinta do Noval Nacional, Penfolds Grange**

## Liquidity and Indices

- **Liv-ex 100** — most-traded fine wines
- **Liv-ex 1000** — broader benchmark
- **Bordeaux 500, Burgundy 150, Champagne 50, Italy 100, Rest of World 60** — regional indices

Liv-ex is a members-only dealer exchange (UK-based); published indices are public. The 2018-2021 Burgundy run that drove Liv-ex Burgundy 150 returns over 100% in three years has since seen correction; the asset class is genuinely volatile.

---

Connoisseur ─── Wine Collecting Is a Multi-Decade Conversation Between Bottle and Cellar

Building a great cellar is not buying expensive wine. It is a multi-decade conversation between the bottles you acquire, the cellar you maintain, the dinners you host, and the wines you choose to age. The collector who acquires Bordeaux 1982 at release in 1983 and drinks it at peak in 2008 has participated in a 25-year conversation with that vintage. The collector who buys 1982 Bordeaux at peak in 2024 has bought an aged wine — beautiful, expensive, but not the same conversation.

Allocator ─── Wine's Illiquidity Premium Has Specific Friction Items

A wine cellar's friction list is unique: bonded storage at $30-60 per case per year; insurance at 0.20-0.40% of value annually; sale at Sotheby's Wine with seller's commission of 10-15% plus buyer's premium of ~22% absorbed by demand; transit insurance for delivery to bonded storage. The all-in friction on a 20-year hold can be 25-35% of gross gain. Liv-ex 1000 has returned roughly 6-8% nominal over the past decade — pre-friction. After-friction realized return is closer to 3-5%, comparable to inflation-adjusted bonds. Allocate to wine for the consumption value, the diversification, and the cultural experience — not for superior realized financial returns.
