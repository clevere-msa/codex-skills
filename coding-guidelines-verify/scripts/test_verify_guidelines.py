from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("verify_guidelines.py")


class VerifyGuidelinesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self._run(["git", "init", "-q", "-b", "main"])
        self._run(["git", "config", "user.email", "test@example.invalid"])
        self._run(["git", "config", "user.name", "Verifier Test"])

    def _run(
        self,
        command: list[str],
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=check,
        )

    def _write_guidelines(
        self,
        *,
        lint: list[str] | None = None,
        tests: list[str] | None = None,
        optional: bool = False,
    ) -> None:
        block = {
            "version": 1,
            "format": {"autofix": True, "commands": ["python3 -c 'print(\"format-ok\")'"]},
            "lint": {"commands": lint or ["python3 -c 'print(\"lint-ok\")'"]},
            "test": {
                "commands": tests or ["python3 -c 'print(\"test-ok\")'"],
                "optional": optional,
            },
            "rules": {"forbid_globs": [], "forbid_regex": []},
        }
        (self.repo / "AGENTS.md").write_text(
            "# Test rules\n\n```codex-guidelines\n"
            + json.dumps(block, indent=2)
            + "\n```\n",
            encoding="utf-8",
        )

    def _commit_fixture(self) -> None:
        (self.repo / "app.py").write_text("value = 1\n", encoding="utf-8")
        self._run(["git", "add", "."])
        self._run(["git", "commit", "-q", "-m", "test fixture"])

    def _verify(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self._run([sys.executable, str(SCRIPT), *args], check=False)

    def test_passing_dirty_worktree_emits_json_and_markdown(self) -> None:
        self._write_guidelines()
        self._commit_fixture()
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        evidence_path = self.root / "evidence.json"
        packet_path = self.root / "packet.md"

        completed = self._verify(
            "--evidence-json",
            str(evidence_path),
            "--review-packet",
            str(packet_path),
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("OK: guidelines verified.", completed.stdout)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["schema_version"], 1)
        self.assertEqual(evidence["overall_result"], "pass")
        self.assertEqual(evidence["binding"]["status"], "unbound")
        self.assertTrue(evidence["binding"]["dirty_worktree"])
        self.assertNotIn("stdout", json.dumps(evidence))
        packet = packet_path.read_text(encoding="utf-8")
        for heading in (
            "## Outcome",
            "## Acceptance evidence",
            "## Validation",
            "## Control path",
            "## Risks/rollback",
            "## Remaining blockers",
        ):
            self.assertIn(heading, packet)

    def test_failing_command_preserves_nonzero_exit(self) -> None:
        self._write_guidelines(lint=["python3 -c 'import sys; sys.exit(3)'"])
        self._commit_fixture()
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        evidence_path = self.root / "evidence.json"

        completed = self._verify("--evidence-json", str(evidence_path))

        self.assertEqual(completed.returncode, 1)
        self.assertIn("FAIL:", completed.stdout)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["overall_result"], "fail")
        self.assertTrue(any(item["status"] == "fail" for item in evidence["commands"]))

    def test_optional_test_failure_is_nonblocking(self) -> None:
        self._write_guidelines(
            tests=["python3 -c 'import sys; sys.exit(4)'"],
            optional=True,
        )
        self._commit_fixture()
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        evidence_path = self.root / "evidence.json"

        completed = self._verify("--evidence-json", str(evidence_path))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["overall_result"], "pass")
        optional_failures = [item for item in evidence["commands"] if item["status"] == "optional-fail"]
        self.assertEqual(len(optional_failures), 1)

    def test_unscoped_files_fail_unless_allowed(self) -> None:
        (self.repo / "app.py").write_text("value = 1\n", encoding="utf-8")
        self._run(["git", "add", "app.py"])
        self._run(["git", "commit", "-q", "-m", "test fixture"])
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")

        blocked = self._verify()
        allowed = self._verify("--allow-unscoped")

        self.assertEqual(blocked.returncode, 1)
        self.assertIn("Missing scoped AGENTS.md", blocked.stdout)
        self.assertEqual(allowed.returncode, 0)

    def test_clean_commit_all_files_evidence_is_bound(self) -> None:
        self._write_guidelines()
        self._commit_fixture()
        evidence_path = self.root / "evidence.json"

        completed = self._verify("--all", "--evidence-json", str(evidence_path))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["binding"]["status"], "bound")
        self.assertFalse(evidence["binding"]["dirty_worktree"])
        self.assertEqual(evidence["repository"]["commit_sha"], self._run(["git", "rev-parse", "HEAD"]).stdout.strip())

    def test_clean_committed_range_evidence_is_bound_to_changed_files(self) -> None:
        self._write_guidelines()
        self._commit_fixture()
        base_sha = self._run(["git", "rev-parse", "HEAD"]).stdout.strip()
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        self._run(["git", "add", "app.py"])
        self._run(["git", "commit", "-q", "-m", "change app"])
        evidence_path = self.root / "evidence.json"

        completed = self._verify(
            "--base-ref",
            base_sha,
            "--evidence-json",
            str(evidence_path),
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["binding"]["status"], "bound")
        self.assertEqual(evidence["scope"]["mode"], "commit-range")
        self.assertEqual(evidence["scope"]["base_commit_sha"], base_sha)
        self.assertEqual(evidence["scope"]["changed_files"], ["app.py"])
        self.assertTrue(evidence["commands"])

    def test_committed_range_includes_deleted_files(self) -> None:
        self._write_guidelines()
        (self.repo / "obsolete.py").write_text("obsolete = True\n", encoding="utf-8")
        self._commit_fixture()
        base_sha = self._run(["git", "rev-parse", "HEAD"]).stdout.strip()
        (self.repo / "obsolete.py").unlink()
        self._run(["git", "add", "-u"])
        self._run(["git", "commit", "-q", "-m", "remove obsolete file"])
        evidence_path = self.root / "evidence.json"

        completed = self._verify(
            "--base-ref",
            base_sha,
            "--evidence-json",
            str(evidence_path),
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["binding"]["status"], "bound")
        self.assertEqual(evidence["scope"]["changed_files"], ["obsolete.py"])

    def test_evidence_redacts_remote_and_command_secrets(self) -> None:
        self._write_guidelines(lint=["TOKEN=do-not-record python3 -c 'print(\"ok\")'"])
        self._commit_fixture()
        self._run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "https://user:remote-secret@example.invalid/org/repo?token=query-secret",
            ]
        )
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        evidence_path = self.root / "evidence.json"

        completed = self._verify("--evidence-json", str(evidence_path))

        self.assertEqual(completed.returncode, 0, completed.stderr)
        serialized = evidence_path.read_text(encoding="utf-8")
        self.assertNotIn("do-not-record", serialized)
        self.assertNotIn("remote-secret", serialized)
        self.assertNotIn("query-secret", serialized)
        self.assertIn("TOKEN=<redacted>", serialized)

    def test_existing_evidence_is_stale_when_file_set_changes(self) -> None:
        self._write_guidelines()
        self._commit_fixture()
        evidence_path = self.root / "evidence.json"
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        first = self._verify("--evidence-json", str(evidence_path))
        self.assertEqual(first.returncode, 0, first.stderr)
        (self.repo / "other.py").write_text("other = True\n", encoding="utf-8")

        second = self._verify("--evidence-json", str(evidence_path))

        self.assertEqual(second.returncode, 0, second.stderr)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertFalse(evidence["binding"]["stale"])
        self.assertEqual(evidence["prior_evidence"]["status"], "stale")
        self.assertIn("changed-file set no longer matches", evidence["prior_evidence"]["reasons"])

    def test_existing_evidence_is_stale_when_commit_changes(self) -> None:
        self._write_guidelines()
        self._commit_fixture()
        evidence_path = self.root / "evidence.json"
        first = self._verify("--all", "--evidence-json", str(evidence_path))
        self.assertEqual(first.returncode, 0, first.stderr)
        (self.repo / "app.py").write_text("value = 2\n", encoding="utf-8")
        self._run(["git", "add", "app.py"])
        self._run(["git", "commit", "-q", "-m", "change commit"])

        second = self._verify("--all", "--evidence-json", str(evidence_path))

        self.assertEqual(second.returncode, 0, second.stderr)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertFalse(evidence["binding"]["stale"])
        self.assertEqual(evidence["prior_evidence"]["status"], "stale")
        self.assertIn("commit SHA no longer matches", evidence["prior_evidence"]["reasons"])

    def test_no_changes_keeps_console_exit_behavior(self) -> None:
        self._write_guidelines()
        self._commit_fixture()

        completed = self._verify()

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout.strip(), "No files to verify.")

    def test_no_changes_evidence_is_unbound(self) -> None:
        self._write_guidelines()
        self._commit_fixture()
        evidence_path = self.root / "evidence.json"

        completed = self._verify("--evidence-json", str(evidence_path))

        self.assertEqual(completed.returncode, 0)
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        self.assertEqual(evidence["binding"]["status"], "unbound")
        self.assertIn("verification scope is empty", evidence["binding"]["reasons"])

    def test_invalid_base_ref_fails_closed(self) -> None:
        self._write_guidelines()
        self._commit_fixture()

        completed = self._verify("--base-ref", "missing/ref")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("cannot resolve merge base", completed.stderr)


if __name__ == "__main__":
    unittest.main()
