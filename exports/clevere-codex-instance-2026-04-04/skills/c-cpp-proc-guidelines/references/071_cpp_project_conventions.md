# C++ Project Conventions (Codex Skill)

## Goals
- Minimal, test-backed changes; preserve semantics and performance envelope.
- Prefer modern C++ only to the extent the repo already uses it (C++11/14/17/20).

## Coding Rules
- Prefer RAII for resource ownership (files, sockets, locks, heap memory).
- Avoid raw `new`/`delete` unless repo policy requires; prefer `std::unique_ptr`, `std::shared_ptr` when ownership is shared (justify shared).
- Prefer references/pointers semantics clearly:
  - `T&` when non-null required
  - `T*` when optional/nullable
- Use `const` correctness; avoid needless copies (pass by `const&` where appropriate).
- Avoid exceptions if repo is exception-free; follow repo norm (exceptions vs error codes).
- Avoid implicit narrowing conversions; prefer explicit casts when necessary.
- Prefer `<chrono>`, `<string_view>`, and `<span>` only if project standard supports them.

## Interfaces & ABI
- Avoid changing exported class layouts, vtables, or inline ABI-sensitive changes unless explicitly required.
- Keep headers stable; limit includes (prefer forward declarations where safe).

## Performance Safety
- Avoid hidden allocations in hot paths.
- Be cautious with `std::regex`, iostream sync, and shared_ptr churn in performance-sensitive code.

## Verification
- Build with the repo’s canonical compiler and standard.
- Ensure warning-clean for the touched files, especially:
  - `-Wall -Wextra -Werror` (if used)
  - `-Wconversion`, `-Wshadow` (if enforced)
- Run unit tests and any relevant integration tests.

## Failure Conditions
- ABI break introduced without explicit approval
- Exceptions/RTTI behavior changed contrary to repo policy
- Untested behavioral change
