#!/usr/bin/env python3
import sys, json, requests
from jsonschema import validate

SCHEMA_PATH = "schemas/agent-card.schema.json"

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_agent_card.py http://host:port/.well-known/agent-card.json")
        sys.exit(2)

    url = sys.argv[1]
    data = requests.get(url, timeout=5).json()
    schema = json.load(open(SCHEMA_PATH, "r"))
    validate(instance=data, schema=schema)
    print("[OK] agent card validates:", data.get("name"))

if __name__ == "__main__":
    main()
