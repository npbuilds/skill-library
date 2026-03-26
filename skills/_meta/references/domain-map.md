# Domain Map

Current hierarchy of the skill library. Regenerate this file when the structure changes.

Last updated: 2026-03-25

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
```

## Domain Summary

| Domain | Skills | Orchestrator | Directors | Knowledge | Action | Observer | Maturity |
|--------|--------|-------------|-----------|-----------|--------|----------|----------|
| infrastructure | 10 | Yes | No | 0 | 9 | 0 | Level 4 |
| design | 13 | Yes | 3 | 9 | 0 | 0 | Level 5 |
| data-science | 13 | Yes | 3 | 10 | 0 | 0 | Level 5 |
| worldbuilding | 7 | Yes | No | 5 | 1 | 0 | Level 3 |
| game-theory | 22 | Yes | 5 | 12 | 4 | 0 | Level 5 |
| _meta | 1 | N/A | N/A | N/A | N/A | 1 | N/A |

**Total: 66 skills** (36 knowledge, 14 action, 8 director, 4 orchestrator, 1 observer, 3 new directors)

## Gaps Remaining

- **worldbuilding**: No directors yet (6 knowledge skills could use a creative-fundamentals director once 1-2 more skills are added)
- **data-science**: Three subdomains (visualization, ml-engineering, frontier) have only 1 skill each — too thin for directors
- **infrastructure**: All action skills, no knowledge layer (acceptable — these are tools, not knowledge)
- **game-theory**: Complete. Future expansions: repeated/dynamic games, combinatorial game theory
