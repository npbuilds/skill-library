---
name: dilemma-analyzer
description: >
  Apply multiple ethical frameworks to a situation and surface where they converge and diverge.
  Use when the user faces a moral dilemma, needs to evaluate whether an action is ethical,
  wants to compare the ethics of different options, or needs to understand why reasonable
  people disagree about a moral question.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Dilemma Analyzer — The Tribunal

Convene a tribunal of ethical frameworks, let each render its verdict, and present the full picture — agreements, disagreements, and the value commitments driving each. The analyzer does not pick a winner. It illuminates the moral landscape so the user can navigate it.

Read `references/framework-comparison.md` for detailed framework descriptions and their key theorists.

## Input

From the ethics director or directly:
- The situation or decision to analyze
- The options available (if a decision between alternatives)
- Context: who is the moral agent? What constraints exist?
- Scope: **quick** (top 2-3 frameworks) or **comprehensive** (all major frameworks)

## Process

### Step 1 — Frame the Dilemma

Restate the moral question precisely. A well-framed dilemma specifies:
- **The agent**: who must decide
- **The options**: what choices are available (including inaction)
- **The stakes**: what's at risk for whom
- **The tension**: why this is a genuine dilemma (not just a hard decision)

A genuine dilemma has morally significant reasons supporting different options. If all reasons point one way, it's not a dilemma — report that and move to validation rather than analysis.

### Step 2 — Apply Ethical Frameworks

Run each framework as an independent lens. For each, answer: "What does this framework say about the situation, and why?"

#### Consequentialism (Utilitarian)
*Core question: Which option produces the best overall outcomes?*

- Identify all consequences for all affected parties
- Weigh positive and negative outcomes
- Consider probability-weighted expected outcomes, not just best-case
- **Act utilitarian**: which specific action maximizes utility?
- **Rule utilitarian**: which rule, if universally followed, would maximize utility?
- Key tension: whose utility counts? How to compare different kinds of harm/benefit?

#### Deontology (Kantian / Duty-Based)
*Core question: Does the action respect moral duties and the dignity of persons?*

- **Universalizability**: Could the maxim of this action be willed as a universal law without contradiction?
- **Humanity formula**: Does the action treat persons as ends in themselves, never merely as means?
- **Rights**: Does the action violate anyone's rights?
- Key tension: what to do when duties conflict (duty to tell truth vs. duty to prevent harm)?

#### Virtue Ethics (Aristotelian)
*Core question: What would a person of good character do?*

- Which virtues are relevant? (courage, justice, temperance, wisdom, honesty, compassion)
- Which vices does each option risk? (cowardice, injustice, excess, folly, dishonesty, cruelty)
- What does practical wisdom (phronesis) suggest given the specific circumstances?
- Key tension: virtues can conflict (courage vs. prudence, honesty vs. compassion)

#### Care Ethics (Gilligan / Noddings)
*Core question: How does this affect relationships and the vulnerable?*

- Who is in a relationship of care with whom?
- Who is most vulnerable in this situation?
- Which option best preserves and strengthens caring relationships?
- What does attentiveness to particular persons and contexts suggest?
- Key tension: partiality toward those we care about vs. impartial moral demands

#### Contractualism (Scanlon / Rawls)
*Core question: Could this action be justified to everyone affected?*

- **Scanlon**: Could anyone reasonably reject the principle behind this action?
- **Rawls**: Would this be chosen behind a veil of ignorance (not knowing which affected party you'd be)?
- Key tension: what counts as "reasonable" rejection?

### Step 3 — Map Convergence and Divergence

After all frameworks have rendered their verdicts:

**Convergence**: Where do frameworks agree? These are the most ethically robust conclusions — if both utilitarian and deontological reasoning point the same way, the case is strong.

**Divergence**: Where do frameworks disagree? For each disagreement:
- Which frameworks are on each side?
- What value commitment drives the disagreement?
- Is the disagreement about facts (resolvable with evidence) or about values (genuine moral disagreement)?

### Step 4 — Identify the Crux

What is the single most important moral question whose answer determines which option is right? This is the ethical crux — the point where the user's own values will resolve the dilemma.

Often the crux is a question like:
- "Do outcomes matter more than principles in this case?"
- "Does the duty to X outweigh the duty to Y here?"
- "Whose interests should take priority?"

### Step 5 — Present Without Prescribing

The analyzer presents the full moral landscape. It does NOT tell the user what to do. Philosophy illuminates the choice; the user makes it.

## Output

```
ETHICAL ANALYSIS
────────────────
Dilemma: [precise framing of the moral question]
Agent: [who must decide]
Options: [available choices]

Framework Verdicts:

  Consequentialist: [verdict and reasoning — 2-3 sentences]
  Deontological:    [verdict and reasoning — 2-3 sentences]
  Virtue Ethics:    [verdict and reasoning — 2-3 sentences]
  Care Ethics:      [verdict and reasoning — 2-3 sentences]
  Contractualist:   [verdict and reasoning — 2-3 sentences]

Convergence:
  [Where frameworks agree, and why this is robust]

Divergence:
  [Where frameworks disagree]
  Driving value tension: [what value commitment is at stake]

Ethical Crux:
  [The single question whose answer resolves the dilemma]

If you prioritize [value A]: [what follows]
If you prioritize [value B]: [what follows]
```

## Error Handling

**Not actually a dilemma:** If all frameworks agree, report the consensus and note that this is ethically straightforward. Don't manufacture controversy where there is none.

**Situation is too vague:** Ask for specifics — who's involved, what are the concrete options, what are the real-world constraints. Abstract ethical questions ("Is lying ever justified?") should be grounded in a specific scenario to produce useful analysis.

**User wants a definitive answer:** Explain that ethical frameworks give different answers because they value different things. Offer to help the user identify which values they prioritize (route to values-excavator), which will often resolve the question for them personally.

**Culturally sensitive topic:** Apply frameworks without cultural bias. All major frameworks are cross-cultural in their formal structure, even though they emerged in specific traditions. Acknowledge that cultural context affects how principles are weighted.



## Related Skills

- **classical-games** — Many moral dilemmas reduce to classical game-theoretic structures. Use classical-games to expose the underlying strategic incentives beneath an ethical question.
