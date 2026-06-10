"""Structural health eval for the skill library.

Independently re-derives state from disk (via real yaml parser) and from
data/registry.json, then cross-checks. Per CLAUDE.md scan-methodology rule:
do not trust cached aggregates — re-derive.

Output: data/health/eval_structural_<utcdate>.json + a stdout summary.
"""

import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY = ROOT / "data" / "registry.json"
OUT_DIR = ROOT / "data" / "health"
OUT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FRONTMATTER = ["name", "description"]
RECOMMENDED_FRONTMATTER = ["type", "tags"]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

# Description lint (Anthropic Agent Skills guidance). These are RATCHET
# warnings, not hard gates — 509 legacy skills predate the convention.
DESC_MAX_LEN = 1024  # Anthropic frontmatter limit
# First/second-person openers — descriptions must be third person because the
# description is injected into the system prompt for skill selection.
_VOICE_RE = re.compile(
    r"^\s*(i\s|i'm\b|i\s+can\b|we\s|we'll\b|we\s+can\b|you\s+can\b|you'll\b|"
    r"helps?\s+you\b|lets?\s+you\b|use\s+this\s+to\s+help\s+you\b)",
    re.IGNORECASE,
)
# A good description names its trigger CONDITION or CONTEXT — "Use when...",
# "Activate when...", "Use during <phase>", "Called by/Coordinates with...".
# This is intentionally broad: the lint flags descriptions that state only
# WHAT a skill does with no signal of WHEN/WHERE it applies.
_TRIGGER_RE = re.compile(
    r"\b(use\s+when|use\s+this\s+when|use\s+during|use\s+for\b|activate\s+when|"
    r"activate\s+during|invoke\s+when|trigger\b|called\s+by|coordinat(es|e)\s+with|"
    r"during\s+\w+('s)?\s+phase|when\s+(you|the\s+user|a\s|an\s|someone|asked|"
    r"evaluating|building|designing|writing|analyzing|the\s+question))",
    re.IGNORECASE,
)
SIBLING_DUPE_RATIO = 0.85  # difflib ratio above which two siblings are near-dupes


def lint_descriptions(disk_skills: dict, reg_skills: dict) -> dict:
    """Lint descriptions for voice, trigger phrasing, length, sibling dupes.

    Returns a dict of issue-name -> list. All findings are warnings.
    """
    voice = []
    no_trigger = []
    overlong = []
    by_parent = defaultdict(list)  # parent -> [(name, description)]

    for name, entry in disk_skills.items():
        desc = (entry["fm"].get("description") or "").strip()
        if not desc:
            continue
        if _VOICE_RE.match(desc):
            voice.append({"name": name, "path": entry["path"], "opens": desc[:50]})
        if not _TRIGGER_RE.search(desc):
            no_trigger.append({"name": name, "path": entry["path"]})
        if len(desc) > DESC_MAX_LEN:
            overlong.append({"name": name, "len": len(desc), "path": entry["path"]})
        parent = reg_skills.get(name, {}).get("parent")
        if parent:
            by_parent[parent].append((name, desc))

    # Sibling near-duplicates: descriptions too similar to a same-parent peer
    # blur routing between them.
    sibling_dupes = []
    for parent, sibs in by_parent.items():
        for i in range(len(sibs)):
            for j in range(i + 1, len(sibs)):
                ratio = SequenceMatcher(None, sibs[i][1], sibs[j][1]).ratio()
                if ratio > SIBLING_DUPE_RATIO:
                    sibling_dupes.append({
                        "parent": parent,
                        "skills": [sibs[i][0], sibs[j][0]],
                        "ratio": round(ratio, 3),
                    })

    return {
        "desc-voice-not-third-person": voice,
        "desc-no-trigger-phrase": no_trigger,
        "desc-overlong": overlong,
        "desc-sibling-near-duplicates": sibling_dupes,
    }


