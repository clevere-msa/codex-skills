# C/C++ Testing Patterns (Codex Skill)

## Prefer existing harness
- If repo uses: CTest, GoogleTest, Catch2, doctest, Unity, CMocka, TAP/prove wrappers—follow that.
- Do not introduce a new framework unless explicitly required.

## Regression-first
- For bug fixes: add a test that fails before the fix and passes after.
- Cover:
  - primary success case
  - one edge/failure case
  - boundary sizes (0, 1, max, off-by-one)

## Determinism
- Avoid timing-based tests unless unavoidable.
- Avoid reliance on global environment; use temp dirs and fixtures.

## Verification Evidence
- Record exact test commands and PASS/FAIL.
- If only integration tests exist, document the reproduction checklist and expected output.
