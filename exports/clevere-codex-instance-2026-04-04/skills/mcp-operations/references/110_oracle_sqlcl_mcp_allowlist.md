# Oracle SQLcl MCP Allowlist + Read-Only Policy

## Allowed targets (TNS aliases only)
- msa_dev (SERVICE_NAME=MSADEV)
- msa_se_dev (SERVICE_NAME=MSADEVB)

## Connection rules
- Use SQLcl via MCP: sql -mcp
- Resolve targets via TNS_ADMIN/tnsnames.ora only.
- No EZCONNECT, no ad-hoc host/service strings.

## Credentials
- Use a dedicated read-only DB user (e.g., mcp_ro).
- Prefer interactive password entry, wallet, or approved secret manager.
- Never print or echo credentials.

## Read-only enforcement
- DB user grants: CREATE SESSION + explicit SELECT on all objects.
- Prohibit any DDL or ANY privileges.

## Safety
- If a requested operation implies writes, stop and request explicit approval and a separate, higher-privilege account.

