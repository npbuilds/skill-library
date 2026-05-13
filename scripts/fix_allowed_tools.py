#!/usr/bin/env python3
"""fix_allowed_tools.py — Add 'allowed-tools: Read' to Mentor suite SKILL.md
files that are missing it. Idempotent.

Inserts after 'compatibility: Designed for Claude Code' line, matching the
shape used by the rest of the skill library.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUITE = ROOT / "skills" / "professional-development"

INSERT_LINE = "allowed-tools: Read"


def fix_file(path: Path) -> str:
    text = path.read_text()
    if not text.startswith("---\n"):
        return "skip:no-frontmatter"
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return "skip:unterminated-frontmatter"

    fm_block = text[4:end]
    if "allowed-tools" in fm_block:
        return "skip:already-present"

    # Insert after the 'compatibility:' line
    lines = fm_block.split("\n")
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and line.startswith("compatibility:"):
            new_lines.append(INSERT_LINE)
            inserted = True
    if not inserted:
        # Fallback: append before end of frontmatter
        new_lines.append(INSERT_LINE)

    new_fm = "\n".join(new_lines)
    new_text = "---\n" + new_fm + text[end:]
    path.write_text(new_text)
    return "fixed"


def main():
    files = sorted(SUITE.rglob("SKILL.md"))
    counts = {"fixed": 0, "skip:already-present": 0, "skip:no-frontmatter": 0, "skip:unterminated-frontmatter": 0}
    for p in files:
        result = fix_file(p)
        counts[result] = counts.get(result, 0) + 1
        if result != "skip:already-present":
            print(f"  {result}: {p.relative_to(ROOT)}")

    print()
    print(f"Total: {sum(counts.values())} | Fixed: {counts['fixed']} | Already present: {counts['skip:already-present']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
