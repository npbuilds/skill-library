---
name: worldbuilding-orchestrator
description: >
  Orchestrate worldbuilding projects across all creative layers. Use when the user wants to
  build a world, design civilizations, create lore, develop naming conventions, establish
  physical rules, or produce any creative artifact that requires coordinating world-bible
  consistency, cultural voice, naming coherence, and narrative depth. Activates when the user
  is constructing fictional worlds for games, novels, tabletop RPGs, or any narrative medium.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Worldbuilding Orchestrator — The Demiurge

Build worlds from constraints outward. This orchestrator ensures that every creative decision — from naming a tavern to designing a magic system — flows from the foundational axioms established in the world-bible and remains internally consistent as the world grows.

## Phases

### Phase 1 — Understand the Creative Need

Before any worldbuilding, determine what the user needs:

- **Scope** — Full world from scratch, new region/civilization in an existing world, single artifact, or consistency check?
- **Medium** — Novel, game, tabletop RPG, screenplay, personal creative project? The medium constrains how much detail is needed and where depth matters most.
- **Existing material** — Is there already a world-bible, existing lore, established cultures? Check `skills/worldbuilding/world-bible/references/world-axioms.md` and `artifacts/` for existing content.
- **Tone** — What should this world feel like? (See world-bible's Tone and Atmosphere section)
- **Priority** — What does the user care about most? Some builders prioritize hard magic systems, others prioritize political intrigue, others prioritize the feel of places.

If the user says "build me a world," ask about medium and tone before proceeding. If they say "write a tavern menu for the desert culture," check existing axioms and culture definitions first.

### Phase 2 — Classify and Route

Determine which worldbuilding skill(s) apply. Most requests touch multiple skills — pick the primary and note dependencies.

**Skill routing summary:**

| Request Type | Primary Skill | Supporting Skills | Why |
|-------------|--------------|-------------------|-----|
| Define physics, fundamental rules | `world-bible` | — | Axioms come first; everything derives from them |
| Design magic/fantasy system | `magic-system-design` | `world-bible` | Design methodology; results go in world-bible |
| Design geography, physical world | `geography-ecology` | `world-bible` | Terrain, climate, resource distribution |
| Design ecosystems, flora, fauna | `ecology-design` | `geography-ecology`, `world-bible` | Getz 10-niche model, food webs |
| Design what the world feels/smells/sounds like | `sensory-worldbuilding` | `geography-ecology`, `cultures-societies` | Five sensory channels, sensory signatures |
| Design spaces that narrate history through physical traces | `environmental-storytelling` | `history-builder`, `geography-ecology` | Jenkins' four types, archaeology method |
| Create a civilization, culture | `cultures-societies` | `naming-system`, `world-bible` | Seven pillars of culture design |
| Design fictional economies, trade, currency, scarcity | `economic-systems` | `cultures-societies`, `geography-ecology` | Five questions, currency systems, trade routes |
| Design characters as products of their world | `character-design` | `cultures-societies`, `faction-design` | Character Diamond, world-shapes-character pipeline |
| Design religions, belief systems | `religion-design` | `cultures-societies`, `world-bible` | Organizational patterns, deity design |
| Name characters, places, institutions | `naming-system` | `world-bible`, `cultures-societies` | Phonetic palettes per culture |
| Build constructed languages beyond naming | `conlang-craft` | `naming-system`, `cultures-societies` | Morphology, Sapir-Whorf, conlang-to-culture pipeline |
| Write in-universe documents, lore | `lore-writer` | `world-bible`, `naming-system` | 7 voices, artifact format |
| Build history, timelines | `history-builder` | `world-bible`, `lore-writer` | Fractal zoom, non-chronological |
| Track who knows what | `character-belief-tracker` | `world-bible`, `lore-writer` | Belief graph against revelation layers |
| Design factions, organizations | `faction-design` | `cultures-societies`, `world-bible` | Pyramid technique, SUPREME method |
| Design political dynamics, conflict web | `world-bible` | `faction-design`, `cultures-societies` | Faction conflict web |
| Design a conflict, war, rebellion, or rivalry (how it starts, escalates, and ends) | `conflict-design` | `faction-design`, `world-bible` | Five axes (stated/felt), metastable game tipped by emotional variance |
| Design technology levels, innovation | `technology-progression` | `magic-system-design`, `world-bible` | Tech trees, fantasy system disruption |
| Control pacing, tension curves | `narrative-pacing` | `lore-writer`, `world-bible` | Storyteller archetypes, revelation spiral pacing |
| Trace consequences of an axiom | `extrapolation-engine` | `world-bible` | "And Then What?" drill, domain cascade |
| Build weird/numinous/alien worlds that resist systematization | `weird-worldbuilding` | `magic-system-design`, `world-bible` | The Glimpse, unreliable world, numinous objects |
| Consistency check across artifacts | `world-bible` | All others | The bible is the authority |
| Evaluate whether a system is SOUND (costed, limited, propagated), not just consistent | `worldbuilding-critic` | `extrapolation-engine`, `world-bible` | Sanderson's Laws + Rule-of-Consequence + "And Then What?" stress-tests; runs after the consistency check |
| "Build me a world from scratch" | All, in sequence | — | Full pipeline (see Phase 3) |

**Classification decision tree:**

0. **Intent gate — judge or build?** Is this asking to **evaluate** whether an *existing* system is **sound** (costed, limited, propagated) — not to build or define one ("is this magic system sound?", "does this hold up?")?
   - Yes → `worldbuilding-critic` (after a `world-bible` consistency check passes). *Check this first — otherwise "magic system" matches the rules branch below and never reaches the critic.*
1. Is this about the **rules** of the world (physics, magic, resources, constraints)?
   - Yes → `world-bible`
2. Is this about how something **sounds** (names, language, phonetics)?
   - Yes → `naming-system` (but check world-bible for cultural context first)
3. Is this about producing an **in-universe document** (letter, myth, report)?
   - Yes → `lore-writer` (but load relevant world-bible context and naming conventions first)
4. Is this about **checking consistency** across existing material?
   - Yes → `world-bible` as authority, cross-reference all relevant artifacts

### Phase 3 — Establish Build Order

Worldbuilding has hard dependencies. You cannot name a culture before you define it. You cannot write a culture's myths before establishing what it believes. The build order enforces this:

**Full World Pipeline (from scratch):**

1. **Core axioms** (`world-bible`)
   - Scale, physics, resources, scarcity
   - Tone and atmosphere

2. **Fantasy system** (`magic-system-design` → results stored in `world-bible`)
   - Source, cost, limits, access, interaction with physics
   - Propagation test across all domains

3. **Geography and ecology** (`geography-ecology` + `ecology-design`)
   - Physical world: continents, climates, biomes
   - Resource distribution, trade route potential
   - Ecosystems: 10 Getz niches, fantasy ecology interactions

4. **Civilizations** (`cultures-societies` + `naming-system`)
   - For each civilization: seven pillars (governance, economy, religion, social structure, military, knowledge, art)
   - Sound palette: phoneme inventory, syllable rules, naming conventions

5. **Religion and mythology** (`religion-design`)
   - Organizational pattern, scale model, deity portfolios
   - Relationship between religion and the fantasy system

6. **Faction conflict web** (`world-bible`)
   - Relationships between civilizations and factions
   - Surface relationships vs. hidden realities
   - Trigger events that would transform relationships

7. **Factions and politics** (`faction-design` + `world-bible`)
   - Faction anatomy: want, vulnerability, internal tension, public face
   - Faction relationships: alliances, rivalries, dependencies, triggers
   - Power vacuum analysis

8. **Technology** (`technology-progression`)
   - Tech levels across 5 domains (materials, energy, information, transport, medicine)
   - Fantasy system as technology disruptor

9. **History** (`history-builder`)
   - Periods, events, and scenes via fractal zoom
   - Master timeline with gaps tracked explicitly

10. **Revelation architecture** (`world-bible` + `character-belief-tracker`)
    - Layer 0 (surface) through Layer 3 (deep truth)
    - Belief graph: who knows what, who believes what incorrectly

11. **Extrapolation pass** (`extrapolation-engine`)
    - Run the "And Then What?" drill on each major axiom
    - Trace consequences across 8 domains, check for missed implications
    - Test interaction effects between axioms

12. **Pacing design** (`narrative-pacing`)
    - Choose storyteller archetype (Cassandra/Phoebe/Randy)
    - Map revelation spiral timing
    - Plan artifact sequence by voice type for rhythm

13. **Artifacts** (`lore-writer`)
    - In-universe documents in 7 voice registers
    - Each artifact from a specific perspective and revelation layer

**Single Artifact Pipeline:**

1. Load relevant world-bible axioms
2. Load the culture's naming conventions
3. Determine perspective, voice, and revelation layer
4. Write the artifact via lore-writer
5. Cross-check for consistency with existing material

### Phase 4 — Delegate

Route to the appropriate skill, passing accumulated context.

**Available worldbuilding skills:**

| Skill | Type | What It Does |
|-------|------|-------------|
| `world-bible` | knowledge | Foundational axioms and constraints — the single source of truth |
| `magic-system-design` | knowledge | Fantasy system design methodology — source, cost, limits, access |
| `geography-ecology` | knowledge | Physical world — terrain, climate, biomes, resource distribution |
| `ecology-design` | knowledge | Complete ecosystems — Getz 10-niche model, food webs |
| `cultures-societies` | knowledge | Civilization design — seven pillars of culture |
| `religion-design` | knowledge | Religion design — organizational patterns, deity portfolios |
| `naming-system` | knowledge | Phonetic palettes and naming conventions per culture |
| `lore-writer` | action | Produces in-universe artifacts in 7 voice registers |
| `history-builder` | action | Non-chronological history building via fractal zoom |
| `character-belief-tracker` | action | Tracks who knows what against revelation layers |
| `narrative-pacing` | knowledge | Tension curves, storyteller archetypes, pacing by artifact type |
| `technology-progression` | knowledge | Tech trees, innovation pathways, fantasy system disruption |
| `faction-design` | knowledge | Pyramid technique, SUPREME method, power vacuums |
| `conflict-design` | knowledge | Conflict as a system — five stated/felt axes, metastable game tipped by emotional variance |
| `extrapolation-engine` | knowledge | "And Then What?" drill, cascading consequences across domains |
| `economic-systems` | knowledge | Fictional economies — trade, currency, scarcity, Five Questions framework |
| `conlang-craft` | knowledge | Constructed languages — morphology, Sapir-Whorf, conlang-to-culture pipeline |
| `character-design` | knowledge | Characters as products of world — Character Diamond, arc patterns |
| `sensory-worldbuilding` | knowledge | What the world feels/smells/sounds like — five sensory channels |
| `environmental-storytelling` | knowledge | Physical spaces narrating history — Jenkins' four types, archaeology method |
| `weird-worldbuilding` | knowledge | Anti-systematic worldbuilding — the Glimpse, numinous objects, estrangement |
| `worldbuilding-critic` | action | Judges whether an invented system is *sound* (cost/limits/access/propagation/bright-line) — runs after the consistency check |

When delegating, always pass:
- Current world-bible state (relevant axioms)
- Relevant naming conventions (if the artifact involves any culture)
- The revelation layer this work operates at
- Any existing artifacts that must be consistent with the new work

For full-world builds, execute in the Phase 3 build order. Each phase receives the output of all prior phases.

### Phase 5 — Harmonize and Present

After creation completes:

1. **Consistency audit** — Does the new content align with existing world-bible axioms? Do names follow the correct sound palette? Does the revelation layer match?

2. **Cross-reference check** — Does the new content reference anything that doesn't exist yet? Flag these as "stubs to build."

3. **Present the work** — Show what was created, organized by type:
   - Axioms established or updated
   - Cultures defined
   - Names generated
   - Artifacts written

4. **Map what's next** — After any worldbuilding session, identify the most natural next thing to build. The world grows organically — each piece creates questions that the next piece answers.

## Knowledge Layer

All worldbuilding knowledge lives in these locations:

| Source | What's There | When to Check |
|--------|-------------|---------------|
| `world-bible/references/` | Axioms, revelation layers, faction web, Wrede taxonomy, OnlyWorlds ontology, generation pipeline | Before any creative decision |
| `magic-system-design/references/` | Cost structure patterns | When designing the fantasy system |
| `ecology-design/references/` | Getz 10-niche model detail | When designing ecosystems |
| `religion-design/references/` | Religion design patterns, deity portfolio framework | When designing belief systems |
| `naming-system/references/` | Culture sound palettes | Before creating any proper noun |
| `lore-writer/references/` | Voice registry, artifact format, output conventions | Before writing any in-universe document |
| `artifacts/` | All produced lore documents | Before writing new artifacts (consistency check) |
| `artifacts/meta/` | Belief graph, master timeline | Before any narrative decision |

**Always check the world-bible first.** It is the single source of truth. Nothing contradicts it. When axioms need to change, they change in the bible first and propagate outward.

## Failure Recovery

- If the user's request contradicts existing axioms, flag the contradiction and ask: "Should we update the axiom, or adjust the request?"
- If a naming palette doesn't exist yet for a culture, build it before generating names — never improvise names without a palette
- If the revelation architecture creates a paradox (Layer 0 document accidentally reveals Layer 2 truth), revise the document's perspective to a character who wouldn't know that information
- If the user rejects a creative direction, ask what specifically feels wrong (tone? detail level? cultural flavor?) rather than starting over

## Scope Boundaries

This orchestrator handles **fictional world construction and maintenance**. It does NOT:
- Write plot, narrative structure, or character arcs (those are storytelling, not worldbuilding)
- Generate visual art or maps (it produces textual descriptions and specifications)
- Make creative decisions without the user's input (it proposes and the user decides)
- Evaluate the world's quality as fiction (it ensures consistency, not literary merit)

## Cross-Domain Routing

When the user finishes building (or has enough built to start drafting) and wants to write IN this world, hand off to the prose orchestrator. The worldbuilding orchestrator owns *what is true*; the prose orchestrator owns *how it lands on the page*.

| When the work shifts to... | Hand off to... | Bridge skill |
|---|---|---|
| Writing prose in the built world (scenes, chapters, drafts) | **prose-orchestrator** | `skills/writing/narrative-craft/world-to-story/` — iceberg methodology, revelation channels, system → scene translation, exposition techniques |
| Rendering a built region in prose (sensory immersion) | **prose-orchestrator** | `skills/writing/narrative-craft/sensory-translation/` — translates `sensory-worldbuilding`'s 5 channels into prose detail-selection and POV-based attention bias |
| Characters speaking and thinking in their culture's voice | **prose-orchestrator** | `skills/writing/narrative-craft/cultural-voice/` — translates `cultures-societies` + `naming-system` into vocabulary domains, idiom, syntax rhythm, metaphor source |
| In-universe document drafting (letters, myths, reports, intercepted intelligence) | **Stay here** | `lore-writer` already covers this — 7 voice registers, artifact format, frontmatter conventions |
| Game systems / mechanics design (loops, balance, progression, catch-up systems) | `skills/narrative-design/game-mechanics/` | Relocated from worldbuilding — it is game design, not world construction |
| Aligning prose pacing with worldbuilding's revelation spiral | **prose-orchestrator** | `narrative-pacing` (here) pairs with `writing/narrative-craft/pacing` — same vocabulary, different scales |

**Operating principle for the handoff:** never hand off prematurely. Establish at least the world-bible axioms, the focal culture(s), and the relevant magic/tech rules before drafting. A scene written before the world supports it will need to be rewritten when the world is filled in. The order is `world-bible → focal cultures → focal factions → relevant systems → hand off`. For one-off lore artifacts, the lore-writer can run on much less.

## Related Skills

The prose orchestrator (writing domain) is the downstream consumer of this orchestrator's output: worldbuilding owns *what is true*, prose owns *how it lands on the page*. The dependency is **directional** — prose-orchestrator depends on worldbuilding-orchestrator (a story needs a world before it can be written), but **not** the reverse: a world bible is built without writing a single scene. That is why the handoff above points to **prose-orchestrator** in plain text rather than as a `depends_on` edge — it is a forward handoff, not a dependency of this orchestrator (see STYLE_GUIDE #6, "The Mutual Dependency").
