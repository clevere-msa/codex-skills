from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit


CODE_FENCE_RE = re.compile(r"```codex-guidelines\s*\r?\n(.*?)\r?\n```", re.DOTALL)
SCHEMA_VERSION = 1


@dataclass(frozen=True)
class CommandResult:
    command: str
    returncode: int
    stdout: str
    stderr: str


def _run_process(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(cwd), capture_output=True, text=True)


def _git(repo_root: Path, args: list[str]) -> str | None:
    proc = _run_process(["git", *args], cwd=repo_root)
    if proc.returncode != 0:
        return None
    return proc.stdout


def _repo_root() -> Path:
    cwd = Path.cwd().resolve()
    out = _git(cwd, ["rev-parse", "--show-toplevel"])
    return Path(out.strip()).resolve() if out else cwd


def _path_set(output: str | None) -> set[str]:
    return {line.strip() for line in (output or "").splitlines() if line.strip()}


def _changed_files(repo_root: Path, all_files: bool, base_commit: str | None) -> list[Path]:
    if all_files:
        out = _git(repo_root, ["ls-files"]) or ""
        return [repo_root / line for line in out.splitlines() if line.strip()]

    paths: set[str] = set()
    for args in (
        ["diff", "--name-only", "--diff-filter=ACMRTUXBD"],
        ["diff", "--name-only", "--diff-filter=ACMRTUXBD", "--cached"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        paths.update(_path_set(_git(repo_root, args)))

    if base_commit is not None:
        paths.update(
            _path_set(
                _git(
                    repo_root,
                    ["diff", "--name-only", "--diff-filter=ACMRTUXBD", f"{base_commit}..HEAD"],
                )
            )
        )

    # Deleted paths remain part of the evidence scope even though they no longer exist on disk.
    return [(repo_root / rel).resolve() for rel in sorted(paths)]


def _find_nearest_agents(repo_root: Path, file_path: Path) -> Path | None:
    current = file_path.parent.resolve()
    while True:
        candidate = current / "AGENTS.md"
        if candidate.is_file():
            return candidate
        if current == repo_root:
            return None
        current = current.parent


def _extract_guidelines_json(agents_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    text = agents_path.read_text(encoding="utf-8", errors="replace")
    match = CODE_FENCE_RE.search(text)
    if not match:
        return (None, "missing ```codex-guidelines fenced block")
    try:
        data = json.loads(match.group(1).strip())
    except json.JSONDecodeError as exc:
        return (None, f"invalid JSON in codex-guidelines block: {exc}")
    if not isinstance(data, dict):
        return (None, "codex-guidelines JSON must be an object")
    if data.get("version") != 1:
        return (None, "unsupported codex-guidelines version (expected 1)")
    return (data, None)


def _shell_prefix() -> list[str]:
    if os.name == "nt":
        return ["powershell", "-NoProfile", "-NonInteractive", "-Command"]
    return ["bash" if shutil.which("bash") else "sh", "-lc"]


def _quote_paths(paths: Iterable[str]) -> str:
    if os.name == "nt":
        return " ".join("'" + path.replace("'", "''") + "'" for path in paths)
    import shlex

    return " ".join(shlex.quote(path) for path in paths)


def _select_commands(block: dict[str, Any], key: str) -> list[str]:
    section = block.get(key) or {}
    if not isinstance(section, dict):
        return []
    override = section.get("windows" if os.name == "nt" else "posix")
    if isinstance(override, list) and override and all(isinstance(item, str) for item in override):
        return override
    commands = section.get("commands")
    if isinstance(commands, list) and all(isinstance(item, str) for item in commands):
        return commands
    return []


def _run_commands(*, commands: list[str], cwd: Path, changed_rel_files: list[str]) -> list[CommandResult]:
    results: list[CommandResult] = []
    files_arg = _quote_paths(changed_rel_files)
    prefix = _shell_prefix()
    for command in commands:
        expanded = command.replace("{files}", files_arg)
        proc = _run_process([*prefix, expanded], cwd=cwd)
        results.append(CommandResult(expanded, proc.returncode, proc.stdout, proc.stderr))
    return results


def _matches_any_glob(path: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in globs)


def _sanitize_remote(value: str) -> str:
    value = value.strip()
    if "://" not in value:
        return value
    parsed = urlsplit(value)
    hostname = parsed.hostname or ""
    if parsed.port:
        hostname = f"{hostname}:{parsed.port}"
    return urlunsplit((parsed.scheme, hostname, parsed.path, "", ""))


def _redact_command(value: str) -> str:
    redacted = re.sub(r"(https?://)[^/\s@]+@", r"\1<redacted>@", value, flags=re.IGNORECASE)
    redacted = re.sub(
        r"(?i)\b(authorization\s*:\s*bearer)\s+[^\s'\"]+",
        r"\1 <redacted>",
        redacted,
    )
    redacted = re.sub(
        r"(?i)\b(token|password|secret|api[_-]?key)=([^\s]+)",
        r"\1=<redacted>",
        redacted,
    )
    return redacted


def _repository_identity(repo_root: Path) -> dict[str, Any]:
    remote = _git(repo_root, ["config", "--get", "remote.origin.url"]) or ""
    branch = _git(repo_root, ["branch", "--show-current"]) or ""
    sha = _git(repo_root, ["rev-parse", "HEAD"]) or ""
    return {
        "name": repo_root.name,
        "remote_url": _sanitize_remote(remote),
        "branch": branch.strip(),
        "commit_sha": sha.strip() or None,
    }


def _is_dirty(repo_root: Path) -> bool:
    return bool((_git(repo_root, ["status", "--porcelain"]) or "").strip())


def _scope_digest(paths: list[str]) -> str:
    payload = "\n".join(sorted(paths)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_existing_evidence(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"_unreadable": True}
    return value if isinstance(value, dict) else {"_unreadable": True}


def _prior_evidence(
    existing: dict[str, Any] | None,
    repository: dict[str, Any],
    scope: dict[str, Any],
) -> dict[str, Any]:
    if existing is None:
        return {"status": "none", "reasons": []}
    if existing.get("_unreadable"):
        return {"status": "unreadable", "reasons": ["existing evidence is unreadable"]}
    reasons: list[str] = []
    old_sha = (existing.get("repository") or {}).get("commit_sha")
    if old_sha != repository["commit_sha"]:
        reasons.append("commit SHA no longer matches")
    old_scope = existing.get("scope") or {}
    old_files = old_scope.get("changed_files")
    if not isinstance(old_files, list) or sorted(old_files) != sorted(scope["changed_files"]):
        reasons.append("changed-file set no longer matches")
    if old_scope.get("mode") != scope["mode"]:
        reasons.append("scope mode no longer matches")
    if old_scope.get("base_commit_sha") != scope.get("base_commit_sha"):
        reasons.append("base commit no longer matches")
    return {"status": "stale" if reasons else "current", "reasons": reasons}


def _write_json(path: Path, evidence: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _render_review_packet(evidence: dict[str, Any]) -> str:
    result = evidence["overall_result"].upper()
    binding = evidence["binding"]
    repo = evidence["repository"]
    commands = evidence["commands"]
    violations = evidence["violations"]
    validation = "\n".join(
        f"- `{item['phase']}`: `{item['command']}` — {item['status']}"
        for item in commands
    ) or "- No configured commands ran."
    blockers = "\n".join(f"- {item['message']}" for item in violations if item["blocking"])
    if not blockers:
        blockers = "- None."
    stale = ", ".join(binding["stale_reasons"]) or "none"
    prior = evidence["prior_evidence"]
    prior_reasons = ", ".join(prior["reasons"]) or "none"
    return f"""# Verification Review Packet

## Outcome

- **Result:** {result}
- **Repository:** {repo['name']}
- **Commit:** `{repo['commit_sha'] or 'unavailable'}`

## Acceptance evidence

- Coding-guideline evidence schema: version {evidence['schema_version']}.
- Acceptance-criterion mapping must be supplied by the orchestrating ticket or PR workflow.

## Validation

{validation}

## Control path

- Evidence binding: **{binding['status']}**
- Changed-file digest: `{binding['changed_files_digest']}`
- Stale: **{'yes' if binding['stale'] else 'no'}** ({stale})
- Prior evidence: **{prior['status']}** ({prior_reasons})
- Applicable `AGENTS.md`: {', '.join(f'`{path}`' for path in evidence['scope']['applicable_agents']) or 'none'}

## Risks/rollback

- Raw command output and secrets are excluded from this packet.
- Regenerate evidence after any commit or changed-file-set change; rollback is to discard this generated evidence.

## Remaining blockers

{blockers}
"""


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _record_command(
    command_records: list[dict[str, Any]],
    *,
    scope: str,
    phase: str,
    result: CommandResult,
    optional: bool = False,
) -> str:
    if result.returncode == 0:
        status = "pass"
    elif optional:
        status = "optional-fail"
    else:
        status = "fail"
    command_records.append(
        {
            "scope": scope,
            "phase": phase,
            "command": _redact_command(result.command),
            "status": status,
            "exit_code": result.returncode,
            "optional": optional,
        }
    )
    return status


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify nested AGENTS.md coding guidelines (codex-guidelines blocks)."
    )
    parser.add_argument("--all", action="store_true", help="Verify all tracked files (otherwise changed files only).")
    parser.add_argument(
        "--base-ref",
        help="Verify the merge-base-to-HEAD change set for a PR branch, plus local changes.",
    )
    parser.add_argument("--no-fix", action="store_true", help="Do not auto-fix formatting (skip format commands).")
    parser.add_argument("--format-only", action="store_true", help="Run formatting only (skip lint/tests/rules).")
    parser.add_argument("--skip-tests", action="store_true", help="Skip test commands even if configured.")
    parser.add_argument(
        "--allow-unscoped",
        action="store_true",
        help="Do not fail when files have no scoped AGENTS.md.",
    )
    parser.add_argument("--evidence-json", type=Path, help="Write canonical schema-version-1 JSON evidence.")
    parser.add_argument("--review-packet", type=Path, help="Write the standardized Markdown review packet.")
    args = parser.parse_args()

    if args.all and args.base_ref:
        parser.error("--all and --base-ref are mutually exclusive")

    repo_root = _repo_root()
    base_commit = None
    if args.base_ref:
        resolved = _git(repo_root, ["merge-base", args.base_ref, "HEAD"])
        if not resolved or not resolved.strip():
            parser.error(f"cannot resolve merge base for {args.base_ref!r}")
        base_commit = resolved.strip()

    files = _changed_files(repo_root, all_files=args.all, base_commit=base_commit)
    repository = _repository_identity(repo_root)
    changed_files = [path.relative_to(repo_root).as_posix() for path in files]
    existing_evidence = _load_existing_evidence(args.evidence_json)
    dirty = _is_dirty(repo_root)
    scope_mode = "all-files" if args.all else ("commit-range" if args.base_ref else "changed-files")

    by_agents: dict[Path | None, list[Path]] = {}
    for file_path in files:
        by_agents.setdefault(_find_nearest_agents(repo_root, file_path), []).append(file_path)

    failures: list[str] = []
    violations: list[dict[str, Any]] = []
    command_records: list[dict[str, Any]] = []
    scope_results: list[dict[str, Any]] = []

    unscoped = by_agents.get(None, [])
    if unscoped:
        lines = [path.relative_to(repo_root).as_posix() for path in unscoped]
        message = "Missing scoped AGENTS.md for:\n" + "\n".join(f"- {path}" for path in lines)
        if args.allow_unscoped:
            print(message)
        else:
            failures.append(message)
        for path in lines:
            violations.append(
                {
                    "type": "unscoped-file",
                    "scope": None,
                    "path": path,
                    "message": f"Missing scoped AGENTS.md for {path}",
                    "blocking": not args.allow_unscoped,
                }
            )

    scoped_items = sorted((key, value) for key, value in by_agents.items() if key is not None)
    for agents_path, scoped_files in scoped_items:
        assert agents_path is not None
        scope_root = agents_path.parent.resolve()
        rel_scope = agents_path.relative_to(repo_root).as_posix()
        rel_files = [path.relative_to(scope_root).as_posix() for path in scoped_files]
        phase_results = {
            "format": "not-configured",
            "lint": "not-configured",
            "test": "not-configured",
            "rules": "pass",
        }

        block, error = _extract_guidelines_json(agents_path)
        if error is not None:
            message = f"{rel_scope}: {error}"
            failures.append(message)
            violations.append(
                {
                    "type": "invalid-guidelines",
                    "scope": rel_scope,
                    "path": rel_scope,
                    "message": message,
                    "blocking": True,
                }
            )
            scope_results.append({"agents_file": rel_scope, "files": rel_files, "phases": phase_results})
            continue

        assert block is not None
        print(f"\n== Scope: {rel_scope} ==")

        if not args.format_only:
            rules = block.get("rules")
            if isinstance(rules, dict):
                forbid_globs = rules.get("forbid_globs")
                if isinstance(forbid_globs, list) and all(isinstance(item, str) for item in forbid_globs):
                    for rel_file in rel_files:
                        if _matches_any_glob(rel_file, forbid_globs):
                            message = f"{rel_scope}: forbidden path matched ({rel_file})"
                            failures.append(message)
                            violations.append(
                                {
                                    "type": "forbidden-path",
                                    "scope": rel_scope,
                                    "path": rel_file,
                                    "message": message,
                                    "blocking": True,
                                }
                            )

                forbid_regex = rules.get("forbid_regex")
                if isinstance(forbid_regex, list):
                    for entry in forbid_regex:
                        if isinstance(entry, str):
                            pattern, message, path_globs = entry, "forbidden pattern matched", None
                        elif isinstance(entry, dict):
                            pattern = entry.get("pattern")
                            message = entry.get("message") or "forbidden pattern matched"
                            candidate_globs = entry.get("paths")
                            path_globs = (
                                candidate_globs
                                if isinstance(candidate_globs, list)
                                and all(isinstance(item, str) for item in candidate_globs)
                                else None
                            )
                        else:
                            continue
                        if not isinstance(pattern, str) or not pattern:
                            continue
                        try:
                            regex = re.compile(pattern)
                        except re.error as exc:
                            full_message = f"{rel_scope}: invalid forbid_regex pattern {pattern!r}: {exc}"
                            failures.append(full_message)
                            violations.append(
                                {
                                    "type": "invalid-rule",
                                    "scope": rel_scope,
                                    "path": rel_scope,
                                    "message": full_message,
                                    "blocking": True,
                                }
                            )
                            continue
                        for rel_file in rel_files:
                            if path_globs is not None and not _matches_any_glob(rel_file, path_globs):
                                continue
                            try:
                                text = (scope_root / rel_file).read_text(encoding="utf-8", errors="replace")
                            except OSError:
                                continue
                            if regex.search(text):
                                full_message = f"{rel_scope}: {message} ({rel_file})"
                                failures.append(full_message)
                                violations.append(
                                    {
                                        "type": "forbidden-pattern",
                                        "scope": rel_scope,
                                        "path": rel_file,
                                        "message": full_message,
                                        "blocking": True,
                                    }
                                )
            if any(item["scope"] == rel_scope and item["type"].startswith("forbidden") for item in violations):
                phase_results["rules"] = "fail"
        else:
            phase_results["rules"] = "skipped"

        if args.no_fix:
            phase_results["format"] = "skipped"
        else:
            format_commands = _select_commands(block, "format")
            if format_commands:
                print("- format (auto-fix)")
                statuses = []
                for result in _run_commands(commands=format_commands, cwd=scope_root, changed_rel_files=rel_files):
                    status = _record_command(command_records, scope=rel_scope, phase="format", result=result)
                    statuses.append(status)
                    if result.returncode != 0:
                        message = f"{rel_scope}: format failed: {result.command}"
                        failures.append(message)
                        violations.append(
                            {
                                "type": "command-failure",
                                "scope": rel_scope,
                                "path": None,
                                "message": message,
                                "blocking": True,
                            }
                        )
                        if result.stdout.strip():
                            print(result.stdout.rstrip())
                        if result.stderr.strip():
                            print(result.stderr.rstrip(), file=sys.stderr)
                        break
                phase_results["format"] = "fail" if "fail" in statuses else "pass"

        if not args.format_only:
            lint_commands = _select_commands(block, "lint")
            if lint_commands:
                print("- lint")
                statuses = []
                for result in _run_commands(commands=lint_commands, cwd=scope_root, changed_rel_files=rel_files):
                    status = _record_command(command_records, scope=rel_scope, phase="lint", result=result)
                    statuses.append(status)
                    if result.returncode != 0:
                        message = f"{rel_scope}: lint failed: {result.command}"
                        failures.append(message)
                        violations.append(
                            {
                                "type": "command-failure",
                                "scope": rel_scope,
                                "path": None,
                                "message": message,
                                "blocking": True,
                            }
                        )
                        if result.stdout.strip():
                            print(result.stdout.rstrip())
                        if result.stderr.strip():
                            print(result.stderr.rstrip(), file=sys.stderr)
                        break
                phase_results["lint"] = "fail" if "fail" in statuses else "pass"

            if args.skip_tests:
                phase_results["test"] = "skipped"
            else:
                test_section = block.get("test")
                optional = isinstance(test_section, dict) and test_section.get("optional") is True
                test_commands = _select_commands(block, "test")
                if test_commands:
                    print("- test")
                    statuses = []
                    for result in _run_commands(commands=test_commands, cwd=scope_root, changed_rel_files=rel_files):
                        status = _record_command(
                            command_records,
                            scope=rel_scope,
                            phase="test",
                            result=result,
                            optional=optional,
                        )
                        statuses.append(status)
                        if result.returncode != 0:
                            message = f"{rel_scope}: test failed: {result.command}"
                            if optional:
                                print(f"  (optional) test failed: {result.command}")
                            else:
                                failures.append(message)
                            violations.append(
                                {
                                    "type": "command-failure",
                                    "scope": rel_scope,
                                    "path": None,
                                    "message": message,
                                    "blocking": not optional,
                                }
                            )
                            if result.stdout.strip():
                                print(result.stdout.rstrip())
                            if result.stderr.strip():
                                print(result.stderr.rstrip(), file=sys.stderr)
                            break
                    phase_results["test"] = (
                        "optional-fail"
                        if "optional-fail" in statuses
                        else ("fail" if "fail" in statuses else "pass")
                    )
        else:
            phase_results["lint"] = "skipped"
            phase_results["test"] = "skipped"

        scope_results.append({"agents_file": rel_scope, "files": rel_files, "phases": phase_results})

    scope = {
        "mode": scope_mode,
        "base_ref": args.base_ref,
        "base_commit_sha": base_commit,
        "changed_files": changed_files,
        "applicable_agents": [path.relative_to(repo_root).as_posix() for path, _ in scoped_items],
    }
    prior_evidence = _prior_evidence(existing_evidence, repository, scope)
    binding_reasons = []
    if dirty:
        binding_reasons.append("worktree is dirty")
    if not changed_files:
        binding_reasons.append("verification scope is empty")
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repository": repository,
        "binding": {
            "status": "unbound" if binding_reasons else "bound",
            "dirty_worktree": dirty,
            "reasons": binding_reasons,
            "changed_files_digest": _scope_digest(changed_files),
            "stale": False,
            "stale_reasons": [],
        },
        "prior_evidence": prior_evidence,
        "scope": scope,
        "commands": command_records,
        "results": scope_results,
        "violations": violations,
        "overall_result": "fail" if failures else "pass",
    }

    if args.evidence_json:
        _write_json(args.evidence_json, evidence)
    if args.review_packet:
        _write_text(args.review_packet, _render_review_packet(evidence))

    if not files:
        print("No files to verify.")
        return 0
    if failures:
        print("\nFAIL:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nOK: guidelines verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
