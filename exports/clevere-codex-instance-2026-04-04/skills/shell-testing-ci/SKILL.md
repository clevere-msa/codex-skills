---
name: shell-testing-ci
description: Shell testing and CI validation workflow for scripts and operational tooling. Use when adding regression checks, validating script behavior, or tightening quality gates for shell changes.
---

# Shell Testing CI

Use this skill when shell changes need executable evidence.
Routing note: for multi-concern routing, use `shell-guidelines` and `shell-guidelines/references/070_shell_skill_matrix.md`.

## Workflow
1. Run syntax checks first.
2. Run linters/static checks available in repo.
3. Execute focused runtime checks (dry-run first where supported).
4. Expand to broader CI-equivalent checks.
5. Report failures with root cause and reproduction command.

## Common Commands
```bash
bash -n path/to/script.sh
```

```bash
shellcheck path/to/script.sh
```

## Guardrails
- Do not mark tests passing without command evidence.
- Do not skip dry-run paths when scripts support them.
- Keep test changes separate from behavior changes when practical.
