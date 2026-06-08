# Modality Lifecycle — Quick Reference

## Input

| Parameter | Source | Required? |
|---|---|---|
| Modality | User | Yes |
| Target tissue / compartment | User | Recommended |
| Specific asset / company | User | Optional |
| Indication | User | Optional |
| Use mode: learn vs screen | User | Optional (default: screen) |

## Master maturity map (modality | stage | delivery bottleneck | what unlocks next | representative drugs / companies)

| Modality | Stage (2026) | Binding delivery bottleneck | What unlocks next stage | Representative drugs / companies |
|---|---|---|---|---|
| Small molecules | Mature | Undruggable targets, selectivity, resistance | Induced-proximity + covalent chemistry expanding target universe | daraxonrasib (RMC-6236), divarasib, sotorasib / Revolution Medicines, Roche, Amgen |
| Monoclonal antibodies | Mature | Solid/cold-tumor penetration | Migration into bispecific/ADC formats | pembrolizumab, dupilumab / Merck, Regeneron, Roche |
| Peptides / macrocycles | Mature | Oral bioavailability, proteolytic stability | Permeation-enhancer formulations | semaglutide, tirzepatide / Novo, Lilly |
| Bispecifics / multispecifics | Established→ | CRS/safety, trispecific manufacturability | Tolerable added valency | linvoseltamab (Lynozyfic), JNJ-5322 (tri), IPH6501 (tetra) / Regeneron, J&J, Innate |
| ADCs | Established | Payload diversity, ILD/tox, linker stability | Beyond-topo-I payloads, polysarcosine linkers, bispecific ADCs | T-DXd (Enhertu), dato-DXd (Datroway), Teliso-V (Emrelis) / AstraZeneca-Daiichi, AbbVie |
| ASO | Established | Extrahepatic + CNS delivery | C16/lipophilic + intrathecal conjugates | nusinersen, tofersen, olezarsen / Ionis, Biogen |
| siRNA | Established | Beyond-liver delivery | Antibody-siRNA (TfR/muscle), C16 (CNS/eye/lung) | inclisiran (Leqvio), vutrisiran (Amvuttra) / Alnylam, Novartis, Avidity, Dyne |
| mRNA vaccines | Established | Reactogenicity, thermostability | Incremental | Comirnaty, Spikevax / Pfizer-BioNTech, Moderna |
| mRNA therapeutics | Proving | Repeat-dose tolerability, non-liver LNP | Extrahepatic LNP + tolerable redosing | mRNA-4157/V940 / Moderna, BioNTech |
| saRNA | Emerging→Proving | Innate sensing of replicon | Engineered replicons evading RIG-I/PKR | ARCT-154 (Kostaive) / Arcturus-CSL, Replicate |
| AAV gene therapy | Established (regressing) | Immunogenicity, no redosing, liver tox | Low-seroprevalence capsids + validated redosing | Elevidys, Hemgenix, Zolgensma / Sarepta, CSL, Novartis |
| Lentiviral | Established (vector layer) | Cost, integration safety | Retargeted 4th-gen for in-vivo CAR | Casgevy mfg, Lenmeldy, Tecelra / Vertex, Orchard, Adaptimmune |
| Base editing | Proving | In-vivo delivery still LNP→liver | Extrahepatic editing | BEAM-302, VERVE-102, BEAM-101 / Beam, Verve/Lilly |
| Prime editing | Emerging | Editor payload size/delivery | Compact deliverable editor | PM359 (CGD) / Prime Medicine |
| CRISPR nuclease — in vivo | Proving | LNP tropism beyond liver | Extrahepatic LNP | lonvo-z (NTLA-2002), NTLA-2001 / Intellia |
| CRISPR nuclease — ex vivo | Established | Conditioning, manufacturing, price (~$2.2M) | Non-myeloablative conditioning | Casgevy (exa-cel) / Vertex-CRISPR |
| CAR-T (autologous) | Established | COGS $100-220K, vein-to-vein, CRS/ICANS | In-vivo or allogeneic to collapse logistics | Yescarta, Kymriah, Carvykti, Abecma / Gilead, Novartis, J&J-Legend, BMS |
| TCR-T | Proving | HLA restriction, solid-tumor antigen | Broader HLA coverage | Tecelra (afami-cel) / Adaptimmune |
| TIL | Proving | Manufacturing, lymphodepletion intensity | Streamlined manufacturing | Amtagvi (lifileucel) / Iovance |
| CAR-NK | Emerging→Proving | Persistence | Engineered persistence | NKX019 / Nkarta |
| Allogeneic cell | Emerging | Persistence + host rejection | Multiplexed HLA editing | cema-cel (ALLO-501A) / Allogene |
| In-vivo CAR | Emerging (steepest) | T-cell-tropic LNP / retargeted vector | Reproducible cell-type-specific tropism in humans | CPTX2309 / Capstan-AbbVie, Umoja, Interius, CREATE |
| TPD (PROTAC / glue) | Proving→Established | Oral PK of bifunctionals, E3-ligase diversity | Expanded usable E3 ligases | vepdegestrant (VEPPANU) / Arvinas-Pfizer, Monte Rosa, C4, Kymera |
| Radioligand therapy | Established | Isotope supply (Ac-225), site infrastructure | Domestic isotope production + more radiopharmacies | Pluvicto, Lutathera / Novartis, Lilly, BMS-RayzeBio |
| Oral peptides / oral biologics | Proving (steep) | Gut absorption often <2% F | Permeation chemistry lifting F to double digits | enlicitide (MK-0616), oral sema, orforglipron / Merck, Novo, Lilly |

