---
name: calibrate
description: Resolve a previously-tagged research claim as true/false/partial — populates data/calibration.jsonl
argument-hint: "<brief-id> <claim-id> <true|false|partial> [notes]"
---

Resolve a Spelunker brief's claim against ground truth that emerged later. This is how the calibration ledger gets populated, which is how we learn whether confidence tags are well-calibrated.

Parse `$ARGUMENTS`:
1. **brief_id** (required) — e.g., `SPK-20260513-pasiv9` (emitted in Spelunker Phase 6 footer)
2. **claim_id** (required) — the numeric or labeled id of the claim within that brief (e.g., `1`, `2.3`, `key-finding-1`)
3. **outcome** (required) — one of `true | false | partial`
4. **notes** (optional) — free text explaining what evidence resolved the claim and when

If `$ARGUMENTS` is malformed, show usage:
```
/calibrate SPK-20260513-pasiv9 2 false  "Reuters retracted the underlying study on 2026-05-10"
```

Steps:

1. Resolve the current ISO-8601 UTC timestamp.
2. Validate `outcome` is one of `true | false | partial`. Reject otherwise.
3. Look up the brief if possible:
   - Search `research/`, `loom-briefings/`, and the user's vault index for the `brief_id`.
   - If found, extract the claim's original confidence tag (Confirmed / Likely / Speculative / Contested / Unverifiable). If not found, set `predicted_confidence: "unknown"` and continue.
4. Append a single JSON line to `data/calibration.jsonl` (create if absent):

   ```json
   {"brief_id": "<id>", "claim_id": "<cid>", "predicted_confidence": "<tier or unknown>", "outcome": "<true|false|partial>", "notes": "<text or empty>", "resolved_at": "<iso8601>"}
   ```

5. Confirm to the user:

   ```
   Calibrated: <brief_id> claim <claim_id> = <outcome>
   Predicted confidence: <tier or "unknown">
   Total resolved entries: <N>
   ```

6. If the total entry count crosses a multiple of 25, suggest running `python3 scripts/calibration-report.py` to see updated hit-rates per confidence tier.

**Why this matters:** Confidence tags are only meaningful if they're calibrated. If "Likely" claims turn out true 50% of the time but should hit ~70%, the confidence framework needs adjustment. Without a ledger, the framework is unfalsifiable scaffolding.
