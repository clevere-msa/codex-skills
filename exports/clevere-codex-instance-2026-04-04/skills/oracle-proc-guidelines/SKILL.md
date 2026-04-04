---
name: oracle-proc-guidelines
description: Oracle Pro*C-specific conventions for embedded SQL, host variables, precompiler constraints, and runtime safety. Use when editing Pro*C files, SQL/C integration code, or build flows that invoke Pro*C preprocessing.
---

# Oracle Pro C Guidelines

Use this skill for Pro*C-specific correctness and maintainability.
Routing note: for multi-concern routing, use `c-cpp-proc-guidelines` and `c-cpp-proc-guidelines/references/075_c_cpp_proc_skill_matrix.md`.

## Focus Areas
- Preserve safe host variable usage and type mapping.
- Keep SQL error handling explicit and consistent.
- Respect precompiler/toolchain constraints.
- Validate integration boundaries between SQL and C layers.

## Guardrails
- Do not alter SQL embedding style without validating precompile output.
- Do not mix Pro*C rewrites with unrelated C/C++ refactors.
- Keep DB-impacting behavior changes testable and explicit.
