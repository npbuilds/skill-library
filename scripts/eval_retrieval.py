"""Retrieval-quality eval for the skill library.

Calls HybridSearchIndex.search() directly with recent_skills=None for
reproducibility (production seeds graph from usage.jsonl, which we want to
isolate out for retrieval-quality measurement).

Metric: for each query we record gold-rank (best-match rank, 1-indexed; None
if absent from top-K), then aggregate recall@1/3/5/10 and false-positive
frequencies.

Two query sources:
  - curated: the hand-written gold set below (EVAL).
  - synthetic: the held-out eval_queries from data/synthetic_queries.json
    (never indexed — index_queries and eval_queries are disjoint by
    construction; a contamination assert enforces it here too).

Used both as a local diagnostic (full hybrid, dated report) and as a CI
regression gate (--check against a committed baseline). CI has no torch, so
the gate runs --signals bm25,graph; the baseline must be recorded in the
same signal mode or the gate measures the environment, not regressions.

Output: data/health/eval_retrieval_<utcdate>.json + stdout summary.

Usage:
  python3 scripts/eval_retrieval.py                         # curated, full hybrid
  python3 scripts/eval_retrieval.py --queries all           # curated + synthetic
  python3 scripts/eval_retrieval.py --signals bm25,graph    # no vectors (CI mode)
  python3 scripts/eval_retrieval.py --write-baseline data/health/eval_baseline.json
  python3 scripts/eval_retrieval.py --baseline data/health/eval_baseline.json --check
"""

import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mcp-server"))

from search_index import HybridSearchIndex  # noqa: E402

REGISTRY = ROOT / "data" / "registry.json"
SKILLS_DIR = ROOT / "skills"
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "health"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Regression-gate tolerances (absolute recall drop allowed vs baseline).
CURATED_TOLERANCE = 0.03   # ~one query flip on the ~30-query gold set
SYNTHETIC_TOLERANCE = 0.02


# ---------------------------------------------------------------------------
# Eval set: (query, gold_targets, intent_tag, domain)
#   gold_targets is a set — any one of them in top-K counts as a hit.
# ---------------------------------------------------------------------------

