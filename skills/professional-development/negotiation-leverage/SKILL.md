---
name: negotiation-leverage
description: >
  Direct offer negotiation, equity literacy, title and scope negotiation, and exit / transition
  craft to the appropriate specialist skill. Activate when the user is negotiating any term —
  base, bonus, equity, title, scope, signing bonus, vesting, severance, non-compete, garden
  leave, or notice. Negotiation leverage is the discipline of converting earned credibility
  into terms that protect the trajectory's optionality.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Negotiation Leverage Director

The most expensive career mistake a senior professional makes is *not negotiating* — leaving 10–30% of compensation, an entire layer of equity, a year of vesting acceleration, or a critical scope term on the table because they did not know it was negotiable. The second most expensive is negotiating from the wrong frame: anchoring on what the company offered rather than what the role requires, optimizing for cash when equity matters more, accepting a title that compresses future earning power, signing a non-compete that destroys downstream optionality.

This director routes negotiation work to the right specialist by *what is being negotiated*. The core stance is that negotiation is collaborative problem-solving with information asymmetry — not adversarial — and the leverage comes from preparation, not posture.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| offer-negotiation | action | Negotiating an incoming offer — base, bonus, signing, performance metrics, start date, relocation, benefits |
| equity-literacy | knowledge | Understanding and negotiating equity — options vs RSUs vs PSUs, strike price, vesting, cliff, refresh, acceleration, dilution, secondary, 409A |
| title-and-scope | action | Negotiating title, reporting line, scope, charter, headcount, budget — the structural levers that shape what the role actually is |
| exit-and-transition | action | Negotiating exit terms — notice, garden leave, severance, non-compete carveouts, IP releases, transition consulting, references |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| Offer, base, bonus, signing, comp package, total comp, "what's market" | offer-negotiation | "They offered $X — what should I counter?" |
| Equity, options, RSUs, strike, vesting, cliff, acceleration, dilution, 409A, secondary | equity-literacy | "Walk me through this option grant" / "What's the right vesting acceleration to ask for?" |
| Title, level, reporting, scope, charter, headcount, budget, "Head of" vs "VP" | title-and-scope | "They want me as Director; I want VP — how do I argue it?" |
| Exit, notice, severance, non-compete, garden leave, transition, separation, last day | exit-and-transition | "I'm leaving in 30 days — what should I negotiate?" |

## Multi-Skill Questions

1. **Full Offer Negotiation** ("Help me negotiate this offer"):
   - Load `offer-negotiation` as primary
   - Load `equity-literacy` to evaluate the equity component
   - Load `title-and-scope` to evaluate the structural component
   - Cross-reference `trajectory-design/optionality-architecture` to assess option-set effect
   - Cross-reference `negotiation-leverage` itself runs the meta — what are the alternatives, what is the BATNA

2. **Equity Counter-Proposal** ("How do I counter this equity grant?"):
   - Load `equity-literacy` as primary
   - Cross-reference `offer-negotiation` for the negotiation structure
   - Hand off to `investing/archon` for cap table modeling if the grant is in a startup with future dilution

3. **Exit Package Negotiation** ("I'm being asked to leave; help me negotiate the package"):
   - Load `exit-and-transition` as primary
   - Cross-reference `equity-literacy` for vesting acceleration questions
   - Note: exit negotiations have legal dimensions — escalate to an employment attorney for contract review

## Curriculum Order

1. **equity-literacy** — Foundation. Without equity literacy, every other negotiation is undermined. Most senior comp upside is in equity; getting the equity wrong dwarfs getting the base right.
2. **offer-negotiation** — Second. The mechanics of running an offer process.
3. **title-and-scope** — Third. The structural levers that compound over time.
4. **exit-and-transition** — Specialized. Comes up less frequently but when it does, the stakes are high.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Offer-negotiation wants to push hard; the user has weak BATNA | Lead with collaborative framing ("help me understand the structure"); ask for information first, then make the case based on the role and market — never on personal need | Hard tactics with weak BATNA usually fail; collaborative framing succeeds more often even with strong BATNA |
| Equity offer is generous; cash is below market | Evaluate via expected-value (probability-weighted equity + cash); if user is liquidity-constrained, prioritize cash with equity refresh | Expected value is the right frame for senior negotiation; if liquidity forces a different optimization, name it explicitly |
| Title and scope conflict — company offers higher title with smaller scope, or lower title with broader scope | Scope matters more for next-job; title matters more for current-job perception; ask what the role actually does and decide from there | Title is mostly a future-signal; scope is mostly a current-reality |

## Teaching Convention

Every leaf in this director includes `## Self-Coaching Track` (applied to the user's actual negotiation, biotech-tilted) and `## Teach / Mentor-Others Track` (how you'd coach a junior or peer through the same negotiation). Default to producing both.

## Scope Boundaries

**This director handles**: All employment / engagement negotiations — incoming offers, ongoing terms, exit packages.

**Route elsewhere when**:
- The negotiation is *whether to take the role* (not the terms) → `trajectory-design`
- The question concerns actual legal review of contract language → escalate to an employment attorney
- The question concerns tax consequences of equity decisions → escalate to a CPA familiar with startup equity
- The question concerns *what to ask for* in the broader career sense (compensation expectations, etc.) → cross-load with `trajectory-design`

## Cross-Domain Connections

- **investing/archon** — Cap-table modeling, dilution math, secondary sale economics
- **trajectory-design/optionality-architecture** — Negotiation outcomes are option-set moves
- **binding-vow/bluf-shaper** — Counter-proposal emails benefit from BLUF structure
- **game-theory/classical-games** — Negotiation structure (BATNA, ZOPA, multi-issue trades) is classical game theory
- **biotech-venture/asclepius** — In biotech startup negotiations, asset-stage diligence informs equity valuation
