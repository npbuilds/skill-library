# MOA Analog Engine — Quick Reference

The generalizable five-phase pattern plus the placement method. Full per-class profiles in `moa-arc-library.md`.

## Input

| Parameter | Source | Required? |
|---|---|---|
| Target or mechanism of action | User / emerging-target-radar | Yes |
| Modality | User | Recommended |
| Indication | User | Recommended |
| Lead asset(s) and sponsor(s) | User / ClinicalTrials.gov | Optional |
| Known false starts | User / PubMed | Optional |

## The five canonical phases

| Phase | What happens | Typical duration | Capital state |
|---|---|---|---|
| **0. Target ID / validation** | Gene/protein linked to disease (genetics, KO, human LOF/GOF) | — | Academic |
| **1. First tool compound / platform** | A molecule or delivery platform engages the target — proof it's *druggable* | 2-8 yr after target ID | Seed / academic |
| **2. First-in-human** | IND, Phase 1 safety + PK, target engagement in patients | 3-7 yr after tool | Venture / pharma |
| **3. First approval (first-in-class)** | First-in-class drug clears its pivotal trial | total 12-39 yr from target ID | Big pharma |
| **4. Class explosion** | Fast-followers, new indications, next-gen chemistry | 2-5 yr after first approval | Crowded |
| **5. Maturity** | Convenience reformulation (oral, SC, less-frequent), combos, biosimilars | 5-15 yr after explosion | Defensive |

## The time constant (target ID → first approval)

| Class | Years | Note |
|---|---|---|
| PCSK9 | ~12 | **Fastest** — clean healthy human LOF carriers |
| IL-23/IL-17 | ~8-15 | Pathway dissection |
| BTK | ~20 | |
| PD-1 | ~22 | |
| GLP-1 | ~20-23 | |
| PROTAC | ~24 | Concept 2001 → vepdegestrant 2025 |
| CAR-T | ~25+ | |
| anti-amyloid | ~31-32 | Brutal failure record |
| KRAS | ~39 | **Slowest** — undruggable until 2013 chemistry |

**Median ~18-25 yr.** Explosion window: **2-5 yr.** Rate-limiter = the slowest of {modality, validation, biology}.

## The three locks (a class needs ALL THREE to explode)

1. **Validated biology** — ideally a human genetic phenotype (PCSK9 LOF, BTK in XLA, APP/PSEN in AD).
2. **A modality that can drug it** — usually the *true* rate-limiter. Enabling-platform unlocks: GalNAc (siRNA), site-specific linkers + DXd (ADC), covalent switch-II (KRAS), E3 recruitment (degraders), costimulatory domain (CAR-T), BBB-shuttle (trontinemab).
3. **A de-risking pivotal readout** — the ignition event. Hard endpoint in a defined population.

## The three named sub-patterns

| Pattern | Index case | The unlock | Leading indicator |
|---|---|---|---|
| **Undruggable-cracking** | KRAS (2013 Shokat) | Chemistry, not biology — covalent / glue / degrader | First co-crystal of covalent/ternary ligand; platform generalizes past index target |
| **Indication-creep explosion** | GLP-1 | Dose pushed high enough; new indications fall | Hard-surrogate signal (weight, LDL) visible years early |
| **Generational resistance-ladder** | BTK (C481S) | Each rung defeats a defined resistance/tolerability problem | A dominant recurrent escape mutation appears |

## Ignition events (the validating readout per class)

| Class | Ignition trial (year) |
|---|---|
| PD-1 | KEYNOTE-024 (2016) |
| PCSK9 | FOURIER (2017) |
| CAR-T | ELIANA / ZUMA-1 (2017) |
| GLP-1 obesity | SELECT (2023) |
| KRAS G12C | CodeBreaK 100 (2021) |
| ADC redemption | DESTINY-Breast / T-DXd (2019-2022) |
| anti-amyloid | CLARITY-AD (2023) |
| PROTAC | VERITAC-2 (2025) |

**Doctrine:** for a pre-ignition candidate, the whole question is *which pending trial is its ignition event, and when does it read out?* It is always a hard-endpoint readout in a genetically- or biomarker-defined population. A soft surrogate or all-comers design does not ignite.

