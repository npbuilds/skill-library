---
name: battle-analysis
description: >
  Produce structured analyses of historical battles and campaigns using the US Army Staff
  Ride methodology adapted for analytical learning. Use when the user wants to understand
  a specific battle's strategic context, force composition, terrain, plan versus execution,
  the decisive moment, and what it teaches about warfare and leadership.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Battle Analysis — The Staff Ride Method

This is an action skill that produces structured analyses of specific historical battles and campaigns. It adapts the US Army's Staff Ride methodology — designed to teach officers by walking battlefields — into an analytical framework that works without being on-site. The goal is not to narrate what happened but to understand *why* it happened and *what it teaches*.

Every battle analysis connects upward to strategic context (via `strategy-and-grand-strategy`) and outward to the technological/operational context (via `warfare-through-the-ages`).

## When This Applies

- User names a specific battle ("Tell me about Cannae / Stalingrad / Midway")
- User asks "what happened at [battle]" in an analytical rather than narrative mode
- User wants to understand why a battle was won or lost
- User wants to extract leadership or strategic lessons from a military engagement

## The Seven-Step Analysis

### Step 1 — Strategic Context

*Why was this battle fought? What were the political and military objectives?*

- What war is this part of? What are the belligerents' war aims?
- What is the campaign context? Where does this battle fit in the larger operational sequence?
- What were each side's strategic objectives for this engagement?

### Step 2 — Force Composition

*Who fought, and with what?*

- Approximate numbers for each side (infantry, cavalry, armor, air, naval)
- Quality factors: training, experience, morale, equipment condition
- Command structure: who was in charge? What was the command relationship?
- Logistics: supply situation, lines of communication, reinforcement availability

### Step 3 — Terrain and Conditions

*Where and when?*

- Key terrain features and their tactical significance
- Weather and its impact on operations
- Infrastructure: roads, bridges, communications, fortifications
- How did terrain advantage/disadvantage each side?

### Step 4 — Plans and Intentions

*What did each side intend to do?*

- Each commander's plan and its underlying assumptions
- What intelligence did each side have about the other?
- Where were the plans realistic? Where were they based on faulty assumptions?

### Step 5 — Execution

*What actually happened?*

- The key phases of the battle in chronological order
- Where did plans survive contact with reality? Where did they break down?
- What decisions were made under pressure? What were the alternatives?
- Clausewitz's friction: what went wrong that no one planned for?

### Step 6 — The Decisive Moment

*What determined the outcome?*

- Identify the turning point — the moment after which the outcome became likely
- Was it a command decision, a technological factor, a logistical reality, or chance?
- Could the losing side have changed the outcome? At what point did the battle become irreversible?

### Step 7 — Lessons and Legacy

*What does this battle teach?*

- What principles of strategy/tactics does it illustrate or complicate?
- How did this battle influence subsequent military thinking?
- What would a different decision at the decisive moment have changed?
- Connect to broader patterns: Does this illustrate offense-defense balance? Overstretch? Intelligence failure?

## Output Template

```
BATTLE: [Name, Date]
WAR/CAMPAIGN: [Context]
BELLIGERENTS: [Side A vs. Side B]

STRATEGIC CONTEXT:
  [Why this battle was fought; political/military objectives]

FORCES:
  [Side A]: [Numbers, composition, quality, commander]
  [Side B]: [Numbers, composition, quality, commander]

TERRAIN: [Key features and their significance]

PLANS:
  [Side A]: [What they intended]
  [Side B]: [What they intended]

EXECUTION:
  [Key phases chronologically; where plans broke down]

DECISIVE MOMENT:
  [The turning point and why it determined the outcome]

OUTCOME: [Winner, casualties, territorial result]

LESSONS:
  1. [Strategic/tactical principle illustrated]
  2. [Leadership lesson]
  3. [Connection to broader historical pattern]

LEGACY: [How this battle influenced subsequent history/thinking]
```

## Anti-Patterns

- **"Great man" fallacy**: Don't attribute outcomes solely to commander genius/failure — structural factors (logistics, terrain, technology, numbers) usually matter more
- **Hindsight bias**: Don't judge decisions by outcomes; judge them by what the commander reasonably knew at the time
- **Narrative smoothing**: Real battles are chaotic; resist the temptation to impose clean storylines on messy events
- **Ignoring the losers**: Analyze both sides; the losing side's decisions are often more instructive than the winner's
