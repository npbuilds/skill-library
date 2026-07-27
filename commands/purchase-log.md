---
name: purchase-log
description: Record a purchase (or pass) against an emptor brief — populates data/purchases.jsonl and starts the 30-day check-in clock
argument-hint: "<brief-id> <product|passed> [price] [merchant] [notes]"
---

Record what the user actually did with an emptor recommendation. This is half of the suite's learning loop (the other half is `/purchase-review`).

Parse `$ARGUMENTS`:
1. **brief_id** (required) — e.g., `CRS-20260610-robvc4` (from the brief footer)
2. **product** (required) — what was bought, or the literal `passed` if they decided not to buy
3. **price** (optional) — actual price paid
4. **merchant** (optional)
5. **notes** (optional)

If malformed, show usage: `/purchase-log CRS-20260610-robvc4 "Robovac A2" 315 manufacturer-store`

Steps:

1. Look up the brief: search `data/decision-journal.jsonl` for the brief_id (fallback: `research/consumer-briefs/`). Unknown ID → list the 5 most recent brief IDs and stop; do not write.
2. Determine `followed_top_pick` by comparing the product to the brief's top pick.
3. If a merchant is given and it wasn't trust-checked in the brief (or was marked `caution`/`avoid`), warn — but record what the user did.
4. Append one line to `data/purchases.jsonl`:
   ```json
   {"event":"purchase","brief_id":"<id>","ts":"<iso8601>","product":"<product>","followed_top_pick":true,"price_paid":315,"merchant":"<merchant or null>","merchant_trust":"verified|caution|avoid|unchecked","notes":"<text>"}
   ```
   For `passed`, use `{"event":"decision","decision":"passed",...}` with a reason in notes if given.
5. If the user's Obsidian vault is reachable, append the purchase to the brief's vault decision note via `vault-writer` (`overwrite_policy: append`); otherwise note the pending sync.
6. Confirm:
   ```
   Logged: <product> against <brief_id> (followed pick: yes/no)
   Check back in ~30 days: /purchase-review <brief_id> <1-5> [notes]
   ```
