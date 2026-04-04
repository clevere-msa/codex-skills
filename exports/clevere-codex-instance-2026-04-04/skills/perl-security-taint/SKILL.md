---
name: perl-security-taint
description: Perl security and taint-mode guidance for input validation, command execution safety, and sensitive data handling. Use when editing Perl code that consumes external input (HTTP, env, files, CLI), invokes system commands, or runs under taint-related constraints.
---

# Perl Security Taint

Use this skill when a Perl change can affect security posture.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Focus Areas
- Validate and constrain all external inputs.
- Avoid interpolated shell commands.
- Prefer safe list-form command execution.
- Apply safe untainting patterns when taint mode is in play.
- Prevent secret leakage in errors and logs.

## Quick Checklist
1. Identify external input boundaries.
2. Confirm validation and normalization at entry points.
3. Replace shell-string execution with list-form execution where possible.
4. Review file/command/env usage for injection risks.
5. Verify logs and error paths do not expose sensitive values.

## Commands
Compile-check touched files:
```bash
perl -c path/to/file.pm
```

Run targeted tests:
```bash
prove -lv t/path/to/security_or_regression_test.t
```

## Guardrails
- Do not weaken validation to satisfy tests.
- Do not add broad allow-lists without justification.
- Keep security fixes minimal and reviewable.
