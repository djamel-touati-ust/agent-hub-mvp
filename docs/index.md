# UST Agent Hub — Docs

- **Submit an agent** → [docs/submit.md](./submit.md)
- **Consume via A2A** → [docs/consume-a2a.md](./consume-a2a.md)
- **Consume via MCP** → [docs/consume-mcp.md](./consume-mcp.md)
- **A2A MVP spec notes** → [docs/a2a-spec.md](./a2a-spec.md)

This hub standardizes:
- **A2A** (Agent-to-Agent) discovery and messaging using an **Agent Card** + **JSON-RPC** (`message/send`).
- **MCP** (Model Context Protocol) tools over **stdio** for desktop LLM hosts (Claude Desktop, etc.).

**Key rules:**
- Each agent MUST implement **both A2A and MCP** surfaces.
- For A2A, **publish** your Agent Card at `/.well-known/agent-card.json` and ensure clients can call `message/send` at the card’s `url`. :contentReference[oaicite:7]{index=7}
- For MCP, use **stdio** transport; **do not print to stdout** (use logging). :contentReference[oaicite:8]{index=8}