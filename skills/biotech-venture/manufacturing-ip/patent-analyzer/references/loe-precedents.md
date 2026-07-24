# Loss-of-Exclusivity Precedents — Extended Reference

Reference tables for the `patent-analyzer` SKILL (`manufacturing-ip/patent-analyzer`): the statutory exclusivity clocks, patent-life math, and the FTO / Paragraph IV / BPCIA frameworks the skill runs, plus externally verified erosion precedents to anchor the "entry impact on revenue" line of a patent-landscape analysis. It codifies what the parent SKILL treats as prose so a diligence run can cite constants rather than re-derive them.

**Provenance legend.** `statutory` = stable legal/regulatory constant (exclusivity terms, PTE cap). `ext✓` = externally verified against a real citation (the erosion precedents below). `int` = internal consensus estimate carried in the parent SKILL's own tables/prose, no external source. Untagged framework text is methodology from the parent SKILL.

## Patent Type Taxonomy (int — from parent SKILL)

| Patent Type | Protection Strength | Vulnerability | Duration |
|---|---|---|---|
| Composition of Matter (CoM) | Strongest — covers the molecule itself | Hardest to design around | Filing + 20 yr + PTE |
| Salt / Polymorph | Strong — covers specific forms | Designable if alternative forms exist | Filing + 20 + PTE |
| Formulation | Moderate — covers delivery method | Generics can reformulate | Filing + 20 + PTE |
| Method of Use | Moderate — covers specific indication | Skinny-label / off-label generic use | Filing + 20 + PTE |
| Dosing Regimen | Weak–Moderate — covers dose/schedule | Hard to enforce; off-label prescribing | Filing + 20 |
| Process / Manufacturing | Weakest for exclusivity | Alternative processes usually possible | Filing + 20 |
| Combination | Variable — covers specific combinations | Protects only the combination | Filing + 20 + PTE |

**Assessment rule (int):** an asset protected only by method-of-use and dosing patents (no CoM) carries materially higher generic-entry risk. A strong estate anchors on CoM with formulation and method-of-use as reinforcement.

## Statutory Exclusivity Clocks (statutory)

| Exclusivity | Term | Trigger / effect | Tag |
|---|---|---|---|
| NCE (New Chemical Entity) | 5 yr | No ANDA filing permitted (4 yr if Para IV) | statutory |
| New Clinical Investigation | 3 yr | ANDAs may file but not be approved | statutory |
| Orphan Drug | 7 yr | No approval of same drug, same indication | statutory |
| Biologic reference-product data exclusivity | 12 yr | No biosimilar approval from first licensure | statutory |
| Biologic filing exclusivity | 4 yr | No 351(k) biosimilar application accepted | statutory |
| Pediatric exclusivity | +6 mo | Added to all existing exclusivities and patents | statutory |
| QIDP (Qualified Infectious Disease Product) | +5 yr | Added to exclusivity | statutory |
| 180-day First-Filer (Para IV) | 180 days | First Para IV filer generic exclusivity | statutory |
| First interchangeable biosimilar | 1 yr | Market exclusivity vs later interchangeables | statutory |

## Patent-Life Math (framework — from parent SKILL)

| Adjustment | Basis | Rule | Cap / tag |
|---|---|---|---|
| Base term | Filing date | Filing + 20 yr | — |
| Patent Term Adjustment (PTA) | 35 USC 154 | + USPTO prosecution delay − applicant delay (net days) | none stated |
| Patent Term Extension (PTE) | 35 USC 156 | 50% of clinical testing time + 100% of regulatory review time | Max 5 yr; total ≤ 14 yr from approval (statutory) |
| PTE eligibility | 35 USC 156 | One patent per product; must be first commercial use | statutory |
| SPC (EU) | EU reg. | (Filing → marketing authorization) − 5 yr | Max 5 yr (+6 mo pediatric) (statutory) |

Effective patent expiry = latest of the US and EU adjusted dates. **30-month stay (statutory):** a Paragraph IV certification triggers an automatic 30-month stay of ANDA approval during litigation — roughly 2.5 yr of protected revenue even if the challenged patent is later invalidated.

