# UST Agent Hub (MVP)

A lightweight monorepo to **register, validate, and consume** internal agents that expose:

- **A2A** (Agent-to-Agent): discovery via Agent Card, JSON-RPC `message/send`
- **MCP** (Model Context Protocol): stdio tools for LLM hosts (Claude Desktop, etc.)

## What's here

- `agents/` — example Python agents:
  - `calculator` — A2A + MCP
  - `weather` — A2A + MCP
- `schemas/`
  - `agent.schema.json` — validation for `agent.yaml` (per-agent manifest)
  - `agent-card.schema.json` — validation for Agent Card JSON (for HTTP A2A servers)
- `templates/`
  - `agent.yaml` — manifest template
  - `README.md` — per-agent README template
  - `PULL_REQUEST_TEMPLATE.md` — submission checklist
- `docs/`
  - `index.md` — landing page
  - `submit.md` — how to submit a new agent
  - `consume-a2a.md` — how to call agents via A2A
  - `consume-mcp.md` — how to use MCP via Claude Desktop
  - `a2a-spec.md` — MVP A2A notes
- `scripts/`
  - `validate_agent_manifest.py` — validate all `agent.yaml` files
  - `validate_agent_card.py` — fetch/validate an agent card (optional)
  - `check_a2a_runtime.py` — quick JSON-RPC probe (supports **no-card** and **card** modes)

## Quick start (local)

### A2A (JSON-RPC + Agent Card)

1) Start an agent:
   ```bash
   uv run agents/calculator/src/a2a_server.py
   ```

2) Discover the card:
   ```bash
   curl -s http://localhost:8081/.well-known/agent-card.json | jq .
   ```

3) Call `message/send` at the card's url with a `messageId` and `parts[].kind="text"`:

   **Windows cmd.exe:**
   ```bat
   curl -s http://localhost:8081/ -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"message/send\",\"params\":{\"message\":{\"messageId\":\"test-1\",\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"7*6\"}]}}}"
   ```

A2A servers MUST publish an Agent Card; clients should rely on it for the endpoint URL and capabilities.

### MCP (Claude Desktop)

Edit `%APPDATA%\Claude\claude_desktop_config.json` and add the provided `mcpServers` entries (see `docs/consume-mcp.md`).

Restart Claude Desktop; it will spawn the stdio servers automatically.

## Weather agent note

Uses Open-Meteo for simple daily summaries; no API key required.

## Submitting a new agent

See `docs/submit.md` and use the templates in `templates/`. CI will validate your `agent.yaml` and (optionally) your Agent Card JSON.