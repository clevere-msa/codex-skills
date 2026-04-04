# C/C++ Build + Debug Tooling (Codex Skill)

## Build Discovery (Do first)
- Identify canonical build system:
  - Make / CMake / Autotools / Bazel / custom scripts
- Identify required env vars, include paths, library paths, and link flags.
- Locate CI build commands and replicate locally where possible.

## Default Build Discipline
- Do not “fix” build by weakening warnings or removing flags.
- Prefer local fixes: missing include, wrong prototype, signedness, format specifiers.
- Avoid global reformatting or sweeping refactors.

## Diagnostics
- Treat warnings as bugs when CI uses -Werror.
- Common correctness checks:
  - format string correctness (`printf`/`scanf`)
  - signed/unsigned comparisons
  - lifetime of pointers/references
  - missing `#include` / ODR violations (C++)

## Sanitizers (Use when practical)
- AddressSanitizer: `-fsanitize=address -fno-omit-frame-pointer`
- UBSan: `-fsanitize=undefined`
- LeakSanitizer (often part of ASan)
- Only enable if compatible with repo/toolchain; record commands used.

## Debugging Workflow
1) Reproduce with exact build/run command.
2) Minimize to targeted test or small repro program.
3) Use `gdb`/`lldb` backtrace and inspect locals.
4) Fix minimally; add regression test if possible.
5) Re-run relevant test suite.

## Artifact Reporting
- Always record:
  - build command(s)
  - compiler version (if relevant)
  - failing test names / error signatures
  - verification PASS/FAIL
