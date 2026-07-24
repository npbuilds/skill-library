# Modality Maturity Map — Extended Reference

A 2026 point-in-time snapshot of where each therapeutic modality sits on its S-curve, the delivery wall that binds it, and the platform-level fixes that convert (or fail to convert) a class. Serves the **modality-lifecycle** SKILL (`skills/biotech-venture/modality-trajectory/modality-lifecycle/`) as its most perishable data layer — extracted here so stage assignments can be refreshed without touching the skill logic.

**Provenance.** Every table below is tagged **`int`** — internal consensus estimate drawn from the parent skill's own quick-reference prose. None carry external citations; treat stage labels, drug lists, and multipliers as the skill's editorial read, not verified benchmarks. Tags used: **`int`** = internal consensus estimate; **`ext✓`** = externally verified with a real citation (none in this doc); **`statutory`** = stable legal/regulatory constant (none in this doc).

> **Perishability warning.** This is the fastest-staling data in the modality-trajectory pillar. Stages shift on single readouts, and classes can regress — e.g. AAV gene therapy is marked "Established (regressing)" here after a marquee safety reversal. Re-audit at least every 6–12 months, or immediately after any pivotal approval, clinical hold, or platform-defining readout.

## Master maturity map `int`

Columns preserved from source: Modality | Stage (2026) | Binding delivery bottleneck | What unlocks next stage | Representative drugs / companies.

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
| CAR-T (autologous) | Established | COGS $100–220K, vein-to-vein, CRS/ICANS | In-vivo or allogeneic to collapse logistics | Yescarta, Kymriah, Carvykti, Abecma / Gilead, Novartis, J&J-Legend, BMS |
| TCR-T | Proving | HLA restriction, solid-tumor antigen | Broader HLA coverage | Tecelra (afami-cel) / Adaptimmune |
| TIL | Proving | Manufacturing, lymphodepletion intensity | Streamlined manufacturing | Amtagvi (lifileucel) / Iovance |
| CAR-NK | Emerging→Proving | Persistence | Engineered persistence | NKX019 / Nkarta |
| Allogeneic cell | Emerging | Persistence + host rejection | Multiplexed HLA editing | cema-cel (ALLO-501A) / Allogene |
| In-vivo CAR | Emerging (steepest) | T-cell-tropic LNP / retargeted vector | Reproducible cell-type-specific tropism in humans | CPTX2309 / Capstan-AbbVie, Umoja, Interius, CREATE |
| TPD (PROTAC / glue) | Proving→Established | Oral PK of bifunctionals, E3-ligase diversity | Expanded usable E3 ligases | vepdegestrant (VEPPANU) / Arvinas-Pfizer, Monte Rosa, C4, Kymera |
| Radioligand therapy | Established | Isotope supply (Ac-225), site infrastructure | Domestic isotope production + more radiopharmacies | Pluvicto, Lutathera / Novartis, Lilly, BMS-RayzeBio |
| Oral peptides / oral biologics | Proving (steep) | Gut absorption often <2% F | Permeation chemistry lifting F to double digits | enlicitide (MK-0616), oral sema, orforglipron / Merck, Novo, Lilly |

### Stage boundary tests `int`

| Stage | Test |
|---|---|
| Emerging | FIH to early Ph1; proof-of-mechanism not durable/safe at scale; often one asset |
| Proving | Ph1/2 signals replicating; ≤1 approval; platform risk live |
| Established | Multiple approvals; mechanism de-risked; scaling/access is the work |
| Mature | Dozens-to-hundreds of approvals; commoditized; innovation incremental or in delivery |

## Delivery-wall lookup `int`

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

## Platform-fix registry `int`

The fix — not the underlying biology — is what converts a class. Status ladder: **LANDED** (validated approval) → **LANDING** (pivotal in progress) → **PARTIAL** (NHP/Ph1 proof only) → **NOT LANDED** (wall still standing).

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

### Arc-direction flags `int`

- **Regression** — marquee safety reversal. AAV: Elevidys ≥3 liver-injury deaths + FDA dosing pause (2025); Sarepta pivoted to siRNA. Apply regression_penalty; borrow a worse matrix.
- **Maturity/commoditization** — class competes on route + cadence, not efficacy. SC nivolumab/pembrolizumab (Keytruda Qlex Sept 2025), oral GLP-1 orforglipron, oral PCSK9 enlicitide, twice-yearly inclisiran. Mature ≠ attractive entry.

## Source Vintage & Staleness

- **Vintage:** 2026 point-in-time snapshot, extracted from the modality-lifecycle quick-reference.
- **Half-life of the data:** short. Stage labels are the most volatile — a single pivotal readout can move a modality up a stage, and a safety reversal can move it down (AAV is the live example, marked "Established (regressing)").
- **What stales fastest:** the Stage column and the Platform-fix Status column (LANDED/LANDING/PARTIAL/NOT LANDED transitions on individual approvals and holds). The delivery-wall physics stale slowest but still shift as new conjugation/LNP chemistry validates.
- **Refresh cadence:** re-audit every 6–12 months, and immediately on any class-defining approval, clinical hold, or platform readout. Re-verify representative drug/company lists at the same cadence — deal ownership and brand names change.
- **Provenance caveat:** all figures are internal consensus (`int`); none are externally verified. Do not cite downstream as sourced benchmarks without independent confirmation.

**Usage note.** This doc serves the **modality-lifecycle** SKILL (`skills/biotech-venture/modality-trajectory/modality-lifecycle/SKILL.md`) as its perishable maturity-map data layer. The scoring primitive `P(modality deliverable) = base_modality_LOA_proxy × delivery_state_multiplier × regression_penalty`, the LOA base proxies, and the multiplier ranges remain in the parent skill's quick-reference (`references/quick-reference.md`) — apply the stage, delivery-wall, and platform-fix reads here against that formula. Cross-reference the parent quick-reference for stage boundary tests and the steepest-adoption-curve investor read.
