# Legacy Code Respect (Codex Skill)

## Purpose
Avoid destabilizing mature/legacy systems by favoring consistency over modernization.

## Default Posture
- Preserve patterns that are common in the repo, even if not modern.
- Avoid sweeping refactors, renames, or “cleanup” changes.
- Prefer the smallest change that fixes correctness.

## Modernization Rules
Only modernize when it:
- is required for correctness/security
- is required to pass repo gates
- reduces complexity in the directly changed area and is low-risk

## Documentation
- When legacy patterns appear risky, record:
  - observed pattern (FACT)
  - risk (INFERENCE)
  - recommended follow-up (TODO)
Do NOT implement follow-up unless asked.

## Failure Conditions
- Introducing new paradigms/frameworks in a legacy module without explicit request
- Large diffs justified as “cleanup”
