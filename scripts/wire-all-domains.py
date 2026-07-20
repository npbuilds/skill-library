#!/usr/bin/env python3
"""Wire depends_on + referenced_by for all non-investing domains.

Covers: sommelier, writing, design, game-theory, worldbuilding,
        data-science, infrastructure, research, world-history,
        product, biotech-venture.

Run:
    python3 scripts/wire-all-domains.py          # dry-run
    python3 scripts/wire-all-domains.py --apply  # write registry.json
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"

DEPENDENCY_MAP: dict[str, list[str]] = {

    # ── SOMMELIER ──────────────────────────────────────────────────────────
    # Directors
    "cellar-service":     ["bacchus"],
    "food-pairing":       ["bacchus", "tasting-evaluation", "regions-terroir"],
    "grape-encyclopedia": ["bacchus", "regions-terroir"],
    "regions-terroir":    ["bacchus", "winemaking"],
    "sommelier-lab":      ["bacchus", "tasting-evaluation", "regions-terroir"],
    "tasting-evaluation": ["bacchus", "grape-encyclopedia", "regions-terroir"],
    "wine-market":        ["bacchus"],
    "winemaking":         ["bacchus"],
    # Tasting-evaluation children (+ cross-refs to aroma/deductive for diagnosis/assessment)
    "aroma-lexicon":          ["tasting-evaluation", "grape-encyclopedia"],
    "deductive-method":       ["tasting-evaluation"],
    "fault-diagnosis":        ["tasting-evaluation", "aroma-lexicon", "deductive-method"],
    "quality-assessment":     ["tasting-evaluation", "aroma-lexicon", "deductive-method"],
    # Regions-terroir children (+ old-world-atlas for appellation-law & indigenous-varieties)
    "appellation-law":        ["regions-terroir", "terroir-science", "old-world-atlas"],
    "new-world-atlas":        ["regions-terroir"],
    "old-world-atlas":        ["regions-terroir"],
    "terroir-science":        ["regions-terroir", "winemaking"],
    # Grape-encyclopedia children (+ noble-grapes for expression; + old-world-atlas for indigenous)
    "grape-expression":       ["grape-encyclopedia", "terroir-science", "noble-grapes"],
    "indigenous-varieties":   ["grape-encyclopedia", "regions-terroir", "old-world-atlas"],
    "noble-grapes":           ["grape-encyclopedia"],
    # Food-pairing children (+ tasting-evaluation for molecular; + molecular-pairing for cuisine)
    "cuisine-pairing":        ["food-pairing", "pairing-science", "molecular-pairing"],
    "molecular-pairing":      ["food-pairing", "pairing-science", "tasting-evaluation"],
    "pairing-engine":         ["food-pairing", "pairing-science", "tasting-evaluation"],
    "pairing-science":        ["food-pairing"],
    # Cellar-service children (+ wine-economics for mgmt; + cellar-management + tasting for service)
    "cellar-management":      ["cellar-service", "wine-economics"],
    "service-protocol":       ["cellar-service", "cellar-management", "tasting-evaluation"],
    # Sommelier-lab children (+ regions-terroir for climate projections)
    "blind-tasting-trainer":  ["sommelier-lab", "tasting-evaluation", "deductive-method"],
    "climate-projections":    ["sommelier-lab", "terroir-science", "regions-terroir"],
    "synesthetic-notes":      ["sommelier-lab", "tasting-evaluation", "aroma-lexicon"],
    # Winemaking children (+ viticulture for special/alternative methods)
    "alternative-winemaking": ["winemaking", "vinification", "viticulture"],
    "special-methods":        ["winemaking", "vinification", "viticulture"],
    "vinification":           ["winemaking", "viticulture"],
    "viticulture":            ["winemaking", "terroir-science"],
    # Wine-market children (+ cellar-management for collecting; + collecting for futures)
    "collecting-investment":  ["wine-market", "wine-economics", "cellar-management"],
    "wine-economics":         ["wine-market"],
    "wine-futures":           ["wine-market", "wine-economics", "collecting-investment"],

    # ── WRITING ────────────────────────────────────────────────────────────
    # Directors
    "narrative-craft":    ["prose-orchestrator"],
    "revision-craft":     ["prose-orchestrator"],
    "rhetoric":           ["prose-orchestrator"],
    "sentence-craft":     ["prose-orchestrator"],
    # Narrative-craft children (cross-wired: dialogue/arc/pov depend on pacing+scene-craft;
    #                           concrete-detail depends on diction+scene-craft)
    "concrete-detail":    ["narrative-craft", "diction", "scene-craft"],
    "dialogue":           ["narrative-craft", "pacing", "scene-craft"],
    "narrative-arc":      ["narrative-craft", "pacing", "scene-craft"],
    "pacing":             ["narrative-craft", "scene-craft"],
    "point-of-view":      ["narrative-craft", "pacing", "scene-craft"],
    "scene-craft":        ["narrative-craft"],
    # Sentence-craft children (syntax-patterns cross-wired to diction+prose-rhythm)
    "diction":            ["sentence-craft"],
    "prose-rhythm":       ["sentence-craft"],
    "style-dna":          ["sentence-craft"],
    "syntax-patterns":    ["sentence-craft", "diction", "prose-rhythm"],
    # Rhetoric children
    "argument-structure": ["rhetoric"],
    "essay-forms":        ["rhetoric", "argument-structure"],
    "rhetorical-appeals": ["rhetoric"],
    "rhetorical-devices": ["rhetoric", "rhetorical-appeals"],
    # Revision-craft children
    "prose-editor":       ["revision-craft", "sentence-craft"],
    "style-analyzer":     ["revision-craft", "style-dna"],
    "style-mixer":        ["revision-craft", "style-dna"],
    "style-mutator":      ["revision-craft", "style-dna", "style-analyzer"],
    # Action
    "prose-writer":       ["prose-orchestrator", "sentence-craft", "narrative-craft"],

    # ── DESIGN ─────────────────────────────────────────────────────────────
    # Directors
    "brand-identity":         ["design-orchestrator"],
    "typography":             ["design-orchestrator"],
    "visual-communication":   ["design-orchestrator"],
    # Brand-identity children
    "brand-foundations":      ["brand-identity"],
    "brand-voice":            ["brand-identity", "brand-foundations"],
    "visual-identity":        ["brand-identity", "brand-foundations"],
    # Typography children
    "responsive-type":        ["typography", "type-fundamentals"],
    "type-fundamentals":      ["typography"],
    "type-pairing":           ["typography", "type-fundamentals"],
    # Visual-communication children (illustration-direction cross-wired to color+principles)
    "color-theory":           ["visual-communication"],
    "design-principles":      ["visual-communication"],
    "illustration-direction": ["visual-communication", "color-theory", "design-principles"],
    "visual-perception":      ["visual-communication"],
    # Specialists / observers
    "aesthetic-identity":       ["design-orchestrator", "brand-identity"],
    "motion-design":            ["design-orchestrator", "visual-communication"],
    "style-evolution-observer": ["design-orchestrator", "aesthetic-identity"],

    # ── GAME THEORY ────────────────────────────────────────────────────────
    # Directors
    "computational-strategy": ["game-theory-orchestrator"],
    "evolutionary-dynamics":  ["game-theory-orchestrator"],
    "information-economics":  ["game-theory-orchestrator"],
    "mechanism-design":       ["game-theory-orchestrator"],
    "strategic-foundations":  ["game-theory-orchestrator"],
    # Strategic-foundations children
    "behavioral-game-theory": ["strategic-foundations"],
    "classical-games":        ["strategic-foundations"],
    "cooperative-games":      ["strategic-foundations", "classical-games"],
    # Computational-strategy children
    "algorithmic-game-theory":["computational-strategy", "classical-games"],
    "learning-in-games":      ["computational-strategy", "behavioral-game-theory"],
    # Evolutionary-dynamics children
    "evolutionary-games":     ["evolutionary-dynamics", "classical-games"],
    "population-dynamics":    ["evolutionary-dynamics", "evolutionary-games"],
    # Information-economics children
    "bayesian-persuasion":    ["information-economics", "signaling-screening"],
    "signaling-screening":    ["information-economics"],
    # Mechanism-design children
    "auction-theory":         ["mechanism-design"],
    "matching-markets":       ["mechanism-design"],
    "social-choice":          ["mechanism-design"],
    # Actions
    "evo-simulator":          ["evolutionary-dynamics", "evolutionary-games", "population-dynamics"],
    "game-solver":            ["strategic-foundations", "classical-games", "algorithmic-game-theory"],
    "info-designer":          ["information-economics", "signaling-screening", "bayesian-persuasion"],
    "mechanism-designer":     ["mechanism-design", "auction-theory", "matching-markets"],

    # ── WORLDBUILDING ──────────────────────────────────────────────────────
    "world-bible":              ["worldbuilding-orchestrator"],
    "character-belief-tracker": ["worldbuilding-orchestrator", "world-bible", "cultures-societies"],
    "cultures-societies":       ["worldbuilding-orchestrator", "world-bible"],
    "ecology-design":           ["worldbuilding-orchestrator", "geography-ecology"],
    "extrapolation-engine":     ["worldbuilding-orchestrator", "world-bible", "history-builder"],
    "faction-design":           ["worldbuilding-orchestrator", "cultures-societies", "history-builder"],
    "geography-ecology":        ["worldbuilding-orchestrator", "world-bible"],
    "history-builder":          ["worldbuilding-orchestrator", "world-bible", "lore-writer"],
    "lore-writer":              ["worldbuilding-orchestrator", "world-bible"],
    "magic-system-design":      ["worldbuilding-orchestrator", "world-bible"],
    "naming-system":            ["worldbuilding-orchestrator", "world-bible", "cultures-societies"],
    "narrative-pacing":         ["worldbuilding-orchestrator", "lore-writer", "world-bible"],
    "religion-design":          ["worldbuilding-orchestrator", "cultures-societies"],
    "technology-progression":   ["worldbuilding-orchestrator", "world-bible", "geography-ecology"],

    # ── DATA SCIENCE ───────────────────────────────────────────────────────
    # Directors
    "data-wrangling":       ["data-science-orchestrator"],
    "modeling":             ["data-science-orchestrator"],
    "statistical-analysis": ["data-science-orchestrator"],
    # Data-wrangling children
    "data-cleaning":        ["data-wrangling"],
    "feature-engineering":  ["data-wrangling", "modeling"],
    # Modeling children
    "drift-detection":      ["modeling", "statistical-analysis"],
    "model-evaluation":     ["modeling", "statistical-analysis"],
    "time-series":          ["modeling", "statistical-analysis"],
    # Statistical-analysis children
    "biostatistics":        ["statistical-analysis"],
    "causal-inference":     ["statistical-analysis"],
    "statistical-testing":  ["statistical-analysis"],
    # Standalone
    "chart-selection":      ["data-science-orchestrator", "statistical-analysis"],
    "responsible-ai":       ["data-science-orchestrator", "modeling"],

    # ── INFRASTRUCTURE ─────────────────────────────────────────────────────
    "skill-analyze":   ["infrastructure-orchestrator"],
    "skill-dashboard": ["infrastructure-orchestrator", "skill-registry", "skill-analyze"],
    "skill-export":    ["infrastructure-orchestrator", "skill-registry"],
    "skill-fork":      ["infrastructure-orchestrator", "skill-registry"],
    "skill-health":    ["infrastructure-orchestrator", "skill-analyze"],
    "skill-network":   ["infrastructure-orchestrator", "skill-registry", "skill-analyze"],
    "skill-registry":  ["infrastructure-orchestrator"],
    "skill-scaffold":  ["infrastructure-orchestrator"],
    "skill-test":      ["infrastructure-orchestrator", "skill-scaffold"],

    # ── RESEARCH ───────────────────────────────────────────────────────────
    "claim-decomposer":    ["spelunker"],
    "evidence-synthesizer":["spelunker", "source-triangulator", "claim-decomposer"],
    "source-triangulator": ["spelunker", "claim-decomposer"],

    # ── WORLD-HISTORY ──────────────────────────────────────────────────────
    # Directors
    "political-history":       ["wan-shi-tong"],
    "economic-history":        ["wan-shi-tong"],
    "cultural-history":        ["wan-shi-tong"],
    "military-history":        ["wan-shi-tong"],
    "intellectual-history":    ["wan-shi-tong"],
    "world-systems":           ["wan-shi-tong"],
    "historiography":          ["wan-shi-tong"],
    "applied-history":         ["wan-shi-tong"],
    "regional-atlas":          ["wan-shi-tong"],
    # Political-history children
    "empires-and-states":                ["political-history"],
    "revolutions-and-regime-change":     ["political-history"],
    "diplomacy-and-international-order": ["political-history"],
    "decolonization-and-sovereignty":    ["political-history"],
    "historical-analogy-engine":         ["political-history", "applied-history"],
    # Economic-history children
    "trade-and-globalization":           ["economic-history"],
    "money-and-financial-systems":       ["economic-history"],
    "industrialization-and-development": ["economic-history"],
    "labor-and-inequality":              ["economic-history"],
    # Cultural-history children
    "religions-and-worldviews":          ["cultural-history"],
    "gender-and-sexuality-history":      ["cultural-history"],
    "social-movements-and-identity":     ["cultural-history"],
    "art-and-cultural-production":       ["cultural-history"],
    "everyday-life-and-material-culture":["cultural-history"],
    # Military-history children
    "strategy-and-grand-strategy":       ["military-history"],
    "warfare-through-the-ages":          ["military-history"],
    "intelligence-and-information-war":  ["military-history"],
    "battle-analysis":                   ["military-history"],
    # Intellectual-history children
    "scientific-revolutions":            ["intellectual-history"],
    "political-thought":                 ["intellectual-history", "political-history"],
    "knowledge-systems":                 ["intellectual-history"],
    # World-systems children
    "comparative-civilizations":         ["world-systems"],
    "environmental-history":             ["world-systems"],
    "deep-history":                      ["world-systems"],
    "demographic-and-structural-forces": ["world-systems"],
    "technology-and-civilizational-change":["world-systems"],
    "comparative-analysis-engine":       ["world-systems", "applied-history"],
    # Historiography children
    "historical-thinking":               ["historiography"],
    "schools-of-thought":                ["historiography"],
    "source-criticism":                  ["historiography"],
    "historical-argument":               ["historiography"],
    "source-evaluator":                  ["historiography", "source-criticism"],
    # Applied-history children
    "historical-pattern-recognition":    ["applied-history"],
    "history-and-decision-making":       ["applied-history"],
    "timeline-builder":                  ["applied-history"],
    "debate-simulator":                  ["applied-history"],
    "nexus-event-analyzer":              ["applied-history"],
    # Regional-atlas children
    "mediterranean-and-near-east":       ["regional-atlas"],
    "east-asia":                         ["regional-atlas"],
    "south-asia":                        ["regional-atlas"],
    "southeast-asia":                    ["regional-atlas"],
    "sub-saharan-africa":                ["regional-atlas"],
    "americas-and-oceania":              ["regional-atlas"],

    # ── PRODUCT ────────────────────────────────────────────────────────────
    # Directors
    "sense":      ["the-loom"],
    "envision":   ["the-loom"],
    "seed":       ["the-loom", "envision"],
    "surface":    ["the-loom", "seed"],
    "evolve":     ["the-loom", "surface"],
    "synthesize": ["the-loom"],
    # Sense children
    "frontier-antenna":     ["sense"],
    "capability-radar":     ["sense"],
    "signal-reader":        ["sense"],
    "emergence-detector":   ["sense"],
    # Envision children
    "possibility-mapper":   ["envision"],
    "thesis-forge":         ["envision"],
    "vision-architect":     ["envision"],
    "paradigm-designer":    ["envision"],
    # Seed children
    "condition-designer":   ["seed"],
    "constraint-sculptor":  ["seed"],
    "prototype-grower":     ["seed"],
    "feedback-architect":   ["seed"],
    # Surface children
    "exposure-strategist":  ["surface"],
    "value-architect":      ["surface"],
    "experience-weaver":    ["surface"],
    "interface-philosopher":["surface"],
    # Evolve children
    "learning-loops":       ["evolve"],
    "pruning-engine":       ["evolve"],
    "amplifier":            ["evolve"],
    "adaptation-observer":  ["evolve"],
    # Synthesize children
    "initiative-tracker":      ["synthesize"],
    "narrative-keeper":        ["synthesize"],
    "product-briefing-engine": ["synthesize"],
    "pattern-weaver":          ["synthesize"],

    # ── BIOTECH-VENTURE ────────────────────────────────────────────────────
    # Directors
    "clinical-development":     ["asclepius"],
    "probability-of-success":   ["asclepius", "clinical-development"],
    "asset-valuation":          ["asclepius", "probability-of-success"],
    "regulatory-strategy":      ["asclepius", "clinical-development"],
    "competitive-intelligence": ["asclepius"],
    "manufacturing-ip":         ["asclepius"],
    "deal-synthesis":           ["asclepius", "asset-valuation", "probability-of-success"],
    # Clinical-development children
    "biomarker-enrichment":     ["clinical-development"],
    "patient-population-sizer": ["clinical-development"],
    "endpoint-selection":       ["clinical-development"],
    "trial-design-optimizer":   ["clinical-development"],
    # Probability-of-success children
    "pos-calculator":           ["probability-of-success", "pos-base-rates"],
    "mechanism-risk-adjuster":  ["probability-of-success"],
    "pos-base-rates":           ["probability-of-success"],
    # Asset-valuation children
    "cost-estimator":           ["asset-valuation"],
    "rnpv-modeler":             ["asset-valuation", "peak-sales-forecaster", "probability-of-success"],
    "deal-economics":           ["asset-valuation"],
    "peak-sales-forecaster":    ["asset-valuation"],
    # Regulatory-strategy children
    "pathway-analyzer":         ["regulatory-strategy"],
    "regulatory-precedent":     ["regulatory-strategy"],
    "regulatory-risk-scorer":   ["regulatory-strategy"],
    # Competitive-intelligence children
    "clinical-differentiator":  ["competitive-intelligence"],
    "market-dynamics":          ["competitive-intelligence"],
    "pipeline-mapper":          ["competitive-intelligence"],
    # Manufacturing-ip children
    "modality-manufacturing":   ["manufacturing-ip"],
    "ip-valuation":             ["manufacturing-ip"],
    "patent-analyzer":          ["manufacturing-ip"],
    "cmc-risk-assessor":        ["manufacturing-ip"],
    # Deal-synthesis children
    "portfolio-analyzer":       ["deal-synthesis"],
    "investment-memo-writer":   ["deal-synthesis", "diligence-scorecard"],
    "diligence-scorecard":      ["deal-synthesis"],
}


def main() -> None:
    dry_run = "--apply" not in sys.argv

    with open(REGISTRY_PATH) as f:
        registry = json.load(f)
    skills = registry["skills"]

    # Build reverse index. Skip parent→child edges — the MCP server adds
    # children to parent's referenced_by from the `parent` field independently,
    # so including the parent here would double-count and re-introduce the
    # parent⇄child cycle through referenced_by.
    referenced_by_index: dict[str, set[str]] = defaultdict(set)
    for skill, deps in DEPENDENCY_MAP.items():
        skill_parent = skills.get(skill, {}).get("parent")
        for dep in deps:
            if dep == skill_parent:
                continue
            referenced_by_index[dep].add(skill)

    changes: list[str] = []
    skipped: list[str] = []

    for skill_name, deps in DEPENDENCY_MAP.items():
        if skill_name not in skills:
            skipped.append(skill_name)
            continue
        entry = skills[skill_name]
        # Filter deps to only those that exist in registry
        valid_deps = sorted(d for d in deps if d in skills)
        old_deps = set(entry.get("depends_on", []))
        # depends_on is the capability DAG: drop the skill's `parent` so the
        # hierarchy field stays the sole carrier of parent→child structure
        # and the dep graph stays acyclic across parent⇄child pairs.
        parent = entry.get("parent")
        merged_deps = old_deps | set(valid_deps)
        if parent:
            merged_deps.discard(parent)
        merged_deps = sorted(merged_deps)
        if sorted(old_deps) != merged_deps:
            changes.append(f"  {skill_name}: deps {sorted(old_deps)} → {merged_deps}")
        if not dry_run:
            entry["depends_on"] = merged_deps

    # Update referenced_by (additive)
    for target, referrers in referenced_by_index.items():
        if target not in skills:
            continue
        entry = skills[target]
        old_refs = set(entry.get("referenced_by", []))
        valid_referrers = {r for r in referrers if r in skills}
        new_refs = old_refs | valid_referrers
        if old_refs != new_refs:
            changes.append(f"  {target}: referenced_by += {sorted(new_refs - old_refs)}")
        if not dry_run:
            entry["referenced_by"] = sorted(new_refs)

    # Final global pass: strip parent from every skill's depends_on, regardless
    # of whether the skill is in DEPENDENCY_MAP. Other writers (investing
    # wiring, manual edits) may have left parent edges that the per-map loop
    # above never reaches. depends_on is the capability DAG; parent is the
    # hierarchy. Keeping them disjoint is the invariant.
    parent_strip_count = 0
    for skill_name, entry in skills.items():
        parent = entry.get("parent")
        if not parent:
            continue
        deps = entry.get("depends_on") or []
        if parent in deps:
            new_deps = sorted(d for d in deps if d != parent)
            changes.append(f"  {skill_name}: stripped parent {parent} from depends_on")
            parent_strip_count += 1
            if not dry_run:
                entry["depends_on"] = new_deps

    # Summary
    mode = "DRY RUN — " if dry_run else ""
    print(f"{mode}All-domains connectivity pass")
    print(f"  Skills in map: {len(DEPENDENCY_MAP)}")
    print(f"  Skipped (not in registry): {len(skipped)}")
    if skipped:
        print(f"    {skipped}")
    print(f"  Registry modifications: {len(changes)}")
    print()
    for line in changes[:60]:
        print(line)
    if len(changes) > 60:
        print(f"  ... and {len(changes) - 60} more")

    if not dry_run:
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
            f.write("\n")
        print("\nRegistry updated.")
        print("Next: python3 scripts/recalibrate_scores.py")
    else:
        print("\nRun with --apply to write changes.")


if __name__ == "__main__":
    main()
