---
name: perl-logging-observability
description: Perl logging and observability guidance for actionable diagnostics without leaking sensitive data. Use when modifying log lines, error reporting, request tracing, or instrumentation in Perl services, CGI handlers, and background jobs.
---

# Perl Logging Observability

Use this skill when changing how Perl code emits logs, errors, or diagnostics.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Goals
- Keep logs concise and operationally useful.
- Preserve enough context for debugging.
- Prevent sensitive data exposure.

## Workflow
1. Identify the execution context (CGI, service, batch, worker).
2. Follow existing logger conventions in the repository.
3. Add context fields that improve triage (operation, IDs, phase).
4. Ensure secrets and PII are redacted or omitted.
5. Validate logs are readable and non-noisy under normal conditions.

## Verification
- Compile-check changed Perl files.
- Run targeted tests and, if applicable, smoke checks to inspect emitted logs.

## Guardrails
- Do not log credentials, tokens, session secrets, or raw sensitive payloads.
- Do not spam high-cardinality logs in hot paths.
- Keep log format changes backward-compatible where possible.
