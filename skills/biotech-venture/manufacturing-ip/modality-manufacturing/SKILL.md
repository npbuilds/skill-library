---
name: modality-manufacturing
description: >
  Catalog manufacturing considerations, COGS benchmarks, scalability profiles, and
  process development timelines for each major therapeutic modality. Reference when
  assessing whether a company's manufacturing strategy is feasible and economically
  viable, evaluating COGS impact on commercial margins, or comparing modality
  risk across portfolio assets.
metadata:
  author: nirav
  version: "1.0"
  parent: manufacturing-ip
compatibility: Designed for Claude Code
allowed-tools: Read, WebSearch, WebFetch
---

# Modality Manufacturing — The Hidden Determinant of Biotech Value

Manufacturing is the most underappreciated risk factor in biotech venture diligence. Financial analysts model peak sales and probability of success but rarely interrogate whether a company can actually manufacture its product at scale, at acceptable cost, with consistent quality. Yet manufacturing failures account for a meaningful fraction of Complete Response Letters, and COGS determines whether a drug that works clinically can generate attractive margins commercially.

The physician-scientist in venture must understand enough about manufacturing to ask the right questions: Can this gene therapy be produced at a cost that supports a commercially viable price? Does this autologous cell therapy have a vein-to-vein time compatible with the disease urgency? Is the ADC linker-payload chemistry scalable, or will batch failures destroy margins?

## Modality Manufacturing Profiles

> **COGS data:** The authoritative, provenance-tagged cross-modality COGS/margin/capex table (incl. autologous cell therapy and the few externally-verified anchors) lives in `references/modality-cogs-profiles.md`. Primary COGS data is scarce — most figures are internal estimates; the reference doc tags each by confidence and lists refuted "lore" (titer ladder, CAR-T parallelization). Use it as the single source; `cmc-risk-assessor` delegates to it too.

### Small Molecule

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $0.10 - $5.00 | Lowest COGS of any modality |
| **Gross margin** | 85-95% | Highest margins in biopharma |
| **Scale-up complexity** | Low | Well-established synthetic chemistry |
| **Facility cost** | $50-150M | Standard chemical synthesis + formulation |
| **Process development timeline** | 12-18 months | Relatively fast; ICH Q8-Q12 framework mature |
| **Key challenges** | Polymorphism, solubility, API sourcing | Crystal form patents important for lifecycle management |
| **CMO availability** | Abundant | Dozens of qualified CMOs globally (Lonza, Catalent, Patheon, Siegfried) |

### Monoclonal Antibody (mAb)

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $20 - $200 | Driven by titer, purification yield, fill-finish |
| **Gross margin** | 75-90% | Strong but lower than small molecule |
| **Scale-up complexity** | Moderate | CHO cell culture well-established; 2,000-15,000L bioreactors standard |
| **Facility cost** | $200-500M | Large-scale mammalian cell culture facility |
| **Process development timeline** | 18-24 months | Cell line development, process optimization, analytical methods |
| **Key challenges** | Cell line stability, aggregation, glycosylation consistency | Biosimilar competition erodes pricing at LOE |
| **CMO availability** | Good | Samsung Biologics, Lonza, Boehringer Ingelheim, WuXi Biologics |
| **Titer benchmarks** | 3-8 g/L typical; >10 g/L achievable | Higher titer = lower COGS; platform processes now standard |

### Antibody-Drug Conjugate (ADC)

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $500 - $3,000 | mAb cost + payload synthesis + conjugation |
| **Gross margin** | 65-80% | Lower than naked mAb due to payload and conjugation complexity |
| **Scale-up complexity** | High | Three separate manufacturing streams (mAb + payload + conjugation) |
| **Facility cost** | $300-600M | Requires cytotoxic containment for payload manufacturing |
| **Process development timeline** | 24-36 months | Linker-payload chemistry optimization, conjugation process, stability |
| **Key challenges** | DAR (drug-to-antibody ratio) consistency, payload potency requirements, aggregation after conjugation | Cytotoxic containment requirements limit CMO options |
| **CMO availability** | Limited | Lonza, Piramal, Novasep, CMIC; cytotoxic capability required |
| **Key metric** | DAR distribution (typically target 4) | Narrow DAR distribution = better product quality and PK consistency |