EVAL = [
    # ---- Sommelier ----
    ("how should I taste this glass of wine",
     {"tasting-evaluation", "bacchus", "deductive-method"}, "tasting", "sommelier"),
    ("what wine should I pair with rack of lamb",
     {"food-pairing", "bacchus"}, "pairing", "sommelier"),
    ("tell me about cabernet sauvignon",
     {"grape-encyclopedia", "bacchus"}, "grape-lookup", "sommelier"),
    ("what makes Burgundy different from Bordeaux",
     {"regions-terroir", "bacchus"}, "region-compare", "sommelier"),
    ("is this 2010 Bordeaux a good investment",
     {"wine-market", "bacchus"}, "investment", "sommelier"),
    ("my wine smells like wet cardboard, is it corked",
     {"fault-diagnosis", "tasting-evaluation"}, "fault", "sommelier"),
    ("what temperature should I serve a champagne",
     {"service-protocol", "cellar-service", "bacchus"}, "service", "sommelier"),
    ("decant a young Barolo or not",
     {"service-protocol", "cellar-service"}, "service-decision", "sommelier"),

    # ---- Biotech VC ----
    ("calculate rNPV for an oncology asset",
     {"asset-valuation", "asclepius"}, "rnpv", "biotech-venture"),
    ("design a phase 2 trial for a PD-L1 inhibitor",
     {"trial-design-optimizer", "clinical-development", "asclepius"}, "trial-design", "biotech-venture"),
    ("how do I enrich for biomarker responders",
     {"biomarker-enrichment", "clinical-development"}, "enrichment", "biotech-venture"),
    ("how does this drug differentiate vs Keytruda",
     {"clinical-differentiator", "asclepius"}, "differentiation", "biotech-venture"),
    ("forecast peak sales for a small molecule oncology drug",
     {"asset-valuation", "asclepius"}, "forecasting", "biotech-venture"),

    # ---- Data science ----
    ("my dataset has 30% missing values, what should I do",
     {"data-cleaning", "data-science-orchestrator"}, "missing-data", "data-science"),
    ("how do I encode categorical features for xgboost",
     {"feature-engineering", "data-science-orchestrator"}, "encoding", "data-science"),
    ("forecast monthly revenue with seasonality",
     {"time-series", "data-science-orchestrator"}, "forecast", "data-science"),
    ("my production model performance is degrading",
     {"drift-detection", "data-science-orchestrator"}, "drift", "data-science"),

    # ---- Philosophy / logic ----
    ("evaluate this syllogism for validity",
     {"argument-analyst", "logic", "formal-logic"}, "argument", "philosophy"),
    ("translate this English claim into propositional logic",
     {"formal-logic", "logic"}, "formalize", "philosophy"),

    # ---- Game theory ----
    ("find the Nash equilibrium of this 2x2 game",
     {"classical-games", "strategic-foundations", "game-theory-orchestrator"}, "nash", "game-theory"),
    ("design an auction for spectrum rights",
     {"mechanism-design", "game-theory-orchestrator"}, "auction", "game-theory"),

    # ---- Research ----
    ("research whether GLP-1s reduce alzheimer risk",
     {"spelunker"}, "deep-research", "research"),
    ("break this question into atomic verifiable claims",
     {"claim-decomposer", "spelunker"}, "decompose", "research"),
    ("triangulate sources for this contested claim",
     {"source-triangulator", "spelunker"}, "triangulate", "research"),

    # ---- World history ----
    ("what does the great divergence debate say about industrialization",
     {"industrialization-and-development", "applied-history", "wan-shi-tong"},
     "great-divergence", "world-history"),
    ("how should I evaluate a primary historical source",
     {"historiography", "wan-shi-tong"}, "source-eval", "world-history"),

    # ---- Worldbuilding / writing ----
    ("design the climate and biomes for a fantasy world",
     {"physical-world"}, "worldbuilding-physical", "worldbuilding"),
    ("how do I render a character's stream of consciousness",
     {"character-interiority"}, "interiority", "writing"),
    ("the line-by-line tension is missing from my chapter",
     {"micro-tension"}, "tension", "writing"),
    ("when should I use metaphor vs simile",
     {"figurative-language"}, "figurative", "writing"),

    # ---- Negative / out-of-scope (no skill should rank highly) ----
    ("how do I tie a windsor knot",
     set(), "out-of-scope-fashion", "negative"),
    ("write a python function to reverse a string",
     set(), "out-of-scope-coding", "negative"),
]

# Skills that historically appear as false positives across unrelated queries
# (semantic-magnet skills with broad descriptions). Tracked so we can flag
# when they dominate top-3 for queries they have no business near.
KNOWN_MAGNETS = {"frontier-scanner", "clarity-engine", "world-bible", "skill-cartographer"}


def _children_of(registry: dict, names: set) -> set:
    """Return the set of skills whose parent is in `names`."""
    children = set()
    for n, e in registry.get("skills", {}).items():
        if e.get("parent") in names:
            children.add(n)
    return children


def _restrict_signals(idx: HybridSearchIndex, signals: set) -> None:
    """Disable signals not in `signals` so the eval matches a target mode.

    Note: the graph signal only fires when search() is given recent_skills,
    which the eval never does (recent_skills=None for reproducibility). So
    'graph' here is effectively inert and 'bm25,graph' means BM25-only — the
    mode CI runs in (no torch → no vectors).
    """
    if "bm25" not in signals:
        idx._bm25 = None
    if "vector" not in signals:
        idx._embeddings = None


