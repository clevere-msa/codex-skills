# MCP Runtime Contract (Codex Skill)

## Purpose
Define the non-negotiable runtime rules for MCP servers operated under Codex.

## Core Contract
- MCP servers MUST communicate exclusively over stdio using MCP framing.
- STDOUT is reserved for MCP protocol bytes ONLY.
- STDERR is reserved for logs, diagnostics, and human-readable output.
- Any text emitted to STDOUT outside MCP frames is a protocol violation.

## Startup Expectations
- Server must remain running after startup and wait for MCP initialize.
- Server must not exit on missing optional configuration; fail fast only on fatal config errors.
- Servers should tolerate delayed client initialize (≥ startup_timeout_sec).

## Failure Handling
- On fatal error: emit structured error to STDERR and exit non-zero.
- On recoverable error: emit MCP error response, not process exit.

## Prohibited Behaviors
- Writing banners, warnings, or logs to STDOUT
- Interactive prompts
- TTY assumptions
- Background daemonization

## Verification
- Server MUST stay alive when run manually in a terminal with stdin open.
- `initialize` handshake must succeed with no stdout contamination.

