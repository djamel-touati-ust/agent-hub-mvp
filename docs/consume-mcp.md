# Consume Agents via MCP (Claude Desktop)

## 1) Install Claude Desktop and find the config

On Windows, open (or create):
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

See MCP "connect local servers" guide for paths and behavior.

## 2) Add the servers

Adjust absolute paths for your machine:

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
    },
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

## 3) Restart Claude Desktop

Claude will spawn both MCP stdio servers automatically (you do not run them yourself).

## 4) Use the tools

- Ask: "Use `ust_calculator.calc` to evaluate 7*6."
- Ask: "Call `ust_weather.forecast` for 36.75, 3.06."

## Notes

- **STDIO servers**: do not print to stdout; use Python logging (stderr)
- FastMCP auto-generates tool schemas from type hints/docstrings