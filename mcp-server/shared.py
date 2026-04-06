"""Shared utilities for the Skill Library MCP server and CLI."""

import json
import os
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REGISTRY_PATH = DATA_DIR / "registry.json"
USAGE_LOG = DATA_DIR / "usage.jsonl"
GAPS_LOG = DATA_DIR / "gaps.jsonl"
FEEDBACK_LOG = DATA_DIR / "feedback.jsonl"
SKILLS_DIR = PROJECT_ROOT / "skills"


def load_log(path: Path) -> list[dict]:
    """Load all events from a JSONL log file."""
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


def atomic_write_registry(registry: dict) -> None:
    """Write registry.json atomically via temp-file rename.

    Raises OSError on failure so callers can catch and return a user-facing
    error string.  The registry is never left in a partial state.
    """
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=REGISTRY_PATH.parent, suffix=".tmp", delete=False
        ) as tmp:
            json.dump(registry, tmp, indent=2)
            tmp.write("\n")
            tmp_path = tmp.name
        os.replace(tmp_path, REGISTRY_PATH)
    except OSError:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
        raise


# ---------------------------------------------------------------------------
# Scoring functions (used by both the MCP server and recalibrate_scores.py)
# ---------------------------------------------------------------------------


def score_structure(metrics: dict) -> int:
    """Section count (density-adjusted) + description quality.

    Rich knowledge docs legitimately have many sections.  We normalise by
    document length so a 4 000-word skill with 40 sections is treated the
    same as a 500-word skill with 5 sections (both ≈ 10 sections/1 000w).
    """
    section_count = metrics.get("section_count", 0)
    desc_words = metrics.get("description_words", 0)
    body_words = metrics.get("body_words", metrics.get("word_count", 0))

    score = 50  # base

    # Density-adjusted section score
    length_factor = max(1.0, body_words / 500)
    adj_sc = section_count / length_factor
    if 1.0 <= adj_sc <= 5.0:
        score += 25
    elif 0.5 <= adj_sc <= 10.0:
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
    """Word count sweet spot + reference coverage.

    Sweet spot is 300-5000 words.  Decay only kicks in above 5000 words.
    """
    body_words = metrics.get("body_words", metrics.get("word_count", 0))
    ref_files = metrics.get("reference_files", 0)

    if 300 <= body_words <= 5000:
        score = 75
    elif body_words < 300:
        score = max(10, int(body_words / 300 * 75))
    else:
        score = max(40, 75 - int((body_words - 5000) / 500))

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


def score_feedback(name: str, feedback_ratings: dict) -> int:
    """Average rating mapped to 0-100."""
    ratings = feedback_ratings.get(name, [])
    if ratings:
        avg = sum(ratings) / len(ratings)
        return int(avg * 20)  # 1-5 -> 20-100
    return 50  # neutral when no feedback


def compute_auto_score(
    entry: dict,
    usage_counts: Counter,
    max_usage: int,
    feedback_ratings: dict,
    now: Optional[datetime] = None,
) -> int:
    """Compute the weighted composite auto_score for a registry entry.

    Weights: structure 20%, depth 25%, connectivity 20%,
             freshness 15%, usage 10%, feedback 10%.

    Pass `now` explicitly when scoring many skills in a loop so all skills
    get the same reference timestamp (consistent freshness scores).
    If omitted, uses the current UTC time.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    metrics = entry.get("metrics", {})
    name = entry.get("name", "")
    return round(
        score_structure(metrics) * 0.20
        + score_depth(metrics) * 0.25
        + score_connectivity(entry) * 0.20
        + score_freshness(entry, now) * 0.15
        + score_usage(name, usage_counts, max_usage) * 0.10
        + score_feedback(name, feedback_ratings) * 0.10
    )
