# UST Weather Agent

Weather helper that exposes:

- **A2A**: Agent Card discovery + JSON-RPC `message/send` (input: `"lat,lon"`)
- **MCP**: stdio tool for Claude Desktop

Port: **8082**

---

## 1) A2A: Run & Call

### Start (local)
```bash
uv run src/a2a_server.py
```

### Discover the Agent Card
```bash
curl -s http://localhost:8082/.well-known/agent-card.json | jq .
```
> Use the **`url` from the card** as the JSON-RPC endpoint.

### Call `message/send`
Send coordinates as `"lat,lon"` (e.g., Algiers: `36.75,3.06`).

**Windows `cmd.exe` one-liner**
```bat
curl -s http://localhost:8082/ -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"message/send\",\"params\":{\"message\":{\"messageId\":\"demo-2\",\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"36.75,3.06\"}]}}}"
```

**bash/zsh (macOS/Linux)**
```bash
curl -s http://localhost:8082/ \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"1","method":"message/send","params":{"message":{"messageId":"demo-2","role":"user","parts":[{"kind":"text","text":"36.75,3.06"}]}}}'
```

---

## 2) MCP: Use from Claude Desktop (stdio)

1) Open the Claude Desktop config:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2) Add this (edit the absolute path):
```json
{
  "mcpServers": {
    "ust_weather": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/ABSOLUTE/PATH/ust-agent-hub-mvp/agents/weather",
        "run",
        "src/mcp_server.py"
      ]
    }
  }
}
```

3) Restart Claude Desktop. Then ask:
> “Call `ust_weather.forecast` for `36.75, 3.06`.”

---

## 3) Notes
- Uses Open-Meteo (no API key) for the daily summary in the A2A server. Ensure outbound internet.
- MCP server: keep stdout clean; use logging for diagnostics.
