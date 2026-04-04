---
name: cover-db-parser
description: Parse Devel::Cover cover_db databases to extract statement/branch/condition/sub coverage, identify uncovered lines/branches, and summarize coverage gaps. Use when analyzing Perl coverage runs, inspecting cover_db output, or scripting coverage reports beyond the built-in cover CLI.
---

# Cover DB Parser

## Overview

Use this skill to read Devel::Cover coverage databases (`cover_db/`), extract per-file metrics, and map uncovered statements/branches back to source lines. Prefer the `cover` CLI for quick summaries and use DB parsing only when you need per-line/branch details or custom reports.

## Quick Workflow

1. Confirm the coverage DB path (default `./cover_db`).
2. Start with a quick summary:
   - `cover -report text`
   - `cover -report html_basic`
3. For targeted modules, narrow the report:
   - `cover -report text -select MSA/Shared/LdapAuth.pm`
4. For custom analysis, parse the DB:
   - Use `cover -dump_db` for a readable structure dump.
   - Or use `Devel::Cover::DB` from Perl for programmatic extraction.

## Parsing Guidance

Read the reference doc before writing scripts or regex parsers:
- `references/cover_db_parsing.md`

That file explains the `cover -dump_db` structure and shows safe patterns for extracting uncovered statements and branch points without relying on fragile HTML parsing.
