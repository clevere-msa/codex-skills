# Perl Skill Matrix

Use this matrix to select the smallest set of Perl skills for a task.

## Primary Routing
| Task type | Primary skill | Add these only if needed |
|---|---|---|
| Implement/refactor `.pm` logic | `perl-module-workflow` | `perl-test-and-prove`, `perl-lint-format` |
| Add/fix tests, run `prove` | `perl-test-and-prove` | `perl-coverage-analysis` |
| Style/lint cleanup | `perl-lint-format` | `perl-module-workflow` (if behavior changes) |
| Coverage gap reduction | `perl-coverage-analysis` | `perl-test-and-prove`, `cover-db-parser` |
| CGI login/SSO/session failures | `perl-cgi-auth-debug` | `perl-security-taint`, `perl-logging-observability` |
| Input validation, taint, command safety | `perl-security-taint` | `perl-cgi-auth-debug` |
| New CPAN dependency decision | `perl-dependency-policy` | `perl-module-workflow`, `perl-test-and-prove` |
| Logging/error context changes | `perl-logging-observability` | `perl-security-taint` |

## Conflict Resolution
1. If security is involved, include `perl-security-taint`.
2. If authentication/session is involved, include `perl-cgi-auth-debug`.
3. If adding tests is part of the fix, include `perl-test-and-prove`.
4. If only style is requested, keep scope to `perl-lint-format`.
5. If dependency changes are proposed, include `perl-dependency-policy`.

## Common Multi-Skill Combos
- Feature + tests: `perl-module-workflow` + `perl-test-and-prove`
- Bug fix + diagnostics: `perl-module-workflow` + `perl-logging-observability`
- Auth incident: `perl-cgi-auth-debug` + `perl-security-taint` + `perl-logging-observability`
- Coverage push: `perl-coverage-analysis` + `perl-test-and-prove`

## Scope Rule
Prefer one primary skill and add secondary skills only for concerns that are explicitly present in the request or evidence.
