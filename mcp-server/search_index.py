"""Hybrid search index for the skill library.

Combines three retrieval signals via Reciprocal Rank Fusion (RRF):
  1. BM25 full-text search over skill content
  2. Vector embeddings (sentence-transformers) for semantic similarity
  3. Graph proximity to recently-used skills

All ML dependencies are optional — the index gracefully degrades to
whichever signals are available.
"""
from __future__ import annotations

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


# ---------------------------------------------------------------------------
# Hybrid search index
# ---------------------------------------------------------------------------

_EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
_RRF_K = 60  # standard constant from Cormack et al. 2009


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

        # Ordered list of skill names — index positions match BM25/vector arrays
        self._names: list[str] = []
        self._bm25: Optional["BM25Okapi"] = None
        self._embeddings: Optional["np.ndarray"] = None
        self._model: Optional["SentenceTransformer"] = None

        # Adjacency list for graph proximity (undirected)
        self._adj: dict[str, set[str]] = defaultdict(set)

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> dict:
        """Build all available indexes. Returns a status dict."""
        t0 = time.monotonic()
        skills = self._skills
        self._names = []
        corpus_tokens: list[list[str]] = []
        corpus_texts: list[str] = []

        for name, entry in sorted(skills.items()):
            if entry.get("status") != "active":
                continue
            location = entry.get("location", "")
            skill_dir = (self.skills_dir.parent / location).parent
            if not skill_dir.is_dir():
                continue

            text = _extract_skill_text(skill_dir)
            desc = entry.get("description", "")
            full_text = f"{name} {desc} {text}"

            self._names.append(name)
            corpus_tokens.append(_tokenize(full_text))
            # For embeddings: description + first ~200 words of body
            body_words = text.split()[:200]
            corpus_texts.append(f"{name}: {desc}. {' '.join(body_words)}")

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

        # Vector embeddings
        if HAS_VECTORS and corpus_texts:
            self._embeddings = self._build_or_load_embeddings(corpus_texts)
            status["vectors"] = self._embeddings is not None

        elapsed = time.monotonic() - t0
        status["build_time_ms"] = round(elapsed * 1000)
        return status

    def _build_or_load_embeddings(self, corpus_texts: list[str]) -> Optional["np.ndarray"]:
        """Load cached embeddings if registry hasn't changed, else rebuild."""
        embed_path = self.data_dir / "skill_embeddings.npy"
        names_path = self.data_dir / "skill_embed_names.json"
        mtime_path = self.data_dir / "skill_embed_mtime.json"

        registry_mtime = _get_registry_mtime(self.data_dir)

        # Check cache validity
        if embed_path.exists() and names_path.exists() and mtime_path.exists():
            try:
                cached_mtime = json.loads(mtime_path.read_text()).get("mtime", 0)
                cached_names = json.loads(names_path.read_text())
                if cached_mtime == registry_mtime and cached_names == self._names:
                    return np.load(str(embed_path))
            except (json.JSONDecodeError, ValueError, OSError, EOFError):
                pass

        # Rebuild embeddings
        try:
            if self._model is None:
                self._model = SentenceTransformer(_EMBED_MODEL_NAME)
            embeddings = self._model.encode(corpus_texts, show_progress_bar=False)
            embeddings = np.array(embeddings, dtype=np.float32)

            # Persist atomically
            _atomic_write_npy(embed_path, embeddings)
            _atomic_write_json(names_path, self._names)
            _atomic_write_json(mtime_path, {"mtime": registry_mtime})

            return embeddings
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
    ) -> list[dict]:
        """Hybrid search with RRF fusion.

        Args:
            query:          Natural language or keyword query.
            recent_skills:  Recently-used skill names for graph proximity boost.
            limit:          Max results to return.

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

        # Signal 2: Vector similarity
        if self._embeddings is not None and self._model is not None:
            try:
                q_embed = self._model.encode([query], show_progress_bar=False)
                q_embed = np.array(q_embed, dtype=np.float32)
                # Cosine similarity
                norms = np.linalg.norm(self._embeddings, axis=1, keepdims=True)
                norms = np.where(norms == 0, 1, norms)
                normed = self._embeddings / norms
                q_norm = q_embed / np.where(
                    np.linalg.norm(q_embed) == 0, 1, np.linalg.norm(q_embed)
                )
                sims = (normed @ q_norm.T).flatten()
                indexed = sorted(enumerate(sims), key=lambda x: -x[1])
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

def _get_registry_mtime(data_dir: Path) -> float:
    """Get registry.json mtime for cache invalidation."""
    reg = data_dir / "registry.json"
    try:
        return reg.stat().st_mtime
    except OSError:
        return 0.0


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
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=path.parent, suffix=".json.tmp", delete=False
        ) as f:
            json.dump(data, f)
            tmp = f.name
        os.replace(tmp, path)
    except OSError:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        raise
