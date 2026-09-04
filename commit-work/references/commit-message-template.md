# Commit message template (Conventional Commits)

```text
<type>(<scope>): <summary>

<What changed.>
<Why it changed.>

[Change-Ticket: <KEY>]
AI-Assisted-By: Codex/<model> (<session>)
Agent-Session: <session>
Agent-Model: <model>
```

Notes:
- Keep the summary imperative and specific ("Add", "Fix", "Remove", "Refactor").
- Avoid implementation minutiae; focus on behavior and intent.
- If breaking: use `!` in header and/or add `BREAKING CHANGE:` footer.
- Organization-owned MSA commits require all four evidence trailers above.
  Personal-repository commits omit the bracketed `Change-Ticket:` line unless
  the user wants optional Jira traceability. Discover the GitHub owner type and
  ask only when it cannot be resolved.
- Every AI-assisted commit requires the three AI provenance trailers. Stop
  rather than using placeholders when the SessionStart identity is missing.
- Keep `Change-Ticket:` bare for machine matching; link any ticket mentioned in
  prose to its Jira source of record.
