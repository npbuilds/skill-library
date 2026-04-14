---
name: initiative-tracker
description: >
  Track product initiatives through their organic lifecycle — from seed to compost. Maintains
  the initiative log with state transitions, learnings, and portfolio-level views. Use when
  checking initiative status, recording state changes, reviewing the portfolio pipeline, or
  understanding what's in flight, what's stuck, and what's been composted.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep
---

# Initiative Tracker — The Living Ledger

Tracks every product initiative through its organic lifecycle. Not a project management tool — a cultivation journal that remembers what was planted, what grew, what was composted, and what the soil learned from each.

## Initiative Lifecycle

```
seed        → An idea planted. A thesis exists but nothing else.
germinating → Conditions designed. Feedback loops specified. Prototype growing.
emerging    → Something is working. Unexpected behaviors appearing. Signal detected.
surfaced    → Capability exposed to the world. Humans/agents can interact with it.
evolving    → Growing from use. Adapting. Developing new behaviors.
mature      → Stable, self-sustaining. The system knows how to do this well.
composted   → Retired. Learnings extracted and fed back into Sense.
```

### Transition Rules

| From → To | Graduation Criteria | Who Decides |
|---|---|---|
| seed → germinating | Thesis crystallized (via thesis-forge). Initial conditions designed. At least one feedback loop specified. | The Loom |
| germinating → emerging | Prototype exists (via prototype-grower). At least one unexpected behavior observed. Signal strength above noise. | Sense (emergence-detector) |
| emerging → surfaced | Behavior is stable enough for external interaction. Interface form chosen (via interface-philosopher). Exposure strategy defined. | Surface (exposure-strategist) |
| surfaced → evolving | Real usage generating real feedback. Adaptation signals detected. The system is changing from use. | Evolve (adaptation-observer) |
| evolving → mature | Growth rate stabilizing. Self-sustaining feedback loops. Minimal manual intervention needed. | Evolve (learning-loops) |
| Any → composted | Decision to retire. Learnings documented. Reusable capabilities preserved. | The Loom (with pruning-engine) |

### Backward Transitions

Initiatives can move backward:

| Backward Move | When |
|---|---|
| surfaced → germinating | The surface form is wrong. Need to redesign conditions. |
| emerging → seed | What emerged isn't what we wanted. Rethink the thesis. |
| evolving → surfaced | Growth stalled. May need to re-expose differently. |

### Skip Transitions

Initiatives can skip states:

| Skip | When |
|---|---|
| seed → emerging | The capability already exists and is already showing emergent behavior. Just needs recognition. |
| seed → surfaced | Mature capability from another domain. Just needs a surface. |

## Initiative Record Format

Each initiative in `loom-briefings/initiative-log.md`:

```markdown
## {Initiative Name}

**Thesis:** {One-sentence falsifiable thesis}
**State:** {current lifecycle state}
**Domains involved:** {list of domain orchestrators engaged}
**Seeded:** {date}
**Last transition:** {state} → {state} on {date}

### Transitions
- {date}: seed → germinating — {reason}
- {date}: germinating → emerging — {reason}

### Key Learnings
- {learning from this initiative}

### Kill Criteria
- {what would falsify the thesis}

### Open Questions
- {thing we still need to learn}
```

## Portfolio Views

When asked for portfolio status, produce:

```
=== INITIATIVE PORTFOLIO ===
Date: {today}

Seeded:      {count} — {names}
Germinating: {count} — {names}
Emerging:    {count} — {names}
Surfaced:    {count} — {names}
Evolving:    {count} — {names}
Mature:      {count} — {names}
Composted:   {count} (last 90 days)

--- Attention Needed ---
{initiatives stuck in one state too long}
{initiatives with unresolved kill criteria}
{initiatives missing key learnings documentation}

--- Pipeline Health ---
Throughput: {initiatives that transitioned this week}
Oldest seed: {name, days since seeded}
Most active: {name, transitions this month}
```

## Operating Rules

1. **Every transition gets a reason.** No silent state changes. The reason is the learning.
2. **Composted initiatives get a full retrospective.** What was the thesis? Was it validated or invalidated? What capabilities survived? What did the soil learn?
3. **Stuck is a signal.** If an initiative hasn't transitioned in 3+ weeks, flag it. Either it needs energy or it needs composting.
4. **Kill criteria are sacred.** If an initiative's kill criteria are met, it gets composted. No exceptions, no "one more week."
5. **The log is append-only.** Never delete history. The record of what was tried and what was learned is the most valuable artifact.
