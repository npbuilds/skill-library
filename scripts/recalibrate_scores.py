#!/usr/bin/env python3
"""Recompute composite scores with a multi-factor model.

Usage:
    python3 scripts/recalibrate_scores.py [--dry-run]

Factors (each 0-100, weighted):
  Structure (22%):    section count, frontmatter completeness, description quality
  Depth (28%):        word count sweet spot (300-5000), reference file coverage
  Connectivity (22%): depends_on + referenced_by links (more = higher)
  Freshness (17%):    days since last_modified (decays over 90 days)
  Feedback (11%):     average rating from feedback.jsonl
  Usage (0%):         load count from usage.jsonl — computed and reported in the
                      U: breakdown column, but UNWEIGHTED. 75% of skills had
                      zero recorded usage over 21 active days, so the axis was a
                      flat penalty for not having happened to be loaded rather
                      than a quality signal. See shared.compute_auto_score.
"""

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# Allow running from the project root or from the scripts/ directory
_here = Path(__file__).resolve().parent
import importlib.util

_shared_path = _here.parent / "mcp-server" / "shared.py"
_spec = importlib.util.spec_from_file_location("shared", _shared_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot locate shared module at {_shared_path}")
_shared = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_shared)

# Re-export what we need
REGISTRY_PATH = _shared.REGISTRY_PATH
USAGE_LOG = _shared.USAGE_LOG
FEEDBACK_LOG = _shared.FEEDBACK_LOG
PROJECT_ROOT = _shared.PROJECT_ROOT
load_log = _shared.load_log
iter_skill_uses = _shared.iter_skill_uses
atomic_write_registry = _shared.atomic_write_registry
score_structure = _shared.score_structure
score_depth = _shared.score_depth
score_connectivity = _shared.score_connectivity
score_freshness = _shared.score_freshness
score_usage = _shared.score_usage
score_feedback = _shared.score_feedback
SCORE_WEIGHTS = _shared.SCORE_WEIGHTS
combine_scores = _shared.combine_scores
compute_composite_score = _shared.compute_composite_score


# ── Health classification ───────────────────────────────────────────────────
# health_status was historically only ever set to "healthy" at creation and
# flipped to "warning" when a skill was hand-edited or deprecated — so nothing
# ever surfaced silent degradation. These thresholds let recalibration derive
# health from the same signals it already computes.
#
# The profile used to be "aggressive", favouring over-surfacing. Measured on the
# real library that produced 469 warnings out of 528 (89%), which is not a
# maintenance queue — it is noise with no discrimination left in it. The causes,
# decomposed:
#
#   warning from low score only :   2
#   warning from staleness only : 246
#   warning from both           : 221
#   healthy                     :  59
#
# So the score threshold was almost inert (moving it 70 -> 60 changed 2 skills)
# and an absolute staleness veto was doing all the work. That veto is removed —
# see classify_health — because freshness is ALREADY 17% of the composite, so
# age was counted twice: once proportionately in the score, once as a binary
# gate. It was also structurally doomed on a write-once knowledge library: every
# skill eventually crosses any fixed age, so the signal trends to "everything is
# unhealthy". At 60 days it was there already, four months in.
#
# Removing the veto does not lose the staleness signal, it routes it through the
# score, where score_freshness decays to 20 at ~270 days — a ~13.6 point drag at
# 17% weight, enough to push a weak skill under the warning bar on its own.
#
# With age no longer vetoing, the score threshold becomes the real knob, so it
# is set where it discriminates: 65 flags the weakest ~quartile (p25 of the
# current distribution is 65; min 58, median 71.5, max 90) — an actionable
# queue of 127 rather than 469. It is an absolute bar, not a percentile, so
# improving a skill's score genuinely clears it.
HEALTH_CRITICAL_SCORE = 50   # composite below this → critical
HEALTH_WARNING_SCORE = 65    # composite below this → warning


def classify_health(entry, composite, skills) -> str:
    """Derive health_status from structural integrity and composite score.

    Order matters: a manual override wins outright; then critical conditions are
    checked before warning conditions. Deprecated skills retain "warning" (their
    lifecycle marker) unless a manual override says otherwise.

    Usage is deliberately NOT a factor, which is why this no longer takes
    usage_counts. It used to return "warning" for any skill with zero recorded
    usage ("never loaded — no evidence it earns its place"), but that cannot
    coexist with usage being unweighted in compute_auto_score: the same signal
    would be non-diagnostic for scoring and authoritative for health. Since 75%
    of skills had zero recorded usage over 21 active days, the rule was mostly
    reporting which skills happened not to be loaded in a narrow window — it
    held 215 skills at "warning" that cleared the score threshold on every
    other axis. If an "unexercised" signal is wanted, it belongs in its own
    field rather than competing with composite_score.

    Staleness is likewise not a factor, which is why this no longer takes
    `now` and is a pure function of the entry plus the skill graph — health
    is fully reproducible from the registry, with no dependence on when it
    is evaluated. `name` is gone for the same reason usage_counts is.
    Health means: structurally sound and scoring adequately.
    """
    # A manual override (set via update_skill_metadata) is authoritative — the
    # auto-classifier must never silently undo a human decision. Cleared by
    # setting health_status="auto", which nulls manual_health.
    manual = entry.get("manual_health")
    if manual:
        return manual

    if entry.get("status") == "deprecated":
        return "warning"

    # ── Critical: structural breakage or a failing score ──
    parent = entry.get("parent")
    if parent and parent not in skills:
        return "critical"  # dangling parent
    if any(dep not in skills for dep in entry.get("depends_on", [])):
        return "critical"  # broken dependency edge
    if composite < HEALTH_CRITICAL_SCORE:
        return "critical"

    # ── Warning: weak score ──
    # No staleness veto: freshness is already 17% of the composite, so age is
    # accounted for proportionately in `composite` rather than as a second,
    # binary gate. See the HEALTH_* constants for the measurements behind this.
    if composite < HEALTH_WARNING_SCORE:
        return "warning"

    return "healthy"


