# Reality Check (Codex Skill)

## Purpose
Prevent repo-inaccurate changes by continuously validating assumptions against repo reality.

## Required Practices
- Before editing:
  - Confirm file paths, function names, flags, and behaviors by reading the source.
  - Identify the canonical build/test entrypoints from repo docs/CI.
- Before concluding:
  - Re-open touched files and ensure the final state matches intent.
  - Confirm no unintended collateral changes (formatting, imports, generated outputs).

## Assumption Handling
- Tag each non-trivial assumption as ASSUMPTION.
- Convert assumptions into FACT by verifying in code/config/logs.
- If verification is not possible, stop and request the missing input.

## Minimal Evidence
- Always cite paths + (approximate) line ranges or symbols (function/class) rather than paraphrasing.
- Prefer “I observed X in file Y” over inference.

## Failure Conditions
- Proceeding on unverified assumptions when verification was available
- Declaring success without referencing verification evidence
