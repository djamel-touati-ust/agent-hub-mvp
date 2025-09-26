#!/usr/bin/env python3
import sys, os, yaml, json, pathlib

if len(sys.argv) != 4:
    print("usage: generate_catalog.py <OWNER> <REPO> <REF>", file=sys.stderr)
    sys.exit(1)

OWNER, REPO, REF = sys.argv[1], sys.argv[2], sys.argv[3]

agents_dir = pathlib.Path("agents")
agents = []
for d in agents_dir.iterdir():
    if not d.is_dir(): continue
    man = d / "agent.yaml"
    if not man.exists(): continue
    y = yaml.safe_load(man.read_text())
    name = y.get("name", d.name)
    version = y.get("version", "0.0.0")
    mcp = y.get("entrypoints", {}).get("mcp", {})
    a2a = y.get("entrypoints", {}).get("a2a", {})
    # Static card copy for docs (optional; mirrors runtime card)
    docs_agent_dir = pathlib.Path("docs/agents") / name
    docs_agent_dir.mkdir(parents=True, exist_ok=True)
    if a2a:
        card = {
            "protocolVersion": "0.3.0",
            "version": version,
            "name": f"UST {name.capitalize()}",
            "description": y.get("description", ""),
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "skills": [{"id": s.get("id"), "name": s.get("id"), "description": s.get("description","")} for s in y.get("a2a",{}).get("skills",[])],
            "preferredTransport": "JSONRPC",
            "url": a2a.get("url", ""),
            "capabilities": {"streaming": False},
        }
        (docs_agent_dir / "agent-card.json").write_text(json.dumps(card, indent=2))

    agents.append({
        "name": name,
        "version": version,
        "git": f"https://github.com/{OWNER}/{REPO}/tree/main/agents/{name}",
        "container": f"ghcr.io/{OWNER}/agent-{name}:{version}",
        "a2aCard": f"https://{OWNER}.github.io/{REPO}/agents/{name}/agent-card.json",
        "mcp": {"type": mcp.get("type","stdio"),
                "command": mcp.get("command",""),
                "args": mcp.get("args",[])},
    })

catalog = {"schemaVersion": "1.0", "agents": agents}
pathlib.Path("registry").mkdir(exist_ok=True)
pathlib.Path("registry/catalog.json").write_text(json.dumps(catalog, indent=2))
pathlib.Path("docs/catalog.json").write_text(json.dumps(catalog, indent=2))
print(f"Wrote {len(agents)} agents to registry/catalog.json and docs/catalog.json")
