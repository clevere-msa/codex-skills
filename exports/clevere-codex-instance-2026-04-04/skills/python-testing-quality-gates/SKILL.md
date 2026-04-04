---
name: python-testing-quality-gates
description: Python testing strategy and quality-gate enforcement for safe changes. Use when adding tests, debugging regressions, or validating lint/type/test gates before merge or release.
---

# Python Testing Quality Gates

Use this skill to produce evidence that Python changes are safe.
Routing note: for multi-concern routing, use `python-guidelines` and `python-guidelines/references/065_python_skill_matrix.md`.

## Workflow
1. Add or update focused tests around changed behavior.
2. Run targeted tests first, then broader suite.
3. Run quality gates used by the repository (lint/type/format/check).
4. Report gate outcomes and remaining risks.

## Guardrails
- Do not broaden assertions to hide regressions.
- Do not claim pass without command output.
- Keep flaky or environment-specific assumptions explicit.
