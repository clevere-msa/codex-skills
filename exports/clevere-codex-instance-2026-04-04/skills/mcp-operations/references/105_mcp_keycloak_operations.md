# MCP Keycloak Operations (Codex Skill)

## Server
- keycloak-model-context-protocol

## Execution Requirements
- MUST be launched via node dist/index.js
- npx launchers are NOT reliable

## Environment Requirements
- KEYCLOAK_URL
- KEYCLOAK_ADMIN
- KEYCLOAK_ADMIN_PASSWORD

## Common Failure Modes
- ESM executed by /bin/sh
- Missing env vars
- TLS trust failures

## Allowed Operations
- Realm inspection
- Client/user/group metadata
- Read-only by default

## Verification
- Manual node execution stays alive
- No stdout noise before MCP initialize

