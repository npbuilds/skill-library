---
name: political-history
description: >
  Route questions about states, empires, governance, revolution, diplomacy, sovereignty,
  and international order. Activate when users ask about how political power has been
  organized, contested, transferred, or dissolved across history, from ancient city-states
  through modern nation-states and international systems.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Political History — The Hall of Thrones

The Hall of Thrones is the largest wing of Wan Shi Tong's library because political power is the thread that connects nearly every historical question. Who rules? How did they gain power? How do they keep it? What happens when they lose it? These questions recur across every civilization, every century, every continent. This wing routes by the *type* of political question — whether it concerns the structure of states, the dynamics of revolution, the architecture of international order, or the dissolution of colonial systems.

Every question in this wing applies across temporal registers. Empires-and-states covers Akkad to the EU. Revolutions covers the English Civil War to the Arab Spring. The chronological lens protocol ensures no question is trapped in a single era.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `empires-and-states` | knowledge | Rise, administration, and fall of states and empires; governance structures; legitimacy; overstretch |
| `revolutions-and-regime-change` | knowledge | Revolutionary dynamics, structural conditions, phases, consolidation and failure |
| `diplomacy-and-international-order` | knowledge | How states relate to each other; balance of power, alliances, international law |
| `decolonization-and-sovereignty` | knowledge | Colonial dissolution, liberation movements, neo-colonialism, modern state creation |
| `historical-analogy-engine` | action | Structured analogy analysis: current event → historical parallels → lessons and limits |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Empire, kingdom, state, governance, dynasty, administration, collapse, fall | `empires-and-states` | Questions about political structures and their life cycles |
| Revolution, uprising, coup, regime change, civil war, overthrow | `revolutions-and-regime-change` | Questions about political rupture and transformation |
| Diplomacy, alliance, treaty, balance of power, international, UN, foreign policy | `diplomacy-and-international-order` | Questions about inter-state relations |
| Colony, independence, liberation, self-determination, post-colonial, imperialism | `decolonization-and-sovereignty` | Questions about colonial systems and their dissolution |
| "Is this like," "what's the parallel," current event + historical comparison | `historical-analogy-engine` | Action: structured analogy with explicit limits |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "Why did the Ottoman Empire collapse?" | empires-and-states → diplomacy-and-international-order | Internal dynamics first, then the international context that accelerated collapse |
| "How does the Arab Spring compare to 1848?" | revolutions-and-regime-change → historical-analogy-engine | Pattern analysis first, then structured comparison |
| "How did decolonization reshape the international order?" | decolonization-and-sovereignty → diplomacy-and-international-order | Colonial dissolution first, then its effects on the state system |

## Curriculum Order

1. **`empires-and-states`** (foundation) — The backbone of political history; state formation is prerequisite to all other political topics
2. **`diplomacy-and-international-order`** (framework) — How states relate; requires understanding what states are
3. **`revolutions-and-regime-change`** (dynamics) — How political orders break; requires understanding what they look like intact
4. **`decolonization-and-sovereignty`** (application) — Applies all three prior skills to the 20th century's defining political transformation
5. **`historical-analogy-engine`** (action) — Structured comparison of current events to historical parallels; requires familiarity with all four knowledge skills

### Level Progression
- **Foundational**: empires-and-states
- **Intermediate**: diplomacy-and-international-order, revolutions-and-regime-change
- **Advanced**: decolonization-and-sovereignty, historical-analogy-engine

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Internal vs. external causes of state collapse | Present both; empires-and-states leads | Most collapses involve both; internal structural weakness is usually primary |
| Structural vs. contingent explanations of revolution | Name both frameworks explicitly | Skocpol (structural) and agency-based accounts are complementary, not contradictory |
| Realist vs. liberal explanations of international order | Present the debate | This IS the field — the tension is the content |

**General rule**: Political history is contested terrain. Always present at least two interpretive frameworks and name the scholars behind them.

## Scope Boundaries

**This director handles**: All questions about political power — how it is organized, contested, transferred, and dissolved, across all times and places.

**Escalate to wan-shi-tong when**:
- The question is primarily about economic causes of political events (route to economic-history)
- The question is about ideas driving political change (route to intellectual-history)
- The question is about military campaigns rather than political outcomes (route to military-history)
- The question is about applying political history to present decisions (route to applied-history)
