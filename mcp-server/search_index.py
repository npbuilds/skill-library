"""Hybrid search index for the skill library.

Combines three retrieval signals via Reciprocal Rank Fusion (RRF):
  1. BM25 full-text search over skill content
  2. Vector embeddings (sentence-transformers) for semantic similarity
  3. Graph proximity to recently-used skills

All ML dependencies are optional — the index gracefully degrades to
whichever signals are available.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import logging
import os
import re
import tempfile
import time
from collections import defaultdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Optional dependency detection
# ---------------------------------------------------------------------------

HAS_BM25 = False
HAS_NUMPY = False
HAS_VECTORS = False

try:
    from rank_bm25 import BM25Okapi  # type: ignore[import-untyped]
    HAS_BM25 = True
except ImportError:
    pass

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None  # type: ignore[assignment]

# sentence-transformers is the heavy dep (pulls PyTorch). Track it
# independently of numpy so lighter callers — the atomic-write helper, the
# unit tests — can use numpy even when the embedding stack is absent.
try:
    from sentence_transformers import SentenceTransformer  # type: ignore[import-untyped]
    HAS_VECTORS = HAS_NUMPY
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Text extraction
# ---------------------------------------------------------------------------

_STRIP_FM_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def _extract_skill_text(skill_dir: Path) -> str:
    """Read SKILL.md + reference docs, strip frontmatter, return plain text."""
    parts = []

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        raw = skill_md.read_text(errors="replace")
        body = _STRIP_FM_RE.sub("", raw, count=1)
        parts.append(body)

    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.iterdir()):
            if ref_file.suffix == ".md" and ref_file.is_file():
                parts.append(ref_file.read_text(errors="replace"))

    return "\n\n".join(parts)


def _tokenize(text: str) -> list[str]:
    """Lowercase, split on non-alphanumeric, drop tokens shorter than 3 chars."""
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if len(t) >= 3]


# Body is split on ## headings then re-packed into word-bounded passages.
# 150 words ≈ 200 tokens, within MiniLM's 256-token window before truncation.
_BODY_MAX_WORDS = 150
_BODY_MAX_CHUNKS = 8
_HEADING_RE = re.compile(r"^#{2,}\s", re.MULTILINE)


def _split_passages(body: str, max_words: int = _BODY_MAX_WORDS,
                    max_chunks: int = _BODY_MAX_CHUNKS) -> list[str]:
    """Split body text into heading-aware, word-bounded passages.

    Splits on ## (or deeper) headings first, then packs sections into
    passages of at most ``max_words`` words. A single oversized section is
    chunked across multiple passages. Returns at most ``max_chunks``
    passages so a sprawling skill can't dominate the embedding matrix.
    """
    # Split at heading boundaries, keeping the heading with its section.
    sections = _HEADING_RE.split(body)
    passages: list[str] = []
    for section in sections:
        words = section.split()
        if not words:
            continue
        for i in range(0, len(words), max_words):
            passages.append(" ".join(words[i:i + max_words]))
            if len(passages) >= max_chunks:
                return passages
    return passages


# Number of body chars folded into the synthetic-query content hash. Must
# match scripts/generate_synthetic_queries.py (which imports the hash below),
# so a regenerated query set and the index agree on what "unchanged" means.
SYNTHETIC_BODY_EXCERPT_CHARS = 1200


def synthetic_content_hash(desc: str, skill_md_text: str) -> str:
    """Canonical hash of a skill's content for synthetic-query staleness.

    Hashes the description plus the frontmatter-stripped SKILL.md body
    (capped at SYNTHETIC_BODY_EXCERPT_CHARS). The generator stamps this hash
    onto each skill's queries; the index recomputes it and skips queries whose
    hash no longer matches, so editing a skill without rerunning the generator
    doesn't index stale expansions that describe the old meaning.
    """
    body = _STRIP_FM_RE.sub("", skill_md_text, count=1).strip()[:SYNTHETIC_BODY_EXCERPT_CHARS]
    return hashlib.sha256((desc + "\x00" + body).encode("utf-8")).hexdigest()


def _load_synthetic_queries(data_dir: Path) -> dict[str, dict]:
    """Load synthetic-query entries per skill from data/synthetic_queries.json.

    Returns {skill_name: {"content_hash": str, "index_queries": [str]}} for
    skills with non-empty index_queries (eval_queries are held out for the
    retrieval eval and must never be indexed). Missing/unreadable file → {}.
    Freshness is validated by the caller against the live skill content.
    """
    path = data_dir / "synthetic_queries.json"
    try:
        payload = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    out: dict[str, dict] = {}
    for name, entry in payload.get("skills", {}).items():
        qs = entry.get("index_queries") or []
        if isinstance(qs, list) and qs:
            out[name] = {
                "content_hash": entry.get("content_hash", ""),
                "index_queries": [str(q) for q in qs],
            }
    return out


def _extract_chunks(skill_dir: Path, name: str, desc: str) -> list[tuple[str, str]]:
    """Build (chunk_kind, embed_text) pairs for one skill.

    chunk 0 is the routing-critical "name: description" line; the rest are
    body passages. Each text is name-prefixed so a passage carries its
    skill identity into the embedding. References stay BM25-only (they
    bloat the vector matrix without improving routing precision).
    """
    chunks: list[tuple[str, str]] = [("desc", f"{name}: {desc}")]

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        raw = skill_md.read_text(errors="replace")
        body = _STRIP_FM_RE.sub("", raw, count=1)
        for i, passage in enumerate(_split_passages(body)):
            chunks.append((f"body:{i}", f"{name}: {passage}"))

    return chunks


# ---------------------------------------------------------------------------
# Hybrid search index
# ---------------------------------------------------------------------------

_EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_RRF_K = 60  # standard constant from Cormack et al. 2009

# Embedding cache schema version. Bump when the row layout changes (e.g.
# one-vector-per-skill → one-vector-per-chunk) so stale caches fail closed
# and rebuild instead of mis-mapping rows to skills.
_EMBED_CACHE_SCHEMA = 2

# Body-passage chunks are down-weighted relative to the "name: description"
# chunk when max-pooling per skill. The description is the routing-critical
# signal (Anthropic Agent Skills guidance); body chunks give every skill 8
# extra chances to match, which surfaces semantically-adjacent wrong skills
# if left at parity. At 0.85 a body passage only outranks a description match
# when it's a markedly stronger semantic hit — so chunks rescue desc misses
# without outvoting good desc matches. Tuned against scripts/eval_retrieval.py.
_BODY_CHUNK_WEIGHT = 0.85

# RRF score floor. Below this, a "match" is single-signal noise (e.g., vector
# similarity scraping the long tail). With k=60: single-signal rank-1 ≈ 0.0164,
# two-signal rank-1 ≈ 0.0328. A floor of 0.02 lets through anything strong
# enough to hit two signals or top-rank one, and filters everything else so
# the gap-detection feature stays meaningful.
#
# When only ONE signal produces rankings for a query (e.g. BM25-only because
# vectors aren't installed and there are no recent skills to seed the graph),
# a 0.02 floor filters even the rank-1 result (1/61 ≈ 0.0164) — search would
# return [] and the server would fall back to weak keyword matching. The floor
# is scaled by _SINGLE_SIGNAL_FLOOR_FACTOR in that case so top single-signal
# hits survive. With ≥2 signals ranking, the full floor applies: a hit
# corroborated by two signals clears 0.02 easily, and a lone single-signal
# long-tail match is correctly dropped (keeping gap detection meaningful).
_MIN_RRF_SCORE = 0.02
_SINGLE_SIGNAL_FLOOR_FACTOR = 0.6  # 0.02 * 0.6 = 0.012 < 0.0164 rank-1


class HybridSearchIndex:
    """Three-signal hybrid search with RRF fusion.

    Signals:
        1. BM25 over tokenized skill content (requires rank-bm25)
        2. Cosine similarity of sentence-transformer embeddings (requires
           sentence-transformers + numpy)
        3. Graph proximity to recently-used skills (no deps)
    """

    def __init__(self, skills_dir: Path, registry: dict, data_dir: Path):
        self.skills_dir = skills_dir
        self.data_dir = data_dir
        self._registry = registry
        self._skills = registry.get("skills", {})

        # Ordered list of skill names — index positions match BM25 corpus rows.
        self._names: list[str] = []
        # Per-skill index for each embedding row: embeddings are CHUNKED
        # (multiple rows per skill), so row i belongs to skill
        # self._names[self._chunk_skill_idx[i]].
        self._chunk_skill_idx: list[int] = []
        # Per-row pooling weight: 1.0 for the description chunk, _BODY_CHUNK_WEIGHT
        # for body passages (parallel to embedding rows).
        self._chunk_weight: list[float] = []
        self._bm25: Optional["BM25Okapi"] = None
        self._embeddings: Optional["np.ndarray"] = None
        self._model: Optional["SentenceTransformer"] = None

        # Adjacency list for graph proximity (undirected)
        self._adj: dict[str, set[str]] = defaultdict(set)

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, build_vectors: bool = True) -> dict:
        """Build all available indexes. Returns a status dict.

        build_vectors=False skips the (expensive) embedding build/load entirely
        — used by callers that only want BM25 + graph (e.g. the CI eval in
        bm25,graph mode), so they don't pay the model download/encode cost just
        to discard the vectors afterward.
        """
        t0 = time.monotonic()
        skills = self._skills
        self._names = []
        self._chunk_skill_idx = []
        self._chunk_weight = []
        # Chunk keys (skill, kind) parallel to embedding rows — persisted so a
        # loaded cache can be validated against the current skill set.
        chunk_keys: list[tuple[str, str]] = []
        corpus_tokens: list[list[str]] = []
        corpus_texts: list[str] = []

        # Synthetic user queries (Re-Invoke doc expansion) — index_queries only.
        synthetic = _load_synthetic_queries(self.data_dir)

        for name, entry in sorted(skills.items()):
            if entry.get("status") != "active":
                continue
            location = entry.get("location", "")
            skill_dir = (self.skills_dir.parent / location).parent
            if not skill_dir.is_dir():
                continue

            text = _extract_skill_text(skill_dir)
            desc = entry.get("description", "")

            # Synthetic queries are only used when their stored content hash
            # still matches the live skill — otherwise they describe the skill's
            # old meaning and are skipped until the generator is rerun.
            syn_entry = synthetic.get(name)
            syn_queries: list[str] = []
            if syn_entry:
                try:
                    raw_md = (skill_dir / "SKILL.md").read_text(errors="replace")
                    if syn_entry["content_hash"] == synthetic_content_hash(desc, raw_md):
                        syn_queries = syn_entry["index_queries"]
                except OSError:
                    pass

            # Synthetic queries join the BM25 doc so keyword search benefits
            # from user-phrased vocabulary too.
            full_text = f"{name} {desc} {text} {' '.join(syn_queries)}"

            skill_idx = len(self._names)
            self._names.append(name)
            corpus_tokens.append(_tokenize(full_text))

            # For embeddings: one row per chunk (desc + body passages + each
            # synthetic query), mapped back to this skill so query-time
            # max-pooling collapses them into a single per-skill similarity.
            chunks = _extract_chunks(skill_dir, name, desc)
            for j, q in enumerate(syn_queries):
                chunks.append((f"q:{j}", f"{name}: {q}"))
            for kind, chunk_text in chunks:
                chunk_keys.append((name, kind))
                self._chunk_skill_idx.append(skill_idx)
                # desc and synthetic-query chunks are full-weight routing
                # signals; body passages are down-weighted (see constant).
                self._chunk_weight.append(
                    _BODY_CHUNK_WEIGHT if kind.startswith("body:") else 1.0
                )
                corpus_texts.append(chunk_text)

        # Build adjacency graph
        self._adj.clear()
        name_set = set(self._names)
        for name in self._names:
            entry = skills[name]
            for dep in entry.get("depends_on", []):
                if dep in name_set:
                    self._adj[name].add(dep)
                    self._adj[dep].add(name)
            for ref in entry.get("referenced_by", []):
                if ref in name_set:
                    self._adj[name].add(ref)
                    self._adj[ref].add(name)

        status = {
            "skills_indexed": len(self._names),
            "bm25": False,
            "vectors": False,
            "graph": True,
        }

        # BM25
        if HAS_BM25 and corpus_tokens:
            self._bm25 = BM25Okapi(corpus_tokens)
            status["bm25"] = True

        # Vector embeddings (chunked: rows ≥ skills)
        if build_vectors and HAS_VECTORS and corpus_texts:
            self._embeddings = self._build_or_load_embeddings(corpus_texts, chunk_keys)
            status["vectors"] = self._embeddings is not None
            status["chunks_indexed"] = len(corpus_texts)

        elapsed = time.monotonic() - t0
        status["build_time_ms"] = round(elapsed * 1000)
        return status

    def _build_or_load_embeddings(
        self,
        corpus_texts: list[str],
        chunk_keys: list[tuple[str, str]],
    ) -> Optional["np.ndarray"]:
        """Load cached chunk embeddings if still valid, else rebuild.

        Cache is keyed on a SHA256 hash of registry.json (content, not
        mtime — robust across Docker overlayfs builds). The names sidecar
        stores the parallel ``chunk_keys`` ([[skill, kind], ...]); a schema
        marker guards against loading a pre-chunking (v1) cache whose row
        layout no longer matches. Either mismatch fails closed → rebuild.
        """
        embed_path = self.data_dir / "skill_embeddings.npy"
        names_path = self.data_dir / "skill_embed_names.json"
        # Filename retained for back-compat; payload is now {"hash", "schema"}.
        key_path = self.data_dir / "skill_embed_mtime.json"

        registry_hash = _get_registry_hash(self.data_dir)
        # chunk_keys is a list of tuples; JSON round-trips them to lists.
        expected_keys = [list(k) for k in chunk_keys]

        def _load_valid_cache() -> Optional["np.ndarray"]:
            if not (embed_path.exists() and names_path.exists() and key_path.exists()):
                return None
            try:
                meta = json.loads(key_path.read_text())
                if meta.get("schema") != _EMBED_CACHE_SCHEMA:
                    return None  # v1 (or unknown) cache — row layout differs
                cached_hash = meta.get("hash", "")
                cached_keys = json.loads(names_path.read_text())
                if cached_hash and cached_hash == registry_hash and cached_keys == expected_keys:
                    return np.load(str(embed_path))
            except (json.JSONDecodeError, ValueError, OSError, EOFError):
                pass
            return None

        cached = _load_valid_cache()
        if cached is not None:
            return cached

        # Rebuild embeddings under an exclusive lock so concurrent builders
        # (e.g. two server processes starting at once) don't interleave
        # writes to the cache files. Double-checked: another process may
        # have finished the rebuild while we waited on the lock.
        lock_path = self.data_dir / ".embed_rebuild.lock"
        try:
            with open(lock_path, "a") as lock_f:
                fcntl.flock(lock_f, fcntl.LOCK_EX)
                try:
                    cached = _load_valid_cache()
                    if cached is not None:
                        return cached

                    if self._model is None:
                        self._model = SentenceTransformer(_EMBED_MODEL_NAME)
                    embeddings = self._model.encode(corpus_texts, show_progress_bar=False)
                    embeddings = np.array(embeddings, dtype=np.float32)

                    # Persist atomically
                    _atomic_write_npy(embed_path, embeddings)
                    _atomic_write_json(names_path, expected_keys)
                    _atomic_write_json(
                        key_path, {"hash": registry_hash, "schema": _EMBED_CACHE_SCHEMA}
                    )

                    return embeddings
                finally:
                    fcntl.flock(lock_f, fcntl.LOCK_UN)
        except Exception as e:
            logger.warning("Failed to build embeddings: %s", e)
            return None

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        recent_skills: list[str] | None = None,
        limit: int = 15,
        min_score: float = _MIN_RRF_SCORE,
    ) -> list[dict]:
        """Hybrid search with RRF fusion.

        Args:
            query:          Natural language or keyword query.
            recent_skills:  Recently-used skill names for graph proximity boost.
            limit:          Max results to return.
            min_score:      RRF score floor; matches below this are dropped as
                            single-signal noise. Pass 0 to disable filtering.

        Returns list of dicts: [{"name", "rrf_score", "signals"}]
        """
        if not self._names:
            return []

        ranked_by_signal: dict[str, list[str]] = {}

        # Signal 1: BM25
        if self._bm25 is not None:
            tokens = _tokenize(query)
            if tokens:
                scores = self._bm25.get_scores(tokens)
                indexed = sorted(
                    enumerate(scores), key=lambda x: -x[1]
                )
                bm25_ranked = [
                    self._names[i] for i, s in indexed if s > 0
                ][:limit * 3]
                if bm25_ranked:
                    ranked_by_signal["bm25"] = bm25_ranked

        # Signal 2: Vector similarity (chunked + max-pooled per skill)
        # Lazy-load the model on first vector search. The cache-hit path in
        # _build_or_load_embeddings sets self._embeddings without loading the
        # model — but the model is needed here to encode the *query*.
        if self._embeddings is not None and HAS_VECTORS:
            try:
                if self._model is None:
                    self._model = SentenceTransformer(_EMBED_MODEL_NAME)
                q_embed = self._model.encode([query], show_progress_bar=False)
                q_embed = np.array(q_embed, dtype=np.float32)
                # Cosine similarity over every chunk row.
                norms = np.linalg.norm(self._embeddings, axis=1, keepdims=True)
                norms = np.where(norms == 0, 1, norms)
                normed = self._embeddings / norms
                q_norm = q_embed / np.where(
                    np.linalg.norm(q_embed) == 0, 1, np.linalg.norm(q_embed)
                )
                chunk_sims = (normed @ q_norm.T).flatten()
                # Down-weight body passages so the description chunk anchors
                # routing; body chunks only win when markedly stronger.
                chunk_sims = chunk_sims * np.asarray(self._chunk_weight, dtype=np.float32)
                # Max-pool chunk similarities into one score per skill: a query
                # matches a single passage, so the best-matching chunk defines
                # the skill's relevance (mean would dilute it across sections).
                pooled = np.full(len(self._names), -1.0, dtype=np.float32)
                np.maximum.at(
                    pooled, np.asarray(self._chunk_skill_idx, dtype=np.intp), chunk_sims
                )
                indexed = sorted(enumerate(pooled), key=lambda x: -x[1])
                vec_ranked = [
                    self._names[i] for i, s in indexed if s > 0.1
                ][:limit * 3]
                if vec_ranked:
                    ranked_by_signal["vector"] = vec_ranked
            except Exception as e:
                logger.warning("Vector search failed: %s", e)

        # Signal 3: Graph proximity to recent skills
        if recent_skills:
            graph_ranked = self._graph_proximity_rank(recent_skills, limit * 3)
            if graph_ranked:
                ranked_by_signal["graph"] = graph_ranked

        if not ranked_by_signal:
            return []

        # RRF fusion
        fused = self._rrf_fuse(*ranked_by_signal.values())

        # Drop sub-threshold matches before applying the result limit so the
        # caller sees a clean "no real hits" empty list (which lets gap-
        # detection downstream actually fire on unmatchable queries).
        #
        # The floor is scaled down only when the index is STRUCTURALLY limited
        # to a single signal for this query (e.g. BM25-only because vectors
        # aren't installed and no recent skills seed the graph). There the
        # rank-1 RRF (1/61 ≈ 0.0164) would be filtered wholesale.
        #
        # Keyed on signals *capable* of corroborating, not on how many fired:
        # if two signals are available but only one matched, that lack of
        # corroboration is itself the gap signal — keep the full floor so the
        # weak single-signal match is dropped and out-of-scope queries come
        # back empty (gap detection). Only when ≤1 signal could corroborate do
        # we lower the floor so the best-effort match survives.
        #
        # BM25 and vectors score *every* skill, so "available" (index built)
        # means they would rank any query with signal — availability is the
        # right test. Graph is different: it can be seeded (recent_skills given)
        # yet rank nothing (isolated/stale seed), so count it only when it
        # actually produced a ranking. Otherwise a BM25-only install with a
        # dead graph seed would falsely read as 2 signals and filter valid
        # single-signal BM25 results to empty.
        capable_signals = (
            (1 if self._bm25 is not None else 0)
            + (1 if (self._embeddings is not None and HAS_VECTORS) else 0)
            + (1 if "graph" in ranked_by_signal else 0)
        )
        if min_score > 0:
            effective_floor = (
                min_score
                if capable_signals >= 2
                else min_score * _SINGLE_SIGNAL_FLOOR_FACTOR
            )
            fused = [(name, score) for name, score in fused if score >= effective_floor]

        results = []
        for name, score in fused[:limit]:
            results.append({
                "name": name,
                "rrf_score": round(score, 5),
                "signals": {
                    sig: name in rlist
                    for sig, rlist in ranked_by_signal.items()
                },
            })
        return results

    def _graph_proximity_rank(
        self, seeds: list[str], limit: int
    ) -> list[str]:
        """BFS from seed skills, rank neighbors by inverse hop distance."""
        visited: set[str] = set()
        # depth -> list of skills
        depth_buckets: dict[int, list[str]] = defaultdict(list)
        frontier = set(s for s in seeds if s in self._adj)
        visited.update(frontier)

        for depth in range(1, 4):  # max 3 hops
            next_frontier: set[str] = set()
            for s in frontier:
                for neighbor in self._adj.get(s, set()):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_frontier.add(neighbor)
                        depth_buckets[depth].append(neighbor)
            frontier = next_frontier
            if not frontier:
                break

        # Flatten: closer hops first
        ranked = []
        for depth in sorted(depth_buckets):
            ranked.extend(depth_buckets[depth])
        return ranked[:limit]

    @staticmethod
    def _rrf_fuse(*ranked_lists: list[str], k: int = _RRF_K) -> list[tuple[str, float]]:
        """Reciprocal Rank Fusion across multiple ranked lists."""
        scores: dict[str, float] = defaultdict(float)
        for rlist in ranked_lists:
            for rank, name in enumerate(rlist):
                scores[name] += 1.0 / (k + rank + 1)
        return sorted(scores.items(), key=lambda x: -x[1])

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    @property
    def is_ready(self) -> bool:
        return len(self._names) > 0

    @property
    def signal_count(self) -> int:
        count = 0
        if self._bm25 is not None:
            count += 1
        if self._embeddings is not None:
            count += 1
        count += 1  # graph is always available
        return count

    def status_summary(self) -> str:
        parts = [f"{len(self._names)} skills indexed"]
        parts.append(f"BM25: {'ready' if self._bm25 else 'unavailable'}")
        parts.append(f"Vectors: {'ready' if self._embeddings is not None else 'unavailable'}")
        parts.append(f"Graph: ready ({sum(len(v) for v in self._adj.values()) // 2} edges)")
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def _get_registry_hash(data_dir: Path) -> str:
    """Composite content hash of the inputs that determine the embeddings.

    Hashes registry.json plus synthetic_queries.json (if present), so that
    regenerating synthetic queries invalidates the embedding cache and
    forces a rebuild. A content hash is robust across Docker image builds
    and overlay filesystems, where mtime semantics are unreliable. If the
    registry is missing or unreadable, returns the empty string (which
    won't match any persisted hash, so the cache check fails closed).
    """
    reg = data_dir / "registry.json"
    try:
        h = hashlib.sha256(reg.read_bytes())
    except OSError:
        return ""
    # Synthetic queries are optional; fold them in when present.
    try:
        h.update(b"\x00synthetic\x00")
        h.update((data_dir / "synthetic_queries.json").read_bytes())
    except OSError:
        pass
    return h.hexdigest()


def _atomic_write_npy(path: Path, arr: "np.ndarray") -> None:
    # np.save auto-appends ".npy" if the path doesn't already end in it,
    # which means a tempfile created with suffix=".npy.tmp" gets the array
    # written to a *different* path (...".npy.tmp.npy") while os.replace
    # then renames the empty stub. Use a ".npy" suffix so np.save writes
    # in place.
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".npy")
        os.close(fd)
        np.save(tmp, arr)
        os.replace(tmp, path)
    except OSError:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        raise


def _atomic_write_json(path: Path, data) -> None:
    # Capture tmp name BEFORE json.dump so cleanup runs even if dump raises
    # (e.g. TypeError on non-serializable data). Without this, a failed dump
    # would leak the NamedTemporaryFile(delete=False) on disk.
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".json.tmp", delete=False
        ) as f:
            tmp = f.name
            json.dump(data, f)
        os.replace(tmp, path)
    except (OSError, TypeError, ValueError):
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        raise
