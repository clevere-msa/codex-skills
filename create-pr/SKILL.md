---
name: create-pr
description: "Pull requests: prepare/open focused PRs with current evidence, eligible reviewers, and explicit merge controls."
---

# Create a PR

## Goal
Produce a PR that’s easy to review and safe to merge:
- small, scoped changes
- green checks (lint/tests/build as appropriate)
- clear description + validation steps

## Workflow (checklist)
1) Confirm scope
   - Restate the goal and acceptance criteria.
   - Identify files likely to change; avoid unrelated cleanup.
   - Discover the GitHub owner type with `gh repo view --json nameWithOwner,owner`.
   - In an MSA-governed repository owned by an `Organization`, verify an approved Jira authorization exists. A `User`-owned repository is Jira-optional. Ask only when ownership cannot be discovered.
2) Create a branch
   - Use a descriptive name: `fix/<topic>`, `feat/<topic>`, `chore/<topic>`.
   - In MSA repos, base new branches on `origin/aws` when that branch exists; otherwise use the repo-local documented source-of-truth branch or remote default branch.
3) Implement changes
   - Keep diffs focused; prefer small commits.
4) Run quality gates
   - Run the repo’s standard commands (lint/tests/build).
   - If `bun.lock` exists, prefer `bun lint` / `bun build`.
   - If `bun.lock` exists but `bun` is not available, tell the user and ask whether to install `bun` or use the repo’s alternative package manager.
5) Commit
   - Prefer Conventional Commits: `fix: ...`, `feat: ...`, `chore: ...`.
6) Discover live controls
   - Inspect the target branch's current protection/ruleset and required status checks.
   - Resolve applicable CODEOWNERS entries for every changed file and verify the requested user or
     team is eligible and has the repository permission GitHub requires.
   - Stop on missing or invalid CODEOWNERS, ineligible reviewers, or a control that cannot be
     verified. Report an escalation route; do not silently downgrade reviewer ownership.
7) Reject stale evidence
   - Require validation evidence generated with the target branch as `--base-ref` to match the PR
     head SHA, resolved merge base, and changed-file set.
   - Treat dirty-worktree evidence as unbound and an older SHA/scope as stale. Regenerate before
     presenting it as review evidence.
8) Push + open PR
   - Always use GitHub CLI (`gh`) for PR workflows (e.g. `gh pr create --fill`).
   - In MSA repos, target PRs to `aws` when that branch exists; otherwise target the repo-local documented source-of-truth branch or remote default branch.
   - If `gh` is not authenticated, run `gh auth login` (or `gh auth status` to check).
   - If `gh` is not installed or cannot be authenticated, tell the user and ask whether to install/authenticate or proceed with manual PR creation steps.
9) Fill in the standardized review packet
   - Use `references/pr-description-template.md`.
   - For organization-owned MSA PRs, title the PR `<KEY>: <short description>` so the bare key remains machine-readable.
   - For personal repositories, use the normal descriptive title; Jira links are optional traceability and do not gate delivery.
   - When Jira authorization applies, link the ticket in prose. Always disclose the Codex model and session used for the change.
   - Include Outcome, Acceptance evidence, Validation, Control path, Risks/rollback, and Remaining
     blockers. Name the head SHA, reviewer ownership, pending gates, and evidence identity.
10) Route review and optional merge automation
   - Assign an eligible reviewer derived from the live control state.
   - Keep approval and merge automation blocked while a required check is failing or evidence is
     stale.
   - Enable auto-merge or enter a merge queue only when the user explicitly authorized that exact
     action, required checks and review behavior are understood, and the repository supports it.
   - Re-read head SHA, checks, and review state after enrollment.

## Notes
- Don't force-push unless you're sure it's safe for collaborators.
- If the PR changes UX, include screenshots or a short GIF.
- Prefer `gh` for create/view/checks (e.g. `gh pr view`, `gh pr checks`).
- Opening a PR is not merging it. Where the branch requires review, the approval must come from
  someone other than the author, and a code-owner rule narrows that further to the owning team --
  being a repo admin does not bypass it when `enforce_admins` is on. Check before assuming a merge
  is available to you:
  ```bash
  gh pr view <n> --json mergeStateStatus,reviewDecision
  gh api /repos/<owner>/<repo>/branches/<branch>/protection --jq '.required_pull_request_reviews'
  ```
- A CODEOWNERS entry naming a team is **silently ignored** by GitHub unless that team is visible
  and has **explicit write access** to the repository. Read or triage access is not enough, so
  confirming the team "has access" can pass while review routing stays broken. If code-owner
  review appears to be required but no reviewer is ever requested, check the permission level:
  ```bash
  gh api /repos/<owner>/<repo>/teams --jq '.[] | "\(.slug): \(.permission)"'
  ```
  See [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

## Deliverable
Provide:
- Branch name and PR URL (or the exact steps to open it manually).
- PR title/body (using `references/pr-description-template.md`).
- Commits included and verification commands run.
- Screenshots/GIFs if UX changed.
- Live control summary, reviewer route, evidence binding, and remaining gates.

PR creation is not ticket completion. Report completion only from the orchestrating workflow after
required checks, authoritative approvals, merge readiness, and requested handoff are established.
