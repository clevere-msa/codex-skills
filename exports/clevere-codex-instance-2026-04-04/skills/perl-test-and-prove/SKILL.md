---
name: perl-test-and-prove
description: "Create, update, and run Perl tests with Test::More and prove for reliable regression checks. Use when adding coverage for new behavior, reproducing bugs, fixing failing tests, or validating Perl code changes before commit."
---

# Perl Test and Prove

## Overview
Use this skill to add high-signal tests and run them efficiently with actionable failure analysis.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Workflow
1. Locate the smallest test scope that exercises the change.
2. Add or update tests for expected behavior and edge cases.
3. Run targeted tests with verbose output.
4. Expand to broader suites only after local pass.
5. Report failures by root cause, not just failing assertions.

## Test Authoring Defaults
- Prefer `Test::More` primitives (`ok`, `is`, `is_deeply`, `like`, `throws_ok` where available).
- Keep one behavioral intent per assertion block.
- Name subtests for fast triage.
- Use fixtures or deterministic setup; avoid time/random/network flakiness unless explicitly required.

## Execution Commands
Targeted run:
```bash
prove -lv t/path/to/test_file.t
```

Directory run:
```bash
prove -lr t/subsystem
```

Full run:
```bash
prove -lr t
```

## Failure Triage
For each failure, capture:
1. failing test name and file
2. expected vs actual
3. whether issue is test bug, code bug, or environment assumption

## Report Format
Return:
1. Tests added/changed.
2. Commands executed.
3. Pass/fail summary.
4. Remaining failures and root cause.
5. Next targeted fix.

## Guardrails
- Do not silently delete failing assertions to make runs pass.
- Do not broaden expected output without linking it to intended behavior change.
- Keep test-only refactors separate from production code changes when possible.
