---
name: perl-dependency-policy
description: Dependency decision policy for Perl projects, including when to avoid new CPAN modules and how to introduce them safely. Use when adding, replacing, or evaluating Perl dependencies, build tooling, or runtime module requirements.
---

# Perl Dependency Policy

Use this skill for dependency-related decisions in Perl codebases.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Policy
- Avoid new dependencies unless they materially reduce complexity or risk.
- Prefer maintained, widely adopted modules.
- Align with repository dependency management conventions.

## Evaluation Workflow
1. Confirm the requirement cannot be met with existing dependencies.
2. Evaluate candidate module maturity and maintenance status.
3. Check licensing and compatibility constraints.
4. Document rationale and alternatives considered.
5. Update dependency and test instructions consistently.

## Output Format
Return:
1. Decision (`no new dep`, `add dep`, `replace dep`).
2. Rationale.
3. Operational impact (build, runtime, packaging).
4. Required repo updates (dependency file, docs, tests).

## Guardrails
- Do not add convenience dependencies without clear benefit.
- Do not mix dependency policy changes with unrelated refactors.
- Keep rollback straightforward when introducing new modules.
