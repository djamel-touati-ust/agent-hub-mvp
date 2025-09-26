# <Agent Name> — Submission Template

## Overview
1–2 sentences on what the agent does.

## Capabilities
- MCP tool(s): `<namespace.tool>` …
- A2A skill(s): `<namespace.skill>` …

## Requirements
- Python 3.11+
- One of:
  - [uv](https://docs.astral.sh/uv/) (recommended), or
  - Poetry, or `python -m venv` + `pip`.

## Local Dev – MCP (stdio)

```bash
uv sync  # or: poetry install / pip install -r requirements.txt
uv run src/mcp_server.py
```

### Claude Desktop config (copy-paste)

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "<agent_name>": {
      "command": "uv",
      "args": ["--directory", "/ABS/PATH/ust-agent-hub-mvp/agents/<agent_name>", "run", "src/mcp_server.py"]
    }
  }
}
```

*(MCP stdio servers must not write logs to stdout; log to stderr.)*

## Local Dev – A2A (SDK server)

Run the A2A SDK server (Starlette + JSON-RPC):

```bash
uv run src/a2a_server.py
```

**Agent Card:**
```bash
curl -s http://localhost:8080/.well-known/agent-card.json | jq .
```

**message/send (JSON-RPC):**
```bash
curl -s http://localhost:8080/a2a/v1 \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"1","method":"message/send",
       "params":{"message":{"role":"user","parts":[{"kind":"text","text":"ping"}]}}}'
```

## Container

```bash
docker build -t ghcr.io/<org>/<agent>:dev .
```

## Security

No secrets in code or agent.yaml. Declare env vars under `env.required`.
Document outbound URLs under `security.outbound_network`.

## Testing

Add minimal tests in `tests/`. CI will run them.

---

## `templates/python-agent/pyproject.toml` ✅ **REPLACE**

*(Use the A2A SDK + MCP; Poetry style; works fine with `uv` too.)*

```toml
[tool.poetry]
name = "python-agent-template"
version = "0.1.0"
description = "UST Agent template (Python + A2A SDK + MCP stdio)"
authors = ["UST Platform <agent-hub@ust.com>"]
package-mode = false

[tool.poetry.dependencies]
python = "^3.11"
uvicorn = "^0.30.0"
pydantic = "^2.8.0"
httpx = "^0.27.0"
# A2A Python SDK (HTTP server helpers + types)
a2a-sdk = {version = "^0.3.0", extras = ["http-server"]}
# MCP python SDK (stdio helpers)
mcp = "^1.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.0"
ruff = "^0.6.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```