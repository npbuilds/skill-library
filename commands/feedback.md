---
name: feedback
description: Log feedback on a skill (1-5 score + optional notes) to data/feedback.jsonl
argument-hint: "<skill-name> <1-5> [optional notes] [brief-id:<SPK-...>]"
---

Log structured feedback for a skill invocation.

Parse `$ARGUMENTS` for:
1. **Skill name** (required) — first token
2. **Rating** (required) — integer 1-5
3. **Notes** (optional) — remaining free text up to the optional `brief-id:` token
4. **Brief ID** (optional) — token of the form `brief-id:SPK-YYYYMMDD-<slug>`. Spelunker emits this in its Phase 6 footer; other skills may emit similar IDs.

If `$ARGUMENTS` is empty or malformed, list the most recently used skills (from `data/usage.jsonl` tail, filtering for entries that have a `skill` field — search events lack one) and ask the user which one they want to rate.

Steps:

1. Resolve the current ISO-8601 UTC timestamp (`date -u +"%Y-%m-%dT%H:%M:%SZ"`).
2. Validate the rating is an integer in [1, 5]. Reject and show the rating scale otherwise.
3. Append a single JSON line to `data/feedback.jsonl` (create the file if it doesn't exist) with this exact shape:

   ```json
   {"skill": "<name>", "score": <int>, "notes": "<text or empty>", "brief_id": "<SPK-... or null>", "timestamp": "<iso8601>"}
   ```

4. Confirm to the user:

   ```
   Logged feedback: <skill> = <score>/5
   Brief: <brief_id or "—">
   Notes: <notes or "—">
   Total feedback entries for this skill: <N>  (count via `grep -c '"skill": "<skill>"' data/feedback.jsonl`)
   ```

5. If this is the first entry for the skill (count was 0 before this insertion), suggest re-running `python3 scripts/recalibrate_scores.py` so the registry's `feedback` subscore picks up the new data.

Rating scale (same as `/skill-rate`):
- 5: Essential, use frequently, works perfectly
- 4: Very useful, reliable
- 3: Useful but has issues
- 2: Rarely useful
- 1: Unused or broken

**Difference from `/skill-rate`:** `/skill-rate` updates the registry's persistent `manual_rating` field (one rating per skill, replaces previous). `/feedback` is an append-only log of every individual feedback event (multiple ratings allowed per skill, with brief-level granularity for orchestrator skills like spelunker).
