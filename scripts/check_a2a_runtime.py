#!/usr/bin/env python3
"""
Usage:
  python scripts/check_a2a_runtime.py http://localhost:8081
  python scripts/check_a2a_runtime.py http://localhost:8081 --nocard
  python scripts/check_a2a_runtime.py http://localhost:8081 --token X
"""
import sys, json, uuid, requests

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    base = sys.argv[1].rstrip("/")
    nocard = "--nocard" in sys.argv
    headers = {}
    if "--token" in sys.argv:
        ti = sys.argv.index("--token")
        if ti + 1 < len(sys.argv):
            headers["Authorization"] = f"Bearer {sys.argv[ti+1]}"

    if nocard:
        endpoint = base if base.endswith("/a2a/v1") else base + "/"
    else:
        # Fetch Agent Card then use card["url"]
        card = requests.get(base + "/.well-known/agent-card.json", headers=headers, timeout=5).json()
        endpoint = card.get("url", base + "/")

    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "message/send",
        "params": {
            "message": {
                "messageId": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"kind": "text", "text": "ping"}]
            }
        }
    }
    r = requests.post(endpoint, json=payload, headers=headers, timeout=10)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    main()
