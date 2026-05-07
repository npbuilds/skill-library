"""Retrieval-quality eval for the skill library.

Calls HybridSearchIndex.search() directly with recent_skills=None for
reproducibility (production seeds graph from usage.jsonl, which we want to
isolate out for retrieval-quality measurement).

Metric: for each query we record gold-rank (best-match rank, 1-indexed; None
if absent from top-K), then aggregate recall@1/3/5/10 and false-positive
frequencies.

Output: data/health/eval_retrieval_<utcdate>.json + stdout summary.
"""

import json
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


def main():
    registry = json.loads(REGISTRY.read_text())
    idx = HybridSearchIndex(SKILLS_DIR, registry, DATA_DIR)
    build_status = idx.build()

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

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "by_domain": by_domain,
        "no_hit_strict": no_hit_strict,
        "no_hit_lenient": no_hit_lenient,
        "magnet_intrusions": magnet_intrusions,
        "results": results_per_query,
    }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUT_DIR / f"eval_retrieval_{stamp}.json"
    out.write_text(json.dumps(payload, indent=2))

    # ---- Print ----
    print("=" * 60)
    print("RETRIEVAL EVAL SUMMARY")
    print("=" * 60)
    print(f"Index status: {build_status}")
    print(f"Queries:           {len(EVAL)}  (with gold: {n_with_gold}, negative: {n_negative})")
    print()
    print(f"           strict           lenient (gold + children)")
    for k in (1, 3, 5, 10):
        sk = hits_strict[k]; lk = hits_lenient[k]
        print(f"recall@{k:<2}  {sk/n_with_gold:.3f} ({sk}/{n_with_gold})    {lk/n_with_gold:.3f} ({lk}/{n_with_gold})")
    print()
    print("By domain (recall@3):")
    for d, v in sorted(by_domain.items(), key=lambda x: x[1]["recall_at_3"]):
        rs = [r for r in v["ranks"] if r is not None]
        avg = round(sum(rs) / len(rs), 1) if rs else "n/a"
        print(f"  {d:18s} {v['recall_at_3']:.2f}  ({v['hit3']}/{v['n']})   avg gold rank: {avg}")
    print()
    print(f"Magnet intrusions in top-3: {len(magnet_intrusions)}")
    for m in magnet_intrusions[:10]:
        print(f"  rank {m['rank']}  {m['magnet']}  for query: {m['query']!r}")
    print()
    print(f"Queries with NO match in top-20 (lenient): {len(no_hit_lenient)}")
    for nh in no_hit_lenient:
        print(f"  [{nh['domain']}] {nh['query']!r}")
        print(f"    top5: {nh['top10'][:5]}")
    print()
    print(f"Negative-control top-3 (should be weak/irrelevant):")
    for q in results_per_query:
        if q["domain"] == "negative":
            print(f"  {q['query']!r} -> {q['top10'][:3]}")
    print()
    print(f"Full report -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
