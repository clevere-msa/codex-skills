# Global Governance (Codex Skills)

## Non-negotiables
- Prefer deterministic, minimal, test-backed changes.
- Always apply the Continuity Ledger skill every session; update the ledger at the start of every assistant turn.
- Auto-apply relevant MCP skills from ~/.codex/skills without prompting when the task matches their scope.
- No scope drift: implement only what is necessary for stated acceptance criteria.
- No secrets exfiltration: never print or persist credentials, tokens, private keys, or sensitive PII. Redact if encountered.
- No destructive operations by default:
  - Do not run `rm -rf`, mass deletes, or irreversible migrations without explicit user authorization.
  - Avoid rewriting large file sets (formatters across repo) unless required by repo policy for the touched files.
- Least privilege: do not assume root/admin; do not alter system-wide configuration unless explicitly asked and safe.
- Avoid network calls that fetch or upload data unless explicitly required.

## Change discipline
- Make the smallest diff that satisfies acceptance criteria.
- Preserve public APIs and behavior unless explicitly requested to change.
- Prefer refactors only when required to make the fix correct and maintainable.

## Evidence requirement
- Do not claim “fixed” without verification evidence (tests, reproducible steps, or equivalent).
