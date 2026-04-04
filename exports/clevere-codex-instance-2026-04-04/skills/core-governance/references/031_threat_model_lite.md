# Threat Model Lite

## Quick checklist
- Entry points: CLI, HTTP handlers, background jobs
- Trust boundaries: user input, external services, file system
- Common risks: injection, SSRF, path traversal, authz bypass, deserialization
- Data handling: PII, credentials, tokens, logs

## Output
- Identify top 3 plausible risks introduced/touched by the change and how mitigated.
