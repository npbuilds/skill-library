# Vault Output Templates

YAML scaffolds + body templates for each artifact type the Archon persists to the vault at `/Users/nirav/Documents/vault`.

**Constraints (from the vault's CLAUDE.md and `_meta/frontmatter-schema.md`):**
- All investment artifacts live in `Notes/` as `type: note` with `domain: investing`
- Discriminate by tag: `thesis | trade | session | macro | source` (exactly one "kind" tag)
- Add one asset-class tag: `equities | rates | commodities | currencies | crypto | credit | volatility | cross-asset`
- Thematic tags freely
- Use `maturity` (seedling | budding | evergreen) and `confidence` (confirmed | likely | contested | speculative | unverifiable) where load-bearing
- Slugs: `^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$` (kebab-case, lowercase, no spaces, no underscores)

vault-writer enforces all of this; an invalid call is rejected without writing.

---

## Thesis

Slug pattern: `<topic>-thesis` (e.g. `ai-capex-rollover-msft-thesis`)
Tags: `[thesis, <asset-class>, <theme>]`

### Frontmatter

```yaml
---
type: note
domain: investing
status: active
created: 2026-05-11
confidence: likely         # confirmed | likely | contested | speculative | unverifiable
maturity: budding          # seedling | budding | evergreen
last_verified: ""
tags: [thesis, equities, ai-infra, mag7]
---
```

### Body skeleton

```markdown
## Claim
<one-sentence thesis. Specific and falsifiable.>

## Conviction
<low | medium | high> — <one-line rationale>

## Time horizon
<days | weeks | months | years> — <expected catalyst window>

## Target
<the specific outcome that "proves" the thesis>

## Exit trigger
<the specific event or price that invalidates the thesis>

## Frameworks applied
<which of the six are operative: regime / contrarian / reflexivity / tail-risk / defense / sizing>

## Reasoning
<2-4 paragraphs. Lead with what consensus thinks; show your gap; quantify asymmetry.>

## What would prove me wrong
<3 bullets. Specific datums, not vague "if it doesn't work">

## Related
- [[<adjacent thesis>]]
- [[<source-slug>]]
```

### vault-writer call

```
target_type: note
target_domain: investing
slug: ai-capex-rollover-msft-thesis
target_folder: Notes/
frontmatter_extra: {confidence: likely, maturity: budding, last_verified: ""}
tags: [thesis, equities, ai-infra, mag7]
log_op: ingest
log_details: "thesis: AI capex rollover (MSFT lens)"
overwrite_policy: fail
```

If updating: write a new note `<slug>-v2.md` and add `Supersedes: [[ai-capex-rollover-msft-thesis]]` at the top of the body. Don't overwrite a thesis — keep the lineage visible.

---

## Trade (open / close)

Slug pattern: `<topic>-trade` (e.g. `long-tlt-stagflation-trade`)
Tags on open: `[trade, <asset-class>, open]` → re-tag to `[trade, <asset-class>, closed]` on exit

### Frontmatter

```yaml
---
type: note
domain: investing
status: active
created: 2026-05-11
maturity: budding          # → evergreen on close (outcome known)
confidence: ""             # (claim-by-claim in body)
last_verified: ""
tags: [trade, rates, open]
---
```

### Body skeleton (open)

```markdown
## Position
<asset, direction, instrument (e.g., long TLT calls; short HYG)>

## Thesis ref
[[<thesis-slug>]]

## Entry
- Date: <YYYY-MM-DD>
- Price/level: <entry>
- Size: <position-size as % of portfolio>
- Stop-loss: <specific level>

## Sizing logic
<conviction + risk budget → size. Druckenmiller lens.>

## Frameworks active
<which frameworks justify this position>

## Invalidation
<what proves the trade wrong vs unlucky — Tudor Jones lens>

## Catalyst calendar
<dated events between entry and expected resolution>
```

### Body skeleton (close — append + re-tag)

```markdown
## Close
- Date: <YYYY-MM-DD>
- Price/level: <exit>
- P&L: <%>
- Reason: <hit stop | hit target | thesis invalidated | time decay | better idea>

## Outcome
<right / wrong / right-for-wrong-reasons / inconclusive>

## Lessons
<2-3 bullets. What did this teach about the framework, the market, or my process?>
```

### vault-writer call (close)

```
overwrite_policy: overwrite
tags: [trade, rates, closed]   # re-tagged
log_op: fix
log_details: "trade closed: long-tlt-stagflation (outcome: <right|wrong>)"
```

---

## Session synthesis

Slug pattern: `<YYYY-MM-DD>-<topic>` (e.g. `2026-05-11-ai-capex`)
Tags: `[session, <topics>]`

### Frontmatter

```yaml
---
type: note
domain: investing
status: active
created: 2026-05-11
maturity: seedling
confidence: ""             # sessions aren't load-bearing claims
last_verified: ""
tags: [session, ai-infra, reflexivity, mag7]
---
```

### Body skeleton

(See `conversational-loop.md` Synthesis skeleton.)

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

## Predictions logged
<links to log_prediction IDs, if any>

## Related
- [[<thesis-slug>]]
- [[<source-slug>]]
```

---

## Macro view

Slug pattern: `<theme>` (e.g. `stagflation-regime` or `dollar-system-2026`)
Tags: `[macro, <regime>, <theme>]`

### Frontmatter

```yaml
---
type: note
domain: investing
status: active
created: 2026-05-11
confidence: likely         # regime claims are load-bearing
maturity: budding          # seedling = nascent thesis; evergreen = durable
last_verified: 2026-05-11
tags: [macro, stagflation, fiscal-dominance]
---
```

### Body skeleton

```markdown
## Regime classification
<the operative regime per Dalio's 2x2 + any nuance>

## Time horizon
<expected duration of the regime>

## Key drivers
<3-5 bullets. What's structurally producing the regime?>

## Active themes (ranked by conviction)
<numbered list with conviction tag per theme>

## Tells of regime shift
<5-7 signals that would indicate transition. Specific thresholds where possible.>

## Asset implications
- Equities: <stance>
- Rates: <stance>
- Credit: <stance>
- Commodities: <stance>
- Currencies: <stance>

## Related
- [[<thesis-slug>]]
- [[<adjacent macro note>]]
```

Use `overwrite_policy: append` for macro views — themes evolve. Each append should include a date subheading: `### Update YYYY-MM-DD`.

---

## Source (research capture)

Spelunker's Phase 6 produces these automatically via vault-writer. For manual source captures:

Slug: `<source-slug>` (e.g. `bridgewater-debt-cycle-2026q1`)
Companion in `Raw/`: `<slug>-<date>.<ext>`

### Frontmatter

```yaml
---
type: source
domain: investing
status: active
created: 2026-05-11
source_type: paper           # paper | web | book | interview | internal-doc | other
url: "https://..."
author: "Ray Dalio"
accessed: 2026-05-11
path: "Raw/bridgewater-debt-cycle-2026q1.pdf"
tags: [source, macro, debt-cycle]
---
```

### Body

Summary in your own words. Never reproduce >15 contiguous words verbatim. Cross-link to related Notes/ with `[[wikilinks]]`.

### vault-writer call (via Workflow 1)

```
target_type: source
target_domain: investing
slug: bridgewater-debt-cycle-2026q1
target_folder: Notes/
companion_source_path: Raw/bridgewater-debt-cycle-2026q1.pdf
companion_body: "<abstract or 1-paragraph summary>"
tags: [source, macro, debt-cycle]
log_op: ingest
log_details: "ingest: Bridgewater debt cycle paper"
```

---

## Notes on overwriting

| Tag pattern | Default overwrite_policy | Why |
|---|---|---|
| `thesis` | `fail` | Theses evolve via new slugs + `Supersedes:` chain |
| `trade, open` → `closed` | `overwrite` | Same trade record, updated status |
| `session` | `fail` | Sessions are immutable conversation records |
| `macro` | `append` | Themes evolve in-place with dated update sections |
| `source` | `fail` | Sources are immutable |

When `overwrite` is used for a trade close, the orchestrator should preserve the original Entry/Sizing/Invalidation sections and append the Close + Outcome + Lessons sections. Don't overwrite the file body entirely.
