---
name: decision-journal
description: >
  Persists purchase research and learns from outcomes: appends research runs to
  data/decision-journal.jsonl, purchases and 30-day check-ins to data/purchases.jsonl,
  maintains data/consumer-preferences.json, and mirrors briefs into the user's Obsidian
  vault via vault-writer when reachable. Use at the start of an emptor run (recall priors),
  at its end (persist the brief), and when /purchase-log or /purchase-review fire. Closes
  the calibration loop by resolving brief confidence against real satisfaction.
metadata:
  author: nirav
  version: "1.0"
type: action
compatibility: Designed for Claude Code
allowed-tools: Read Write bash Glob Grep
---

# Decision Journal — The Memory

Action skill: the suite's persistence and learning layer. A recommendation engine that never learns whether its picks worked is unfalsifiable; this journal records what was researched, what was bought, and how it turned out — feeding both the existing calibration ledger and a preference profile that makes the next run smarter.

## Description

Dual persistence: append-only JSONL in `data/` is the canonical machine log (works in any session, cloud or desktop); the user's Obsidian vault is the human-readable mirror, written via `vault-writer` and read via `vault-reader` (`skills/infrastructure/`). When the vault is unreachable, JSONL still lands and the entry is marked `vault_synced: false` for catch-up sync on the next vault-reachable session.

## Input

One of four operations from the caller:

| Operation | Caller | Payload |
|---|---|---|
| `recall` | emptor Phase 0 | category / product type |
| `persist_brief` | emptor Phase 8 | the delivered brief + requirements spec |
| `log_purchase` | `/purchase-log` | brief_id, product, price, merchant |
| `log_checkin` | `/purchase-review` | brief_id, satisfaction 1-5, notes |

## Process

**recall** — Read `data/consumer-preferences.json` (cold start: silently skip) and scan `data/decision-journal.jsonl` for same-category runs; if a `vault_path` is configured and reachable, also `vault-reader` text-search/tag-filter for prior purchase notes. Return priors (weight priors, recurring must-haves, prior briefs, pending check-ins) for `needs-elicitor` to propose — never auto-apply.

**persist_brief** —
1. Append one line to `data/decision-journal.jsonl` (schema below).
2. Write the full brief to `research/consumer-briefs/CRS-<id>.md` — this makes the brief ID resolvable by the existing `/calibrate` command, which searches `research/`.
3. Vault mirror (when reachable): `vault-writer` with the full brief as a `Raw/` companion source and a `Notes/<slug>.md` decision note (frontmatter per the vault's `_meta/frontmatter-schema.md`; `confidence`, `last_verified`; tags incl. `purchase-decision` + category). Schema mismatch → fall back to JSONL-only and tell the user which schema extension would enable sync (schema changes are deliberate user acts; vault-writer is fail-closed).
4. Record `vault_synced: true|false` on the journal line.

**log_purchase** — Append a `purchase` event to `data/purchases.jsonl`; set `followed_top_pick`; warn if the merchant was not trust-checked in the brief; remind about the 30-day `/purchase-review`. Vault note gets the purchase appended (`overwrite_policy: append`) when reachable.

**log_checkin** — Append a `check_in` event; map satisfaction → calibration outcome (≥4 → `true`, 3 → `partial`, ≤2 → `false`) and append to `data/calibration.jsonl` with `claim_id: "top-pick"` and the brief's predicted confidence; update the preference profile (weight priors from what mattered in hindsight, brand/merchant lists, satisficer lean, regret triggers from `surprises`); append the verdict to the vault note when reachable.

**Catch-up sync** — any operation that finds `vault_synced: false` entries while the vault is reachable offers to sync them; never blocks the primary operation.

## Output

Schemas (canonical, append-only):

`data/decision-journal.jsonl` — one line per run:
```json
{"brief_id":"CRS-20260610-robvc4","ts":"<iso8601>","query":"...","category":"home/floor-care","depth":"standard","jtbd":{...},"must_haves":[...],"weighted_criteria":[{"criterion":"...","weight":0.35}],"budget":{"cap":400,"currency":"USD","locked_before_prices":true},"candidates_considered":23,"finalists":[...],"top_pick":{"product":"...","confidence":"Likely","price_seen":329},"runners_up":[...],"sensitivity":"stable","satisficing_exit_offered":true,"sources_used":[{"name":"Rtings","tier":1,"age_months":2}],"forensics_flags":[...],"availability_checks":{...},"brief_path":"research/consumer-briefs/CRS-20260610-robvc4.md","vault_synced":false}
```

`data/purchases.jsonl` — events discriminated by `event`:
```json
{"event":"purchase","brief_id":"...","ts":"...","product":"...","followed_top_pick":true,"price_paid":315,"merchant":"...","merchant_trust":"verified","notes":""}
{"event":"check_in","brief_id":"...","ts":"...","days_since_purchase":32,"satisfaction":4,"would_rebuy":true,"must_haves_held":{...},"surprises":["..."],"calibration_outcome_written":true,"notes":""}
{"event":"return","brief_id":"...","ts":"...","product":"...","reason":"..."}
```

`data/consumer-preferences.json` — mutable compiled profile, regenerable from the JSONLs:
```json
{"updated_at":"...","global":{"satisficer_lean":0.7,"recurring_must_haves":[...],"trusted_merchants":[...],"blocked_merchants":[...],"budget_style":"value"},"categories":{"home/floor-care":{"runs":2,"weight_priors":{...},"brands_liked":[...],"brands_avoid":[...],"last_brief":"CRS-..."}}}
```

## Error Handling

| Failure | Response |
|---|---|
| Vault unreachable (cloud session) | JSONL only; `vault_synced: false`; no error to user beyond one line |
| Vault schema rejects the note | Fall back; report which fields the vault schema would need |
| Unknown brief_id on log/check-in | List recent brief IDs from the journal; do not write |
| Malformed JSONL line encountered | Skip and report; never rewrite history |

## Scope Boundaries

**Handles:** persistence, recall, profile learning, calibration hand-off.
**Does not:** make or alter recommendations, edit past entries (append-only), or extend the vault schema.

## Related Skills

- Reuses `vault-writer`/`vault-reader` (infrastructure) and the `/calibrate` ledger; serves `emptor` Phases 0 and 8.

## Learn Block

With the journal understood, learn the `emptor` orchestrator — the pipeline all of this serves.
