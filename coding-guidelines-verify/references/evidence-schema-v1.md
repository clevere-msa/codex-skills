# Verification Evidence Schema Version 1

Canonical JSON contains these stable top-level fields:

- `schema_version`: integer `1`;
- `generated_at`: UTC RFC 3339 timestamp;
- `repository`: repository name, remote URL, branch, and commit SHA;
- `binding`: `bound` or `unbound`, dirty state, changed-file digest, stale flag, and reasons;
- `prior_evidence`: whether a replaced evidence file was absent, current, stale, or unreadable,
  with mismatch reasons;
- `scope`: mode, optional base ref and resolved merge-base SHA, changed files, and applicable
  `AGENTS.md` files;
- `commands`: exact command, scope, phase, status, exit code, and optional flag;
- `results`: per-scope phase results;
- `violations`: structured type, scope, path, and message entries; and
- `overall_result`: `pass` or `fail`.

Never include raw stdout/stderr, environment contents, credentials, or secrets. Redact sensitive
values if they appear in a configured command while retaining the command shape. Evidence is
unbound when generated from a dirty worktree or an empty scope.

Use `changed-files` for uncommitted work, `commit-range` with `--base-ref` for a committed PR diff,
and `all-files` for an explicit whole-repository run. Commit-range scope resolves and records the
merge base, includes deletions, and also includes local changes so a dirty run remains complete but
unbound.

A newly generated artifact describes the current run and therefore has `binding.stale: false`.
When it replaces an existing file, `prior_evidence` records whether that older artifact's commit,
scope mode, base commit, or changed-file set no longer matched.
