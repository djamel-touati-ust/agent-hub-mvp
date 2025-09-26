# Consume Agents via A2A

## 1) Discover the Agent Card

```bash
curl -s http://HOST:PORT/.well-known/agent-card.json | jq .
```

The card contains the service endpoint in `url`. Always post JSON-RPC to that URL.

## 2) Call message/send

A2A JSON-RPC requires `messageId`, `role`, and `parts` with text content (`{"kind":"text","text":"..."}`).

### Windows cmd.exe one-line (Calculator)

```bat
curl -s http://localhost:8081/ -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"message/send\",\"params\":{\"message\":{\"messageId\":\"demo-1\",\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"12/3\"}]}}}"
```

### Windows cmd.exe one-line (Weather)

```bat
curl -s http://localhost:8082/ -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"message/send\",\"params\":{\"message\":{\"messageId\":\"demo-2\",\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"36.75,3.06\"}]}}}"
```

If your card advertises `/a2a/v1` instead of `/`, post to `/a2a/v1`. The card is the source of truth.

## JSON-RPC error codes

Server replies may include codes like `-32601` (method not found) and `-32602` (invalid params) per JSON-RPC 2.0.