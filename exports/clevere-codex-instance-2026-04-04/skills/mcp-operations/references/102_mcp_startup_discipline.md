# MCP Startup Discipline (Codex Skill)

## Purpose
Ensure deterministic MCP startup under Codex orchestration.

## Requirements
- All servers must tolerate cold start delays.
- npx / first-run installs REQUIRE increased startup_timeout_sec.
- Docker-based MCPs REQUIRE explicit env injection (-e or --env-file).

## Timeout Guidance
- Pure Python/Node: 30–60s
- npx-based tools: 60–120s
- Docker-based MCPs: ≥60s

## Environment Injection
- env table affects launcher ONLY.
- Containers require explicit env pass-through.
- Prefer --env-file for secrets.

## Verification
- Server must survive startup when launched manually.
- No interactive prompts allowed during startup.

