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
from app import compute

# --- Executor: Pure orchestration; calls our app logic.
class CalculatorExecutor(AgentExecutor):
    async def execute(self, context, event_queue: EventQueue) -> None:
        text = (context.get_user_input() or "").strip()
        reply = compute(text)
        await event_queue.enqueue_event(new_agent_text_message(reply))
        # DefaultRequestHandler will handle final response based on queued events.

    async def cancel(self, context, event_queue: EventQueue) -> None:
        await event_queue.close(immediate=True)

# --- Agent Card (served at /.well-known/agent-card.json)
PORT = int(os.environ.get("PORT", "8081"))
BASE_URL = os.environ.get("BASE_URL", f"http://localhost:{PORT}/")

card = AgentCard(
    # snake_case fields in Python -> serialized to camelCase in JSON
    protocol_version="0.3.0",
    version="0.1.0",
    name="UST Calculator",
    description="Simple calculator agent.",
    url=BASE_URL,                     # RPC endpoint (your card shows root '/')
    preferred_transport="JSONRPC",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(
            id="calc.compute",
            name="Compute arithmetic",
            description="Compute 'A+B', 'A-B', 'A*B', or 'A/B' from user text.",
            tags=["math", "arithmetic"],
            input_modes=["text"],
            output_modes=["text"],
        )
    ],
)

# --- Wire SDK server
handler = DefaultRequestHandler(
    agent_executor=CalculatorExecutor(),
    task_store=InMemoryTaskStore(),
    request_context_builder=SimpleRequestContextBuilder(),
)
server = A2AStarletteApplication(agent_card=card, http_handler=handler)

if __name__ == "__main__":
    # Exposes:
    #   GET /.well-known/agent-card.json  (discovery)
    #   POST /                            (JSON-RPC message/send, per your card url)
    uvicorn.run(server.build(), host="0.0.0.0", port=PORT)
