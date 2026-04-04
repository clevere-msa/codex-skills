# Generated Code Policy (Codex Skill)

## Purpose
Prevent corruption of generated artifacts and ensure reproducible generation.

## Identification
Treat as generated until proven otherwise:
- Pro*C outputs: `.c/.cpp` generated from `.pc`
- parser outputs, codegen, vendored bundles, build artifacts
- files marked with “DO NOT EDIT” headers

## Rules
- Do not hand-edit generated files unless repo policy explicitly requires it.
- Prefer to modify the source generator input:
  - `.pc` for Pro*C
  - templates/specs for codegen
- If generated files are checked in:
  - regenerate using the repo’s canonical command
  - record generator version/options and commands used

## Reporting
- Always state whether a touched file is source vs generated.
- If regeneration changed many lines, summarize and ensure verification is strong.

## Failure Conditions
- Editing generated output directly when source exists
- Regeneration performed with guessed options
