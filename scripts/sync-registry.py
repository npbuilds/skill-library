#!/usr/bin/env python3
"""sync-registry.py — Discover new skills on disk and add them to registry.json.

Usage:
    python3 scripts/sync-registry.py              # dry-run (shows what would change)
    python3 scripts/sync-registry.py --apply       # actually update registry.json

This script:
  1. Walks skills/ for every SKILL.md
  2. Extracts metadata (name, description, type) from heterogeneous formats
  3. Infers parent/domain/subdomain from directory structure
  4. Adds missing entries to registry.json
  5. Flags registry entries whose files no longer exist on disk
  6. Reports location mismatches for existing entries
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"

SKIP_DIRS = {".obsidian", "references", "agents", "examples"}

# ── Metadata extraction ────────────────────────────────────────────────

def extract_yaml_frontmatter(text: str) -> dict | None:
    """Extract YAML frontmatter between --- delimiters using regex (no PyYAML dep)."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    result = {}
    block = m.group(1)
    # Handle multi-line description (with > or |). The trailing newline on
    # the final line is optional — outer frontmatter regex consumes the \n
    # before the closing ---, so the last description line lacks one.
    desc_match = re.search(r"^description:\s*[>|]\s*\n((?:[ \t]+.+(?:\n|$))+)", block, re.MULTILINE)
    if desc_match:
        result["description"] = " ".join(
            line.strip() for line in desc_match.group(1).strip().split("\n")
        )
    for line in block.split("\n"):
        kv = re.match(r"^(\w[\w-]*):\s+(.+)$", line)
        if kv:
            key, val = kv.group(1).strip(), kv.group(2).strip()
            if key == "description" and "description" in result:
                continue  # Already handled multi-line
            result[key] = val
    return result if result else None


