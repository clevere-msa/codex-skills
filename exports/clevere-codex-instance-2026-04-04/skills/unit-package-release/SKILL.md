---
name: unit-package-release
description: Build distributable release archives for systemd unit repositories, including .service/.timer files and installer assets. Use when preparing handoff packages, deployment bundles, or release artifacts, and when archive manifests and checksums are required.
---

# Unit Package Release

## Overview
Use this skill to produce a clean, reproducible archive for unit distribution and installation.

## Repository Defaults (msa_systemd)
- Packaging entrypoint: `make` (default target builds zip).
- Explicit packaging target: `make zip`.
- Default artifact path: `dist/msa-systemd-units.zip`.
- Installer entrypoint: `make install` (runs `./install-units.sh`).
- Installer safety flags: `--dry-run`, `--no-start`, `--skip-verify`, `--dest <dir>`.

## Workflow
1. Select package inputs (`.service`, `.timer`, installer script, and required docs).
2. Build a versioned archive under `dist/`.
3. Validate archive contents.
4. Generate checksums and a manifest.
5. Report artifact name, contents, and install command.

## Select Inputs
Keep relative paths so extraction preserves unit layout.

```bash
find . -type f \( -name '*.service' -o -name '*.timer' \) | sed 's|^\./||' | sort
```

Recommended extras:
- `install-units.sh`
- `README.md`

## Build Archive
For this repository, prefer the Makefile target to keep packaging behavior consistent.

```bash
make zip
```

or with a custom artifact name:

```bash
make ZIP_NAME=<artifact-name> zip
```

Manual `zip` is a fallback only.

```bash
mkdir -p dist
zip -q dist/<artifact-name>.zip <file1> <file2> ...
```

Use a versioned name when available, for example `msa-systemd-units-2026.02.18.zip`.

## Validate Archive
Confirm exact contents and file count.

```bash
unzip -l dist/<artifact-name>.zip
```

## Generate Integrity Files
Create checksum and manifest files beside the archive.

```bash
sha256sum dist/<artifact-name>.zip > dist/<artifact-name>.zip.sha256
unzip -l dist/<artifact-name>.zip | awk 'NR>3 {print $4}' | sed '/^$/d' > dist/<artifact-name>.manifest.txt
```

For deterministic manifests without trailer lines:

```bash
unzip -l dist/<artifact-name>.zip | awk 'NR>3 && $4 != "" && $4 != "Name" && $4 != "----" {print $4}' | sed '/^---------$/d' > dist/<artifact-name>.manifest.txt
```

## Install Validation
Include recipient-safe install examples in release notes:

```bash
./install-units.sh --dry-run
./install-units.sh --dry-run --no-start
sudo ./install-units.sh
```

## Report Format
Return:
1. Archive path.
2. Included file list summary.
3. Checksum file path.
4. Install command for recipients.
5. PR evidence snippet (impact + validation + rollback).

Use this PR evidence template:

```text
Artifact:
- dist/<artifact-name>.zip
- dist/<artifact-name>.zip.sha256
- dist/<artifact-name>.manifest.txt

Packaging command:
- make ZIP_NAME=<artifact-name> zip

Install path:
- make install

Validation:
- unzip -l dist/<artifact-name>.zip => <file count + key files>
- ./install-units.sh --dry-run      => <summary>

Rollback:
- restore prior unit bundle
- rerun installer
- systemctl daemon-reload
```

## Guardrails
- Exclude secrets and environment-specific credential files.
- Exclude local build debris unless explicitly requested.
- Do not overwrite existing artifacts silently when versioning is expected.
- Keep packaging deterministic by sorting input file lists.
