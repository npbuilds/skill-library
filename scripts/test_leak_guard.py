#!/usr/bin/env python3
"""Regression tests for leak-guard's empty and deletion-only diff handling."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "leak-guard.sh"
PRE_COMMIT_HOOK = ROOT / "hooks" / "pre-commit-stray-check.sh"


def run(cmd: list[str], cwd: Path, check: bool = True):
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def make_repo() -> Path:
    directory = Path(tempfile.mkdtemp())
    run(["git", "init", "-q"], directory)
    run(["git", "config", "user.email", "test@example.com"], directory)
    run(["git", "config", "user.name", "Test"], directory)
    terms = directory / "terms.txt"
    terms.write_text("forbidden-project\n")
    run(["git", "config", "leakguard.file", str(terms)], directory)
    baseline = directory / "safe.txt"
    baseline.write_text("safe machinery\n")
    run(["git", "add", "safe.txt"], directory)
    run(["git", "commit", "-qm", "baseline"], directory)
    return directory


def test_empty_staging_area_passes():
    repo = make_repo()
    result = run(["bash", str(HOOK), "staged"], repo, check=False)
    assert result.returncode == 0, result.stderr


def test_deletion_only_staged_diff_passes():
    repo = make_repo()
    (repo / "safe.txt").unlink()
    run(["git", "add", "-u"], repo)
    result = run(["bash", str(HOOK), "staged"], repo, check=False)
    assert result.returncode == 0, result.stderr


def test_private_term_is_blocked():
    repo = make_repo()
    (repo / "unsafe.txt").write_text("forbidden-project\n")
    run(["git", "add", "unsafe.txt"], repo)
    result = run(["bash", str(HOOK), "staged"], repo, check=False)
    assert result.returncode == 1
    assert "BLOCKED" in result.stderr


def test_pre_commit_hook_runs_leak_guard():
    repo = make_repo()
    hooks = repo / "hooks"
    hooks.mkdir()
    shutil.copy2(HOOK, hooks / HOOK.name)
    shutil.copy2(PRE_COMMIT_HOOK, hooks / PRE_COMMIT_HOOK.name)
    (repo / "README.md").write_text("forbidden-project\n")
    run(["git", "add", "README.md"], repo)
    result = run(
        ["bash", str(hooks / PRE_COMMIT_HOOK.name)],
        repo,
        check=False,
    )
    assert result.returncode == 1
    assert "BLOCKED" in result.stderr


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
