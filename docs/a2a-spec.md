# UST A2A v0.1 (MVP)

**Transport**: HTTP(S) + JSON-RPC 2.0  
**Discovery**: Serve a public Agent Card at `GET /.well-known/agent-card.json`. This follows A2A's recommended location and the IETF "well-known URI" convention.

## Scope

This doc defines the minimum A2A surface an agent must implement for the MVP:

- A valid Agent Card (public) at `/.well-known/agent-card.json`
- A JSON-RPC 2.0 endpoint exposing `message/send` at the URL advertised in the Agent Card
- Responses use the A2A wire objects (Message/Task/Artifacts) and `parts[].kind` ("text" | "file" | "data")

## Agent Card (required fields)

Your public card must include at least:

- `protocolVersion` (default in spec is "0.3.0"; keep current)
- `name`, `description`
- `url` (primary A2A base URL)
- `preferredTransport` (e.g., "JSONRPC")
- `skills`: one or more skills (id/name/description, etc.)
- `provider` with organization and url
- `securitySchemes` and `security` (HTTP Bearer is fine for MVP)
- *(Optional)* `additionalInterfaces` if you expose multiple transports/URLs

See the A2A spec's Agent Card structure and transport notes.

### Example (public Agent Card)

```json
{
  "protocolVersion": "0.3.0",
  "name": "UST Hello Support",
  "description": "Answers brief internal FAQs.",
  "url": "https://agents.ust.local/hello-support/a2a/v1",
  "preferredTransport": "JSONRPC",
  "version": "1.0.0",
  "default_input_modes": ["text"],
  "default_output_modes": ["text"],
  "provider": {
    "organization": "UST",
    "url": "https://ust.com"
  },
  "skills": [
    {
      "id": "faq.answer",
      "name": "Answer short FAQs",
      "description": "Answers brief internal IT/HR FAQs.",
      "examples": ["vpn reset", "expense policy"]
    }
  ],
  "securitySchemes": [
    { "type": "http", "scheme": "bearer", "name": "bearer" }
  ],
  "security": [
    { "bearer": [] }
  ]
}
```

*Why this shape?* The SDK/spec defines `url` + `preferredTransport` and uses `provider.organization/url`. `additionalInterfaces[]` is available when you want to advertise more transports/URLs.

## Methods (MVP)

### message/send (REQUIRED)

**Purpose**: send a user message to an agent; server returns either a final Task (with artifacts/history) or a Message.

#### Request (JSON-RPC 2.0)

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "message/send",
  "params": {
    "message": {
      "messageId": "e1f9b3e0-2e7c-4b97-9a88-6d8b5e0c8c1a",
      "role": "user",
      "parts": [
        { "kind": "text", "text": "hello" }
      ]
    }
  }
}
```

#### Success (Task result, synchronous)

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "task": {
      "id": "7a9c6b6a-8f19-4a75-bf1b-38b3f46df7a0",
      "state": "completed",
      "artifacts": [
        {
          "parts": [
            { "kind": "text", "text": "Hi! How can I help?" }
          ]
        }
      ],
      "history": []
    }
  }
}
```

A2A's JSON form uses lower-case task states like "completed", and Part discriminators are `kind: "text" | "file" | "data"`.

#### Errors (JSON-RPC 2.0)

- **Standard**: `-32700` parse error, `-32600` invalid request, `-32601` method not found, `-32602` invalid params, `-32603` internal error
- **Server-defined range**: `-32000..-32099` (e.g., `-32001` unauthenticated)

## Using the A2A Python SDK (recommended)

Run a server with `A2AStarletteApplication`, using `DefaultRequestHandler` + a `TaskStore` (e.g., `InMemoryTaskStore`).

The app exposes your public Agent Card at `/.well-known/agent-card.json` and maps JSON-RPC methods (e.g., `message/send`) to your executor.

<details>
<summary>Minimal server shape (illustrative)</summary>

```python
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentSkill, AgentCapabilities
import uvicorn

# define skills, card, and your AgentExecutor()...
handler = DefaultRequestHandler(agent_executor=YourExecutor(), task_store=InMemoryTaskStore())
app = A2AStarletteApplication(agent_card=your_public_card, http_handler=handler)

if __name__ == "__main__":
    uvicorn.run(app.build(), host="0.0.0.0", port=8080)
```

</details>

See the SDK tutorial for the full example with skills/cards/executor.

## Security (MVP)

- Public card can be anonymous; your RPC endpoint should require HTTP Bearer for non-demo use
- Production MUST use HTTPS; the spec provides TLS guidance

## Copy-paste templates

### `/templates/agent-card.json`

```json
{
  "protocolVersion": "0.3.0",
  "name": "<AGENT NAME>",
  "description": "<one-line description>",
  "url": "http://localhost:8080/a2a/v1",
  "preferredTransport": "JSONRPC",
  "version": "0.1.0",
  "default_input_modes": ["text"],
  "default_output_modes": ["text"],
  "provider": { "organization": "UST", "url": "https://ust.com" },
  "skills": [
    { "id": "<namespace.skill>", "name": "<Skill name>", "description": "What it does" }
  ],
  "securitySchemes": [{ "type": "http", "scheme": "bearer", "name": "bearer" }],
  "security": [{ "bearer": [] }]
}
```

## Quick test (cURL)

```bash
# Fetch public Agent Card (well-known)
curl -s http://localhost:8080/.well-known/agent-card.json | jq .name

# Call message/send (JSON-RPC over HTTP)
curl -s http://localhost:8080/a2a/v1 \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer X' \
  -d '{
        "jsonrpc":"2.0","id":"1","method":"message/send",
        "params":{
          "message":{
            "messageId":"11111111-2222-3333-4444-555555555555",
            "role":"user",
            "parts":[{"kind":"text","text":"vpn reset?"}]
          }
        }
      }'
```