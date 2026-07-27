---
name: purchase-review
description: Post-purchase satisfaction check-in — resolves the brief's pick into the calibration ledger and updates learned preferences
argument-hint: "<brief-id> <1-5> [notes]  (no args: list pending check-ins)"
---

Close the loop on a purchase: was the recommendation actually good? This populates the calibration ledger (the same one `/calibrate` feeds) and the preference profile that makes future emptor runs smarter.

**No arguments?** Scan `data/purchases.jsonl` for `purchase` events ≥21 days old with no matching `check_in`, list them with days elapsed, and stop.

Otherwise parse `$ARGUMENTS`:
1. **brief_id** (required)
2. **satisfaction** (required) — 1-5
3. **notes** (optional) — what held up, what surprised

If malformed, show usage: `/purchase-review CRS-20260610-robvc4 4 "great pickup, louder than reviews said"`

Steps:

1. Find the matching `purchase` event in `data/purchases.jsonl` and the brief line in `data/decision-journal.jsonl`. Missing either → say which, suggest `/purchase-log` first; do not write.
2. Ask (briefly) if not inferable from notes: would you rebuy? did the must-haves hold? any surprises?
3. Append to `data/purchases.jsonl`:
   ```json
   {"event":"check_in","brief_id":"<id>","ts":"<iso8601>","days_since_purchase":32,"satisfaction":4,"would_rebuy":true,"must_haves_held":{"<must-have>":true},"surprises":["<text>"],"calibration_outcome_written":true,"notes":"<text>"}
   ```
4. Map satisfaction → calibration outcome: **≥4 → `true`, 3 → `partial`, ≤2 → `false`**. Append to `data/calibration.jsonl`:
   ```json
   {"brief_id":"<id>","claim_id":"top-pick","predicted_confidence":"<the brief's TOP PICK CONFIDENCE>","outcome":"<true|partial|false>","notes":"<satisfaction + key notes>","resolved_at":"<iso8601>"}
   ```
5. Update `data/consumer-preferences.json`: category weight priors (what mattered in hindsight), brands/merchants liked or avoided, satisficer lean, regret triggers from surprises. Set `updated_at`.
6. If the vault is reachable, append the 30-day verdict to the brief's vault decision note (`vault-writer`, `overwrite_policy: append`).
7. Confirm:
   ```
   Check-in recorded: <brief_id> = <satisfaction>/5 → calibration outcome <outcome>
   Predicted confidence was <tier>. Preferences updated.
   ```
8. If total resolved calibration entries crosses a multiple of 25, suggest `python3 scripts/calibration-report.py`.
