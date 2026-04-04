# MCP STDIO Hygiene (Codex Skill)

## Purpose
Prevent MCP handshake failures caused by stdout contamination.

## Rules
- All logging MUST go to STDERR.
- Logging level MUST be configurable via env (e.g., FASTMCP_LOG_LEVEL).
- Default log level in Codex environments: ERROR.

## Validation Procedure
1. Run server with stdout redirected to file.
2. If file contains any bytes before MCP frames → protocol violation.
3. Wrap server with a stdio-cleaner shim if upstream cannot be fixed.

## Approved Mitigation
- Use a stdio-cleaner wrapper that forwards only MCP frames to STDOUT.
- Divert all other stdout bytes to STDERR with prefix.

## Anti-Patterns
- print(), console.log(), logging.basicConfig() without stream override
- Third-party libraries writing banners to stdout

