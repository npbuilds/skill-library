---
name: personal-positioning
description: >
  Direct narrative architecture, LinkedIn optimization, public portfolio strategy, credibility
  translation, audience tuning, resume craft, and cover letter craft to the right specialist
  skill. Activate when the user is shaping how they show up to a target audience — refreshing
  a resume, drafting a cover letter, rewriting a LinkedIn About, deciding what to publish on
  GitHub, or translating clinical credibility for non-clinical audiences. Personal positioning
  is the discipline of being legible to the rooms you want to enter.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Personal Positioning Director

The hardest part of a career transition is not changing what you can do — it is changing how you are *read*. The same trial-design judgment that makes you a senior clinical scientist makes you an investable operator, but only if the people in the next room can see it. Personal positioning is the discipline of producing legibility on demand: a resume tuned to a specific job description, a LinkedIn About that signals the trajectory, a cover letter that proves you have read the firm, a public artifact that demonstrates how you think.

This director routes positioning questions to the right specialist and sequences multi-skill work so that narrative coherence holds across surfaces. A resume that contradicts the LinkedIn that contradicts the cover letter signals carelessness — the opposite of the legibility you are trying to produce.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| narrative-architecture | knowledge | Building or refreshing the underlying career story arc — the "why now," the through-line, the role-archetype thesis |
| linkedin-optimization | action | Profile, headline, About, featured section, activity strategy, recruiter visibility |
| public-portfolio | action | What to publish on GitHub, blog, or other public surfaces; how to use a public artifact as proof of work |
| credibility-translation | knowledge | Converting clinical-vocabulary credentials into operator/investor vocabulary the target audience parses |
| audience-tuning | action | Same story, different audiences (clinical peer, exec, VC partner, board) — what to emphasize and what to suppress |
| resume-craft | action | Building or refreshing a resume; converting an academic CV to an industry resume; tailoring a resume to a specific JD |
| cover-letter-craft | action | Drafting a firm-specific, thesis-aware cover letter for a job, fellowship, board seat, or advisory role |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| "What is my story?" / "Why am I making this move?" / "How do I explain this transition?" | narrative-architecture | "Help me write the through-line for my pivot" / "What's my one-sentence positioning?" |
| LinkedIn, profile, headline, About section, recruiter visibility, activity | linkedin-optimization | "Rewrite my LinkedIn About" / "What should my headline say?" |
| GitHub, blog, public writing, portfolio, proof of work, what to publish | public-portfolio | "What should I publish to show I think like an operator?" |
| MDs / clinical / academic vocabulary → operator / investor / board language | credibility-translation | "How do I describe running a Phase 2 in operator language?" |
| Same content, different audience; recruiter vs partner vs peer | audience-tuning | "Rewrite this bullet for a VC partner instead of a recruiter" |
| Resume, CV, bullet rewrites, JD tailoring, one-page vs two-page | resume-craft | "Convert my CV to a one-page operator resume" |
| Cover letter, application letter, firm-specific intro, board letter | cover-letter-craft | "Draft a cover letter for [firm] partner role" |

## Multi-Skill Questions

Most real positioning work spans multiple children. Common combinations:

1. **Narrative + Resume + LinkedIn** ("I'm starting my search; help me get my materials in shape"):
   - Load `narrative-architecture` first to establish the through-line
   - Then `resume-craft` and `linkedin-optimization` in parallel, both sourced from the named through-line
   - Finally `audience-tuning` to produce a per-target-archetype variant

2. **Cover Letter for a Specific Firm** ("Draft a cover letter for [firm]"):
   - Load `cover-letter-craft` as primary
   - It will hand off to `research/spelunker` for firm-specific research before drafting
   - Then `credibility-translation` to ensure the credibility paragraph speaks the firm's language
   - Finally a `writing/prose-editor` pass for polish

3. **Public Portfolio Strategy** ("What should I be publishing on my GitHub?"):
   - Load `public-portfolio` as primary
   - Cross-reference `narrative-architecture` to ensure published work reinforces the named through-line
   - Cross-reference `credibility-translation` to ensure the framing is legible to the target audience

## Curriculum Order

1. **narrative-architecture** — Foundation. Without a named through-line, every artifact drifts. This is always first.
2. **credibility-translation** — Second. Once you know the trajectory, translate your existing credentials into the target audience's language.
3. **resume-craft + linkedin-optimization** — Built in parallel from the same source. Each is a tuned surface of the same underlying story.
4. **cover-letter-craft** — Per-application work. Always firm-specific; never generic.
5. **public-portfolio** — Long-horizon. The artifact you publish today is the credibility you draw on next year.
6. **audience-tuning** — A practice that runs continuously across all surfaces.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Resume emphasizes scientific depth; cover letter emphasizes operator framing — they read inconsistently | `narrative-architecture` resolves: both must serve the same through-line, with depth-of-emphasis tuned per surface | Inconsistency across surfaces is itself a signal — usually negative |
| LinkedIn About reads VC-ready but title says "Director, Clinical Scientist" — recruiters confused | `audience-tuning` resolves: keep the title accurate; use the About to position toward the trajectory | Misrepresentation of the title is dishonest and recruiter-detectable; positioning happens in the prose |
| Public portfolio includes work that doesn't match the trajectory (e.g., side hobbies dominating GitHub) | `public-portfolio` resolves: not every public artifact serves the trajectory; pin and prioritize the ones that do | Visitors look at top-pinned work, not your full activity |

## Teaching Convention

Every leaf in this director includes a `## Self-Coaching Track` (applied to your situation, biotech-tilted) and a `## Teach / Mentor-Others Track` (how you'd explain this to a junior or in an interview). When responding from any leaf, default to producing both. This convention is documented in the Mentor orchestrator.

## Scope Boundaries

**This director handles**: All questions about how the user shows up across written and live surfaces — resume, CV, LinkedIn, GitHub, blog, cover letter, professional bio, board bio.

**Route elsewhere when**:
- The question is about live conversation craft (interview answers, panel performance) → `interview-mastery`
- The question is about building the relationships that *consume* the positioning → `network-cultivation`
- The question is about the underlying trajectory itself (which role to target) → `trajectory-design`
- The question concerns how to *speak* in front of a room (not write for it) → `executive-presence/public-speaking` or `executive-presence/meeting-mastery`

## Cross-Domain Connections

- **binding-vow/audience-classifier, bluf-shaper, executive-distiller, minto-scqa** — Audience taxonomy and executive-prose craft underpin audience-tuning, resume bullets, and cover letter openings
- **design/brand-identity/brand-foundations, brand-voice** — Personal narrative borrows the brand-identity discipline applied to a person
- **writing/prose-editor** — Final polish pass on every written artifact
- **research/spelunker** — Firm research before cover letter drafting
- **biotech-venture/asclepius** (and clinical-development director) — Source of the clinical-content the user is translating
