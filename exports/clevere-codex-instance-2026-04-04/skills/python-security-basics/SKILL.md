---
name: python-security-basics
description: Python security baseline guidance for input validation, secrets handling, and safe execution patterns. Use when editing Python code that touches external input, file/network I/O, auth/session flows, or sensitive data.
---

# Python Security Basics

Use this skill for security-focused Python reviews and fixes.
Routing note: for multi-concern routing, use `python-guidelines` and `python-guidelines/references/065_python_skill_matrix.md`.

## Checklist
1. Validate and constrain external input at boundaries.
2. Avoid unsafe eval/exec/subprocess patterns.
3. Ensure secrets are not logged or exposed.
4. Handle auth/session/state data with least privilege.
5. Add regression tests for fixed vulnerabilities.

## Guardrails
- Do not weaken validation to pass tests.
- Do not print credentials/tokens in logs.
- Keep security fixes minimal and auditable.