## Stage boundary tests

| Stage | Test |
|---|---|
| Emerging | FIH to early Ph1; proof-of-mechanism not durable/safe at scale; often one asset |
| Proving | Ph1/2 signals replicating; ≤1 approval; platform risk live |
| Established | Multiple approvals; mechanism de-risked; scaling/access is the work |
| Mature | Dozens-to-hundreds of approvals; commoditized; innovation incremental or in delivery |

## Delivery-wall lookup

| Modality | The delivery wall |
|---|---|
| siRNA / ASO | Beyond liver — CNS, muscle, lung, immune cells |
| Base/prime/CRISPR in vivo | LNPs go to liver; everything else is hard |
| In-vivo CAR | T-cell- (or HSC/NK-) tropic LNP / retargeted vector |
| AAV | Pre-existing immunity, no redosing, capsid de-targeting from liver |
| mRNA therapeutics | Repeat-dose tolerability; extrahepatic LNP |
| Oral peptides/biologics | Gut proteolysis + epithelial permeability (<2% F) |
| Radioligand | Isotope supply (Ac-225) + site infrastructure |
| Cell therapies | "Delivery" = manufacturing logistics + persistence |

## Platform-fix registry (the fix, not biology, converts the class)

| Fix | Converts | Status |
|---|---|---|
| GalNAc conjugation | siRNA/ASO → liver | LANDED (inclisiran, vutrisiran) |
| Covalent switch-II (2013 Shokat) | KRAS druggability | LANDED (sotorasib 2021) |
| Tri-complex / RAS(ON) | pan-RAS beyond G12C | LANDING (daraxonrasib Ph3/BTD; ~8.8mo mPFS 2L PDAC) |
| E3-ligase recruitment | targeted degradation | LANDED (vepdegestrant 2025, +2.9mo PFS VERITAC-2) |
| Site-specific linker + DXd payload | ADC redemption | LANDED (T-DXd, Datroway, Emrelis) |
| T-cell-tropic LNP (tLNP) | in-vivo CAR | PARTIAL (CPTX2309 Ph1 Jun 2025; NHP data; AbbVie ~$2.1B) |
| C16 / antibody-siRNA conjugate | extrahepatic RNAi | PARTIAL (muscle AOCs; SCAD/intrathecal RAG-17 NCT06556394) |
| Low-seroprevalence capsid | AAV redosing | NOT LANDED (class regressed post-Elevidys) |
| Multiplexed HLA editing | allogeneic persistence/rejection | NOT LANDED |

## Arc-direction flags

- **Regression** — marquee safety reversal. AAV: Elevidys ≥3 liver-injury deaths + FDA dosing pause (2025); Sarepta pivoted to siRNA. Apply regression_penalty; borrow a worse matrix.
- **Maturity/commoditization** — class competes on route + cadence, not efficacy. SC nivolumab/pembrolizumab (Keytruda Qlex Sept 2025), oral GLP-1 orforglipron, oral PCSK9 enlicitide, twice-yearly inclisiran. Mature ≠ attractive entry.

## Scoring primitive — P(modality deliverable)

```
P(modality deliverable) = base_modality_LOA_proxy × delivery_state_multiplier × regression_penalty

base proxies (LOA):
  vaccines ~9.7% | biologics ~9.1% > small molecules ~5.7% | CGT ~5.3% bimodal
  (CAR-T / AAV ~13.6% in validated indications)

delivery_state_multiplier:
  LANDED for this tissue        = 1.0
  PARTIAL (NHP/Ph1 proof only)  = 0.6-0.8
  NOT LANDED (wall standing)    = 0.3-0.5
  zero-clinical-history class   = borrow nearest validated class matrix, never de novo optimism

regression_penalty:
  active safety reversal        = ×0.5-0.7
  none                          = ×1.0
```

Platform risk concentrates in Phase 1→2. Down-weight "AI-discovered" novelty unless the platform has independent wet-lab + clinical validation.

## 2026 steepest adoption curves (for the investor read)

1. In-vivo CAR (autoimmune-first) — concept → clinic → ~$2.1B exit in ~18mo
2. Oral incretins / oral biologics — orforglipron 11.2% wt loss (ATTAIN-1, n=3,127); enlicitide both CORALreef endpoints
3. In-vivo gene editing (base + CRISPR) — lonvo-z positive Ph3 HAELO (global first); BEAM-302, VERVE-102 (LDL ~50%)
4. Targeted protein degradation — first PROTAC approval (vepdegestrant)
5. Radioligand therapy — Pluvicto+Lutathera $2.8B 2025; industrialization curve, gated by Ac-225

**Cooling:** AAV (safety overhang, no redosing); allogeneic cells (unsolved persistence/rejection).

## Error handling

| Scenario | Response |
|---|---|
| Modality not on map | Place by analogy to nearest class; flag zero-history; borrow matrix + novelty haircuts |
| Approval but class regressing | Stage = approvals shipped; apply regression_penalty separately |
| Delivery claim only preprint/NHP | Mark PARTIAL; name the human Ph1 trial that closes it |
| "AI-discovered" framing | Down-weight unless platform has independent wet-lab + clinical validation |
| Tissue not specified | Default validated tissue (usually liver); extrahepatic = separate harder state |
| One asset = whole class | Treat as Emerging regardless of hype |
