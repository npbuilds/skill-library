---
name: value-architect
description: >
  Design the value exchange for intelligence products — not just pricing but the full model
  of how value flows between the system and its users. Handles free vs. paid, usage-based,
  capability-tiered, outcome-based, and subscription models. Addresses the unique challenge:
  how do you price something that gets better the more you use it?
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Value Architect — Designing How Value Flows

Pricing an intelligence product is unlike pricing software. Software delivers a fixed capability at a fixed price. Intelligence delivers a growing capability that improves with use. The value increases over time — for both sides.

This creates a design challenge traditional pricing models don't address: **the system gets more valuable to the user the longer they use it, AND the user gets more valuable to the system the more they contribute.**

## The Value Flow Model

Before pricing, map how value moves:

```
User → System: Usage data, feedback, behavioral signals, direct input
System → User: Intelligence, capability, personalization, time saved
System → System: Learning, capability compounding, pattern recognition
User → User: (Network effects, if applicable)
```

The value architecture must respect all four flows, not just the system→user transaction.

## Pricing Models for Intelligence

### Free Surface / Paid Depth

The surface layer is free. Deeper capability costs money.

| When | Risk | Mitigation |
|---|---|---|
| Core capability is enough to demonstrate value but depth is where real power lives | Free tier is too good — no conversion motivation | Make the depth genuinely different, not just "more of the same" |

**AI-native variant:** The free surface learns from use and becomes more valuable — but the depth of personalization and capability only unlocks with payment.

### Usage-Based

Pay for what you consume.

| When | Risk | Mitigation |
|---|---|---|
| Usage directly correlates with value received. Heavy users get more value. | Users ration usage to save money, reducing the system's ability to learn from them | Generous free tier for the learning loop; charge for output, not input |

**AI-native variant:** Charge for outputs (deliverables, analyses, artifacts) not inputs (questions, conversations). This aligns incentives — the user is paying for value delivered.

### Capability-Tiered

Different capability levels at different prices.

| When | Risk | Mitigation |
|---|---|---|
| Clear capability tiers exist (basic analysis vs. deep synthesis vs. cross-domain orchestration) | Users feel artificially limited. The intelligence COULD do more but WON'T. | Tiers should reflect genuine complexity, not artificial restriction |

**AI-native variant:** Tiers based on domain breadth — single-domain intelligence is one tier, cross-domain synthesis (The Loom's unique value) is a higher tier.

### Outcome-Based

Pay based on results achieved.

| When | Risk | Mitigation |
|---|---|---|
| Outcomes are measurable and attributable to the system | Attribution is hard. What if the user would have succeeded anyway? | Hybrid: base fee + outcome bonus. Or money-back guarantee if outcome not achieved. |

**AI-native variant:** The system tracks the outcomes its recommendations produce. Price adjusts based on demonstrated value. Radical alignment of incentives.

### Subscription

Fixed recurring payment.

| When | Risk | Mitigation |
|---|---|---|
| Ongoing relationship, continuous value, the default for most SaaS | Users forget they're paying. System has no incentive to improve for retained users. | Regular value demonstrations. "Here's what you got this month." |

**AI-native variant:** Subscription with value reporting — the system actively shows the user what it did for them each period. Not just features used, but value delivered.

## The Value Architecture Document

```markdown
# Value Architecture: {surface name}

## Value Flows
User → System: {what the system receives from use}
System → User: {what the user receives}
Compounding: {how value increases over time for both sides}

## Pricing Model
Primary: {model chosen}
Rationale: {why this model fits this intelligence surface}

## Tiers / Levels (if applicable)
{tier}: {what's included} — {price}

## Free Component
What's free: {what and why}
Why free: {learning loop value / demonstration / network effects}

## The Reflexivity Question
How does pricing affect behavior?
{Does the price signal quality? Does free usage reduce perceived value?
Does the pricing model incentivize the usage patterns that make the system better?}

## Anti-Models
{Pricing models explicitly rejected and why}
```

## Cross-Domain Synthesis

Value architecture is the most cross-domain product decision:

- **game-theory/mechanism-design** — Pricing IS mechanism design. Is the pricing incentive-compatible? Does it produce honest behavior?
- **archon (investing)** — Market positioning through price. What does the price signal about the product's nature?
- **prose-orchestrator** — Value framing. The words used to present pricing shape perception as much as the numbers.
- **investing/reflexivity** — Price affects perception affects value affects price. The reflexive loop in pricing intelligence.
