# Review-Ready Gate (Codex Skill)

## Purpose
Define an objective bar for declaring work ready for human review or acceptance.

## Required Before “READY FOR REVIEW”
- Acceptance criteria checklist updated and mapped to evidence
- Tests/verification run and recorded (commands + PASS/FAIL)
- No commented-out code or debug prints left behind
- Continuity ledger updated (if used)
- Diff is minimal and scoped; no unrelated churn

## Output Requirements
Provide a short “Review Packet”:
- What changed (1–3 bullets)
- Files touched
- How to verify (exact commands)
- Risks/edge cases
- Follow-ups (if any)

## Failure Conditions
- Declaring review-ready without evidence
- Hidden TODOs in code that affect correctness
