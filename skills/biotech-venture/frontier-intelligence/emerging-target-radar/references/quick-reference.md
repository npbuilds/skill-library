# Emerging Target Radar — Quick Reference

Condensed cheat-sheet: the watchlist schema, the fusion/ranking primitives, the pattern-tag decision rule, and the current top-15 emerging target × modality candidates with pattern-tag and lead-time columns. All figures are 2024-2026 point estimates; spot-verify before load-bearing use.

## Input

| Parameter | Source | Required? |
|---|---|---|
| Scope (TA, modality, or broad frontier scan) | User | Yes |
| Signal-scanner output (velocity + acceleration + breadth) | signal-scanner / WebSearch | Recommended |
| Mindshare-tracker output (0-100 + Consensus gate) | mindshare-tracker / WebSearch | Recommended |
| Data-generation-monitor output (convergence count) | data-generation-monitor | Recommended |
| Velocity window | User | Optional (default 3 yr) |
| Financing-regime year | User | Optional (default current) |

## Watchlist Schema (candidate object — handoff contract to analog engine)

```
{
  target:            str          # e.g. "RAS(ON) tri-complex", "GPR75"
  modality:          str          # e.g. "molecular glue", "GalNAc-siRNA", "tLNP in vivo CAR"
  indication:        str
  arc_position:      enum         # target-ID | tool-compound | FIH | first-approval | explosion | maturity
  pattern_tag:       enum         # genetics-first | modality-unlock | resistance-ladder
  lead_time:         {realized_yr | expected_yr, basis}   # inflection→FIH; 3yr if tractable, 7yr if biology-stage
  newco_events:      [{company, $, date, builder, regime_weight}]   # incl. big-pharma deal-equivalents
  supporting_signals:{velocity_accel, breadth_herfindahl, mindshare_0_100, convergence_count}
  evidence_gate:     enum         # PASS | HYPE | SINGLE-LAB | AI-NOVELTY-DISCOUNT
  radar_rank:        0-100
}
```

## Ranking Primitive (pseudocode)

```
RADAR RANK (0-100) =
    0.35 × fused_signal_strength      # velocity accel + multi-lab breadth + convergence count, evidence-gated
  + 0.25 × newco_signal               # event count × regime-normalization weight
  + 0.25 × lead_time_actionability    # remaining runway before consensus; penalize already-crowded
  + 0.15 × pattern_clarity            # clean genetics-first / post-ignition modality-unlock > ambiguous

HARD GATES (apply first; cap rank at 40):
  HYPE             : high volume + low Consensus evidence quality → "watch, don't underwrite"
  SINGLE-LAB       : author-affiliation Herfindahl too concentrated → artifact discount
  AI-NOVELTY       : "AI-found a novel target" w/o wet-lab/clinical validation → discount
                     (AI in molecular DESIGN is credible; AI does NOT yet move Ph2/3 odds)

LEAD TIME:
  realized_lead = FIH_year − inflection_year          # only if FIH reached (ClinicalTrials.gov v2)
  expected_lead = 3 yr (tractable chem matter exists) … 7 yr (biology-stage, no handle)
  novel-target literature-inflection → FIH gap typically 3-7 yr
```

## Pattern-Tag Decision Rule

| If… | Tag | Ignition event to watch | Index analog |
|---|---|---|---|
| Human-genetics (esp. LoF-protective) validation preceded the drug | **genetics-first** | CV / hard-outcome trial | PCSK9 (~12 yr, speed champ); GPR75; TL1A |
| Flat/disordered/pocketless target unlocked by chemistry/platform fix, not new biology | **modality-unlock** | First-in-class pivotal readout | KRAS (covalent switch-II, 2013→2021); VAV1 (glue); in vivo CAR (tLNP); siRNA (GalNAc) |
| Each sub-class triggered by a defined resistance mutation | **resistance-ladder** | The resistance mutation itself | BTK: ibrutinib → acal/zanu → pirtobrutinib (C481S) → degraders |

**Doctrine:** a marquee failure followed by a modality re-engineering is a BUY, not a KILL (anti-amyloid → lecanemab; ADC → DXd payloads; siRNA → GalNAc). Convenience/cadence reformulation (oral, subcutaneous, longer dosing) = commodity maturity → alpha has left.

## Signal Hierarchy (lead time, ranked)

| Signal | Lead | Notes |
|---|---|---|
| Publication/preprint **2nd derivative** (acceleration) | 1-3 yr ahead of counts | Single most actionable; strip reviews first |
| Preprint velocity (bioRxiv/medRxiv) | 6-18 mo ahead of peer-review | Earliest formal-literature signal |
| Citation burst on landmark paper (Kleinberg/CiteSpace) | — | Beats diffuse incremental growth |
| **NewCo-creation event** | 1-2 yr ahead of consensus | SHARPEST venture signal; normalize to regime |
| Conference share-of-voice (AACR/ASCO/ASH/ESMO; JPM) | near-real-time | Low-lag attention; ASCO 2025 >5,000 studies |
| New data-engine release (pQTL/MR, DepMap, Perturb-seq) | — | Pipeline of pre-validated targets; score by net-new convergences |
| Patent velocity (PCT/WO) | mid-stage confirm | Structural 18-mo publication lag |
| NIH RePORTER grant flows | ~5-7 yr (deepest) | Lowest velocity, most lagging to novel biology |
| Altmetric/social | tripwire only | rho~0.59, R²~0.12; never standalone |
| **ClinicalTrials.gov v2 first IND/Ph1** | ground truth | Closes the lead-time measurement |

