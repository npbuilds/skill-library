#!/usr/bin/env python3
"""Wire canonical depends_on + referenced_by links for investing skills.

This is the 'autoresearch' connectivity pass — adds cross-skill dependencies
so the scoring formula's connectivity dimension (20% weight) can reward skills
that are part of a coherent knowledge graph.

Run:
    python3 scripts/wire-investing-graph.py          # dry-run
    python3 scripts/wire-investing-graph.py --apply  # write registry.json
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"

# ---------------------------------------------------------------------------
# Dependency map — each skill lists what it depends on.
# References flow from more-specific to more-general (child → parent → sibling).
# ---------------------------------------------------------------------------

DEPENDENCY_MAP: dict[str, list[str]] = {
    # ── Regime Intelligence ───────────────────────────────────────────────
    "macro-cycles":        ["regime-intelligence", "monetary-regime", "fiscal-regime"],
    "monetary-regime":     ["regime-intelligence", "macro-cycles"],
    "fiscal-regime":       ["regime-intelligence", "macro-cycles", "monetary-regime"],

    # ── Risk Architecture ─────────────────────────────────────────────────
    "correlation-regimes": ["risk-architecture", "regime-intelligence", "tail-risk"],
    "drawdown-psychology": ["risk-architecture", "position-sizing", "tail-risk", "market-psychology"],
    "position-sizing":     ["risk-architecture", "tail-risk", "portfolio-construction"],
    "tail-risk":           ["risk-architecture", "correlation-regimes", "position-sizing"],

    # ── Portfolio Construction ────────────────────────────────────────────
    "asset-allocation":    ["portfolio-construction", "regime-intelligence", "risk-architecture", "correlation-regimes"],
    "factor-exposure":     ["portfolio-construction", "equities", "asset-allocation"],
    "hedging-architecture":["portfolio-construction", "tail-risk", "correlation-regimes"],
    "tax-optimization":    ["portfolio-construction", "asset-allocation"],

    # ── Reflexivity & Sentiment ───────────────────────────────────────────
    "market-psychology":   ["reflexivity-sentiment", "reflexivity-theory", "sentiment-signals"],
    "reflexivity-theory":  ["reflexivity-sentiment", "market-psychology", "macro-cycles"],
    "sentiment-signals":   ["reflexivity-sentiment", "market-psychology", "alt-data-monitoring"],

    # ── Value & Quality ───────────────────────────────────────────────────
    "intrinsic-value":     ["value-quality", "second-level-thinking", "quality-compounders"],
    "quality-compounders": ["value-quality", "intrinsic-value", "factor-exposure"],
    "second-level-thinking":["value-quality", "market-psychology", "reflexivity-theory"],

    # ── Market Microstructure ─────────────────────────────────────────────
    "liquidity-topology":  ["market-microstructure"],
    "options-mechanics":   ["market-microstructure", "tail-risk"],
    "passive-flow-dynamics":["market-microstructure", "factor-exposure"],

    # ── Geopolitical Overlay ──────────────────────────────────────────────
    "energy-security":     ["geopolitical-overlay", "great-power-dynamics"],
    "great-power-dynamics":["geopolitical-overlay", "macro-cycles"],
    "secular-themes":      ["geopolitical-overlay", "regime-intelligence"],

    # ── Asset Universe ────────────────────────────────────────────────────
    "alternatives":        ["asset-universe", "asset-allocation", "correlation-regimes"],
    "commodities":         ["asset-universe", "macro-cycles"],
    "currencies":          ["asset-universe", "monetary-regime", "macro-cycles"],
    "digital-assets":      ["asset-universe", "asset-allocation", "market-microstructure"],
    "equities":            ["asset-universe", "factor-exposure", "regime-intelligence"],
    "fixed-income":        ["asset-universe", "monetary-regime", "fiscal-regime", "correlation-regimes"],

    # ── Adaptive Monitoring ───────────────────────────────────────────────
    "alt-data-monitoring":     ["adaptive-monitoring", "sentiment-signals"],
    "performance-attribution": ["adaptive-monitoring", "asset-allocation", "factor-exposure"],
    "rebalancing-logic":       ["adaptive-monitoring", "asset-allocation"],

    # ── Special Situations ────────────────────────────────────────────────
    "complexity-premium":    ["special-situations", "second-level-thinking", "event-driven"],
    "event-driven":          ["special-situations", "insider-signals", "spinoffs-restructuring"],
    "insider-signals":       ["special-situations", "event-driven", "sentiment-signals"],
    "spinoffs-restructuring":["special-situations", "intrinsic-value", "event-driven"],

    # ── House Policy (added 2026-07-27, investing-house-policy/1.0) ───────
    # Every actor that can propose or gate an intent must depend on the
    # committed parameters. These edges are declared here, not patched into
    # registry.json directly, so they survive re-sync. house-policy itself
    # depends on nothing — it is the root of the policy hierarchy.
    "dca-investor":          ["house-policy"],
    "rebalancer":            ["house-policy"],
    "swing-trader":          ["house-policy"],
    "macro-overlay-trader":  ["house-policy"],
    "options-strategist":    ["house-policy"],
    "day-trader":            ["house-policy"],
    "earnings-event-trader": ["house-policy"],
    "reflexivity-trader":    ["house-policy"],
    "executor":              ["house-policy"],
}


def _detect_cycles(dep_map: dict[str, list[str]]) -> list[tuple[str, str]]:
    """Detect mutual dependency cycles (A→B and B→A). Returns list of (a, b) pairs."""
    cycles = []
    seen = set()
    for skill, deps in dep_map.items():
        for dep in deps:
            if dep in dep_map and skill in dep_map[dep]:
                pair = tuple(sorted([skill, dep]))
                if pair not in seen:
                    seen.add(pair)
                    cycles.append(pair)
    return cycles


def desired_dependencies(entry: dict, declared: list[str]) -> list[str]:
    """Return canonical capability edges, keeping hierarchy in `parent` only."""
    desired = set(declared)
    parent = entry.get("parent")
    if parent:
        desired.discard(parent)
    return sorted(desired)


def derive_referenced_by(skills: dict[str, dict]) -> dict[str, list[str]]:
    """Rebuild the exact reverse index from parent and capability edges."""
    reverse: dict[str, set[str]] = {name: set() for name in skills}
    for source, entry in skills.items():
        targets = set(entry.get("depends_on") or [])
        parent = entry.get("parent")
        if parent:
            targets.add(parent)
        for target in targets:
            if target in reverse and target != source:
                reverse[target].add(source)
    return {name: sorted(referrers) for name, referrers in reverse.items()}


def main() -> None:
    dry_run = "--apply" not in sys.argv

    # Check for mutual dependency cycles before wiring
    cycles = _detect_cycles(DEPENDENCY_MAP)
    if cycles:
        print(f"WARNING: {len(cycles)} mutual dependency cycle(s) detected:")
        for a, b in cycles:
            print(f"  {a} ↔ {b}")
        print()

    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    skills = registry["skills"]

    changes: list[str] = []
    prospective = {
        name: {
            **entry,
            "depends_on": list(entry.get("depends_on") or []),
            "referenced_by": list(entry.get("referenced_by") or []),
        }
        for name, entry in skills.items()
    }

    for skill_name, deps in DEPENDENCY_MAP.items():
        if skill_name not in skills:
            print(f"  SKIP (not in registry): {skill_name}")
            continue
        entry = prospective[skill_name]
        old_deps = set(entry.get("depends_on", []))
        canonical = desired_dependencies(entry, deps)
        new_deps = set(canonical)
        if old_deps != new_deps:
            changes.append(f"  {skill_name}: depends_on {sorted(old_deps)} → {sorted(new_deps)}")
        entry["depends_on"] = canonical

    # referenced_by is denormalized data. Rebuild it from the complete
    # prospective graph so removed edges cannot survive as stale referrers.
    expected_referenced_by = derive_referenced_by(prospective)
    for target_name, referrers in expected_referenced_by.items():
        entry = prospective[target_name]
        old_refs = set(entry.get("referenced_by", []))
        new_refs = set(referrers)
        if old_refs != new_refs:
            changes.append(
                f"  {target_name}: referenced_by "
                f"{sorted(old_refs)} → {sorted(new_refs)}"
            )
        entry["referenced_by"] = referrers

    if not dry_run:
        for name, entry in prospective.items():
            skills[name]["depends_on"] = entry["depends_on"]
            skills[name]["referenced_by"] = entry["referenced_by"]

    # Report
    print(f"{'DRY RUN — ' if dry_run else ''}Connectivity pass for investing skills")
    print(f"  Skills with dependency changes: {len(DEPENDENCY_MAP)}")
    print(f"  Total registry modifications: {len(changes)}")
    print()
    for line in changes[:40]:
        print(line)
    if len(changes) > 40:
        print(f"  ... and {len(changes) - 40} more")

    if not dry_run:
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
            f.write("\n")
        print("\nRegistry updated.")
        print("Next: run `python3 scripts/recalibrate_scores.py` to recompute scores.")
    else:
        print("\nRun with --apply to write changes.")


if __name__ == "__main__":
    main()
