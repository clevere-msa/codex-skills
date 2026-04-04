---
name: perl-guidelines
description: Router skill for Perl engineering standards across module workflow, testing, lint/format, security/taint, dependency policy, logging/observability, coverage, and CGI auth debugging. Use when a Perl task spans multiple concerns and you need to select the right specialized Perl skill(s).
---

# Perl Guidelines

Use this skill as the entry point for Perl tasks, then route to the smallest set of specialized skills.

## Routing Map
- Module implementation and refactor: `perl-module-workflow`
- Test authoring and `prove` execution: `perl-test-and-prove`
- Style/lint and formatting: `perl-lint-format`
- Coverage gap analysis: `perl-coverage-analysis`
- CGI/SSO/session auth incidents: `perl-cgi-auth-debug`
- Security and taint concerns: `perl-security-taint`
- Dependency decisions: `perl-dependency-policy`
- Logging and observability changes: `perl-logging-observability`

## Skill Matrix
For a concise decision table and common multi-skill combinations, use:
- references/045_perl_skill_matrix.md

## Usage Pattern
1. Identify the dominant Perl concern(s).
2. Invoke matching specialized skill(s).
3. Keep overlap minimal and avoid duplicate instructions.

## Legacy References
These remain available for baseline guidance:
- references/040_perl_project_conventions.md
- references/041_perl_testing_patterns.md
- references/042_perl_dependency_policy.md
- references/043_perl_security_and_taint.md
- references/044_perl_logging_and_observability.md
