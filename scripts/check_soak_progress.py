#!/usr/bin/env python3
"""
check_soak_progress.py — Eyeball session-tagged telemetry quality during
the 30-day soak window before PR #2 (derive_coactivation) can be written.

Reads data/usage.jsonl and reports:
  - Total events split by type (skill loads vs. searches)
  - Session count + events-per-session distribution (median, p90)
  - Search-to-get chain rate (skill loads preceded by a search within
    10 min in the same session — the load-bearing signal for coactivation)
  - Top 10 co-retrieved skill pairs within sessions (preview of what
    derive_coactivation will surface)

Run: python3 scripts/check_soak_progress.py [--days 7]
"""

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
USAGE_LOG = ROOT / "data" / "usage.jsonl"


def _parse_iso(s: str):
    try:
        ts = datetime.fromisoformat(s)
        return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def load_events(window_days: int) -> list[dict]:
    if not USAGE_LOG.exists():
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    events = []
    for line in USAGE_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = _parse_iso(e.get("timestamp", ""))
        if ts is None or ts < cutoff:
            continue
        e["_ts"] = ts
        events.append(e)
    return events


def report(events: list[dict], window_days: int) -> None:
    if not events:
        print(f"No events in the last {window_days} days. Has the MCP server run?")
        return

    skill_events = [e for e in events if e.get("skill")]
    search_events = [e for e in events if e.get("type") == "search"]
    pre_pr1_events = [e for e in events if "session_id" not in e]

    sessions: dict[str, list[dict]] = defaultdict(list)
    for e in events:
        sessions[e.get("session_id", "<pre-PR-#1>")].append(e)

    eps = sorted(len(v) for v in sessions.values())
    med = median(eps) if eps else 0
    p90 = eps[int(len(eps) * 0.9)] if eps else 0

    # Co-retrieved skill pairs within session (unordered, unique pairs only)
    pair_counts: Counter = Counter()
    for evs in sessions.values():
        skills = [e["skill"] for e in evs if e.get("skill")]
        for i in range(len(skills)):
            for j in range(i + 1, len(skills)):
                a, b = sorted((skills[i], skills[j]))
                if a != b:
                    pair_counts[(a, b)] += 1

    # Chain rate: skill loads with a search in the same session within 10 min prior
    chains = 0
    for evs in sessions.values():
        ordered = sorted(evs, key=lambda x: x["_ts"])
        for i, e in enumerate(ordered):
            if not e.get("skill"):
                continue
            for j in range(i - 1, -1, -1):
                if (e["_ts"] - ordered[j]["_ts"]).total_seconds() > 600:
                    break
                if ordered[j].get("type") == "search":
                    chains += 1
                    break
    chain_rate = chains / len(skill_events) if skill_events else 0

    print(f"=== Soak progress (last {window_days} days) ===")
    print(f"  Events:     {len(events):>5}  ({len(skill_events)} skill loads, {len(search_events)} searches)")
    print(f"  Sessions:   {len(sessions):>5}  (events/session: median {med}, p90 {p90})")
    print(f"  Chain rate: {chain_rate:>5.0%}  (skill loads preceded by a search within 10 min, same session)")
    if pre_pr1_events:
        print(f"  Note:       {len(pre_pr1_events)} events predate PR #1 (no session_id)")
    print()
    print("  Top co-retrieved pairs (within session):")
    if pair_counts:
        for (a, b), count in pair_counts.most_common(10):
            print(f"    {count:>3}  {a}  ↔  {b}")
    else:
        print("    (no pairs yet — sessions need ≥2 skill loads to produce a pair)")


def main():
    parser = argparse.ArgumentParser(description="Eyeball soak window telemetry quality")
    parser.add_argument("--days", type=int, default=7, help="Window in days (default 7)")
    args = parser.parse_args()
    events = load_events(args.days)
    report(events, args.days)


if __name__ == "__main__":
    main()
