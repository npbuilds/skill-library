#!/usr/bin/env python3
"""contracts.py — deterministic OUTPUT-CONTRACT graders for format-adherence skills.

Unlike the game-theory grader (which checks a parsed answer), these score the
FULL rollout text for *structural compliance* with a skill's output contract:
required headers in the right order, one-sentence rules, length budgets,
numbered vs bulleted lists, banned hedging words, etc. Every check is a
regex/structural test — never fuzzy content quality. Each scorer returns a
0-100 compliance score plus a per-check breakdown.
"""
from __future__ import annotations

import json
import re

# Hedging words banned from a BLUF bottom line (the skill says: qualify in
# discussion, never in the bottom line).
_HEDGES = ("likely", "potentially", "we think", "maybe", "probably", "perhaps", "possibly")
_BULLET_RE = re.compile(r"^\s*[-*•]\s+\S")
_NUM_RE = re.compile(r"^\s*\d+\.\s+\S")

_BLUF_LABELS = ["BOTTOM LINE:", "BACKGROUND:", "DISCUSSION:", "RECOMMENDATION:"]


def _strip_md(line: str) -> str:
    """Drop leading markdown decoration (#, *, >, backticks, spaces)."""
    return line.lstrip("#*->` \t")


def _label_index(lines: list[str], label: str) -> int:
    for i, ln in enumerate(lines):
        if _strip_md(ln).startswith(label):
            return i
    return -1


def _section_lines(lines: list[str], start: int, all_header_idxs: list[int]) -> list[str]:
    nexts = [i for i in all_header_idxs if i > start]
    end = min(nexts) if nexts else len(lines)
    return lines[start + 1:end]


def _label_inline_value(line: str, label: str) -> str:
    s = _strip_md(line)
    return s.split(label, 1)[1].strip().strip("*` ").strip() if label in s else ""


def _sentence_count(text: str) -> int:
    parts = [p for p in re.split(r"[.!?]+", text) if p.strip()]
    return len(parts)


def score_bluf(text: str) -> dict:
    """Score BLUF output-contract compliance 0-100 with a per-check breakdown.

    Contract (from skills/binding-vow/bluf-shaper/SKILL.md Output Format):
      1. has BOTTOM LINE: header
      2. has BACKGROUND: header
      3. has DISCUSSION: header
      4. has RECOMMENDATION: header
      5. those four headers appear in that exact order
      6. bottom line is exactly ONE sentence
      7. bottom line contains NO hedging words
      8. BACKGROUND has 1-3 bullet lines (minimum context, not a memo)
      9. DISCUSSION has 1-5 NUMBERED (priority-ordered) points, not bullets
     10. RECOMMENDATION is a non-empty, non-vague specific action
    """
    text = text or ""
    lines = text.splitlines()
    idx = {lbl: _label_index(lines, lbl) for lbl in _BLUF_LABELS}
    header_idxs = [i for i in idx.values() if i >= 0]

    checks: dict[str, bool] = {}
    checks["has_bottom_line"] = idx["BOTTOM LINE:"] >= 0
    checks["has_background"] = idx["BACKGROUND:"] >= 0
    checks["has_discussion"] = idx["DISCUSSION:"] >= 0
    checks["has_recommendation"] = idx["RECOMMENDATION:"] >= 0

    present = [idx[l] for l in _BLUF_LABELS if idx[l] >= 0]
    checks["headers_in_order"] = (
        len(present) == 4 and present == sorted(present)
    )

    # Bottom line content = inline value on the header line + any continuation
    # lines up to the next header.
    if idx["BOTTOM LINE:"] >= 0:
        bl = _label_inline_value(lines[idx["BOTTOM LINE:"]], "BOTTOM LINE:")
        cont = _section_lines(lines, idx["BOTTOM LINE:"], header_idxs)
        bl_full = (bl + " " + " ".join(c.strip() for c in cont if c.strip())).strip()
        checks["bottom_line_one_sentence"] = _sentence_count(bl_full) == 1 and bool(bl_full)
        checks["bottom_line_no_hedging"] = bool(bl_full) and not any(h in bl_full.lower() for h in _HEDGES)
    else:
        checks["bottom_line_one_sentence"] = False
        checks["bottom_line_no_hedging"] = False

    if idx["BACKGROUND:"] >= 0:
        bg = _section_lines(lines, idx["BACKGROUND:"], header_idxs)
        bullets = [ln for ln in bg if _BULLET_RE.match(ln)]
        checks["background_1to3_bullets"] = 1 <= len(bullets) <= 3
    else:
        checks["background_1to3_bullets"] = False

    if idx["DISCUSSION:"] >= 0:
        ds = _section_lines(lines, idx["DISCUSSION:"], header_idxs)
        numbered = [ln for ln in ds if _NUM_RE.match(ln)]
        checks["discussion_numbered_1to5"] = 1 <= len(numbered) <= 5
    else:
        checks["discussion_numbered_1to5"] = False

    if idx["RECOMMENDATION:"] >= 0:
        rec = _label_inline_value(lines[idx["RECOMMENDATION:"]], "RECOMMENDATION:")
        cont = _section_lines(lines, idx["RECOMMENDATION:"], header_idxs)
        rec_full = (rec + " " + " ".join(c.strip() for c in cont if c.strip())).strip()
        vague = bool(re.search(r"\b(should consider|we should|consider whether)\b", rec_full.lower()))
        checks["recommendation_specific"] = bool(rec_full) and not vague
    else:
        checks["recommendation_specific"] = False

    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    return {
        "score": round(100.0 * passed / total, 1),
        "passed_count": passed,
        "total": total,
        "checks": checks,
    }


