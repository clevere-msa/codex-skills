---
name: shell-guidelines
description: Router skill for shell engineering standards across safety/idempotency, testing/CI, and security/CLI contracts. Use when a shell task spans multiple concerns and you need to select the right specialized shell skill(s).
---

# Shell Guidelines

Use this skill as the entry point for shell tasks, then route to the smallest set of specialized skills.

## Routing Map
- Safety and idempotent state changes: `shell-safety-idempotency`
- Test execution and CI evidence: `shell-testing-ci`
- Security hardening and CLI contracts: `shell-security-cli-contracts`

## Skill Matrix
For decision table and combinations, use:
- references/070_shell_skill_matrix.md

## Usage Pattern
1. Identify dominant shell concern(s).
2. Invoke matching specialized skill(s).
3. Keep overlap minimal and avoid duplicate instructions.

## Legacy References
These remain available for baseline guidance:
- references/004_shell_safety.md
- references/065_shell_project_conventions.md
- references/066_shell_safety_and_idempotency.md
- references/067_shell_testing_and_ci.md
- references/068_shell_security_hardening.md
- references/069_shell_style_and_cli_contracts.md
