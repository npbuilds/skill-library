---
name: applied-history
description: >
  Route questions about using history as a practical tool for understanding the present
  and making decisions. Activate when users seek historical analogies, recurring patterns,
  lessons for current situations, or want to build timelines and argue both sides of
  historical debates.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Applied History — The Council Chamber

The Council Chamber is where history meets the present. This wing does not ask "what happened?" — the thematic wings handle that. It asks: "what does history *teach*?" and "how can historical reasoning improve decisions made today?" Applied history is the most powerful and most dangerous wing of Wan Shi Tong's library. Powerful because historical patterns genuinely recur. Dangerous because misapplied analogies have led to catastrophic decisions (Munich, Vietnam, Iraq).

The Council Chamber's core discipline: every analogy has *limits*. The skill is knowing where the analogy holds and where it breaks.

## Child Skills

| Skill | Type | Path | Handles |
|---|---|---|---|
| `historical-pattern-recognition` | knowledge | `historical-pattern-recognition/SKILL.md` | Identifying and evaluating recurring patterns: overstretch, traps, manias, cycles |
| `history-and-decision-making` | knowledge | `history-and-decision-making/SKILL.md` | Neustadt and May's "Thinking in Time," scenario planning, intelligence analysis |
| `timeline-builder` | action | `timeline-builder/SKILL.md` | Annotated visual timelines with causal connections |
| `debate-simulator` | action | `debate-simulator/SKILL.md` | Argue both sides of contested historical questions |
| `nexus-event-analyzer` | action | `nexus-event-analyzer/SKILL.md` | Multi-wing synthesis for events spanning all domains |

## Routing Table

| User Signal | Route To | Rationale |
|---|---|---|
| "Is this like," "does history repeat," "what pattern," "has this happened before" | `historical-pattern-recognition` | Pattern identification and evaluation |
| "What should we learn from," "what's the lesson," "how does history help us decide" | `history-and-decision-making` | Applied reasoning for decisions |
| "Give me a timeline of," "what's the sequence," "show me the chronology" | `timeline-builder` | Structured chronological output |
| "Argue both sides," "what would X say vs Y," "debate this" | `debate-simulator` | Structured multi-perspective argumentation |
| "How did the Industrial Revolution affect everything," "all dimensions of X" | `nexus-event-analyzer` | Multi-wing synthesis |

### Multi-Skill Questions

| Scenario | Load Order | Why |
|---|---|---|
| "Is the current US-China rivalry like the Thucydides Trap?" | historical-pattern-recognition → history-and-decision-making | First identify the pattern and its limits, then apply it to decision-making |
| "What can the 2008 financial crisis teach us about today?" | historical-pattern-recognition → (bridge to investing/archon) | Pattern recognition first, then cross-domain application |
| "Give me a comprehensive view of how decolonization reshaped the world" | nexus-event-analyzer → timeline-builder | Multi-wing synthesis first, then structured chronological output |

## Curriculum Order

1. **`historical-pattern-recognition`** (foundation) — Learn to see patterns AND their limits before applying them
2. **`history-and-decision-making`** (application) — Apply patterns to present decisions using structured frameworks
3. **`timeline-builder`** (tool) — Structure historical knowledge visually
4. **`debate-simulator`** (advanced) — Test understanding by arguing multiple positions
5. **`nexus-event-analyzer`** (synthesis) — The most complex skill; requires familiarity with all thematic wings

### Level Progression
- **Foundational**: historical-pattern-recognition
- **Intermediate**: history-and-decision-making, timeline-builder
- **Advanced**: debate-simulator, nexus-event-analyzer

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Pattern suggests X but specific case differs | Specific case wins | Patterns are heuristics; case evidence trumps general patterns |
| Two patterns apply but suggest different outcomes | Present both with confidence levels | Applied history is probabilistic, not deterministic |
| Historical analogy conflicts with domain-specific analysis | Defer to domain expert with historical context | History provides context, not overrides |

**General rule**: Analogies always have limits. Always name the limits alongside the analogy.

## Scope Boundaries

**This director handles**: Questions about what history teaches, how to use historical reasoning for present decisions, and structured historical analysis outputs.

**Escalate to wan-shi-tong when**:
- The question is about a specific historical event (route to thematic wing)
- The question is about historical methods (route to historiography)
- The question requires deep regional context (route to regional-atlas)