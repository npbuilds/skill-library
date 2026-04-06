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
_shared = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_shared)  # type: ignore[union-attr]

# Re-export what we need
REGISTRY_PATH = _shared.REGISTRY_PATH
USAGE_LOG = _shared.USAGE_LOG
FEEDBACK_LOG = _shared.FEEDBACK_LOG
PROJECT_ROOT = _shared.PROJECT_ROOT
load_log = _shared.load_log
atomic_write_registry = _shared.atomic_write_registry
score_structure = _shared.score_structure
score_depth = _shared.score_depth
score_connectivity = _shared.score_connectivity
score_freshness = _shared.score_freshness
score_usage = _shared.score_usage
score_feedback = _shared.score_feedback


def main():
    dry_run = "--dry-run" in sys.argv

    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    skills = reg.get("skills", {})

    # Load analytics
    usage_counts: Counter = Counter()
    for e in load_log(USAGE_LOG):
        usage_counts[e.get("skill", "")] += 1

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

        if not dry_run:
            entry["auto_score"] = composite
            entry["composite_score"] = composite

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

    if not dry_run and changes:
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
