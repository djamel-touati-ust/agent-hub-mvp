# agents/calculator/src/mcp_server.py
import logging
from mcp.server.fastmcp import FastMCP  # official SDK FastMCP
from app import compute

# For STDIO servers: never print to stdout; use logging (stderr). 
# (Claude will capture stderr logs.) 
# Ref: modelcontextprotocol.io transports/logging guidance
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("ust_calculator")

@mcp.tool()
def calc(expression: str) -> str:
    """Compute a simple arithmetic expression like '2+2', '10/4', '7-3'."""
    return compute(expression)

if __name__ == "__main__":
    # Use STDIO transport so Claude Desktop can spawn it
    mcp.run(transport="stdio")
