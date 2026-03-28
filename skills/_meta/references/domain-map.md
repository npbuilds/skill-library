# Domain Map

Current hierarchy of the skill library. Regenerate this file when the structure changes.

Last updated: 2026-03-28

```
skills/
│
├── _meta/                              [observer]  Meta Observer
│   └── references/
│       ├── domain-map.md               (this file)
│       └── maturity-model.md
│
├── infrastructure/                     Domain: infrastructure  |  Maturity: Level 4
│   ├── infrastructure-orchestrator/    [orchestrator]  The Architect — coordinates lifecycle ops
│   │   └── references/
│   │       └── workflow-patterns.md    Common multi-skill orchestration patterns
│   ├── skill-registry/                 [action]  Manage the skill catalog
│   ├── skill-health/                   [action]  Quality and health checks
│   ├── skill-dashboard/                [action]  Visual reports and ratings
│   ├── skill-scaffold/                 [action]  Create new skills from templates
│   ├── skill-test/                     [action]  Structural and behavioral testing
│   ├── skill-analyze/                  [action]  API-powered skill analysis
│   ├── skill-fork/                     [action]  Decompose skills into children
│   ├── skill-network/                  [action]  Dependency graph visualization
│   └── skill-export/                   [action]  Package skills for sharing
│
├── design/                             Domain: design  |  Maturity: Level 5
│   ├── design-orchestrator/            [orchestrator]  Creative Director
│   │   ├── agents/                     6 specialist agents
│   │   └── references/
│   │
│   ├── visual-communication/           [director]  Dept Head — routes visual design questions
│   │   ├── color-theory/               [knowledge]  Palettes, harmony, contrast, accessibility
│   │   ├── design-principles/          [knowledge]  Contrast, alignment, proximity, Gestalt
│   │   └── visual-perception/          [knowledge]  Attention, readability, visual weight
│   │
│   ├── typography/                     [director]  Dept Head — routes type questions
│   │   ├── type-fundamentals/          [knowledge]  Anatomy, classification, history
│   │   ├── type-pairing/              [knowledge]  Combination logic, contrast, harmony
│   │   └── responsive-type/           [knowledge]  Fluid scales, viewport adaptation
│   │
│   └── brand-identity/                [director]  Dept Head — routes brand questions
│       ├── brand-foundations/          [knowledge]  Positioning, values, audience
│       ├── visual-identity/           [knowledge]  Logo, color system, visual language
│       └── brand-voice/               [knowledge]  Tone, style, verbal identity
│
├── data-science/                       Domain: data-science  |  Maturity: Level 5
│   ├── data-science-orchestrator/      [orchestrator]  The Analyst — routes analytical questions
│   │   └── references/
│   │       ├── delegation-rules.md     Subdomain routing logic
│   │       └── domain-taxonomy.md      Full subfield map
│   │
│   ├── data-wrangling/                [director]  Dept Head — routes data preparation questions
│   │   ├── data-cleaning/             [knowledge]  Missing values, outliers, dedup, validation
│   │   │   └── references/
│   │   │       └── imputation-guide.md
│   │   └── feature-engineering/       [knowledge]  Encoding, transforms, feature creation/selection
│   │       └── references/
│   │           └── encoding-catalog.md
│   │
│   ├── statistical-analysis/          [director]  Dept Head — routes inference questions
│   │   ├── statistical-testing/       [knowledge]  Hypothesis tests, power, multiple comparisons
│   │   │   └── references/
│   │   │       └── test-selection-flowchart.md
│   │   ├── causal-inference/          [knowledge]  Treatment effects, quasi-experiments, identification
│   │   │   └── references/
│   │   │       └── method-comparison.md
│   │   └── biostatistics/             [knowledge]  Survival, clinical trials, meta-analysis, regulatory
│   │       └── references/
│   │           ├── survival-methods.md
│   │           └── regulatory-standards.md
│   │
│   ├── modeling/                      [director]  Dept Head — routes prediction questions
│   │   ├── model-evaluation/          [knowledge]  Metrics, validation, comparison, calibration
│   │   │   └── references/
│   │   │       └── metrics-catalog.md
│   │   └── time-series/               [knowledge]  Forecasting, seasonality, temporal modeling
│   │       └── references/
│   │           └── model-selection-guide.md
│   │
│   ├── visualization/                 [subdomain — no director yet]
│   │   └── chart-selection/           [knowledge]  Chart types, design principles, accessibility
│   │       └── references/
│   │           └── chart-decision-matrix.md
│   │
│   ├── ml-engineering/                [subdomain — no director yet]
│   │   └── drift-detection/           [knowledge]  Production monitoring, drift types, retraining
│   │       └── references/
│   │           └── detection-methods.md
│   │
│   └── frontier/                      [subdomain — no director yet]
│       └── responsible-ai/            [knowledge]  Fairness metrics, bias, governance, model cards
│           └── references/
│               └── fairness-metrics.md
│
├── worldbuilding/                      Domain: worldbuilding  |  Maturity: Level 3
│   ├── worldbuilding-orchestrator/     [orchestrator]  The Demiurge — coordinates world creation
│   │   └── references/
│   │       └── build-sequences.md      Canonical build orders
│   ├── world-bible/                    [knowledge]  Axioms, constraints, revelation architecture
│   │   └── references/
│   │       ├── world-axioms.md
│   │       ├── revelation-layers.md
│   │       └── faction-conflict-web.md
│   ├── lore-writer/                    [action]  In-universe artifact generation
│   │   └── references/
│   │       ├── voice-registry.md
│   │       └── artifact-format.md
│   ├── naming-system/                  [knowledge]  Phonetic naming for cultures
│   │   └── references/
│   │       └── culture-sound-palettes.md
│   ├── geography-ecology/              [knowledge]  Terrain, climate, biomes, resource distribution
│   ├── cultures-societies/             [knowledge]  Social structures, governance, economy, religion
│   └── magic-systems/                  [knowledge]  Fantasy system design methodology
│
├── writing/                               Domain: writing  |  Maturity: Level 3
│   ├── prose-orchestrator/               [orchestrator]  The Editor's Desk — routes writing tasks
│   ├── prose-writer/                     [action]  Draft prose from a brief — voice-aware, form-aware
│   │
│   ├── sentence-craft/                   [director]  Routes line-level prose questions
│   │   ├── prose-rhythm/                 [knowledge]  Sentence length, cadence, the music of prose
│   │   │   └── references/
│   │   │       └── rhythm-diagnostics.md  Step-by-step rhythm diagnosis protocol
│   │   ├── diction/                      [knowledge]  Word choice, precision, register, connotation
│   │   │   └── references/
│   │   │       └── diction-checklists.md  Revision-ready checklists by problem type
│   │   └── syntax-patterns/              [knowledge]  Cumulative, periodic, balanced, fragment patterns
│   │       └── references/
│   │           └── syntax-exercises.md    Practice exercises by pattern type
│   │
│   ├── narrative-craft/                  [director]  Routes scene, structure, pacing, dialogue, POV
│   │   ├── narrative-arc/                [knowledge]  Story structure — three-act, kishotenketsu, Truby, Cron, Coyne
│   │   ├── scene-craft/                  [knowledge]  Scene as unit of change, enter late/leave early
│   │   ├── pacing/                       [knowledge]  Narrative tempo — compression, expansion, Hitchcock's bomb
│   │   ├── dialogue/                     [knowledge]  Subtext, attribution, distinct character voices
│   │   ├── point-of-view/               [knowledge]  Psychic distance, free indirect discourse, unreliable narration
│   │   └── concrete-detail/              [knowledge]  Objective correlative, telling detail, show vs tell
│   │
│   ├── rhetoric/                         [director]  Routes persuasion, argument, devices, essay forms
│   │   ├── rhetorical-appeals/           [knowledge]  Ethos, pathos, logos, kairos
│   │   ├── argument-structure/           [knowledge]  Toulmin, Rogerian, classical, the volta/turn
│   │   ├── rhetorical-devices/           [knowledge]  Anaphora, tricolon, antithesis, chiasmus, asyndeton
│   │   └── essay-forms/                  [knowledge]  Personal, argumentative, lyric, braided, hermit crab
│   │
│   └── revision-craft/                   [director]  Routes editing passes and style analysis
│       ├── prose-editor/                 [action]  Three-pass editing — structural, line, copy
│       └── style-analyzer/               [action]  Prose style measurement and characterization
│
├── research/                            Domain: research  |  Maturity: Level 3
│   ├── spelunker/                     [orchestrator]  The Deep Researcher — epistemic rigor
│   │   └── references/
│   │       ├── confidence-framework.md  5-tier confidence labeling system
│   │       └── domain-routing.md        Tool chain selection by domain
│   ├── claim-decomposer/              [action]  Split complex questions into atomic claims
│   │   └── references/
│   │       └── decomposition-patterns.md  Common question structures
│   ├── source-triangulator/           [action]  Multi-source verification engine
│   │   └── references/
│   │       └── source-evaluation.md    Source quality assessment framework
│   └── evidence-synthesizer/          [action]  Research brief assembly with confidence tags
│       └── references/
│           └── synthesis-templates.md  Output format templates
│
└── game-theory/                        Domain: game-theory  |  Maturity: Level 5
    ├── game-theory-orchestrator/       [orchestrator]  The Strategist — formalizes and routes
    │   └── references/
    │       ├── delegation-rules.md     Subdomain routing logic
    │       └── domain-taxonomy.md      Full subfield map with sources
    │
    ├── strategic-foundations/           [director]  Routes classical, cooperative, and applied analysis
    │   ├── classical-games/            [knowledge]  Nash, extensive form, refinements, canonical games
    │   ├── cooperative-games/          [knowledge]  Shapley, core, bargaining, matching, fair division
    │   └── game-solver/                [action]  Formalize situations → find equilibria → interpret
    │
    ├── mechanism-design/               [director]  Routes auctions, markets, voting, incentives
    │   ├── auction-theory/            [knowledge]  Formats, revenue equivalence, optimal auctions
    │   ├── matching-markets/          [knowledge]  DA, TTC, market design, real-world deployments
    │   ├── social-choice/             [knowledge]  Arrow, Gibbard-Satterthwaite, voting rules
    │   └── mechanism-designer/        [action]  Design incentive-compatible mechanisms
    │
    ├── evolutionary-dynamics/         [director]  Routes ESS, replicator dynamics, population games
    │   ├── evolutionary-games/        [knowledge]  ESS, hawk-dove, cooperation evolution
    │   ├── population-dynamics/       [knowledge]  Replicator equations, phase portraits, stochastic
    │   └── evo-simulator/             [action]  Simulate evolutionary dynamics computationally
    │
    ├── information-economics/         [director]  Routes signaling, screening, persuasion, disclosure
    │   ├── signaling-screening/       [knowledge]  Spence signaling, adverse selection, moral hazard
    │   ├── bayesian-persuasion/       [knowledge]  Kamenica-Gentzkow, cheap talk, information design
    │   └── info-designer/             [action]  Design optimal information disclosure policies
    │
    └── computational-strategy/        [director]  Routes algorithmic GT, behavioral GT, learning
        ├── algorithmic-game-theory/   [knowledge]  PPAD, price of anarchy, congestion games
        ├── behavioral-game-theory/    [knowledge]  Level-k, QRE, social preferences, experimental
        └── learning-in-games/         [knowledge]  Fictitious play, no-regret, MARL, self-play

├── sommelier/                          Domain: sommelier  |  Maturity: Level 4
│   ├── bacchus/                        [orchestrator]  Bacchus — God of the Vine
│   │   └── references/
│   │       ├── delegation-rules.md     Multi-director routing, edge cases, Learn block protocol
│   │       └── domain-taxonomy.md      Full skill tree, knowledge dependencies, curriculum progression
│   │
│   ├── tasting-evaluation/             [director]  Routes tasting, fault, and quality questions
│   │   ├── deductive-method/           [knowledge]  CMS Deductive Grid — Sight→Nose→Palate→Conclusion
│   │   │   └── references/
│   │   │       └── deductive-grid-schema.md  Structured decision tree, diagnostic implications
│   │   ├── fault-diagnosis/            [knowledge]  17+ faults — compounds, thresholds, flaw vs fault
│   │   ├── quality-assessment/         [knowledge]  BLIC framework, scoring systems, readiness
│   │   └── aroma-lexicon/              [knowledge]  Noble's Aroma Wheel — 3-tier, 119 terms
│   │
│   ├── regions-terroir/                [director]  Routes geography, terroir science, appellation law
│   │   ├── old-world-atlas/            [knowledge]  France, Italy, Spain, Germany, Portugal, Austria, Greece, Georgia
│   │   ├── new-world-atlas/            [knowledge]  USA, Australia, NZ, South Africa, Argentina, Chile
│   │   ├── terroir-science/            [knowledge]  Soil types, Winkler/Huglin indices, mesoclimate
│   │   └── appellation-law/            [knowledge]  AOC/DOC/AVA/GI systems, classification hierarchies
│   │
│   ├── grape-encyclopedia/             [director]  Routes variety identification and expression questions
│   │   ├── noble-grapes/               [knowledge]  15 major varieties — profiles, benchmarks, blind tells
│   │   ├── indigenous-varieties/       [knowledge]  50 regional varieties — the forgotten vine renaissance
│   │   └── grape-expression/           [knowledge]  Same grape, different terroir — 5 case studies
│   │
│   ├── winemaking/                     [director]  Routes viticulture, vinification, special production
│   │   ├── viticulture/                [knowledge]  Vine cycle, canopy, yield, farming philosophy, phylloxera
│   │   ├── vinification/               [knowledge]  Fermentation, maceration, MLF, oak, fining, SO₂
│   │   ├── special-methods/            [knowledge]  Sparkling, Port, Sherry, Madeira, botrytis, ice wine
│   │   └── alternative-winemaking/     [knowledge]  Natural, orange, pét-nat, amphorae, carbonic, biodynamic
│   │
│   ├── food-pairing/                   [director]  Routes pairing principles, cuisine, and recommendations
│   │   ├── pairing-science/            [knowledge]  5-axis framework, elimination rules, molecular pairing
│   │   ├── cuisine-pairing/            [knowledge]  9 cuisine traditions — French to Korean
│   │   └── pairing-engine/             [action]  Generate 3-5 wine recommendations for any dish
│   │
│   ├── cellar-service/                 [director]  Routes service protocol and cellar management
│   │   ├── service-protocol/           [knowledge]  Temperature, decanting, glassware, opening, formal service
│   │   └── cellar-management/          [knowledge]  Storage conditions, drinking windows, provenance
│   │
│   ├── wine-market/                    [director]  Routes pricing, collecting, and market trends
│   │   ├── wine-economics/             [knowledge]  Pricing mechanics, Parker Effect, en primeur, distribution
│   │   ├── collecting-investment/      [knowledge]  Blue-chip wines, Liv-ex, counterfeiting, collector philosophy
│   │   └── wine-futures/               [knowledge]  Climate change projections, rising regions, consumption trends
│   │
│   └── sommelier-lab/                  [director]  The experimental wing — creative and scientific frontiers
│       ├── synesthetic-notes/          [knowledge]  Wine as color, music, texture, season, emotion
│       ├── blind-tasting-trainer/      [action]  Coached blind tasting sessions with scored reveals
│       ├── climate-projections/        [knowledge]  Region-by-region climate futures, adaptation strategies
│       └── molecular-pairing/         [knowledge]  Flavor compound science, non-obvious pairings, Ahn et al.
│
├── investing/                         Domain: investing  |  Maturity: Level 4
│   ├── archon/                        [orchestrator]  The Archon — master investment orchestrator
│   │   └── references/
│   │       ├── delegation-rules.md    Subdomain routing logic
│   │       ├── domain-taxonomy.md     Full skill architecture map
│   │       └── investor-dna.md        Framework origins (Soros, Buffett, Dalio, etc.)
│   │
│   ├── regime-intelligence/           [director]  Routes macro, monetary, and fiscal analysis
│   │   ├── macro-cycles/              [knowledge]  Dalio debt cycles, business cycles, leading indicators
│   │   ├── monetary-regime/           [knowledge]  Central bank policy, liquidity, yield curves
│   │   └── fiscal-regime/             [knowledge]  Fiscal dominance, sovereign debt, treasury dynamics
│   │
│   ├── reflexivity-sentiment/         [director]  Routes reflexivity, psychology, and sentiment signals
│   │   ├── reflexivity-theory/        [knowledge]  Soros feedback loops, boom-bust 8-phase model
│   │   ├── market-psychology/         [knowledge]  Behavioral biases, fear/greed cycle, crowd dynamics
│   │   └── sentiment-signals/         [knowledge]  Social NLP, GEX signals, flow data, alt sentiment
│   │
│   ├── value-quality/                 [director]  Routes valuation, contrarian, and quality analysis
│   │   ├── intrinsic-value/           [knowledge]  Buffett owner earnings, DCF, moats, margin of safety
│   │   ├── second-level-thinking/     [knowledge]  Marks contrarian framework, cycle positioning
│   │   └── quality-compounders/       [knowledge]  Munger ROIC analysis, compounding math, mental models
│   │
│   ├── risk-architecture/             [director]  Routes sizing, tail risk, correlations, drawdowns
│   │   ├── position-sizing/           [knowledge]  Kelly criterion, risk budgets, Tudor Jones 2:1 rule
│   │   ├── tail-risk/                 [knowledge]  Taleb antifragility, barbell, convexity, black swans
│   │   ├── correlation-regimes/       [knowledge]  Regime-dependent correlations, diversification illusion
│   │   └── drawdown-psychology/       [knowledge]  Marks aggressive/defensive, recovery math, stop losses
│   │
│   ├── market-microstructure/         [director]  Routes passive flows, options mechanics, liquidity
│   │   ├── passive-flow-dynamics/     [knowledge]  Index rebalancing, ETF mechanics, passive dominance
│   │   ├── options-mechanics/         [knowledge]  0DTE gamma, GEX, dealer hedging, vol surface
│   │   └── liquidity-topology/        [knowledge]  Dark pools, VPIN, flash crashes, liquidity illusion
│   │
│   ├── asset-universe/                [director]  Routes asset-class-specific analysis
│   │   ├── equities/                  [knowledge]  Factors, sectors, geography, earnings analysis
│   │   ├── fixed-income/              [knowledge]  Yield curves, credit, duration, TIPS, treasuries
│   │   ├── commodities/               [knowledge]  Energy, metals, agriculture, contango/backwardation
│   │   ├── currencies/                [knowledge]  FX frameworks, dollar dynamics, carry trades
│   │   ├── digital-assets/            [knowledge]  Bitcoin, ETH, tokenization, on-chain analytics
│   │   └── alternatives/              [knowledge]  PE, private credit, real estate, hedge funds, CTA
│   │
│   ├── geopolitical-overlay/          [director]  Routes great power, energy security, secular themes
│   │   ├── great-power-dynamics/      [knowledge]  US-China, Taiwan risk, friend-shoring, de-dollarization
│   │   ├── energy-security/           [knowledge]  Energy transition, oil, nuclear, critical minerals
│   │   └── secular-themes/            [knowledge]  AI capex gap, demographics, deglobalization, debt
│   │
│   ├── special-situations/            [director]  Routes spinoffs, insider signals, complexity, events
│   │   ├── spinoffs-restructuring/    [knowledge]  Greenblatt framework, forced selling, corporate actions
│   │   ├── insider-signals/           [knowledge]  Insider buying patterns, signal hierarchy, data sources
│   │   ├── complexity-premium/        [knowledge]  Holding company discounts, stubs, CEF discounts, net-nets
│   │   └── event-driven/              [knowledge]  Merger arb, activism, catalysts, distressed investing
│   │
│   ├── portfolio-construction/        [director]  Routes allocation, factors, hedging, tax optimization
│   │   ├── asset-allocation/          [knowledge]  60/40, risk parity, all-weather, regime-based allocation
│   │   ├── factor-exposure/           [knowledge]  Factor zoo, robust factors, timing, smart beta
│   │   ├── hedging-architecture/      [knowledge]  Puts, collars, tail hedges, barbell, cross-asset hedges
│   │   └── tax-optimization/          [knowledge]  Tax-loss harvesting, direct indexing, asset location
│   │
│   └── adaptive-monitoring/           [director]  Routes attribution, rebalancing, alt data monitoring
│       ├── performance-attribution/   [knowledge]  Brinson-Fachler, factor attribution, risk attribution
│       ├── rebalancing-logic/         [knowledge]  Calendar vs threshold, tax-aware, thesis invalidation
│       └── alt-data-monitoring/       [knowledge]  Satellite, credit card, NLP, social, geolocation data
```

