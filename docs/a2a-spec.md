# UST A2A v0.1 (MVP)

**Transport:** HTTP(S) + JSON-RPC 2.0.  
**Discovery:** `GET /.well-known/agent-card.json` returns the Agent Card (see schema).

## Agent Card (must-have fields)

- `protocolVersion` e.g. `0.1.0`
- `name`, `description`, `provider`
- `skills`: at least one id+description
- `interfaces`: at least one `{ "url": ".../a2a/v1", "transport": "JSONRPC" }`
- `securitySchemes`: `{ "type": "http", "scheme": "bearer" }`
- `security`: array referencing schemes

## Methods (MVP)

### `message/send` (REQUIRED)

#### Request
```json
{"jsonrpc":"2.0","id":"1","method":"message/send",
 "params":{"message":{"messageId":"demo-1","role":"user","parts":[{"kind":"text","text":"hello"}]}}}
```

#### Success
```json
{"jsonrpc":"2.0","id":"1","result":{"task":{
  "id":"<uuid>","state":"TASK_STATE_COMPLETED",
  "artifacts":[{"parts":[{"kind":"text","text":"...reply..."}]}]}}}
```

**Errors (JSON-RPC 2.0):**

- `-32601` method not found
- `-32602` invalid params
- `-32700` parse error
- Use `-32000..-32099` for app errors (e.g., `-32001` unauthenticated).

---

## Agent Card template (ready to edit)

Create `templates/agent-card.json`:

```json
{
  "protocolVersion": "0.3.0",
  "version": "0.1.0",
  "name": "<AGENT NAME>",
  "description": "<one-line description>",
  "provider": { "name": "UST", "contact": "agent-hub@ust.com" },
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": [{ "id": "<namespace.skill>", "name": "Skill name", "description": "What it does" }],
  "preferredTransport": "JSONRPC",
  "url": "http://localhost:8080/",
  "capabilities": { "streaming": false },
  "securitySchemes": [{ "type": "http", "scheme": "bearer", "name": "bearer" }],
  "security": [{ "bearer": [] }]
}
```
