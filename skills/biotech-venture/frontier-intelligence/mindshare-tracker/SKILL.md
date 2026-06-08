---
name: mindshare-tracker
description: >
  Compute a 0-100 weighted momentum score for an emerging target or modality from conference
  share-of-voice (AACR/ASCO/ASH/ESMO abstract share, JPM January agenda), financing and NewCo-formation
  flows, and Altmetric as a calibrated high-noise tripwire. Treats reflexivity as structural and pairs
  the score with a contrarian froth-vs-merit overlay plus an orthogonal Consensus evidence-maturity gate.
  Activate when sizing where scientific attention and capital are flowing, whether a theme is pre- or
  post-consensus, and whether momentum is durable merit or reflexive hype.
metadata:
  author: nirav
  version: "1.0"
  parent: frontier-intelligence
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Mindshare Tracker — Quantifying Scientific Attention and the Reflexivity of Capital

By the time a target or modality is consensus — covered in *Nature Reviews*, multiple Phase 2 readouts in hand, generalist-press attention — the asymmetric return is gone. Edge comes from reading the leading indicators of where attention and capital are accreting, and within each indicator, reading the *acceleration* rather than the level. A theme with 200 abstracts/year growing 60% YoY is a far stronger signal than one with 2,000 abstracts/year growing 5%. This skill converts that intuition into a calibrated 0-100 momentum score.

The hard part is not measurement; it is interpretation. Mindshare is **reflexive**: capital concentration genuinely raises probability of success (more shots on goal, better funding, faster iteration, more talent), so the loop *mindshare → capital → talent → higher PoS → more mindshare* is partly self-fulfilling. The score is therefore a **positioning/timing instrument, not a truth-meter** — it tells you where the field is on the attention curve and whether you are early. To keep it honest, every score carries two overlays: a **contrarian froth-vs-merit** read that flags the reflexive hype regime, and an orthogonal **Consensus evidence-maturity gate** that catches the canonical false-positive (high volume, weak/contested evidence).

This skill is dual-use. For a **clinical-scientist learning the field**, it answers "what is everyone suddenly working on, and is the excitement earned?" For an **investor screening early opportunities**, it answers "where is capital flowing, am I early or late, and is this durable or froth?" Both read the same score; they act on different bands.

## How to Run

### Input

| Parameter | Source | Required? |
|---|---|---|
| Target or modality (string + synonyms/MeSH) | User | Yes |
| Peer set to percentile against (sibling targets/modalities) | User | Recommended (default: same MoA class) |
| Conference window (years of meetings to score) | User | Optional (default: last 3 cycles) |
| Indication/asset-class context | User | Optional |
| Financing-regime baseline year | User | Optional (default: current) |

### Steps

#### Step 1 — Define the entity and peer set

Lock the query string, synonym set, and MeSH expansion (e.g. "PROTAC" = "targeted protein degradation" OR "proteolysis-targeting chimera"). Then define the **peer set** you will percentile against — the score is built on acceleration *percentile* versus siblings, not absolute level, so the peer set is consequential. Default to the same MoA class (e.g. all next-gen KRAS inhibitors; all in-vivo programming modalities). A score is meaningless without its comparison cohort.

#### Step 2 — Conference share-of-voice (the core attention signal, 12% + 12%)

Conference SOV is the near-real-time, low-lag attention layer. SOV = (abstracts mentioning target/modality) / (total abstracts) per meeting per year. Denominators are large and stable (ASCO 2025 had >5,000 studies), so SOV is a clean ratio.

- **Query** AACR, ASCO, ASH abstract archives directly; ESMO via *Annals of Oncology* supplements; use WebSearch/WebFetch since these lack clean APIs (note the manual/scraped-count limitation in Error Handling).
- Track the **SOV slope** across consecutive years — a rising slope is the signal, not the level.
- Weight **late-breaking / plenary / oral** (high-conviction) above **poster** (speculative). A poster→oral shift is a maturation signal. Weight investigator-initiated abstracts above sponsor-driven presence.
- Map the leads: Keystone/Gordon (basic science) leads ASCO/ASH (clinical) by 2-4 years; **JPM Healthcare in January sets the annual capital-allocation/narrative agenda** and is roughly coincident with financing.
- Require **multi-meeting persistence** — a single-meeting spike from one big readout is noise.

#### Step 3 — Financing and NewCo-formation flows (12% + 8%)

The **company-creation event is the sharpest venture signal** — a venture builder spinning out a NewCo around a *specific* target/modality front-runs consensus by 1-2 years, far more informative than aggregate sector financing.

