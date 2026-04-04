# CI Alignment

## Goal
Match local verification to CI expectations.

## Actions
- Find CI config and identify canonical commands.
- Prefer `make test` / `tox` / `nox` targets if used.
- Ensure version constraints match CI (python version, perl version, env vars).

## Output
- List the CI-relevant commands and what you ran locally.
