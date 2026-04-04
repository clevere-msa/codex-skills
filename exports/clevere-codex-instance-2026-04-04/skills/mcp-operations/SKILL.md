---
name: mcp-operations
description: MCP runtime rules, stdio hygiene, startup discipline, Docker usage, and server-specific operations. Use when operating MCP servers or tools.
---

# MCP Operations

Use this skill whenever MCP servers or MCP tools are involved.

## How to Use the References (Routing Rule)
When you need details beyond the high-level rules in this skill, consult the **single most relevant** reference file below using this decision order. Only consult additional references if the first one is insufficient.

### Reference Routing Table (choose one primary)
- Runtime contract / invariant rules → references/100_mcp_runtime_contract.md
- STDIO safety, echo risks, secret handling → references/101_mcp_stdio_hygiene.md
- Startup sequencing, readiness checks, timeouts → references/102_mcp_startup_discipline.md
- Docker/container-specific MCP operations → references/103_mcp_docker_usage.md
- GitHub MCP operations → references/104_mcp_github_operations.md
- Keycloak MCP operations → references/105_mcp_keycloak_operations.md
- OpenLDAP MCP operations → references/106_mcp_openldap_operations.md
- Context management and documentation conventions → references/107_mcp_context_and_docs.md
- Failure triage, diagnostics, log capture → references/109_mcp_failure_diagnostics.md
- Oracle SQLcl MCP allowlist constraints → references/110_oracle_sqlcl_mcp_allowlist.md
- fast-playwright-mcp usage, options, expectations → references/111_fast_playwright_mcp.md

### Application Rule
- Always start with the routing table selection above.
- If multiple domains apply (e.g., Playwright + secrets + startup), read them in this order:
  1) 101_mcp_stdio_hygiene.md (secrets/echo safety)
  2) 102_mcp_startup_discipline.md (startup/readiness)
  3) <server-specific reference> (e.g., 111_fast_playwright_mcp.md)

## References
- references/100_mcp_runtime_contract.md
- references/101_mcp_stdio_hygiene.md
- references/102_mcp_startup_discipline.md
- references/103_mcp_docker_usage.md
- references/104_mcp_github_operations.md
- references/105_mcp_keycloak_operations.md
- references/106_mcp_openldap_operations.md
- references/107_mcp_context_and_docs.md
- references/109_mcp_failure_diagnostics.md
- references/110_oracle_sqlcl_mcp_allowlist.md
- references/111_fast_playwright_mcp.md

