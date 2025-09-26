import os
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.simple_request_context_builder import SimpleRequestContextBuilder
from a2a.server.events import EventQueue
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
from a2a.utils.message import new_agent_text_message
from app import daily_summary

def _parse_latlon(text: str):
    try:
        lat_s, lon_s = text.split(",", 1)
        return float(lat_s.strip()), float(lon_s.strip())
    except Exception:
        return None

class WeatherExecutor(AgentExecutor):
    async def execute(self, context, event_queue: EventQueue) -> None:
        text = (context.get_user_input() or "").strip()
        pair = _parse_latlon(text)
        if not pair:
            reply = "Send coordinates as 'lat,lon' (e.g., '36.75,3.06')."
        else:
            lat, lon = pair
            try:
                reply = await daily_summary(lat, lon)
            except Exception as e:
                reply = f"Error: {e}"
        await event_queue.enqueue_event(new_agent_text_message(reply))

    async def cancel(self, context, event_queue: EventQueue) -> None:
        await event_queue.close(immediate=True)

PORT = int(os.environ.get("PORT", "8082"))
BASE_URL = os.environ.get("BASE_URL", f"http://localhost:{PORT}/")

card = AgentCard(
    protocol_version="0.3.0",
    version="0.1.0",
    name="UST Weather",
    description="Daily forecast summary for 'lat,lon'.",
    url=BASE_URL,
    preferred_transport="JSONRPC",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(
            id="weather.forecast_daily",
            name="Daily forecast summary",
            description="Return a daily forecast summary for latitude,longitude input.",
            tags=["weather", "open-meteo"],
            input_modes=["text"],
            output_modes=["text"],
        )
    ],
)

handler = DefaultRequestHandler(
    agent_executor=WeatherExecutor(),
    task_store=InMemoryTaskStore(),
    request_context_builder=SimpleRequestContextBuilder(),
)
server = A2AStarletteApplication(agent_card=card, http_handler=handler)

if __name__ == "__main__":
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT)
