# Shell Style & CLI Contracts (Codex Skill)

## Style
- Use functions for logical units; avoid copy/paste blocks.
- Prefer `printf` over `echo` for portability and control.
- Keep variable names descriptive; avoid single-letter names except in tiny scopes.

## CLI Contract
- Usage function: `usage()` prints to stderr.
- Standard flags (if appropriate and consistent with repo):
  - `-h|--help`
  - `-v|--verbose`
  - `-n|--dry-run` (highly recommended for scripts that modify state)
- Always document required environment variables (names only).

## Dry-run Pattern
- Implement a `run()` helper:
  - in dry-run, print the command
  - otherwise, execute
- Ensure dry-run still validates inputs and resolves paths.

## Exit Codes
- 0 success
- 2 usage/argument error
- 1 runtime failure (generic) unless repo uses a specific scheme
