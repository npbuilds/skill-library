# Minto Scqa — Quick Reference


## Quick Reference

| Element | Purpose | Example |
|---|---|---|
| **Situation** | A familiar truth the reader already accepts | "We have grown 3× in the last two years." |
| **Complication** | Something has changed, or a tension has emerged | "But customer churn has accelerated to 12%." |
| **Question** | The implicit question the complication raises | "What's driving the churn and how do we stop it?" |
| **Answer** | The governing thought (top of the pyramid) | "Churn is driven by onboarding; we should rebuild it in Q3." |

## Quick Reference

| Variant | Use when |
|---|---|
| Standard SCQA | Reader is informed but unfocused |
| SCRA (Resolution instead of Q→A) | Reader knows the answer; you're proposing what to do |
| Concern-priming SCQA | Reader is skeptical; lead with their objection |

## Quick Reference

| Failure | Symptom | Fix |
|---|---|---|
| Not ME | "The three reasons are: cost, complexity, and the engineering team's skill." | Cost and complexity overlap; restructure |
| Not CE | "Customers leave for two reasons: price and product." | What about service, alternatives, life changes? |
| False parallel | "The plan has three phases: discovery, planning, and exiting" | "Exiting" isn't parallel to discovery and planning; structural mismatch |

## Quick Reference

| Audience | Default structure | Why |
|---|---|---|
| Exec (decision-maker, time-pressured) | BLUF for short; SCQA-Pyramid for memos | They need the answer first; supporting detail second |
| Peer (collaborator, parallel context) | SCQA | Story structure invites engagement; matches conversational priors |
| Self (your own clarity) | Pyramid (skip SCQA intro) | You already have the situation; you need the structure |
| Public (broad audience, mixed context) | SCQA with Concern-priming | Trust must be built; objections pre-empted |
| LLM | Anthropic-canonical structural order (see `cursed-speech`) | Different audience entirely; format-shape matters more than narrative |

## Quick Reference

| Compression skill | Implements |
|---|---|
| `bluf-shaper` (binding-vow, future) | BLUF format directly |
| `scqa-formatter` (binding-vow, future) | SCQA introduction + 1-level pyramid |
| `executive-distiller` (binding-vow, future) | Full Pyramid Principle with N-level recursion |
| `cursed-speech` (binding-vow, future) | NOT Minto — Anthropic-canonical order. Minto is for humans; LLMs need different shape. |

## Formula / Pseudocode

```
[Single governing thought]
                    /             |             \
            [Subthought 1]  [Subthought 2]  [Subthought 3]
              /     \         /     \         /     \
          [...]   [...]   [...]   [...]   [...]   [...]
```

## Formula / Pseudocode

```
BOTTOM LINE: [One sentence — the recommendation or finding]

BACKGROUND: [What changed; minimum context to make the bottom line make sense]

DISCUSSION: [The reasoning, in priority order]

RECOMMENDATION: [Specific action(s) requested]
```
