#!/usr/bin/env python3
"""Route Codex apply_patch hook events to the existing skill watcher."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


PATCH_PATH_RE = re.compile(
    r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$",
    re.MULTILINE,
)


def extract_skill_paths(payload: dict, repo_root: Path) -> list[Path]:
    """Return unique, existing skills/**/SKILL.md paths affected by a hook."""
    tool_input = payload.get("tool_input") or {}
    candidates: list[str] = []

    command = tool_input.get("command")
    if isinstance(command, str):
        for match in PATCH_PATH_RE.finditer(command):
            candidates.append(match.group(1) or match.group(2))

    # Retain compatibility with Edit/Write-style hook payloads.
    file_path = tool_input.get("file_path")
    if isinstance(file_path, str) and file_path:
        candidates.append(file_path)

    results: list[Path] = []
    seen: set[Path] = set()
    root = repo_root.resolve()
    for raw in candidates:
        path = Path(raw.strip())
        path = path if path.is_absolute() else root / path
        resolved = path.resolve()
        try:
            relative = resolved.relative_to(root)
        except ValueError:
            continue
        parts = relative.parts
        if (
            len(parts) >= 4
            and parts[0] == "skills"
            and parts[-1] == "SKILL.md"
            and resolved.exists()
            and resolved not in seen
        ):
            results.append(resolved)
            seen.add(resolved)
    return results


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0

    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return 0

    root = Path(completed.stdout.strip())
    watcher = root / "hooks" / "skill-file-watcher.sh"
    for skill_path in extract_skill_paths(payload, root):
        subprocess.run(
            ["bash", str(watcher), str(skill_path)],
            cwd=root,
            check=False,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
