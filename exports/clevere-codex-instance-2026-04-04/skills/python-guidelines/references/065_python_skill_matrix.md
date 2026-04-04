# Python Skill Matrix

Use this matrix to choose the smallest Python skill set.

## Primary Routing
| Task type | Primary skill | Add these only if needed |
|---|---|---|
| Test additions, regressions, quality gates | `python-testing-quality-gates` | `python-security-basics` |
| New package/dependency decisions | `python-dependency-policy` | `python-testing-quality-gates` |
| Input/auth/secrets security review | `python-security-basics` | `python-testing-quality-gates` |

## Conflict Resolution
1. If external input or secrets are involved, include `python-security-basics`.
2. If package changes are proposed, include `python-dependency-policy`.
3. If merge readiness is requested, include `python-testing-quality-gates`.

## Scope Rule
Choose one primary skill, then add secondary skills only for concerns visible in request or evidence.
