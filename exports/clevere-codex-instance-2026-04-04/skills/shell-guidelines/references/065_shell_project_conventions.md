# Shell Project Conventions (Codex Skill)

## Goals
- Deterministic, safe scripts that behave correctly in CI and production-like environments.
- Minimal diffs; preserve existing calling conventions and outputs unless explicitly requested.

## Baseline Safety
- Use `#!/usr/bin/env bash` when Bash is required; otherwise prefer POSIX `sh` if repo mandates.
- Default strict mode (Bash):
  - `set -euo pipefail`
  - `IFS=$'\n\t'` for scripts that iterate over words (apply only if safe for repo)
- Quote variables and command substitutions: `"$var"`, `"$(cmd)"`.
- Prefer arrays over word-splitting for argument lists.
- Avoid `eval`. If unavoidable, treat as security-sensitive and justify.

## Portability
- Do not assume GNU vs BSD tool behavior unless repo targets a specific OS.
- Prefer POSIX tools and flags where possible; otherwise gate OS-specific behavior.

## Output Stability
- Preserve stdout/stderr behavior relied upon by callers.
- For CLIs, provide `--help`/usage text if appropriate, but do not change interface without explicit request.

## Filesystem Discipline
- Use explicit paths; avoid `cd` gymnastics. If `cd` is needed, use `pushd/popd` or subshell.
- Create temp files/dirs with `mktemp`; ensure cleanup with traps.

## Security
- Never echo secrets (tokens, passwords, private keys).
- Avoid unsafe globbing and unbounded expansions.
- Validate user-provided paths/inputs (prevent path traversal, injection into commands).

## Verification
- Lint (if available): shellcheck
- Format (if enforced): shfmt
- Smoke test: run with representative args and failure cases.
