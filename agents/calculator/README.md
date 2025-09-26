# UST Calculator Agent

Minimal calculator that exposes:
- **A2A** (Agent-to-Agent): Agent Card discovery + JSON-RPC `message/send`
- **MCP** (Model Context Protocol): stdio tools for Claude Desktop

**Port**: 8081

---

## 1) A2A: Run & Call

### Start (local)

```bash
uv run src/a2a_server.py
```

### Discover the Agent Card

```bash
curl -s http://localhost:8081/.well-known/agent-card.json | jq .
```

A2A clients should use the `url` field from the card as the JSON-RPC endpoint.

### Call message/send

The payload must include a `messageId` and text parts with `{"kind":"text","text":"..."}`.

**Windows cmd.exe one-liner:**

```bat
curl -s http://localhost:8081/ -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"message/send\",\"params\":{\"message\":{\"messageId\":\"demo-1\",\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"7*6\"}]}}}"
```

**bash/zsh (macOS/Linux):**

```bash
curl -s http://localhost:8081/ \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"1","method":"message/send","params":{"message":{"messageId":"demo-1","role":"user","parts":[{"kind":"text","text":"7*6"}]}}}'
```

*Windows cmd.exe does not support single quotes—use double quotes and escape inner quotes.*

---

## 2) MCP: Use from Claude Desktop (stdio)

Claude Desktop can launch local MCP servers from a JSON config file.

### Open the Claude Desktop config:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
  (e.g., `C:\Users\<you>\AppData\Roaming\Claude\claude_desktop_config.json`)

### Add this (edit the absolute path):

```json
{
  "mcpServers": {
    "ust_calculator": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/ABSOLUTE/PATH/ust-agent-hub-mvp/agents/calculator",
        "run",
        "src/mcp_server.py"
      ]
    }
  }
}
```

Restart Claude Desktop. It will spawn the stdio server for you. In chat, try:

**"Use `ust_calculator.calc` to evaluate 7*6."**

FastMCP auto-generates tool schemas from your function signatures/docstrings, and stdio is the recommended transport for local tooling.

---

## 3) Notes

- No secrets required
- For MCP servers, don't print to stdout; use Python logging (stderr)