# Oracle Pro*C (Pro*C/C++) Conventions (Codex Skill)

## Goals
- Deterministic, minimal diffs; ensure `proc` precompile + C/C++ compile + link succeed.
- Preserve SQL semantics; avoid changing schema expectations unless explicitly requested.

## Build Pipeline (Must respect)
1) Precompile: `proc` (or repo wrapper) generates `.c`/`.cpp` from `.pc`
2) Compile generated C/C++
3) Link with Oracle client libraries (often `-lclntsh`, plus system libs)

## Pro*C Code Patterns
- Always use explicit error handling paths:
  - `EXEC SQL WHENEVER SQLERROR ...;` (if repo uses it) OR
  - explicit checks using `sqlca.sqlcode` after statements
- Do not mix styles in the same module unless repo already does.

## SQLCA / Error Handling
- If using SQLCA:
  - Check `sqlca.sqlcode` after DML/DDL/SELECT as required by repo patterns.
  - For diagnostics, use `sqlca.sqlerrm.sqlerrmc` (ensure bounded usage).
- No secret leakage: avoid logging full connection strings or credentials.

## Host Variables & Indicators
- Ensure host variables match Oracle types and sizes.
- Use indicator variables for nullable columns; do not ignore nullability.
- Validate buffer sizes for `VARCHAR`-like host variables; avoid overflow.
- For strings:
  - Follow repo’s conventions for `VARCHAR` struct vs C strings.
  - Ensure explicit null-termination when converting to C strings.

## Transactions
- Do not introduce implicit commits/rollbacks.
- Match repo conventions:
  - explicit `COMMIT WORK` / `ROLLBACK`
  - autocommit policy (if any)
- Be careful with error paths to avoid leaving transactions open.

## Cursor Discipline
- Ensure every opened cursor is closed on all paths.
- For fetch loops:
  - handle `NOT FOUND` / end-of-data consistently
  - avoid infinite loops on unexpected codes

## Precompiler Options (Do not guess)
- Respect existing proc options in Makefile/scripts (e.g., `sqlcheck=`, `userid=`, `include=`, `iname=`, `oname=`, `parse=`, `unsafe_null=`)
- If missing, do not invent; discover from repo build scripts/CI.

## Verification
- Confirm these steps succeed:
  - `proc` generates output deterministically
  - compilation passes
  - link passes (Oracle libs resolved)
  - a minimal runtime smoke test if repo provides one (without real creds)

## Failure Conditions
- Generated code not reproducible or not tracked per repo policy
- Null handling regression (missing indicators)
- Transaction/cursor leaks
- Build breaks due to proc option drift
