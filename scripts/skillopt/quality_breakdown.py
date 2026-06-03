#!/usr/bin/env python3
"""Post-eval: per-task quality breakdown from rollout cache (no new rollouts)."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evaluate import _states
from grader import grade_one
from llm import get_solver_client
from runner import _cache_key, _cache
from tasks import load_tasks

cfg_path = Path("skills/research/spelunker/eval/quality-tasks.yaml")
tasks = [t for t in load_tasks(cfg_path) if t["split"] in ("val", "test")]
states = _states("quality")
client = get_solver_client()
jc = getattr(client, "_complete", None)
cache = _cache()

rows = []
judge_sums = defaultdict(lambda: defaultdict(list))

for t in tasks:
    for label, skill in [("no-skill", states["no-skill"]), ("current", states["current"])]:
        key = _cache_key(client.name, skill, t["id"])
        rollout = cache.get(key)
        if not rollout:
            print(f"MISSING CACHE: {label} {t['id']}", file=sys.stderr)
            continue
        r = grade_one(t, rollout, judge_complete=jc)
        cal = (r.get("detail") or {}).get("calibration", {})
        cit = (r.get("detail") or {}).get("citation_integrity", {})
        judged = (r.get("detail") or {}).get("judged") or {}
        rows.append({
            "id": t["id"], "split": t["split"], "state": label,
            "gate": r["score"], "passed": r["passed"],
            "tag": cal.get("core_tag"), "gold": cal.get("gold_status") or t.get("epistemic_status"),
            "cal": cal.get("score"), "cit": cit.get("score"),
        })
        if label == "current" and isinstance(judged, dict) and "error" not in judged:
            for crit, v in judged.items():
                if isinstance(v, dict) and v.get("score") is not None:
                    judge_sums[t["split"]][crit].append(float(v["score"]))

print("=== Per-task (val+test) ===")
print(f"{'id':32} {'spl':5} {'st':8} {'gate':6} {'tag':12} {'gold':10} {'cal':5} {'cit':5}")
for row in rows:
    print(f"{row['id']:32} {row['split']:5} {row['state']:8} {row['gate']:6.1f} {str(row['tag'] or '-'):12} {str(row['gold']):10} {row['cal']:5.1f} {row['cit']:5.1f}")

print("\n=== Judge diagnostic means (current only, 1-5 scale) ===")
for spl in ("val", "test"):
    print(f"  [{spl}]")
    for crit, vals in sorted(judge_sums[spl].items()):
        if vals:
            print(f"    {crit}: {sum(vals)/len(vals):.2f} (n={len(vals)})")

print("\n=== Calibration component means by gold (current) ===")
by_gold = defaultdict(list)
for row in rows:
    if row["state"] == "current":
        by_gold[row["gold"]].append((row["cal"], row["cit"], row["gate"]))
for gold in ("true", "refuted", "contested"):
    if gold in by_gold:
        vals = by_gold[gold]
        print(f"  {gold}: cal={sum(v[0] for v in vals)/len(vals):.1f} cit={sum(v[1] for v in vals)/len(vals):.1f} gate={sum(v[2] for v in vals)/len(vals):.1f} n={len(vals)}")

print("\n=== Calibration misses (current) ===")
for row in rows:
    if row["state"] != "current":
        continue
    g, tag, cal = row["gold"], row["tag"], row["cal"]
    if not tag:
        print(f"  MISSING CORE TAG: {row['id']} gate={row['gate']}")
        continue
    if g == "contested" and tag in ("Confirmed", "Likely") and cal < 70:
        print(f"  OVERCLAIM contested: {row['id']} tag={tag} cal={cal}")
    if g == "refuted" and tag in ("Confirmed", "Likely") and cal < 50:
        print(f"  REFUTED affirmed: {row['id']} tag={tag} cal={cal}")
    if g == "true" and tag == "Contested" and cal < 70:
        print(f"  UNDER-true (too cautious): {row['id']} tag={tag} cal={cal}")
