# Perl Testing Patterns

## Preferred approach
- Match the repo’s existing test framework.
- Use `subtest` for structured cases.
- Use fixtures sparingly; keep tests deterministic.

## Coverage targets (per change)
- Primary success case
- At least one failure/edge case
- Regression scenario when fixing a bug

## Commands
- Prefer repo canonical command (e.g., `prove -lr t`, `make test`).
