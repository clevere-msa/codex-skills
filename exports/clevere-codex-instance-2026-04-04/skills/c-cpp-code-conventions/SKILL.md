---
name: c-cpp-code-conventions
description: C and C++ coding conventions for maintainable, low-risk native changes. Use when editing C/C++ source or headers, refactoring interfaces, or aligning new code with project standards.
---

# C Cpp Code Conventions

Use this skill for source-level C/C++ coding standards.
Routing note: for multi-concern routing, use `c-cpp-proc-guidelines` and `c-cpp-proc-guidelines/references/075_c_cpp_proc_skill_matrix.md`.

## Focus Areas
- Preserve established naming, ownership, and error-handling patterns.
- Keep header/source contracts clear and minimal.
- Minimize undefined behavior and lifetime hazards.
- Prefer small, reviewable refactors.

## Guardrails
- Do not mix broad style churn with behavior changes.
- Do not introduce ABI-risking changes without explicit requirement.
- Keep cross-module contract changes explicit and documented.
