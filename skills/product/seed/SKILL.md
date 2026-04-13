---
name: seed
description: >
  Route product seeding work — designing initial conditions for product emergence, sculpting
  constraints that channel behavior productively, growing rapid capability prototypes, and
  architecting the feedback loops that will shape the product's evolution. Activates when the
  question transitions from "what should we build?" to "how do we create conditions for it to emerge?"
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write Bash Glob Grep Agent
---

# Seed — The Cultivation Engine

The paradigm shift: you don't spec and build an intelligence product. You design **initial conditions** — capabilities to combine, constraints to impose, feedback loops to listen to, and space to leave open — then observe what emerges.

Seed receives a thesis and seed requirements from Envision, and produces a living prototype with designed feedback loops. The product is planted, not manufactured.

## Child Skills

| Skill | Type | When to Route |
|---|---|---|
| `condition-designer` | action | Designing initial conditions for a product: capabilities, constraints, openings |
| `constraint-sculptor` | knowledge | Frameworks for using constraints creatively to channel emergence |
| `prototype-grower` | action | Rapid capability prototyping — living demos, not wireframes |
| `feedback-architect` | action | Designing the feedback loops that shape evolution |

## Routing Logic

| Signal | Route To |
|---|---|
| "How do we start?", "initial conditions", "what to combine" | condition-designer |
| "Too broad", "constrain this", "scope", "boundaries", "rails" | constraint-sculptor |
| "Show me", "prototype", "demo", "what would this look like alive?" | prototype-grower |
| "What signals to watch?", "how will we know?", "feedback", "metrics" | feedback-architect |
| "Full seed specification" | condition-designer → constraint-sculptor → feedback-architect → prototype-grower |

## Curriculum Order

```
constraint-sculptor (understand constraints) → condition-designer (design conditions)
→ feedback-architect (design loops) → prototype-grower (grow the prototype)
```

## The Seed → Surface Handoff

When a seed has germinated and shows emergence, the handoff to Surface includes:
1. The prototype and its observed behaviors
2. Feedback signals collected so far
3. Which emergent behaviors to amplify vs. which to constrain
4. The thesis (from Envision) for context
