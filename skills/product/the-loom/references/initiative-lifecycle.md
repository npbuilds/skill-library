# Initiative Lifecycle — Organic States and Graduation Criteria

## The States

```
seed → germinating → emerging → surfaced → evolving → mature → composted
```

## State Definitions and Graduation Criteria

### Seed
**Definition:** An idea planted. A thesis exists, possibly from thesis-forge, possibly from a conversation. Nothing else.

**What exists:** A thesis statement with kill criteria. Maybe notes. No prototype, no conditions designed.

**Graduate to Germinating when:**
- [ ] Thesis crystallized and written down (via thesis-forge)
- [ ] At least one domain orchestrator identified as capability ingredient
- [ ] Kill criteria specified and committed to in advance

### Germinating
**Definition:** Conditions designed. The seed has a specification, feedback loops, and possibly a prototype.

**What exists:** Seed specification (from condition-designer), feedback architecture (from feedback-architect), possibly a prototype (from prototype-grower).

**Graduate to Emerging when:**
- [ ] Prototype exists and has been run at least once
- [ ] At least one unexpected behavior observed (emergence signal)
- [ ] Primary feedback signal is producing data
- [ ] Observation: the capability combination produces something neither domain could alone

### Emerging
**Definition:** Something is working. Behaviors are appearing that weren't explicitly designed. Signals are coming in.

**What exists:** A working prototype with observed emergent behavior. Feedback signals. Early indication of thesis validity.

**Graduate to Surfaced when:**
- [ ] Behavior is stable enough for external interaction (not just demo-quality)
- [ ] Interface form chosen (via interface-philosopher)
- [ ] Exposure plan defined (via exposure-strategist)
- [ ] Experience brief created (via experience-weaver)
- [ ] Value architecture at least sketched (via value-architect)

### Surfaced
**Definition:** The capability is exposed to the world. Humans or agents can interact with it.

**What exists:** A live capability surface with designed experience, exposure plan, and feedback loops active.

**Graduate to Evolving when:**
- [ ] Real usage occurring (not just testing)
- [ ] Feedback loops are generating genuine signals
- [ ] At least one adaptation observed (behavior changing from use)
- [ ] User behavior diverges from designer expectations in at least one way

### Evolving
**Definition:** Growing from use. The product is alive — adapting, developing new behaviors, responding to feedback.

**What exists:** Active usage, running feedback loops, observable adaptation, amplification and pruning decisions being made.

**Graduate to Mature when:**
- [ ] Growth rate stabilizing (not zero — stable)
- [ ] Self-sustaining feedback loops (minimal manual intervention)
- [ ] Core thesis validated (original kill criteria not triggered, positive evidence accumulated)
- [ ] User trust established (repeated use, reliance, would-miss-it-if-gone)

### Mature
**Definition:** Stable, self-sustaining. The system knows how to do this well. Requires maintenance, not cultivation.

**What exists:** Reliable capability surface with established user patterns, working feedback loops, stable behavior.

**Note:** Mature does not mean finished. Mature means the cultivation phase is over — the product now maintains itself through its feedback architecture. It can still improve and evolve, but it doesn't need active seeding or shaping.

### Composted
**Definition:** Retired. But not wasted. Learnings extracted and fed back into the system.

**What must happen before composting:**
- [ ] Full retrospective written (narrative-keeper)
- [ ] Learnings documented: What was the thesis? Validated or invalidated? What capabilities survived?
- [ ] Reusable capabilities identified and preserved
- [ ] Emergence log updated with any patterns observed during the initiative's life
- [ ] Decision journal updated with the composting decision and reasoning

## Backward Transitions

| From → To | When | Action Required |
|---|---|---|
| surfaced → germinating | Surface form is wrong. Behavior is right, interface is wrong. | Redesign conditions and exposure plan. Prototype-grower may re-engage. |
| emerging → seed | What emerged isn't what we wanted. Thesis may be wrong. | Re-evaluate thesis. May need thesis-forge again. |
| evolving → surfaced | Growth stalled. Feedback loops may be miscalibrated. | Re-examine feedback architecture. May need new exposure strategy. |
| mature → evolving | External change (frontier shift, market change) disrupts stability. | Active cultivation resumes. |

## Skip Transitions

| Skip | When | Validation |
|---|---|---|
| seed → emerging | Capability already exists and shows emergent behavior. Just needs recognition. | Confirm the emergence is genuine and the thesis is articulated. |
| seed → surfaced | Mature capability from another domain that just needs a product surface. | Confirm readiness and create exposure plan. |
| germinating → surfaced | Prototype is immediately good enough for external interaction. | Confirm stability and create minimal exposure plan. |

## Attention Flags

| Condition | Flag |
|---|---|
| Initiative in seed state > 2 weeks | **Stale seed.** Either germinate it or compost it. Seeds that sit too long lose relevance. |
| Initiative in germinating state > 4 weeks | **Slow germination.** Check: are conditions right? Is the thesis too ambitious? |
| Initiative in emerging state > 3 weeks | **Stuck emergence.** Either the emergence isn't real, or it needs a surface to grow further. |
| Initiative in surfaced state with no evolution signals > 3 weeks | **Dead surface.** Users aren't engaging or the feedback loops aren't working. |
| Initiative in evolving state with negative trajectory > 2 weeks | **Failing evolution.** Consider: prune aggressively, redesign, or compost. |
