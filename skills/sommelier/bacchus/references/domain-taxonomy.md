# Sommelier Domain Taxonomy

## Skill Architecture Map

```
skills/
│
└── sommelier/                              Domain: sommelier  |  Maturity: Level 2
    │
    ├── bacchus/                            [orchestrator]  Bacchus — God of the Vine
    │   └── references/
    │       ├── delegation-rules.md         Multi-director routing logic and edge cases
    │       └── domain-taxonomy.md          Full skill architecture map (this file)
    │
    ├── tasting-evaluation/                 [director]  Dept Head — routes evaluation, blind tasting, faults
    │   ├── deductive-method/               [knowledge]  CMS Deductive Grid: Sight → Nose → Palate → Conclusion
    │   │   └── references/
    │   │       └── grid-notation.md        Standard notation format for grid entries
    │   ├── quality-assessment/             [knowledge]  BLIC framework, finish analysis, typicity vs. quality
    │   │   └── references/
    │   │       └── quality-vocabulary.md   Approved descriptors by tier (outstanding → faulty)
    │   ├── fault-diagnosis/                [knowledge]  TCA, brett, VA, reduction, oxidation, heat damage
    │   │   └── references/
    │   │       └── fault-threshold-table.md  Sensory thresholds and fault vs. style decision matrix
    │   └── blind-tasting/                  [action]  Run a systematic blind tasting session
    │       └── references/
    │           └── varietal-clue-map.md    Key structural and aromatic clues by grape and region
    │
    ├── food-pairing/                       [director]  Dept Head — routes all pairing questions
    │   ├── component-rules/                [knowledge]  Acid, fat, salt, sugar, umami, heat, bitter — the 7 variables
    │   │   └── references/
    │   │       └── component-matrix.md     What each food component calls for in wine structure
    │   ├── weight-matching/                [knowledge]  Body, texture, and occasion-weight calibration
    │   │   └── references/
    │   │       └── weight-scale.md         Light → full weight scale for wine and food categories
    │   ├── classic-pairings/               [knowledge]  Canonical regional pairings and why they work structurally
    │   │   └── references/
    │   │       └── pairing-canon.md        50 classic wine-food pairings with structural explanations
    │   └── pairing-advisor/                [action]  Generate pairing recommendations from a dish description
    │
    ├── regions-terroir/                    [director]  Dept Head — routes regional, appellation, terroir questions
    │   ├── old-world-regions/              [knowledge]  France, Italy, Spain, Germany, Portugal, Austria, Greece
    │   │   └── references/
    │   │       ├── france-appellations.md  AOC hierarchy, major regions, key appellations
    │   │       ├── italy-appellations.md   DOC/DOCG structure, 20 regions, key varieties
    │   │       └── spain-germany-etc.md    Remaining Old World appellation systems
    │   ├── new-world-regions/              [knowledge]  USA, Australia, New Zealand, South Africa, Argentina, Chile
    │   │   └── references/
    │   │       └── new-world-appellations.md  AVA / GI systems, key regions, structural profiles
    │   ├── terroir-theory/                 [knowledge]  Soil types, climate classification, aspect, altitude, viticulture
    │   │   └── references/
    │   │       ├── soil-typology.md        Key soil types (limestone, clay, granite, volcanic, alluvial) and structural effects
    │   │       └── climate-classification.md  Winkler heat summation, cool vs. warm vs. hot, maritime vs. continental
    │   └── appellation-law/                [knowledge]  How appellation systems work: EU, US, Australia, comparative
    │
    ├── grape-encyclopedia/                 [director]  Dept Head — routes all variety questions
    │   ├── noble-varieties/                [knowledge]  The 18 CMS canonical varieties — structural fingerprints and regions
    │   │   └── references/
    │   │       └── variety-profiles.md     Canonical Sight/Nose/Palate profile for each noble variety
    │   ├── indigenous-varieties/           [knowledge]  Grillo, Nerello Mascalese, Touriga Nacional, Grüner, Xinomavro, etc.
    │   │   └── references/
    │   │       └── indigenous-index.md     Country-organized index with synonyms and structural notes
    │   └── variety-mapping/                [action]  Map a grape to its canonical regions and structural expectations
    │
    ├── winemaking/                         [director]  Dept Head — routes production, chemistry, process questions
    │   ├── viticulture/                    [knowledge]  Vine training, canopy management, yield, organic/biodynamic
    │   │   └── references/
    │   │       └── viticulture-decisions.md  How farming decisions translate to structural outcomes
    │   ├── vinification/                   [knowledge]  Fermentation types, vessel choice, skin contact, chaptalization, SO2
    │   │   └── references/
    │   │       ├── fermentation-spectrum.md  From conventional to natural, intervention by intervention
    │   │       └── closure-effects.md      Cork vs. screwcap vs. DIAM — oxygen transmission rates, aging implications
    │   ├── elevage/                        [knowledge]  Oak maturation, lees aging, battonage, fining, filtration, blending
    │   │   └── references/
    │   │       └── oak-effects-guide.md    New vs. used oak, toast levels, species (French/American/Slavonian), time
    │   └── natural-wine/                   [knowledge]  Low-intervention spectrum: natural, biodynamic, organic, skin-contact
    │       └── references/
    │           └── flaw-vs-style-guide.md  Where intentional character becomes genuine fault — thresholds with examples
    │
    ├── cellar-service/                     [director]  Dept Head — routes service, glassware, temperature, aging
    │   ├── service-standards/              [knowledge]  CMS service sequence, decanting technique, glassware by style
    │   │   └── references/
    │   │       └── service-checklist.md    Step-by-step restaurant service and home service protocols
    │   ├── temperature-guide/              [knowledge]  Optimal serving temperatures by style, over/under-chilling effects
    │   │   └── references/
    │   │       └── temperature-table.md    Quick reference: 12 wine categories with min/max serving temps
    │   ├── aging-curves/                   [knowledge]  How wines develop over time — peak windows, decline indicators
    │   │   └── references/
    │   │       └── aging-curve-library.md  Canonical aging curves for Bordeaux, Burgundy, Barolo, Riesling, Champagne, etc.
    │   └── cellar-management/              [knowledge]  Building a cellar: proportions, rotation, storage conditions, tracking
    │       └── references/
    │           └── cellar-planning-guide.md  Cellar composition by budget tier, reorder logic, condition monitoring
    │
    ├── wine-market/                        [director]  Dept Head — routes pricing, collecting, investment, trends
    │   ├── fine-wine-economics/            [knowledge]  How fine wine is priced, what drives appreciation, scarcity mechanics
    │   │   └── references/
    │   │       └── valuation-framework.md  Score normalization, vintage spread, appellation tier, provenance premium
    │   ├── auction-strategy/               [knowledge]  Major houses (Christie's, Hart Davis Hart, Acker), buying and selling strategy
    │   │   └── references/
    │   │       └── auction-guide.md        Reserve vs. estimate, buyer's premium math, timing for categories
    │   ├── emerging-regions/               [knowledge]  High-QPR regions gaining critical and market attention
    │   │   └── references/
    │   │       └── emerging-region-tracker.md  Regions indexed by structural quality, price trajectory, and market visibility
    │   └── en-primeur/                     [knowledge]  Bordeaux futures system, Burgundy DRC allocation, Port vintage declarations
    │       └── references/
    │           └── en-primeur-guide.md     When buying en primeur makes financial sense vs. spot market
    │
    └── sommelier-lab/                      [director]  Dept Head — routes experimental, synesthetic, and training questions
        ├── sensory-training/               [knowledge]  How to build a sensory memory: aroma kits, threshold exercises, calibration
        │   └── references/
        │       └── training-protocols.md   CMS-aligned tasting drills, notebook methods, progression milestones
        ├── wine-language/                  [knowledge]  Writing tasting notes: the literary tasting note vs. the clinical grid note
        │   └── references/
        │       └── note-styles.md          Four tasting note registers with annotated examples
        ├── climate-wine/                   [knowledge]  How climate change is reshaping regions, varieties, and vintages
        │   └── references/
        │       └── climate-shift-atlas.md  Region-by-region impact: which are improving, which are threatened
        └── molecular-pairing/              [knowledge]  Flavor compound overlap between wine and food — the science behind great matches
            └── references/
                └── compound-pairings.md    Key aromatic compounds in wine and their food resonances
```

