import httpx

BASE = "https://api.open-meteo.com/v1/forecast"

async def daily_summary(lat: float, lon: float) -> str:
    """
    Return a short daily summary (high/low/precip) for given lat, lon.
    Uses Open-Meteo (no API key required).
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(BASE, params=params)
        r.raise_for_status()
        data = r.json()

    d = data.get("daily", {})
    if not d or not d.get("time"):
        return "No forecast available."
    hi = d["temperature_2m_max"][0]
    lo = d["temperature_2m_min"][0]
    p  = d["precipitation_sum"][0]
    return f"Today: high {hi}°C, low {lo}°C, precip {p} mm."
#