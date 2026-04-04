# Python Testing Patterns (pytest-centric)

## Preferred approach
- Use pytest if present; match repo fixture patterns.
- Keep tests deterministic; avoid sleeps and time-based flakiness.

## Coverage targets (per change)
- Success case
- Failure/edge case
- Regression scenario for bugs

## Commands
- Prefer repo canonical command (e.g., `pytest -q`, `tox -e py`, `nox -s tests`).
