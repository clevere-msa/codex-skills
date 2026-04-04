---
name: shell-safety-idempotency
description: Shell safety and idempotency practices for scripts and automation. Use when editing shell logic that can mutate system state, rerun across environments, or fail partially and require safe retries.
---

# Shell Safety Idempotency

Use this skill for resilient shell execution and repeatable operations.
Routing note: for multi-concern routing, use `shell-guidelines` and `shell-guidelines/references/070_shell_skill_matrix.md`.

## Core Checks
1. Use strict mode where compatible (`set -euo pipefail`).
2. Make mutating steps idempotent and rerunnable.
3. Validate preconditions before side effects.
4. Add clear error paths and exit codes.
5. Avoid hidden global state and unsafe temp file usage.

## Guardrails
- Do not make destructive operations implicit.
- Do not assume tools/files/users exist without checks.
- Keep rollback strategy explicit for stateful actions.
