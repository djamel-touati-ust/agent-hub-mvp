import logging
from mcp.server.fastmcp import FastMCP

# IMPORTANT: MCP stdio uses stdout for protocol frames; log to stderr only.
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("<agent_name>")

@mcp.tool()
async def echo(text: str) -> str:
    """Echo a piece of text."""
    return f"echo: {text}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
