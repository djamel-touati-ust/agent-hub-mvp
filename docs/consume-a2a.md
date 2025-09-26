# Consume via A2A (JSON-RPC)

## 1) Discover the agent (well-known path)

Fetch its **Agent Card**:

```bash
curl -s http://localhost:8080/.well-known/agent-card.json | jq .
```

The card advertises the primary A2A endpoint `url` and `preferredTransport` (e.g., JSONRPC).

## 2) Call message/send with cURL

```bash
curl -s http://localhost:8080/a2a/v1 \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer X' \
  -d '{
        "jsonrpc":"2.0",
        "id":"1",
        "method":"message/send",
        "params":{
          "message":{
            "role":"user",
            "parts":[{"kind":"text","text":"ping"}]
          }
        }
      }'
```

Responses follow JSON-RPC 2.0. Typical errors:
- `-32700` parse error
- `-32600` invalid request
- `-32601` method not found
- `-32602` invalid params
- `-32603` internal error

Servers may reserve `-32000..-32099` for app-specific errors (e.g., unauthenticated).

## 3) Minimal Python (requests)

```python
import requests, json

card = requests.get("http://localhost:8080/.well-known/agent-card.json").json()
endpoint = card["url"]  # e.g., http://localhost:8080/a2a/v1

payload = {
  "jsonrpc": "2.0",
  "id": "1",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "ping"}]
    }
  }
}

r = requests.post(endpoint, json=payload, headers={"Authorization": "Bearer X"})
print(json.dumps(r.json(), indent=2))
```

For production, prefer HTTPS and proper auth; the agent card's `securitySchemes`/`security` tell you what's required.

## 4) Notes

- We standardize on the well-known path `/.well-known/agent-card.json` for discovery
- Our A2A server templates use the official A2A Python SDK (Starlette app + default handler), which serves the card and the JSON-RPC endpoint