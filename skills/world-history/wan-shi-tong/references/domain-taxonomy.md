# Domain Taxonomy — The Library of Wan Shi Tong

The library has nine wings. Each wing is a director that routes to specialist knowledge skills. The taxonomy is **thematic, not chronological** — every wing applies its analysis across all temporal registers (Deep, Ancient, Post-classical, Early Modern, Modern, Contemporary).

## Architecture

```
wan-shi-tong (orchestrator)
│
├── political-history          [Hall of Thrones]      States, empires, governance
│   ├── empires-and-states
│   ├── revolutions-and-regime-change
│   ├── diplomacy-and-international-order
│   └── decolonization-and-sovereignty
│
├── economic-history           [Counting House]       Trade, finance, material life
│   ├── trade-and-globalization
│   ├── money-and-financial-systems
│   ├── industrialization-and-development
│   └── labor-and-inequality
│
├── cultural-history           [Gallery of Voices]    Art, religion, identity, daily life
│   ├── religions-and-worldviews
│   ├── art-and-cultural-production
│   ├── gender-and-sexuality-history
│   ├── social-movements-and-identity
│   └── everyday-life-and-material-culture
│
├── military-history           [War Room]             Warfare, strategy, intelligence
│   ├── warfare-through-the-ages
│   ├── strategy-and-grand-strategy
│   ├── battle-analysis
│   └── intelligence-and-information-war
│
├── intellectual-history       [Hall of Minds]        Ideas, science, political thought
│   ├── political-thought
│   ├── scientific-revolutions
│   └── knowledge-systems
│
├── world-systems              [Observatory]          Civilizations, environment, deep time
│   ├── deep-history
│   ├── environmental-history
│   ├── demographic-and-structural-forces
│   ├── comparative-civilizations
│   └── technology-and-civilizational-change
│
├── historiography             [Scriptorium]          Methods, sources, schools
│   ├── historical-thinking
│   ├── source-criticism
│   ├── historical-argument
│   ├── schools-of-thought
│   └── source-evaluator   (action)
│
├── applied-history            [Council Chamber]      Analogies, patterns, decision-making
│   ├── historical-analogy-engine          (action)
│   ├── historical-pattern-recognition
│   ├── history-and-decision-making
│   ├── timeline-builder                   (action)
│   ├── debate-simulator                   (action)
│   ├── comparative-analysis-engine        (action)
│   └── nexus-event-analyzer               (action)
│
└── regional-atlas             [Map Room]             Region-specific connected histories
    ├── mediterranean-and-near-east
    ├── east-asia
    ├── sub-saharan-africa
    └── americas-and-oceania
```

## Wing Descriptions

### ① political-history — Hall of Thrones
**Scope:** How political power has been organized, contested, transferred, or dissolved — from ancient city-states through modern nation-states and international systems.
**Strongest cross-domain bridge:** game-theory-orchestrator (strategic interaction).
**Boundary signal:** If the question is about the *ideas* legitimating power, escalate to intellectual-history. If it's about *violence* enforcing power, military-history.

### ② economic-history — Counting House
**Scope:** How economies have been organized, how wealth has been created and distributed, why some societies industrialized and others did not, how financial systems evolved and crashed.
**Strongest cross-domain bridge:** investing/archon (market-cycle analysis informed by financial history).
**Boundary signal:** If the question is about *labor as identity*, supporting cast cultural-history. If about *technology driving production*, supporting cast world-systems.

### ③ cultural-history — Gallery of Voices
**Scope:** How ordinary people lived; how belief systems shaped civilizations; how marginalized groups changed history; how cultural production reflects and reshapes power.
**Strongest cross-domain bridges:** writing (narrative), worldbuilding (lived texture).
**Boundary signal:** If the question is about *formal theology or doctrine*, escalate to intellectual-history. If about *gendered power structures*, primary cultural-history with political-history support.

### ④ military-history — War Room
**Scope:** Warfare, strategy, military technology, intelligence, peacemaking — the persistent organization of organized violence and its consequences.
**Strongest cross-domain bridge:** game-theory-orchestrator (deterrence, signaling, coordination).
**Boundary signal:** Always connect military events to political, economic, and social context (Clausewitz). Never treat battles as standalone.

### ⑤ intellectual-history — Hall of Minds
**Scope:** How ideas emerged from specific contexts, spread across networks, and produced consequences their originators never imagined.
**Strongest cross-domain bridge:** philosophy-orchestrator (intellectual-history provides the *historical context*; philosophy evaluates *analytically*).
**Boundary signal:** If the question evaluates whether an idea is *true*, that's philosophy. If it asks *how the idea took hold*, that's intellectual-history.

### ⑥ world-systems — Observatory
**Scope:** Deep structural forces — environmental, demographic, technological — that operate beneath political, economic, and cultural events. Braudel's *longue durée*; Diamond; Turchin; Christian's Big History.
**Strongest cross-domain bridges:** data-science (cliodynamics), worldbuilding (deep-time scaffolds).
**Boundary signal:** If a question feels too big for any single thematic wing, world-systems is usually primary.

### ⑦ historiography — Scriptorium
**Scope:** How history works as a discipline — methods, evidence, interpretation, argument, and the history of history itself.
**Strongest cross-domain bridge:** research/spelunker (evidence triangulation, source evaluation).
**Boundary signal:** If the question is "what happened," route to a thematic wing. If it is "how do we know what happened," historiography is primary.

### ⑧ applied-history — Council Chamber
**Scope:** Using history as a practical tool for understanding the present — analogies, recurring patterns, lessons for current decisions.
**Strongest cross-domain bridges:** investing/archon, game-theory-orchestrator (decision-making under uncertainty).
**Boundary signal:** Every analogy has limits. The skill is knowing where the analogy *holds* and where it *breaks* — name both.

### ⑨ regional-atlas — Map Room
**Scope:** Geographic depth that thematic wings cannot provide — using Subrahmanyam's "connected histories" lens to emphasize cross-regional entanglements over isolated area studies.
**Strongest cross-domain bridges:** worldbuilding, regional cultural traditions in cultural-history.
**Boundary signal:** Never treat a region in isolation. Always surface at least one cross-regional connection.

## Cross-Wing Dependencies

| Wing A | Wing B | Dependency |
|---|---|---|
| political-history | military-history | Wars are politics by other means; cannot separate |
| economic-history | political-history | Fiscal-military states; tax → war → state-building |
| cultural-history | intellectual-history | Popular belief vs. elite doctrine — symbiotic |
| world-systems | every wing | Provides the deep-structural substrate |
| historiography | every wing | Provides the meta-methodology for evaluating claims |
| regional-atlas | every wing | Grounds thematic claims in geographic specificity |
| applied-history | every wing | Pulls patterns from other wings into present decisions |

## Routing Heuristic

When a question arrives:
1. **Identify the thematic axis** (which wing's keywords appear?).
2. **Identify the temporal register** (which era, or trans-temporal?).
3. **If only one wing matches** → route there.
4. **If multiple wings match** → assign primary by *which director's frameworks are necessary to even formulate the question*; the rest are supporting.
5. **If no thematic wing matches but the question is meta** ("how do we know," "what's the evidence") → historiography.
6. **If the question asks for a present-day decision** → applied-history primary, with thematic wings supporting.
