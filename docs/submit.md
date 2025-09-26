# Submit an Agent

This guide shows how to add a new agent to the hub.

---

## 1) Create your agent folder

Copy the Python template into the monorepo:
`/templates/python-agent` → `/agents/<agent-name>`

Then add/edit:
- `/agents/<agent-name>/agent.yaml` (start from `/templates/agent.yaml`)
- `src/mcp_server.py` (MCP stdio)
- `src/a2a_server.py` (A2A SDK server)
- `pyproject.toml`, `Dockerfile`
- `tests/` (at least a smoke test)

---

## 2) Fill out `agent.yaml`

- Keep `entrypoints.mcp` as **stdio** for Claude Desktop
- Set A2A dev port to **8080** and card path `/.well-known/agent-card.json` for local runs
- Declare at least **one MCP tool** and **one A2A skill**
- List any outbound domains under `security.outbound_network` (e.g., `["api.open-meteo.com"]`)
- If you'll publish a mirrored card to Pages later, you can fill `entrypoints.a2a.publicCardUrl`

---

## 3) Install deps & run locally

Using **uv** (recommended) from your agent folder:

```bash
uv sync

# MCP stdio:
uv run src/mcp_server.py

# A2A server (JSON-RPC over HTTP):
uv run src/a2a_server.py
```

*MCP stdio = JSON-RPC over stdin/stdout. Do not print logs to stdout; use stderr (MCP rule).*

---

## 4) Local validation (before PR)

From the repo root:

```bash
# schema check for all manifests
python scripts/validate_agent_manifest.py

# when your A2A server is running on :8080
python scripts/validate_agent_card.py http://localhost:8080/.well-known/agent-card.json
python scripts/check_a2a_runtime.py http://localhost:8080
```

---

## 5) MCP in Claude Desktop (quick test)

Edit `claude_desktop_config.json` (see OS paths in the MCP consume guide), add your agent under `mcpServers`, restart Claude Desktop, and verify the tool appears.

---

## 6) Open a PR

Include:
- README under `/agents/<agent-name>/`
- Updated `agent.yaml`
- Tests
- CI green
- Checklist in `/templates/PULL_REQUEST_TEMPLATE.md` all checked

---