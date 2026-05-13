---
name: feedback-loops
description: >
  Direct 360 feedback design, performance review craft, personal advisory board, and
  reflection and journaling to the appropriate specialist skill. Activate when the user is
  designing how they collect, structure, and metabolize feedback — running a 360, drafting
  a self-assessment, building a personal advisory board, or maintaining a reflection
  practice. Feedback loops are the discipline that turns experience into compounding
  judgment.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Feedback Loops Director

Experience does not produce wisdom by default. Without a loop that names what was learned, the same lesson re-recurs every 18 months until the career either stalls or breaks. Senior professionals who compound learning have, in some form, the four practices this director routes: structured peer feedback (360s), self-aware performance reviews, a small set of trusted advisors who deliver hard truths, and a personal reflection practice that captures lessons before they fade.

This director routes the user to the right specialist by *kind of feedback loop* and helps integrate insights across loops so that they reinforce rather than fragment.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| 360-feedback-design | action | Designing a personal 360 — selecting raters, drafting questions, running the process, synthesizing the report |
| performance-review-craft | action | Writing self-assessments, preparing for review conversations, calibrating against rubric, "managing up" the review |
| advisor-board | action | Constructing and maintaining a personal advisory board — selection, cadence, asks, reciprocity |
| reflection-and-journaling | action | Reflection practice — daily / weekly / quarterly — and journaling structures that turn experience into nameable lessons |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| 360, peer feedback, anonymous, multi-rater, "I want unbiased feedback" | 360-feedback-design | "Help me run a 360 on myself" / "Design the questions for my 360" |
| Performance review, self-assessment, year-end, rubric, calibration, manager review | performance-review-craft | "Draft my year-end self-assessment" |
| Advisory board, advisors, mentors-collective, trusted-circle, kitchen cabinet | advisor-board | "Help me build a personal advisory board for the transition" |
| Reflection, journaling, retrospective, lessons, "what did I learn from X" | reflection-and-journaling | "Run a retrospective on the past quarter" |

## Multi-Skill Questions

1. **Annual Career Review** ("Help me run my own year-end review"):
   - Load `reflection-and-journaling` first — produce the raw lesson set
   - Load `360-feedback-design` to triangulate self-perception against peer perception
   - Load `performance-review-craft` to write the formal self-assessment
   - Hand off to `trajectory-design/idp-and-okrs` to convert lessons into next-year goals

2. **Pre-Transition Calibration** ("Before I make the move, I want to know where I really stand"):
   - Load `360-feedback-design` as primary — surface blind spots
   - Load `advisor-board` to triangulate with trusted advisors
   - Cross-reference `trajectory-design/skill-gap-analysis` once the picture is clear

3. **Quarterly Reflection Practice**:
   - Load `reflection-and-journaling` as primary
   - Cross-reference `trajectory-design/idp-and-okrs` for the goal context
   - Hand off to `product/the-loom` for the underlying decision-journal substrate

## Curriculum Order

1. **reflection-and-journaling** — Foundation. Without an internal practice, external feedback has no place to land. Start here.
2. **advisor-board** — Second. A small set of trusted external observers is the single highest-leverage feedback channel. Build it deliberately.
3. **360-feedback-design** — Third. A structured 360 every 18–24 months is the calibration tool — but it requires sufficient psychological safety to be useful, which the reflection practice and advisor board help create.
4. **performance-review-craft** — Specialized. When the user is in a formal review structure, this matters every cycle; otherwise it activates on-demand.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| 360 feedback contradicts the user's self-assessment | Trust the 360 when multiple raters converge; trust self-assessment only when supported by *external* evidence (specific results, dated artifacts) | Self-assessment has reliable known biases (Dunning-Kruger, attribution); multi-rater convergence is harder to fake |
| Advisor says "stay in current role another year"; user is ready to leave | Surface *why* the advisor says it — usually one specific concern; address the concern explicitly, then decide | Advisors usually compress complex judgments into a recommendation; the underlying reasoning is the actual value |
| Reflection practice produces lessons that contradict prior reflection practice | Welcome it — that is learning; update the journal explicitly with the date and reason for the update | A consistent journal that never updates is a journal that has stopped learning |

## Teaching Convention

Every leaf in this director includes `## Self-Coaching Track` (applied to the user's feedback practice, biotech-tilted) and `## Teach / Mentor-Others Track` (how you'd coach a junior or peer through the same practice). Default to producing both.

## Scope Boundaries

**This director handles**: All feedback collection, structuring, and integration — peer feedback, performance reviews, advisory feedback, self-reflection.

**Route elsewhere when**:
- The feedback reveals a need to *reframe the trajectory* → `trajectory-design`
- The feedback concerns *executive presence* specifically (delivery, presence) → `executive-presence`
- The feedback is *interview feedback* (post-loop debrief from a recruiter) → `interview-mastery` (debrief track)
- The reflection rises to a *life decision* (not a career decision) → outside Mentor's scope; recommend a therapist or coach

## Cross-Domain Connections

- **product/the-loom** — The Loom is the decision-journal substrate; reflection-and-journaling routes there for the writing practice
- **trajectory-design/idp-and-okrs** — Feedback loops feed the IDP cycle
- **executive-presence** — Feedback often targets presence specifically
- **binding-vow/audience-classifier** — Drafting self-assessments and 360 questions benefits from audience tuning
- **writing/prose-editor** — Self-assessment and 360 synthesis benefit from a prose-editor pass before sharing
