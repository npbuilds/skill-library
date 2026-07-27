"""Shared utilities for the Skill Library MCP server and CLI."""

import fcntl
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

# Telemetry provenance. "mcp" = the MCP server's get_skill tool; "plugin" =
# Claude Code's native Skill tool / slash commands, captured by the
# PostToolUse hook (hooks/skill-invocation-telemetry.sh). Events written
# before the hook existed carry no `source` and are all MCP loads, so
# event_source() defaults them to "mcp" rather than "unknown".
SOURCE_MCP = "mcp"
SOURCE_PLUGIN = "plugin"


def record_feedback_entry(skill_name: str, rating: int, note: str = "") -> str:
    """Record feedback for a skill (standalone, no MCP server dependency)."""
    if not REGISTRY_PATH.exists():
        return f"Registry not found at {REGISTRY_PATH}"
    registry = json.loads(REGISTRY_PATH.read_text())
    if skill_name not in registry.get("skills", {}):
        return f"Skill '{skill_name}' not found in registry."
    if not 1 <= rating <= 5:
        return "Rating must be between 1 and 5."
    entry = {
        "skill": skill_name,
        "rating": rating,
        "note": note,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    FEEDBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(FEEDBACK_LOG, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.write(json.dumps(entry) + "\n")
            f.flush()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    return f"Recorded: {skill_name} rated {rating}/5{f' — {note}' if note else ''}."


def load_log(path: Path) -> list[dict]:
    """Load all events from a JSONL log file.

    Enforces the `list[dict]` return type rather than merely annotating it. A
    jsonl line like `"foo"`, `[1,2]`, `123` or `null` parses without error and
    is not a dict, and every consumer here treats rows as mappings — the raw
    `e.get(...)` in get_skill_stats' unattributed count, cli's _show_skill_stats,
    source_breakdown, and pull_telemetry's _fs_id dedupe all raise
    AttributeError on one. Guarding each call site is whack-a-mole; the parse
    boundary is the one place that covers them, so a malformed line degrades to
    a skipped row exactly like a JSONDecodeError already does.
    """
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
    return events


def iter_skill_uses(events):
    """Yield only skill-load events (those with a truthy string `skill` field).

    usage.jsonl mixes get_skill events ({skill, type, ...}) with search events
    ({type: "search", query, ...}). Analytics that count "how many times was
    skill X used" must skip search events; this helper makes the intent
    explicit and prevents the empty-string bucket from inflating max_usage.

    The `str` check is load-bearing, not paranoia. This is the ONE filter every
    usage consumer shares — recalibrate_scores.py's usage_counts,
    get_skill_stats, the CLI, and scripts/usage_rollup.py's dashboard totals —
    so anything it admits must be usable as a dict key by all of them. A row
    whose `skill` is a number or a list reaches Counter fine but then explodes
    in `sorted()` (mixed-type comparison) or as an unhashable key, and because
    the rollup is built inside sync_registry before the meta/registry commit
    marker, that exception silently aborts the WHOLE Firestore registry sync.
    Skipping such rows here keeps every consumer in agreement by construction,
    which is what makes "usage on the dashboard == usage behind auto_score"
    hold.

    The `isinstance(e, dict)` check is belt-and-braces: load_log already drops
    non-dict rows at the parse boundary, which is what protects the call sites
    that never come through here. Keeping it means this helper is also safe on
    a hand-built list.
    """
    return (
        e for e in events
        if isinstance(e, dict) and isinstance(e.get("skill"), str) and e["skill"]
    )


def event_source(event: dict) -> str:
    """Provenance of a telemetry event: SOURCE_MCP or SOURCE_PLUGIN.

    Pre-hook rows have no `source` field and were all written by the MCP
    server's get_skill, so a missing field reads as "mcp".
    """
    return event.get("source") or SOURCE_MCP


def source_breakdown(events) -> Counter:
    """Count events by provenance — how much usage is MCP vs plugin-native."""
    return Counter(event_source(e) for e in events)


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
        mod_date = datetime.fromisoformat(last_mod)
        if mod_date.tzinfo is None:
            mod_date = mod_date.replace(tzinfo=timezone.utc)
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


# The composite weights, in ONE place. Previously these numbers were written
# out three times — here, in recalibrate_scores.py's inline formula, and in the
# Infra Observatory's "Scoring Model" panel (app/infra.html) — guarded by
# nothing but a "update both together" comment. When usage went to 0% the HTML
# copy was missed and the live dashboard advertised a 10% Usage bar for an axis
# contributing nothing, which is exactly the failure mode a comment cannot
# prevent. recalibrate now imports this, and scripts/test_scoring_weights.py
# pins the HTML panel against it, so all three can no longer disagree.
#
# usage is 0.00 deliberately — see compute_auto_score for why it is retained as
# observability rather than deleted.
SCORE_WEIGHTS: dict[str, float] = {
    "structure": 0.22,
    "depth": 0.28,
    "connectivity": 0.22,
    "freshness": 0.17,
    "usage": 0.00,
    "feedback": 0.11,
}


def combine_scores(axes: dict) -> int:
    """Weight per-axis scores into a composite, using SCORE_WEIGHTS.

    Raises KeyError if an axis is missing, so adding a scoring axis cannot
    silently contribute zero: the caller must supply every weighted axis.
    """
    return round(sum(axes[k] * w for k, w in SCORE_WEIGHTS.items()))


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

    Weights: structure 22%, depth 28%, connectivity 22%,
             freshness 17%, feedback 11%.  Usage is 0% — see below.

    Usage is deliberately UNWEIGHTED, not removed. score_usage is still
    computed and still reported in recalibrate's breakdown (`U:` column) and on
    the dashboard, because the telemetry is genuinely useful as observability —
    it is how `biotech-venture` was caught sitting at 1 recorded load despite
    heavy daily use, which exposed commands that skipped their get_skill. What
    it is not is evidence of quality:

      - 397 of 528 skills (75%) had zero recorded usage, across 21 active days
        in 4 months. For those, the axis contributed a flat 0 on a 10% weight,
        so it functioned as a uniform penalty for not having happened to be
        loaded — which tracks how recently a skill was built, not how good it
        is.
      - The 10% weight put a scoring dependency on a mutable append-only log
        written by three producers. Most of the sharp edges in this pipeline
        exist only because of that coupling: the max_usage denominator (one
        inflated skill deflates every other), the per-session cap, the
        skill_raw quarantine for unresolved plugin names, and the requirement
        that every telemetry commit carry a matching recalibration.

    The remaining 10% is redistributed proportionally across the other five
    axes (each × 100/90, rounded to sum to exactly 100), so the model's shape
    is unchanged apart from usage's removal — this is deliberately the least
    opinionated redistribution available.

    `usage_counts` and `max_usage` are retained in the signature even though
    they no longer affect the result: callers pass them positionally
    (server.py:1685 passes `Counter(), 0`, and recalibrate passes real
    counts), and keeping them means re-weighting usage later is a one-line
    change rather than an API break.

    Pass `now` explicitly when scoring many skills in a loop so all skills
    get the same reference timestamp (consistent freshness scores).
    If omitted, uses the current UTC time.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    metrics = entry.get("metrics", {})
    name = entry.get("name", "")
    return combine_scores({
        "structure": score_structure(metrics),
        "depth": score_depth(metrics),
        "connectivity": score_connectivity(entry),
        "freshness": score_freshness(entry, now),
        "usage": score_usage(name, usage_counts, max_usage),
        "feedback": score_feedback(name, feedback_ratings),
    })


# ---------------------------------------------------------------------------
# Impact analysis
# ---------------------------------------------------------------------------


def _get_domain(entry: dict) -> str:
    """Extract the domain tag from a skill entry, or '?' if missing."""
    for tag in entry.get("tags", []):
        if tag.startswith("domain:"):
            return tag.split(":", 1)[1]
    return "?"


def blast_radius(
    skills: dict,
    skill_name: str,
    direction: str = "upstream",
    max_depth: int = 3,
) -> dict:
    """Trace the blast radius of changing a skill in the dependency graph.

    Args:
        skills:     The ``registry["skills"]`` dict.
        skill_name: Starting skill.
        direction:  ``"upstream"`` follows *referenced_by* (who depends on me),
                    ``"downstream"`` follows *depends_on* (what do I depend on).
        max_depth:  Maximum BFS depth (1-5, clamped).

    Returns a dict::

        {
            "risk": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
            "total_affected": int,
            "domains_hit": int,
            "tiers": {
                1: [{"skill": str, "via": str, "domain": str}, ...],
                2: [...],
                ...
            },
        }
    """
    max_depth = max(1, min(5, max_depth))
    edge_key = "referenced_by" if direction == "upstream" else "depends_on"

    tiers: dict[int, list[dict]] = {}
    visited: set[str] = {skill_name}
    frontier: set[str] = {skill_name}

    for depth in range(1, max_depth + 1):
        next_frontier: set[str] = set()
        for s in frontier:
            s_entry = skills.get(s)
            if not s_entry:
                continue
            for neighbor in s_entry.get(edge_key, []):
                if neighbor not in visited and neighbor in skills:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)
                    tiers.setdefault(depth, []).append({
                        "skill": neighbor,
                        "via": s,
                        "domain": _get_domain(skills[neighbor]),
                    })
        frontier = next_frontier
        if not frontier:
            break

    total = sum(len(v) for v in tiers.values())
    all_domains = {e["domain"] for tier in tiers.values() for e in tier}
    domains_hit = len(all_domains - {"?"})

    if total >= 10 and domains_hit >= 3:
        risk = "CRITICAL"
    elif total >= 10:
        risk = "HIGH"
    elif total >= 4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "risk": risk,
        "total_affected": total,
        "domains_hit": domains_hit,
        "tiers": tiers,
    }
