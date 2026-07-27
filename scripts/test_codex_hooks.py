#!/usr/bin/env python3
"""Contract tests for the Codex apply_patch skill watcher hook."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HANDLER_PATH = ROOT / "hooks" / "codex-skill-file-watcher.py"

spec = importlib.util.spec_from_file_location("codex_skill_hook", HANDLER_PATH)
assert spec and spec.loader
handler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handler)


def test_hook_configuration_is_single_and_codex_native():
    config = json.loads((ROOT / ".codex" / "hooks.json").read_text())
    hooks = config["hooks"]["PostToolUse"]
    assert len(hooks) == 1
    assert "apply_patch" in hooks[0]["matcher"]
    commands = [hook["command"] for hook in hooks[0]["hooks"]]
    assert len(commands) == 1
    assert "codex-skill-file-watcher.py" in commands[0]
    assert "jq" not in commands[0]
    assert "tool_input.file_path" not in commands[0]


def test_extracts_all_unique_existing_skill_files_from_patch():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        first = root / "skills" / "design" / "alpha" / "SKILL.md"
        second = root / "skills" / "data" / "beta" / "SKILL.md"
        first.parent.mkdir(parents=True)
        second.parent.mkdir(parents=True)
        first.write_text("# Alpha\n")
        second.write_text("# Beta\n")
        payload = {
            "tool_input": {
                "command": (
                    "*** Begin Patch\n"
                    "*** Update File: skills/design/alpha/SKILL.md\n"
                    "*** Update File: skills/design/alpha/SKILL.md\n"
                    "*** Add File: skills/data/beta/SKILL.md\n"
                    "*** Delete File: skills/old/gone/SKILL.md\n"
                    "*** Update File: docs/not-a-skill.md\n"
                    "*** End Patch\n"
                )
            }
        }
        assert handler.extract_skill_paths(payload, root) == [
            first.resolve(),
            second.resolve(),
        ]


def test_supports_legacy_file_path_and_rejects_outside_repo():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        skill = root / "skills" / "infra" / "gamma" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Gamma\n")
        payload = {"tool_input": {"file_path": str(skill)}}
        assert handler.extract_skill_paths(payload, root) == [skill.resolve()]
        outside = {"tool_input": {"file_path": "/tmp/SKILL.md"}}
        assert handler.extract_skill_paths(outside, root) == []


def main() -> None:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✓ {test.__name__}")
        except Exception as exc:
            print(f"  ✗ {test.__name__}: {exc}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
