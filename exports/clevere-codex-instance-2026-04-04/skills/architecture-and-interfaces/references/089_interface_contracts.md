# Interface Contracts (Codex Skill)

## Purpose
Prevent silent breakage of external callers by preserving contracts unless explicitly changed.

## Contracts to Protect
- CLI:
  - flags, positional args, stdout/stderr format, exit codes
- Public APIs:
  - function signatures, struct/class layout, symbol visibility (C/C++)
- File formats:
  - CSV/JSON/YAML/layout, headers, delimiters, encoding
- Protocol/DB interactions:
  - SQL semantics, transaction behavior, cursor handling

## Required Checklist (pre-merge)
- Identify which contract(s) the change touches.
- If contract change is intended:
  - update docs/help text
  - add tests for old/new behavior or add migration notes
- If contract change is NOT intended:
  - add regression coverage or explicit verification step to confirm stability

## Failure Conditions
- Contract change introduced without documentation and verification
- Exit codes or stdout format changed unintentionally (scripts/CLIs)
