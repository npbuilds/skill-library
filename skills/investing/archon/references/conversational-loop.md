# Conversational Loop — The Analytical Session

The Archon's session protocol for chat-mode investment thinking. Read this before opening a session; consult mid-session to surface context; follow the close protocol at exit.

## Opening prompts

Pick the opener that matches the user's framing. Don't recite all four — just lead.

- **Open-ended:** "What's on your mind? Trade idea, regime question, position review, or something else?"
- **Continuation:** "Are we picking up a thread, or starting fresh? Anything from the macro narrative I should re-read first?"
- **Regime-first:** "Want a quick regime check before we dive in? Current frame: [stagflation / late-cycle / mid-cycle expansion]. Useful to anchor against or skip?"
- **Conviction surface:** "How firm is this for you — a hunch you want to stress-test, or something you're sized into already?"

The opener is also the first chance to classify the question (see SKILL.md "Chat-Mode Routing" Step 1).

## Mid-session checkpoints

Surface the session context every ~3 user turns or at any director handoff. Light touch — one or two lines, not a recap dump.

```
Session context so far:
  Regime: stagflation (set turn 1)
  Operative subdomains: value-quality, reflexivity-sentiment
  Key assumptions: AI capex demand is ahead of consumption proof
  Decisions pending: thesis logging, sizing
```

When you cross a director boundary (e.g. moving from regime-intelligence to risk-architecture), say so explicitly: *"Switching to risk-architecture for sizing reasoning."* This makes handoffs legible to the user and to any escalated skill.

## Escalation triggers

Don't silently invoke — name the escalation in conversation.

| Trigger | Offer |
|---|---|
| Named assumption could be wrong | "Want me to verify that with spelunker?" |
| What-if branching needed | "Stress-test via neocortex/scenario-planner?" |
| Concept needs cross-domain translation | "Want neocortex/domain-translator to map this to another asset class?" |
| Investing capability seems missing | "Worth asking neocortex/skill-evolutionist about?" |
| Concept needs plain-language explanation | "Want neocortex/clarity-engine to take a pass?" |

Spelunker auto-persists research to the vault (`Notes/<slug>.md` + `Raw/<slug>-research-brief-<date>.md`) — no extra step needed. Neocortex outputs are conversational; persist via vault-writer if worth keeping.

## Session-close protocol

Offer the close menu when the user signals end (any of: "let's stop here," "I need to think on this," "OK that's enough for now," or a long pause after a synthesis).

```
Wrap-up — anything to persist?
  [a] Yes — write session synthesis to Notes/<YYYY-MM-DD>-<topic>.md
  [b] Yes + thesis — also write Notes/<topic>-thesis.md (tagged thesis)
  [c] No — chat is ephemeral
```

(Prediction logging retired 2026-07-26 — never offer it.)

If [a] or [b], confirm the slug ("Persist as `2026-05-11-ai-capex`? [y / edit]") before invoking vault-writer.

### Synthesis skeleton

When persisting a session, structure the body as:

```markdown
## Topic
<one-line framing>

## Frameworks applied
<which of the six were active in this session — 1-3 typical>

## Conclusions
<2-5 bullets, each with confidence tag when load-bearing>

## Open assumptions
<unverified claims that, if wrong, change the conclusion>

## Decisions pending
<sizing, entry/exit, what to revisit, what to research next>
```

Keep it tight — sessions are conversation digests, not deep dives. The user can promote a session synthesis to a full thesis later by writing `Notes/<topic>-thesis.md` and linking back.

## What NOT to do

- Don't auto-invoke spelunker or neocortex — name them as offers
- Don't pull live data tools unless the user asks ("what's the current VIX?")
- Don't recite all six frameworks in one turn — Chat-Mode Routing Step 3 says single-domain or primary-with-flag
- Don't generate a structured 7-section briefing — that's the briefing-mode protocol, deactivated since 2026-05-11
- Don't write to the vault without confirmation — vault-writer is fail-closed, but human-in-loop is the convention
