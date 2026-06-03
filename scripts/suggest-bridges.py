#!/usr/bin/env python3
"""
suggest-bridges.py — Suggest cross-domain connections for a skill.

Given a skill name, analyzes its content and the existing registry to suggest
cross-domain bridges that should be wired. Uses TF-IDF keyword similarity,
domain adjacency boosting, and structural role matching.

Usage:
    python3 scripts/suggest-bridges.py <skill-name>
    python3 scripts/suggest-bridges.py <skill-name> --apply  # also writes to registry
    python3 scripts/suggest-bridges.py --scan-all             # find all missing bridges
    python3 scripts/suggest-bridges.py --test-pair <a> <b>    # debug similarity between two skills
"""

import json
import math
import sys
import re
from collections import Counter, defaultdict
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PLUGIN_ROOT / "data" / "registry.json"


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def get_domain(skill):
    """Extract domain from skill tags."""
    for tag in skill.get("tags", []):
        if isinstance(tag, str) and tag.startswith("domain:"):
            return tag.split(":", 1)[1]
    return "unknown"


def get_level(skill):
    """Extract level/type from skill tags."""
    for tag in skill.get("tags", []):
        if isinstance(tag, str) and tag.startswith("level:"):
            return tag.split(":", 1)[1]
    return skill.get("type", "unknown")


def read_skill_content(skill):
    """Read the SKILL.md file content."""
    location = skill.get("location", "")
    path = PLUGIN_ROOT / location
    if path.is_file():
        return path.read_text()
    return ""


def extract_keywords(text):
    """Extract meaningful keywords from skill content."""
    # Remove markdown formatting
    text = re.sub(r"[#*`|_\-\[\]()]", " ", text.lower())
    # Split into words
    words = re.findall(r"\b[a-z]{4,}\b", text)
    # Filter common stop words and markdown artifacts
    stop = {
        "this", "that", "with", "from", "have", "will", "when", "what",
        "which", "their", "about", "each", "should", "would", "could",
        "does", "doesn", "skill", "skills", "domain", "user", "using",
        "based", "level", "example", "examples", "section", "table",
        "reference", "references", "read", "write", "route", "director",
        "orchestrator", "handle", "handles", "question", "questions",
        "approach", "framework", "analysis", "process", "system",
        "understand", "understanding", "apply", "applies", "applied",
        "consult", "escalate", "scope", "boundaries", "note", "true",
        "false", "first", "second", "third", "most", "more", "than",
        "also", "just", "like", "into", "over", "only", "between",
        "through", "both", "other", "some", "same", "different",
        "need", "needs", "make", "makes", "help", "helps", "want",
        "wants", "know", "knows", "think", "thinks", "look", "looks",
        "work", "works", "give", "gives", "take", "takes", "come",
        "comes", "tell", "tells", "show", "shows", "find", "finds",
        "here", "there", "where", "then", "them", "they", "these",
        "those", "your", "been", "being", "were", "after", "before",
        "under", "above", "such", "very", "well", "much", "many",
        "every", "even", "back", "still", "down", "long", "while",
        "good", "great", "best", "right", "high", "part", "type",
        "types", "case", "cases", "used", "uses", "form", "forms",
        "pattern", "patterns", "way", "ways", "key", "common",
        "specific", "across", "within", "include", "includes",
        "create", "creates", "check", "checks", "related",
        "important", "often", "rather", "whether", "because",
        "primary", "consider", "following", "without", "another",
        "multiple", "single", "against", "general", "current",
        "possible", "allow", "allows", "require", "requires",
        "ensure", "provides", "support", "supports", "identify",
    }
    return Counter(w for w in words if w not in stop)


# ---------------------------------------------------------------------------
# TF-IDF computation
# ---------------------------------------------------------------------------

def build_corpus(registry):
    """Build a keyword corpus for all skills, returning {name: Counter}."""
    corpus = {}
    for name, skill in registry["skills"].items():
        content = read_skill_content(skill)
        corpus[name] = extract_keywords(content)
    return corpus


def compute_idf(corpus):
    """Compute inverse-document-frequency for every term in the corpus."""
    n_docs = len(corpus)
    doc_freq = Counter()
    for kw in corpus.values():
        for word in kw:
            doc_freq[word] += 1
    # IDF = log(N / df).  Terms in every doc get ~0; rare terms get high weight.
    return {word: math.log(n_docs / df) for word, df in doc_freq.items()}


def tfidf_vector(kw_counter, idf, top_n=80):
    """Return the top-N TF-IDF weighted terms as a dict {term: weight}."""
    scored = {}
    total = sum(kw_counter.values()) or 1
    for word, count in kw_counter.items():
        tf = count / total
        scored[word] = tf * idf.get(word, 0)
    # Keep top N by TF-IDF weight
    top = sorted(scored, key=scored.get, reverse=True)[:top_n]
    return {w: scored[w] for w in top}


