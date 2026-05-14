#!/usr/bin/env python3
"""Calibration report — reads data/calibration.jsonl and prints hit-rates per confidence tier.

Usage: python3 scripts/calibration-report.py [--json]

Reports for each Spelunker confidence tier (Confirmed/Likely/Speculative/Contested/Unverifiable):
- Number of resolved claims
- Outcome breakdown (true/false/partial)
- Hit rate (true / total, with partial counted as 0.5)
- Distance from target hit rate (Confirmed: ~95%, Likely: ~70%, Speculative: ~40%)
- Miscalibration flag if distance > 15 percentage points

Confidence tiers without enough resolutions (n < 5) are reported but flagged as "low n".
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / "data" / "calibration.jsonl"

TARGETS = {
    "Confirmed": 0.95,
    "Likely": 0.70,
    "Speculative": 0.40,
    "Contested": None,
    "Unverifiable": None,
    "unknown": None,
}

OUTCOME_WEIGHTS = {"true": 1.0, "partial": 0.5, "false": 0.0}


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def aggregate(entries: list[dict]) -> dict[str, dict]:
    buckets: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "true": 0, "false": 0, "partial": 0, "weighted": 0.0}
    )
    for e in entries:
        tier = e.get("predicted_confidence", "unknown") or "unknown"
        outcome = e.get("outcome", "")
        if outcome not in OUTCOME_WEIGHTS:
            continue
        b = buckets[tier]
        b["n"] += 1
        b[outcome] += 1
        b["weighted"] += OUTCOME_WEIGHTS[outcome]
    return buckets


def render_text(buckets: dict[str, dict]) -> str:
    lines = []
    lines.append("Spelunker Calibration Report")
    lines.append("=" * 60)
    total = sum(b["n"] for b in buckets.values())
    if total == 0:
        lines.append("No calibration entries yet. Use `/calibrate` to start logging.")
        return "\n".join(lines)
    lines.append(f"Total resolved claims: {total}")
    lines.append("")
    lines.append(f"{'Tier':<14} {'n':>5} {'True':>5} {'Part':>5} {'False':>5} {'Hit%':>7} {'Target':>7} {'Δ':>7} Status")
    lines.append("-" * 76)
    for tier in ["Confirmed", "Likely", "Speculative", "Contested", "Unverifiable", "unknown"]:
        if tier not in buckets:
            continue
        b = buckets[tier]
        n = b["n"]
        if n == 0:
            continue
        hit_rate = b["weighted"] / n
        target = TARGETS.get(tier)
        if target is None:
            target_s = "—"
            delta_s = "—"
            status = "(no target)"
        else:
            delta = hit_rate - target
            target_s = f"{target * 100:.0f}%"
            delta_s = f"{delta * 100:+.0f}pp"
            if n < 5:
                status = "low n"
            elif abs(delta) > 0.15:
                status = "MISCALIBRATED"
            elif abs(delta) > 0.08:
                status = "drifting"
            else:
                status = "ok"
        lines.append(
            f"{tier:<14} {n:>5} {b['true']:>5} {b['partial']:>5} {b['false']:>5} "
            f"{hit_rate * 100:>6.0f}% {target_s:>7} {delta_s:>7} {status}"
        )
    lines.append("")
    lines.append("Targets: Confirmed ~95%, Likely ~70%, Speculative ~40%.")
    lines.append("Contested/Unverifiable have no target — they describe knowledge state, not predictions.")
    lines.append("Δ = hit_rate − target. |Δ| > 15pp → MISCALIBRATED. n < 5 → low confidence in the estimate.")
    return "\n".join(lines)


def main() -> int:
    as_json = "--json" in sys.argv
    entries = load_entries(LEDGER)
    buckets = aggregate(entries)
    if as_json:
        out = {
            "ledger": str(LEDGER),
            "total": sum(b["n"] for b in buckets.values()),
            "buckets": {
                tier: {
                    "n": b["n"],
                    "true": b["true"],
                    "partial": b["partial"],
                    "false": b["false"],
                    "hit_rate": (b["weighted"] / b["n"]) if b["n"] else None,
                    "target": TARGETS.get(tier),
                }
                for tier, b in buckets.items()
            },
        }
        print(json.dumps(out, indent=2))
    else:
        print(render_text(buckets))
    return 0


if __name__ == "__main__":
    sys.exit(main())
