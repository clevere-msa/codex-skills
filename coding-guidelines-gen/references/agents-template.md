# Nested AGENTS.md template (coding guidelines)

Use this as a starting point for each **module root**.

```markdown
# Agent instructions (scope: <module-relative-path>)

## Shared guardrails
- For MSA repos, read the repo-local `.ai-guidelines/system-prompt.md` when present. Until adopted, read `$HOME/ai_guardrails/guidelines/core/system-prompt.md`.
- For AWS/Terraform work, also read `$HOME/ai_guardrails/guidelines/overlays/aws-terraform/`.

## Scope
- Applies to: `<module-relative-path>` and subdirectories
- Languages/tooling: <detected>

## Architecture (high-level)
- Style: layered | hex | clean
- Boundaries:
  - <short bullets; keep enforceable where possible>

## Conventions
- Formatting: <tool> (auto-fix enabled)
- Linting: <tool>
- Tests: <tool>

## Commands
- Format: `<cmd>`
- Lint: `<cmd>`
- Test: `<cmd>`

## Verifiable config (used by `coding-guidelines-verify`)
```codex-guidelines
{
  "version": 1,
  "format": {
    "autofix": true,
    "commands": ["<cmd with optional {files}>"],
    "windows": ["<optional override>"],
    "posix": ["<optional override>"]
  },
  "lint": { "commands": ["<cmd>"], "windows": [], "posix": [] },
  "test": { "commands": ["<cmd>"], "optional": true, "windows": [], "posix": [] },
  "rules": {
    "forbid_globs": [],
    "forbid_regex": [
      { "pattern": "<regex>", "message": "<why this is forbidden>" }
    ]
  }
}
```
```