### Bispecific Antibody

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $50 - $500 | Depends on format; some approach mAb COGS |
| **Gross margin** | 70-85% | Format-dependent |
| **Scale-up complexity** | Moderate-High | Chain pairing, mispairing reduction, purification of correct species |
| **Facility cost** | $200-500M | Similar to mAb with additional purification complexity |
| **Process development timeline** | 24-30 months | Format-specific optimization, chain pairing solutions |
| **Key challenges** | Light-chain mispairing, heterodimer purity, stability | Knobs-into-holes, CrossMAb, common light chain address mispairing |
| **Platform maturity** | Rapidly improving | Roche (CrossMAb), Amgen (BiTE), AbbVie/Genmab (DuoBody) |
| **Formats** | IgG-like, BiTE (tandem scFv), DVD-Ig, trispecific | IgG-like formats have longer half-life; BiTE requires continuous infusion or SubQ |

### Gene Therapy (AAV)

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $50,000 - $500,000 | Highest COGS in biopharma; driven by vector yield |
| **Gross margin** | 40-70% | Under severe pressure at $1-3.5M price points |
| **Scale-up complexity** | Very High | Vector yield, full/empty capsid ratio, potency assay variability |
| **Facility cost** | $300-800M | Specialized viral vector manufacturing |
| **Process development timeline** | 30-48 months | Serotype optimization, process scale-up, fill-finish at low volume |
| **Key challenges** | Full/empty capsid separation (target >80% full), potency assay standardization, immunogenicity to capsid limiting re-dosing | Scale remains the defining challenge |
| **CMO availability** | Constrained | Catalent, Lonza, FUJIFILM Diosynth; capacity improving but still tight |
| **Manufacturing platforms** | Triple transfection (HEK293), baculovirus/Sf9, stable producer cell lines | Stable producer lines improving yield but require longer development |
| **Critical quality attributes** | Vector genome titer, full/empty ratio, potency, residual DNA, capsid identity | Analytical methods still evolving; FDA scrutiny increasing |

### Cell Therapy — Autologous

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $50,000 - $150,000 | Patient-specific manufacturing; no economies of scale |
| **Gross margin** | 30-55% | Lowest margins in biopharma at current pricing |
| **Scale-up complexity** | Very High (scale-out, not scale-up) | Each patient = one manufacturing run; parallel processing |
| **Facility cost** | $200-500M | Cleanroom suites, often decentralized |
| **Process development timeline** | 24-36 months | Apheresis optimization, transduction/editing, expansion, cryopreservation |
| **Key challenges** | Vein-to-vein time (14-28 days typical), manufacturing failure rate (5-10%), variability in starting material | Logistics are a competitive differentiator |
| **Vein-to-vein time** | 14-28 days (target <14 days) | Shorter = fewer patients lost to bridging therapy progression |
| **Manufacturing success rate** | 90-95% (target >95%) | Patient apheresis quality is the primary variable |

### Cell Therapy — Allogeneic ("Off-the-Shelf")

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $5,000 - $30,000 | Dramatic COGS reduction vs autologous |
| **Gross margin** | 70-85% | Approaches mAb-like margins at scale |
| **Scale-up complexity** | High | Donor selection, gene editing for HLA knockout, banking, potency |
| **Facility cost** | $200-500M | Similar to autologous but centralized |
| **Process development timeline** | 30-42 months | Gene editing optimization, master cell bank creation |
| **Key challenges** | GvHD risk, persistence (typically shorter than autologous), re-dosing strategy, NK cell rejection | Clinical efficacy still being proven; no approvals yet |
| **Key advantage** | Inventory model — manufacture in advance, ship on demand | Eliminates vein-to-vein delay and manufacturing failure at patient level |

### mRNA/LNP

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $2 - $20 (vaccine); $50-500 (therapeutic) | COVID demonstrated extreme scalability |
| **Gross margin** | 80-90% (vaccine scale) | At pandemic scale; smaller indications higher COGS |
| **Scale-up complexity** | Low-Moderate | In vitro transcription (IVT) is cell-free; LNP formulation is the bottleneck |
| **Facility cost** | $100-300M | Cell-free manufacturing; simpler than biologics |
| **Process development timeline** | 12-24 months | Sequence design, modified nucleosides, LNP optimization |
| **Key challenges** | LNP targeting beyond liver (limits non-liver indications), cold chain requirements (-20C to -80C), repeat dosing immunogenicity | Non-hepatic delivery is the key technical frontier |
| **CMO availability** | Growing rapidly | Moderna (in-house), BioNTech (in-house), Catalent, Samsung |
| **Platform advantage** | Same manufacturing process for different sequences | Rapid program iteration; manufacturing does not restart for new targets |