- **Log every NewCo** formed around the entity, with founding date, founding investor, and the specific biology. Query SEC EDGAR (Form D private placements, S-1), Crunchbase/Pitchbook, and venture-builder press (Flagship, Arch, Third Rock, Versant). Flagship's July 2024 $3.6B raise to create ~25 companies (Lila Sciences, Expedition Medicines) is the template event.
- **Financing velocity** = $ raised and round count per quarter in the theme.
- **Regime-normalize — mandatory.** Q1 2025 was the lowest US biotech startup-formation quarter in ≥10 years (~70% below the 2021 peak); 2024 ran $26B over 416 rounds with capital barbelled toward de-risked Phase II (median round ~$50M in 2024 → ~$63M by Q3 2025). In a contractionary regime, *relative* concentration of scarce new-formation dollars into a theme beats absolute counts. Watch for momentum/tourist capital ("AI-drug-discovery" rounds with thin biology) — the reflexivity trap.

#### Step 4 — Altmetric as a calibrated high-noise tripwire (4%)

Altmetric Attention Score correlates only moderately with eventual citations (Spearman ρ ≈ 0.59 overall, ≈0.68 in Medicine) and explains only ~12% of 3-year citation variance (R²=0.12). **Use it as a tripwire, never a standalone driver** — its job is surfacing landmark papers within 1-7 days of drop. Read polarity: controversy/retraction inflates attention. Cap its weight; never let a social spike move a band on its own.

#### Step 5 — Supporting velocity inputs (from signal-scanner where available)

If `signal-scanner` output is on hand, ingest its publication acceleration (relative growth index, primary-research only, review-stripped), preprint surge + conversion, citation-burst, patent (priority-date) velocity, and NIH RePORTER new-grant velocity as pre-computed sub-scores. If not, pull headline velocity directly (PubMed `total_count` per rolling window; bioRxiv/medRxiv). These carry the deepest lead times (grants ~5-7yr, literature ~4-7yr) and anchor the "deep signals leading, shallow quiet" contrarian read.

#### Step 6 — Evidence-maturity gate (Consensus, anti-hype multiplier, 4%)

Query **Consensus** on the core mechanistic/efficacy claim: does the accumulating literature actually *support* it (effect direction, replication, study quality), or is it just voluminous? This is the orthogonal quality axis the velocity signals lack. **High volume + low Consensus support = the canonical hype false-positive.** Convert to a **0.7-1.0 multiplier** on the composite.

#### Step 7 — Breadth gate (anti single-lab artifact)

>50% of preclinical findings are irreproducible. Compute an author/institution Herfindahl concentration index on the literature behind the signal. If concentration is in the top decile (single-lab dominated), **cap the literature-derived sub-scores at 50** regardless of raw acceleration. Genuine emergence is broad-based.

#### Step 8 — Score, gate, and cross-check against the clinic

Combine de-noised sub-scores with the weights below, apply the evidence-maturity multiplier and breadth gate, and place the result in an interpretation band. Then **pull the first-IND/Phase-1 date from ClinicalTrials.gov v2** — the gap between attention inflection and first-in-human is the realized lead time the whole exercise exists to capture. A high score with *no* clinical entries = maximal asymmetry; a high score with multiple Phase 2 readouts = you are already at consensus.

#### Step 9 — Apply the contrarian froth-vs-merit overlay

Before reporting, classify the regime:
- **Reflexive froth (avoid):** high financing velocity + high Altmetric/social + LOW Consensus evidence-maturity + HIGH single-lab concentration. The hype-cycle peak.
- **Durable pre-consensus merit (target):** rising primary-research acceleration + broad author breadth + grant flows present, while financing/social are still muted — genuine momentum the market hasn't priced.
- **Rule:** trust deep+broad signals (primary-research acceleration with high breadth, multi-meeting SOV, evidence-maturity) over shallow+concentrated signals (social spikes, single-incumbent patents, tourist financing). When they diverge, the divergence is the most valuable read.

## Output

