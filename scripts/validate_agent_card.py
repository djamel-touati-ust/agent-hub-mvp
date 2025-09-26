#!/usr/bin/env python3
import sys, json, pathlib
from urllib.parse import urlparse
from jsonschema import Draft202012Validator
import requests

if len(sys.argv) != 2:
    print("usage: validate_agent_card.py <URL-or-path>")
    sys.exit(2)

target = sys.argv[1]
root = pathlib.Path(__file__).resolve().parents[1]
schema = json.load(open(root/"schemas/agent-card.schema.json"))
validator = Draft202012Validator(schema)

if urlparse(target).scheme in ("http","https"):
    resp = requests.get(target, timeout=5)
    resp.raise_for_status()
    data = resp.json()
else:
    data = json.load(open(target))

errs = list(validator.iter_errors(data))
if errs:
    print("[FAIL] agent card:")
    for e in errs:
        print("  -", e.message)
    sys.exit(1)
print("[OK] agent card")
