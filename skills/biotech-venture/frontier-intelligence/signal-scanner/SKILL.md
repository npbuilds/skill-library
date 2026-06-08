---
name: signal-scanner
description: >
  Measure scientific momentum for an emerging target or modality by computing the second
  derivative (acceleration) of PubMed and bioRxiv/medRxiv volume, citation-burst detection
  on landmark papers, and author-affiliation concentration to subtract single-lab artifacts,
  cross-checked against patent velocity, NIH grant flows, and the first-IND translation event.
  Activate when asking whether a target/modality is inflecting before consensus, how early you
  are, or when separating a genuine emerging field from review-driven or single-lab hype.
metadata:
  author: nirav
  version: "1.0"
  parent: frontier-intelligence
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Signal Scanner — Reading the Second Derivative of Scientific Mindshare

By the time a target or modality is consensus — covered in *Nature Reviews*, multiple Phase 2 readouts, generalist-press coverage — the asymmetric return is gone. Edge comes from reading the leading indicators, and within each indicator, from reading the **acceleration** rather than the level. A field with 200 papers/year growing 60% YoY is a far stronger signal than a field with 2,000 papers/year growing 5% YoY. The second derivative of publication and preprint volume leads aggregate counts by 1-3 years and leads first-in-human by roughly 4-7 years for a novel target — it is the single most actionable literature signal.

This skill is the velocity primitive of the frontier-intelligence suite. It takes a target/modality query and emits, per entity, a velocity + acceleration + breadth profile across a layered set of sources ordered by lead time: deepest and slowest (NIH grants, primary literature), through the middle (preprints, citation bursts, patents), to the translation-event ground truth (first IND). It does *not* score attention or hype — that is `mindshare-tracker`'s job. It quantifies data-generation velocity and de-noises it.

The discipline that separates signal from noise is three filters applied *before* any number is trusted: strip review/perspective publication types (reviews are a trailing maturity marker, not a leading one); compute an author-affiliation Herfindahl concentration index to subtract single-lab artifacts (over 50% of preclinical findings are irreproducible, ~$28B/yr in the US, and single-lab standardized studies systematically fail to predict effect size); and normalize against all-PubMed baseline growth (~4%/yr) so that not every field looks like it is growing.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Target or modality (gene/pathway/mechanism string) | User | Yes |
| Synonym / MeSH term set | User or skill-generated | Recommended |
| Lookback window (default 8 years of rolling 12-month or quarterly windows) | User | Optional |
| Peer set for acceleration-percentile ranking | User or skill-generated | Optional |
| Signal layers to run (default: all) | User | Optional |

### Steps

#### Step 1 — Build the Query Set

Define the entity precisely before counting anything. A sloppy query set is the dominant source of false velocity.

- Assemble the target/modality string plus synonyms and MeSH terms (e.g., for degraders: `PROTAC OR "targeted protein degradation" OR "molecular glue" OR "degrader"`).
- Watch for renaming/MeSH drift — the same biology rebranded inflates apparent novelty. When using the PubMed tool, capture the expanded `query_translation` so the MeSH mapping is auditable.
- For narrow/novel targets (rare-disease, single-gene) note that absolute denominators are small, so acceleration will be noisy and a single lab or grant can dominate — flag for higher breadth-filter sensitivity downstream.

#### Step 2 — Publication Velocity and Acceleration (PubMed)

Primary literature is the workhorse signal. Source: **PubMed E-utilities** (the connected `search_articles` MCP tool returns an exact `total_count` per query + date window — the atomic operation of the whole method; e.g., a 2024-restricted PROTAC query returns 658).

```
LITERATURE VELOCITY — PubMed

For each rolling 12-month (or quarterly) window over the last ~8 years:
  N(t) = total_count for [query set] in window t
         WITH "Review"[Publication Type], Editorial, Comment EXCLUDED

  velocity(t)      = ΔN / Δt                 (papers per year)
  acceleration(t)  = Δvelocity / Δt          (the LEAD signal — 2nd derivative)
  RGI(t)           = field CAGR / all-PubMed CAGR   (~4%/yr baseline)

Flag inflection when: RGI > ~3 for 3 consecutive years
                      AND acceleration is positive and rising
                      AND primary-research fraction is rising (not review-driven)
```

Track the **primary-research fraction** separately: a healthy emerging field shows rising *original-article* velocity; a hype field shows reviews outrunning primary data.

#### Step 3 — Preprint Surge (bioRxiv / medRxiv)

The earliest *formal-literature* signal — preprints lead peer-reviewed publication by 6-18 months. Source: **bioRxiv/medRxiv API** (`search_preprints`, `search_published_preprints`, `funder_search`, `get_statistics`).

