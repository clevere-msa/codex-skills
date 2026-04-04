---
name: systemd-unit-verify
description: Validate systemd unit changes for .service, .timer, and templated @ units before install or release. Use when creating, editing, reviewing, or debugging unit files, and when PR evidence needs systemd-analyze verify, status checks, journal checks, and timer verification.
---

# Systemd Unit Verify

## Overview
Use this skill to run repeatable verification for changed unit files and produce concise pass/fail evidence.

## Repository Defaults (msa_systemd)
- Unit discovery pattern: top-level service folders with unit files at depth 2.
- Template pattern in use: `msa-avi-process-run@.service` with instance timers like `msa-avi-process-run@Billing1.timer`.
- Preferred install path: `make install` (runs `./install-units.sh`).
- Safe pre-install command: `./install-units.sh --dry-run`.

## Workflow
1. Identify changed unit files.
2. Run `systemd-analyze verify` on every changed `.service` and `.timer` file.
3. Perform runtime checks in the target environment when requested.
4. Summarize results as file-level pass/fail plus actionable errors.

## Identify Target Files
Use changed files first. Fall back to all unit files only when needed.

```bash
git diff --name-only -- '*.service' '*.timer'
```

```bash
find . -type f \( -name '*.service' -o -name '*.timer' \) | sort
```

For this repository layout, a stricter selector is also valid:

```bash
find . -mindepth 2 -maxdepth 2 -type f \( -name '*.service' -o -name '*.timer' \) | sort
```

## Static Verification
Run verification in batches so failures are easy to map to files.

```bash
systemd-analyze verify <unit1.service> <unit1.timer> <unit2.service>
```

If verify fails, capture exact error lines and map each to the owning file.

To match local install behavior, verify each file individually when producing audit evidence:

```bash
for f in $(find . -mindepth 2 -maxdepth 2 -type f \( -name '*.service' -o -name '*.timer' \) | sort); do
  systemd-analyze verify "$f"
done
```

## Runtime Verification
Run runtime checks only in the intended host environment.

```bash
systemctl status <name>.service <name>.timer
journalctl -u <name>.service -n 100 --no-pager
systemctl list-timers | grep <name>
```

When checking a templated unit, include the full instance name.

```bash
systemctl status 'msa-avi-process-run@Billing1.timer'
```

When validating installer outcomes, check these explicit examples:

```bash
systemctl status msa-gozer.service
systemctl status msa-avi-rptrun.timer
systemctl status 'msa-avi-process-run@Billing1.timer'
```

## Report Format
Return results in this order:
1. Files verified.
2. `systemd-analyze verify` result per file (`pass` or `fail`).
3. Runtime findings (`status`, `journalctl`, `list-timers`) when executed.
4. Required follow-up actions.

Use this PR evidence template:

```text
Units changed:
- <path/to/unit>

Schedule/runtime impact:
- OnCalendar: <old> -> <new> (or "unchanged")
- ExecStart: <old> -> <new> (or "unchanged")
- Type: <old> -> <new> (or "unchanged")

Validation commands:
- systemd-analyze verify <units...>  => <pass/fail>
- systemctl status <units...>        => <summary>
- journalctl -u <service> -n 100     => <summary>
- systemctl list-timers | grep <unit> => <summary>

Rollback:
- restore prior unit files to /etc/systemd/system
- systemctl daemon-reload
- re-enable prior timer/service state
```

## Guardrails
- Do not enable, start, or restart units unless explicitly requested.
- Do not edit unrelated units while fixing one failure.
- Keep credential placeholders unchanged; do not introduce secrets into unit files.
- Prefer concrete commands and outputs over generic recommendations.
