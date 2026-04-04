# Perl Security and Taint Considerations

## Input safety
- Validate all external inputs (CLI args, env vars, HTTP params, file contents).
- Avoid interpolated shell commands.
- If invoking external commands, use list form and sanitize inputs.

## Taint mode
- If repo uses taint mode, ensure data is untainted explicitly and safely.