def main():
    dry_run = "--dry-run" in sys.argv

    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    skills = reg.get("skills", {})

    # Load analytics — skill loads only; search events are excluded
    usage_counts: Counter = Counter(e["skill"] for e in iter_skill_uses(load_log(USAGE_LOG)))

    feedback_ratings: dict[str, list[int]] = {}
    for e in load_log(FEEDBACK_LOG):
        s = e.get("skill", "")
        r = e.get("rating")
        if s and r is not None:
            feedback_ratings.setdefault(s, []).append(r)

    # Compute once before the loop for consistent freshness across all skills
    now = datetime.now(timezone.utc)
    max_usage = max(usage_counts.values()) if usage_counts else 1

    changes = []
    health_changes = []  # (name, old_health, new_health)
    health_dist: Counter = Counter()

    for name, entry in skills.items():
        metrics = entry.get("metrics", {})

        # Individual scores kept for the breakdown output. The weights are NOT
        # repeated here — combine_scores applies shared.SCORE_WEIGHTS, so this
        # can no longer drift from compute_auto_score. s_usage is still computed
        # and still printed in the U: column, but carries weight 0; see
        # compute_auto_score's docstring for why usage is observability rather
        # than a quality signal.
        s_struct = score_structure(metrics)
        s_depth = score_depth(metrics)
        s_conn = score_connectivity(entry)
        s_fresh = score_freshness(entry, now)
        s_usage = score_usage(name, usage_counts, max_usage)
        s_fb = score_feedback(name, feedback_ratings)

        auto_score = combine_scores({
            "structure": s_struct,
            "depth": s_depth,
            "connectivity": s_conn,
            "freshness": s_fresh,
            "usage": s_usage,
            "feedback": s_fb,
        })
        composite = compute_composite_score(
            auto_score, entry.get("manual_rating")
        )

        old_score = entry.get("composite_score", 0)

        if old_score != composite:
            changes.append({
                "name": name,
                "old": old_score,
                "new": composite,
                "breakdown": {
                    "structure": s_struct,
                    "depth": s_depth,
                    "connectivity": s_conn,
                    "freshness": s_fresh,
                    "usage": s_usage,
                    "feedback": s_fb,
                },
            })

        # Health is derived from the freshly-computed composite so the two
        # never disagree. Manual quality (manual_rating) still feeds composite
        # upstream; health classification is purely automatic.
        new_health = classify_health(entry, composite, skills)
        old_health = entry.get("health_status", "healthy")
        health_dist[new_health] += 1
        if new_health != old_health:
            health_changes.append((name, old_health, new_health))

        if not dry_run:
            entry["auto_score"] = auto_score
            entry["composite_score"] = composite
            entry["health_status"] = new_health

    # Summary
    if changes:
        new_scores = [c["new"] for c in changes]
        old_scores = [c["old"] for c in changes]
        print(f"Recalibrated {len(changes)} skills")
        print(f"  Old range: {min(old_scores)}-{max(old_scores)}, avg {sum(old_scores)/len(old_scores):.1f}")
        print(f"  New range: {min(new_scores)}-{max(new_scores)}, avg {sum(new_scores)/len(new_scores):.1f}")
        print()

        changes.sort(key=lambda c: abs(c["new"] - c["old"]), reverse=True)
        print("Biggest changes:")
        for c in changes[:15]:
            delta = c["new"] - c["old"]
            sign = "+" if delta > 0 else ""
            b = c["breakdown"]
            print(
                f"  {c['name']}: {c['old']} -> {c['new']} ({sign}{delta})"
                f"  [S:{b['structure']} D:{b['depth']} C:{b['connectivity']}"
                f" F:{b['freshness']} U:{b['usage']} Fb:{b['feedback']}]"
            )
    else:
        print("No score changes needed.")

    # Health summary
    print()
    print("Health distribution: " + ", ".join(
        f"{k} {health_dist.get(k, 0)}" for k in ("healthy", "warning", "critical")
    ))
    if health_changes:
        flips = Counter((old, new) for _, old, new in health_changes)
        print(f"Health reclassified {len(health_changes)} skills:")
        for (old, new), n in sorted(flips.items(), key=lambda x: -x[1]):
            print(f"  {old} -> {new}: {n}")
    else:
        print("No health changes.")

    if not dry_run and (changes or health_changes):
        try:
            atomic_write_registry(reg)
        except OSError as e:
            print(f"\nError writing registry: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"\nRegistry updated.")

        # Evolution snapshots are no longer appended here. They persist to
        # Firestore via the "Daily maintenance (Firestore)" GitHub Action
        # (scripts/snapshot_to_firestore.py). data/evolution.jsonl is gitignored,
        # so appending during recalibration would be discarded dead work and
        # would silently drop the snapshot instead of persisting it.
    elif dry_run:
        print("\n(dry run — no changes written)")


if __name__ == "__main__":
    main()