def extract_inline_metadata(text: str) -> dict:
    """Extract metadata from inline patterns like '## skill-metadata' blocks or bold labels."""
    meta = {}

    # Pattern 1: ## skill-metadata block with "- key: value" lines
    m = re.search(r"## skill-metadata\s*\n((?:- .+\n)+)", text)
    if m:
        for line in m.group(1).strip().split("\n"):
            kv = re.match(r"- ([\w-]+):\s*(.+)", line)
            if kv:
                key = kv.group(1).strip()
                val = kv.group(2).strip()
                if key == "skill-type":
                    meta["type"] = val
                elif key == "skill-id":
                    meta["skill_id"] = val
                elif key == "parent":
                    meta["parent_id"] = val

    # Pattern 2: **Type:** value  /  **Suite:** value
    for pattern, field in [
        (r"\*\*Type:\*\*\s*(\w+)", "type"),
        (r"\*\*Suite:\*\*\s*(\w+)", "suite"),
        (r"\*\*Skill Type\*\*\s*\n\*\*(\w+)\*\*", "type"),
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            meta[field] = m.group(1).strip().lower()

    # Pattern 3: ## Skill Type\n**Knowledge**
    m = re.search(r"## Skill Type\s*\n\*\*(\w+)\*\*", text)
    if m:
        meta["type"] = m.group(1).strip().lower()

    # Extract description from ## description or ## Description section
    m = re.search(r"## [Dd]escription\s*\n(.+?)(?:\n##|\n---|\Z)", text, re.DOTALL)
    if m:
        desc = m.group(1).strip().split("\n")[0].strip()
        if desc:
            meta["description"] = desc

    return meta


def extract_description_from_header(text: str) -> str | None:
    """Fallback: grab first paragraph after the H1 header."""
    lines = text.split("\n")
    past_h1 = False
    for line in lines:
        if line.startswith("# ") and not past_h1:
            past_h1 = True
            continue
        if past_h1 and line.strip():
            # Skip if it's another header or metadata
            if line.startswith("#") or line.startswith("**") or line.startswith("---"):
                continue
            return line.strip()[:200]
    return None


def compute_metrics(text: str, skill_dir: Path) -> dict:
    """Compute the full canonical metrics block — schema mirrors
    analyze-skill.sh so downstream scorers (mcp-server/shared.py,
    autoresearch.py) see identical keys regardless of source.

    body_words counts body only (frontmatter excluded). The legacy
    body_words = len(full_text) bug is fixed here."""
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = text[fm_match.end():]
    else:
        frontmatter = ""
        body = text

    all_words = text.split()
    body_words = body.split()

    # description_words: words in the description: field, mirroring analyze-skill.sh
    desc_words = 0
    capture = False
    for line in frontmatter.split("\n"):
        if re.match(r"^description:", line):
            capture = True
            value = re.sub(r"^description:\s*[>|]?\s*", "", line)
            desc_words += len(value.split())
            continue
        if capture and re.match(r"^[A-Za-z_-]+:", line):
            break
        if capture:
            desc_words += len(line.split())

    # Section count: ## headings outside fenced code blocks (only body)
    section_count = 0
    in_code = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if not in_code and line.startswith("## "):
            section_count += 1

    def _count(subdir: str) -> int:
        d = skill_dir / subdir
        return sum(1 for _ in d.iterdir() if _.is_file() and _.name != ".gitkeep") if d.is_dir() else 0

    # Token estimate is bytes/4 (matches analyze-skill.sh's wc -c, which
    # counts bytes). UTF-8 multi-byte chars (em-dashes, curly quotes) need
    # the byte length, not Python's char count, to stay in sync.
    body_chars = len(body.encode("utf-8"))
    est_tokens_body = body_chars // 4
    est_tokens_metadata = (desc_words * 13 + 9) // 10
    est_tokens_total = est_tokens_metadata + est_tokens_body

    return {
        "word_count": len(all_words),
        "body_words": len(body_words),
        "description_words": desc_words,
        "section_count": section_count,
        "reference_files": _count("references"),
        "example_files": _count("examples"),
        "script_files": _count("scripts"),
        "template_files": _count("templates"),
        "estimated_tokens_metadata": est_tokens_metadata,
        "estimated_tokens_body": est_tokens_body,
        "estimated_tokens_total": est_tokens_total,
    }


# ── Structural inference ───────────────────────────────────────────────

TYPE_KEYWORDS = {
    "orchestrator": "orchestrator",
    "director": "director",
    "observer": "observer",
    "action": "action",
    "knowledge": "knowledge",
    "agent": "action",
}


def infer_type(name: str, text: str, meta: dict) -> str:
    """Infer skill type from metadata, name, or content."""
    # Explicit metadata wins
    if "type" in meta:
        t = meta["type"].lower()
        return TYPE_KEYWORDS.get(t, t)

    # Name-based inference
    for keyword, stype in TYPE_KEYWORDS.items():
        if keyword in name:
            return stype

    # Content-based inference
    text_lower = text.lower()
    if "routing table" in text_lower or "child skills" in text_lower:
        return "director"
    if "## delegate" in text_lower or "## phase" in text_lower:
        return "orchestrator"

    return "knowledge"


def infer_structure(skill_path: Path) -> dict:
    """Infer domain, subdomain, parent from directory structure."""
    rel = skill_path.relative_to(SKILLS_DIR)
    parts = list(rel.parts[:-1])  # Remove SKILL.md

    info = {"domain": None, "subdomain": None, "parent": None}

    if len(parts) >= 1:
        info["domain"] = parts[0]
    if len(parts) >= 3:
        info["subdomain"] = parts[1]
        info["parent"] = parts[-2]  # Direct parent directory
    elif len(parts) == 2:
        # Could be domain/skill or domain/subdomain
        info["parent"] = parts[0] if parts[0] != parts[-1] else None

    return info


# ── Main sync logic ────────────────────────────────────────────────────

def discover_skills() -> dict[str, dict]:
    """Walk disk and return {name: entry_data} for every SKILL.md found."""
    discovered = {}

    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        skill_dir = skill_md.parent

        # Skip meta/hidden directories
        if any(part in SKIP_DIRS for part in skill_md.relative_to(SKILLS_DIR).parts[:-1]):
            continue

        rel_path = str(skill_md.relative_to(PROJECT_ROOT))
        text = skill_md.read_text(errors="replace")

        # Extract metadata from all formats
        yaml_meta = extract_yaml_frontmatter(text) or {}
        inline_meta = extract_inline_metadata(text)
        structure = infer_structure(skill_md)

        # Skill key: prefer frontmatter `name` (handles non-conventional layouts
        # like skills/_meta/SKILL.md → sentinel-prime), fall back to directory.
        skill_name = (yaml_meta.get("name") or "").strip() or skill_dir.name

        # Merge: YAML > inline > inferred
        description = (
            yaml_meta.get("description", "").strip()
            or inline_meta.get("description", "")
            or extract_description_from_header(text)
            or f"{skill_name} skill"
        )

        skill_type = infer_type(skill_name, text, {**inline_meta, **yaml_meta})
        metrics = compute_metrics(text, skill_dir)

        # Build tags
        tags = []
        if structure["domain"]:
            tags.append(f"domain:{structure['domain']}")
        if structure["subdomain"]:
            tags.append(f"subdomain:{structure['subdomain']}")
        tags.append(f"layer:{skill_type}")

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        discovered[skill_name] = {
            "name": skill_name,
            "description": description,
            "location": rel_path,
            "plugin": f"skill-{structure['domain']}" if structure["domain"] else "skill-infra",
            "type": skill_type,
            "source": "self",
            "context_mode": "inline",
            "invocation": "both",
            "version": "1.0.0",
            "metrics": metrics,
            "health_status": "healthy",
            "issues": [],
            "last_checked": f"{today}T00:00:00Z",
            "status": "active",
            "deprecated_date": None,
            "replacement_skill": None,
            "deprecation_reason": None,
            "auto_score": 50,  # Default score, needs calibration
            "manual_rating": None,
            "manual_notes": None,
            "composite_score": 50,
            "depends_on": [],
            "referenced_by": [],
            "shares_references_with": [],
            "forked_from": None,
            "forked_into": [],
            "tags": tags,
            "created": today,
            "last_modified": today,
            "changelog": [
                {
                    "date": today,
                    "action": "created",
                    "note": "Auto-discovered by sync-registry.py",
                }
            ],
            "parent": structure.get("parent"),
        }

    return discovered


def sync(apply: bool = False) -> None:
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    existing = registry["skills"]
    discovered = discover_skills()

    # ── Find new skills (on disk, not in registry) ──
    new_names = sorted(set(discovered) - set(existing))
    # ── Find ghosts (in registry, not on disk) ──
    ghost_names = []
    for name, entry in existing.items():
        loc = entry.get("location", "")
        full = PROJECT_ROOT / loc
        if not full.exists():
            ghost_names.append(name)
    # ── Find location mismatches ──
    mismatches = []
    for name in set(discovered) & set(existing):
        disk_loc = discovered[name]["location"]
        reg_loc = existing[name].get("location", "")
        if disk_loc != reg_loc:
            mismatches.append((name, reg_loc, disk_loc))

    # ── Find description / metrics drift on existing entries ──
    drift_desc: list[tuple[str, str, str]] = []
    drift_metrics: list[str] = []
    for name in set(discovered) & set(existing):
        cur = existing[name]
        new = discovered[name]
        cur_desc = (cur.get("description") or "").strip()
        new_desc = (new.get("description") or "").strip()
        if new_desc and cur_desc != new_desc:
            drift_desc.append((name, cur_desc, new_desc))
        if cur.get("metrics") != new.get("metrics"):
            drift_metrics.append(name)

    # ── Report ──
    print(f"Registry: {len(existing)} skills")
    print(f"On disk:  {len(discovered)} skills")
    print()

    if new_names:
        print(f"NEW ({len(new_names)}) — will be added:")
        for n in new_names:
            t = discovered[n]["type"]
            print(f"  + {n:<30s} [{t:<12s}] {discovered[n]['location']}")
    else:
        print("No new skills to add.")

    print()
    if ghost_names:
        print(f"GHOSTS ({len(ghost_names)}) — in registry but file missing:")
        for n in sorted(ghost_names):
            print(f"  ! {n:<30s} {existing[n].get('location', '?')}")
    else:
        print("No ghost entries.")

    print()
    if mismatches:
        print(f"LOCATION MISMATCHES ({len(mismatches)}):")
        for name, old, new in sorted(mismatches):
            print(f"  ~ {name}")
            print(f"      registry: {old}")
            print(f"      disk:     {new}")
    else:
        print("No location mismatches.")

    print()
    if drift_desc:
        print(f"DESCRIPTION DRIFT ({len(drift_desc)}):")
        for name, old, new in sorted(drift_desc)[:5]:
            print(f"  ~ {name}: {len(old)} → {len(new)} chars")
        if len(drift_desc) > 5:
            print(f"    ... and {len(drift_desc) - 5} more")
    if drift_metrics:
        print(f"METRICS DRIFT ({len(drift_metrics)} entries will be refreshed)")

    # ── Apply changes ──
    if apply:
        print("\n── Applying changes ──")
        for n in new_names:
            existing[n] = discovered[n]
            print(f"  Added: {n}")

        for name, old, new in mismatches:
            existing[name]["location"] = new
            print(f"  Fixed location: {name}")

        for name, _, new_desc in drift_desc:
            existing[name]["description"] = new_desc
        if drift_desc:
            print(f"  Refreshed description on {len(drift_desc)} entries")

        for name in drift_metrics:
            existing[name]["metrics"] = discovered[name]["metrics"]
        if drift_metrics:
            print(f"  Refreshed metrics on {len(drift_metrics)} entries")

        # Re-derive network.domains from on-disk paths so renames
        # (e.g., meta → _meta) propagate automatically.
        new_domains: dict[str, list[str]] = {}
        for name, entry in existing.items():
            parts = (entry.get("location") or "").split("/")
            if len(parts) >= 3 and parts[0] == "skills":
                new_domains.setdefault(parts[1], []).append(name)
        registry.setdefault("network", {})["domains"] = {
            dom: sorted(set(names)) for dom, names in sorted(new_domains.items())
        }
        print(f"  Re-derived network.domains: {len(new_domains)} domains")

        # Update timestamp
        registry["last_scan"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
            f.write("\n")

        print(
            f"\nRegistry updated: {len(new_names)} added, "
            f"{len(mismatches)} locations fixed, "
            f"{len(drift_desc)} descriptions refreshed, "
            f"{len(drift_metrics)} metrics refreshed."
        )
        if ghost_names:
            print(f"NOTE: {len(ghost_names)} ghost(s) left in place — review manually:")
            for n in sorted(ghost_names):
                print(f"  ! {n}")
    else:
        total_changes = (
            len(new_names) + len(mismatches) + len(drift_desc) + len(drift_metrics)
        )
        if total_changes:
            print(f"\nDry run complete. {total_changes} change(s) pending.")
            print("Run with --apply to update registry.json")
        else:
            print("\nRegistry is in sync.")


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    sync(apply=apply)
