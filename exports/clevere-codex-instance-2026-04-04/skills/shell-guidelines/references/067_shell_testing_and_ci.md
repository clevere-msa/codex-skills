# Shell Testing & CI (Codex Skill)

## Test Strategy
- Prefer the repo’s existing test harness (bats-core, shunit2, pytest wrappers, make targets).
- If none exists:
  - add a minimal smoke test script under `tests/` or `t/` consistent with repo norms
  - ensure it is deterministic and fast

## What to Test
- Exit codes:
  - success path returns 0
  - expected failures return non-zero and print actionable errors
- Argument parsing:
  - missing required args
  - unknown flags
- Filesystem behaviors:
  - safe handling of spaces/newlines in paths (where relevant)
  - correct temp handling and cleanup

## CI Alignment
- Use the same shell as CI (bash vs sh) and note version differences.
- Record exact commands run and results (PASS/FAIL).

## Tooling
- shellcheck:
  - run on touched scripts; address relevant warnings
- shfmt:
  - apply only if repo enforces; avoid mass formatting
