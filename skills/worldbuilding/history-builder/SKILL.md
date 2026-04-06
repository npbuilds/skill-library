---
name: history-builder
description: >
  Build fictional history non-chronologically using fractal zoom — jump to any era, define
  events at any scale, and let the narrative emerge from the gaps. Based on the Microscope RPG
  methodology. Use when creating timelines, defining eras, or building historical depth for
  civilizations.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Glob
---

# History Builder — The Fractal Zoom

History is not built chronologically. You don't start at year 1 and write forward — you start with whatever interests you and fill in the gaps. The most interesting part of your world's history might be 3,000 years ago, or it might be last Tuesday. The Microscope method lets you jump to any point and work at any scale.

This skill produces history artifacts and maintains a master timeline.

## How to Run

### Input

The user provides one of:
1. **Define a Period** — a broad sweep of history (decades to millennia)
2. **Define an Event** — something that happened within a period (days to years)
3. **Zoom into a Scene** — a specific moment within an event (minutes to hours)
4. **Query the timeline** — "What happened between [era A] and [era B]?" or "What do we know about [civilization] during [period]?"

### Steps

1. Read the master timeline from `artifacts/meta/timeline.md` (create if it doesn't exist)
2. Read the world-bible for axioms and revelation layers
3. Read any existing history artifacts that relate to the same era/civilization
4. Perform the requested operation
5. If producing a new history artifact, use the lore-writer's chronicle or mythic voice
6. Update the master timeline
7. Save artifacts to `artifacts/histories/`

### Output

A history artifact in `artifacts/histories/` and an updated master timeline in `artifacts/meta/timeline.md`.

## The Three Scales

History operates at three fractal levels. You can start at any level and zoom in or out:

```
PERIOD ──────────────────────────────────────────────────
  "The Age of Expansion" (centuries)
  Tone: Light or Dark (was this broadly good or bad?)
  │
  ├── EVENT ─────────────────────────────────────────────
  │     "The Founding of the Second Compact" (years)
  │     Tone: Light or Dark
  │     │
  │     ├── SCENE ───────────────────────────────────────
  │     │     "The night the Compact was signed" (hours)
  │     │     Characters present. What was said.
  │     │     What was left unsaid.
  │     │
  │     └── SCENE
  │           "The assassination attempt that almost
  │            prevented it" (minutes)
  │
  ├── EVENT
  │     "The Collapse of the Northern Routes" (decades)
  │     Tone: Dark
  │
  └── EVENT
        "First Contact with the Deep" (days)
        Tone: Dark
```

### Period Design

A period is a **broad sweep** — an era with a character. It answers: "What was the world like during this time?"

| Field | Description |
|-------|-------------|
| Name | Evocative, not technical ("The Silence," not "Period 3") |
| Span | Approximate duration (centuries, decades, a single generation) |
| Tone | Light (things got better) or Dark (things got worse) — simple binary |
| One-line summary | What defines this era in one sentence |
| Bookends | What event starts it? What event ends it? |

### Event Design

An event is a **specific thing that happened** within a period. It has consequences.

| Field | Description |
|-------|-------------|
| Name | What happened, stated clearly |
| When | Where in the period this falls |
| Tone | Light or Dark |
| Cause | What led to this (may reference another event) |
| Consequence | What this caused (may reference another event or period) |
| Who was involved | Civilizations, factions, key figures |
| What was lost | Every event should cost something |

### Scene Design

A scene is a **moment** — the smallest unit of history. It's where history becomes personal.

| Field | Description |
|-------|-------------|
| Setting | Where and when, specifically |
| Characters present | Named individuals, with their belief states |
| The question | What's being decided or revealed in this scene? |
| What happened | The actual moment |
| What was hidden | What was happening that the participants didn't know (revelation layer) |

## The Master Timeline

The timeline lives at `artifacts/meta/timeline.md` and serves as the index for all history artifacts:

```markdown
# Master Timeline

## Periods (chronological)

| # | Period | Span | Tone | Events | Artifacts |
|---|--------|------|------|--------|-----------|
| 1 | The Seeding | ~10,000 years ago | Light | 2 | founding-myth-mythic.md |
| 2 | The Age of Expansion | ~3,000 years ago | Light | 4 | expansion-chronicle.md |
| 3 | The Silence | ~800 years ago | Dark | 3 | the-silence-uncanny.md |
| 4 | The Second Compact | ~200 years ago | Light | 5 | compact-signing-chronicle.md |
| 5 | The Current Era | Now | ??? | ongoing | — |

## Gaps (periods with no events yet)

- Between The Seeding and The Age of Expansion (~7,000 years unaccounted)
- Between The Silence and The Second Compact (~600 years unaccounted)
```

### Gaps Are Features

An empty space in the timeline is not a problem — it's a creative prompt. The gap between two defined periods is where the most interesting history might live. The history-builder tracks gaps explicitly so you can fill them when inspiration strikes.

## Non-Chronological Building

The core principle: **you do not need to build in order.** The workflow is:

1. Define whatever period interests you right now
2. Place it on the timeline (before, after, or between existing periods)
3. Add events within it
4. Zoom into scenes if a moment feels important
5. Notice: the gaps between your defined periods imply things. What happened between "The Age of Expansion" and "The Silence"? You'll know when you need to.

This mirrors how real historians work — they don't start at the beginning. They start with what they have evidence for and reconstruct the gaps.

## History and Revelation Architecture

Every historical element has a revelation layer:

- **Layer 0**: The commonly accepted version — what textbooks say
- **Layer 1**: What scholars notice doesn't add up — contradictions in the record
- **Layer 2**: What was deliberately suppressed — the victors' edits
- **Layer 3**: What actually happened — the truth beneath the myth

When building history, define the **Layer 3 truth first**, then build the layers of distortion on top. This ensures the hidden history is coherent, not a last-minute twist.

## Integration with Other Skills

- **world-bible**: History must respect axioms (if no FTL, empires fragment; the history should show this)
- **lore-writer**: Produces the actual history artifacts in voice (chronicle for records, mythic for origin stories, clinical for analyses)
- **character-belief-tracker**: Characters alive during historical events have beliefs shaped by which layer they've access to
- **religion-design**: Religions rewrite history to serve their narratives; religious history is always Layer 0 with deeper truths beneath