## Erosion Precedents (ext✓ — for the revenue-impact line)

These anchor the parent SKILL's "entry impact on revenue: [X]% erosion over [X] years" output. The **full erosion curves live in `competitive-intelligence/market-dynamics/references/launch-and-erosion-benchmarks.md`** — use these as headline precedents, that doc for the modelable curves.

### Small-molecule generic erosion

| Cohort | Yr-1 price | Yr-2 price | Longer horizon | Source (ext✓) |
|---|---|---|---|---|
| All medicines | −51% | −57% | — | IQVIA / IMS Institute 2016 |
| Oral solids | −66% | −74% | −80% by yr 5 | IQVIA / IMS Institute 2016 |
| Accelerated orals (2011–13) | −79% at 12 mo | — | — | IQVIA / IMS Institute 2016 |

FDA competitor-count gradient (net price vs pre-generic AMP):

| # of generic competitors | Price level | Source (ext✓) |
|---|---|---|
| 1 generic | −39% | FDA 2019 |
| 2 generics | −54% | FDA 2019 |
| 6+ generics | > −95% | FDA 2019 |

### Biosimilar erosion — Humira precedent (ext✓)

| Metric | Value | Notes | Source |
|---|---|---|---|
| Net price per Rx (2023) | −43% | Defensive rebating pre/early biosimilar | PMC11645644 |
| US net sales, Q4 2023 | −45% | Despite < 2% biosimilar Rx share (rebate wall) | Drug Channels |
| Reference net price, 3-yr (2023–2025) | > −70% | With 20+ biosimilar competitors | AJMC |
| Biosimilar volume share, Nov 2024 (~2 yr) | ~23% | Far slower than small-molecule ~80–90% yr-1 | Drug Channels / AJMC |

**Read-through (int):** biosimilar erosion is slower and rebate-mediated, not price-list-mediated — a biologic LOE tail should not be modeled on the small-molecule cliff. Interchangeability accelerates it (pharmacy-level substitution); non-interchangeable biosimilars require physician switching and erode more slowly.

Note: named small-molecule cliff case studies (e.g. Lipitor, Plavix) are **int, illustrative — unverified**; no dollar figures are asserted here because this suite has no verified source for them.

## Freedom-to-Operate & Para IV Risk (framework — from parent SKILL)

FTO royalty exposure when encumbered: typically **2–8% of net sales (int)**. FTO outcomes: Clean (no third-party risk) / Encumbered (license or design-around; quantify royalty) / Blocked (license mandatory or development halts).

Paragraph IV risk rises with: no CoM (method-of-use/formulation only); narrow species claims; peak sales > $1B (generic incentive); prior IPR losses; multiple ANDA filers. It falls with: strong validated CoM; broad genus claims; peak sales < $500M; clean IPR record; 0–1 filers.

## Source Vintage & Staleness

| Block | Vintage | Stales because |
|---|---|---|
| Statutory clocks & PTE cap | Stable law | Only on Hatch-Waxman / BPCIA statutory amendment — rare; re-verify on any FDA guidance change |
| Small-molecule erosion (IQVIA 2016; FDA 2019) | 2016 / 2019 | Structural (generic-market dynamics shift slowly); directionally durable, magnitudes drift with rebate/PBM practice |
| Humira biosimilar precedent | 2023–2024 | Fast-moving — share and net-price figures update quarterly; treat as a snapshot, refresh from Drug Channels / AJMC |
| Patent-taxonomy & FTO ranges | int, undated | Consensus heuristics; revisit if the parent SKILL's tables change |

## Usage note

Serves the `patent-analyzer` SKILL (`skills/biotech-venture/manufacturing-ip/patent-analyzer/SKILL.md`) — supplies its statutory constants, patent-life math, and the erosion precedents behind the LOE / revenue-impact output. Cross-reference `competitive-intelligence/market-dynamics/references/launch-and-erosion-benchmarks.md` for the full modelable erosion curves; feeds Pillar 5 (IP Fortress) of the 8-pillar diligence scorecard.
