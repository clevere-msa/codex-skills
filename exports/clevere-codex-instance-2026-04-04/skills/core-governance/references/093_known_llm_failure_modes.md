# Known LLM Failure Modes (Codex Skill)

## Purpose
Reduce predictable agent errors by enforcing explicit checks.

## Common Pitfalls (must guard)
- Assuming tools/frameworks exist (tests, linters, build systems) without verifying
- Assuming GNU/BSD behavior equivalence for core utilities
- Assuming POSIX sh when script is Bash-specific (or vice versa)
- Inventing file paths, targets, or proc options
- Over-refactoring due to “best practice” bias
- Claiming success without runnable evidence

## Mandatory Pause Conditions
Pause and verify when:
- You are about to add a dependency/tool
- You are about to change public interfaces or outputs
- You cannot find a referenced command in repo scripts/docs
- You cannot reproduce a reported failure

## Failure Conditions
- Any of the above pitfalls occur without being explicitly checked and documented
