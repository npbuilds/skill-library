#!/usr/bin/env python3
"""Recompute composite scores with a multi-factor model.

Usage:
    python3 scripts/recalibrate_scores.py [--dry-run]

Factors (each 0-100, weighted):
  Structure (20%):    section count, frontmatter completeness, description quality
  Depth (25%):        word count sweet spot (500-2000), reference file coverage
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
USAGE_LOG = PROJECT_ROOT / "data" / "usage.jsonl"
FEEDBACK_LOG = PROJECT_ROOT / "data" / "feedback.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def score_structure(metrics: dict) -> int:
    """Section count + description quality."""
    section_count = metrics.get("section_count", 0)
    desc_words = metrics.get("description_words", 0)

    score = 50  # base
    # Section count: ideal 3-6
    if 3 <= section_count <= 6:
        score += 25
    elif 2 <= section_count <= 8:
        score += 15

    # Description: ideal 20-60 words
    if 20 <= desc_words <= 60:
        score += 25
    elif 15 <= desc_words <= 100:
        score += 15
    else:
        score += 5

    return score


def score_depth(metrics: dict) -> int:
    """Word count sweet spot + reference coverage."""
    body_words = metrics.get("body_words", metrics.get("word_count", 0))
    ref_files = metrics.get("reference_files", 0)

    if 500 <= body_words <= 2000:
        score = 70
    elif 300 <= body_words < 500:
        score = 50
    elif 2000 < body_words <= 3000:
        # Linear decay from 70 at 2000 to 50 at 3000
        score = 70 - int((body_words - 2000) / 1000 * 20)
    elif body_words < 300:
        score = max(10, int(body_words / 300 * 50))
    else:
        # >3000: continue decay from 50
        score = max(20, 50 - int((body_words - 3000) / 200))

    # Reference bonus
    score += min(30, ref_files * 10)
    return min(100, score)


def score_connectivity(entry: dict) -> int:
    """Number of dependency + referenced_by links."""
    deps = len(entry.get("depends_on", []))
    refs = len(entry.get("referenced_by", []))
    total = deps + refs

    if total == 0:
        return 20
    elif total <= 2:
        return 40
    elif total <= 5:
        return 65
    elif total <= 10:
        return 85
    else:
        return 100


def score_freshness(entry: dict, now: datetime) -> int:
    """Days since last_modified, with decay."""
    last_mod = entry.get("last_modified", "2020-01-01")
    try:
        mod_date = datetime.fromisoformat(last_mod).replace(tzinfo=timezone.utc)
        days_old = (now - mod_date).days
    except (ValueError, TypeError):
        days_old = 90

    if days_old <= 7:
        return 100
    elif days_old <= 30:
        return 80
    elif days_old <= 60:
        return 60
    elif days_old <= 90:
        return 40
    else:
        return max(20, 40 - int((days_old - 90) / 30) * 5)


def score_usage(name: str, usage_counts: Counter, max_usage: int) -> int:
    """Relative usage frequency."""
    uses = usage_counts.get(name, 0)
    if max_usage > 0 and uses > 0:
        return min(100, int((uses / max_usage) * 80) + 20)
    return 0


def score_feedback(name: str, feedback_ratings: dict[str, list[int]]) -> int:
    """Average rating mapped to 0-100."""
    ratings = feedback_ratings.get(name, [])
    if ratings:
        avg = sum(ratings) / len(ratings)
        return int(avg * 20)  # 1-5 -> 20-100
    return 50  # neutral when no feedback


def main():
    dry_run = "--dry-run" in sys.argv

    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    skills = reg.get("skills", {})

    # Load analytics
    usage_counts: Counter = Counter()
    for e in load_jsonl(USAGE_LOG):
        usage_counts[e.get("skill", "")] += 1

    feedback_ratings: dict[str, list[int]] = {}
    for e in load_jsonl(FEEDBACK_LOG):
        s = e.get("skill", "")
        r = e.get("rating")
        if s and r is not None:
            feedback_ratings.setdefault(s, []).append(r)

    now = datetime.now(timezone.utc)
    max_usage = max(usage_counts.values()) if usage_counts else 1

    changes = []

    for name, entry in skills.items():
        metrics = entry.get("metrics", {})

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
        with open(REGISTRY_PATH, "w") as f:
            json.dump(reg, f, indent=2)
            f.write("\n")
        print(f"\nRegistry updated.")
    elif dry_run:
        print("\n(dry run — no changes written)")


if __name__ == "__main__":
    main()
