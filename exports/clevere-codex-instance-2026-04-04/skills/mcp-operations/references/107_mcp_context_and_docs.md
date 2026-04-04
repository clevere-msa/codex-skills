# MCP Context & Document Servers (Codex Skill)

## Servers
- context7
- document_loader

## Characteristics
- npx-based
- Slow first startup
- Network-dependent

## Required Settings
- startup_timeout_sec >= 60
- STDERR-only logging

## Usage Guidelines
- Context enrichment only
- No authority over repo state
- Treat outputs as advisory

## Verification
- First run may exceed default timeout
- Subsequent runs should stabilize

