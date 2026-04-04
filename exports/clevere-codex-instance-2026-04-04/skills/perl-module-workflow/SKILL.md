---
name: perl-module-workflow
description: Create, refactor, and maintain Perl modules (.pm) and related Perl code with stable interfaces and low-risk edits. Use when implementing module features, changing exports, cleaning package structure, fixing compile/runtime issues, or reviewing Perl module design.
---

# Perl Module Workflow

## Overview
Use this skill for safe, incremental Perl module development with strong compile/test feedback.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Workflow
1. Identify the module and call sites.
2. Make minimal behavioral changes first.
3. Compile-check edited files.
4. Run targeted tests, then broader tests if needed.
5. Summarize interface and behavior impact.

## Module Baseline
Apply these defaults unless the repository standard differs:
- `use strict;`
- `use warnings;`
- explicit package name and version strategy already used by the repo
- avoid implicit globals and bareword filehandles

## Change Strategy
- Keep public interfaces stable unless change is requested.
- If interface changes are required, update callers and tests in the same change.
- Prefer small helper subs over deeply nested inline logic.
- Preserve existing error-handling style (`die`, return codes, exceptions) used in that codebase.

## Fast Verification
```bash
perl -c path/to/Module.pm
```

```bash
prove -lv t/path/to/module.t
```

If no targeted test exists, run the nearest relevant test file and record the gap.

## Report Format
Return:
1. Files changed.
2. Interface impact (`none` or exact API change).
3. Compile result.
4. Test result.
5. Follow-up tests still needed.

## Guardrails
- Do not rewrite unrelated modules while refactoring one module.
- Do not change behavior and style in the same large edit unless requested.
- Avoid speculative API redesign; ship the smallest correct change first.