```
MINDSHARE / MOMENTUM SCORE — [Target × Modality]
Date: [assessment date]   |   Peer set: [comparison cohort]

COMPOSITE MOMENTUM: [0-100]   →   BAND: [80-100 / 55-79 / 30-54 / 0-29]
Evidence-maturity multiplier (Consensus): [0.70-1.00]
Breadth gate: [PASS / CAPPED — literature sub-scores held at 50]

Weighted sub-scores (acceleration-percentile vs peer set):
| # | Signal                                   | Weight | Sub-score | Contribution |
|---|------------------------------------------|--------|-----------|--------------|
| 1 | Publication acceleration (RGI, primary)  |  18%   |   [0-100] |    [w×s]     |
| 2 | Preprint surge + conversion              |  14%   |   [0-100] |    [w×s]     |
| 3 | Citation acceleration / landmark burst   |  14%   |   [0-100] |    [w×s]     |
| 4 | Conference share-of-voice trajectory     |  12%   |   [0-100] |    [w×s]     |
| 5 | Company-creation events (regime-norm.)   |  12%   |   [0-100] |    [w×s]     |
| 6 | Venture financing velocity (regime-norm.)|   8%   |   [0-100] |    [w×s]     |
| 7 | Patent velocity (priority-date adjusted) |   8%   |   [0-100] |    [w×s]     |
| 8 | NIH/funder new-grant velocity            |   6%   |   [0-100] |    [w×s]     |
| 9 | Altmetric/KOL attention (tripwire)       |   4%   |   [0-100] |    [w×s]     |
|10 | Consensus evidence-maturity (multiplier) |   4%   |   [mult]  |    gate      |

CONFERENCE SOV DETAIL:
  AACR/ASCO/ASH/ESMO SOV slope: [rising/flat/falling], poster→oral shift: [Y/N]
  JPM January agenda presence: [yes/no]

CAPITAL DETAIL:
  NewCos formed: [N, with founding investor + biology]
  Financing velocity (regime-normalized): [$/quarter vs theme baseline]

TRANSLATION CROSS-CHECK (ClinicalTrials.gov v2):
  First IND/Phase-1 date: [date or "none yet"]
  Realized lead time (attention inflection → FIH): [X years]
  Position: [pre-clinical / first INDs filed / multiple Ph2 = consensus]

CONTRARIAN OVERLAY:
  Regime: [REFLEXIVE FROTH / DURABLE PRE-CONSENSUS MERIT / MIXED]
  Rationale: [deep-vs-shallow signal divergence]

DUAL-USE READ:
  For the scientist: [is the excitement earned by evidence?]
  For the investor: [early or late? durable or froth? action by band]
```

## Error Handling

| Scenario | Response |
|---|---|
| No clean conference-abstract API | Use WebSearch/WebFetch on AACR/ASCO/ASH archives and *Annals of Oncology* supplements; count manually; flag denominator normalization across meetings as approximate |
| Score is high but Consensus evidence-maturity is low | Apply the 0.7-1.0 multiplier; flag as candidate hype false-positive; do not report a high band uncaveated |
| Literature dominated by one lab/group (high Herfindahl) | Cap literature sub-scores (1,2,3) at 50; surface the breadth problem explicitly |
| Financing looks strong in absolute terms | Regime-normalize against the contractionary baseline (Q1 2025 ~70% off 2021 peak); report *relative* concentration, not absolute $ |
| Altmetric spike with no other signal | Treat as tripwire only; do not move the band; check polarity for controversy/retraction |
| Rare/novel target with tiny denominators | Acceleration is noisy at small N; widen the window, lower sensitivity, and lean on company-creation + grant signals over ratio-based SOV |
| High score AND multiple Phase 2 readouts already | You are at consensus — the asymmetric edge is gone; report the realized-lead-time gap and down-rank as a fresh opportunity |

## Cross-Domain Connections

- **frontier-intelligence/signal-scanner** (depends on): supplies the de-noised literature/preprint/patent/grant velocity sub-scores (signals 1-3, 7-8). mindshare-tracker layers attention, capital, and the reflexivity overlays on top.
- **frontier-intelligence/emerging-target-radar**: consumes this momentum score as the attention dimension when ranking the candidate watchlist.
- **frontier-intelligence/frontier-conviction-scorer**: momentum is a *positioning* input, deliberately orthogonal to the *biological-merit* conviction score — the two are read together to separate reflexive timing from durable merit.
- **investing/reflexivity-theory** (depends on): the structural foundation — mindshare→capital→talent→PoS is a Soros-style reflexive loop; the score measures a partly self-fulfilling phenomenon, which is why it is a timing instrument and demands a contrarian overlay.
- **investing/secular-themes** (depends on): conference SOV and financing flows are the leading edge of secular-theme formation in biotech; this skill is how a nascent theme is detected before it is priced.
- **Dual use, explicit:** the same score serves a *clinical-scientist* mapping where the field's energy is going (and whether it is evidence-backed via the Consensus gate) and an *investor* screening early opportunities (and whether momentum is durable merit or reflexive froth). Scientist reads the evidence-maturity gate hardest; investor reads the band, the lead-time gap, and the contrarian overlay hardest.
