---
name: network-cultivation
description: >
  Direct cold outreach, relationship stewardship, mentorship design, ecosystem mapping, and
  introductions / referrals to the appropriate specialist skill. Activate when the user is
  building or maintaining the relationships that compound into opportunities — sending a
  first email to a partner, designing a mentor cadence, mapping a venture ecosystem,
  asking for or giving an introduction. The compounding asset of a career is a small
  number of high-trust relationships, not a large number of weak ones.
metadata:
  author: nirav
  version: "1.0"
compatibility: Designed for Claude Code
allowed-tools: Read
---

# Network Cultivation Director

A career system that wins over a decade is the one that nurtures a small number of high-trust relationships, not the one that maximizes weekly LinkedIn touchpoints. Most clinicians are bad at this — not because they are unfriendly, but because the institutional structure of medicine substitutes for it. In academic medicine, your fellowship director, your division chief, and your trial PIs are your network by default. Outside that structure, the network has to be built deliberately. This director routes that work.

## Child Skills

| Skill | Type | When to Use |
|---|---|---|
| cold-outreach | action | Sending a first email or DM to someone you do not yet know — partner, founder, operator, recruiter |
| relationship-stewardship | action | Maintaining warm relationships over months and years — cadence, touchpoint craft, light CRM |
| mentorship-design | action | Finding mentors (and being a mentor) — structure, asks, reciprocity, cadence, exit-with-grace |
| ecosystem-mapping | action | Mapping a target landscape — VC firms in a thesis, operating teams at a stage, people-of-interest network graphs |
| introductions-and-referrals | action | Asking for, giving, and tracking introductions — the warm-intro economy that moves senior careers |

## Routing Logic

| Question Signal | Route To | Examples |
|---|---|---|
| Cold email, DM, reach out, never met, first message | cold-outreach | "Draft a cold email to [partner]" / "How should I message this VC?" |
| Keep in touch, nurture, check in, cadence, CRM | relationship-stewardship | "I haven't talked to X in 6 months, how do I re-warm?" |
| Mentor, mentee, advisor, coaching, sponsor | mentorship-design | "How do I ask someone to be my mentor?" |
| Map, landscape, who's who, ecosystem, target list | ecosystem-mapping | "Map the early-stage biotech VCs in oncology" |
| Intro, warm intro, referral, "can you connect me," double opt-in | introductions-and-referrals | "Ask my contact for an intro to X" |

## Multi-Skill Questions

1. **Full Search Network Setup** ("I'm starting a search; help me build my network plan"):
   - Load `ecosystem-mapping` first — produce the target landscape
   - Then `relationship-stewardship` to triage existing relationships against the target list
   - Then `cold-outreach` for the gaps that warm intros cannot cover
   - Then `introductions-and-referrals` for the warm-intro paths
   - All work routed through a single tracker (suggest Loom-style notes or a Notion)

2. **Re-Warming a Cold Relationship** ("I haven't talked to X in 2 years and want to reach out"):
   - Load `relationship-stewardship` as primary — re-warming is its own move
   - Cross-reference `cold-outreach` for the message structure (it is cold-adjacent)

3. **Mentor Search** ("Help me find a mentor for the venture transition"):
   - Load `mentorship-design` as primary
   - Load `ecosystem-mapping` to build the candidate set
   - Load `cold-outreach` for first messages where warm-intro is unavailable

## Curriculum Order

1. **ecosystem-mapping** — Foundation. Without a map, all other network activity is random.
2. **relationship-stewardship** — Second. The relationships you already have are usually undermanaged; fix that before adding more.
3. **introductions-and-referrals** — Third. The warm-intro economy is how senior moves actually happen.
4. **cold-outreach** — Fourth. The fallback when warm-intro is unavailable, and a craft in its own right.
5. **mentorship-design** — Continuous. Mentor relationships are a special case that runs in parallel to all of the above.

## Conflict Resolution

| Conflict | Resolution | Reason |
|---|---|---|
| Cold outreach wants to feel personalized; over-personalization (mentioning their kid's school) reads as creepy | Personalize to *professional* signal only (a recent essay, a public post, a deal they led) | Personal-life personalization signals stalking, not preparation |
| Stewardship cadence wants to be regular; recipient may feel pestered | Tie touchpoints to *signal* (their post, their deal, a relevant article) not to *calendar* | Calendar-driven check-ins read as transactional; signal-driven ones read as engaged |
| Asking for an intro feels presumptuous, but warm-intro economy requires asking | Use double-opt-in: ask the connector if they'd be comfortable forwarding a short blurb the recipient can accept or decline silently | Double-opt-in preserves the connector's social capital |

## Teaching Convention

Every leaf includes `## Self-Coaching Track` (applied to the user's network, biotech-tilted) and `## Teach / Mentor-Others Track` (how to coach a junior or peer through this craft). Default to producing both.

## Scope Boundaries

**This director handles**: Building, maintaining, and using a professional network — at any scale, for any career goal.

**Route elsewhere when**:
- The question is about what to *say* once the conversation happens → `interview-mastery` or `executive-presence`
- The question is about your *positioning* across surfaces (not the relationships) → `personal-positioning`
- The question is about *which* trajectory to pursue (not who to talk to about it) → `trajectory-design`

## Cross-Domain Connections

- **research/spelunker, source-triangulator** — Ecosystem mapping is, mechanically, a research task
- **product/the-loom** — Light CRM and decision-journaling for relationship work
- **writing/prose-editor** — Outreach and stewardship messages finish with a prose-editor pass
- **personal-positioning/cover-letter-craft** — Cold outreach to firms often includes a short cover-letter-style ask
- **biotech-venture/asclepius** — Ecosystem mapping in biotech VC is partly a thesis-mapping exercise; Asclepius is the substance