# ── Declarative contract engine ────────────────────────────────────────────────
# A contract is `{"sections": [labels...], "checks": [check, ...]}`. Each check is
# a dict `{"type": <checker>, ...params}` and may carry `"section": <label>` to
# scope the check to that section's text. Score = 100 * passed / total_checks.
# This lets a new skill be added by authoring tasks.yaml alone — no Python.

def _section_text(label: str | None, lines: list[str], idx: dict, header_idxs: list[int]) -> str:
    """Joined text of a section: inline value after the label + continuation lines."""
    if label is None:
        return "\n".join(lines)
    i = idx.get(label, -1)
    if i < 0:
        return ""
    inline = _label_inline_value(lines[i], label)
    cont = _section_lines(lines, i, header_idxs)
    return (inline + " " + " ".join(c.strip() for c in cont if c.strip())).strip()


def _section_raw_lines(label: str, lines: list[str], idx: dict, header_idxs: list[int]) -> list[str]:
    i = idx.get(label, -1)
    return _section_lines(lines, i, header_idxs) if i >= 0 else []


def _extract_json(text: str, source: str = "auto"):
    """Best-effort JSON extraction: fenced ```json block, else first {...} span."""
    if source in ("fenced", "auto"):
        m = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1).strip())
            except (json.JSONDecodeError, ValueError):
                if source == "fenced":
                    return None
    try:
        start, end = text.index("{"), text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        return None


_TYPE_MAP = {
    "str": str, "string": str, "int": int, "integer": int, "float": float,
    "number": (int, float), "bool": bool, "boolean": bool,
    "list": list, "array": list, "dict": dict, "object": dict,
}


def _matches(patterns, text, regex: bool) -> bool:
    """True if ANY pattern matches `text`."""
    low = text if regex else text.lower()
    for p in patterns:
        if regex:
            if re.search(p, text):
                return True
        elif str(p).lower() in low:
            return True
    return False


# Each checker: fn(ctx) -> bool. ctx = dict(chk, scoped, full, lines, idx, header_idxs).
def _c_sections_in_order(ctx) -> bool:
    labels = ctx["chk"].get("labels") or ctx["sections"]
    present = [ctx["idx"].get(l, -1) for l in labels]
    return all(i >= 0 for i in present) and present == sorted(present)


def _c_section_present(ctx) -> bool:
    return ctx["idx"].get(ctx["chk"]["label"], -1) >= 0


def _c_json_valid(ctx) -> bool:
    chk = ctx["chk"]
    obj = _extract_json(ctx["scoped"], chk.get("source", "auto"))
    if obj is None:
        return False
    for key in chk.get("required_keys", []):
        if not isinstance(obj, dict) or key not in obj:
            return False
    for key, tname in (chk.get("types") or {}).items():
        pytype = _TYPE_MAP.get(tname)
        if pytype is None or not isinstance(obj.get(key), pytype):
            return False
    return True


def _c_length(ctx) -> bool:
    chk = ctx["chk"]
    txt = ctx["scoped"]
    unit = chk.get("unit", "words")
    n = len(txt.split()) if unit == "words" else len(txt)
    if "min" in chk and n < chk["min"]:
        return False
    if "max" in chk and n > chk["max"]:
        return False
    return True


def _c_one_sentence(ctx) -> bool:
    return bool(ctx["scoped"]) and _sentence_count(ctx["scoped"]) == 1


def _c_must_include(ctx) -> bool:
    chk = ctx["chk"]
    pats = chk.get("patterns", [])
    regex = chk.get("regex", False)
    if chk.get("mode", "all") == "any":
        return _matches(pats, ctx["scoped"], regex)
    return all(_matches([p], ctx["scoped"], regex) for p in pats)


def _c_must_not_include(ctx) -> bool:
    return not _matches(ctx["chk"].get("patterns", []), ctx["scoped"], ctx["chk"].get("regex", False))


