# Compliance report template

When `--review-packet` is used, render these headings in order:

1. Outcome
2. Acceptance evidence
3. Validation
4. Control path
5. Risks/rollback
6. Remaining blockers

The console summary remains:

- **Mode:** changed-files (default) | commit-range (`--base-ref`) | all-files
- **Auto-fix formatting:** yes | no
- **Scopes checked:** <count>
- **Result:** pass | fail

Per scope:
- `<path to AGENTS.md>`:
  - Format: ok | fail
  - Lint: ok | fail
  - Tests: ok | fail | skipped (optional)
  - Rule violations: none | <summary>

If failing:
- Missing scoped `AGENTS.md`: <paths>
- Missing/invalid `codex-guidelines` blocks: <paths>
- Command failures: <what + where>
- Rule violations: <what + where>
