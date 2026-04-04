# Repo Intake Protocol

## Read order (binding if present)
1) AGENTS.md
2) CONTRIBUTING.md
3) README.md
4) docs/ (developer workflow pages, architecture notes)

## Identify
- Project entrypoints (bin/, scripts/, service units, main modules)
- Language split: Perl vs Python directories
- Test runners + canonical commands:
  - Perl: `prove`, `make test`, `dzil test`, etc.
  - Python: `pytest`, `tox`, `nox`, `python -m unittest`, etc.
- Lint/format tools used in CI and their scope rules
- Configuration and env expectations (.env.example, config templates)

## Output (brief)
- 5–10 bullet summary of repo structure and the safest workflow to make changes.
