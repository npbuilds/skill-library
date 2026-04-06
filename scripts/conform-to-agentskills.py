#!/usr/bin/env python3
"""
conform-to-agentskills.py
Convert skill library SKILL.md files to agentskills.io spec compliance.

Changes made:
  - tools: Read, Write  →  allowed-tools: Read Write  (comma → space, renamed)
  - Optionally injects metadata, license, compatibility fields

Usage:
  python3 conform-to-agentskills.py              # dry run (default)
  python3 conform-to-agentskills.py --apply      # write changes
  python3 conform-to-agentskills.py --apply --license MIT
  python3 conform-to-agentskills.py --apply --author yourname --version 1.0
  python3 conform-to-agentskills.py --apply --compatibility "Designed for Claude Code"
  python3 conform-to-agentskills.py --skill skills/worldbuilding/worldbuilding-orchestrator  # single skill
"""

import argparse
import os
import re
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).parent.parent / "skills"

# ─── Parsing ──────────────────────────────────────────────────────────────────

def split_frontmatter(text: str) -> tuple[str, str, str]:
    """Split file into (pre, frontmatter, body). Returns (None, None, text) if no frontmatter."""
    if not text.startswith("---"):
        return None, None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, None, text
    pre = "---\n"
    fm = text[4:end]          # content between opening and closing ---
    body = text[end + 4:]     # everything after closing ---
    return pre, fm, body


def convert_tools_field(frontmatter: str) -> tuple[str, str | None]:
    """
    Convert `tools: A, B, C` → `allowed-tools: A B C`.
    Returns (new_frontmatter, original_tools_value | None).
    """
    match = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        return frontmatter, None

    original = match.group(1).strip()
    # Split on commas, strip whitespace from each tool name
    tools = [t.strip() for t in original.split(",") if t.strip()]
    new_value = " ".join(tools)

    # Replace the tools: line with allowed-tools:
    new_fm = re.sub(
        r"^tools:\s*.+$",
        f"allowed-tools: {new_value}",
        frontmatter,
        flags=re.MULTILINE
    )
    return new_fm, original


def inject_optional_fields(
    frontmatter: str,
    license_val: str | None,
    author: str | None,
    version: str | None,
    compatibility: str | None,
) -> str:
    """Inject optional fields after the description block if not already present."""
    additions = []

    if license_val and "license:" not in frontmatter:
        additions.append(f"license: {license_val}")

    # Build metadata block
    meta_lines = []
    if author and "author:" not in frontmatter:
        meta_lines.append(f"  author: {author}")
    if version and "version:" not in frontmatter:
        meta_lines.append(f'  version: "{version}"')
    if meta_lines and "metadata:" not in frontmatter:
        additions.append("metadata:\n" + "\n".join(meta_lines))

    if compatibility and "compatibility:" not in frontmatter:
        additions.append(f"compatibility: {compatibility}")

    if not additions:
        return frontmatter

    # Insert after the last line of the description block
    # Find the end of the description field (handles multi-line > blocks)
    lines = frontmatter.splitlines()
    insert_after = -1
    in_description = False
    for i, line in enumerate(lines):
        if line.startswith("description:"):
            in_description = True
            insert_after = i
        elif in_description:
            # Multi-line description continues if line starts with whitespace
            if line.startswith(" ") or line.startswith("\t"):
                insert_after = i
            else:
                in_description = False

    if insert_after == -1:
        # Fallback: append before the end
        return frontmatter + "\n" + "\n".join(additions)

    lines_out = lines[: insert_after + 1] + additions + lines[insert_after + 1 :]
    return "\n".join(lines_out)


# ─── Processing ───────────────────────────────────────────────────────────────

