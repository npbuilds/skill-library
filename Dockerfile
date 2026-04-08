FROM python:3.12-slim

WORKDIR /app

# Install MCP server dependencies
COPY mcp-server/pyproject.toml mcp-server/
RUN pip install --no-cache-dir mcp>=1.0.0

# Copy the full project (skills, data, scripts, mcp-server)
COPY . .

WORKDIR /app/mcp-server

# Cloud Run sets PORT env var; default to 8080
ENV PORT=8080
ENV MCP_REMOTE=true

CMD python server.py --remote --port $PORT
