#!/usr/bin/env python3
"""Detect algorithmic communities in the skill dependency graph using Leiden.

Compares emergent Leiden communities against manual domain assignments to
surface fragmented domains, natural bridges, and cohesion issues.

Usage:
    python3 scripts/detect-communities.py                     # Full analysis
    python3 scripts/detect-communities.py --domain sommelier  # One domain
    python3 scripts/detect-communities.py --json              # Machine-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "data" / "registry.json"

try:
    import igraph as ig
    import leidenalg
except ImportError:
    print(
        "This script requires python-igraph and leidenalg.\n"
        "Install with:  pip install python-igraph leidenalg",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_registry() -> dict:
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def get_domain(entry: dict) -> str:
    for tag in entry.get("tags", []):
        if tag.startswith("domain:"):
            return tag.split(":", 1)[1]
    return "?"


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def detect_communities(registry: dict, focus_domain: str | None = None) -> dict:
    """Run Leiden community detection and compare against manual domains.

    Returns a dict with:
        communities: list of community dicts
        domain_report: per-domain alignment analysis
        recommendations: list of actionable suggestions
    """
    skills = registry.get("skills", {})

    # Build node list (active skills only)
    names = []
    for name, entry in skills.items():
        if entry.get("status") != "active":
            continue
        if focus_domain and get_domain(entry) != focus_domain:
            continue
        names.append(name)

    if len(names) < 3:
        return {"communities": [], "domain_report": {}, "recommendations": [
            "Too few active skills to detect communities."
        ]}

    name_to_idx = {n: i for i, n in enumerate(names)}
    name_set = set(names)

    # Build edges (undirected — both depends_on directions)
    edges = set()
    for name in names:
        entry = skills[name]
        for dep in entry.get("depends_on", []):
            if dep in name_set:
                a, b = name_to_idx[name], name_to_idx[dep]
                edges.add((min(a, b), max(a, b)))
        for ref in entry.get("referenced_by", []):
            if ref in name_set:
                a, b = name_to_idx[name], name_to_idx[ref]
                edges.add((min(a, b), max(a, b)))

    G = ig.Graph(n=len(names), edges=list(edges), directed=False)
    G.vs["name"] = names

    # Run Leiden
    partition = leidenalg.find_partition(
        G, leidenalg.RBConfigurationVertexPartition, resolution_parameter=1.0
    )

    # Analyze communities
    communities = []
    for comm_id, members in enumerate(partition):
        if len(members) < 2:
            continue  # skip singletons
        member_names = [names[i] for i in members]
        domains = Counter(get_domain(skills[n]) for n in member_names)

        # Cohesion: internal edges / (internal + external edges)
        subgraph = G.subgraph(members)
        internal_edges = subgraph.ecount()
        total_incident = sum(G.degree(m) for m in members)
        external_edges = total_incident - 2 * internal_edges
        total = internal_edges + external_edges
        cohesion = internal_edges / total if total > 0 else 0.0

        communities.append({
            "id": comm_id,
            "size": len(members),
            "members": sorted(member_names),
            "cohesion": round(cohesion, 3),
            "dominant_domain": domains.most_common(1)[0][0],
            "domain_mix": dict(domains.most_common()),
            "is_cross_domain": len(domains) > 1,
        })

    communities.sort(key=lambda c: -c["size"])

    # Domain alignment report
    domain_report = {}
    domain_skills = {}
    for name in names:
        d = get_domain(skills[name])
        domain_skills.setdefault(d, []).append(name)

    for domain, d_skills in sorted(domain_skills.items()):
        # Which communities do this domain's skills land in?
        comm_assignments = Counter()
        for s in d_skills:
            for c in communities:
                if s in c["members"]:
                    comm_assignments[c["id"]] += 1
                    break

        # Domain cohesion: fraction of skills in the dominant community
        if comm_assignments:
            dominant_comm_count = comm_assignments.most_common(1)[0][1]
            alignment = dominant_comm_count / len(d_skills)
        else:
            alignment = 0.0

        domain_report[domain] = {
            "total_skills": len(d_skills),
            "communities_spanned": len(comm_assignments),
            "alignment": round(alignment, 3),
            "community_distribution": dict(comm_assignments.most_common()),
            "fragmented": len(comm_assignments) >= 3,
        }

    # Recommendations
    recommendations = []

    for domain, report in domain_report.items():
        if report["fragmented"]:
            recommendations.append(
                f"Domain '{domain}' is fragmented across "
                f"{report['communities_spanned']} communities (alignment "
                f"{report['alignment']:.0%}). Consider adding a director or "
                f"strengthening internal dependencies."
            )
        elif report["alignment"] < 0.5 and report["total_skills"] >= 5:
            recommendations.append(
                f"Domain '{domain}' has low alignment ({report['alignment']:.0%}). "
                f"Its skills cluster more with other domains than with each other."
            )

    for c in communities:
        if c["is_cross_domain"] and c["size"] >= 4:
            domains = list(c["domain_mix"].keys())
            recommendations.append(
                f"Community {c['id']} ({c['size']} skills, cohesion {c['cohesion']:.2f}) "
                f"bridges {', '.join(domains)}. These domains have strong natural affinity."
            )

    low_cohesion = [c for c in communities if c["cohesion"] < 0.3 and c["size"] >= 4]
    for c in low_cohesion:
        recommendations.append(
            f"Community {c['id']} ({c['dominant_domain']}, {c['size']} skills) "
            f"has low cohesion ({c['cohesion']:.2f}). Members talk more to outsiders "
            f"than to each other."
        )

    # Singletons — skills not in any community of size >= 2
    community_members = {s for c in communities for s in c["members"]}
    singletons = [n for n in names if n not in community_members]
    if singletons:
        recommendations.append(
            f"{len(singletons)} skill(s) are isolates (no community): "
            f"{', '.join(singletons[:10])}"
            + ("..." if len(singletons) > 10 else "")
        )

    return {
        "communities": communities,
        "domain_report": domain_report,
        "recommendations": recommendations,
        "stats": {
            "total_skills": len(names),
            "total_edges": len(edges),
            "communities_found": len(communities),
            "singletons": len(singletons),
            "modularity": round(partition.modularity, 4),
        },
    }


# ---------------------------------------------------------------------------
# CLI output formatting
# ---------------------------------------------------------------------------

def print_report(result: dict) -> None:
    stats = result["stats"]
    print(f"\n=== Community Detection Report ===")
    print(f"Skills: {stats['total_skills']}, Edges: {stats['total_edges']}, "
          f"Communities: {stats['communities_found']}, "
          f"Singletons: {stats['singletons']}, "
          f"Modularity: {stats['modularity']}")

    print(f"\n--- Communities (by size) ---")
    for c in result["communities"]:
        cross = " [CROSS-DOMAIN]" if c["is_cross_domain"] else ""
        print(f"\n  Community {c['id']}: {c['size']} skills, "
              f"cohesion {c['cohesion']:.2f}{cross}")
        print(f"    Domains: {c['domain_mix']}")
        # Show first 8 members
        shown = c["members"][:8]
        print(f"    Members: {', '.join(shown)}"
              + (f" (+{c['size'] - 8} more)" if c["size"] > 8 else ""))

    print(f"\n--- Domain Alignment ---")
    for domain, report in sorted(result["domain_report"].items()):
        frag = " FRAGMENTED" if report["fragmented"] else ""
        print(f"  {domain}: {report['total_skills']} skills, "
              f"alignment {report['alignment']:.0%}, "
              f"across {report['communities_spanned']} communities{frag}")

    if result["recommendations"]:
        print(f"\n--- Recommendations ---")
        for r in result["recommendations"]:
            print(f"  - {r}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Detect skill communities via Leiden algorithm")
    parser.add_argument("--domain", help="Focus on a single domain")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of formatted report")
    args = parser.parse_args()

    registry = load_registry()
    result = detect_communities(registry, focus_domain=args.domain)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
