FROM python:3.14-slim

WORKDIR /app

# System deps:
#   git -> required by the maintenance router to clone & push bot PRs
#          (Layer 2: /maint/* endpoints operate on fresh clones)
# ca-certificates, curl -> surface useful if a debug shell is ever needed.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python deps. Split across layers so the heavy ML stack is cached
# independently of the lightweight server deps.
#
#   mcp                  -> MCP protocol + FastMCP + transitive Starlette/Uvicorn
#   httpx                -> GitHub API calls from the maintenance router
#   anthropic            -> Claude API calls from kb-pipeline (T1 enrichment)
#   rank-bm25, numpy     -> BM25 signal in HybridSearchIndex
#   google-cloud-firestore -> durable telemetry mirroring (firestore_telemetry.py)
#   torch (CPU-only)     -> required by sentence-transformers; pulled from
#                           PyTorch's CPU index to avoid ~600MB of CUDA wheels
#   sentence-transformers -> vector signal in HybridSearchIndex (MiniLM)
COPY mcp-server/pyproject.toml mcp-server/
RUN pip install --no-cache-dir \
      "mcp>=1.0.0" "httpx>=0.25" "anthropic>=0.30" \
      "rank-bm25>=0.2.2" "numpy>=1.24.0" \
      "google-cloud-firestore>=2.14"
RUN pip install --no-cache-dir \
      --extra-index-url https://download.pytorch.org/whl/cpu \
      "torch>=2.0,<3.0" \
      "sentence-transformers>=2.2.0"

# Pre-download the embedding model into the image so the first request after
# a cold start does not pay a HuggingFace round-trip. ~80MB on disk.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# HuggingFace + Transformers should not phone home — at build time (the
# embedding pre-build below) or at runtime. The MiniLM weights are baked
# into the image; without these flags, sentence-transformers makes a
# revision-check API call to huggingface.co on every model load, which
# times out under Cloud Run cpu-throttling.
ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1

# Copy the full project (skills, data, scripts, mcp-server)
COPY . .

WORKDIR /app/mcp-server

# Pre-build the embedding cache so the first MCP request after a cold
# start doesn't pay the encoding cost (~30s under Cloud Run cpu-throttling
# for ~4.5k chunk embeddings across 509 skills). The cache is schema-v2
# (one vector per body/desc chunk, max-pooled per skill at query time) and
# keyed on a registry content hash; a stale or pre-chunking cache fails
# closed and rebuilds. Editing a skill after this point regenerates on
# first request — the common case (no changes between deploys) hits the
# cache and serves the first request in ~1s.
RUN python -c "import json; from pathlib import Path; \
from search_index import HybridSearchIndex; \
reg = json.loads(Path('/app/data/registry.json').read_text()); \
idx = HybridSearchIndex(Path('/app/skills'), reg, Path('/app/data')); \
status = idx.build(); \
print(f'Pre-built index: {status}'); \
assert status.get('vectors'), f'Embedding pre-build failed: {status}'"

# Cloud Run sets PORT env var; default to 8080
ENV PORT=8080
ENV MCP_REMOTE=true

CMD python server.py --remote --port $PORT
