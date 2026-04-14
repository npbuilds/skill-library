---
name: feedback-architect
description: >
  Design the feedback loops that will shape a product's evolution. The feedback architecture
  IS the growth plan — what signals the system listens to, how it adapts, what reinforces
  good behavior, what dampens bad behavior. Use when designing how a product learns and
  improves from use.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Feedback Architect — Designing How Products Learn

In traditional product design, the architecture is the code structure. In intelligence products, the architecture is the **feedback loops**. What the system pays attention to and how it responds determines what the product becomes over time.

Design the loops, and the product designs itself.

## Feedback Loop Anatomy

Every feedback loop has four components:

```
Signal → Sensor → Response → Effect → (back to Signal)
```

- **Signal** — What's happening in the world (user behavior, usage pattern, outcome quality)
- **Sensor** — How the system detects the signal (metrics, observation, explicit feedback)
- **Response** — How the system reacts (amplify, dampen, adjust, alert)
- **Effect** — What changes in the product as a result

## Loop Types

### Reinforcing Loops (Virtuous Cycles)

The system gets better because people use it, and people use it because it's getting better.

**Example:** User provides feedback on writing quality → system adjusts voice → output improves → user provides more feedback → system improves further

**Design principle:** Reinforcing loops are powerful but dangerous. Unchecked, they can spiral toward extremes. Always pair with a balancing loop.

### Balancing Loops (Stability Mechanisms)

The system self-corrects when it drifts too far in one direction.

**Example:** System detects it's becoming too verbose → triggers compression → output gets more concise → if too concise, triggers expansion

**Design principle:** Balancing loops prevent pathological behavior. Every reinforcing loop needs at least one balancing counterpart.

### Learning Loops (Capability Improvement)

The system develops new capabilities or refines existing ones through accumulated experience.

**Example:** Pattern of questions the system can't answer → gap detection → triggers skill development → new capability added → gap closed

**Design principle:** Learning loops operate on longer timescales than reinforcing/balancing loops. They change what the system CAN do, not just how well it does it.

## The Feedback Architecture Document

For each seeded initiative, produce:

```markdown
# Feedback Architecture: {initiative name}

## Primary Loop
Type: {reinforcing/balancing/learning}
Signal: {what triggers it}
Sensor: {how we detect it}
Response: {what changes}
Effect: {what the user experiences}
Health check: {how we know the loop is working}

## Supporting Loops
{Additional loops with same structure}

## Balancing Mechanisms
{What prevents runaway reinforcement}

## Observation Points
{Where and when to check loop health}
Frequency: {how often}
Metrics: {what to measure}

## Failure Modes
{What happens if loops malfunction}
Dead loop: {signal exists but sensor misses it}
Runaway: {reinforcing loop without balancing counterpart}
Stale loop: {loop was relevant but environment changed}
```

## Design Process

### Step 1 — Identify Natural Signals

What signals will the product naturally generate?
- Usage frequency and patterns
- Output quality (can it be measured?)
- User explicit feedback (thumbs up/down, corrections, abandonment)
- Downstream effects (did the user act on the output?)

### Step 2 — Design Sensors

For each signal, how does the system detect it?
- Automatic: usage logs, behavioral data
- Prompted: occasional "was this helpful?" checks
- Inferred: user behavior as implicit signal (editing output = dissatisfaction, sharing output = satisfaction)

### Step 3 — Specify Responses

What should change when the signal is detected?
- Parameter adjustment (tone, depth, format)
- Capability routing (different skill engagement)
- Exposure change (surface more or less)
- Alert (flag for human attention)

### Step 4 — Pair Reinforcing with Balancing

For every reinforcing loop, identify:
- What extreme it could spiral toward
- What balancing mechanism prevents it
- What the healthy operating range is

## Cross-Domain

- **data-science-orchestrator** — For quantitative feedback signals and metric design. "What should we measure and how?"
- **game-theory-orchestrator** — For incentive-compatible feedback design. "Will this feedback mechanism produce honest signals or gaming behavior?"
