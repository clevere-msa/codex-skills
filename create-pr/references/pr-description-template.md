# PR title
Use Conventional Commits if your team does (e.g. `fix: …`, `feat: …`).

For organization-owned MSA repositories, use `<KEY>: <short description>`.
PR titles do not render Markdown, so retain the bare ticket key for the
authorization gate. For personal repositories, use the normal descriptive
title without a required ticket prefix.

## Authorization (organization-owned MSA repositories)

- Change ticket: [<KEY>](<JIRA-URL>)
- AI assistance: Codex/<model> (session `<session>`)

For a personal repository, omit the change-ticket line and keep any Jira link
only as optional traceability. Retain the AI-assistance disclosure.

## Outcome
What changed and the current delivery state (1–3 bullets).

## Acceptance evidence
Map each acceptance criterion to current evidence.

## Validation
Exact commands and results. Include the evidence schema/version and bound commit SHA when present.

## Control path
Head SHA, applicable controls/CODEOWNERS, eligible reviewer, pending gates, and escalation route.

## Screenshots / GIF (if UI changes)
Before/after or key flows.

## Risks/rollback
Edge cases, rollout boundary, backwards compatibility, and rollback.

## Remaining blockers
Unsatisfied gates or `None`.
