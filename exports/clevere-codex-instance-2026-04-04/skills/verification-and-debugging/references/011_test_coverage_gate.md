# Test Coverage Gate

## Default expectation
- New behavior or bug fixes should have tests in the repo’s standard test framework.
- At minimum, cover:
  - The primary success case
  - One failure/edge case
  - The reported regression scenario (if applicable)

## Exceptions (must be explicit)
- Legacy area has no test harness and adding one is out-of-scope
- Change is purely operational documentation
- Verification via integration tests already exists and is referenced

## Evidence
- Include the exact commands run and PASS/FAIL results.
