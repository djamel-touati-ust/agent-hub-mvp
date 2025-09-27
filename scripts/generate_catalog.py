#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

"""
Generate catalog + static agent cards for GitHub Pages.

Usage from CI (as in your publish workflow):
  python scripts/generate_catalog.py <OWNER> <REPO> <REF>

Outputs:
  - docs/catalog.json
  - docs/agents/<agent>/agent-card.json  (one per agent)
  - registry/catalog.json                (mirror for non-Pages uses)

Reads:
  - agents/<agent>/agent.yaml

Notes:
  - a2aCard path in catalog points to "agents/<agent>/agent-card.json"
    which is served under the Pages site root once deployed.
  - Container image tags match your build job:
      ghcr.io/<OWNER>/agent-<agent>:<version>
      ghcr.io/<OWNER>/agent-<agent>:sha-<shortref>
      ghcr.io/<OWNER>/agent-<agent>:edge
"""

DOCS_DIR = Path("docs")
AGENTS_DIR = Path("agents")
REGISTRY_DIR = Path("registry")


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def build_agent_card(agent: str, y: Dict[str, Any]) -> Dict[str, Any]:
    """Create a minimal static Agent Card JSON for Pages."""
    name = y.get("name", agent)
    version = y.get("version", "0.1.0")
    description = y.get("description", "")
    # Skills: accept minimal list of ids/descriptions; add a default name
    skills_src = (y.get("a2a", {}) or {}).get("skills", []) or []
    skills = []
    for s in skills_src:
        sid = s.get("id", "")
        sdesc = s.get("description", "")
        skills.append(
            {
                "id": sid,
                "name": s.get("name") or sid or "skill",
                "description": sdesc,
            }
        )

    # We don't know a public runtime URL in Pages; leave empty or point to "/"
    # Consumers can still read the card structure for discovery.
    card = {
        "protocolVersion": "0.3.0",
        "version": version,
        "name": f"UST {name.capitalize()}",
        "description": description or f"{name} agent.",
        "provider": {"name": "UST", "contact": "agent-hub@ust.com"},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": skills,
        "preferredTransport": "JSONRPC",
        "url": "",
        "capabilities": {"streaming": False},
        "securitySchemes": [{"type": "http", "scheme": "bearer", "name": "bearer"}],
        "security": [{"bearer": []}],
    }
    return card


def main() -> int:
    import sys

    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: generate_catalog.py <OWNER> <REPO> <REF>")
        return 2

    owner = sys.argv[1]
    repo = sys.argv[2]
    ref = sys.argv[3] if len(sys.argv) == 4 else ""

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "agents").mkdir(parents=True, exist_ok=True)
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

    agents_list: List[Dict[str, Any]] = []

    for d in sorted(AGENTS_DIR.iterdir()):
        if not d.is_dir():
            continue
        man = d / "agent.yaml"
        if not man.exists():
            continue

        y = load_yaml(man)
        agent_dir_name = d.name
        name = y.get("name", agent_dir_name)
        version = y.get("version", "0.1.0")
        description = y.get("description", "")
        language = y.get("language", "")
        frameworks = y.get("frameworks", [])

        # Write static Agent Card under docs/agents/<name>/agent-card.json
        out_card_dir = DOCS_DIR / "agents" / name
        out_card_dir.mkdir(parents=True, exist_ok=True)
        card_path = out_card_dir / "agent-card.json"
        card_json = build_agent_card(name, y)
        card_path.write_text(json.dumps(card_json, indent=2) + "\n", encoding="utf-8")

        # MCP entry (pass-through)
        mcp_entry = (y.get("entrypoints", {}) or {}).get("mcp", {})

        # Image tags (align with your build-and-push job)
        shortref = ref[:7] if ref else ""
        images = {
            "version": f"ghcr.io/{owner}/agent-{name}:{version}",
            "sha": f"ghcr.io/{owner}/agent-{name}:sha-{shortref}" if shortref else "",
            "edge": f"ghcr.io/{owner}/agent-{name}:edge",
        }

        agents_list.append(
            {
                "name": name,
                "version": version,
                "description": description,
                "language": language,
                "frameworks": frameworks,
                "git": f"https://github.com/{owner}/{repo}/tree/main/agents/{agent_dir_name}",
                "container": images,
                "a2aCard": f"agents/{name}/agent-card.json",
                "mcp": mcp_entry,
            }
        )

    catalog = {
        "schemaVersion": "1.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "agents": agents_list,
    }

    # Write for Pages
    (DOCS_DIR / "catalog.json").write_text(
        json.dumps(catalog, indent=2) + "\n", encoding="utf-8"
    )
    # Mirror for non-Pages consumers
    (REGISTRY_DIR / "catalog.json").write_text(
        json.dumps(catalog, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Wrote docs/catalog.json with {len(agents_list)} agents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
