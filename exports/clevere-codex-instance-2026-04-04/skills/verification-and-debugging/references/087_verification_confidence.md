# Verification Confidence (Codex Skill)

## Purpose
Make verification meaningful and appropriately scoped to the change.

## Verification Levels (record one or more)
- STATIC: lint/typecheck/compile only
- UNIT: unit tests for changed logic
- INTEGRATION: integration tests across components
- SMOKE: minimal runtime validation (non-production)
- MANUAL: deterministic checklist when automation is impossible

## Default Requirement
- Logic/behavior change: UNIT + (INTEGRATION or SMOKE) when available
- Refactor (no behavior intended): UNIT or existing suite sufficient
- Build/system changes: STATIC + SMOKE when applicable

## Evidence Rules
- Record exact commands run and PASS/FAIL.
- If tests were skipped, state why and provide an alternative verification artifact.

## Anti-Patterns
- “Tests passed” without stating which tests and how they map to acceptance criteria
- Running an unrelated test subset and declaring success

## Failure Conditions
- No verification evidence for a behavior change
- Verification does not cover acceptance criteria
