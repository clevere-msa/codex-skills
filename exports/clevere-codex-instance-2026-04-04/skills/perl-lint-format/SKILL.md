---
name: perl-lint-format
description: "Apply Perl linting and formatting standards with Perl::Critic and Perl::Tidy while minimizing noisy diffs. Use when enforcing style rules, preparing code for review, reducing maintainability risks, or cleaning Perl files before release."
---

# Perl Lint Format

## Overview
Use this skill to enforce consistent Perl style with minimal behavioral risk.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Workflow
1. Discover active lint/format config files.
2. Run lint first to identify policy violations.
3. Apply formatting to changed files only unless full reformat is requested.
4. Re-run lint and compile checks.
5. Report remaining violations with policy names.

## Config Discovery
Check for repository policy files first:
- `.perlcriticrc`
- `.perltidyrc`
- `perltidyrc`

If none exist, state defaults used.

## Commands
Lint:
```bash
perlcritic path/to/file.pm
```

Format in place:
```bash
perltidy -b path/to/file.pm
```

Compile check after formatting:
```bash
perl -c path/to/file.pm
```

## Diff Control
- Prefer file-scoped formatting over repository-wide formatting.
- Keep semantic changes separate from style-only changes where practical.
- If perltidy causes large reflow, call it out before proceeding broadly.

## Report Format
Return:
1. Files linted/formatted.
2. Policy config used.
3. Violations fixed.
4. Violations deferred.
5. Compile/test impact.

## Guardrails
- Do not introduce style churn in untouched files unless requested.
- Do not suppress critic policies without explicit rationale.
- Preserve existing indentation or wrapping in legacy files when policy allows either style.
