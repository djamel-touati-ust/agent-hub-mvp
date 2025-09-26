#!/usr/bin/env python3
import os, json, yaml
from jsonschema import validate

SCHEMA = "schemas/agent.schema.json"

def find_manifests(root="agents"):
    for dirpath, dirnames, filenames in os.walk(root):
        if "agent.yaml" in filenames or "agent.yml" in filenames:
            yield os.path.join(dirpath, "agent.yaml")

def main():
    schema = json.load(open(SCHEMA, "r"))
    errors = 0
    for manifest in find_manifests():
        try:
            data = yaml.safe_load(open(manifest, "r"))
            validate(instance=data, schema=schema)
            print(f"[OK] {manifest}")
        except Exception as e:
            print(f"[FAIL] {manifest}: {e}")
            errors += 1
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
