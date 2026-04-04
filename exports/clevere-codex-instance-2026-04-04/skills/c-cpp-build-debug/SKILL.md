---
name: c-cpp-build-debug
description: Build and debug workflow for C/C++ native code changes. Use when compile/link behavior changes, build flags are modified, or native runtime failures require structured debugging.
---

# C Cpp Build Debug

Use this skill for compile/link troubleshooting and reproducible native debugging.
Routing note: for multi-concern routing, use `c-cpp-proc-guidelines` and `c-cpp-proc-guidelines/references/075_c_cpp_proc_skill_matrix.md`.

## Workflow
1. Reproduce the build/debug failure with exact command.
2. Isolate compile, link, or runtime stage.
3. Apply minimal fix and rebuild.
4. Validate with targeted runtime checks.
5. Summarize root cause and verification evidence.

## Guardrails
- Do not change optimization/debug flags broadly without reason.
- Do not hide warnings that indicate real defects.
- Keep environment assumptions explicit.
