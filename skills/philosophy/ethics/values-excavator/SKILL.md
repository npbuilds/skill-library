---
name: values-excavator
description: >
  Surface implicit values, competing goods, and hidden moral assumptions in a proposal,
  decision, policy, or argument. Use when the user needs to understand what values are
  driving a decision (their own or someone else's), identify competing goods that create
  tension, reveal whose interests a proposal serves, or make the moral logic of a position
  explicit.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Values Excavator — The Dowser

Find the hidden values flowing beneath the surface of any decision. Every proposal, policy, argument, and choice embeds value judgments — assumptions about what matters, whose interests count, and what trade-offs are acceptable. Most of these are invisible to the person making them.

The values-excavator is a moral analog of the assumption-excavator in the logic subdomain. Where that skill finds hidden premises, this one finds hidden values. They complement each other: assumptions are epistemic; values are moral.

## Input

From the ethics director or directly:
- The proposal, decision, policy, or argument to excavate
- Context: whose values? (the user's, an organization's, a policy's, an argument's)
- Depth: **surface** (identify the top 3-5 implicit values) or **deep** (comprehensive value mapping)

## Process

### Step 1 — Identify Explicit Values

Before excavating what's hidden, map what's visible. What values are *stated*?

- Mission statements, stated goals, explicit priorities
- "We believe in...", "Our priority is...", "What matters most is..."
- Criteria explicitly used for the decision

These are the above-waterline values.

### Step 2 — Excavate Implicit Values

Dig for values hidden in the structure of the decision:

#### Values in Metrics
*What you measure reveals what you value.*

- What metrics are being used or proposed? (Revenue, engagement, satisfaction, safety, equity)
- What metrics are *absent*? (Often more revealing than what's present)
- How are trade-offs between metrics resolved?

*Example*: Optimizing for "user engagement" implicitly values time-on-platform over user wellbeing, advertiser revenue over information quality, and behavioral manipulation over autonomy — even if none of this is stated.

#### Values in Defaults
*The default option reveals the preferred outcome.*

- What happens if no one takes action? Who benefits from inertia?
- What's treated as the "normal" baseline against which alternatives are judged?
- Who bears the burden of proof — those proposing change or those defending the status quo?

*Example*: "Innocent until proven guilty" values individual liberty over collective security. "Precautionary principle" values safety over innovation. Neither is objectively correct — they're value choices.

#### Values in Scope
*Who and what are included reveals whose interests count.*

- Whose interests are considered in the analysis?
- Whose interests are excluded or invisible?
- What time horizon is assumed? (Short-term profit vs. long-term sustainability)
- What geographic scope? (Local community vs. global impact)

*Example*: A cost-benefit analysis that counts only shareholder value implicitly values shareholders over employees, customers, and communities.

#### Values in Framing
*How the question is posed reveals what counts as a solution.*

- Is this framed as an efficiency problem? (Values productivity)
- Is this framed as a rights problem? (Values autonomy)
- Is this framed as a safety problem? (Values security)
- Is this framed as a fairness problem? (Values equity)

*Example*: "How do we reduce healthcare costs?" (efficiency frame) vs. "How do we ensure everyone has access to healthcare?" (rights frame) — same domain, completely different value landscapes.

#### Values in Omission
*What's not discussed reveals what's taken for granted.*

- What obvious considerations are missing from the analysis?
- What stakeholders are not mentioned?
- What potential harms are not acknowledged?
- What alternative approaches are not considered?

### Step 3 — Map Value Tensions

Identify where implicit values conflict with each other or with stated values:

| Tension Type | Pattern | Example |
|---|---|---|
| **Stated vs. revealed** | Organization says X but does Y | "We value work-life balance" + mandatory 60-hour weeks |
| **Value vs. value** | Two legitimate goods in competition | Privacy vs. security; innovation vs. safety; efficiency vs. equity |
| **Short-term vs. long-term** | Immediate benefits vs. future costs | Quarterly earnings vs. long-term sustainability |
| **Individual vs. collective** | One person's good vs. the group's | One employee's advancement vs. team cohesion |
| **Means vs. ends** | The process conflicts with the goal | Achieving equity through inequitable methods |

### Step 4 — Trace Value Origins

Where do these values come from? Understanding the source helps the user evaluate them:

| Source | Description | Stability |
|--------|-------------|-----------|
| **Institutional** | Embedded in organizational structure, incentives, or culture | Highly stable; persists even when individuals change |
| **Professional** | Derived from professional norms and training | Stable within a field; varies across fields |
| **Cultural** | Absorbed from broader cultural context | Often invisible to those within the culture |
| **Personal** | Individual beliefs and experiences | Variable; may conflict with institutional or professional values |
| **Ideological** | Part of a coherent political or philosophical worldview | Stable but often unexamined |

### Step 5 — Assess Value Coherence

Are the excavated values *coherent* — can they all be satisfied simultaneously, or are trade-offs inevitable?

- **Compatible**: Values can all be served (rare for non-trivial decisions)
- **Tension**: Values pull in different directions but compromise is possible
- **Contradiction**: Values are mutually exclusive in this context — choosing one means sacrificing another
- **Hierarchy needed**: Values are compatible in general but this specific situation forces a ranking

## Output

```
VALUES EXCAVATION
─────────────────
Subject: [the proposal/decision/policy/argument analyzed]
Whose values: [individual/organization/policy/argument]

Stated Values:
  - [explicitly stated value] — Source: [where stated]
  ...

Implicit Values Excavated:
  1. [Value] — Found in: [metrics/defaults/scope/framing/omission]
     Evidence: [specific feature of the decision that reveals this value]
     Visibility: [hidden / semi-visible / visible but unchallenged]

  2. [Value] — Found in: [category]
     ...

Value Tensions:
  T1: [Value A] vs. [Value B] — Type: [stated-vs-revealed / value-vs-value / etc.]
      In this decision: [how the tension manifests]
      Resolution requires: [what the user would need to decide]

  T2: ...

Value Coherence: [compatible / tension / contradiction / hierarchy needed]

Most Critical Finding:
  [The single most important implicit value or tension the user should be aware of]

Recommended Next Steps:
  - [e.g., "Run dilemma-analyzer on tension T1 to see how ethical frameworks weigh in"]
  - [e.g., "Route to stakeholder-mapper to check whose values are missing"]
```

## Error Handling

**No hidden values found:** Rare for any non-trivial decision. If the proposal is genuinely transparent about its values, report this as a positive finding. More likely, dig deeper — values in omission are the hardest to see.

**User is emotionally attached to the values excavated:** Handle with care. "Your decision reflects a value of X" is descriptive, not accusatory. Values are not flaws — they're choices, and making them explicit gives the user more control, not less.

**Values are culturally specific:** Note cultural context without universalizing. "In this cultural context, X is valued" is better than "X is good/bad." The excavator surfaces values; it doesn't rank them.

**Too many values to map:** Focus on values that are load-bearing for the specific decision at hand. Group minor values into clusters ("productivity values," "equity values") and detail only the ones in active tension.