def process_skill(
    skill_path: Path,
    apply: bool,
    license_val: str | None,
    author: str | None,
    version: str | None,
    compatibility: str | None,
) -> dict:
    """Process a single SKILL.md. Returns a result dict."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"path": skill_path, "status": "skip", "reason": "no SKILL.md"}

    original = skill_md.read_text(encoding="utf-8")
    pre, fm, body = split_frontmatter(original)

    if fm is None:
        return {"path": skill_path, "status": "skip", "reason": "no frontmatter"}

    # Convert tools field
    new_fm, tools_original = convert_tools_field(fm)

    # Inject optional fields
    new_fm = inject_optional_fields(new_fm, license_val, author, version, compatibility)

    new_text = pre + new_fm + "\n---" + body

    if new_text == original:
        return {"path": skill_path, "status": "unchanged"}

    changes = []
    if tools_original:
        tools_new = " ".join(t.strip() for t in tools_original.split(",") if t.strip())
        changes.append(f"  tools: {tools_original}")
        changes.append(f"  → allowed-tools: {tools_new}")
    if license_val and "license:" not in fm:
        changes.append(f"  + license: {license_val}")
    if author and "author:" not in fm:
        changes.append(f"  + metadata.author: {author}")
    if version and "version:" not in fm:
        changes.append(f"  + metadata.version: {version}")
    if compatibility and "compatibility:" not in fm:
        changes.append(f"  + compatibility: {compatibility}")

    if apply:
        skill_md.write_text(new_text, encoding="utf-8")

    return {
        "path": skill_path,
        "status": "changed" if apply else "would-change",
        "changes": changes,
    }


def find_skills(root: Path) -> list[Path]:
    """Recursively find all skill directories (containing SKILL.md)."""
    return sorted(p.parent for p in root.rglob("SKILL.md"))


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert skill library to agentskills.io spec compliance"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes (default is dry run)",
    )
    parser.add_argument(
        "--skill",
        metavar="PATH",
        help="Process a single skill directory instead of all skills",
    )
    parser.add_argument("--license", metavar="LICENSE", help="License to inject (e.g. MIT)")
    parser.add_argument("--author", metavar="AUTHOR", help="Author for metadata block")
    parser.add_argument("--version", metavar="VERSION", help="Version for metadata block")
    parser.add_argument(
        "--compatibility",
        metavar="TEXT",
        help='Compatibility note (e.g. "Designed for Claude Code")',
    )
    args = parser.parse_args()

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"\n{'='*60}")
    print(f"  agentskills.io Conformance Converter  [{mode}]")
    print(f"{'='*60}\n")

    if not args.apply:
        print("  ℹ  No changes will be written. Pass --apply to write.\n")

    # Determine target skills
    if args.skill:
        target = Path(args.skill)
        if not target.is_absolute():
            target = SKILLS_ROOT.parent / args.skill
        skills = [target]
    else:
        skills = find_skills(SKILLS_ROOT)

    print(f"  Skills found: {len(skills)}\n")

    results = {"unchanged": [], "changed": [], "skipped": []}

    for skill_path in skills:
        result = process_skill(
            skill_path,
            apply=args.apply,
            license_val=args.license,
            author=args.author,
            version=args.version,
            compatibility=args.compatibility,
        )
        rel = skill_path.relative_to(SKILLS_ROOT.parent)

        if result["status"] == "unchanged":
            results["unchanged"].append(rel)
        elif result["status"] in ("changed", "would-change"):
            results["changed"].append((rel, result.get("changes", [])))
            verb = "✓ Updated" if args.apply else "~ Would update"
            print(f"  {verb}: {rel}")
            for c in result.get("changes", []):
                print(f"         {c}")
        else:
            results["skipped"].append((rel, result.get("reason", "")))

    # Summary
    print(f"\n{'─'*60}")
    print(f"  Summary")
    print(f"{'─'*60}")
    n_changed = len(results["changed"])
    n_unchanged = len(results["unchanged"])
    n_skipped = len(results["skipped"])

    if args.apply:
        print(f"  ✓ Updated:   {n_changed}")
    else:
        print(f"  ~ Would update: {n_changed}")
    print(f"  ✓ Already compliant: {n_unchanged}")
    if n_skipped:
        print(f"  ⊘ Skipped:   {n_skipped}")

    if not args.apply and n_changed > 0:
        print(f"\n  Run with --apply to write {n_changed} change(s).")

    print()


if __name__ == "__main__":
    main()
