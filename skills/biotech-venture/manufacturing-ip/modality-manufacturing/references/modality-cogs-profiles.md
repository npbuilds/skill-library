# Modality COGS Profiles — Extended Reference

Authoritative, single-source COGS/margin/capex profiles by modality for `modality-manufacturing` and `cmc-risk-assessor` (both should delegate here rather than duplicating COGS blocks).

> **Confidence warning — read first.** Primary, citable manufacturing-COGS data is **scarce and largely proprietary**. A dedicated deep-research pass surfaced only *two* externally-verifiable anchors (below) and **refuted two** commonly-repeated figures. Most per-modality numbers in this suite are **internal consensus estimates**, not sourced statistics. Each row is tagged by provenance — respect the tags, and never present an `int` figure as a benchmark distribution in a live memo without a primary source.

**Provenance tags:** `int` = internal consensus estimate (from `modality-manufacturing` skill, unsourced) · `ext✓` = externally verified (primary/peer-reviewed) · `ext~` = external but directional (secondary/blog, not independently verified).

## Cross-Modality COGS Comparison

| Modality | COGS / dose | Gross margin | Facility capex | Process-dev | Provenance |
|---|---|---|---|---|---|
| Small molecule | $0.10–$5.00 | 85–95% | $50–150M | 12–18 mo | int |
| Monoclonal antibody (mAb) | $20–$200 | 75–90% | $200–500M | 18–24 mo | int; mAb drug-substance $50–200/g commercial (`ext~`) |
| Bispecific antibody | $50–$500 | 70–85% | $200–500M | 24–30 mo | int |
| Antibody-drug conjugate (ADC) | $500–$3,000 | 65–80% | $300–600M | 24–36 mo | int; drug-substance modeled $499–778/g, ~10× mAb (`ext~`) |
| Oligonucleotide (ASO/siRNA) | $100–$2,000 | 70–85% | $100–250M | 18–30 mo | int |
| mRNA / LNP | $2–$20 (vax) / $50–500 (therapeutic) | 80–90% (vax scale) | $100–300M | 12–24 mo | int |
| **Autologous cell therapy (CAR-T)** | **~$80,000–150,000+/dose commercial** | — | $200–500M | 30–42 mo | `ext~` ($95,780/dose, 2019); academic in-house model **€57–63K** (`ext✓`) |
| Allogeneic cell therapy | $5,000–$30,000 | 70–85% | $200–500M | 30–42 mo | int ($4,460/dose 2019 basis, `ext~`) |
| Gene therapy (AAV) | $50,000–$500,000 | 40–70% | $300–800M | 30–48 mo | int |

> The **autologous CAR-T** row fills a gap the audit flagged (it was absent from the quick-reference). Note the wide, provenance-split range: an academic in-house *model* puts it at €57–63K, but commercial COGS is generally cited at ~$80–150K+/dose — **never quote the academic model as a generic commercial benchmark.**

## Externally-Verified Anchors

| Anchor | Value | Source (vintage) | Confidence |
|---|---|---|---|
| CMC (process dev + manufacturing) share of mAb R&D | **13–17%** of budget preclinical→approval (17% at 22% success rate) | Farid et al., *mAbs* 2020 (PMC7531566) | High — but a *modeled* prediction, mAb-specific |
| Autologous CAR-T cost (academic in-house model) | €63K manual / €61K semi-auto / €57K fully auto | Frontiers Bioeng. Biotechnol. 2025 | Medium — perspective/model, below commercial COGS |
| mAb drug-substance cost trajectory | fell from ~$1,000s/g historically to $10s–$100s/g; price ~$2,000+/g | BioProcess Intl / PubMed (secondary) | Directional only |
| ADC drug-substance | ~$777.50/g (dedicated) / $499.70/g (integrated); ~10× mAb | biopharmservices (blog) | Directional only |

## Do NOT Use — Refuted During Research

| Refuted claim | Vote |
|---|---|
| "mAb titers benchmark at 2.5 g/L early rising to ~5 g/L by Phase III" | 1-2 (the quick-reference's "3–8 g/L typical" is the internal estimate; treat titer numbers as unsourced) |
| "CAR-T parallelization of 12 products cuts cost to ~€42–52K (20–31% reduction)" | 0-3 |

## Source Vintage & Staleness

COGS trajectories improve over time (titers rise, processes mature), so **internal estimates drift toward lower COGS** — the directional pattern (small molecule ≪ mAb ≪ ADC ≪ cell/gene therapy) is durable, the absolute dollars are not. **This doc is deliberately thin on the COGS dimension pending a targeted primary-source pass** (BioProcess International benchmarking surveys, company 10-K COGS lines, CDMO capacity data would upgrade it).

**Usage note.** `cmc-risk-assessor` should pull its COGS block from this table (kills the current duplication) and layer its FMEA/occurrence base-rates on top. When COGS drives an rNPV gross-margin assumption, state the provenance tag — an `int`/`ext~` figure carries far more uncertainty than the sourced anchors, and gene-therapy/cell-therapy margins in particular are under active pricing pressure.
