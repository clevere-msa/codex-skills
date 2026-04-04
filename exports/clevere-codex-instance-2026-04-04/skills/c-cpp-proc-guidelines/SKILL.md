---
name: c-cpp-proc-guidelines
description: Router skill for C/C++ and Pro*C standards across code conventions, build/debug workflow, testing patterns, and Pro*C-specific SQL/C integration rules. Use when a native or Pro*C task spans multiple concerns and you need the right specialized skill(s).
---

# C Cpp Pro C Guidelines

Use this skill as the entry point for C/C++/Pro*C tasks, then route to the smallest set of specialized skills.

## Routing Map
- C/C++ source and header conventions: `c-cpp-code-conventions`
- Build, link, and runtime debugging: `c-cpp-build-debug`
- Native testing strategy and regression checks: `c-cpp-testing-patterns`
- Pro*C embedded SQL and host variable rules: `oracle-proc-guidelines`

## Skill Matrix
For decision table and combinations, use:
- references/075_c_cpp_proc_skill_matrix.md

## Usage Pattern
1. Identify dominant native/Pro*C concern(s).
2. Invoke matching specialized skill(s).
3. Keep overlap minimal and avoid duplicate instructions.

## Legacy References
These remain available for baseline guidance:
- references/070_c_project_conventions.md
- references/071_cpp_project_conventions.md
- references/072_c_cpp_build_debug_tooling.md
- references/073_oracle_pro_c_conventions.md
- references/074_c_cpp_testing_patterns.md
