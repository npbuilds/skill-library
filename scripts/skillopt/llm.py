#!/usr/bin/env python3
"""llm.py — pluggable LLM access for rollouts and the rubric judge.

The pilot must run end-to-end even with no LLM API access, so everything is
written against a small interface and ships with a deterministic mock:

  SolverClient.rollout(skill_text, task) -> {"answer", "raw_text", "mode"}

Backends (auto-detected, override with SKILLOPT_LLM=anthropic|cursor|mock):
  - AnthropicSolver   real rollouts via the `anthropic` SDK (needs ANTHROPIC_API_KEY)
  - CursorAgentSolver real rollouts via the `cursor-agent` CLI (-p print mode)
  - MockSolver        deterministic; models "the skill confers capability":
                      a competent skill (see gametheory.COMPETENCE_MARKERS)
                      yields a correctly-solved answer, an incompetent skill
                      yields a naive (usually-wrong) guess.

The mock is what makes the optimization landscape real but reproducible: edits
that add a correct procedural recipe flip a task type from incompetent to
competent, which is exactly what the val gate rewards.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gametheory  # noqa: E402
from tasks import compose_prompt  # noqa: E402
from grader import parse_answer  # noqa: E402

SYSTEM_PREAMBLE = (
    "You are an expert game theorist. The following skill document is your "
    "operating procedure; follow it precisely.\n\n"
)


# ── Mock (default, no API needed) ──────────────────────────────────────────────

class MockSolver:
    """Deterministic solver whose accuracy depends on skill competence."""

    name = "mock"

    def rollout(self, skill_text: str, task: dict) -> dict:
        ttype = task["type"]
        competent = gametheory.is_competent(skill_text, ttype)
        if task["checker"] == "rubric":
            anchors = task.get("expect_contains", [])
            if competent:
                body = (
                    "Interpretation: " + "; ".join(anchors)
                    + ". The reasoning follows the skill's interpretation step."
                )
            else:
                body = "Here is a general comment without a structured method."
            return {"answer": "", "raw_text": body, "mode": "competent" if competent else "incompetent"}

        if competent:
            answer = gametheory.solve(task)
            mode = "competent"
        else:
            answer = gametheory.naive_guess(task)
            mode = "incompetent"
        raw = f"Reasoning per skill guidance ({mode}).\nANSWER: {json.dumps(answer)}"
        return {"answer": answer, "raw_text": raw, "mode": mode}

    def judge(self, task: dict, answer_text: str) -> float:
        # Deterministic keyword-coverage judge (used as rubric fallback in mock mode)
        anchors = task.get("expect_contains", [])
        if not anchors:
            return 0.0
        low = (answer_text or "").lower()
        return round(100.0 * sum(1 for a in anchors if a.lower() in low) / len(anchors), 1)


# ── Real backends ──────────────────────────────────────────────────────────────

class AnthropicSolver:
    name = "anthropic"

    def __init__(self, model: str | None = None):
        import anthropic  # type: ignore
        self._client = anthropic.Anthropic()
        self._model = model or os.environ.get("SKILLOPT_MODEL", "claude-3-5-sonnet-latest")

    def _complete(self, system: str, user: str) -> str:
        msg = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(block.text for block in msg.content if getattr(block, "type", "") == "text")

    def rollout(self, skill_text: str, task: dict) -> dict:
        text = self._complete(SYSTEM_PREAMBLE + skill_text, compose_prompt(task))
        return {"answer": parse_answer(text), "raw_text": text, "mode": "llm"}

    def judge(self, task: dict, answer_text: str) -> float:
        rubric = (
            "Score the following answer 0-100 for how well it satisfies these "
            f"required ideas: {task.get('expect_contains', [])}. "
            "Reply with only a number.\n\nANSWER:\n" + (answer_text or "")
        )
        out = self._complete("You are a strict grader.", rubric)
        m = __import__("re").search(r"\d+(\.\d+)?", out)
        return float(m.group(0)) if m else 0.0


class CursorAgentSolver:
    name = "cursor-agent"

    def __init__(self, model: str | None = None):
        self._bin = shutil.which("cursor-agent")
        if not self._bin:
            raise RuntimeError("cursor-agent not on PATH")
        self._model = model or os.environ.get("SKILLOPT_MODEL")
        # Read-only headless Q&A: --mode ask avoids tool/edit use (faster, safe),
        # --trust bypasses the workspace-trust prompt in headless mode.
        self._base = [self._bin, "-p", "--output-format", "text", "--trust", "--mode", "ask"]
        if self._model:
            self._base += ["--model", self._model]
        # Preflight so we fail loudly here instead of silently producing empty
        # rollouts (which would score 0 and look like a real run).
        probe = self._invoke("Reply with the single word: PONG", timeout=120)
        if probe.returncode != 0:
            raise RuntimeError(
                "cursor-agent is not usable: "
                + (probe.stderr.strip() or f"exited {probe.returncode}")
            )

    def _invoke(self, prompt: str, timeout: int = 240):
        return subprocess.run(
            self._base + [prompt], capture_output=True, text=True, timeout=timeout,
        )

    def _complete(self, system: str, user: str) -> str:
        proc = self._invoke(system + "\n\n" + user)
        if proc.returncode != 0:
            raise RuntimeError(f"cursor-agent rollout failed: {proc.stderr.strip()}")
        return proc.stdout

    def rollout(self, skill_text: str, task: dict) -> dict:
        text = self._complete(SYSTEM_PREAMBLE + skill_text, compose_prompt(task))
        return {"answer": parse_answer(text), "raw_text": text, "mode": "llm"}

    def judge(self, task: dict, answer_text: str) -> float:
        return MockSolver().judge(task, answer_text)


def get_solver_client():
    """Resolve a backend.

    An EXPLICIT choice (SKILLOPT_LLM=anthropic|cursor) fails loudly if that
    backend is unusable — it never silently falls back to the mock, so a
    blocked live run is impossible to mistake for a real one. Only pure
    auto-detection (no SKILLOPT_LLM set) falls back to the deterministic mock.
    """
    choice = os.environ.get("SKILLOPT_LLM", "").strip().lower()
    if choice == "mock":
        return MockSolver()
    if choice == "anthropic":
        return AnthropicSolver()  # raises if unavailable — intentional
    if choice == "cursor":
        return CursorAgentSolver()  # raises if unauthenticated — intentional
    # Auto-detect: prefer a real backend if a key is present, else mock.
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return AnthropicSolver()
        except Exception as e:  # pragma: no cover - depends on env
            print(f"[llm] anthropic unavailable ({e}); falling back to mock", file=sys.stderr)
    return MockSolver()
