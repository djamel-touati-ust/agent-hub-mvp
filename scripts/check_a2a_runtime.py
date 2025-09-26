#!/usr/bin/env python3
import sys, json, requests

if len(sys.argv) < 2:
    print("usage: check_a2a_runtime.py <base_url> [bearer_token]")
    sys.exit(2)

base = sys.argv[1].rstrip("/")
token = sys.argv[2] if len(sys.argv) > 2 else None
headers = {"Authorization": f"Bearer {token}"} if token else {}

# 1) Card
card_url = f"{base}/.well-known/agent-card.json"
card = requests.get(card_url, headers=headers, timeout=5).json()
print("[OK] fetched agent card:", card.get("name"))

# 2) message/send (JSON-RPC 2.0)
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
resp = requests.post(f"{base}/a2a/v1", json=payload, headers=headers, timeout=10)
data = resp.json()
assert data.get("jsonrpc") == "2.0" and ("result" in data or "error" in data)
print("[OK] message/send response:", json.dumps(data, indent=2)[:400])
