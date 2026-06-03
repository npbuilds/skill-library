#!/usr/bin/env python3
"""edits.py — bounded skill edits + edit proposers.

An Edit is a single bounded add/delete/replace span. `apply_edit` performs it on
a skill body; `edit_size` measures it against the textual learning-rate budget.

Proposers turn the lowest-scoring train rollouts into a candidate edit:
  - MockEditProposer  deterministic, draws from a curated pool of crisp
                      procedural recipes (the "good" moves), plus a neutral
                      rephrase and a harmful deletion so the val gate has
                      something to reject. Prioritizes the worst-scoring type.
  - RealEditProposer  prompts an LLM to return one bounded edit as JSON.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

# Textual learning-rate budget: cap how much a single edit can add per step.
MAX_EDIT_CHARS = 700
MAX_EDIT_LINES = 16


@dataclass
class Edit:
    id: str
    op: str                       # "add" | "replace" | "delete"
    text: str = ""                # add: inserted text; replace: replacement
    after: str = ""               # add: anchor substring to insert after
    find: str = ""                # replace/delete: target substring
    target: str | None = None     # task type this edit intends to help
    rationale: str = ""

    def summary(self) -> dict:
        return {
            "id": self.id, "op": self.op, "target": self.target,
            "rationale": self.rationale,
            "preview": (self.text or self.find)[:80].replace("\n", " "),
        }


def edit_size(edit: Edit) -> tuple[int, int]:
    """(added_chars, added_lines) charged against the learning-rate budget."""
    if edit.op == "delete":
        return 0, 0
    added = edit.text if edit.op == "add" else edit.text
    return len(added), added.count("\n") + 1


def within_budget(edit: Edit) -> bool:
    chars, lines = edit_size(edit)
    return chars <= MAX_EDIT_CHARS and lines <= MAX_EDIT_LINES


def apply_edit(body: str, edit: Edit) -> str | None:
    """Return the new body, or None if the edit could not be applied cleanly."""
    if edit.op == "add":
        block = ("\n" + edit.text.strip("\n") + "\n")
        if edit.after and edit.after in body:
            idx = body.index(edit.after) + len(edit.after)
            # advance to end of the anchor line
            nl = body.find("\n", idx)
            insert_at = len(body) if nl == -1 else nl
            return body[:insert_at] + "\n" + block + body[insert_at:]
        return body.rstrip("\n") + "\n" + block
    if edit.op == "replace":
        if edit.find and edit.find in body:
            return body.replace(edit.find, edit.text, 1)
        return None
    if edit.op == "delete":
        if edit.find and edit.find in body:
            return body.replace(edit.find, "", 1)
        return None
    return None


# ── Curated candidate pools (deterministic optimizer model), keyed by skill ────

RECIPE_ANCHOR = "Apply the appropriate solution concept:"

_GAME_POOL: list[Edit] = [
    Edit(
        id="recipe-strictly-dominant", op="add", target="strictly_dominant",
        after=RECIPE_ANCHOR,
        rationale="train rollouts mis-handle dominance: add a crisp rule.",
        text=(
            "#### Recipe — Strictly Dominant Strategy\n"
            "A strategy is strictly dominant when it yields a strictly higher payoff "
            "against each of the opponent's actions (it strictly dominates every "
            "alternative). Check each of your strategies against every opponent "
            "action; if none clears that bar for every action, answer \"none\"."
        ),
    ),
    Edit(
        id="recipe-mixed-nash", op="add", target="mixed_nash_2x2",
        after=RECIPE_ANCHOR,
        rationale="no procedure for mixed equilibria; add the indifference method.",
        text=(
            "#### Recipe — Mixed-Strategy Nash (2x2)\n"
            "To find a mixed equilibrium, make the opponent indifferent: choose your "
            "mixing probability so the opponent's expected payoff is the same across "
            "their actions (set expected payoffs equal and solve). Report p (prob the "
            "row player plays its first strategy) and q (prob the column player plays "
            "its first strategy)."
        ),
    ),
    Edit(
        id="recipe-zero-sum", op="add", target="zero_sum_value",
        after=RECIPE_ANCHOR,
        rationale="no value-of-game procedure; add the saddle-point method.",
        text=(
            "#### Recipe — Zero-Sum Value\n"
            "For a zero-sum game the value of the game is the saddle point: take each "
            "row's minimum and each column's maximum; when the maximin equals the "
            "minimax, that common number is the value to the row player."
        ),
    ),
    Edit(
        id="recipe-maximin", op="add", target="maximin",
        after=RECIPE_ANCHOR,
        rationale="no maximin/security procedure; add it.",
        text=(
            "#### Recipe — Maximin / Security Strategy\n"
            "A player's maximin (security level) strategy maximizes their guaranteed "
            "worst-case payoff: for each of your strategies take the minimum payoff "
            "over the opponent's actions, then pick the strategy with the largest "
            "such minimum."
        ),
    ),
    Edit(
        id="recipe-pareto", op="add", target="pareto",
        after=RECIPE_ANCHOR,
        rationale="no Pareto procedure; add the dominance test.",
        text=(
            "#### Recipe — Pareto-Optimal Outcomes\n"
            "An outcome is Pareto-optimal when no other outcome makes one player "
            "better off without making the other worse off. Enumerate the cells and "
            "discard any cell weakly dominated in both payoffs by another cell."
        ),
    ),
    # Neutral rephrase — adds no procedural capability, so the val gate rejects it.
    Edit(
        id="noise-empathy", op="add", target=None,
        after=RECIPE_ANCHOR,
        rationale="stylistic addition with no procedural content.",
        text=(
            "Strategic analysis benefits from clear communication and empathy for the "
            "stakeholders involved."
        ),
    ),
    # Harmful deletion — removes best-response guidance, dropping pure_nash; rejected.
    Edit(
        id="harmful-drop-bestresponse", op="delete", target=None,
        find="best-response analysis",
        rationale="careless deletion that would remove a working capability.",
    ),
]


# bluf-shaper: format-adherence. Anchored after the last process step so the
# recovered contract lands just before "## Failure Modes". The good edits
# re-introduce the output CONTRACT the ablated baseline is missing.
BLUF_ANCHOR = "state that explicitly:"

_BLUF_POOL: list[Edit] = [
    Edit(
        id="bluf-format-core", op="add", target="bluf", after=BLUF_ANCHOR,
        rationale="output has no required headers; add the exact BLUF contract block.",
        text=(
            "## Output Format — return EXACTLY this block, labels uppercase, in this order:\n"
            "BOTTOM LINE: [one sentence answer or recommendation]\n"
            "BACKGROUND:\n"
            "- [fact 1; minimum context]\n"
            "- [fact 2; only if essential]\n"
            "DISCUSSION:\n"
            "1. [strongest reason]\n"
            "2. [second-strongest]\n"
            "RECOMMENDATION: [specific action requested]"
        ),
    ),
    Edit(
        id="bluf-discipline", op="add", target="bluf", after=BLUF_ANCHOR,
        rationale="enforce the one-sentence / no-hedging / length sub-rules.",
        text=(
            "### Output discipline (mandatory)\n"
            "- BOTTOM LINE must be EXACTLY ONE sentence.\n"
            "- Never use hedging words (likely, probably, potentially, perhaps, "
            "possibly) in the bottom line.\n"
            "- BACKGROUND: at most 3 bullets. DISCUSSION: numbered, at most 5 points.\n"
            "- RECOMMENDATION must name a specific action, not \"we should consider\"."
        ),
    ),
    # Neutral — no contract content, so the val gate rejects it.
    Edit(
        id="bluf-noise", op="add", target=None, after=BLUF_ANCHOR,
        rationale="stylistic addition with no contract content.",
        text="Good communication respects the reader's time and builds trust.",
    ),
    # Harmful — tells the model headers are optional; would drop compliance.
    Edit(
        id="bluf-harmful-freeform", op="add", target=None, after=BLUF_ANCHOR,
        rationale="loosens the contract; should reduce compliance and be rejected.",
        text="Use whatever free-form structure feels natural; headers are optional.",
    ),
]

# scqa-formatter: shipped skill scores 80 — the lone failing check is the
# one-sentence ANSWER rule. One targeted emphasis edit should recover it.
_SCQA_POOL: list[Edit] = [
    Edit(
        id="scqa-one-sentence", op="add", target="scqa", after="## Output Format",
        rationale="model writes a multi-sentence ANSWER; enforce one sentence.",
        text=(
            "### Output discipline (mandatory)\n"
            "The ANSWER must be EXACTLY ONE sentence (a single terminal period). If it "
            "needs more, move the surplus into SUPPORTING — never let ANSWER become two "
            "sentences or a paragraph."
        ),
    ),
    Edit(
        id="scqa-noise", op="add", target=None, after="## Output Format",
        rationale="stylistic; no contract content.",
        text="Clear structure helps the reader follow your reasoning.",
    ),
]

# executive-distiller: shipped skill scores only 25 — the model omits/renames the
# exact INTRODUCTION (SCQA): / BODY: headers and the numbered body. Emphasize them.
_EXEC_POOL: list[Edit] = [
    Edit(
        id="exec-exact-headers", op="add", target="exec-memo", after="## Output Format",
        rationale="model deviates from the exact section labels; pin them down.",
        text=(
            "### Output discipline (mandatory — exact labels)\n"
            "Your output MUST use these EXACT uppercase section labels, in this order: "
            "`INTRODUCTION (SCQA):` (with Situation:, Complication:, Question:, Answer: "
            "inside), then `BODY:` containing 2-5 NUMBERED level-1 points (1., 2., 3.), "
            "then a `DISTILLATION METADATA` block (with Pyramid depth, MECE, Length). "
            "Do not rename, merge, or omit these headers."
        ),
    ),
    Edit(
        id="exec-noise", op="add", target=None, after="## Output Format",
        rationale="stylistic; no contract content.",
        text="Executive readers value clarity and brevity.",
    ),
]

POOLS = {
    "game-solver": _GAME_POOL,
    "bluf-shaper": _BLUF_POOL,
    "scqa-formatter": _SCQA_POOL,
    "executive-distiller": _EXEC_POOL,
}


class MockEditProposer:
    name = "mock"

    def __init__(self):
        import common  # skill name resolved here so the right pool is selected
        self._pool = list(POOLS.get(common.SKILL_NAME, _GAME_POOL))

    def propose(self, body: str, type_order: list[str],
                rejected: set[str], applied: set[str]) -> Edit | None:
        # Prioritize edits targeting the worst-scoring train types.
        for ttype in type_order:
            for e in self._pool:
                if e.target == ttype and e.id not in applied and e.id not in rejected:
                    return e
        # Then untargeted candidates (neutral / harmful) so the gate can reject them.
        for e in self._pool:
            if e.target is None and e.id not in applied and e.id not in rejected:
                return e
        return None


class RealEditProposer:
    name = "llm"

    def __init__(self, complete_fn):
        self._complete = complete_fn

    def propose(self, body: str, type_order: list[str],
                rejected: set[str], applied: set[str]) -> Edit | None:
        prompt = (
            "You are optimizing a SKILL.md. Propose ONE bounded edit (<=700 chars) "
            "that will most improve task accuracy on the weakest area.\n"
            f"Weakest task types (worst first): {type_order}\n"
            f"Already-rejected edit ids (do not repeat): {sorted(rejected)}\n"
            "Return JSON: {\"id\":..., \"op\":\"add|replace|delete\", \"after\":..., "
            "\"find\":..., \"text\":..., \"target\":..., \"rationale\":...}\n\n"
            "Current skill body:\n" + body
        )
        out = self._complete("You are a careful skill editor.", prompt)
        try:
            start, end = out.index("{"), out.rindex("}") + 1
            d = json.loads(out[start:end])
        except (ValueError, json.JSONDecodeError):
            return None
        if d.get("id") in rejected or d.get("id") in applied:
            return None
        return Edit(
            id=d.get("id", "llm-edit"), op=d.get("op", "add"), text=d.get("text", ""),
            after=d.get("after", ""), find=d.get("find", ""), target=d.get("target"),
            rationale=d.get("rationale", ""),
        )


def get_proposer(client):
    """Choose the edit proposer.

    SKILLOPT_PROPOSER overrides: 'mock' forces the curated candidate pool
    (bounded + reproducible — useful for a controlled A/B where only the
    rollout/grading backend changes); 'llm' forces the LLM proposer. Default:
    use the LLM proposer when a real rollout backend is selected, else mock.
    """
    choice = os.environ.get("SKILLOPT_PROPOSER", "").strip().lower()
    if choice == "mock":
        return MockEditProposer()
    if choice == "llm" and hasattr(client, "_complete"):
        return RealEditProposer(client._complete)
    if os.environ.get("SKILLOPT_LLM", "").lower() in ("anthropic", "cursor") and hasattr(client, "_complete"):
        return RealEditProposer(client._complete)
    return MockEditProposer()
