---
name: coding-guidelines-verify
description: "Coding-guideline verification: check changed files against nearest AGENTS.md; emit JSON evidence/review packets."
---

# Coding guidelines verifier

## Goal
Validate that changes follow the **nearest nested** `AGENTS.md`:
- default: **changed files only**
- default: **auto-fix formatting** before lint/tests
- monorepo-aware: each module’s `AGENTS.md` is the source of truth for that scope

## Workflow (checklist)
1) Collect changed files (staged + unstaged + untracked).
2) For each changed file, find the nearest parent `AGENTS.md`.
   - If a file has no scoped `AGENTS.md`, report it (suggest running `coding-guidelines-gen`).
3) Parse the `codex-guidelines` block (schema: `references/verifiable-block.md`).
4) Run, per scope:
   - format (auto-fix) -> lint -> tests
   - apply simple forbid rules (globs/regex) from the block
5) Produce a short compliance report (template: `references/report-template.md`).

## Automation
Use `scripts/verify_guidelines.py` to group scopes, run commands, and report results.
- Preserve console-only behavior by omitting output options.
- Use the default changed-files mode for uncommitted working-tree and index changes.
- Use `--base-ref <target-branch>` after committing to verify the merge-base-to-`HEAD` PR scope,
  including deletions and any additional local changes.
- Use `--all` only when whole-repository evidence is required. It is mutually exclusive with
  `--base-ref`.
- Add `--evidence-json <path>` for schema-version-1 canonical evidence.
- Add `--review-packet <path>` for rendered Markdown with Outcome, Acceptance evidence,
  Validation, Control path, Risks/rollback, and Remaining blockers.
- Evidence excludes raw stdout/stderr and secrets. Dirty-worktree and empty-scope evidence is
  unbound. A regenerated artifact is current; `prior_evidence` reports whether the file it replaced
  was current, stale, or unreadable.

See `references/evidence-schema-v1.md` for the stable JSON contract and
`references/report-template.md` for the Markdown contract.

From a fresh login shell, run the shared checkout with:

```bash
cd "$HOME/<path-to-shared-dev-agent-skills>" && \
  python3 skills/coding-guidelines-verify/scripts/verify_guidelines.py \
    --base-ref origin/main \
    --evidence-json /tmp/coding-guidelines-evidence.json \
    --review-packet /tmp/coding-guidelines-review.md
```
- If `python` is not available or the script fails, tell the user and ask whether to install Python or proceed with a manual per-scope verification.

## Deliverable
Provide:
- The per-scope compliance report (use `references/report-template.md`).
- Any auto-fix formatting changes applied.
- Lint/test commands run and their results, plus any violations.
- Evidence paths, binding state, scope/base identity, and prior-evidence status when output options
  are used.