## Leading indicators a class WILL explode (rank-ordered)

1. **Healthy human LOF carriers** mirroring the drug effect (PCSK9 — strongest signal there is).
2. **n-of-1 durable/curative responses** in terminal disease (CAR-T; PD-1 melanoma tail).
3. **A dominant recurrent resistance mutation** (guarantees a next sub-class — BTK C481S).
4. **A platform/chemistry unlock that generalizes** beyond the index target (KRAS → pan-RAS; GalNAc → any hepatic gene).
5. **Efficacy in a population the target "shouldn't" reach** (T-DXd in HER2-low).
6. **Dose-dependent effect on a hard surrogate, visible years early** (GLP-1 weight loss; amyloid clearance tracking cognition).
7. **A clear unmet need *inside* an already-treated population** (EVH on C5 blockade → factor B/D wedge).

## Leading indicators a class will STALL

- Effect on a **soft/unvalidated surrogate** with no genetic tie to outcomes (CETP/torcetrapib).
- **No modality** despite validated biology — idles for decades (KRAS 1982-2013).
- **Wrong molecular species or disease stage** (γ-secretase, BACE in symptomatic AD).
- **A platform that can't make drug-like molecules** (early PROTAC oral PK).
- **A manufacturing/cost ceiling** capping the market (ex-vivo CAR-T → in vivo is the next bet).

## False-start diagnostic (the BUY-not-kill doctrine)

```
Is the failure in the BIOLOGY or the MODALITY/EXECUTION?

  BIOLOGY failure  → KILLS the class
    - soft surrogate, no genetic tie (CETP raised mortality)
    - confirmed mechanism harm (γ-secretase worsened cognition)
    → AVOID

  MODALITY/EXECUTION failure → RE-ENGINEERABLE
    - bad linker (1st-gen ADC), bad delivery (pre-GalNAc siRNA),
      wrong dose, wrong amyloid species, bad oral PK (early PROTAC)
    → the failure is the PENULTIMATE stage.
       If a re-engineered asset with the fix is advancing → BUY-on-ignition-readout
```

Comebacks that proved the doctrine: anti-amyloid (15 yr of failures → lecanemab/donanemab), ADC (gemtuzumab 2010 withdrawal → T-DXd), siRNA (2010-11 industry exodus → patisiran via GalNAc).

## Placement method (6 steps)

```
1. CHARACTERIZE  → target class, validation type, modality maturity, stage
                   (Open Targets, gnomAD, ClinicalTrials.gov, ChEMBL)
2. FIND ANALOG   → match on UNLOCK MECHANISM, not indication
3. SUB-PATTERN   → undruggable-cracking | indication-creep | resistance-ladder
4. ARC-POSITION  → place Phase 0-5; remaining clock = time constant − elapsed;
                   flag rate-limiter
5. IGNITION      → name the still-pending pivotal readout (NCT#, endpoint, window)
6. FALSE-START   → biology-killed (avoid) vs modality-redeemable (buy)
```

## Maturity tells (the alpha has left)

Convenience/cadence reformulation = commodity maturity: subcutaneous PD-1 (Keytruda Qlex, Sept 2025), oral GLP-1 (orforglipron), oral PCSK9 (enlicitide), twice-yearly inclisiran. When a class competes on route/dosing cadence rather than efficacy, it has matured.

## Error Handling

| Scenario | Response |
|---|---|
| No clean analog | Match on sub-pattern (unlock mechanism); flag "novel — widen uncertainty" |
| Modality on a validated target | Split: biology rides the validated arc; modality risk → modality-lifecycle. Don't double-count |
| Multiple analogs | Report primary (mechanism shape) + secondary (explosion pattern); state dominant time constant |
| Ignition trial not yet registered | Name the endpoint/population a future pivotal must hit; monitor CT.gov + congress abstracts |
| Failure but no re-engineered successor | Hold "biology-vs-modality unresolved"; no buy until the fix is advancing |
| Pre-IND / tool stage | Place Phase 1-2; emphasize time-constant estimate over ignition trial |