---

## Knowledge Dependencies

Some skills require prior conceptual loading before they deliver full value. These are not hard technical dependencies — they are pedagogical sequencing rules.

```
deductive-method
    └── required before: quality-assessment, blind-tasting, fault-diagnosis
        rationale: quality and fault assessment are interpretive layers on top of raw
        perception. If the grid isn't internalized, the interpreter has no data to work with.

terroir-theory
    └── required before: old-world-regions, new-world-regions, appellation-law
        rationale: appellation law only makes sense when you understand what it is trying
        to protect. A region is not a place on a map; it is a terroir argument encoded
        into law. Load the terroir framework before the geography.

component-rules
    └── required before: weight-matching, classic-pairings, pairing-advisor
        rationale: weight matching is the application of the component framework to
        body and texture. Classic pairings are illustrations of the rules. Without the
        rules, the pairings are just a list of recommendations with no transferable logic.

noble-varieties
    └── required before: blind-tasting, indigenous-varieties
        rationale: the 18 noble varieties are the structural reference points. Indigenous
        varieties are understood in contrast to them ("Xinomavro tastes like Nebbiolo
        crossed with Pinot Noir" is meaningless without the reference points).

viticulture + vinification
    └── required before: elevage, natural-wine
        rationale: élevage decisions only matter in the context of what arrived at the
        winery. Natural wine philosophy is a position on the viticulture-vinification
        spectrum; understanding the spectrum first makes the position meaningful.

service-standards
    └── required before: cellar-management
        rationale: cellar management is downstream of service. Building a cellar without
        knowing how and when wines will be served is inventory management, not sommelier craft.

fine-wine-economics
    └── required before: auction-strategy, en-primeur
        rationale: buying and selling strategy requires a model of value. Without
        understanding what drives fine wine appreciation, auction and futures decisions
        are uninformed speculation.
```

