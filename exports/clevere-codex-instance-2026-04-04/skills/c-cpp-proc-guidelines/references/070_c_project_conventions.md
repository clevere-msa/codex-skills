# C Project Conventions (Codex Skill)

## Goals
- Correctness-first, minimal diffs, build-clean with repo flags, warning-clean where feasible.
- Preserve ABI/API unless explicitly requested.

## Coding Rules
- Prefer C99/C11 style consistent with repo.
- Include headers explicitly; avoid relying on transitive includes.
- Keep functions small; avoid hidden side effects.
- Use `static` for internal linkage; do not export symbols unintentionally.
- Prefer `size_t` for sizes/indices; avoid signed/unsigned mismatches.
- Check return values for syscalls/library calls; propagate errors with context.
- For pointer ownership:
  - Document ownership at boundaries.
  - Pair allocations/frees; avoid double-free and use-after-free.
- For buffers/strings:
  - Prefer bounded APIs (`snprintf`, `strnlen`, `memcpy` with validated lengths).
  - Avoid `strcpy`, `sprintf`, unchecked `strcat`.

## Headers & Interfaces
- Header contains only declarations and required types; keep includes minimal.
- Use include guards or `#pragma once` consistent with repo.
- If adding a public function:
  - Add prototype + doc comment in header.
  - Add unit/integration test where possible.

## Portability & Toolchain
- Follow repo’s standard flags; do not weaken warnings.
- Avoid non-standard extensions unless already used.
- If changing struct layouts or exported symbols, note ABI risk explicitly.

## Verification
- Prefer repo’s canonical build/test targets.
- If available, run:
  - `make clean all` (or equivalent)
  - targeted unit tests
  - sanitizers (ASan/UBSan) for touched area when practical

## Failure Conditions
- Build breaks or new warnings treated as errors in CI
- Unverified behavior changes
- Memory/resource leaks introduced without mitigation
