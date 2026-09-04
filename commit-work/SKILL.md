---
name: commit-work
description: "Git commits: inspect, stage, split, message, and verify focused Conventional Commits."
---

# Commit work

## Goal
Make commits that are easy to review and safe to ship:
- only intended changes are included
- commits are logically scoped (split when needed)
- commit messages describe what changed and why

## Inputs to ask for (if missing)
- Single commit or multiple commits? (If unsure: default to multiple small commits when there are unrelated changes.)
- Commit style: Conventional Commits are required.
- Any rules: max subject length, required scopes.

## MSA authorization and provenance

First discover the repository's GitHub owner type, for example with
`gh repo view --json nameWithOwner,owner`. In an MSA-governed repository:

- If GitHub reports the owner type as `Organization`, require an approved Jira
  work item and include `Change-Ticket:`.
- If GitHub reports the owner type as `User`, Jira is optional traceability;
  do not require a ticket or `Change-Ticket:`.
- Ask the user only when ownership cannot be discovered.

Always require the session identity supplied by the Codex `SessionStart` hook.
Stop if the session or model is missing. Organization-owned MSA commits use all
four trailers:

```text
Change-Ticket: <KEY>
AI-Assisted-By: Codex/<model> (<session>)
Agent-Session: <session>
Agent-Model: <model>
```

Keep the ticket key bare in `Change-Ticket:` for automated evidence checks. If
the commit body names the ticket, link it to its Jira URL there.

Personal-repository commits omit `Change-Ticket:` unless the user explicitly
chooses to retain it as optional traceability. They still use the three AI
provenance trailers with the values announced in the session banner.

## Workflow (checklist)
1) Inspect the working tree before staging
   - `git status`
   - `git diff` (unstaged)
   - If many changes: `git diff --stat`
2) Decide commit boundaries (split if needed)
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.
   - If changes are mixed in one file, plan to use patch staging.
3) Stage only what belongs in the next commit
   - Prefer patch staging for mixed changes: `git add -p`
   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`
   - If the commit is whole-file (no partial hunks), prefer the committer helper:
     - `committer.ps1 "type(scope): summary" path1 path2 ...`
       - If script execution is blocked, run: `pwsh -File committer.ps1 "type(scope): summary" path1 path2 ...`
     - It clears the index and stages exactly the files you list (never use `.`).
     - Use `--force` only if git reports a stale `.git/index.lock`.
     - Skip it when you need partial hunks or a multi-line commit message body.
4) Review what will actually be committed
   - `git diff --cached`
   - Sanity checks:
     - no secrets or tokens
     - no accidental debug logging
     - no unrelated formatting churn
5) Describe the staged change in 1-2 sentences (before writing the message)
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.
6) Write the commit message
   - Use Conventional Commits (required):
     - `type(scope): short summary`
     - blank line
     - body (what/why, not implementation diary)
     - footer (BREAKING CHANGE) if needed
   - If type choice is unclear, use `references/conventional-commit-types.md`.
   - Prefer an editor for multi-line messages: `git commit -v`
   - Use `references/commit-message-template.md` if helpful.
7) Run the smallest relevant verification
   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on.
8) Repeat for the next commit until the working tree is clean

## Deliverable
Provide:
- the final commit message(s)
- a short summary per commit (what/why)
- the commands used to stage/review (at minimum: `git diff --cached`, plus any tests run)
