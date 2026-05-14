---
name: military-history
description: >
  Route questions about warfare, strategy, military technology, intelligence, and peacemaking
  across history. Activate when users ask about battles, campaigns, grand strategy, revolutions
  in military affairs, espionage, or the evolution of how humans organize violence and its
  consequences for political and social order.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Military History — The War Room

The War Room does not glorify war — it studies it as a persistent feature of human civilization that has shaped borders, toppled empires, driven technological change, and defined the lives of billions. Military history is not just about battles; it encompasses strategy (why wars are fought and how they connect to political goals), technology (how the tools of war reshape societies), intelligence (how information asymmetry determines outcomes), and the human experience of combat.

War is Clausewitz's "continuation of politics by other means" — and understanding military history requires always connecting military events to their political, economic, and social contexts.

## Child Skills

| Skill | Type | Handles |
|---|---|---|
| `strategy-and-grand-strategy` | knowledge | Strategic thought from Sun Tzu through modern theory; alignment of military means to political ends |
| `warfare-through-the-ages` | knowledge | How humans fight: phalanx through hybrid warfare; revolutions in military affairs |
| `intelligence-and-information-war` | knowledge | Espionage, codebreaking, deception, propaganda, cyber; information asymmetry in conflict |
| `battle-analysis` | action | Structured analysis of specific battles/campaigns using Staff Ride methodology |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| Strategy, grand strategy, Clausewitz, Sun Tzu, political-military, deterrence | `strategy-and-grand-strategy` | Questions about strategic thinking and its application |
| Battle, campaign, army, navy, weapons, tactics, military technology, revolution in military affairs | `warfare-through-the-ages` | Questions about how wars are fought and how warfare evolves |
| Espionage, intelligence, spy, codebreaking, propaganda, information warfare, cyber, deception | `intelligence-and-information-war` | Questions about the information dimension of conflict |
| "Analyze this battle," specific battle name, "what happened at Gettysburg/Stalingrad/Midway" | `battle-analysis` | Action: structured battle/campaign analysis |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "Why did Germany lose WWII?" | strategy-and-grand-strategy → warfare-through-the-ages | Grand strategic failures first, then operational/tactical dimension |
| "How did codebreaking at Bletchley Park affect the war?" | intelligence-and-information-war → strategy-and-grand-strategy | Intelligence capability first, then its strategic impact |
| "Analyze the Battle of Cannae" | battle-analysis → strategy-and-grand-strategy | Specific battle analysis first, then strategic context and lessons |

## Curriculum Order

1. **`strategy-and-grand-strategy`** (foundation) — Strategic thinking frames all military questions; without it, battles are just violence
2. **`warfare-through-the-ages`** (evolution) — How the practice of war has changed; requires strategic framing to interpret
3. **`intelligence-and-information-war`** (dimension) — The information layer; requires understanding of both strategy and operations
4. **`battle-analysis`** (action) — Applied analysis; requires all three knowledge skills as context

### Level Progression
- **Foundational**: strategy-and-grand-strategy
- **Intermediate**: warfare-through-the-ages, intelligence-and-information-war
- **Advanced**: battle-analysis

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Strategic vs. tactical explanation of outcomes | Strategy leads | Tactical brilliance rarely compensates for strategic failure (Napoleon in Russia, Germany in WWII) |
| Technology vs. leadership as decisive factor | Context-dependent; present both | Sometimes technology matters more (machine guns in WWI), sometimes leadership (Alexander's campaigns) |
| Military vs. political explanation of war's outcome | Political framing wins | Wars are instruments of policy; military outcomes must be evaluated against political objectives |

**General rule**: War is always political. Every military question ultimately connects to a political question. The War Room always routes back to the Hall of Thrones when the user needs to understand *why* a war happened or *what* its outcome meant.

## Scope Boundaries

**This director handles**: All questions about organized violence, its conduct, its tools, its intelligence dimension, and its analysis.

**Escalate to wan-shi-tong when**:
- The question is about *causes* of war rather than its conduct (route to political-history)
- The question is about *economic* consequences of war (route to economic-history)
- The question is about *ideas* driving military change (route to intellectual-history)
- The question is about applying military history to present strategic decisions (route to applied-history)
