#!/usr/bin/env python3
"""Generate a health report from registry.json (sentinel lite).

Reads data/registry.json and writes a structured JSON report to
data/health/YYYY-MM-DD.json covering:
  - Skills by health status (healthy/warning/critical)
  - Low-score skills (composite_score < 50)
  - Stale skills (last_modified > 90 days ago)
  - Orphaned skills (no connections, not an orchestrator/director)
  - Domain coverage summary

This is a lightweight stand-in for the full Sentinel Prime skill
invocation (which requires Agent SDK + API key, Layer 4 territory).

Usage:
    python3 scripts/health-report.py

Exits 0 on success. Prints summary to stdout.
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

_here = Path(__file__).resolve().parent
PROJECT_ROOT = _here.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"
HEALTH_DIR = PROJECT_ROOT / "data" / "health"

# Thresholds (tunable)
LOW_SCORE_THRESHOLD = 50
STALE_DAYS = 90
MAX_LIST_ITEMS = 20  # cap list lengths in the report


def build_report(reg: dict, now: datetime) -> dict:
    """Pure function: registry + timestamp → health report dict."""
    skills = reg.get("skills", {})
    stale_cutoff = now - timedelta(days=STALE_DAYS)

    active = {n: s for n, s in skills.items() if s.get("status") != "deprecated"}
    deprecated_count = len(skills) - len(active)

    # --- Health breakdown ---
    health_counts: dict[str, int] = {}
    for s in active.values():
        h = s.get("health_status", "unknown")
        health_counts[h] = health_counts.get(h, 0) + 1

    # --- Low scores ---
    low_score = sorted(
        [
            {"name": n, "score": s.get("composite_score", 0)}
            for n, s in active.items()
            if s.get("composite_score", 0) < LOW_SCORE_THRESHOLD
        ],
        key=lambda x: x["score"],
    )

    # --- Stale skills (last_modified > threshold) ---
    stale = []
    for n, s in active.items():
        lm = s.get("last_modified", "")
        if not lm:
            continue
        try:
            mod_dt = datetime.fromisoformat(lm)
            if mod_dt.tzinfo is None:
                mod_dt = mod_dt.replace(tzinfo=timezone.utc)
            if mod_dt < stale_cutoff:
                stale.append({"name": n, "last_modified": lm, "days_ago": (now - mod_dt).days})
        except (ValueError, TypeError):
            pass
    stale.sort(key=lambda x: -x["days_ago"])

    # --- Orphaned skills (no deps, no referenced_by, not a hub type) ---
    # Observers (like Sentinel Prime) are standalone by design — not orphans.
    hub_types = {"orchestrator", "director", "observer"}
    orphans = sorted(
        n for n, s in active.items()
        if not s.get("depends_on") and not s.get("referenced_by")
        and s.get("type") not in hub_types
    )

    # --- Domain summary ---
    domains: dict[str, dict] = {}
    for n, s in active.items():
        loc = s.get("location", "")
        parts = loc.split("/")
        domain = parts[1] if len(parts) >= 3 else "unknown"
        if domain not in domains:
            domains[domain] = {"count": 0, "scores": []}
        domains[domain]["count"] += 1
        domains[domain]["scores"].append(s.get("composite_score", 0))

    domain_summary = {}
    for d, info in sorted(domains.items()):
        scores = info["scores"]
        domain_summary[d] = {
            "count": info["count"],
            "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
        }

    # --- Build report ---
    return {
        "timestamp": now.isoformat(),
        "total_active": len(active),
        "total_deprecated": deprecated_count,
        "health_breakdown": health_counts,
        "low_score_count": len(low_score),
        "low_score_skills": low_score[:MAX_LIST_ITEMS],
        "stale_count": len(stale),
        "stale_skills": stale[:MAX_LIST_ITEMS],
        "orphan_count": len(orphans),
        "orphans": orphans[:MAX_LIST_ITEMS],
        "domain_summary": domain_summary,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Generate a registry health report")
    parser.add_argument("--firestore", action="store_true",
                        help="Write to the Firestore 'health_reports' collection instead "
                             "of a local dated file (no git commit — used by CI).")
    parser.add_argument("--project", default="skill-library-prod", help="GCP project ID")
    args = parser.parse_args()

    if not REGISTRY_PATH.exists():
        print(f"ERROR: {REGISTRY_PATH} not found", file=sys.stderr)
        sys.exit(1)

    reg = json.loads(REGISTRY_PATH.read_text())
    now = datetime.now(timezone.utc)
    report = build_report(reg, now)
    date_str = now.strftime("%Y-%m-%d")

    if args.firestore:
        # Persist to Firestore (doc id = date), keeping health reports out of git.
        from migrate_to_firestore import get_db
        db = get_db(args.project)
        db.collection("health_reports").document(date_str).set(report)
        dest = f"Firestore health_reports/{date_str}"
    else:
        # Local dated file (gitignored) — for ad-hoc local runs.
        HEALTH_DIR.mkdir(parents=True, exist_ok=True)
        output_path = HEALTH_DIR / f"{date_str}.json"
        output_path.write_text(json.dumps(report, indent=2) + "\n")
        dest = str(output_path.relative_to(PROJECT_ROOT))

    # --- Print summary to stdout ---
    print(f"Health report: {report['total_active']} active, {report['total_deprecated']} deprecated")
    print(f"  Health: {report['health_breakdown']}")
    print(f"  Low score (<{LOW_SCORE_THRESHOLD}): {report['low_score_count']}")
    print(f"  Stale (>{STALE_DAYS}d): {report['stale_count']}")
    print(f"  Orphans: {report['orphan_count']}")
    print(f"  Domains: {len(report['domain_summary'])}")
    print(f"  Written to: {dest}")


if __name__ == "__main__":
    main()
