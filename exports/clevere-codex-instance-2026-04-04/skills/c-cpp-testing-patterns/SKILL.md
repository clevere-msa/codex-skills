---
name: c-cpp-testing-patterns
description: Testing patterns for C/C++ changes, including unit, integration, and regression-focused validation. Use when adding tests, reproducing native bugs, or proving change safety before merge.
---

# C Cpp Testing Patterns

Use this skill for evidence-driven C/C++ test coverage and regression protection.
Routing note: for multi-concern routing, use `c-cpp-proc-guidelines` and `c-cpp-proc-guidelines/references/075_c_cpp_proc_skill_matrix.md`.

## Workflow
1. Reproduce target behavior with smallest test scope.
2. Add/adjust tests for success and failure cases.
3. Run targeted tests first, then broader suites.
4. Capture failures with root cause and repro command.

## Guardrails
- Do not loosen assertions to hide defects.
- Keep flaky timing-dependent tests explicit.
- Separate test-only edits from production logic when practical.
