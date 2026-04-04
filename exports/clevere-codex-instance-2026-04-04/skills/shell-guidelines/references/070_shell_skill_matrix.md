# Shell Skill Matrix

Use this matrix to choose the smallest shell skill set.

## Primary Routing
| Task type | Primary skill | Add these only if needed |
|---|---|---|
| Safe rerunnable script logic | `shell-safety-idempotency` | `shell-testing-ci` |
| Test/CI validation for script changes | `shell-testing-ci` | `shell-safety-idempotency` |
| CLI behavior, args, exit codes, hardening | `shell-security-cli-contracts` | `shell-safety-idempotency` |

## Conflict Resolution
1. If security or input trust boundary is involved, include `shell-security-cli-contracts`.
2. If script mutates state, include `shell-safety-idempotency`.
3. If acceptance requires evidence, include `shell-testing-ci`.

## Scope Rule
Choose one primary skill, then add secondary skills only for explicitly present concerns.