def parse_skill_file(path: Path):
    """Return (frontmatter_dict_or_None, body_text, parse_error)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FM_RE.match(text)
    if not m:
        return None, text, "missing-frontmatter"
    raw = m.group(1)
    try:
        fm = yaml.safe_load(raw)
        if not isinstance(fm, dict):
            return None, text[m.end():], "frontmatter-not-mapping"
        return fm, text[m.end():], None
    except yaml.YAMLError as e:
        return None, text[m.end():], f"yaml-error: {e}"


def main():
    findings = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {},
        "issues": defaultdict(list),
        "summary": {},
    }

    # ---- Walk disk ----
    disk_skills = {}  # name -> {path, fm, body_len, errors}
    duplicates_by_name = defaultdict(list)
    parse_failures = []

    for skill_path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        rel = skill_path.relative_to(ROOT).as_posix()
        fm, body, err = parse_skill_file(skill_path)
        if err:
            parse_failures.append({"path": rel, "error": err})
            continue
        name = fm.get("name")
        if not name:
            findings["issues"]["missing-name"].append({"path": rel})
            continue
        entry = {
            "path": rel,
            "fm": fm,
            "body_len": len(body),
            "description_len": len(fm.get("description") or ""),
        }
        if name in disk_skills:
            duplicates_by_name[name].append(entry)
            duplicates_by_name[name].append(disk_skills[name])
        disk_skills[name] = entry

    findings["counts"]["disk_skill_files"] = len(list(SKILLS_DIR.rglob("SKILL.md")))
    findings["counts"]["disk_skills_parsed"] = len(disk_skills)
    findings["counts"]["parse_failures"] = len(parse_failures)
    findings["issues"]["parse-failures"] = parse_failures
    findings["issues"]["duplicate-names"] = [
        {"name": n, "paths": [e["path"] for e in entries]}
        for n, entries in duplicates_by_name.items()
    ]

    # ---- Frontmatter validation ----
    missing_required = []
    missing_recommended = defaultdict(list)
    short_descriptions = []  # too short for retrieval to work

    for name, entry in disk_skills.items():
        fm = entry["fm"]
        for req in REQUIRED_FRONTMATTER:
            if not fm.get(req):
                missing_required.append({"name": name, "path": entry["path"], "field": req})
        for rec in RECOMMENDED_FRONTMATTER:
            if not fm.get(rec):
                missing_recommended[rec].append(name)
        if entry["description_len"] < 60:
            short_descriptions.append(
                {"name": name, "len": entry["description_len"], "path": entry["path"]}
            )

    findings["issues"]["missing-required-fields"] = missing_required
    findings["issues"]["missing-recommended"] = dict(missing_recommended)
    findings["issues"]["short-descriptions"] = short_descriptions

    # ---- Load registry ----
    reg = json.loads(REGISTRY.read_text())
    reg_skills = reg.get("skills", {})
    findings["counts"]["registry_skills"] = len(reg_skills)
    findings["counts"]["registry_schema_version"] = reg.get("schema_version")
    findings["counts"]["registry_last_scan"] = reg.get("last_scan")

    # ---- Description lint (ratchet warnings) ----
    lint = lint_descriptions(disk_skills, reg_skills)
    for key, items in lint.items():
        findings["issues"][key] = items
    findings["summary"]["description_lint"] = {k: len(v) for k, v in lint.items()}

    # ---- Disk <-> Registry sync ----
    disk_names = set(disk_skills.keys())
    reg_names = set(reg_skills.keys())
    findings["issues"]["on-disk-not-in-registry"] = sorted(disk_names - reg_names)
    findings["issues"]["in-registry-not-on-disk"] = sorted(reg_names - disk_names)

    # location-field drift: registry says X, disk says Y
    location_mismatches = []
    for name in disk_names & reg_names:
        reg_loc = (reg_skills[name].get("location") or "").strip()
        disk_loc = disk_skills[name]["path"]
        if reg_loc and reg_loc != disk_loc:
            location_mismatches.append(
                {"name": name, "registry": reg_loc, "disk": disk_loc}
            )
    findings["issues"]["location-drift"] = location_mismatches

    # ---- Reference integrity (re-derive, do NOT trust referenced_by) ----
    # depends_on, parent
    broken_parent = []
    broken_depends_on = []
    derived_referenced_by = defaultdict(set)

    for name, sk in reg_skills.items():
        parent = sk.get("parent")
        if parent and parent not in reg_skills:
            broken_parent.append({"name": name, "missing_parent": parent})
        if parent and parent in reg_skills:
            derived_referenced_by[parent].add(name)
        for dep in sk.get("depends_on") or []:
            if dep not in reg_skills:
                broken_depends_on.append({"name": name, "missing_dep": dep})
            else:
                derived_referenced_by[dep].add(name)

    findings["issues"]["broken-parent-refs"] = broken_parent
    findings["issues"]["broken-depends-on"] = broken_depends_on

    # Compare derived referenced_by to stored referenced_by
    rb_drift = []
    for name, sk in reg_skills.items():
        stored = set(sk.get("referenced_by") or [])
        derived = derived_referenced_by.get(name, set())
        if stored != derived:
            rb_drift.append(
                {
                    "name": name,
                    "stored_only": sorted(stored - derived),
                    "derived_only": sorted(derived - stored),
                }
            )
    findings["issues"]["referenced-by-drift"] = rb_drift

    # ---- Health-status sanity (registry self-claims) ----
    by_health = defaultdict(int)
    for name, sk in reg_skills.items():
        by_health[sk.get("health_status") or "unset"] += 1
    findings["summary"]["health_status_distribution"] = dict(by_health)

    by_status = defaultdict(int)
    for name, sk in reg_skills.items():
        by_status[sk.get("status") or "unset"] += 1
    findings["summary"]["status_distribution"] = dict(by_status)

    # auto_score distribution buckets
    score_buckets = {"<50": 0, "50-69": 0, "70-79": 0, "80-89": 0, ">=90": 0, "missing": 0}
    for name, sk in reg_skills.items():
        s = sk.get("auto_score")
        if s is None:
            score_buckets["missing"] += 1
        elif s < 50:
            score_buckets["<50"] += 1
        elif s < 70:
            score_buckets["50-69"] += 1
        elif s < 80:
            score_buckets["70-79"] += 1
        elif s < 90:
            score_buckets["80-89"] += 1
        else:
            score_buckets[">=90"] += 1
    findings["summary"]["auto_score_distribution"] = score_buckets

    # ---- Severity counts ----
    severity = {
        "critical": (
            len(parse_failures)
            + len(missing_required)
            + len(broken_parent)
            + len(broken_depends_on)
            + len(findings["issues"]["on-disk-not-in-registry"])
            + len(findings["issues"]["in-registry-not-on-disk"])
            + len(duplicates_by_name)
        ),
        "warnings": (
            len(location_mismatches)
            + len(rb_drift)
            + len(short_descriptions)
            + sum(len(v) for v in lint.values())
        ),
    }
    findings["summary"]["severity_counts"] = severity

    # convert defaultdict
    findings["issues"] = dict(findings["issues"])

    # ---- Write file ----
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = OUT_DIR / f"eval_structural_{stamp}.json"
    out_path.write_text(json.dumps(findings, indent=2, default=str))

    # ---- Stdout summary ----
    print("=" * 60)
    print("STRUCTURAL EVAL SUMMARY")
    print("=" * 60)
    print(f"Disk SKILL.md files:  {findings['counts']['disk_skill_files']}")
    print(f"Disk parsed OK:       {findings['counts']['disk_skills_parsed']}")
    print(f"Registry entries:     {findings['counts']['registry_skills']}")
    print(f"Registry last_scan:   {findings['counts']['registry_last_scan']}")
    print()
    print("Critical issues:")
    print(f"  parse failures:                 {len(parse_failures)}")
    print(f"  missing required fields:        {len(missing_required)}")
    print(f"  duplicate names:                {len(duplicates_by_name)}")
    print(f"  on-disk not in registry:        {len(findings['issues']['on-disk-not-in-registry'])}")
    print(f"  in-registry not on-disk:        {len(findings['issues']['in-registry-not-on-disk'])}")
    print(f"  broken parent refs:             {len(broken_parent)}")
    print(f"  broken depends_on refs:         {len(broken_depends_on)}")
    print()
    print("Warnings:")
    print(f"  location drift:                 {len(location_mismatches)}")
    print(f"  referenced_by drift:            {len(rb_drift)}")
    print(f"  short descriptions (<60 chars): {len(short_descriptions)}")
    print()
    print("Description lint (ratchet warnings):")
    print(f"  not third person:               {len(lint['desc-voice-not-third-person'])}")
    print(f"  no trigger phrase:              {len(lint['desc-no-trigger-phrase'])}")
    print(f"  overlong (>1024 chars):         {len(lint['desc-overlong'])}")
    print(f"  sibling near-duplicates:        {len(lint['desc-sibling-near-duplicates'])}")
    print()
    print("Distributions:")
    print(f"  health_status: {dict(by_health)}")
    print(f"  status:        {dict(by_status)}")
    print(f"  auto_score:    {score_buckets}")
    print()
    print(f"Full report -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