def _c_list_items(ctx) -> bool:
    chk = ctx["chk"]
    label = chk.get("section")
    raw = _section_raw_lines(label, ctx["lines"], ctx["idx"], ctx["header_idxs"]) if label else ctx["lines"]
    style = chk.get("style", "any")
    rx = {"bullet": _BULLET_RE, "numbered": _NUM_RE}.get(style)
    if rx is not None:
        count = sum(1 for ln in raw if rx.match(ln))
    else:
        count = sum(1 for ln in raw if _BULLET_RE.match(ln) or _NUM_RE.match(ln))
    if "min" in chk and count < chk["min"]:
        return False
    if "max" in chk and count > chk["max"]:
        return False
    return True


def _c_non_empty(ctx) -> bool:
    return bool(ctx["scoped"].strip())


CHECKS = {
    "sections_in_order": _c_sections_in_order,
    "section_present": _c_section_present,
    "json_valid": _c_json_valid,
    "length": _c_length,
    "one_sentence": _c_one_sentence,
    "must_include": _c_must_include,
    "must_not_include": _c_must_not_include,
    "list_items": _c_list_items,
    "non_empty": _c_non_empty,
}


def evaluate_contract(text: str, contract: dict) -> dict:
    """Compose declared checks into a 0-100 score with a per-check breakdown."""
    text = text or ""
    lines = text.splitlines()
    sections = contract.get("sections", [])
    idx = {lbl: _label_index(lines, lbl) for lbl in sections}
    header_idxs = sorted(i for i in idx.values() if i >= 0)

    results: dict[str, bool] = {}
    for n, chk in enumerate(contract.get("checks", [])):
        cid = chk.get("id") or f"{chk.get('type', 'check')}#{n}"
        label = chk.get("section")
        # A required section that is absent => non-compliant for that check.
        if label is not None and idx.get(label, -1) < 0:
            results[cid] = False
            continue
        ctx = {
            "chk": chk,
            "scoped": _section_text(label, lines, idx, header_idxs),
            "full": text,
            "lines": lines,
            "idx": idx,
            "header_idxs": header_idxs,
            "sections": sections,
        }
        fn = CHECKS.get(chk.get("type"))
        results[cid] = bool(fn(ctx)) if fn else False

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    return {
        "score": round(100.0 * passed / total, 1) if total else 0.0,
        "passed_count": passed,
        "total": total,
        "checks": results,
    }


# Named declarative contracts reusable via `type:`/`contract:` shorthand.
NAMED_CONTRACTS: dict[str, dict] = {}

# Legacy hard-coded scorers (kept so existing skills grade byte-identically).
SCORERS = {"bluf": score_bluf}


def score_contract(task: dict, text: str) -> dict:
    """Resolve a task's contract and score it.

    Priority: inline declarative `contract` block > named declarative contract
    > legacy hard-coded scorer keyed by `type`.
    """
    contract = task.get("contract")
    if isinstance(contract, dict) and "checks" in contract:
        return evaluate_contract(text, contract)
    if isinstance(contract, str) and contract in NAMED_CONTRACTS:
        return evaluate_contract(text, NAMED_CONTRACTS[contract])
    fn = SCORERS.get(task.get("type"))
    if fn is not None:
        return fn(text)
    return {"score": 0.0, "passed_count": 0, "total": 0, "checks": {}}


if __name__ == "__main__":
    import json as _json
    good = (
        "BOTTOM LINE: Approve the $2M Q3 onboarding rebuild.\n\n"
        "BACKGROUND:\n- Churn rose to 12%.\n- Onboarding is the top driver.\n\n"
        "DISCUSSION:\n1. Activation window is the leak.\n2. Fix is scoped at 4 eng-quarters.\n\n"
        "RECOMMENDATION: Approve $2M and reallocate 3 engineers this week."
    )
    print("score_bluf (legacy):", score_bluf(good)["score"])
    # Same contract expressed declaratively — should also score 100.
    decl = {
        "sections": ["BOTTOM LINE:", "BACKGROUND:", "DISCUSSION:", "RECOMMENDATION:"],
        "checks": [
            {"type": "sections_in_order"},
            {"type": "one_sentence", "section": "BOTTOM LINE:"},
            {"type": "must_not_include", "section": "BOTTOM LINE:",
             "patterns": ["likely", "probably", "potentially", "perhaps", "possibly"]},
            {"type": "list_items", "section": "BACKGROUND:", "style": "bullet", "min": 1, "max": 3},
            {"type": "list_items", "section": "DISCUSSION:", "style": "numbered", "min": 1, "max": 5},
            {"type": "non_empty", "section": "RECOMMENDATION:"},
        ],
    }
    print("evaluate_contract (declarative):", _json.dumps(evaluate_contract(good, decl), indent=2))