### Oligonucleotide (ASO, siRNA, saRNA)

| Parameter | Typical Range | Notes |
|---|---|---|
| **COGS per dose** | $100 - $2,000 | Driven by synthesis scale and modification chemistry |
| **Gross margin** | 70-85% | Moderate; improving with scale |
| **Scale-up complexity** | Moderate | Solid-phase synthesis is well-established; scale is the challenge |
| **Facility cost** | $100-250M | Oligonucleotide synthesis + purification + formulation |
| **Process development timeline** | 18-30 months | Chemistry optimization, delivery vehicle development, stability |
| **Key challenges** | Delivery to target tissue (GalNAc for liver is solved; CNS, muscle, kidney are harder), off-target effects (sequence-dependent), manufacturing purity at scale | Delivery technology is the primary differentiator |
| **Delivery platforms** | GalNAc conjugate (liver), LNP, intrathecal (CNS), naked (local) | GalNAc-siRNA (Alnylam platform) is the gold standard for liver targets |
| **Key players** | Alnylam, Ionis, Arrowhead, Dicerna (Novo Nordisk) | Each has proprietary chemistry and delivery platform |

## Cross-Modality COGS Comparison

| Modality | COGS/Dose | Typical Price/Dose | Gross Margin | Scale-Up Risk |
|---|---|---|---|---|
| Small molecule | $0.10-5 | $10-500 | 85-95% | Low |
| mAb | $20-200 | $1,000-10,000 | 75-90% | Moderate |
| ADC | $500-3,000 | $10,000-30,000 | 65-80% | High |
| Bispecific | $50-500 | $5,000-20,000 | 70-85% | Moderate-High |
| mRNA/LNP | $2-500 | $20-5,000 | 80-90% | Low-Moderate |
| Oligonucleotide | $100-2,000 | $5,000-50,000 | 70-85% | Moderate |
| Gene therapy (AAV) | $50K-500K | $500K-3.5M | 40-70% | Very High |
| Cell therapy (auto) | $50K-150K | $373K-475K | 30-55% | Very High |
| Cell therapy (allo) | $5K-30K | $100K-300K (est) | 70-85% | High |

## Venture Diligence Manufacturing Questions

For any asset under evaluation, ask:

1. **What is the current manufacturing scale and has it been validated for commercial production?**
2. **What is the projected COGS at commercial scale, and does it support the target pricing?**
3. **Is there a CMO partnership in place, or is the company building in-house capacity?**
4. **What are the critical quality attributes and how mature are the analytical methods?**
5. **Has the FDA inspected the manufacturing facility, and were there any 483 observations?**
6. **What is the backup plan if the primary manufacturing site fails?**
7. **For cell/gene therapy: what is the batch failure rate and how does it trend with scale?**

## Structured Output Format

```
MANUFACTURING ASSESSMENT
==========================
Product: [drug name]
Modality: [modality type]

COGS ANALYSIS:
  Current COGS/dose: [$X]
  Projected commercial COGS/dose: [$Y]
  Target price/dose: [$Z]
  Implied gross margin: [X%]
  Margin viability: [viable/marginal/concerning]

MANUFACTURING READINESS:
  Current scale: [clinical/pilot/commercial]
  Manufacturing partner: [in-house/CMO name]
  Process validation status: [complete/in progress/not started]
  Facility readiness: [approved/under construction/planned]

SCALE-UP RISKS:
  1. [Risk + mitigation]
  2. [Risk + mitigation]
  3. [Risk + mitigation]

MODALITY-SPECIFIC CONSIDERATIONS:
  [2-3 key modality-specific manufacturing points]

OVERALL MANUFACTURING RISK: [Low / Moderate / High / Very High]
```

## Cross-Domain Connections

- **Biotech-venture/cmc-risk-assessor**: Provides modality-specific failure modes and scalability profiles that feed into program-level FMEA risk assessment
- **Biotech-venture/cost-estimator**: COGS benchmarks by modality are critical inputs to development cost models and commercial margin analysis
- **Biotech-venture/trial-design-optimizer**: Manufacturing constraints may limit trial design options — vein-to-vein time for cell therapy, cold chain for mRNA, and vector yield for gene therapy all constrain protocol design
