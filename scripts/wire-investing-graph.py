#!/usr/bin/env python3
"""Wire up depends_on + referenced_by links for all 37 investing knowledge skills.

This is the 'autoresearch' connectivity pass — adds cross-skill dependencies
so the scoring formula's connectivity dimension (20% weight) can reward skills
that are part of a coherent knowledge graph.

Run:
    python3 scripts/wire-investing-graph.py          # dry-run
    python3 scripts/wire-investing-graph.py --apply  # write registry.json
"""

import json
import sys
from collections import defaultdict
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
    "hedging-architecture":["portfolio-construction", "tail-risk", "options-mechanics", "correlation-regimes"],
    "tax-optimization":    ["portfolio-construction", "asset-allocation", "rebalancing-logic"],

    # ── Reflexivity & Sentiment ───────────────────────────────────────────
    "market-psychology":   ["reflexivity-sentiment", "reflexivity-theory", "sentiment-signals"],
    "reflexivity-theory":  ["reflexivity-sentiment", "market-psychology", "macro-cycles"],
    "sentiment-signals":   ["reflexivity-sentiment", "market-psychology", "alt-data-monitoring"],

    # ── Value & Quality ───────────────────────────────────────────────────
    "intrinsic-value":     ["value-quality", "second-level-thinking", "quality-compounders"],
    "quality-compounders": ["value-quality", "intrinsic-value", "factor-exposure"],
    "second-level-thinking":["value-quality", "market-psychology", "reflexivity-theory"],

    # ── Market Microstructure ─────────────────────────────────────────────
    "liquidity-topology":  ["market-microstructure", "passive-flow-dynamics"],
    "options-mechanics":   ["market-microstructure", "hedging-architecture", "tail-risk"],
    "passive-flow-dynamics":["market-microstructure", "liquidity-topology", "factor-exposure"],

    # ── Geopolitical Overlay ──────────────────────────────────────────────
    "energy-security":     ["geopolitical-overlay", "commodities", "great-power-dynamics"],
    "great-power-dynamics":["geopolitical-overlay", "secular-themes", "macro-cycles"],
    "secular-themes":      ["geopolitical-overlay", "great-power-dynamics", "regime-intelligence"],

    # ── Asset Universe ────────────────────────────────────────────────────
    "alternatives":        ["asset-universe", "asset-allocation", "correlation-regimes"],
    "commodities":         ["asset-universe", "energy-security", "macro-cycles"],
    "currencies":          ["asset-universe", "monetary-regime", "macro-cycles"],
    "digital-assets":      ["asset-universe", "asset-allocation", "market-microstructure"],
    "equities":            ["asset-universe", "factor-exposure", "regime-intelligence"],
    "fixed-income":        ["asset-universe", "monetary-regime", "fiscal-regime", "correlation-regimes"],

    # ── Adaptive Monitoring ───────────────────────────────────────────────
    "alt-data-monitoring":     ["adaptive-monitoring", "sentiment-signals"],
    "performance-attribution": ["adaptive-monitoring", "asset-allocation", "factor-exposure"],
    "rebalancing-logic":       ["adaptive-monitoring", "asset-allocation", "tax-optimization"],

    # ── Special Situations ────────────────────────────────────────────────
    "complexity-premium":    ["special-situations", "second-level-thinking", "event-driven"],
    "event-driven":          ["special-situations", "insider-signals", "spinoffs-restructuring"],
    "insider-signals":       ["special-situations", "event-driven", "sentiment-signals"],
    "spinoffs-restructuring":["special-situations", "intrinsic-value", "event-driven"],
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

    # Capture before-state
    before: dict[str, tuple[list, list]] = {
        name: (list(entry.get("depends_on", [])), list(entry.get("referenced_by", [])))
        for name, entry in skills.items()
    }

    # Build the full referenced_by index from the dependency map
    referenced_by_index: dict[str, set[str]] = defaultdict(set)
    for skill, deps in DEPENDENCY_MAP.items():
        for dep in deps:
            referenced_by_index[dep].add(skill)

    changes: list[str] = []

    for skill_name, deps in DEPENDENCY_MAP.items():
        if skill_name not in skills:
            print(f"  SKIP (not in registry): {skill_name}")
            continue
        entry = skills[skill_name]
        old_deps = set(entry.get("depends_on", []))
        new_deps = set(deps)
        if old_deps != new_deps:
            changes.append(f"  {skill_name}: depends_on {sorted(old_deps)} → {sorted(new_deps)}")
        if not dry_run:
            entry["depends_on"] = sorted(deps)

    # Update referenced_by for every skill that appears as a dependency target
    for target_name, referrers in referenced_by_index.items():
        if target_name not in skills:
            continue
        entry = skills[target_name]
        old_refs = set(entry.get("referenced_by", []))
        new_refs = old_refs | referrers  # additive — never remove existing refs
        if old_refs != new_refs:
            changes.append(f"  {target_name}: referenced_by += {sorted(new_refs - old_refs)}")
        if not dry_run:
            entry["referenced_by"] = sorted(new_refs)

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
