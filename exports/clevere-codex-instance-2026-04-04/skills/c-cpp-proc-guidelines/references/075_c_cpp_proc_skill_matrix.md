# C Cpp Pro C Skill Matrix

Use this matrix to route native and Pro*C tasks.

## Primary Routing
| Task type | Primary skill | Add these only if needed |
|---|---|---|
| C/C++ coding conventions and interface edits | `c-cpp-code-conventions` | `c-cpp-testing-patterns` |
| Compile/link/debug failures | `c-cpp-build-debug` | `c-cpp-code-conventions` |
| Add/adjust native tests | `c-cpp-testing-patterns` | `c-cpp-build-debug` |
| Embedded SQL/Pro*C updates | `oracle-proc-guidelines` | `c-cpp-build-debug` |

## Conflict Resolution
1. If Pro*C or embedded SQL is touched, include `oracle-proc-guidelines`.
2. If build or runtime failure is present, include `c-cpp-build-debug`.
3. If interface/header contracts changed, include `c-cpp-code-conventions`.
4. If acceptance needs evidence, include `c-cpp-testing-patterns`.

## Scope Rule
Choose one primary skill, then add secondary skills only for concrete concerns in scope.
