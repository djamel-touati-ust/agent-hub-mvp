# agents/weather/src/mcp_server.py
import logging
from mcp.server.fastmcp import FastMCP
from app import daily_summary  # async function

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("ust_weather")

@mcp.tool()
async def forecast(lat: float, lon: float) -> str:
    """Return a one-line daily summary for latitude,longitude (e.g., 36.75,3.06)."""
    return await daily_summary(lat, lon)

if __name__ == "__main__":
    mcp.run(transport="stdio")
