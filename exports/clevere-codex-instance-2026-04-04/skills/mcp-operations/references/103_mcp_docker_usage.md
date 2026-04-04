# MCP Docker Usage (Codex Skill)

## Purpose
Define when Docker is acceptable for MCP servers.

## Allowed Uses
- Vendor-provided MCP servers with no native binary
- Isolation of high-risk tooling
- Temporary bootstrap / evaluation

## Required Constraints
- Docker daemon access MUST be explicit and intentional.
- User must be in docker group (root-equivalent risk acknowledged).
- Secrets passed via --env-file, never inline args.

## Prohibited Uses
- Running non-MCP services as MCP servers (e.g., databases)
- Expecting port-based services to speak MCP over stdio

## Exit Criteria
- Prefer native binary or venv-based execution when available.

