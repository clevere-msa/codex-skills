---
name: perl-cgi-auth-debug
description: "Debug Perl CGI authentication, SSO/OIDC, session, and redirect failures with evidence-driven root cause analysis. Use when login flows fail, users loop on redirects, CGI endpoints return 4xx/5xx, or auth-related environment/config mismatches are suspected."
---

# Perl CGI Auth Debug

## Overview
Use this skill for fast triage and root-cause isolation of authentication issues in Perl CGI applications.
Routing note: for multi-concern tasks, use `perl-guidelines` and `perl-guidelines/references/045_perl_skill_matrix.md`.

## Workflow
1. Capture symptom and affected endpoint(s).
2. Reproduce with the smallest authorized request flow.
3. Inspect CGI/server logs and Perl errors.
4. Trace auth/session state transitions and environment dependencies.
5. Propose fix plus verification commands.

## Initial Evidence Collection
Gather:
- exact URL and environment
- HTTP status and redirect chain
- timestamp window and affected user type
- recent code/config changes

## Useful Commands
Headers and redirects:
```bash
curl -k -I <url>
curl -k -s -L -D - <url> -o /dev/null
```

Perl compile checks:
```bash
perl -c path/to/cgi-or-module.pm
```

Log triage (example pattern):
```bash
rg -n "500|failed|Can't locate|OIDC|session|auth" /var/log/apache2/*error.log
```

## Common Root-Cause Buckets
- missing Perl module or wrong library path
- CGI environment mismatch (realm/client/metadata URL/env vars)
- cookie/session domain or path mismatch
- redirect URI mismatch or state/nonce validation failure
- stale unit/process state after deployment (reload/restart gap)

## Report Format
Return:
1. Reproduction path.
2. Evidence by source (HTTP, logs, code, config).
3. Most likely root cause and confidence.
4. Fix steps.
5. Post-fix verification commands.

## Guardrails
- Only test authorized targets and credentials.
- Do not expose secrets in logs, commands, or reports.
- Keep diagnostic changes reversible and minimal.
