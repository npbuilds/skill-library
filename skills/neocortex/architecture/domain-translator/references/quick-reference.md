# Domain Translator — Quick Reference


## Quick Reference

| Component | What to Capture |
|-----------|----------------|
| **Name** | What it's called in the source domain |
| **Function** | What it does — what problem it solves |
| **Mechanism** | How it works — the internal logic |
| **Assumptions** | What has to be true for it to work |
| **Scope** | Where it applies and where it doesn't |

## Quick Reference

| Question | Purpose |
|----------|---------|
| If I removed all domain-specific nouns, what's the verb? | Finds the action/relationship at the core |
| Does this concept exist in other fields under a different name? | Tests whether the structure is truly general |
| What's the minimum description that preserves the insight? | Prevents carrying over domain-specific baggage |

## Quick Reference

| Adaptation Check | Question |
|-----------------|---------|
| **Language fit** | Does the translation use the target domain's natural vocabulary? |
| **Constraint fit** | Does the target domain have constraints that change how the concept applies? |
| **Scale fit** | Does the concept operate at the same scale in both domains? |
| **Mechanism fit** | Is the causal mechanism the same, or just the pattern? |

## Quick Reference

| Test | Method |
|------|--------|
| **Edge cases** | Apply the translated concept to extreme scenarios in the target domain |
| **Counterexamples** | Look for cases where the target domain behaves differently than the source |
| **Mechanism check** | Is the underlying mechanism actually the same, or is this surface similarity? |
| **Practitioner test** | Would an expert in the target domain find this translation useful or forced? |

## Quick Reference

| Payoff Type | Description |
|-------------|------------|
| **New question** | The translation suggests a question nobody in the target domain was asking |
| **New tool** | A methodology from the source domain can be adapted for the target |
| **Warning** | A known failure mode in the source domain might apply to the target |
| **Connection** | The translation creates a new cross-domain edge in the skill library |

## Quick Reference

| Pattern | Source Example | Transfers To | Core Structure |
|---------|--------------|-------------|---------------|
| **Feedback loops** | Market reflexivity (investing) | Narrative pacing (writing), population dynamics (game theory) | Output feeds back as input |
| **Multi-framework analysis** | Ethical dilemma analysis (philosophy) | Investment thesis evaluation (investing) | Apply N lenses, compare conclusions |
| **Stakeholder mapping** | Moral stakeholders (ethics) | Risk factor mapping (investing), character webs (worldbuilding) | Identify all affected parties and their claims |
| **Excavation** | Assumption-excavator (logic) | Values-excavator (ethics), bias-detector (decision-theory) | Surface what's hidden beneath the visible |
| **Quality hierarchies** | Evidence hierarchies (epistemology) | Data quality tiers (data-science), source reliability (research) | Rank inputs by reliability |
| **Regime detection** | Market regimes (investing) | Paradigm shifts (philosophy of science), narrative phases (writing) | Recognize which state the system is in |

## Output Format

```
DOMAIN TRANSLATION — [Source Concept] → [Target Domain]

Source:
  Concept: [name] from [domain]
  Function: [what it does in the source domain]

Structural Core:
  [The domain-independent principle in one sentence]

Translation:
  In [target domain], this maps to: [concrete adaptation]
  Target vocabulary: [how to express this in the target domain's language]

Where It Holds:
  - [Aspect 1 that transfers cleanly]
  - [Aspect 2 that transfers cleanly]

Where It Breaks:
  - [Aspect that doesn't transfer, and why]

Payoff:
  [What the target domain gains — new question, tool, warning, or connection]

Confidence: [High / Medium / Low — how clean is this translation?]
```
