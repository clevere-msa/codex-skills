# Shell Safety & Idempotency (Codex Skill)

## Idempotency
- Prefer scripts that can be run repeatedly without causing damage:
  - use “create if missing” semantics
  - check state before acting
  - avoid destructive default actions

## Destructive Operations
- Never run or introduce:
  - `rm -rf` without explicit user authorization and guarded paths
  - wildcard deletes without validation
- When deletion is required:
  - validate the target is within an allowed root
  - print the resolved target path
  - require explicit `--force` or confirmation flag if interactive

## Traps & Cleanup
- Use traps to clean up temps:
  - `trap 'cleanup' EXIT INT TERM`
- Ensure cleanup doesn’t delete unexpected paths.

## Robust Argument Parsing
- Prefer `getopts` for POSIX.
- For Bash-only, accept a simple `--flag value` parser if repo already uses it.
- Fail with usage on unknown flags.

## Logging
- Use a consistent log prefix; write errors to stderr.
- Provide a `--verbose` mode when helpful; keep default quiet.
