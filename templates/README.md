# <Agent Name>

Short description.

## Surfaces

### A2A

- **Card**: `GET /.well-known/agent-card.json`
- **RPC URL**: from the card's `url` (often `/`)
- **Method**: `message/send` (requires `messageId`, `parts[].kind="text"`)

### MCP

- `src/mcp_server.py` (FastMCP stdio)
- **Tool names**: see function names in server

## Local run

```bash
uv run src/a2a_server.py
# then:
curl -s http://localhost:<port>/.well-known/agent-card.json | jq .
```

**Claude Desktop MCP config:**

```json
{
  "mcpServers": {
    "<agent-id>": {
      "command": "uv",
      "args": ["--directory", "C:/ABSOLUTE/PATH/agents/<name>", "run", "src/mcp_server.py"]
    }
  }
}
```