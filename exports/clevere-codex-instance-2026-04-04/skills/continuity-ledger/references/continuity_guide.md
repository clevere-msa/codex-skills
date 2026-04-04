# Continuity Ledger (compaction-safe)

Maintain a single Continuity Ledger for this session in `~/.ledger/<session_id>/CONTINUITY.md`.
Each agent instance uses its own per-session ledger location.

## How it works

- At the start of every assistant turn: read `~/.ledger/<session_id>/CONTINUITY.md`, update it to reflect the latest goal/constraints/decisions/state, then proceed with the work. Prefer filesystem MCP tools for these reads/writes to avoid approval prompts under strict sandbox policies.
- Update `~/.ledger/<session_id>/CONTINUITY.md` again whenever any of these change: goal, constraints/assumptions, key decisions, progress state (Done/Now/Next), or important tool outcomes. Prefer filesystem MCP tools for these writes to avoid approval prompts under strict sandbox policies.
- Keep it short and stable: facts only, no transcripts. Prefer bullets. Mark uncertainty as `UNCONFIRMED` (never guess).
- If you notice missing recall or a compaction/summary event: refresh/rebuild the ledger from visible context, mark gaps `UNCONFIRMED`, ask up to 1–3 targeted questions, then continue.

## functions.update_plan vs the Ledger

- `functions.update_plan` is for short-term execution scaffolding while you work (a small 3–7 step plan with pending/in_progress/completed).
- `~/.ledger/<session_id>/CONTINUITY.md` is for long-running continuity across compaction (the “what/why/current state”), not a step-by-step task list.
- Keep them consistent: when the plan or state changes, update the ledger at the intent/progress level (not every micro-step).
- Store the current short-term plan in `~/.ledger/<session_id>/functions.update_plan`.

## In replies

- Begin with a brief “Ledger Snapshot” (Goal + Now/Next + Open Questions).
- Print the full ledger only when it materially changes or when the user asks.

## Ledger format (keep headings)

- Goal (incl. success criteria):
- Constraints/Assumptions:
- Key decisions:
- State:
- Done:
- Now:
- Next:
- Open questions (UNCONFIRMED if needed):
- Working set (files/ids/commands):

## Secret-safety filter

- Never store credentials, tokens, private keys, or sensitive PII.
- Replace with placeholders: `<REDACTED>`, `<TOKEN>`, `<HOST_ALIAS>`.
