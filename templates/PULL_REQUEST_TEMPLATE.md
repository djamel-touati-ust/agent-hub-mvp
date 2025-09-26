# UST Agent Hub – Pull Request

## 1) Summary
- Agent name:
- Short description:
- Owner/team (email):

## 2) Checklist – Repo Rules
- [ ] `agents/<name>/agent.yaml` present and **valid** (passes `/schemas/agent.schema.json`)
- [ ] Dockerfile exists; image builds locally
- [ ] README with quickstart (MCP + A2A), env vars, security notes
- [ ] Minimal tests included (unit or smoke)

## 3) MCP Surface
- [ ] `src/mcp_server.py` present; declares at least one tool
- [ ] Local MCP quickstart tested (Claude Desktop or other MCP host)
- [ ] **No stdout logging** from MCP stdio server (stderr only)

## 4) A2A Surface (SDK-based)
- [ ] Uses **A2A Python SDK** (`a2a-sdk`): `A2AStarletteApplication`, `DefaultRequestHandler`, `InMemoryTaskStore`
- [ ] Serves Agent Card at `/.well-known/agent-card.json` (public or auth per README)
- [ ] Agent Card includes (at minimum): `protocolVersion`, `name`, `description`, `url`, `preferredTransport`, `skills[]`
- [ ] `message/send` smoke passes with `parts[].kind="text"`

## 5) Security & Policy
- [ ] No secrets in code
- [ ] Data handling documented (PII? none/limited)
- [ ] Outbound domains listed under `security.outbound_network` in `agent.yaml`
- [ ] License set to `internal`

## 6) Container & Catalog
- [ ] Image naming: `ghcr.io/<org>/<agent>:<semver>`
- [ ] If new agent or version tag: added via script to `registry/catalog.json`
- [ ] If unchanged agent: CI skips rebuild/push to avoid duplicate images

## 7) Docs
- [ ] Updated `/docs/consume-a2a.md` & `/docs/consume-mcp.md` snippets if needed
- [ ] (Optional) mirrored card at `/docs/agents/<name>/agent-card.json`
