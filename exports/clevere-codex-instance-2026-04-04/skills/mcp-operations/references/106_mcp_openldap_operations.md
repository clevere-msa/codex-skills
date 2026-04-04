# MCP OpenLDAP Operations (Codex Skill)

## Server
- RedHatLDAP-MCP

## Execution Model
- Python venv execution
- stdio-cleaner wrapper REQUIRED if stdout contamination exists

## Configuration
- REDHAT_LDAP_CONFIG (JSON)
- FASTMCP_LOG_LEVEL=ERROR

## Security Rules
- Read-only bind by default
- LDAPS preferred
- CA trust must be configured at OS level

## Common Failure Modes
- TLS CA not trusted
- Bad base DN / search base
- Schema mismatch (inetOrgPerson expectations)

## Verification
- ldapsearch works from host
- MCP server remains running awaiting handshake

