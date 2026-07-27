#!/usr/bin/env python3
"""Pin imperative Cloud Run deploy flags to the declarative service reference."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = (ROOT / ".github" / "workflows" / "deploy.yml").read_text()
SERVICE = (ROOT / "cloudrun" / "service.yaml").read_text()


def _workflow_names(flag: str) -> set[str]:
    match = re.search(rf'--{flag}="([^"]+)"', WORKFLOW)
    assert match, f"deploy.yml missing --{flag}"
    return {item.split("=", 1)[0] for item in match.group(1).split(",")}


def test_deploy_and_service_env_are_identical():
    workflow_names = _workflow_names("set-env-vars") | _workflow_names("set-secrets")
    service_names = set(re.findall(r"^\s+- name: ([A-Z][A-Z0-9_]*)$", SERVICE, re.MULTILINE))
    assert service_names == workflow_names, (
        f"Cloud Run config drift:\n"
        f"  workflow only: {sorted(workflow_names - service_names)}\n"
        f"  service only: {sorted(service_names - workflow_names)}"
    )


def test_public_runtime_is_strictly_read_only():
    assert "MCP_READ_ONLY=1" in WORKFLOW
    assert re.search(
        r"- name: MCP_READ_ONLY\s+value: \"1\"", SERVICE, re.MULTILINE
    )


def test_concurrency_and_instance_limit_are_pinned():
    assert "--concurrency=8" in WORKFLOW
    assert "--max-instances=1" in WORKFLOW
    assert "containerConcurrency: 8" in SERVICE
    assert 'autoscaling.knative.dev/maxScale: "1"' in SERVICE


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