## Domain Summary

| Domain | Skills | Orchestrator | Directors | Knowledge | Action | Observer | Maturity |
|--------|--------|-------------|-----------|-----------|--------|----------|----------|
| infrastructure | 10 | Yes | No | 0 | 9 | 0 | Level 4 |
| design | 13 | Yes | 3 | 9 | 0 | 0 | Level 5 |
| data-science | 13 | Yes | 3 | 10 | 0 | 0 | Level 5 |
| worldbuilding | 7 | Yes | No | 5 | 1 | 0 | Level 3 |
| game-theory | 22 | Yes | 5 | 12 | 4 | 0 | Level 5 |
| research | 4 | Yes | No | 0 | 3 | 0 | Level 3 |
| writing | 21 | Yes | 4 | 13 | 3 | 0 | Level 4 |
| investing | 47 | Yes | 10 | 36 | 0 | 0 | Level 4 |
| sommelier | 36 | Yes | 8 | 24 | 2 | 0 | Level 4 |
| _meta | 1 | N/A | N/A | N/A | N/A | 1 | N/A |

**Total: 178 skills** (114 knowledge, 22 action, 34 director, 9 orchestrator, 1 observer)

## Gaps Remaining

- **writing**: Full architecture built (21 skills). Future: agent files (prose-drafting, line-edit), reference files for narrative-craft and rhetoric knowledge skills, intermediate/advanced skill tiers
- **research**: v1 complete (Spelunker orchestrator + 3 action skills). Future: add directors (discovery, verification, synthesis) and sub-skills (citation-chaser, lateral-searcher, temporal-validator)
- **worldbuilding**: No directors yet (6 knowledge skills could use a creative-fundamentals director once 1-2 more skills are added)
- **data-science**: Three subdomains (visualization, ml-engineering, frontier) have only 1 skill each — too thin for directors
- **infrastructure**: All action skills, no knowledge layer (acceptable — these are tools, not knowledge). skill-scaffold now integrates with Spelunker for domain research.
- **game-theory**: Complete. Future expansions: repeated/dynamic games, combinatorial game theory
- **investing**: Full architecture built (47 skills). Future: action skills (regime-detector, fundamental-screener, narrative-tracker, flow-scanner, geopolitical-scanner, situation-screener, portfolio-optimizer, portfolio-sentinel, stress-tester), reference files for knowledge skills, integration with data-science domain for quantitative analysis