def cosine_similarity(vec_a, vec_b):
    """Cosine similarity between two TF-IDF vectors (dicts)."""
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot = sum(vec_a[w] * vec_b[w] for w in common)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ---------------------------------------------------------------------------
# Domain adjacency — existing bridges boost new suggestions
# ---------------------------------------------------------------------------

def build_domain_adjacency(registry):
    """Build a set of (domain_a, domain_b) pairs that already have bridges."""
    skills = registry["skills"]
    pairs = set()
    for name, skill in skills.items():
        src_domain = get_domain(skill)
        for dep in skill.get("depends_on", []) + skill.get("referenced_by", []):
            if dep in skills:
                tgt_domain = get_domain(skills[dep])
                if src_domain != tgt_domain:
                    pair = tuple(sorted([src_domain, tgt_domain]))
                    pairs.add(pair)
    return pairs


# ---------------------------------------------------------------------------
# Main bridge-finding logic
# ---------------------------------------------------------------------------

def find_bridge_candidates(target_name, registry, corpus, idf, threshold=0.05):
    """Find skills in other domains with high TF-IDF cosine similarity."""
    skills = registry["skills"]
    if target_name not in skills:
        print(f"Error: skill '{target_name}' not found in registry")
        sys.exit(1)

    target = skills[target_name]
    target_domain = get_domain(target)
    target_level = get_level(target)
    target_vec = tfidf_vector(corpus.get(target_name, Counter()), idf)

    # Get existing connections
    existing = set(target.get("depends_on", []) + target.get("referenced_by", []))

    # Domain adjacency for boosting
    adjacency = build_domain_adjacency(registry)

    candidates = []
    for name, skill in skills.items():
        if name == target_name:
            continue
        skill_domain = get_domain(skill)
        if skill_domain == target_domain:
            continue  # Only cross-domain
        if name in existing:
            continue  # Already connected

        vec = tfidf_vector(corpus.get(name, Counter()), idf)
        sim = cosine_similarity(target_vec, vec)

        if sim < threshold * 0.5:
            continue  # Skip very low scores early

        # --- Boosting signals ---

        # 1. Domain adjacency: if these two domains are already connected,
        #    boost by 30% (more likely to be a real bridge)
        pair = tuple(sorted([target_domain, skill_domain]))
        if pair in adjacency:
            sim *= 1.3

        # 2. Structural role matching: directors bridge better to directors,
        #    leaf skills to leaf skills. Slight boost for matching type.
        skill_level = get_level(skill)
        if target_level == skill_level:
            sim *= 1.1

        # 3. Penalty for infrastructure/meta skills bridging to content skills
        #    (these are usually false positives)
        meta_domains = {"infrastructure", "neocortex", "_meta"}
        if (target_domain in meta_domains) != (skill_domain in meta_domains):
            sim *= 0.6

        if sim >= threshold:
            # Find shared top terms for display
            shared = sorted(
                set(target_vec) & set(vec),
                key=lambda w: -(target_vec.get(w, 0) + vec.get(w, 0))
            )[:10]
            candidates.append({
                "name": name,
                "domain": skill_domain,
                "similarity": sim,
                "shared_keywords": shared,
            })

    candidates.sort(key=lambda c: -c["similarity"])
    return candidates


def scan_all_missing(registry):
    """Find all skills that should be cross-domain connected but aren't."""
    skills = registry["skills"]
    missing = []

    for name, skill in skills.items():
        domain = get_domain(skill)
        existing = set(skill.get("depends_on", []) + skill.get("referenced_by", []))
        # Check if this skill has ANY cross-domain connections
        has_cross = False
        for conn in existing:
            if conn in skills:
                conn_domain = get_domain(skills[conn])
                if conn_domain != domain:
                    has_cross = True
                    break
        if not has_cross:
            missing.append({"name": name, "domain": domain})

    return missing


def apply_bridges(target_name, candidates, registry, max_bridges=3):
    """Apply the top N bridge suggestions to the registry."""
    skills = registry["skills"]
    applied = []
    healed = 0
    for c in candidates[:max_bridges]:
        src = target_name
        tgt = c["name"]
        is_new = tgt not in skills[src].get("depends_on", [])
        if is_new:
            skills[src].setdefault("depends_on", []).append(tgt)
            applied.append(c)
        if src not in skills[tgt].get("referenced_by", []):
            skills[tgt].setdefault("referenced_by", []).append(src)
            if not is_new:
                healed += 1

    if applied or healed:
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)
            f.write("\n")

    if healed:
        print(f"  (also healed {healed} missing referenced_by back-links)")

    return applied


