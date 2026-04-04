# Perl Project Conventions

## Code style
- Follow repo precedent (Test2::V0 vs Test::More, Moo/Moose usage, etc.).
- Prefer `use strict; use warnings;` unless repo explicitly differs.
- Keep packages in `lib/` with matching namespace-to-path mapping.

## Common patterns
- Validate inputs at boundaries.
- Use `Carp` (`croak`) for caller-facing errors when appropriate.
- Avoid shelling out; if required, use safe list-form execution.

## Layout hints
- `lib/` modules, `t/` tests, `bin/` or `script/` executables (repo-dependent).
