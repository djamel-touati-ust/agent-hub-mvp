# Consume via MCP (Claude Desktop)

## 1) Where is the config?

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

*(You can also open it from Claude Desktop → **Settings → Developer → Edit Config**, then restart.)*

## 2) Add your agent (copy–paste)

Update your JSON to include an entry like this (set an **absolute path**):

```json
{
  "mcpServers": {
    "<agent_name>": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABS/PATH/ust-agent-hub-mvp/agents/<agent_name>",
        "run",
        "src/mcp_server.py"
      ]
    }
  }
}
```

Restart Claude Desktop; the tool should appear automatically under MCP.

## 3) Troubleshooting

- Path must be absolute and the directory must contain your `src/mcp_server.py`
- Run the server manually to surface errors:

```bash
uv run src/mcp_server.py
```

- **Stdio rule:** MCP servers must not write logs to stdout (protocol frames only). Log to stderr.