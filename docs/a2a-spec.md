# UST A2A v0.1 (MVP)

**Transport:** HTTP(S) + JSON-RPC 2.0  
**Discovery:** `GET /.well-known/agent-card.json` returns the Agent Card (see schema). Servers **MUST** publish an Agent Card, and clients should post to the `url` field in the card.

## Agent Card (must-have fields)

- `protocolVersion` (e.g., `0.3.0`), `version` (agent/card semver)
- `name`, `description`, `provider` (optional)
- `skills`: at least one id+name+description+tags
- `defaultInputModes`, `defaultOutputModes` (e.g., `["text"]`)
- `preferredTransport` (e.g., `JSONRPC`)
- `url`: base JSON-RPC endpoint (often `/` or `/a2a/v1`)
- `securitySchemes` and `security` (bearer pattern for later)

## Methods (MVP)

### `message/send` (REQUIRED)

**Request**

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "message/send",
  "params": {
    "message": {
      "messageId": "<uuid-or-string>",
      "role": "user",
      "parts": [{"kind": "text", "text": "hello"}]
    }
  }
}
```

**Success** (example returning a Task or Message)

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "task": {
      "id": "<uuid>",
      "state": "completed",
      "artifacts": [{"parts": [{"kind": "text", "text": "...reply..."}]}]
    }
  }
}
```

**Errors** (JSON-RPC 2.0):
- `-32601` method not found
- `-32602` invalid params
- `-32700` parse error
- `-32000..-32099` for app errors