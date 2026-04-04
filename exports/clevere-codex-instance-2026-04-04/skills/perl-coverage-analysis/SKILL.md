---
name: perl-coverage-analysis
description: "Analyze Perl test coverage using Devel::Cover outputs and prioritize missing tests by risk. Use when evaluating test completeness, finding untested branches/conditions, tracking regressions in coverage, or planning targeted test additions from cover_db."
---

# Perl Coverage Analysis

## Overview
Use this skill to turn coverage data into prioritized, actionable test work.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Workflow
1. Identify existing coverage artifacts (`cover_db` or reports).
2. Generate coverage data if missing.
3. Inspect statement/branch/condition/subroutine coverage.
4. Prioritize gaps by production risk and change frequency.
5. Propose concrete new test cases.

## Generate Coverage (if needed)
```bash
HARNESS_PERL_SWITCHES=-MDevel::Cover prove -lr t
cover
```

## Analyze Coverage
Quick summary:
```bash
cover -summary
```

Detailed analysis:
- Use the `cover-db-parser` skill when deep branch/condition gap extraction is needed.
- Focus first on uncovered logic in auth, billing, scheduling, and error-handling paths.

## Prioritization Rules
Rank gaps in this order:
1. uncovered error paths and exception handling
2. uncovered conditional branches in business logic
3. uncovered boundary cases for parsers/validators
4. untouched low-risk utility code

## Report Format
Return:
1. Coverage source used (`cover_db` path and command context).
2. Top uncovered files/functions.
3. Highest-priority uncovered branches/conditions.
4. Exact test additions recommended.
5. Expected risk reduction.

## Guardrails
- Do not treat raw percentage as success by itself.
- Do not prioritize trivial lines over critical branch logic.
- Call out stale coverage runs if code changed after coverage generation.
