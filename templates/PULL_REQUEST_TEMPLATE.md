# New Agent Submission

## Checklist
- [ ] `agents/<name>/agent.yaml` passes schema validation
- [ ] A2A server exposes:
  - [ ] `/.well-known/agent-card.json` (validates against schema)
  - [ ] JSON-RPC `message/send` at the card `url`
  - [ ] `messageId` + `parts[].kind="text"` supported
- [ ] MCP stdio server works (Claude Desktop shows tools)
- [ ] Dockerfile builds and runs A2A with `python -u src/a2a_server.py`
- [ ] README added with instructions
- [ ] No secrets committed; outbound domains documented
- [ ] `agents/<name>/README.md` exists and includes **A2A** and **MCP** sections

## Notes
Explain what your agent does, required env vars, and any limitations.