# Diff Hygiene

## Principles
- No drive-by refactors.
- No style-only changes unless required by repo lint/format gates for touched files.
- Keep changes localized and reversible.

## Patch style
- Prefer small, focused hunks.
- Avoid reordering imports/uses unless needed.
- Preserve file structure and naming conventions.

## Documentation
- If behavior changes, update docs or comments where users will see it.
- If a bug is fixed, add a regression test when feasible.
