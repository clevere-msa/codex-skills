---
name: msa-log-reader
description: Read and analyze MSA application and server logs for mod_perl and batch issues. Use for requests like "check the CGI log", "find the 500", "tail the vhost error log", or "locate the log for a specific /cgi-bin/*.cgi page" across shell/titan, msa (aviation), opsver, and epic (airbp).
---

# Msa Log Reader

## Overview

Locate the correct log file for a given page or batch job, read only what is needed, and report the smallest useful error context.

## Web App Log Heuristics

- vhost error logs live under `/var/log/apache2/<vhost>/error.log` (path defined in the vhost config).
- App CGI logs live under `<app_root>/web/cgi-logs/<cgi_base>/log.YYYYMMDD` unless the app uses `cgi_logs` instead of `cgi-logs`.
- The framework logger strips directories and the `.cgi` extension, so `/cgi-bin/admin/user.cgi` logs under `.../cgi-logs/user/`, not `.../cgi-logs/admin/user/`.

## App Mapping (current host)

- shell/titan: `/project/shell/web` with `cgi-logs`
- opsver: `/project/opsver/web` with `cgi-logs`
- msa (aviation): `/project/aviation/web` with `cgi_logs`
- epic: `/project/airbp/web` with `cgi-logs` (per vhost config)

If a path is missing, confirm the vhost `DocumentRoot`/`ScriptAlias` to find the live app root.

## Batch Log Heuristics

- Check `/project/<app>/log/` (common for shell and msa) and `/project/<app>/log/daily/` if present.
- If no log directory exists, search within the app root for `log` or `logs` directories.

## Workflow

1. Identify the app root from the vhost config (`DocumentRoot` or `ScriptAlias`).
2. Identify the CGI base name from the URL (last path segment, drop `.cgi`).
3. Check both `cgi-logs` and `cgi_logs` under `<app_root>/web/`.
4. Read `log.YYYYMMDD` (today) and then any rotated files if needed.

## Quick Commands

- `rg -n "ServerName|DocumentRoot|ScriptAlias|ErrorLog" <vhost.conf>`
- `tail -n 200 <log>`
- `rg -n "error|exception|fatal|panic|500|timeout" <log>`
- `zgrep -n "<pattern>" <log>.gz`

## Guardrails

- Read-only commands only; do not edit or delete logs.
- Redact secrets and credentials in any pasted output.