def test_pair(name_a, name_b, registry, corpus, idf):
    """Debug: show detailed similarity breakdown between two skills."""
    skills = registry["skills"]
    for n in (name_a, name_b):
        if n not in skills:
            print(f"Error: '{n}' not found in registry")
            sys.exit(1)

    vec_a = tfidf_vector(corpus.get(name_a, Counter()), idf)
    vec_b = tfidf_vector(corpus.get(name_b, Counter()), idf)

    raw_sim = cosine_similarity(vec_a, vec_b)
    shared = set(vec_a) & set(vec_b)

    domain_a = get_domain(skills[name_a])
    domain_b = get_domain(skills[name_b])
    level_a = get_level(skills[name_a])
    level_b = get_level(skills[name_b])

    # Apply the same boosts as find_bridge_candidates
    boosted_sim = raw_sim
    boosts = []

    adjacency = build_domain_adjacency(registry)
    pair = tuple(sorted([domain_a, domain_b]))
    if pair in adjacency:
        boosted_sim *= 1.3
        boosts.append("domain adjacency ×1.3")

    if level_a == level_b:
        boosted_sim *= 1.1
        boosts.append("role match ×1.1")

    meta_domains = {"infrastructure", "neocortex", "_meta"}
    if (domain_a in meta_domains) != (domain_b in meta_domains):
        boosted_sim *= 0.6
        boosts.append("meta penalty ×0.6")

    print(f"SIMILARITY DEBUG — {name_a} ↔ {name_b}")
    print(f"{'=' * 55}")
    print(f"  Domain A:   {domain_a}")
    print(f"  Domain B:   {domain_b}")
    print(f"  Level A:    {level_a}")
    print(f"  Level B:    {level_b}")
    print(f"  Raw cosine: {raw_sim:.4f}")
    print(f"  Boosted:    {boosted_sim:.4f}  ({', '.join(boosts) if boosts else 'no boosts'})")
    print(f"  Threshold:  0.0500  → {'PASS' if boosted_sim >= 0.05 else 'FAIL'}")
    print(f"  Shared terms ({len(shared)}):")

    ranked = sorted(shared, key=lambda w: -(vec_a[w] + vec_b[w]))
    for w in ranked[:15]:
        print(f"    {w:25s}  A={vec_a[w]:.4f}  B={vec_b[w]:.4f}")

    print(f"\n  Top A terms (unique):")
    for w in sorted(set(vec_a) - shared, key=lambda w: -vec_a[w])[:10]:
        print(f"    {w:25s}  {vec_a[w]:.4f}")
    print(f"\n  Top B terms (unique):")
    for w in sorted(set(vec_b) - shared, key=lambda w: -vec_b[w])[:10]:
        print(f"    {w:25s}  {vec_b[w]:.4f}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    registry = load_registry()

    if sys.argv[1] == "--scan-all":
        missing = scan_all_missing(registry)
        if missing:
            by_domain = defaultdict(list)
            for m in missing:
                by_domain[m["domain"]].append(m["name"])
            print(f"SKILLS WITHOUT CROSS-DOMAIN BRIDGES: {len(missing)}")
            for domain, names in sorted(by_domain.items()):
                print(f"\n  {domain} ({len(names)}):")
                for n in names:
                    print(f"    - {n}")
        else:
            print("All skills have at least one cross-domain bridge.")
        sys.exit(0)

    if sys.argv[1] == "--test-pair":
        if len(sys.argv) < 4:
            print("Usage: --test-pair <skill-a> <skill-b>")
            sys.exit(1)
        corpus = build_corpus(registry)
        idf = compute_idf(corpus)
        test_pair(sys.argv[2], sys.argv[3], registry, corpus, idf)
        sys.exit(0)

    target_name = sys.argv[1]
    do_apply = "--apply" in sys.argv

    print("Building TF-IDF corpus...", end=" ", flush=True)
    corpus = build_corpus(registry)
    idf = compute_idf(corpus)
    print(f"done ({len(corpus)} skills, {len(idf)} terms)")

    candidates = find_bridge_candidates(target_name, registry, corpus, idf)

    if not candidates:
        print(f"No cross-domain bridge candidates found for '{target_name}'.")
        sys.exit(0)

    print(f"\nBRIDGE SUGGESTIONS — {target_name}")
    print(f"{'=' * 55}")
    for i, c in enumerate(candidates[:10], 1):
        print(f"\n  {i}. {c['name']} ({c['domain']})")
        print(f"     Similarity: {c['similarity']:.1%}")
        print(f"     Shared: {', '.join(c['shared_keywords'][:7])}")

    if do_apply and candidates:
        applied = apply_bridges(target_name, candidates, registry)
        print(f"\n{'=' * 55}")
        print(f"Applied {len(applied)} bridges to registry.")
        print("NOTE: You still need to add Cross-Domain Connections")
        print("sections to the SKILL.md files manually.")


if __name__ == "__main__":
    main()
