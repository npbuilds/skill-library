# Domain Map

Current hierarchy of the skill library. Regenerate this file when the structure changes.

Last updated: 2026-03-22

```
skills/
│
├── _meta/                              [observer]  Meta Observer
│   └── references/
│       ├── domain-map.md               (this file)
│       └── maturity-model.md
│
├── infrastructure/                     Domain: infrastructure  |  Maturity: Level 2
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
├── design/                             Domain: design  |  Maturity: Level 4
│   ├── design-orchestrator/            [orchestrator]  Creative Director
│   │   ├── agents/                     6 specialist agents
│   │   └── references/
│   │
│   └── visual-communication/           [director]  Dept Head — routes visual design questions
│       ├── color-theory/               [knowledge]  Palettes, harmony, contrast, accessibility
│       ├── design-principles/          [knowledge]  Contrast, alignment, proximity, Gestalt
│       └── visual-perception/          [knowledge]  Attention, readability, visual weight
│
├── worldbuilding/                      Domain: worldbuilding  |  Maturity: Level 2
│   ├── world-bible/                    [knowledge]  Axioms, magic systems, revelation layers
│   ├── lore-writer/                    [action]  In-universe artifact generation
│   └── naming-system/                  [knowledge]  Phonetic naming for cultures
│
└── game-theory/                        Domain: game-theory  |  Maturity: Level 4
    ├── game-theory-orchestrator/       [orchestrator]  The Strategist — formalizes and routes
    │   └── references/
    │       ├── delegation-rules.md     Subdomain routing logic
    │       └── domain-taxonomy.md      Full subfield map with sources
    │
    ├── strategic-foundations/           [director]  Routes classical, cooperative, and applied analysis
    │   ├── classical-games/            [knowledge]  Nash, extensive form, refinements, canonical games
    │   │   └── references/
    │   │       ├── canonical-games.md  Named games catalog with payoffs and applications
    │   │       ├── solution-concepts.md Formal definitions, hierarchy, selection criteria
    │   │       └── sources.md          Bibliography — Osborne & Rubinstein, Fudenberg & Tirole, etc.
    │   ├── cooperative-games/          [knowledge]  Shapley, core, bargaining, matching, fair division
    │   │   └── references/
    │   │       ├── solution-concepts-cooperative.md  Core, Shapley, nucleolus, bargaining formal defs
    │   │       ├── matching-and-fairness.md          Gale-Shapley, school choice, kidney exchange, cake-cutting
    │   │       └── sources.md          Bibliography — Maschler/Solan/Zamir, Roth & Sotomayor, etc.
    │   └── game-solver/                [action]  Formalize situations → find equilibria → interpret
    │       └── references/
    │           └── formalization-patterns.md  Real-world-to-game mappings
    │
    ├── mechanism-design/               [director]  Routes auctions, markets, voting, incentives
    │   ├── auction-theory/            [knowledge]  Formats, revenue equivalence, optimal auctions, winner's curse
    │   │   └── references/
    │   │       ├── auction-formats.md Multi-item, combinatorial, GSP, reserve prices
    │   │       └── sources.md         Bibliography — Krishna, Milgrom, Myerson, etc.
    │   ├── matching-markets/          [knowledge]  DA, TTC, market design, real-world deployments
    │   │   └── references/
    │   │       ├── market-design-cases.md  NRMP, NYC schools, kidney exchange, spectrum auctions
    │   │       └── sources.md         Bibliography — Roth & Sotomayor, Abdulkadiroglu & Sonmez, etc.
    │   ├── social-choice/             [knowledge]  Arrow, Gibbard-Satterthwaite, voting rules
    │   │   └── references/
    │   │       └── sources.md         Bibliography — Arrow, Moulin, etc.
    │   └── mechanism-designer/        [action]  Design incentive-compatible mechanisms
    │       └── references/
    │           └── design-patterns.md Common problems and mechanism solutions
    │
    ├── evolutionary-dynamics/         [director]  Routes ESS, replicator dynamics, population games
    │   ├── evolutionary-games/        [knowledge]  ESS, hawk-dove, cooperation evolution, canonical evo games
    │   │   └── references/
    │   │       └── sources.md         Bibliography — Maynard Smith, Weibull, Sandholm, etc.
    │   ├── population-dynamics/       [knowledge]  Replicator equations, phase portraits, Moran, stochastic
    │   │   └── references/
    │   │       └── sources.md         Bibliography — Sandholm, Hofbauer & Sigmund, Nowak, etc.
    │   └── evo-simulator/             [action]  Simulate evolutionary dynamics computationally
    │       └── references/
    │           └── simulation-parameters.md  Defaults, model selection, trajectory patterns
    │
    ├── information-economics/         [director]  Routes signaling, screening, persuasion, disclosure
    │   ├── signaling-screening/       [knowledge]  Spence signaling, Rothschild-Stiglitz, adverse selection, moral hazard
    │   │   └── references/
    │   │       └── sources.md         Bibliography — Bolton & Dewatripont, Fudenberg & Tirole, etc.
    │   ├── bayesian-persuasion/       [knowledge]  Kamenica-Gentzkow, cheap talk, disclosure, information design
    │   │   └── references/
    │   │       └── sources.md         Bibliography — Kamenica & Gentzkow, Crawford & Sobel, etc.
    │   └── info-designer/             [action]  Design optimal information disclosure policies
    │
    └── computational-strategy/        [director]  Routes algorithmic GT, behavioral GT, learning in games
        ├── algorithmic-game-theory/   [knowledge]  PPAD, price of anarchy, congestion games, potential games
        │   └── references/
        │       └── sources.md         Bibliography — Nisan et al., Roughgarden, etc.
        ├── behavioral-game-theory/    [knowledge]  Level-k, QRE, social preferences, experimental evidence
        │   └── references/
        │       └── sources.md         Bibliography — Camerer, Crawford et al., etc.
        └── learning-in-games/         [knowledge]  Fictitious play, no-regret, MARL, self-play, mean field
            └── references/
                └── sources.md         Bibliography — Fudenberg & Levine, Cesa-Bianchi & Lugosi, etc.
```

## Domain Summary

| Domain | Skills | Orchestrator | Directors | Knowledge | Action | Maturity |
|--------|--------|-------------|-----------|-----------|--------|----------|
| infrastructure | 9 | No | No | 0 | 9 | Level 3 |
| design | 5 | Yes | 1 | 3 | 0 | Level 4 |
| worldbuilding | 3 | No | No | 2 | 1 | Level 2 |
| game-theory | 22 | Yes | 5 | 12 | 4 | Level 5 |
| _meta | 1 | N/A | N/A | N/A | N/A | N/A |

## Gaps Detected

- **infrastructure**: No orchestrator (acceptable — these are flat tools, not layered knowledge)
- **design**: No typography subdomain (referenced by typography-agent in design-orchestrator)
- **design**: No brand-identity subdomain (referenced by brand-agent in design-orchestrator)
- **design**: No interaction-design subdomain (referenced by ui-design-agent)
- **worldbuilding**: No orchestrator or director (low maturity)
- **game-theory**: All 5 subdomains complete. No stub directors remain. Future expansions: repeated/dynamic games, combinatorial game theory, quantum game theory