**Regime normalization:** Q1 2025 = decade-low US biotech startup formation (~70% off 2021 peak). Up-weight each 2025 NewCo.

## Current Top-15 Watchlist (2026-06)

| # | Target × Modality | Pattern Tag | Arc Position | Lead Time | Key Sponsor / NewCo-Deal Signal |
|---|---|---|---|---|---|
| 1 | RAS(ON) tri-complex (daraxonrasib RMC-6236; zoldonrasib G12D; elironrasib G12C) | modality-unlock | FIH→1st-approval (Ph3, BTD) | realized ~8 yr (tool 2013→Ph3) | Revolution Medicines; ~47% ORR 1L PDAC |
| 2 | Human-genetics obesity (GPR75, INHBE/activin E, ACVR1C/ALK7) × GalNAc-siRNA/Ab | genetics-first | tool→FIH (early clinical) | expected 4-6 yr | Arrowhead (ARO-INHBE, ARO-ALK7), Regeneron 640K exomes |
| 3 | Amylin (CagriSema; amycretin oral GLP-1/amylin) | genetics-first / indication-creep | 1st-approval filed → explosion | realized (filed 2025) | Novo Nordisk; Lilly; Metsera/Zealand |
| 4 | TL1A / anti-TNFSF15 (duvakitug; tulisokibart; afimkibart) | genetics-first | FIH→1st-approval (best-in-class Ph2b) | realized, pre-explosion | Sanofi/Teva ~48% UC remission; Merck; Roche |
| 5 | TREM2 agonism (oral VG-3927) | genetics-first | tool→FIH (Ph2 planned) | expected 3-5 yr | Sanofi × Vigil $470M+; Alector; Denali |
| 6 | Molecular-glue immune degraders (VAV1: MRT-6160) | modality-unlock | tool→FIH | expected 3-5 yr | Monte Rosa × Novartis up to $2.1B; Neomorph × Novo $1.46B, × Biogen $1.45B |
| 7 | WRN synthetic lethality (MSI-high) (HRO761; VVD-133214; GSK4418959) | modality-unlock | tool→FIH (multi-asset Ph1) | expected 4-6 yr | Novartis; Vividion/Roche; GSK |
| 8 | MTA-cooperative PRMT5 (MTAP-deleted ~10-15%) (AMG193; AZD3470; IDE892) | modality-unlock | tool→FIH (multi-asset Ph1) | expected 4-6 yr | Amgen; AstraZeneca; IDEAYA (IND Q3 2025) |
| 9 | In vivo CAR (anti-CD19 mRNA in tLNP) (CPTX2309) | modality-unlock | FIH (steepest curve) | realized (Ph1 Jun 2025) | Capstan × AbbVie ~$2.1B; CREATE $122M Series B |
| 10 | In vivo CRISPR / base editing (lonvo-z NTLA-2002; BEAM-302; VERVE-102) | modality-unlock | first-approval (registrational) | realized | Intellia (Ph3 HAELO positive); Beam; Verve |
| 11 | Muscle-sparing obesity (activin RII / myostatin) (bimagrumab; apitegromab) | genetics-first | FIH (commercially contested) | expected 3-5 yr | Lilly/Versanis; Scholar Rock; Regeneron (COURAGE) |
| 12 | IL-2 muteins / Treg-selective tolerance (efavaleukin alfa; mRNA muteins; CAR-Treg) | modality-unlock | FIH | expected 4-6 yr | Amgen; Moderna; Sonoma/Abata/Quell |
| 13 | TP53 reactivation / MYC-MYCN degradation (eprenetapopil APR-246) | modality-unlock | tool→FIH | expected 5-7 yr | Aprea-lineage; multiple glue/PROTAC players |
| 14 | Partial reprogramming / precision senolytics (ER-100; UBX1325) | modality-unlock | tool→FIH | expected 5-7 yr (high variance) | Life Bio (ER-100 FIH Q1 2026); Unity (Ph2b DME) |
| 15 | NLRP3 inflammasome (NACHT binders BAL-0028/0598) — WATCH, DON'T UNDERWRITE | modality-unlock | tool (high mindshare, evidence gap) | expected 5-7 yr | No approved direct inhibitor yet; evidence-gate caution |

**Tiering:** #1-10 = de-risked / maturing-into-winners (clinical data + capital converging). #11-12 = genetics-first emerging (validation strong, modality being built / commercially contested). #13-14 = modality-enabled undruggable unlocks, earlier and higher-variance. #15 = HYPE-gated watch (high mindshare, thin human data).

**Also-on-radar (Tier-4 watch):** GPNMB (neuro + senescence dual-use, Alector ADP027); gut-brain / α-synuclein PD prevention (GUT-PARFECT FMT) — both early, heterogeneous, prevention-distinctive.

## Error Handling

| Scenario | Response |
|---|---|
| Upstream streams unavailable | Reconstruct via PubMed E-utilities, bioRxiv/medRxiv, conference abstracts, EDGAR/press; flag lower-fidelity |
| High velocity, no convergence, HYPE flag | Hard-gate to "watch, don't underwrite"; cap rank at 40 |
| Single-lab dominance (Herfindahl fail) | Discount as artifact; require multi-lab breadth |
| No FIH yet | Use expected lead time (3 yr if tractable matter, 7 yr if biology-stage) |
| NewCo events sparse | Use big-pharma licensing/M&A on the exact mechanism as confirmation-equivalent |
| "AI-discovered target" claim | Down-weight unless AI acted in molecular design with independent validation |
| Crowded/post-explosion class | Lower lead-time actionability; flag alpha has likely left |
| Contractionary financing year | Up-weight each NewCo event (2025 spinout > 2021 spinout) |
