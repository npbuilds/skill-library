#!/usr/bin/env python3
"""Recompute composite scores with a multi-factor model.

Usage:
    python3 scripts/recalibrate_scores.py [--dry-run]

Factors (each 0-100, weighted):
  Structure (20%):    section count, frontmatter completeness, description quality
  Depth (25%):        word count sweet spot (300-5000), reference file coverage
  Connectivity (20%): depends_on + referenced_by links (more = higher)
  Freshness (15%):    days since last_modified (decays over 90 days)
  Usage (10%):        load count from usage.jsonl
  Feedback (10%):     average rating from feedback.jsonl
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


# ── Health classification (aggressive profile) ──────────────────────────────
# health_status was historically only ever set to "healthy" at creation and
# flipped to "warning" when a skill was hand-edited or deprecated — so nothing
# ever surfaced silent degradation. These thresholds let recalibration derive
# health from the same signals it already computes. "Aggressive" is intentional:
# it favours surfacing borderline skills over false reassurance.
HEALTH_CRITICAL_SCORE = 50   # composite below this → critical
HEALTH_WARNING_SCORE = 70    # composite below this → warning
HEALTH_STALE_DAYS = 60       # last_modified older than this → warning


def _parse_dt(value: str | None):
    """Parse an ISO-8601 or YYYY-MM-DD timestamp into an aware datetime."""
    if not value:
        return None
    dt = None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None
    # Normalise to UTC-aware so arithmetic against an aware `now` is safe.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def classify_health(name, entry, composite, skills, usage_counts, now) -> str:
    """Derive health_status from score, structural integrity, usage, and freshness.

    Order matters: critical conditions are checked before warning conditions.
    Deprecated skills retain "warning" (their lifecycle marker) regardless.
    """
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

    # ── Warning: weak score, never exercised, or gone stale ──
    if composite < HEALTH_WARNING_SCORE:
        return "warning"
    if usage_counts.get(name, 0) == 0:
        return "warning"  # never loaded — no evidence it earns its place
    lm = _parse_dt(entry.get("last_modified"))
    if lm is not None and (now - lm).days > HEALTH_STALE_DAYS:
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

        # Individual scores kept for the breakdown output.
        # Weights here must match shared.compute_auto_score — update both together.
        s_struct = score_structure(metrics)
        s_depth = score_depth(metrics)
        s_conn = score_connectivity(entry)
        s_fresh = score_freshness(entry, now)
        s_usage = score_usage(name, usage_counts, max_usage)
        s_fb = score_feedback(name, feedback_ratings)

        composite = round(
            s_struct * 0.20
            + s_depth * 0.25
            + s_conn * 0.20
            + s_fresh * 0.15
            + s_usage * 0.10
            + s_fb * 0.10
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
        new_health = classify_health(name, entry, composite, skills, usage_counts, now)
        old_health = entry.get("health_status", "healthy")
        health_dist[new_health] += 1
        if new_health != old_health:
            health_changes.append((name, old_health, new_health))

        if not dry_run:
            entry["auto_score"] = composite
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

        # Append evolution snapshot after successful recalibration
        import subprocess
        snapshot_script = Path(__file__).resolve().parent / "snapshot_evolution.py"
        if snapshot_script.exists():
            subprocess.run(
                [sys.executable, str(snapshot_script), "--event=recalibrate"],
                capture_output=True,
            )
    elif dry_run:
        print("\n(dry run — no changes written)")


if __name__ == "__main__":
    main()
