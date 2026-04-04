---
name: continuity-ledger
description: Maintain a per-workspace continuity ledger across sessions. Update it at the start of every turn and whenever goals, constraints, decisions, state, or tool outcomes change.
---

# Continuity Ledger

Use this skill to keep a compact, durable record of work state across sessions.
Each agent instance writes to its own per-session ledger under `~/.ledger/<session_id>/`.

When updating the ledger, prefer the filesystem MCP tools for reads/writes to avoid approval prompts under strict sandbox policies.

## References
- references/continuity_guide.md
