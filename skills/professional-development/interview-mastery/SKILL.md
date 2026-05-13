---
name: interview-mastery
description: >
  Direct behavioral interview prep, domain-technical deep-dives, VC interviews, executive
  interviews, and panel/case interviews to the appropriate specialist skill. Activate when
  the user is preparing for any interview that matters — first conversations, IC pitches,
  partner interviews, board candidate screens, or executive panels. Interview mastery is
  the discipline of rehearsing the conversation before it happens, with the right framework
  for the format.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Interview Mastery Director

An interview is not a conversation; it is a structured evaluation pretending to be one. The interviewer is running a small number of stable patterns — behavioral probes, technical depth checks, fit signals, judgment tests — and the interviewee who knows the patterns and has rehearsed against them outperforms the interviewee who is "being themselves." This is not cynicism; it is craft. Every senior physician who has run an interview team for fellowship applicants knows this from the other side.

This director routes interview-prep questions to the right specialist by *format* (behavioral, domain-technical, VC, executive, panel/case) and sequences multi-skill prep when the loop spans formats — which most senior loops do.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| behavioral-frameworks | knowledge | STAR, CAR, "tell me about a time" stories; building a story bank; mapping stories to common probes |
| domain-deepdives | action | Domain-technical interviews — clinical development, regulatory, asset evaluation; preparing to be tested on what you claim to know |
| vc-interview-prep | action | VC associate / principal / partner / venture-partner / EIR interviews; market thesis, deal review, portfolio reasoning |
| executive-interview-prep | action | C-suite, SVP, Head-of interviews; strategic thinking, P&L judgment, leadership scenarios, "first 90 days" |
| panel-and-case | action | Multi-interviewer dynamics, live cases, working sessions, take-home cases, IC simulations |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| "Tell me about a time," STAR, story bank, behavioral, behavioral round | behavioral-frameworks | "Build me a story bank" / "How do I answer 'tell me about a conflict'?" |
| Clinical, regulatory, asset evaluation prep, "they're going to test my [domain]" | domain-deepdives | "Prep me for a clinical-development deep-dive interview" |
| VC, venture, associate / principal / partner interview, deal review, market thesis | vc-interview-prep | "I have a VC associate interview at [firm]" |
| C-suite, SVP, Head-of, executive panel, "first 90 days," P&L | executive-interview-prep | "Prep me for the CMO interview at [company]" |
| Panel, working session, live case, take-home, IC simulation | panel-and-case | "They're running me through a live case on Tuesday" |

## Multi-Skill Questions

Most senior interview loops span multiple formats. Common combinations:

1. **VC Associate Loop** ("Full prep for [firm] associate interviews"):
   - Load `vc-interview-prep` as primary
   - Load `behavioral-frameworks` for the people round and "why VC" questions
   - Load `domain-deepdives` (handing off to `biotech-venture/asclepius` for the diligence round)
   - Load `panel-and-case` for the IC simulation or live diligence exercise

2. **CMO Interview Loop** ("Full prep for the CMO role at [company]"):
   - Load `executive-interview-prep` as primary
   - Load `domain-deepdives` for the clinical-development scrutiny round
   - Load `behavioral-frameworks` for the leadership-story round
   - Load `panel-and-case` for the strategy presentation

3. **Board Candidate Screen** ("Prep me for the board interview"):
   - Load `executive-interview-prep` as primary (board interviews test strategic and governance judgment)
   - Load `panel-and-case` for the multi-board-member dynamic
   - Hand off to `executive-presence/board-readiness` for posture and protocol

## Curriculum Order

1. **behavioral-frameworks** — Foundation. The story bank built here gets reused across every other interview type.
2. **domain-deepdives** — Second. You cannot pretend to depth you do not have; rehearse the depth you actually have.
3. **panel-and-case** — Third. Live formats require their own muscle memory.
4. **vc-interview-prep** and **executive-interview-prep** — Format-specific layers built on top of the above.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Behavioral story is true and well-structured but boring; embellishment would make it land | Always truth, never embellishment | Discovery of fabrication ends the search; the cost is asymmetric |
| Domain-deepdive prep wants to optimize for breadth; loop will probably go deep in one area | Optimize for depth on the 2–3 highest-stakes areas; have a credible "I don't know, but here's how I'd think about it" for the rest | Senior interviewers value reasoning under uncertainty more than encyclopedic recall |
| VC interview prep wants to script answers; firm partners pattern-match scripted candidates as "not VC material" | Script the *thinking*, improvise the *expression* | Memorized answers are detectable; rehearsed reasoning is not |

## Teaching Convention

Every leaf in this director includes a `## Self-Coaching Track` (applied to the user's specific upcoming interview, biotech-tilted) and a `## Teach / Mentor-Others Track` (how you'd coach a junior through the same prep). When responding from any leaf, default to producing both.

## Scope Boundaries

**This director handles**: All interview preparation — first conversations through final rounds, across formats and seniority levels.

**Route elsewhere when**:
- The question is about the underlying *narrative* you're presenting (not how to deliver it in an interview) → `personal-positioning/narrative-architecture`
- The question is about *getting* the interview (cold outreach, network warm intros) → `network-cultivation`
- The question is about negotiating the offer that follows → `negotiation-leverage`
- The question is about presence and delivery (not interview-specific) → `executive-presence`

## Cross-Domain Connections

- **biotech-venture/asclepius** (and the clinical-development, regulatory-strategy, asset-valuation, probability-of-success, deal-synthesis directors) — Source of substance for VC and domain-deepdive interviews
- **binding-vow/bluf-shaper, minto-scqa** — Structuring case and presentation answers
- **personal-positioning/narrative-architecture** — Source of the underlying through-line
- **personal-positioning/credibility-translation** — Translating clinical experience into the audience's language
- **network-cultivation/ecosystem-mapping** — Firm and partner research before the interview
- **research/spelunker** — Deep firm/partner research