---

## Curriculum Progression

A complete learning path from first-time wine drinker to master-level competency, mapped to specific skills in this domain.

### Beginner — "I like wine but don't know why"

Goal: Build a sensory vocabulary and structural intuition. Be able to describe what's in the glass and make basic pairing decisions.

1. `deductive-method` — Learn the grid. Start with Sight (color depth, clarity, viscosity). Do this for every glass for 30 days.
2. `component-rules` — Understand the 4 structural pillars: acidity, tannin, body, sweetness. Taste wines specifically to find each one.
3. `noble-varieties` — Learn 6 of the 18 to start: Chardonnay, Sauvignon Blanc, Riesling, Pinot Noir, Cabernet Sauvignon, Syrah. Know what to expect in the glass.
4. `weight-matching` — Make basic pairing decisions using body alone. Light wine → light food. Build from there.
5. `temperature-guide` — Serve wine correctly. This single skill improves every bottle immediately.

**Milestone:** Can describe a wine's structure without help and suggest a food pairing with a reason.

### Intermediate — "I want to drink more intentionally"

Goal: Understand terroir, recognize regional typicity, begin building a meaningful cellar.

6. `terroir-theory` — Understand what soil, climate, and aspect do to wine structure. Read a label as a terroir argument.
7. `old-world-regions` — France first (Burgundy, Bordeaux, Rhône, Alsace, Loire, Champagne). Then Italy (Barolo, Brunello, Chianti, Amarone, Soave). Build mental maps.
8. `classic-pairings` — Study the canonical pairings (Chablis/oysters, Sancerre/goat cheese, Barolo/truffle and braised meat, Sauternes/foie gras) and understand the structural logic behind each.
9. `quality-assessment` — BLIC: balance, length, intensity, complexity. Begin distinguishing good from great.
10. `aging-curves` — Learn which wines age and why. Understand what acidity and tannin do over time.
11. `cellar-management` — Build a modest cellar with intentional proportions. Track what you own and when to open it.

**Milestone:** Can taste a wine and name the likely region and variety with some accuracy. Can build a dinner wine list from scratch.

### Advanced — "I'm studying seriously or work in wine professionally"

Goal: Blind tasting competency, full regional depth, winemaking literacy, market awareness.

12. `blind-tasting` — Systematic deductive practice. Use varietal-clue-map.md. Taste the same grape from 5 regions in the same session.
13. `fault-diagnosis` — Identify TCA, brett, VA, reduction, and oxidation in the glass. Understand thresholds.
14. `new-world-regions` — California, Australia, New Zealand, South Africa, Argentina, Chile — structural profiles and how they compare to Old World equivalents.
15. `indigenous-varieties` — Expand beyond the 18. Grüner Veltliner, Touriga Nacional, Nebbiolo-family, Grenache/Garnacha variations, Assyrtiko, Xinomavro, Nero d'Avola.
16. `vinification` — Full production literacy: fermentation vessel choices, whole-cluster, carbonic maceration, extended maceration, orange wine process, sparkling method (traditional vs. tank vs. pétillant naturel).
17. `elevage` — Oak regime decisions: new vs. neutral, toast level, time in barrel, lees contact. Understand what each does to the palate.
18. `service-standards` — Professional service sequence. Decanting technique for old wines (sediment management). Champagne service. Restaurant-level presentation.
19. `fine-wine-economics` — Understand what makes a wine worth collecting. Score systems, vintage variation, critic influence.

**Milestone:** Passes WSET Diploma or CMS Advanced. Can run a wine program for a restaurant.

### Master — "Building toward MW or MS level"

Goal: Full theoretical depth, exam-ready, able to teach and evaluate with authority.

