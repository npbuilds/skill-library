FROM python:3.12-slim

WORKDIR /app

# System deps:
#   git -> required by the maintenance router to clone & push bot PRs
#          (Layer 2: /maint/* endpoints operate on fresh clones)
# ca-certificates, curl -> surface useful if a debug shell is ever needed.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python deps:
#   mcp  -> MCP protocol + FastMCP + transitive Starlette/Uvicorn
#   httpx -> GitHub API calls from the maintenance router
COPY mcp-server/pyproject.toml mcp-server/
RUN pip install --no-cache-dir "mcp>=1.0.0" "httpx>=0.25"

# Copy the full project (skills, data, scripts, mcp-server)
COPY . .

WORKDIR /app/mcp-server

# Cloud Run sets PORT env var; default to 8080
ENV PORT=8080
ENV MCP_REMOTE=true

CMD python server.py --remote --port $PORT
