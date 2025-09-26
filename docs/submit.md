# Submit an Agent

## Requirements
- Provide **both** surfaces:
  - **A2A**: HTTP JSON-RPC with `message/send`; card at `/.well-known/agent-card.json`. Clients post to the **`url` in the card**. :contentReference[oaicite:16]{index=16}
  - **MCP**: stdio server (FastMCP). No stdout printing. :contentReference[oaicite:17]{index=17}
- Containerize the A2A surface (Dockerfile); publish image to GHCR via CI.
- Add `agent.yaml` (see template) and a per-agent `README.md`.

## Steps
1) Fork `templates/agent.yaml` and `templates/README.md` into `agents/<name>/`.
2) Implement:
   - `src/app.py` — business logic
   - `src/a2a_server.py` — A2A transport (Agent Card + JSON-RPC)
   - `src/mcp_server.py` — MCP stdio tools
3) Run locally:
   - A2A:
     ```bash
     uv run agents/<name>/src/a2a_server.py
     curl -s http://localhost:<port>/.well-known/agent-card.json | jq .
     ```
   - MCP (Claude Desktop): configure, restart, and verify tools appear.
4) Add a **Dockerfile** for A2A and ensure it boots with `python -u src/a2a_server.py`.
5) Open a PR and fill the **PR template**; CI will validate manifests and cards.