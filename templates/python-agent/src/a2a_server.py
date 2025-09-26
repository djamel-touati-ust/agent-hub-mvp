import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

# --- Simple "executor" bridging incoming A2A messages to your logic ---
# You can replace this with a LangGraph-powered executor later.
class EchoAgentExecutor:
    async def execute(self, *, message, event_queue, context=None):
        # Pull any text parts and echo them back
        texts = [p.text for p in getattr(message, "parts", []) if getattr(p, "kind", "") == "text"]
        reply = "echo: " + " ".join(texts) if texts else "echo: (no text)"
        # SDK utility: create an agent message and enqueue via event_queue
        await event_queue.enqueue_text_message(reply)

    async def cancel(self, *, task_id, context=None):
        # Basic MVP agents can raise for unsupported cancel
        raise NotImplementedError("cancel not supported in MVP")

# --- Agent Card (minimal, SDK-aligned) ---
agent_card = AgentCard(
    protocolVersion="0.3.0",
    name="<Agent Name>",
    description="Example UST Agent (template, SDK-based).",
    url="http://localhost:8080/a2a/v1",
    preferredTransport="JSONRPC",
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(id="example.echo", description="Echo a piece of text"),
    ],
)

# --- Wire the handler + server ---
request_handler = DefaultRequestHandler(
    agent_executor=EchoAgentExecutor(),
    task_store=InMemoryTaskStore(),
)

# NOTE: We override the SDK default card path to satisfy the hub rule:
#       serve at "/.well-known/agent-card.json"; RPC at "/a2a/v1".
server = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
    agent_card_url="/.well-known/agent-card.json",
    rpc_url="/a2a/v1",
)

if __name__ == "__main__":
    uvicorn.run(server.build(), host="0.0.0.0", port=8080)