20. `appellation-law` — Full legal frameworks: EU wine law, AOC system, Italian DOC/DOCG, German Prädikat system, American AVA, Australian GI. Understand what each system protects and why.
21. `terroir-theory` (deep) — Soil profiles at the parcel level: Kimmeridgian vs. Portlandian in Chablis, Comblanchien limestone in Côte de Nuits, Pondalowie basalt in Heathcote. Geological time as a wine variable.
22. `climate-wine` — Climate change impacts by region. Which regions are gaining, which are threatened. How vintage character is shifting.
23. `natural-wine` — Full spectrum literacy: organic vs. biodynamic vs. natural vs. conventional. Flaw vs. style distinction at the threshold level.
24. `sensory-training` — Calibration protocols. Aroma kit work. Threshold detection. Building the sensory memory that blind tasting requires.
25. `wine-language` — Writing tasting notes at a high level. The literary tasting note (Parker, Robinson) vs. the clinical grid note (CMS, WSET). Know both modes.
26. `molecular-pairing` — Flavor compound theory: why certain pairings work at a chemical level (umami amplification, ester bridging, phenolic resonance). Useful for creative pairing work and MS theory sections.
27. `auction-strategy` + `en-primeur` — Investment and collecting literacy. Useful for client advisory and personal cellar strategy.

**Milestone:** MW or MS qualification. Able to conduct a masterclass, write a rigorous tasting note, advise on cellar investment, and teach any topic in this tree.

---

## Cross-Domain Connections

The sommelier domain does not live in isolation. Several wine topics connect deeply to other skill domains in this library.

### → investing (archon)

Fine wine as an alternative asset class has a meaningful overlap with investment logic:
- Collectible wine appreciation follows scarcity economics (tiny Burgundy parcels, allocated production)
- Liv-ex fine wine indices behave like commodities — mean-reversion in off-vintages, momentum in iconic years
- Auction strategy (timing, reserve setting, provenance premium) uses the same analytical frame as event-driven investing
- En primeur (Bordeaux futures) is a structured product with carry, storage costs, and vintage risk baked in

**Handoff rule:** When a wine question becomes primarily about portfolio allocation, risk-adjusted return, or capital preservation, route to `archon`. Return with wine-specific context (provenance, condition, auction timing) that financial frameworks alone cannot supply.

### → worldbuilding (worldbuilding-orchestrator)

Fictional wine cultures require both viticultural plausibility and narrative coherence:
- Invented appellations need terroir logic (climate, soil, latitude analogue) to feel real
- Fantasy fermented beverages need a production mechanism grounded in real biochemistry
- Wine ceremony, culture, and symbolism need to connect to the fictional society's values and history
- The sensory language of wine writing translates directly to evocative worldbuilding description

**Handoff rule:** When a user is building a fictional world and wine is a cultural or narrative element, route to `worldbuilding-orchestrator`. Bacchus can supply the viticultural and sensory substrate; worldbuilding-orchestrator shapes the cultural and narrative architecture.

### → writing (prose-orchestrator)

Wine writing is a distinct literary form with its own conventions:
- The tasting note as prose: Parker's baroque richness vs. Jancis Robinson's precision vs. the New Wave tasting note
- Wine criticism as persuasion: how critics build authority, deploy metaphor, manage subjectivity
- Label copy and wine marketing: compression, voice, the problem of making a commodity feel unique
- Wine memoir and narrative non-fiction (the genre of Kermit Lynch, Terry Theise, Matt Kramer)

**Handoff rule:** When the question is primarily about the craft of writing about wine — not about the wine itself — route to `prose-orchestrator` or `rhetoric`. Bacchus supplies the content knowledge; the writing domain supplies the craft.

### → data-science (data-science-orchestrator)

Wine science and sensory science overlap with quantitative analysis:
- Gas chromatography / mass spectrometry of aromatic compounds (esters, terpenes, thiols, pyrazines)
- Hedonic regression models for score-price relationships (what variables predict critic scores?)
- Climate data analysis: temperature anomalies by vintage year, growing degree day calculations
- Sensory panel data: principal component analysis of tasting note vocabulary
- Wine fraud detection: isotope ratio analysis, spectral fingerprinting

**Handoff rule:** When a wine question requires quantitative analysis, statistical modeling, or computational methods, route to `data-science-orchestrator`. Bacchus supplies the wine domain framing; data-science supplies the analytical machinery.

### → research (spelunker)

For deep factual questions with disputed or uncertain answers:
- Contested appellation history (the Franciacorta vs. Prosecco marketing claims)
- Emerging scientific consensus on terroir transmission (can vines really uptake soil minerals into flavor compounds?)
- Producer histories with conflicting accounts
- Regulatory changes in appellation law

**Handoff rule:** When a wine question requires primary source verification, multi-source triangulation, or navigating contested claims, route to `spelunker`. The confidence framework from the research domain applies to wine knowledge as much as any other field.
