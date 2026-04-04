# Blast Radius Assessment (Codex Skill)

## Purpose
Assess and control risk from changes, especially in shared or production-adjacent code.

## Required Assessment (brief)
- Affected surfaces:
  - callers (APIs/CLIs)
  - runtime components (services/jobs)
  - data stores (DB/files)
- Risk level: LOW / MEDIUM / HIGH
- Why: 1–3 bullets
- Mitigation:
  - tests added/run
  - rollout/guard strategy (flags, backward-compat, staged deploy)
  - monitoring/logging notes (if relevant)

## Defaults
- Treat interface changes as at least MEDIUM risk.
- Treat DB/transaction behavior changes as HIGH until proven safe.

## Failure Conditions
- No risk classification for non-trivial changes
- High-risk change without mitigation plan
