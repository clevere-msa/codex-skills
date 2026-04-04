---
name: python-dependency-policy
description: Python dependency policy for deciding when and how to add or change packages safely. Use when proposing new libraries, replacing dependencies, or updating packaging/runtime requirements.
---

# Python Dependency Policy

Use this skill for package selection and dependency governance.
Routing note: for multi-concern routing, use `python-guidelines` and `python-guidelines/references/065_python_skill_matrix.md`.

## Decision Flow
1. Confirm existing dependencies cannot solve the requirement.
2. Evaluate maintenance, adoption, and compatibility.
3. Assess runtime/build and security impact.
4. Document rationale and fallback options.
5. Update dependency metadata and tests consistently.

## Guardrails
- Avoid convenience-only dependencies.
- Keep dependency updates isolated from unrelated refactors.
- Prefer reversible dependency changes when possible.
