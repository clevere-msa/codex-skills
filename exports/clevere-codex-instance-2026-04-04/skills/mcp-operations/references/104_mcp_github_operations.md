# MCP GitHub Operations (Codex Skill)

## Server
- github-mcp-server (official GitHub)

## Execution Mode
- Native binary preferred over Docker
- stdio mode only

## Security Posture
- GITHUB_READ_ONLY=1 by default
- Toolsets restricted unless explicitly expanded
- Token provided via env-file or env var

## Allowed Actions
- Repository inspection
- Issues / PR metadata
- File content read

## Prohibited Actions
- Repo mutation unless explicitly approved
- Token echoing or logging

## Verification
- Manual run stays alive awaiting MCP handshake
- No stdout output prior to MCP frames

