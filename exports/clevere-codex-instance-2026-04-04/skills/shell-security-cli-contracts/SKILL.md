---
name: shell-security-cli-contracts
description: Shell security hardening and CLI contract discipline for script interfaces. Use when changing argument parsing, command wrappers, secrets handling, privilege boundaries, or user-facing CLI behavior.
---

# Shell Security CLI Contracts

Use this skill for secure shell interfaces and predictable CLI behavior.
Routing note: for multi-concern routing, use `shell-guidelines` and `shell-guidelines/references/070_shell_skill_matrix.md`.

## Focus
- Validate and sanitize arguments and environment input.
- Avoid command injection patterns.
- Keep help text, defaults, and exit codes stable.
- Protect secrets in logs and error output.

## Contract Checklist
1. `--help` output is accurate.
2. Exit codes are meaningful and stable.
3. Required/optional args are explicit.
4. Unsafe inputs fail fast with clear errors.

## Guardrails
- Do not print credentials/tokens in stdout or logs.
- Do not silently change CLI semantics.
- Do not rely on implicit privilege assumptions.