def run_synthetic(idx, registry, sample, seed):
    """Evaluate the held-out synthetic eval_queries (self-retrieval).

    Each eval query's gold is its own skill (strict); lenient adds the
    skill's parent and children. Returns (metrics, n, detail). Asserts the
    eval queries never overlap the indexed index_queries (contamination).
    """
    syn_path = DATA_DIR / "synthetic_queries.json"
    try:
        payload = json.loads(syn_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None, 0, {"error": "no synthetic_queries.json"}

    skills_meta = registry.get("skills", {})
    pairs = []  # (query, skill)
    self_contaminated = []  # eval query that also indexes its OWN skill
    for name, entry in payload.get("skills", {}).items():
        if name not in skills_meta:
            continue
        own_index = {q.strip().lower() for q in entry.get("index_queries", [])}
        for q in entry.get("eval_queries", []):
            pairs.append((q, name))
            if q.strip().lower() in own_index:
                self_contaminated.append((name, q))

    # Contamination guard: a skill's held-out eval query must never also be one
    # of THAT skill's index queries (a self-leak that would inflate recall).
    # Cross-skill phrase collisions are fine — they make retrieval harder, not
    # easier, so they aren't leaks.
    assert not self_contaminated, (
        f"{len(self_contaminated)} eval queries leak into their own skill's "
        f"index set: {self_contaminated[:3]}"
    )

    if sample and len(pairs) > sample:
        pairs = random.Random(seed).sample(pairs, sample)

    hits = {1: 0, 5: 0}
    n = 0
    misses = []
    for query, skill in pairs:
        parent = skills_meta.get(skill, {}).get("parent")
        gold = {skill}
        gold_lenient = {skill} | _children_of(registry, {skill})
        if parent:
            gold_lenient.add(parent)
        ranked = [r["name"] for r in idx.search(query, recent_skills=None, limit=10)]
        rank = next((i for i, nm in enumerate(ranked, 1) if nm in gold_lenient), None)
        n += 1
        for k in (1, 5):
            if rank is not None and rank <= k:
                hits[k] += 1
        if rank is None:
            misses.append({"query": query, "skill": skill, "top5": ranked[:5]})

    metrics = {f"recall_at_{k}": round(hits[k] / n, 3) if n else 0.0 for k in (1, 5)}
    return metrics, n, {"misses": misses[:20]}


def _check_baseline(baseline_path, curated_summary, synth_metrics, synth_n):
    """Compare current metrics to a committed baseline. Returns (ok, lines)."""
    lines = []
    try:
        base = json.loads(Path(baseline_path).read_text())
    except (OSError, json.JSONDecodeError) as e:
        return False, [f"::error::cannot read baseline {baseline_path}: {e}"]

    ok = True
    checks = [
        ("curated strict recall@5",
         curated_summary["strict"]["recall_at_5"],
         base.get("curated", {}).get("strict", {}).get("recall_at_5"),
         CURATED_TOLERANCE),
        ("curated lenient recall@3",
         curated_summary["lenient"]["recall_at_3"],
         base.get("curated", {}).get("lenient", {}).get("recall_at_3"),
         CURATED_TOLERANCE),
    ]
    if synth_metrics is not None:
        checks.append((
            "synthetic recall@5",
            synth_metrics["recall_at_5"],
            base.get("synthetic", {}).get("recall_at_5"),
            SYNTHETIC_TOLERANCE,
        ))

    base_n = base.get("meta", {})
    lines.append(
        f"Baseline n: curated={base_n.get('curated_n', '?')} "
        f"synthetic={base_n.get('synthetic_n', '?')}  |  "
        f"current n: curated={curated_summary['queries_with_gold']} synthetic={synth_n}"
    )
    for label, cur, base_val, tol in checks:
        if base_val is None:
            lines.append(f"  ?  {label}: no baseline value (skipped)")
            continue
        delta = cur - base_val
        status = "OK" if delta >= -tol else "FAIL"
        if status == "FAIL":
            ok = False
        lines.append(
            f"  {status:4s} {label}: {cur:.3f} vs baseline {base_val:.3f} "
            f"(Δ {delta:+.3f}, tol -{tol})"
        )
    return ok, lines


def run_curated(idx, registry, build_status):
    """Evaluate the curated EVAL gold set. Returns the full payload dict."""
    results_per_query = []
    hits_strict = {1: 0, 3: 0, 5: 0, 10: 0}
    hits_lenient = {1: 0, 3: 0, 5: 0, 10: 0}
    no_hit_strict = []
    no_hit_lenient = []
    magnet_intrusions = []
    n_with_gold = sum(1 for _, gold, _, _ in EVAL if gold)
    n_negative = len(EVAL) - n_with_gold

    for query, gold, intent, domain in EVAL:
        ranked = idx.search(query, recent_skills=None, limit=20)
        names_in_order = [r["name"] for r in ranked]

        # Strict gold = exactly what's named. Lenient gold = strict + children
        # of any director in the strict set (a child specialist out-ranking
        # its parent is the desired behavior).
        gold_lenient = set(gold) | _children_of(registry, set(gold))

        def _rank(target_set):
            for r, n in enumerate(names_in_order, start=1):
                if n in target_set:
                    return r
            return None

        strict_rank = _rank(gold) if gold else None
        lenient_rank = _rank(gold_lenient) if gold_lenient else None

        if gold:
            for k in (1, 3, 5, 10):
                if strict_rank is not None and strict_rank <= k:
                    hits_strict[k] += 1
                if lenient_rank is not None and lenient_rank <= k:
                    hits_lenient[k] += 1
            if strict_rank is None:
                no_hit_strict.append({"query": query, "domain": domain,
                                       "top10": names_in_order[:10]})
            if lenient_rank is None:
                no_hit_lenient.append({"query": query, "domain": domain,
                                        "top10": names_in_order[:10]})

        # magnet intrusions in top-3 for queries where the magnet is NOT a
        # gold target (so frontier-scanner counts as intrusion for "wine"
        # queries but not for an AI-frontier query)
        for r, n in enumerate(names_in_order[:3], start=1):
            if n in KNOWN_MAGNETS and n not in gold:
                magnet_intrusions.append({"query": query, "magnet": n, "rank": r,
                                          "domain": domain})

        results_per_query.append({
            "query": query, "domain": domain, "intent": intent,
            "gold_strict": sorted(gold),
            "gold_lenient_added": sorted(gold_lenient - set(gold)),
            "strict_rank": strict_rank,
            "lenient_rank": lenient_rank,
            "top10": names_in_order[:10],
        })

    # negatives: any non-magnet skill in top-3 that scores well is hard to call
    # a false positive without a human, but if a magnet shows up that's clearly
    # bad. We just record top-3 for the negatives in the report.
    def _rec(h):
        return {f"recall_at_{k}": round(h[k] / n_with_gold, 3) for k in (1, 3, 5, 10)}

    summary = {
        "build_status": build_status,
        "total_queries": len(EVAL),
        "queries_with_gold": n_with_gold,
        "queries_negative": n_negative,
        "strict": _rec(hits_strict),
        "lenient": _rec(hits_lenient),
        "no_hit_strict_count": len(no_hit_strict),
        "no_hit_lenient_count": len(no_hit_lenient),
        "magnet_intrusion_count_top3": len(magnet_intrusions),
    }

    # by-domain recall (lenient — fairer to library structure)
    by_domain = {}
    for q in results_per_query:
        d = q["domain"]
        if d == "negative" or not q["gold_strict"]:
            continue
        by_domain.setdefault(d, {"n": 0, "hit3": 0, "ranks": []})
        by_domain[d]["n"] += 1
        if q["lenient_rank"] is not None:
            if q["lenient_rank"] <= 3:
                by_domain[d]["hit3"] += 1
            by_domain[d]["ranks"].append(q["lenient_rank"])
        else:
            by_domain[d]["ranks"].append(None)
    for d, v in by_domain.items():
        v["recall_at_3"] = round(v["hit3"] / v["n"], 3)

    return {
        "summary": summary,
        "by_domain": by_domain,
        "no_hit_strict": no_hit_strict,
        "no_hit_lenient": no_hit_lenient,
        "magnet_intrusions": magnet_intrusions,
        "results": results_per_query,
    }


def _print_curated(c):
    s = c["summary"]
    n_with_gold = s["queries_with_gold"]
    print("=" * 60)
    print("RETRIEVAL EVAL SUMMARY")
    print("=" * 60)
    print(f"Index status: {s['build_status']}")
    print(f"Queries:           {s['total_queries']}  "
          f"(with gold: {n_with_gold}, negative: {s['queries_negative']})")
    print()
    print("           strict           lenient (gold + children)")
    for k in (1, 3, 5, 10):
        sk = s["strict"][f"recall_at_{k}"]
        lk = s["lenient"][f"recall_at_{k}"]
        print(f"recall@{k:<2}  {sk:.3f} ({round(sk*n_with_gold)}/{n_with_gold})    "
              f"{lk:.3f} ({round(lk*n_with_gold)}/{n_with_gold})")
    print()
    print("By domain (recall@3):")
    for d, v in sorted(c["by_domain"].items(), key=lambda x: x[1]["recall_at_3"]):
        rs = [r for r in v["ranks"] if r is not None]
        avg = round(sum(rs) / len(rs), 1) if rs else "n/a"
        print(f"  {d:18s} {v['recall_at_3']:.2f}  ({v['hit3']}/{v['n']})   avg gold rank: {avg}")
    print()
    print(f"Magnet intrusions in top-3: {s['magnet_intrusion_count_top3']}")
    print(f"Queries with NO match in top-20 (lenient): {s['no_hit_lenient_count']}")
    for nh in c["no_hit_lenient"]:
        print(f"  [{nh['domain']}] {nh['query']!r}")
    print()
    print("Negative-control top-3 (should be weak/irrelevant):")
    for q in c["results"]:
        if q["domain"] == "negative":
            print(f"  {q['query']!r} -> {q['top10'][:3]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--queries", choices=["curated", "synthetic", "all"], default="curated")
    ap.add_argument("--signals", default="bm25,vector,graph",
                    help="comma list of signals to keep (bm25,vector,graph)")
    ap.add_argument("--sample", type=int, default=0, help="cap synthetic queries (0=all)")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--baseline", help="baseline JSON to compare against")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if metrics regress beyond tolerance vs --baseline")
    ap.add_argument("--write-baseline", help="write current metrics as a baseline JSON")
    args = ap.parse_args()

    signals = {s.strip() for s in args.signals.split(",") if s.strip()}
    registry = json.loads(REGISTRY.read_text())
    idx = HybridSearchIndex(SKILLS_DIR, registry, DATA_DIR)
    build_status = idx.build()
    _restrict_signals(idx, signals)

    curated = run_curated(idx, registry, build_status)
    _print_curated(curated)

    synth_metrics, synth_n, synth_detail = (None, 0, {})
    if args.queries in ("synthetic", "all"):
        synth_metrics, synth_n, synth_detail = run_synthetic(
            idx, registry, args.sample, args.seed
        )
        print()
        if synth_metrics is None:
            print(f"Synthetic eval skipped: {synth_detail.get('error')}")
        else:
            print(f"Synthetic holdout ({synth_n} queries, signals={sorted(signals)}): "
                  f"recall@1 {synth_metrics['recall_at_1']:.3f}  "
                  f"recall@5 {synth_metrics['recall_at_5']:.3f}")

    # Write a dated diagnostic report (skip in pure --check CI runs to keep
    # the working tree clean).
    if not args.check:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = OUT_DIR / f"eval_retrieval_{stamp}.json"
        out.write_text(json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "signals": sorted(signals),
            **curated,
            "synthetic": {"metrics": synth_metrics, "n": synth_n, **synth_detail},
        }, indent=2))
        print(f"\nFull report -> {out.relative_to(ROOT)}")

    # Baseline payload (used by both --write-baseline and --check).
    baseline_payload = {
        "meta": {
            "signals": sorted(signals),
            "curated_n": curated["summary"]["queries_with_gold"],
            "synthetic_n": synth_n,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "curated": {
            "strict": curated["summary"]["strict"],
            "lenient": curated["summary"]["lenient"],
        },
        "synthetic": synth_metrics or {},
    }

    if args.write_baseline:
        Path(args.write_baseline).write_text(json.dumps(baseline_payload, indent=2))
        print(f"\nWrote baseline -> {args.write_baseline}")

    if args.check:
        if not args.baseline:
            print("::error::--check requires --baseline", file=sys.stderr)
            return 2
        ok, lines = _check_baseline(
            args.baseline, curated["summary"], synth_metrics, synth_n
        )
        print("\n" + "=" * 60)
        print("REGRESSION GATE")
        print("=" * 60)
        for ln in lines:
            print(ln)
        if not ok:
            print("::error::retrieval regression beyond tolerance")
            return 1
        print("PASS — no regression beyond tolerance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
