# Mindshare Tracker — Quick Reference

## Input

| Parameter | Source | Required? |
|---|---|---|
| Target or modality (string + synonyms/MeSH) | User | Yes |
| Peer set to percentile against | User | Recommended (default: same MoA class) |
| Conference window | User | Optional (default: last 3 cycles) |
| Indication/asset-class context | User | Optional |
| Financing-regime baseline year | User | Optional (default: current) |

## The weighted scoring rubric (signal → weight → source)

Sub-scores are 0-100 on **acceleration percentile vs the peer set**, not on level. De-noise per the gates, then weight.

| # | Signal (acceleration-percentile sub-score) | Weight | Data source / tool | Lead to FIH | Noise |
|---|---|---|---|---|---|
| 1 | Publication acceleration (primary-research, RGI) | **18%** | PubMed E-utilities `total_count` | ~4-7 yr | Med |
| 2 | Preprint surge + conversion rate | **14%** | bioRxiv / medRxiv API | ~3-6 yr | Higher |
| 3 | Citation acceleration / landmark burst | **14%** | OpenAlex, Dimensions, Semantic Scholar | ~3-5 yr | Med |
| 4 | Conference share-of-voice trajectory | **12%** | AACR/ASCO/ASH archives, ESMO via Ann Oncol; JPM (Jan agenda) | ~1-3 yr | Low-med |
| 5 | Company-creation events (regime-normalized) | **12%** | SEC EDGAR (Form D/S-1), Crunchbase, Pitchbook, VB press | ~2-4 yr | Low-freq, high-signal |
| 6 | Venture financing velocity (regime-normalized) | **8%** | EDGAR, BioPharma Dive, Pitchbook | ~2-4 yr | Regime-dependent |
| 7 | Patent velocity (PCT/WO, priority-date adjusted) | **8%** | Lens.org, PatentsView, Espacenet | ~2-4 yr (−18mo) | Structurally lagged |
| 8 | NIH/funder new-grant velocity | **6%** | NIH RePORTER API | ~5-7 yr | Low velocity, lags novelty |
| 9 | Altmetric / KOL attention (tripwire only) | **4%** | Altmetric, Dimensions | ~0-2 yr | Very high |
| 10 | Consensus evidence-maturity | **4% (also a multiplier)** | Consensus / consensus.app | — | Quality axis |

`Composite = Σ(sub-score × weight)`, then apply gates below. **Translation ground truth:** ClinicalTrials.gov v2 first-IND date (lead-time gap = attention inflection → FIH).

## Gates (apply before reporting the band)

```
EVIDENCE-MATURITY GATE (anti-hype):  composite ×= mult ∈ [0.70, 1.00]   (low Consensus support → toward 0.70)
BREADTH GATE (anti single-lab):      if author-affiliation Herfindahl in top decile
                                     → cap literature sub-scores (1,2,3) at 50
```

## Interpretation bands

| Band | Meaning | Action |
|---|---|---|
| **80-100** | Inflecting hard; at/near consensus | Check lead-time gap — if INDs already filed, edge is gone |
| **55-79** | Genuine emerging momentum, pre-consensus | **The target zone** |
| **30-54** | Early / ambiguous | Watch the acceleration trend |
| **0-29** | Dormant or decelerating | Pass |

## Anti-hype gate checklist (must clear before reporting a high band)

- [ ] **Review-stripped:** literature counts exclude Review/Editorial/Comment publication types (primary-research fraction rising?)
- [ ] **Breadth:** author/institution Herfindahl NOT top-decile (not a single-lab artifact; >50% preclinical findings irreproducible)
- [ ] **Evidence direction:** Consensus confirms effect direction + replication + study quality (multiplier ≥ 0.85?)
- [ ] **Polarity:** citation/Altmetric bursts are NOT driven by refutation, retraction, or controversy
- [ ] **Regime-normalized capital:** financing/NewCo read as *relative* concentration vs contractionary baseline, not absolute $
- [ ] **Multi-meeting persistence:** conference SOV rises across ≥2 consecutive meetings, not one spike
- [ ] **Altmetric capped:** social signal is a tripwire only, did not move the band
- [ ] **Clinic cross-check:** ClinicalTrials.gov first-IND date pulled; lead-time gap reported

## Contrarian froth-vs-merit overlay

| Regime | Configuration | Verdict |
|---|---|---|
| **Reflexive froth** | high financing + high social + LOW Consensus maturity + HIGH single-lab concentration | Avoid — hype-cycle peak |
| **Durable pre-consensus merit** | rising primary-research accel + broad author breadth + grants present; financing/social still muted | **Target — unpriced momentum** |
| **Mixed** | deep and shallow signals disagree | The divergence IS the read; trust deep+broad over shallow+concentrated |

## Reflexivity primitive (why this is a timing instrument, not a truth-meter)

```
mindshare → capital → talent → genuinely higher P(success) → more mindshare   (self-fulfilling loop)
```
The score measures position on the attention curve, NOT underlying biological merit. Reflexivity is structural, not a bug. Always pair with: (1) Consensus evidence-maturity gate, (2) contrarian froth overlay, (3) ClinicalTrials.gov lead-time cross-check.

## Calibration anchors (from source brief)

- PubMed returns exact `total_count` per query+window — e.g. **658 PROTAC/TPD papers in 2024** (the atomic velocity op).
- Altmetric ↔ citations: **Spearman ρ ≈ 0.59** overall (≈0.68 Medicine), **R² ≈ 0.12** → tripwire only.
- Preprints lead journal pub by **6-18 months**; preprinted papers get first citation ~1mo earlier, ~0.5× more citations.
- Patent PCT/WO: **18-month publication lag** → back-date to priority; mid-stage confirmation, not earliest-mover.
- Capital regime: **Q1 2025 lowest US biotech startup-formation quarter in ≥10 yr (~70% off 2021 peak)**; 2024 = $26B / 416 rounds; median round ~$50M (2024) → ~$63M (Q3 2025).
- Flagship July 2024: **$3.6B to create ~25 companies** (Lila Sciences, Expedition Medicines) — the NewCo-event template.
- ASCO 2025: **>5,000 studies** (stable SOV denominator).
- Reproducibility: **>50% of preclinical findings irreproducible (~$28B/yr US)** → breadth gate.
- Realized lead time (literature inflection → FIH) for a novel target: **typically 3-7 years**.
