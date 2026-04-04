# Architecture Constraints

## Rules of engagement
- Respect layering and module boundaries.
- Avoid introducing new cross-dependencies.
- Keep configuration changes minimal and documented.

## When to refactor
Only if necessary to:
- Fix correctness issues
- Improve testability
- Reduce duplicated logic directly in the changed area

Otherwise, leave architecture unchanged.
