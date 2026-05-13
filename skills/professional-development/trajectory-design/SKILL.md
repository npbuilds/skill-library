---
name: trajectory-design
description: >
  Direct role-archetype mapping, optionality architecture, IDPs and OKRs, skill-gap analysis,
  and pivot sequencing to the appropriate specialist skill. Activate when the user is making
  or remaking the underlying choice of *what career to build* — picking a target role
  archetype, designing optionality, setting personal OKRs, naming skill gaps, sequencing a
  multi-year pivot. Trajectory design is the strategic layer that every other career
  activity serves.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Trajectory Design Director

Most career problems are not execution problems — they are trajectory problems mistaken for execution problems. The resume is being rewritten over and over because the role-archetype is not yet named. The networking is feeling unproductive because the ecosystem map is unclear. The interview prep is anxious because the candidate is not sure which role they are auditioning for. Trajectory design is where Mentor starts when the user is unsure, and where Mentor returns when downstream work feels chronically unsettled.

This director handles the strategic layer: which role to aim at, what optionality the choice preserves or forfeits, what to measure progress against, what skills must be built before the move is credible, and how to sequence the moves across years.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| role-archetype-mapping | knowledge | Naming the target — operator, investor, advisor, founder, board member, EIR, venture partner; understanding what each archetype actually does day to day |
| optionality-architecture | knowledge | Evaluating a choice by its effect on the option set — what doors does this open, what doors does it close |
| idp-and-okrs | action | Personal OKRs, individual development plans, quarterly reviews — making the trajectory measurable |
| skill-gap-analysis | action | Honest naming of the gap between current skill stack and target role; designing the smallest credible action to close it |
| pivot-sequencing | knowledge | Multi-year transition plans — what to do in year 1 to make year 3 possible; intermediate roles, advisor seats, side artifacts |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| "What role should I be targeting?" / "What does a [role] actually do?" / Comparing archetypes | role-archetype-mapping | "Operator vs investor — which fits me?" / "What does a venture partner actually do?" |
| Optionality, "if I do X, what does that close off," reversibility, off-ramps | optionality-architecture | "If I take a startup CMO role, what does that do to my VC optionality?" |
| OKRs, IDP, quarterly review, personal goals, measurable, what to track | idp-and-okrs | "Set personal OKRs for Q3" / "Build my IDP for the year" |
| Skill gap, "what am I missing," readiness, "what would I need to learn to..." | skill-gap-analysis | "What skills am I missing for a Head of Clin Dev role at a Series A?" |
| Pivot, multi-year, sequence, year 1 / year 3, stepping stones | pivot-sequencing | "Design the 3-year pivot from director to operating partner" |

## Multi-Skill Questions

1. **Trajectory Reset** ("I'm not sure what I want next — help me think it through"):
   - Load `role-archetype-mapping` first — surface the full archetype set so the user is choosing from a known menu, not their imagination
   - Then `optionality-architecture` — evaluate the top 2–3 archetypes by their option-set effect
   - Then `skill-gap-analysis` — name the gap for the chosen archetype
   - Then `pivot-sequencing` — multi-year plan
   - Then `idp-and-okrs` — convert plan into measurable quarterly work

2. **"Should I Take This Offer?"**:
   - Load `optionality-architecture` as primary — every offer is an option-set move
   - Cross-reference `role-archetype-mapping` to confirm the offer fits the named target
   - Hand off to `negotiation-leverage/offer-negotiation` once the strategic question is settled

3. **Year-End Reset** ("Help me plan next year"):
   - Load `idp-and-okrs` as primary
   - Cross-reference `skill-gap-analysis` to ensure the goals close real gaps
   - Cross-reference `pivot-sequencing` to ensure the year fits the multi-year plan

## Curriculum Order

1. **role-archetype-mapping** — Foundation. The archetype menu has to be known before it can be chosen from. For the MD → biotech-VC user, the relevant archetypes include: clinical operator (CMO, Head of Clin Dev), biotech founder/co-founder, VC associate/principal/partner, venture-partner, EIR (entrepreneur-in-residence), operating-partner, board-of-directors candidate, advisor.
2. **optionality-architecture** — Second. Once the menu is known, evaluate by option-set effect, not by next-paycheck logic.
3. **skill-gap-analysis** — Third. Honest gap analysis against the chosen archetype.
4. **pivot-sequencing** — Fourth. Multi-year sequencing to close the gap and execute the move.
5. **idp-and-okrs** — Continuous. The plan only exists if it is measurable; this is the operating cadence.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Role-archetype analysis says "operator" but optionality analysis says "EIR or advisor" preserves more options | Optionality wins for *path-dependent* careers (early-stage venture, founder paths); archetype wins when the gap to the named role is small and time is short | Optionality preservation matters most when the future is uncertain; commit when the move is high-conviction and the target is achievable |
| Skill-gap analysis says "you need 2 years of P&L ownership"; pivot-sequencing wants to make the move in 1 year | Either compress the gap (a credible 1-year P&L-adjacent role) or extend the timeline (2 years is honest) | Pretending a gap doesn't exist is the failure mode; surfacing it explicitly is the win |
| OKRs are precise and measurable; the trajectory is genuinely exploratory and not yet committable | Use a different OKR shape — exploration OKRs measure *learning velocity* (conversations had, archetypes assessed, gaps named) rather than *output* | Forcing output OKRs onto exploration produces theater, not learning |

## Teaching Convention

Every leaf in this director includes `## Self-Coaching Track` (applied to the user's specific trajectory question, biotech-tilted) and `## Teach / Mentor-Others Track` (how you'd coach a junior or peer making the same kind of decision). Default to producing both.

## Scope Boundaries

**This director handles**: The strategic layer of career — which role, which optionality, which gap, which sequence.

**Route elsewhere when**:
- The trajectory is named and the question is now "how do I get there" → `personal-positioning`, `network-cultivation`, `interview-mastery`
- The question is about a specific offer's *terms* (not whether to take it) → `negotiation-leverage`
- The question is about how to *perform* in the current role → `executive-presence` or functional skills (data, product, etc.)
- The question is about processing feedback that may reframe the trajectory → `feedback-loops`

## Cross-Domain Connections

- **product/the-loom** — Decision-journal trajectory choices; The Loom is the natural home for the multi-year reflection
- **investing/archon** — When trajectory choices involve evaluating startup equity and dilution math, Archon is the substance
- **biotech-venture/asclepius** — Role-archetype mapping in biotech (e.g., what does a clinical-development VC actually evaluate) routes into Asclepius for the day-to-day reality
- **game-theory/classical-games** — Multi-year pivot sequencing has strategic-game structure (committed vs reversible moves)
- **research/spelunker** — Researching role archetypes via real-world examples (read 20 LinkedIn paths to a target role)