- Run the same rolling-window velocity/acceleration on preprint counts.
- Compute the **preprint-to-publication conversion rate** (`search_published_preprints`): fraction reaching a journal within 12-18 months. Rising conversion = the field is maturing and being validated; falling conversion alongside rising preprint volume = low-quality flooding (a warning).
- Track **preprint citation velocity** — preprinted papers receive their first citation ~1 month earlier and ~0.5x more citations on average; time-to-first-citation is a within-field momentum sub-metric.
- Preprints are unreviewed: the breadth filter (Step 6) is *essential* here. Verify subject category with `get_categories`.

#### Step 4 — Citation Burst Detection on Landmark Papers

A single landmark mechanism paper (Nature/Cell/Science) that triggers a citation burst is a higher-quality signal than diffuse incremental growth. Source: **OpenAlex** (free citation graph), Dimensions, Semantic Scholar; Web of Science/Scopus where licensed.

- Run **Kleinberg burst detection** (the CiteSpace-style algorithm) over the field's citation graph: a burst is a sudden, statistically significant jump in citation rate for a paper or cluster. Direct citation detects young, fast-growing clusters earlier than co-citation or bibliographic coupling.
- Identify **landmark papers** — the small core that the citing literature co-cites (the formal definition of a "research front").
- Use **field-normalized** citation acceleration (control for baseline field citation rates), not raw counts.
- Read **polarity**: discount citation-farming/self-citation rings; a paper cited because it is being *refuted* is a negative signal masquerading as positive.

#### Step 5 — Patent Velocity (PCT/WO) — Mid-Stage Confirmation

Forward-looking but with a structural 18-month visibility penalty, so this is a **mid-stage confirmation** signal, not an earliest-mover one. Source: **Lens.org** (free, strong biotech coverage), **PatentsView** (USPTO), Espacenet (EPO), Google Patents, WIPO PATENTSCOPE for PCT/WO.

- Count PCT (WO) applications and priority filings per quarter mentioning the target/modality (composition-of-matter and method-of-use claims).
- **Critical caveat:** applications publish ~18 months after the priority filing date. Velocity on *publication date* lags reality by 18 months; the true leading metric is velocity on *priority date* (visible only retrospectively). **Always back-date to priority.** Patents become public 18-36 months before any product — they front-run commercialization but trail the earliest literature.
- Discount defensive/blocking filings with no development intent, and a single incumbent's broad portfolio spray (breadth filter again — many independent filers > one big-pharma sprayer).

#### Step 6 — Author/Institution Breadth (Herfindahl De-Noising Filter)

The most important de-noiser. N papers from 2 labs ≠ N papers from 40 independent groups.

```
BREADTH FILTER — author-affiliation Herfindahl

For the primary-research + preprint corpus of the field:
  s_i = share of papers from institution/group i
  HHI = Σ (s_i)^2          (0 → maximally broad; 1 → single lab)

If HHI is in the top decile (single-lab dominated):
  → CAP the literature-derived sub-scores (Steps 2, 3, 4) regardless of raw acceleration
  → genuine emergence is broad-based; concentration = discount the signal
```

ORCID coverage is incomplete in older literature, so affiliation disambiguation is imperfect — when breadth is uncertain, treat it as a flag, not a hard gate.

#### Step 7 — NIH / Funder Grant Velocity — Deepest, Most-Lagging

The deepest leading indicator (~5-7 years to clinic) but the lowest velocity and most lagging to *genuinely novel* biology, because study sections are conservative and fund incrementally. Source: **NIH RePORTER API** (project counts, $ awarded, by RCDC category and free-text); plus CZI, Wellcome, ERC, ARPA-H portfolios.

- Compute **new-grant velocity** (new awards/year, excluding renewals — renewals lag) and total $ committed per year in the theme.
- Read this as *confirmation that academic mindshare has institutionalized*, not as a frontier signal.
- Check whether a spike is RFA/program-announcement-driven (an artifact) versus organic.

#### Step 8 — Translation-Event Cross-Check (ClinicalTrials.gov v2)

The ground truth that closes the lead-time measurement. Source: **ClinicalTrials.gov v2 API** (`search_trials`, `search_by_sponsor`).

- Pull the **first IND / Phase 1 entry** date for the target/modality. This is the moment mindshare converts to clinical reality.
- The **gap between literature-velocity inflection and first-in-human** is the realized lead time the whole framework exists to capture (typically 3-7 years for a novel target).
- Interpretation: a strong acceleration signal with *no* clinical entries = maximal asymmetry (you are early); a strong signal with multiple Phase 2 readouts = you are at consensus (the literature edge is gone).

### Output

