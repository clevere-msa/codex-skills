# Error Handling Standards

## Principles
- Fail fast on programmer errors; handle expected runtime errors gracefully.
- Prefer explicit errors over silent fallbacks.
- Ensure error messages are actionable and safe (no secrets).

## Perl
- Prefer structured errors (die/croak with context) consistent with repo norms.
- Avoid leaking sensitive values in exception messages.

## Python
- Raise specific exceptions; avoid catching broad Exception unless re-raising with context.
- Use timeouts for I/O where relevant.
