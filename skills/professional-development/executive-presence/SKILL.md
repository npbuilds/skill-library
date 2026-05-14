---
name: executive-presence
description: >
  Direct executive communication, meeting mastery, public speaking, and board readiness to
  the appropriate specialist skill. Activate when the user is preparing to *show up* at an
  executive level — running a meeting, presenting to a board, giving a conference talk,
  writing an exec memo, or stepping into a board-adjacent role. Executive presence is the
  discipline of being read as senior when you are in the room, in print, and on stage.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Executive Presence Director

Executive presence is not personality; it is a small bundle of trainable behaviors — how you open a memo, how you handle a meeting derailment, how you accept a question you cannot fully answer, how you decline a request without burning the relationship. The clinicians and scientists who acquire it most quickly are the ones who treat it as craft (rehearsable, debuggable, improvable) rather than as character. This director routes that craft to the right specialist.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| executive-communication | action | Exec-grade written communication — memos, decks, BLUF-structured updates, recommendations, board materials |
| meeting-mastery | action | Running and contributing to meetings — agenda design, opening moves, derailment recovery, decision protocols, follow-ups |
| public-speaking | action | Conference talks, podcast appearances, panel performance, keynote-style remarks |
| board-readiness | knowledge | Preparing to take a board seat (observer or director) — fiduciary literacy, board-meeting protocol, IC dynamics |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| Memo, exec summary, BLUF, deck, recommendation, board materials | executive-communication | "Help me write a board update on our trial readout" |
| Meeting, agenda, decision, derailment, follow-up, "run the room" | meeting-mastery | "Design the agenda for tomorrow's strategy offsite" |
| Conference, podcast, panel, keynote, public talk | public-speaking | "Prep me for the panel at [conference]" |
| Board seat, fiduciary, IC, governance, directorship | board-readiness | "I've been offered a board observer seat — prep me" |

## Multi-Skill Questions

1. **Conference Talk + Subsequent Networking** ("Prep me for the keynote and the dinner after"):
   - Load `public-speaking` as primary for the talk
   - Cross-reference `meeting-mastery` for the dinner-as-meeting structure
   - Hand off to `network-cultivation/relationship-stewardship` for follow-up

2. **Board Meeting Presentation** ("I'm presenting to the board next month"):
   - Load `executive-communication` for the board materials
   - Load `meeting-mastery` for the presentation flow
   - Load `board-readiness` for the protocol / fiduciary context

3. **Decision Memo to CEO** ("Draft a memo recommending we drop the program"):
   - Load `executive-communication` as primary
   - Hand off to `binding-vow/bluf-shaper` and `binding-vow/executive-distiller` for the prose craft
   - Cross-reference `biotech-venture/asclepius/deal-synthesis` for the underlying recommendation logic

## Curriculum Order

1. **executive-communication** — Foundation. Written craft is the highest-leverage exec skill; one good memo creates an artifact that travels.
2. **meeting-mastery** — Second. Most exec work happens in meetings; the ability to *run* a meeting is what separates senior from staff.
3. **public-speaking** — Third. External-facing voice; trainable but lower frequency than written and meeting work.
4. **board-readiness** — Specialized. When the user is on a board track, this becomes essential; otherwise it remains a future-prep skill.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Executive memo wants brevity; the underlying analysis genuinely requires nuance | Use BLUF for the headline + summary, then append the nuance as a section labeled "If you want the full reasoning" | Exec readers scan; the doc must serve the scan and the deep-read on the same page |
| Meeting is going off the rails; the urge is to "let it play out" | Name it explicitly ("we have 15 minutes; let me name what we still need to decide") | Naming the derailment is the senior move; tolerating it is the staff move |
| Public talk wants to be the user's authentic voice; the venue rewards a more performative voice | Start from authentic; layer in performative shape (pace, repetition, contrast) as craft on top | Authenticity without craft is monotony; craft without authenticity is theater |

## Teaching Convention

Every leaf in this director includes `## Self-Coaching Track` (applied to the user's situation) and `## Teach / Mentor-Others Track` (how you'd coach a junior through the same skill). Default to producing both.

## Scope Boundaries

**This director handles**: How the user shows up at an executive level — in writing, in meetings, on stage, in board contexts.

**Route elsewhere when**:
- The question is about interview performance specifically → `interview-mastery`
- The question is about written *positioning* artifacts (resume, LinkedIn, cover letter) → `personal-positioning`
- The question is about technical content of the message (not the delivery) → relevant functional domain (biotech-venture, data-science, etc.)

## Cross-Domain Connections

- **binding-vow/bluf-shaper, executive-distiller, minto-scqa, audience-classifier** — Executive communication's core craft is inherited from binding-vow
- **writing/prose-editor** — Final polish on every exec written artifact
- **biotech-venture/asclepius/deal-synthesis** — Source of the substance for biotech-context exec communication
- **product/the-loom** — Decision journaling around exec choices
- **investing/archon** — Board readiness in venture-backed companies inherits literacy from Archon's portfolio framing
