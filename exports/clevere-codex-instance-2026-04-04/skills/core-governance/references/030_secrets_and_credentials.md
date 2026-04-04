# Secrets and Credentials

## Handling
- Never print secrets to stdout/stderr or commit them to repo.
- Redact tokens/keys/passwords in logs and examples.
- Prefer `.env.example` patterns and documented env vars.

## Storage
- Prefer OS keyring / dedicated secrets manager when available.
- If not available, document a least-bad local dev approach (restricted perms, short-lived, rotation).
