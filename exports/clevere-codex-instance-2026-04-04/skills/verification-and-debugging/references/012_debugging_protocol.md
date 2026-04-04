# Debugging Protocol

## Steps
1) Reproduce reliably (exact command, inputs, environment notes).
2) Reduce to minimal failing case (narrow test or script).
3) Inspect logs/stack traces; identify the failing invariant.
4) Hypothesize root cause; validate with instrumentation (minimal logging).
5) Implement minimal fix.
6) Add/extend regression test.
7) Re-run targeted tests, then broader suite.

## Guardrails
- Avoid “random edits”. Each change must tie to a hypothesis.
- Prefer reversible instrumentation; remove noisy debug output before finalizing.
