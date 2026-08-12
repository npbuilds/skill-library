#!/usr/bin/env python3
"""patch_mentor_suite.py — Post-sync patches for the Mentor suite.

After scripts/sync-registry.py --apply, this script:
  1. Sets mentor's parent to null (orchestrator)
  2. Sets each director's parent to "mentor"
  3. Populates depends_on lists per the plan's cross-suite integration table
  4. Mirrors entries into referenced_by on the dependency target side
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "registry.json"

# Map of skill_name -> list of depends_on entries.
#
# CONVENTION (reconciled with data/registry.json 2026-08-11): depends_on never
# includes a skill's own structural parent — the parent/child edge lives in the
# `parent` field, and duplicating it here created the cycles removed in the
# registry cleanups (3cd9717, 7082150). This script does a blind overwrite of
# every list below, so DEPS must stay byte-identical to the registry's
# depends_on for these skills; a bare run should always be a no-op
# (git diff data/registry.json empty). Durable edge changes go in BOTH places.
DEPS = {
    # Orchestrator
    "mentor": [],

    # Directors
    "personal-positioning": [],
    "interview-mastery": [],
    "network-cultivation": [],
    "trajectory-design": [],
    "executive-presence": [],
    "negotiation-leverage": [],
    "feedback-loops": [],

    # Standalone action leaves (parent: mentor via sync-registry inference).
    "ariadne": ["vault-writer"],

    # personal-positioning leaves
    "narrative-architecture": ["brand-foundations", "brand-voice", "minto-scqa"],
    "linkedin-optimization": [
        "audience-classifier", "audience-tuning", "credibility-translation",
        "narrative-architecture", "prose-editor"
    ],
    "public-portfolio": [
        "asclepius", "credibility-translation", "linkedin-optimization",
        "narrative-architecture", "prose-editor", "spelunker", "the-loom"
    ],
    "credibility-translation": [
        "asclepius", "audience-classifier", "narrative-architecture"
    ],
    "audience-tuning": [
        "audience-classifier", "behavioral-frameworks", "cover-letter-craft",
        "credibility-translation", "narrative-architecture", "prose-editor"
    ],
    "resume-craft": [
        "asclepius", "audience-tuning", "cover-letter-craft", "credibility-translation",
        "linkedin-optimization", "narrative-architecture", "prose-editor"
    ],
    "cover-letter-craft": [
        "asclepius", "audience-classifier", "bluf-shaper", "credibility-translation",
        "narrative-architecture", "prose-editor", "spelunker"
    ],

    # interview-mastery leaves
    "behavioral-frameworks": [
        "asclepius", "credibility-translation", "minto-scqa", "narrative-architecture"
    ],
    "domain-deepdives": [
        "asclepius", "asset-valuation", "behavioral-frameworks", "clinical-development",
        "credibility-translation", "deal-synthesis", "executive-interview-prep",
        "probability-of-success", "regulatory-strategy", "spelunker", "the-loom",
        "vc-interview-prep"
    ],
    "vc-interview-prep": [
        "asclepius", "asset-valuation", "behavioral-frameworks", "cover-letter-craft",
        "credibility-translation", "deal-synthesis", "ecosystem-mapping",
        "probability-of-success", "regulatory-strategy", "spelunker"
    ],
    "executive-interview-prep": [
        "asclepius", "behavioral-frameworks", "credibility-translation",
        "executive-communication", "role-archetype-mapping"
    ],
    "panel-and-case": [
        "asclepius", "asset-valuation", "behavioral-frameworks", "bluf-shaper",
        "deal-synthesis", "domain-deepdives", "executive-communication",
        "executive-interview-prep", "minto-scqa", "vc-interview-prep"
    ],

    # network-cultivation leaves
    "cold-outreach": [
        "cover-letter-craft", "credibility-translation", "ecosystem-mapping",
        "prose-editor", "relationship-stewardship", "spelunker"
    ],
    "relationship-stewardship": ["ecosystem-mapping", "prose-editor", "the-loom"],
    "mentorship-design": [
        "advisor-board", "cold-outreach", "ecosystem-mapping",
        "relationship-stewardship", "role-archetype-mapping", "the-loom"
    ],
    "ecosystem-mapping": [
        "asclepius", "cover-letter-craft", "source-triangulator", "spelunker", "the-loom"
    ],
    "introductions-and-referrals": [
        "audience-tuning", "cold-outreach", "credibility-translation",
        "ecosystem-mapping", "narrative-architecture", "prose-editor",
        "relationship-stewardship"
    ],

    # trajectory-design leaves
    "role-archetype-mapping": [
        "ecosystem-mapping", "narrative-architecture", "vc-interview-prep"
    ],
    "optionality-architecture": ["archon", "role-archetype-mapping", "the-loom"],
    "idp-and-okrs": ["role-archetype-mapping", "the-loom"],
    "skill-gap-analysis": [
        "advisor-board", "idp-and-okrs", "public-portfolio", "role-archetype-mapping"
    ],
    "pivot-sequencing": [
        "ecosystem-mapping", "idp-and-okrs", "optionality-architecture",
        "public-portfolio", "role-archetype-mapping", "skill-gap-analysis"
    ],

    # executive-presence leaves
    "executive-communication": [
        "audience-classifier", "bluf-shaper", "cover-letter-craft",
        "executive-distiller", "minto-scqa", "prose-editor"
    ],
    "meeting-mastery": [
        "audience-classifier", "bluf-shaper", "board-readiness",
        "executive-communication", "panel-and-case", "the-loom"
    ],
    "public-speaking": [
        "audience-tuning", "executive-communication", "meeting-mastery", "minto-scqa",
        "prose-editor", "public-portfolio"
    ],
    "board-readiness": [
        "archon", "asclepius", "equity-literacy", "executive-communication",
        "executive-interview-prep", "role-archetype-mapping"
    ],

    # negotiation-leverage leaves
    "offer-negotiation": ["archon", "bluf-shaper", "optionality-architecture"],
    "equity-literacy": [
        "archon", "asset-valuation", "offer-negotiation", "optionality-architecture"
    ],
    "title-and-scope": [
        "board-readiness", "equity-literacy", "narrative-architecture",
        "offer-negotiation", "optionality-architecture", "role-archetype-mapping"
    ],
    "exit-and-transition": [
        "equity-literacy", "narrative-architecture", "offer-negotiation",
        "optionality-architecture", "relationship-stewardship"
    ],

    # feedback-loops leaves
    "360-feedback-design": [
        "advisor-board", "idp-and-okrs", "reflection-and-journaling",
        "skill-gap-analysis"
    ],
    "performance-review-craft": [
        "360-feedback-design", "audience-tuning", "credibility-translation",
        "idp-and-okrs", "prose-editor", "reflection-and-journaling", "resume-craft"
    ],
    "advisor-board": ["idp-and-okrs", "relationship-stewardship", "the-loom"],
    "reflection-and-journaling": [
        "advisor-board", "idp-and-okrs", "prose-editor", "the-loom"
    ],

}

# Director parent overrides (the auto-inference makes them parent=domain;
# we want them to be parent=mentor)
DIRECTORS = [
    "personal-positioning", "interview-mastery", "network-cultivation",
    "trajectory-design", "executive-presence", "negotiation-leverage",
    "feedback-loops",
]


def main():
    with open(REG) as f:
        reg = json.load(f)
    skills = reg["skills"]

    patched = 0
    missing_deps = []

    # 1. Mentor: parent = None, depends_on = []
    if "mentor" in skills:
        skills["mentor"]["parent"] = None
        skills["mentor"]["depends_on"] = []
        patched += 1

    # 2. Directors: parent = mentor
    for d in DIRECTORS:
        if d in skills:
            skills[d]["parent"] = "mentor"
            patched += 1

    # 3. depends_on for each Mentor-suite skill
    for skill_name, deps in DEPS.items():
        if skill_name not in skills:
            missing_deps.append(skill_name)
            continue
        # Filter: keep only deps that resolve in the registry
        resolved = [d for d in deps if d in skills]
        unresolved = [d for d in deps if d not in skills]
        skills[skill_name]["depends_on"] = resolved
        if unresolved:
            print(f"  WARN: {skill_name} has unresolved deps: {unresolved}")

    # 4. Mirror referenced_by on the target side
    # For each skill in DEPS, for each resolved dep, add skill to dep's referenced_by
    for skill_name, deps in DEPS.items():
        if skill_name not in skills:
            continue
        for dep in skills[skill_name].get("depends_on", []):
            if dep in skills:
                rb = skills[dep].get("referenced_by", [])
                if skill_name not in rb:
                    rb.append(skill_name)
                    rb.sort()
                    skills[dep]["referenced_by"] = rb

    if missing_deps:
        print(f"  WARN: {len(missing_deps)} skills in DEPS not in registry: {missing_deps}")

    with open(REG, "w") as f:
        json.dump(reg, f, indent=2)
        f.write("\n")

    print(f"\nPatched {patched} parent overrides and {len(DEPS)} depends_on lists.")
    print("Done.")


if __name__ == "__main__":
    main()
