---
name: emergence-detector
description: >
  Monitor the skill library for unexpected capability combinations — behaviors that emerge
  from cross-domain interaction that nobody explicitly designed. Use when you notice the
  system doing something surprising, when domains produce unexpected synergies, or when
  you want to proactively scan for emergent product opportunities hiding in the library.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep Agent
---

# Emergence Detector — The Surprise Sensor

The most valuable product behaviors are often ones nobody designed. They emerge from the interaction of capabilities in ways that surprise even the builder. This skill watches for those surprises.

Emergence is the core thesis of AI-native product design: if you create the right conditions, intelligence produces behaviors more valuable than anything you could have specified.

## What Counts as Emergence

**Emergence IS:**
- Two domains producing a result neither could alone (design + game-theory → incentive-aligned UX)
- A skill being used for purposes beyond its original design (sommelier tasting grid applied to coffee evaluation)
- Unexpected user behaviors that reveal latent system capability
- Capability combinations that feel obvious in retrospect but weren't planned

**Emergence IS NOT:**
- A skill working as designed (that's just function)
- An obvious combination that was intended (that's architecture)
- A bug that happens to be useful (that's serendipity — note it, but don't confuse it with emergence)

## Detection Methods

### Passive Detection — Reading the Traces

Scan for emergence signals in existing data:

1. **Usage patterns** — Read `data/usage.jsonl`. Look for skills being invoked in unusual combinations or by unexpected orchestrators.
2. **Cross-domain references** — Read `data/registry.json`. Find `depends_on` chains that span 3+ domains. These are emergence-prone zones.
3. **Gap log anomalies** — Read `data/gaps.jsonl`. When the same gap is flagged from multiple domains, it may indicate an emergent need.
4. **Feedback patterns** — Read `data/feedback.jsonl`. Positive feedback on unexpected skill combinations.

### Active Detection — Probing for Combinations

When asked to scan proactively:

1. **Identify high-connectivity skills** — Skills with many cross-domain `referenced_by` entries are emergence catalysts.
2. **Map untested combinations** — Which domain pairs have never been combined in a product context? These are the blind spots.
3. **Stress-test boundaries** — Take a domain's methodology and apply it to a completely different domain. What happens when you apply sommelier's deductive tasting grid to evaluating code quality? What happens when you apply investing's regime intelligence to content strategy?

### User-Reported Detection

When the user says "I noticed something unexpected":

1. **Characterize the surprise** — What happened? What did you expect instead?
2. **Trace the cause** — Which capabilities interacted to produce this behavior?
3. **Assess reproducibility** — Can you recreate it? Is it stable or was it a one-off?
4. **Rate the value** — Is this emergent behavior useful? More useful than the designed behavior?

## Output

Log each emergence event to `loom-briefings/emergence-log.md`:

```markdown
## Emergence: {descriptive name}
**Detected:** {date}
**Method:** {passive/active/user-reported}
**Domains involved:** {which domains interacted}
**What happened:** {description of the emergent behavior}
**Why it's surprising:** {what was expected vs. what occurred}
**Reproducible:** {yes/partially/unknown}
**Value assessment:** {high/medium/low — why}
**Product implication:** {what this means for product surfaces}
**Recommended action:** {amplify / investigate further / note and watch}
```

## Connection to The Loom Cycle

Emergence detection feeds directly into:
- **Envision** (possibility-mapper) — emergent behaviors expand the possibility space
- **Evolve** (amplifier) — confirmed valuable emergence should be amplified
- **Synthesize** (pattern-weaver) — emergence across products may reveal meta-patterns