```
SIGNAL SCAN — [Target / Modality]
Query set: [string + synonyms + MeSH]    |    Window: [years]    |    Date: [scan date]

LITERATURE (PubMed, reviews stripped)
  Latest annual count (primary):  [N]
  Velocity (papers/yr):           [v]
  Acceleration (2nd derivative):  [a]   ← LEAD SIGNAL
  Relative Growth Index (RGI):    [x]   (>3 for 3yr = inflection)
  Primary-research fraction:      [%]   (rising / falling)

PREPRINTS (bioRxiv/medRxiv)
  Velocity / acceleration:        [v] / [a]
  Preprint→publication conversion:[%]   (rising = validating; falling = flooding)
  Time-to-first-citation:         [months]

CITATION BURST
  Landmark paper(s):              [citation + burst window]
  Field-normalized acceleration:  [x]
  Polarity check:                 [supportive / refutational / mixed]

PATENTS (PCT/WO, priority-date adjusted)
  Priority-date filing velocity:  [v]   (mid-stage confirmation; −18mo visibility)
  Filer breadth:                  [many independent / single incumbent]

GRANTS (NIH RePORTER)
  New-grant velocity:             [awards/yr]   (deepest, ~5-7yr lead, lagging-to-novelty)
  RFA-driven?                     [yes/no]

DE-NOISING
  Author-affiliation HHI:         [0-1]   (top decile → literature sub-scores CAPPED)

TRANSLATION GROUND TRUTH (ClinicalTrials.gov v2)
  First IND / Phase 1 date:       [date or NONE]
  Realized lead time (lit-inflection → FIH): [years]

READ
  Inflection?                     [Yes / Ambiguous / No]
  How early are you?              [pre-clinical-entry / first INDs filed / at consensus]
  Confidence flags:               [single-lab artifact / review-inflated / RFA artifact / narrow-denominator noise]
```

## Error Handling

| Scenario | Response |
|---|---|
| PubMed count surging but driven by reviews | Re-run with `Review[Publication Type]`/Editorial/Comment excluded; report primary-research fraction; downgrade the signal |
| High volume but author-affiliation HHI in top decile | Single-lab artifact — cap literature/preprint/citation sub-scores; require multi-lab breadth before trusting |
| Citation burst from a refuted/retracted paper | Read polarity; a refutation/controversy burst is a negative signal, not momentum |
| Patent velocity looks flat or low | Confirm you are back-dating to priority (not publication) date — the true metric is only visible retrospectively due to the 18-month lag |
| Narrow/novel target, tiny denominators | Acceleration is noisy at small N; widen the window, lower sensitivity, lean on the breadth and translation-event checks |
| Grant spike in an emerging area | Check for an RFA/program-announcement artifact before crediting organic interest |
| Every field "looks like it's growing" | Normalize against all-PubMed CAGR (~4%/yr) — report RGI, not raw growth |
| First IND already filed and multiple Phase 2 readouts exist | You are at consensus; the literature edge is gone — flag low asymmetry |

## Cross-Domain Connections

This skill is deliberately **dual-use**, serving two readers from the same scan:

- For the **clinical scientist learning a field**: the scan is a map of where the data is being generated *fastest* and *most broadly* — which preprints to read first, which landmark paper ignited the front, whether the evidence base is broad or one-lab-deep, and how far the biology is from the clinic. It tells you where the frontier of a field actually is, before the review articles catch up.
- For the **investor screening early opportunities**: the scan is a timing instrument — the realized lead time (literature inflection → first IND) is the asymmetry window, and the de-noising filters (review-stripping, Herfindahl breadth, polarity) are the anti-hype discipline that separates a genuine emerging field from capital-manufactured froth.

- **frontier-intelligence/mindshare-tracker** (sibling): consumes signal-scanner's velocity/acceleration/breadth and adds the attention layer — conference share-of-voice (AACR/ASCO/ASH/ESMO/JPM), Altmetric as a high-noise tripwire, and the 0-100 reflexivity-aware momentum score with a Consensus evidence-maturity gate. Signal-scanner measures *data generation*; mindshare-tracker measures *attention* and reflexive froth.
- **frontier-intelligence/emerging-target-radar** (sibling): the integrator that fuses signal-scanner velocity with mindshare attention and data-engine convergence into a ranked watchlist of target × modality candidates.
- **competitive-intelligence/pipeline-mapper** (depends_on): the first-IND/Phase-1 translation event surfaced in Step 8 is the seed for a full pipeline map — once a target inflects and enters the clinic, pipeline-mapper enumerates the competitive set, stages, and timelines.
- **research/spelunker** (depends_on): supplies the deep-source-spelunking and confidence-vocabulary discipline behind the de-noising layer (polarity reads, breadth assessment, distinguishing primary data from echo) — signal-scanner is its quantitative, target/modality-scoped specialization.
- **probability-of-success/pos-base-rates**: a target that clears the inflection + breadth bar and reaches first-in-human feeds the PoS pipeline; the realized lead time and biomarker/genetics context inform which base-rate row applies.
