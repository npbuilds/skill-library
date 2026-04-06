---
name: stakeholder-mapper
description: >
  Identify all parties affected by a decision, their moral claims, power dynamics, and
  vulnerability. Use when the user needs to understand who is affected by a proposal,
  whose interests are visible vs. invisible, what power asymmetries exist, or who has
  standing to make moral claims about a decision.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read Write
---

# Stakeholder Mapper — The Census Taker

Count everyone who matters. The most common ethical blind spot is not getting the values wrong — it's not seeing all the people affected. The census taker systematically identifies who has a stake, what kind of stake they have, and whose voice is missing from the room.

## Input

From the ethics director or directly:
- The decision, policy, or proposal to map
- Context: who is the decision-maker? What's the scope?
- Depth: **core** (direct stakeholders only) or **comprehensive** (direct + indirect + future + systemic)

## Process

### Step 1 — Map Direct Stakeholders

Who is immediately, obviously affected?

For each stakeholder, identify:
- **Who**: specific person, group, or entity
- **Stake**: what do they stand to gain or lose?
- **Claim type**: right, interest, contractual obligation, or moral claim
- **Direction**: are they helped, harmed, or affected ambiguously?

### Step 2 — Map Indirect Stakeholders

Who is affected through second-order effects?

| Ring | Description | Examples |
|------|-------------|---------|
| **Ring 1**: Direct | Immediately affected by the decision | Employees, customers, shareholders |
| **Ring 2**: Indirect | Affected through consequences of the decision | Competitors, suppliers, families of employees |
| **Ring 3**: Systemic | Affected through changes to systems or norms | Industry, regulatory environment, market structure |
| **Ring 4**: Future | Affected in future time periods | Future employees, future generations, future selves |
| **Ring 5**: Non-human | Non-human entities affected | Animals, ecosystems, AI systems (if relevant) |

### Step 3 — Assess Power and Vulnerability

For each stakeholder:

| Dimension | Questions |
|-----------|----------|
| **Voice** | Can this stakeholder speak for themselves in the decision process? |
| **Exit** | Can this stakeholder walk away if they dislike the outcome? |
| **Power** | Can this stakeholder influence the decision? |
| **Vulnerability** | Is this stakeholder in a position of dependency, disadvantage, or fragility? |
| **Visibility** | Is this stakeholder visible to the decision-maker? |

**Power-vulnerability matrix**: Stakeholders who are highly affected but have low power and low visibility are the ones most likely to be overlooked — and often the ones with the strongest moral claim to consideration.

### Step 4 — Identify Missing Voices

The most important step. Ask:
- Whose interests are not represented in the decision-making process?
- Who cannot speak for themselves? (Future generations, children, animals, people in other jurisdictions)
- Who would be affected but is not considered a "stakeholder" by the decision-maker?
- Whose concerns have been dismissed as irrelevant?

### Step 5 — Assess Moral Weight

Not all stakes are equal. Assess:

| Factor | Higher Moral Weight | Lower Moral Weight |
|--------|---|---|
| **Severity** | Existential or irreversible harm | Inconvenience or temporary loss |
| **Vulnerability** | Affected party is dependent, disadvantaged | Affected party has resources and alternatives |
| **Proximity** | Direct, personal impact | Remote, diffuse impact |
| **Number** | Many people affected | Few people affected |
| **Consent** | Affected without consent or knowledge | Affected after informed voluntary agreement |
| **Alternatives** | No alternative available | Readily available alternatives |

## Output

```
STAKEHOLDER MAP
───────────────
Decision: [the decision/policy/proposal]
Decision-maker: [who decides]

Stakeholders:

  Ring 1 — Direct:
    [Stakeholder] — Stake: [what they gain/lose]
      Claim: [right/interest/obligation] | Direction: [helped/harmed/mixed]
      Power: [high/medium/low] | Vulnerability: [high/medium/low] | Voice: [has/lacks]

  Ring 2 — Indirect:
    [Stakeholder] — Stake: [second-order effect]
      ...

  Ring 3+ — Systemic/Future/Non-human:
    [Stakeholder] — Stake: [systemic or future effect]
      ...

Missing Voices:
  - [Who is affected but absent from the process?]
  - [Who cannot speak for themselves?]

Power Map:
  High power + low vulnerability: [list] — likely overrepresented
  Low power + high vulnerability: [list] — likely underrepresented

Moral Weight Assessment:
  Highest-priority stakeholders: [who faces the most severe, irreversible, unconsented impacts]

Key Finding: [the single most important stakeholder insight — often a missing voice]
```

## Error Handling

**Stakeholder list is enormous:** Focus on Ring 1-2 for the core map. Group Ring 3+ stakeholders into categories rather than enumerating individuals. The goal is to ensure no *category* of affected party is missed, not to list every individual.

**Decision-maker is also a stakeholder:** Common and fine. Note the dual role and flag where their interests as decision-maker diverge from their interests as a stakeholder.

**No missing voices found:** Unusual for significant decisions. Double-check by asking: "Who would be most angry if they found out about this decision after the fact?" That person is probably a missing stakeholder.
