# Python Security Basics

## Common pitfalls
- Avoid unsafe deserialization (pickle/yaml load without SafeLoader).
- Use timeouts for HTTP requests; validate URLs if user-provided.
- Avoid shell=True; use list-form subprocess with input validation.
- Do not log secrets; redact tokens/keys.

## File handling
- Prevent path traversal when handling user-provided paths.
