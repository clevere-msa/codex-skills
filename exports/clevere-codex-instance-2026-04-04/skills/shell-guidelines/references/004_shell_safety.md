# Shell Safety

## Defaults
- Use: `set -euo pipefail`
- Quote variables. Use explicit paths. Avoid unsafe globbing.

## Prohibited without explicit permission
- `rm -rf` (or equivalent)
- `chmod -R` / `chown -R`
- Mass edits (sed over entire repo) unless narrowly scoped
- Writing into sensitive locations (/, /etc, /usr) unless requested and necessary

## Logging
- Prefer commands that are easy to reproduce.
- Capture key outputs (redact secrets).
