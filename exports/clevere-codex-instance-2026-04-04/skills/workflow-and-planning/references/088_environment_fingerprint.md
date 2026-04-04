# Environment Fingerprint (Codex Skill)

## Purpose
Preserve a compact, reproducible record of the environment used for verification.

## What to Record (compact)
- OS / distro (or container image)
- Key tool versions relevant to the change:
  - compilers (gcc/clang), make/cmake
  - interpreters (perl/python) if used
  - Oracle client/proc version if Pro*C is involved
- Key build flags or env toggles that materially affect behavior

## Constraints
- Do not record secrets or credential values.
- Record env var NAMES only; never values.

## Where to Store
- Prefer continuity ledger section “Environment & Verify”
- If no ledger is used, include in the final report under Verification

## Failure Conditions
- Verification cannot be reproduced due to missing environment details
