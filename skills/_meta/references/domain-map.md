# Domain Map

Current hierarchy of the skill library. Regenerate this file when the structure changes.

Last updated: 2026-04-12

```
skills/
│
├── _meta/                              [observer]  Sentinel Prime — The Eternal Watchguard
│   └── references/
│       ├── domain-map.md               (this file)
│       ├── maturity-model.md           6-level domain maturity scale
│       └── quick-reference.md          Output format template
│
├── artifacts/                          Domain: artifacts  |  Maturity: Level 3
│   ├── master-artificer/              [orchestrator]  Coordinates artifact creation
│   ├── (2 knowledge skills)
│
├── infrastructure/                     Domain: infrastructure  |  Maturity: Level 4
│   ├── infrastructure-orchestrator/    [orchestrator]  The Architect — coordinates lifecycle ops
│   └── (9 action skills)              skill-registry, skill-health, skill-dashboard,
│                                       skill-scaffold, skill-test, skill-analyze,
│                                       skill-fork, skill-network, skill-export
│
├── design/                             Domain: design  |  Maturity: Level 5
│   ├── design-orchestrator/            [orchestrator]  Creative Director
│   ├── visual-communication/           [director]  3 knowledge skills
│   ├── typography/                     [director]  3 knowledge skills
│   ├── brand-identity/                 [director]  3 knowledge skills
│   └── style-evolution-observer/       [observer]
│
├── data-science/                       Domain: data-science  |  Maturity: Level 5
│   ├── data-science-orchestrator/      [orchestrator]  The Analyst
│   ├── data-wrangling/                 [director]  2 knowledge skills
│   ├── statistical-analysis/           [director]  3 knowledge skills
│   ├── modeling/                       [director]  2 knowledge skills
│   └── (3 singleton subdomains)        visualization, ml-engineering, frontier
│
├── game-theory/                        Domain: game-theory  |  Maturity: Level 5
│   ├── game-theory-orchestrator/       [orchestrator]  The Strategist
│   ├── strategic-foundations/           [director]  2 knowledge + 1 action
│   ├── mechanism-design/               [director]  3 knowledge + 1 action
│   ├── evolutionary-dynamics/          [director]  2 knowledge + 1 action
│   ├── information-economics/          [director]  2 knowledge + 1 action
│   └── computational-strategy/         [director]  3 knowledge
│
├── investing/                          Domain: investing  |  Maturity: Level 5
│   ├── archon/                         [orchestrator]  The Archon — master investment orchestrator
│   ├── regime-intelligence/            [director]  3 knowledge skills
│   ├── reflexivity-sentiment/          [director]  3 knowledge skills
│   ├── value-quality/                  [director]  3 knowledge skills
│   ├── risk-architecture/              [director]  4 knowledge skills
│   ├── market-microstructure/          [director]  3 knowledge skills
│   ├── asset-universe/                 [director]  6 knowledge skills
│   ├── geopolitical-overlay/           [director]  3 knowledge skills
│   ├── special-situations/             [director]  4 knowledge skills
│   ├── portfolio-construction/         [director]  4 knowledge skills
│   └── adaptive-monitoring/            [director]  3 knowledge skills
│
├── research/                           Domain: research  |  Maturity: Level 3
│   ├── spelunker/                      [orchestrator]  The Deep Researcher
│   └── (4 action skills)              claim-decomposer, source-triangulator,
│                                       evidence-synthesizer, agentic-researcher
│
├── sommelier/                          Domain: sommelier  |  Maturity: Level 5
│   ├── bacchus/                        [orchestrator]  God of the Vine
│   ├── tasting-evaluation/             [director]  4 knowledge skills
│   ├── regions-terroir/                [director]  4 knowledge skills
│   ├── grape-encyclopedia/             [director]  3 knowledge skills
│   ├── winemaking/                     [director]  4 knowledge skills
│   ├── food-pairing/                   [director]  2 knowledge + 1 action
│   ├── cellar-service/                 [director]  2 knowledge skills
│   ├── wine-market/                    [director]  3 knowledge skills
│   └── sommelier-lab/                  [director]  3 knowledge + 1 action
│
├── worldbuilding/                      Domain: worldbuilding  |  Maturity: Level 5
│   ├── worldbuilding-orchestrator/     [orchestrator]  The Demiurge
│   ├── (3 directors)                   Routes world creation subdomains
│   ├── (19 knowledge skills)           World bible, naming, geography, cultures, magic, etc.
│   └── (3 action skills)              lore-writer, character-belief-tracker, etc.
│
└── writing/                            Domain: writing  |  Maturity: Level 5
    ├── prose-orchestrator/             [orchestrator]  The Editor's Desk
    ├── sentence-craft/                 [director]  3 knowledge skills
    ├── narrative-craft/                [director]  6 knowledge skills
    ├── rhetoric/                       [director]  4 knowledge skills
    ├── revision-craft/                 [director]  2 action skills
    └── (6 action skills)              prose-writer, style-mixer, etc.
```

## Domain Summary

| Domain | Skills | Orchestrator | Directors | Knowledge | Action | Observer | Maturity |
|--------|--------|-------------|-----------|-----------|--------|----------|----------|
| artifacts | 3 | Yes | 0 | 2 | 0 | 0 | Level 3 |
| data-science | 14 | Yes | 3 | 10 | 0 | 0 | Level 5 |
| design | 17 | Yes | 3 | 12 | 0 | 1 | Level 5 |
| game-theory | 22 | Yes | 5 | 12 | 4 | 0 | Level 5 |
| infrastructure | 10 | Yes | 0 | 0 | 9 | 0 | Level 4 |
| investing | 47 | Yes | 10 | 36 | 0 | 0 | Level 5 |
| research | 5 | Yes | 0 | 0 | 4 | 0 | Level 3 |
| sommelier | 36 | Yes | 8 | 25 | 2 | 0 | Level 5 |
| worldbuilding | 26 | Yes | 3 | 19 | 3 | 0 | Level 5 |
| writing | 30 | Yes | 4 | 19 | 6 | 0 | Level 5 |
| _meta | 1 | N/A | N/A | N/A | N/A | 1 | N/A |

**Total: 253 skills** (137 knowledge, 57 action, 45 director, 12 orchestrator, 2 observer)

## Structural Notes

- **4 orphan skills** (no parent director): lore-writer, character-belief-tracker, narrative-pacing, extrapolation-engine
- **game-mechanics** relocated to new `narrative-design` domain — it is tabletop/digital game systems design, not worldbuilding
- **1 unhealthy skill**: character-interiority (writing domain)
- **73% of skills have never been used** — usage is concentrated in orchestrators and a handful of action skills
- **artifacts** and **research** domains are at Level 3 — candidates for structural investment if usage warrants it
