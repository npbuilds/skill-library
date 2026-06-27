#!/usr/bin/env python3
"""
score-validity.py — grade the whole-story-judge against the validity set, in BOTH directions:
let-a-broken-whole-through (false-pass) and reject-a-sound-one (false-fail, e.g. wrongly failing an
earned subversion — a gun deliberately not fired). Mirrors the other critic harnesses; the scorer
is domain-agnostic.

Each item has fail_passage (should FAIL) and pass_passage (should PASS), tagged by `kind` (the
macro dimension under test). Run the judge BLIND on each skeleton, record PASS/FAIL on the target
dimension into a verdicts JSON, then this scorer compares against the gold labels.

Headline metrics:
  - DROPPED-SETUP TOLERANCE = false-pass rate (passed a structurally broken whole) — lower is better.
  - MACRO CONFORMITY = false-fail rate on subversion-trap (failed an earned subversion).
  - overall false-pass / false-fail, plus a per-kind breakdown.

Usage:
    python3 score-validity.py VERDICTS.json [--set validity-set.yaml]
                              [--max-false-pass 0.0] [--max-false-fail 0.0]

VERDICTS.json shape:
    { "payoff-01": {"fail_passage": "FAIL", "pass_passage": "PASS"}, ... }

Exit 0 if the harness passes (every item usable, false-pass <= threshold, false-fail <= threshold).
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SET = HERE / "validity-set.yaml"
VALID_TOKENS = {"PASS", "FAIL"}


def load_set(path: Path) -> dict:
    """Return {id: {kind, dimension, fail_passage(expected), pass_passage(expected)}}."""
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        out = {}
        for item in data.get("items", []):
            exp = item.get("expected", {}) or {}
            out[item["id"]] = {
                "kind": item.get("kind", "?"),
                "dimension": item.get("dimension", "?"),
                "fail_passage": str(exp.get("fail_passage", "FAIL")).upper(),
                "pass_passage": str(exp.get("pass_passage", "PASS")).upper(),
            }
        return out
    except ModuleNotFoundError:
        pass

    out: dict = {}
    cur = None
    for line in text.splitlines():
        m = re.match(r"\s*-\s*id:\s*(\S+)", line)
        if m:
            cur = m.group(1)
            out[cur] = {"kind": "?", "dimension": "?", "fail_passage": "FAIL", "pass_passage": "PASS"}
            continue
        if cur is None:
            continue
        mk = re.match(r"\s+kind:\s*(.+?)\s*$", line)
        if mk and out[cur]["kind"] == "?":
            out[cur]["kind"] = mk.group(1).strip()
        md = re.match(r"\s+dimension:\s*(.+?)\s*$", line)
        if md and out[cur]["dimension"] == "?":
            out[cur]["dimension"] = md.group(1).strip()
        me = re.search(r"expected:\s*\{(.+?)\}", line)
        if me:
            for key in ("fail_passage", "pass_passage"):
                km = re.search(rf"{key}\s*:\s*(\w+)", me.group(1))
                if km:
                    out[cur][key] = km.group(1).upper()
    return out


def norm(v: str) -> str:
    return str(v).strip().upper()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verdicts")
    ap.add_argument("--set", dest="set_path", default=str(DEFAULT_SET))
    ap.add_argument("--max-false-pass", type=float, default=0.0)
    ap.add_argument("--max-false-fail", type=float, default=0.0)
    ap.add_argument("--max-conformity", type=float, default=0.0,
                    help="max tolerated macro-conformity rate; hard gate, independent of --max-false-fail (default 0.0)")
    args = ap.parse_args()

    gold = load_set(Path(args.set_path))
    if not gold:
        print("ERROR: no items parsed from validity set", file=sys.stderr)
        return 2
    verdicts = json.loads(Path(args.verdicts).read_text(encoding="utf-8"))

    rows = []
    n = missing = unusable = both_correct = false_pass = false_fail = 0
    by_kind: dict = {}

    for sid, g in sorted(gold.items()):
        v = verdicts.get(sid)
        kind, dim = g["kind"], g["dimension"]
        bk = by_kind.setdefault(kind, {"n": 0, "scored": 0, "valid": 0, "false_pass": 0, "false_fail": 0})
        bk["n"] += 1
        n += 1
        if v is None:
            missing += 1
            rows.append((sid, kind, dim, "—", "—", "MISSING"))
            continue
        if not isinstance(v, dict) or not v:
            unusable += 1
            rows.append((sid, kind, dim, "—", "—", "UNUSABLE"))
            continue
        vf, vp = norm(v.get("fail_passage", "")), norm(v.get("pass_passage", ""))
        if vf not in VALID_TOKENS or vp not in VALID_TOKENS:
            unusable += 1
            rows.append((sid, kind, dim, vf or "—", vp or "—", "UNUSABLE"))
            continue
        bk["scored"] += 1
        fp = vf == "PASS"   # passed something that should FAIL → too lenient (broken whole let through)
        ff = vp == "FAIL"   # failed something that should PASS → too harsh (rejected a sound whole)
        if fp:
            false_pass += 1
            bk["false_pass"] += 1
        if ff:
            false_fail += 1
            bk["false_fail"] += 1
        valid = not fp and not ff
        if valid:
            both_correct += 1
            bk["valid"] += 1
        tag = "VALID" if valid else ("FALSE-PASS" if fp and not ff else "FALSE-FAIL" if ff and not fp else "BOTH-WRONG")
        rows.append((sid, kind, dim, vf, vp, tag))

    scored = n - missing - unusable
    fp_rate = false_pass / scored if scored else 1.0
    ff_rate = false_fail / scored if scored else 1.0
    accuracy = both_correct / scored if scored else 0.0
    sub = by_kind.get("subversion-trap")
    sub_scored = sub["scored"] if sub else 0
    macro_conformity = (sub["false_fail"] / sub_scored) if sub_scored else None

    print("\n=== whole-story-judge VALIDITY REPORT ===\n")
    print(f"{'ID':<18}{'KIND':<20}{'DIMENSION':<24}{'FAIL-PSG':<10}{'PASS-PSG':<10}OUTCOME")
    print("-" * 96)
    for sid, kind, dim, vf, vp, tag in rows:
        print(f"{sid:<18}{kind:<20}{dim:<24}{vf:<10}{vp:<10}{tag}")

    print("\n--- by control kind ---")
    for kind, k in sorted(by_kind.items()):
        print(f"  {kind:<18} valid {k['valid']}/{k['scored']}   false-pass {k['false_pass']}/{k['scored']}   false-fail {k['false_fail']}/{k['scored']}")

    excluded = missing + unusable
    print("\n--- headline metrics ---")
    print(f"  items scored:            {scored}/{n}" + (f"  ({missing} missing, {unusable} unusable)" if excluded else ""))
    print(f"  structure accuracy:      {accuracy:.0%}  (both calls correct)")
    print(f"  DROPPED-SETUP TOLERANCE: {fp_rate:.0%}  (passed a broken whole — lower is better)")
    if macro_conformity is not None:
        print(f"  MACRO CONFORMITY:        {macro_conformity:.0%}  (failed an earned subversion — crushed a valid whole)")
    print(f"  overall false-fail:      {ff_rate:.0%}  (too harsh — lower is better)")

    harness_pass = (
        excluded == 0
        and scored == n
        and fp_rate <= args.max_false_pass
        and ff_rate <= args.max_false_fail
        and (macro_conformity is None or macro_conformity <= args.max_conformity)
    )
    print(f"\n  HARNESS: {'PASS' if harness_pass else 'FAIL'} "
          f"(threshold: every item usable, false-pass <= {args.max_false_pass:.0%}, "
          f"false-fail <= {args.max_false_fail:.0%}, conformity <= {args.max_conformity:.0%})\n")
    return 0 if harness_pass else 1


if __name__ == "__main__":
    sys.exit(main())
