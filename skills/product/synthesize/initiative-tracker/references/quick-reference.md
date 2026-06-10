# Initiative Tracker — Quick Reference


## Transition Rules

| From → To | Graduation Criteria | Who Decides |
|---|---|---|
| seed → germinating | Thesis crystallized (via thesis-forge). Initial conditions designed. At least one feedback loop specified. | The Loom |
| germinating → emerging | Prototype exists (via prototype-grower). At least one unexpected behavior observed. Signal strength above noise. | Sense (emergence-detector) |
| emerging → surfaced | Behavior is stable enough for external interaction. Interface form chosen (via interface-philosopher). Exposure strategy defined. | Surface (exposure-strategist) |
| surfaced → evolving | Real usage generating real feedback. Adaptation signals detected. The system is changing from use. | Evolve (adaptation-observer) |
| evolving → mature | Growth rate stabilizing. Self-sustaining feedback loops. Minimal manual intervention needed. | Evolve (learning-loops) |
| Any → composted | Decision to retire. Learnings documented. Reusable capabilities preserved. | The Loom (with pruning-engine) |

## Quick Reference

| Backward Move | When |
|---|---|
| surfaced → germinating | The surface form is wrong. Need to redesign conditions. |
| emerging → seed | What emerged isn't what we wanted. Rethink the thesis. |
| evolving → surfaced | Growth stalled. May need to re-expose differently. |

## Quick Reference

| Skip | When |
|---|---|
| seed → emerging | The capability already exists and is already showing emergent behavior. Just needs recognition. |
| seed → surfaced | Mature capability from another domain. Just needs a surface. |

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

## Formula / Pseudocode

```
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

## Formula / Pseudocode

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
