# Signal Scanner — Quick Reference

## Input

| Parameter | Source | Required? |
|---|---|---|
| Target or modality (gene/pathway/mechanism string) | User | Yes |
| Synonym / MeSH term set | User or skill-generated | Recommended |
| Lookback window (default 8 yr, rolling 12-mo or quarterly) | User | Optional |
| Peer set for acceleration-percentile ranking | User or skill-generated | Optional |
| Signal layers to run (default: all) | User | Optional |

## Signal Taxonomy — Ordered by Lead Time

| Layer | Signal | Source / tool | Lead to first-in-human | Velocity (noise) | Role |
|---|---|---|---|---|---|
| Deep | NIH/funder new-grant velocity | NIH RePORTER API | ~5-7 yr | Low / low; lagging-to-novelty | Institutional confirmation |
| Deep | Publication count + **acceleration** | PubMed E-utilities (`total_count`) | ~4-7 yr | Med / med | **Primary lead** |
| Middle | Preprint surge + conversion | bioRxiv/medRxiv API | ~3-6 yr | High / higher | Earliest formal-lit signal |
| Middle | Citation acceleration / landmark burst | OpenAlex, Dimensions, Semantic Scholar | ~3-5 yr | Med | High-quality single event |
| Middle | Patent velocity (PCT/WO) | Lens.org, PatentsView, Espacenet | ~2-4 yr (−18mo visibility) | Med, lagged | Mid-stage confirmation |
| Deep | Grants (above) | — | — | — | — |
| Translation | First IND / Phase 1 | **ClinicalTrials.gov v2 API** | 0 (the event) | Ground truth | Closes lead-time measure |

> Sibling skill `mindshare-tracker` owns the shallow layers (conference share-of-voice ~1-3 yr; Altmetric/social ~0-2 yr) and the reflexivity scoring. Signal-scanner stops at data-generation velocity + de-noising.

## Velocity / Acceleration Primitives

```
For each rolling window t over ~8 years:
  N(t)            = PubMed total_count, [query set], REVIEWS/Editorial/Comment STRIPPED
  velocity(t)     = ΔN / Δt                         (papers per year)
  acceleration(t) = Δvelocity / Δt                  (2nd derivative — THE lead signal)
  RGI(t)          = field CAGR / all-PubMed CAGR    (baseline ~4%/yr)

INFLECTION when:  RGI > ~3 for 3 consecutive years
              AND acceleration positive & rising
              AND primary-research fraction rising
```

Acceleration leads aggregate counts by **1-3 yr**; literature inflection leads first-in-human by **~4-7 yr** for a novel target.

## De-Noising Filters (apply BEFORE trusting any number)

| Filter | Rule | Why |
|---|---|---|
| **Review-strip** | Exclude `Review[Publication Type]`, Editorial, Comment; track primary-research fraction | Reviews are a *trailing* maturity marker; review-inflation is the #1 false positive |
| **Herfindahl breadth** | HHI = Σ(institution share)²; top decile → CAP literature/preprint/citation sub-scores | >50% of preclinical findings irreproducible (~$28B/yr); single-lab studies fail to predict effect size |
| **Polarity** | Read whether a burst/citation is supportive vs refuting/retraction/controversy | Refutation bursts are negative signals masquerading as momentum |
| **Baseline normalization** | Report RGI, not raw growth | All of biomedicine grows ~4%/yr — otherwise every field "grows" |

## Source-Specific Cheats

| Source | Key call | Gotcha |
|---|---|---|
| PubMed E-utilities (`search_articles`) | `total_count` per query+window (PROTAC 2024 = 658) | Capture `query_translation`; watch MeSH/rename drift |
| bioRxiv/medRxiv API | `search_preprints`, `search_published_preprints` for conversion | Unreviewed → breadth filter essential; preprints lead journals 6-18 mo |
| OpenAlex / Semantic Scholar | Kleinberg burst detection; field-normalized | Direct citation > co-citation for young clusters; discount self-citation rings |
| Lens.org / PatentsView (PCT/WO) | Priority-date filing velocity | **Back-date to priority** — publication date lags 18 mo; visible 18-36 mo pre-product |
| NIH RePORTER API | New-award velocity (exclude renewals) | Conservative study sections → lags novelty; check for RFA artifact |
| ClinicalTrials.gov v2 | `search_trials`, `search_by_sponsor` → first IND date | The gap (lit-inflection → FIH) IS the asymmetry window |

## Interpretation Bands (asymmetry read)

| State | Meaning |
|---|---|
| Strong acceleration + broad HHI + **no clinical entries** | Maximal asymmetry — you are early, pre-consensus |
| Strong acceleration + first INDs filed | Genuine emerging momentum; window closing |
| Strong acceleration + multiple Phase 2 readouts | At consensus — literature edge gone |
| High volume + high HHI / review-inflated / low conversion | Likely artifact or single-lab hype — discount |

## Worked Loop

```
1. Build query set (target/modality + synonyms + MeSH)
2. PubMed total_count × 8yr rolling windows → velocity, acceleration, RGI (reviews stripped)
3. bioRxiv/medRxiv velocity + conversion rate + time-to-first-citation
4. OpenAlex Kleinberg burst → landmark papers, polarity
5. Author-affiliation Herfindahl → cap lit sub-scores if top-decile
6. Lens.org PCT/WO velocity, priority-date adjusted
7. NIH RePORTER new-grant velocity (RFA check)
8. ClinicalTrials.gov v2 first-IND date → realized lead time
9. Emit velocity + acceleration + breadth per entity; report band + flags
```

## Anchors (from source brief, spot-verify before load-bearing use)

- PROTAC / targeted protein degradation: 658 PubMed papers in 2024 (live-verified `total_count`).
- Preprints lead journals 6-18 mo; preprinted papers get first citation ~1 mo earlier, ~0.5x more citations.
- Patent visibility lag: structural 18 mo (priority → publication); public 18-36 mo pre-product.
- Irreproducibility: >50% of preclinical findings, ~$28B/yr US; multi-lab (2-4 labs) designs raise coverage probability up to 42 points.
- NIH RePORTER lead ~5-7 yr but most lagging to genuinely novel biology.
- Realized novel-target lead time (lit-inflection → first-in-human): typically 3-7 yr.
- Example targets currently worth scanning: RAS(ON) tri-complex (daraxonrasib), GPR75/INHBE/ALK7 obesity genetics, amylin, TL1A, TREM2 (VG-3927), molecular-glue immune degraders (VAV1/MRT-6160), WRN & MTA-cooperative PRMT5 synthetic lethality, in vivo CAR/CRISPR.
