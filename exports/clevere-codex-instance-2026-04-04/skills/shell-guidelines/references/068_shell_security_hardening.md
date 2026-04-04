# Shell Security Hardening (Codex Skill)

## Injection Avoidance
- Never build commands via string concatenation when arguments are user-influenced.
- Use arrays to construct commands safely:
  - `cmd=(tool --flag "$val"); "${cmd[@]}"`
- Avoid `xargs` without `-0` when handling arbitrary filenames.

## Path Safety
- Resolve and validate paths for destructive actions.
- Prefer allowlists of base directories.
- Guard against empty variables:
  - `: "${VAR:?VAR must be set}"`

## Sensitive Data
- Redact secrets in logs; do not write them to disk.
- Be cautious with `set -x`; if enabled, ensure secrets cannot be printed.

## Permissions
- Apply least-privilege file modes:
  - secrets/config: `chmod 600`
  - executables: `chmod 755` (or repo policy)
