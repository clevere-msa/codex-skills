# Drift Detection (Codex Skill)

## Purpose
Prevent scope creep and accidental refactors during implementation.

## Scope Boundary Rule
- Define a scope boundary in the Plan:
  - acceptance criteria
  - expected files to touch
  - allowed secondary changes (if any)
- Any change outside boundary requires an explicit “Scope Expansion” note.

## Triggers That Indicate Drift
- Touching new directories not in the Plan
- Introducing new dependencies or tooling
- Changing interfaces (APIs/CLIs/file formats) unintentionally
- Large formatting churn or mechanical rewrites
- “While I’m here” refactors

## Required Response to Drift Trigger
1) Pause implementation.
2) State what triggered the drift.
3) Propose the minimal alternative.
4) If scope expansion is truly needed, document it and update Acceptance Criteria.

## Failure Conditions
- Unannounced scope expansion
- Diff includes unrelated refactors or formatting churn
