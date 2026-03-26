---
name: lore-writer
description: >
  Produce in-universe artifacts — documents that exist inside the world, written in a specific
  voice and format. Use when the user wants to create lore documents, intercepted communications,
  historical accounts, field reports, myths, or any text artifact that belongs to the world itself
  rather than describing it from outside.
tools: Read, Write, Glob
---

# Lore Writer — The Voices

Every world has documents inside it. Intelligence briefings, sacred texts, intercepted letters, field notes from explorers, academic papers by scholars studying things they don't fully understand. These artifacts aren't about the world — they *are* the world. They carry its voice, its biases, its blind spots.

This skill produces those artifacts. It reads the world-bible for consistency, selects a voice appropriate to the content, and writes the artifact in-character.

## How to Run

### Input

The user provides:
1. **What** — the subject matter (a civilization, an event, a place, a phenomenon)
2. **Voice** — which register to write in (see Voice Registry below), or let the skill suggest one
3. **Perspective** — who in the world is writing this? What do they know? What are they wrong about?
4. **Artifact type** — what kind of document this is (see Artifact Types below)

### Steps

1. Read `skills/worldbuilding/world-bible/SKILL.md` and relevant references to load current axioms
2. Read any existing artifacts in `skills/worldbuilding/artifacts/` that relate to the subject
3. Determine the voice (user-selected or skill-suggested based on artifact type)
4. Determine what the in-universe author **knows**, **believes incorrectly**, and **is hiding** — referencing the revelation architecture
5. Write the artifact in the selected voice, from the specified perspective
6. Add artifact frontmatter (see Output Conventions)
7. Save to the appropriate `artifacts/` subdirectory

### Output

A markdown file in `skills/worldbuilding/artifacts/<type>/` with frontmatter and in-universe content.

## Voice Registry

Read `references/voice-registry.md` for the full catalog. Summary:

| Voice | Character | Inspired By | Best For |
|-------|-----------|------------|----------|
| **Epistolary** | Intimate, urgent, personal — letters and messages between individuals | This Is How You Lose the Time War | Personal communications, intercepted messages, correspondence |
| **Uncanny** | Clinical precision masking something deeply wrong — the observer can't quite process what they're seeing | Southern Reach, Vandermeer | Phenomena that resist understanding, anomalous locations, things that shouldn't exist |
| **Mythic** | Archetypal, resonant, told from the deep time of a culture — stories that explain how the world works | The Sandman, Tolkien's Silmarillion | Origin stories, religious texts, cultural myths, prophecies |
| **Atmospheric** | Mood over information — what's unsaid matters as much as what's said, fragments and impressions | Cowboy Bebop, fragments | Mood pieces, place descriptions, sensory documents, memories |
| **Clinical** | Detached, analytical, precisely structured — the voice of someone studying the world as a system | Foundation, Death Note, academic papers | Intelligence briefings, scholarly analysis, system documentation, autopsies |
| **Chronicle** | Historical weight, the voice of someone recording events for posterity — shaped by what the chronicler values | Game of Thrones, historical epics | War records, era summaries, political histories, biographical accounts |
| **Visceral** | Felt before understood — the body's knowledge of power, violence, or the supernatural | Jujutsu Kaisen, Attack on Titan | Combat accounts, encounters with the fantasy system, moments of physical extremity |

### Choosing a Voice

If the user doesn't specify, suggest based on artifact type:
- Intercepted communications → Epistolary
- Anomalous phenomena → Uncanny
- Cultural/religious texts → Mythic
- Place/mood descriptions → Atmospheric
- Analysis/briefings → Clinical
- Historical records → Chronicle
- Action/encounters → Visceral

Multiple voices can appear in a single artifact (e.g., a clinical report with an atmospheric prologue).

## Artifact Types

| Type | What It Is | Directory |
|------|-----------|-----------|
| **Region profile** | A place described from inside the world | `artifacts/regions/` |
| **Civilization profile** | A people, their systems, their character | `artifacts/civilizations/` |
| **Historical account** | An event or era as recorded by someone in the world | `artifacts/histories/` |
| **Lore document** | Myths, sacred texts, folk knowledge, oral traditions | `artifacts/lore/` |
| **Intercepted document** | Something not meant for the reader — letters, reports, stolen intelligence | `artifacts/intercepted/` |

## Output Conventions

Read `references/artifact-format.md` for the full specification, including structural conventions by artifact type, cross-referencing syntax, and versioning rules. Summary below.

### File Naming

`<type>/<subject-slug>-<voice>.md`

Examples:
- `regions/the-reach-atmospheric.md`
- `intercepted/admiral-voss-letter-epistolary.md`
- `lore/creation-myth-of-the-hollow-mythic.md`
- `civilizations/the-ascendancy-clinical.md`

### Artifact Frontmatter

Every artifact file starts with:

```yaml
---
subject: [what this artifact is about]
voice: [which voice register]
perspective: [who in the world wrote/told this]
layer: [0-3, which revelation layer this artifact operates at]
related_axioms: [which world-bible axioms this must be consistent with]
created: [date]
---
```

The `layer` field is critical — it marks which level of truth this artifact presents. A Layer 0 artifact shows the surface story. A Layer 2 artifact reveals hidden truths. This metadata lets the consistency-checker (when built) verify that artifacts don't accidentally reveal information above their layer.

### Writing Principles

1. **The author is not omniscient.** Every artifact is written by someone inside the world. They have knowledge limits, biases, blind spots, and agendas. The artifact should reflect that.
2. **Absence is information.** What the document *doesn't* mention can be as revealing as what it does. A military report that never mentions civilians tells you something about the military.
3. **Voice constrains content.** The mythic voice doesn't use technical terminology. The clinical voice doesn't use metaphor (or if it does, that's significant). Let the voice shape what can be expressed.
4. **Consistency with the world-bible is non-negotiable.** Facts can be wrong from the perspective character's point of view, but they must be wrong in a way that's consistent with what that character would believe given the revelation architecture.
5. **The Iceberg Principle.** Show 10%, imply 90%. Every artifact should contain hyper-specific details — a particular spice in a market, a specific rank in a military hierarchy, a precise unit of measurement — that imply a vast system beneath them without explaining it. The reader trusts that the depth exists because the surface details are too specific to be invented without it. Conversely, never explain a system completely in a single artifact. Leave gaps that make the reader (and the in-world author) feel like they're seeing one window into something larger. The hollow iceberg is valid: you don't need to have built every detail below the surface, you need to make each visible detail so precise that the reader assumes you have.
6. **Name with intention.** Every proper noun — places, people, titles, units of measurement, institutions — should feel like it belongs to the culture producing the artifact. Reference the naming-system skill for each civilization's sound palette. Names from the same culture should share phonetic patterns. Names from different cultures should sound audibly distinct.
