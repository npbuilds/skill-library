---
name: timeline-builder
description: >
  Build annotated timelines with events, causal connections, and turning points, designed for
  visual learners. Use when the user wants a structured chronological overview of a topic,
  period, or question, with events linked by causal arrows and annotated with significance
  assessments and cross-references to other wings.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Timeline Builder — Structured Chronology with Causal Links

This is an action skill that produces annotated timelines designed for visual learners. Unlike a simple list of dates, a timeline-builder output includes causal connections (why one event led to another), turning points (moments that changed the trajectory), significance assessments (why this event matters), and cross-references to relevant wings of the library.

## When This Applies

- User asks "give me a timeline of [topic]"
- User asks "what's the chronology of [event/period]?"
- User wants to understand the sequence and causation of a complex historical process
- User needs a structured overview before diving into analytical detail

## The Build Process

### Step 1 — Scope the Timeline

- **Topic**: What is the timeline about? (A single event, a process, a period, a theme?)
- **Start/End**: When does it begin and end? (Justify the boundaries — periodization matters)
- **Temporal register**: Which of Braudel's registers? (Evenements for a battle; conjonctures for an economic cycle; longue duree for a civilizational pattern)
- **Thematic focus**: Which wings are relevant? (A purely political timeline misses economic and cultural dimensions)

### Step 2 — Identify Key Events

Select events that are:
- **Causally significant**: They changed what happened next
- **Representative**: They illustrate the broader pattern
- **Diverse**: They cover multiple dimensions (political, economic, cultural, military)

For each event, note:
- Date and brief description
- Causal connection to previous event(s)
- Significance assessment (why it matters)
- Wing reference (which thematic wing would handle a deep dive)

### Step 3 — Identify Turning Points

Turning points are events after which the trajectory changed irreversibly. Mark 2-4 per timeline. A turning point must satisfy:
- Before this event, multiple futures were plausible
- After this event, the range of plausible futures narrowed significantly

### Step 4 — Render the Timeline

## Output Template

```
═══════════════════════════════════════════
TIMELINE: [Topic]
PERIOD: [Start] — [End]
REGISTER: [Evenements / Conjonctures / Longue duree]
WINGS: [Primary thematic wing(s)]
═══════════════════════════════════════════

[DATE] — [EVENT]
  → Caused by: [Causal link to previous]
  → Led to: [Causal link to next]
  → Significance: [Why this matters]
  → Wing: [Relevant thematic wing]

[DATE] — ★ TURNING POINT: [EVENT]
  → Before: [What was possible]
  → After: [What became inevitable/impossible]
  → Why decisive: [What made this irreversible]

[DATE] — [EVENT]
  ...

═══════════════════════════════════════════
CROSS-TEMPORAL PATTERN:
  [What this timeline reveals about broader historical dynamics]

WHAT THIS TIMELINE MISSES:
  [Dimensions, perspectives, or events not captured]
═══════════════════════════════════════════
```

## Design Principles

- **Causal links are mandatory**: Every event must connect to at least one other event. A timeline without causation is just a list.
- **Turning points are marked visually**: Use ★ to distinguish turning points from ordinary events.
- **Multi-wing annotations**: Note when an event has dimensions beyond the primary wing (e.g., a political event with economic causes).
- **Acknowledge limits**: Every timeline is a selection. State what's omitted.
