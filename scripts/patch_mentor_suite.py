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

# Map of skill_name -> list of depends_on entries
DEPS = {
    # Orchestrator
    "mentor": [],

    # Directors
    "personal-positioning": ["mentor"],
    "interview-mastery": ["mentor"],
    "network-cultivation": ["mentor"],
    "trajectory-design": ["mentor"],
    "executive-presence": ["mentor"],
    "negotiation-leverage": ["mentor"],
    "feedback-loops": ["mentor"],

    # personal-positioning leaves
    "narrative-architecture": [
        "personal-positioning", "design", "brand-foundations", "brand-voice", "minto-scqa"
    ],
    "linkedin-optimization": [
        "personal-positioning", "narrative-architecture", "credibility-translation",
        "audience-tuning", "public-portfolio", "prose-editor", "audience-classifier"
    ],
    "public-portfolio": [
        "personal-positioning", "narrative-architecture", "linkedin-optimization",
        "credibility-translation", "prose-editor", "asclepius", "the-loom", "spelunker"
    ],
    "credibility-translation": [
        "personal-positioning", "narrative-architecture", "audience-tuning",
        "resume-craft", "cover-letter-craft", "linkedin-optimization",
        "behavioral-frameworks", "asclepius", "audience-classifier"
    ],
    "audience-tuning": [
        "personal-positioning", "audience-classifier", "narrative-architecture",
        "credibility-translation", "resume-craft", "cover-letter-craft",
        "linkedin-optimization", "behavioral-frameworks", "prose-editor"
    ],
    "resume-craft": [
        "personal-positioning", "narrative-architecture", "credibility-translation",
        "audience-tuning", "linkedin-optimization", "cover-letter-craft",
        "prose-editor", "asclepius"
    ],
    "cover-letter-craft": [
        "personal-positioning", "spelunker", "credibility-translation",
        "narrative-architecture", "audience-tuning", "bluf-shaper",
        "audience-classifier", "prose-editor", "asclepius"
    ],

    # interview-mastery leaves
    "behavioral-frameworks": [
        "interview-mastery", "panel-and-case", "vc-interview-prep",
        "executive-interview-prep", "credibility-translation",
        "narrative-architecture", "minto-scqa", "asclepius"
    ],
    "domain-deepdives": [
        "interview-mastery", "asclepius", "clinical-development", "regulatory-strategy",
        "asset-valuation", "probability-of-success", "deal-synthesis",
        "vc-interview-prep", "executive-interview-prep", "behavioral-frameworks",
        "spelunker", "credibility-translation", "the-loom"
    ],
    "vc-interview-prep": [
        "interview-mastery", "asclepius", "deal-synthesis", "probability-of-success",
        "asset-valuation", "regulatory-strategy", "behavioral-frameworks",
        "panel-and-case", "domain-deepdives", "credibility-translation",
        "cover-letter-craft", "spelunker", "ecosystem-mapping"
    ],
    "executive-interview-prep": [
        "interview-mastery", "board-readiness", "executive-communication",
        "behavioral-frameworks", "domain-deepdives", "panel-and-case",
        "asclepius", "credibility-translation", "role-archetype-mapping"
    ],
    "panel-and-case": [
        "interview-mastery", "vc-interview-prep", "executive-interview-prep",
        "behavioral-frameworks", "domain-deepdives", "asclepius", "deal-synthesis",
        "asset-valuation", "meeting-mastery", "executive-communication",
        "bluf-shaper", "minto-scqa"
    ],

    # network-cultivation leaves
    "cold-outreach": [
        "network-cultivation", "relationship-stewardship", "introductions-and-referrals",
        "ecosystem-mapping", "credibility-translation", "cover-letter-craft",
        "prose-editor", "spelunker"
    ],
    "relationship-stewardship": [
        "network-cultivation", "cold-outreach", "mentorship-design",
        "introductions-and-referrals", "ecosystem-mapping", "the-loom",
        "prose-editor", "advisor-board"
    ],
    "mentorship-design": [
        "network-cultivation", "cold-outreach", "relationship-stewardship",
        "ecosystem-mapping", "advisor-board", "role-archetype-mapping", "the-loom"
    ],
    "ecosystem-mapping": [
        "network-cultivation", "spelunker", "source-triangulator", "cold-outreach",
        "relationship-stewardship", "introductions-and-referrals", "cover-letter-craft",
        "vc-interview-prep", "asclepius", "the-loom"
    ],
    "introductions-and-referrals": [
        "network-cultivation", "ecosystem-mapping", "relationship-stewardship",
        "cold-outreach", "credibility-translation", "narrative-architecture",
        "audience-tuning", "prose-editor"
    ],

    # trajectory-design leaves
    "role-archetype-mapping": [
        "trajectory-design", "optionality-architecture", "skill-gap-analysis",
        "pivot-sequencing", "narrative-architecture", "ecosystem-mapping",
        "vc-interview-prep", "executive-interview-prep"
    ],
    "optionality-architecture": [
        "trajectory-design", "role-archetype-mapping", "pivot-sequencing",
        "offer-negotiation", "archon", "the-loom"
    ],
    "idp-and-okrs": [
        "trajectory-design", "role-archetype-mapping", "skill-gap-analysis",
        "pivot-sequencing", "reflection-and-journaling", "advisor-board", "the-loom"
    ],
    "skill-gap-analysis": [
        "trajectory-design", "role-archetype-mapping", "pivot-sequencing",
        "idp-and-okrs", "360-feedback-design", "advisor-board", "public-portfolio"
    ],
    "pivot-sequencing": [
        "trajectory-design", "role-archetype-mapping", "skill-gap-analysis",
        "optionality-architecture", "idp-and-okrs", "public-portfolio",
        "ecosystem-mapping"
    ],

    # executive-presence leaves
    "executive-communication": [
        "executive-presence", "bluf-shaper", "executive-distiller", "minto-scqa",
        "audience-classifier", "meeting-mastery", "board-readiness",
        "cover-letter-craft", "prose-editor"
    ],
    "meeting-mastery": [
        "executive-presence", "executive-communication", "board-readiness",
        "panel-and-case", "bluf-shaper", "audience-classifier", "the-loom"
    ],
    "public-speaking": [
        "executive-presence", "executive-communication", "meeting-mastery",
        "public-portfolio", "audience-tuning", "minto-scqa", "prose-editor"
    ],
    "board-readiness": [
        "executive-presence", "executive-communication", "meeting-mastery",
        "equity-literacy", "executive-interview-prep", "archon", "asclepius",
        "role-archetype-mapping"
    ],

    # negotiation-leverage leaves
    "offer-negotiation": [
        "negotiation-leverage", "equity-literacy", "title-and-scope",
        "exit-and-transition", "optionality-architecture", "archon", "bluf-shaper"
    ],
    "equity-literacy": [
        "negotiation-leverage", "offer-negotiation", "exit-and-transition",
        "archon", "asset-valuation", "optionality-architecture"
    ],
    "title-and-scope": [
        "negotiation-leverage", "offer-negotiation", "equity-literacy",
        "role-archetype-mapping", "optionality-architecture", "board-readiness",
        "narrative-architecture"
    ],
    "exit-and-transition": [
        "negotiation-leverage", "equity-literacy", "offer-negotiation",
        "optionality-architecture", "narrative-architecture", "relationship-stewardship"
    ],

    # feedback-loops leaves
    "360-feedback-design": [
        "feedback-loops", "performance-review-craft", "advisor-board",
        "reflection-and-journaling", "skill-gap-analysis", "idp-and-okrs"
    ],
    "performance-review-craft": [
        "feedback-loops", "resume-craft", "credibility-translation",
        "audience-tuning", "360-feedback-design", "reflection-and-journaling",
        "idp-and-okrs", "prose-editor"
    ],
    "advisor-board": [
        "feedback-loops", "mentorship-design", "relationship-stewardship",
        "360-feedback-design", "idp-and-okrs", "the-loom",
        "reflection-and-journaling"
    ],
    "reflection-and-journaling": [
        "feedback-loops", "the-loom", "360-feedback-design", "advisor-board",
        "performance-review-craft", "idp-and-okrs", "prose-editor"
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
