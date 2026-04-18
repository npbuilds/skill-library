# Delegation Rules

How wan-shi-tong routes a user question through the 5-step loop (ORIENT → SITUATE → ANALYZE → DELIVER → CONNECT) into one or more wings.

## Single-Wing Routing

Most questions resolve to a single primary wing. Match the strongest keyword cluster.

| Signal cluster | Primary wing |
|---|---|
| state, empire, regime, revolution, election, treaty, sovereignty, nation, government | political-history |
| trade, money, currency, market, debt, tax, industrialization, labor, inequality, finance | economic-history |
| religion, art, ritual, gender, identity, daily life, family, sexuality, popular belief | cultural-history |
| war, battle, campaign, strategy, weapon, espionage, deterrence, occupation | military-history |
| idea, philosophy, science, paradigm, Enlightenment, ideology, knowledge | intellectual-history |
| civilization (compared), climate, plague, demography, longue durée, deep time, Big History | world-systems |
| how do we know, source, evidence, historian disagrees, methodology, primary source | historiography |
| analogy, lesson, "what does X teach us," timeline, "is this like Y," precedent | applied-history |
| China, Africa, Mediterranean, Americas, region-specific question | regional-atlas |

## Multi-Wing Routing

If two or more clusters match, identify the **primary** (whose framework is *required to formulate* the question) and **supporting** (whose context illuminates).

| Question template | Primary | Supporting |
|---|---|---|
| "Why did [empire] fall?" | political-history | economic, military, world-systems |
| "How did [technology] change history?" | intellectual-history | cultural, economic, world-systems |
| "Was [empire/system] good or bad?" | applied-history | political, economic, cultural |
| "Tell me about [trade route]" | economic-history | cultural, regional-atlas |
| "How did [marginalized group] resist [system]?" | cultural-history | political, applied-history |
| "What caused [war]?" | political-history | military, economic, intellectual |
| "How did [religion] spread?" | cultural-history | intellectual, regional-atlas, world-systems |
| "Why did [region] industrialize first / later?" | economic-history | world-systems, regional-atlas, intellectual |
| "Compare [civilization A] and [civilization B]" | world-systems | regional-atlas + relevant thematic wings |
| "How do historians disagree about [event]?" | historiography | the thematic wing for the event |

## Multi-Wing Sequencing

When loading multiple wings, follow this sequence:

1. **World-systems first** if structural/environmental forces are in play — sets the substrate.
2. **Regional-atlas second** if a specific region is named — grounds the analysis.
3. **Primary thematic wing** — does the core analytical work.
4. **Supporting thematic wings** — contribute color and complication.
5. **Historiography last** if interpretation is contested — names the schools and stakes.

## Cross-Domain Escalation

| Trigger | Escalate to | Why |
|---|---|---|
| Question evaluates whether an idea is *true* | philosophy-orchestrator | Philosophy adjudicates truth; intellectual-history traces emergence |
| Question models strategic interaction (deterrence, signaling, alliance) | game-theory-orchestrator | Formal frameworks beat narrative |
| Question asks for a *story* about history (fiction, narrative non-fiction) | writing | Craft of prose, not historical analysis |
| Question asks for *quantitative* historical analysis | data-science | Statistical methods, regression, time-series |
| Question seeks historical *foundations for fiction worlds* | worldbuilding | Synthesis for invention |
| Question maps history → market-cycle inference | investing/archon | Cycle pattern reuse |
| Question asks for *systematic source triangulation* on contested claim | research/spelunker | Evidence-tagged briefs |

## When NOT to Delegate (Handle at Orchestrator Level)

- **Pure scope/orientation questions**: "What is world history?" "How is this library organized?" → answer directly using domain-taxonomy.md.
- **Multi-wing curriculum requests**: "Teach me history" → orchestrator builds the curriculum, then delegates each topic.
- **Cross-temporal pattern questions** so general no single wing dominates: "How do empires fall?" → orchestrator synthesizes from multiple wings using historical-pattern-recognition.

## Conflict Resolution

| Conflict | Resolution |
|---|---|
| Two wings both seem primary | Default to whichever wing's *director must be loaded first* to interpret the question — usually the wing whose vocabulary the user actually used |
| Question is contested by historians | Always load historiography as supporting cast — name the schools, present both interpretations |
| Question imports modern assumptions into pre-modern context | Flag the anachronism explicitly before answering (Chronological Lens Protocol step 4) |
| User signals advanced knowledge | Push toward historiography earlier — show the debate, not just the conclusion |
| User signals beginner | Stay in the primary wing only; defer multi-wing complexity until they ask "why" |

## Worked Example

**Question:** "Why did the Roman Empire fall?"

1. **ORIENT** — political (empire), declines (fall), advanced vocabulary inferable from "Roman Empire" specificity.
2. **SITUATE** — Late antiquity, 3rd–5th centuries CE, Mediterranean world.
3. **ANALYZE** — Primary: political-history. Supporting: economic-history (currency debasement, fiscal collapse), military-history (legions, foederati), world-systems (climate downturn, Antonine plague), historiography (Gibbon vs. Pirenne vs. Wickham vs. Ward-Perkins debate).
4. **DELIVER** — At "Learning" depth, present 3 layered causes (immediate / underlying / structural). At "Advanced" depth, surface the historiographical debate up front.
5. **CONNECT** — Learn block on the recurring pattern: imperial overreach + fiscal exhaustion + climatic stress + frontier contagion = collapse.
