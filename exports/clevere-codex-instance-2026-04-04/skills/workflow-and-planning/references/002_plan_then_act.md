# Plan-Then-Act Workflow

## Before editing
- Convert the task into explicit acceptance criteria (checkboxes).
- Produce a short numbered plan.
- List exact files expected to change.
- List exact commands to run for verification.

## While implementing
- Touch the minimum number of files.
- Prefer local changes; avoid cross-cutting changes.
- Keep commits/diffs reviewable (small, coherent steps).

## Stop conditions
Stop and ask a targeted question if:
- Acceptance criteria are ambiguous and cannot be inferred safely
- Required environment variables/paths are unknown
- Multiple plausible behaviors exist and choice affects users
