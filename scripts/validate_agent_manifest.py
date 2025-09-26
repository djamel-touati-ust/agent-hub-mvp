#!/usr/bin/env python3
import sys, json, yaml, pathlib
from jsonschema import validate, Draft202012Validator

root = pathlib.Path(__file__).resolve().parents[1]
schema = json.load(open(root/"schemas/agent.schema.json"))
validator = Draft202012Validator(schema)

errors = 0
for p in sorted((root/"agents").glob("*/agent.yaml")):
    data = yaml.safe_load(open(p))
    errs = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errs:
        print(f"[FAIL] {p}")
        for e in errs:
            print("  -", e.message)
        errors += 1
    else:
        print(f"[OK]   {p}")

sys.exit(1 if errors else 0)
