# Skill: fast-playwright-mcp On-Demand Browser Provisioning and Use (Ports 8231–8299)

## Purpose
Enable the current Codex agent (Supervisor) to provision and manage one or more isolated browser instances on demand using fast-playwright-mcp, without collisions and without running idle instances.

This skill covers:
- leasing a port (8231–8299)
- starting/stopping/releasing fast-playwright-mcp instances
- maintaining an agent-local browser registry
- safe authentication practices (avoid secrets in echoed channels)

## Capability Note (Mandatory)
This session cannot dynamically attach new MCP servers after startup unless explicitly supported by the runtime.
If Playwright MCP was not configured at session start, browser automation requires either:
- starting the session with fast-playwright-mcp attached, or
- spawning a worker Codex process that starts with the needed MCP attached.

## Preconditions
- The helper script `pw-mcp-lease` exists in PATH and is executable.
- Node/npx is installed and can run: `npx -y @tontoko/fast-playwright-mcp@latest --help`
- The agent session has a per-agent directory and ledger:
  - CODEX_AGENT_DIR
  - CODEX_LEDGER
- Preferred: `jq` installed (optional; skill includes non-jq fallback).

## Definitions
- Browser Instance: one fast-playwright-mcp server bound to one port; provides an isolated browser profile.
- Port Range: 8231–8299 inclusive.
- Registry: JSON file tracking running browser instances for this agent.
  - REGISTRY_PATH = $CODEX_AGENT_DIR/browser_registry.json

## Hard Rules (Non-Negotiable)
1) Start with 0 instances. Only provision when required.
2) Never share a port between agents; always lease via pw-mcp-lease.
3) Prefer storage-state or test auth bypass over password entry.
4) Password entry is allowed only under the Dev-Only Credential Entry Exception (see below).
5) Always release leased ports when no longer needed or at session end.

## When to Provision a New Browser Instance
Provision a new instance when any is true:
- Separate identity/session is required (different user, different cookies).
- Parallel browser workflows are needed concurrently.
- Isolation is required to avoid state contamination (cookies/localStorage/cache).
- A prior browser instance is in an unknown state.

If the task can be accomplished with additional tabs under the same identity/session, prefer using the existing instance (tabs) instead of provisioning another server.

## Registry Protocol
Each agent maintains a local registry:
- File: $CODEX_AGENT_DIR/browser_registry.json
- Content: array of objects with:
  - id: short name (e.g., "b1", "b2")
  - port: integer
  - url: "http://127.0.0.1:<port>/mcp"
  - pid: integer
  - purpose: short text
  - created_utc: ISO timestamp
  - status: "running" | "stopped" | "released"

The registry is used so the agent can consistently refer to browsers by id (b1/b2/b3) rather than by port.

## Provisioning Procedure (Create Browser bN)
1) Allocate a port (does not start MCP):
   PORT="$(pw-mcp-lease alloc)"

2) Start MCP:
   read -r PORT URL PID < <(pw-mcp-lease start "$PORT")

3) Assign a stable browser id:
   - Use "b1" for the first instance, then "b2", etc.
   - Maintain mapping in browser_registry.json.

4) Append a short ledger note:
   - Add entry under "Recent Actions" with browser id, port, purpose.

## Registry Update Commands (Recommended)
Initialize registry if missing:
  if [ ! -f "$CODEX_AGENT_DIR/browser_registry.json" ]; then echo "[]" > "$CODEX_AGENT_DIR/browser_registry.json"; fi

Append entry (jq preferred):
  jq --arg id "b1" --argjson port "$PORT" --arg url "$URL" --argjson pid "$PID" \
     --arg purpose "login as test-user-a" --arg created "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
     '. + [{"id":$id,"port":$port,"url":$url,"pid":$pid,"purpose":$purpose,"created_utc":$created,"status":"running"}]' \
     "$CODEX_AGENT_DIR/browser_registry.json" > "$CODEX_AGENT_DIR/browser_registry.json.tmp" \
  && mv "$CODEX_AGENT_DIR/browser_registry.json.tmp" "$CODEX_AGENT_DIR/browser_registry.json"

Non-jq fallback (append-only JSONL next to registry):
  echo "{\"id\":\"b1\",\"port\":$PORT,\"url\":\"$URL\",\"pid\":$PID,\"purpose\":\"...\",\"created_utc\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"status\":\"running\"}" \
    >> "$CODEX_AGENT_DIR/browser_registry.jsonl"

## Using a Browser Instance
Because Codex may not be able to attach/detach MCP servers dynamically mid-session without restart, treat each browser instance as an external resource:
- Use fast-playwright-mcp for browser automation steps.
- Prefer using a dedicated worker subagent for complex browser sequences:
  - The Supervisor spawns a subagent tasked with browser actions, referencing the specific browser id (b1/b2) and URL/port from the registry.

The subagent must:
- read the registry to determine the target URL/port
- perform browser automation
- write results to output.md
- never print secrets

## Authentication Policy (Secrets)
Preferred in order:
1) storageState.json (pre-authenticated state) loaded by the browser context, if supported by your fast-playwright-mcp invocation pattern.
2) test environment auth bypass (signed test token / internal endpoint / header-based bypass).
3) environment variable secret injection only if you have verified:
   - tool responses do not echo executed code/args
   - Codex does not display tool arguments
   - no xtrace, no verbose logs, no trace/session saving that captures secrets

### Playwright-Auth Tool Integration (Local)
Use the local `playwright-auth` helper to keep site configs, user profiles, and secrets separate and to avoid typing credentials into MCP flows.

Recommended pattern:
- Site configs live under `/home/clevere/playwright-auth/sites/<site>.json`.
- User profiles live under `/home/clevere/playwright-auth/profiles/<user>.json`.
- Passwords live in `pass` (preferred). Materialize a short-lived password file only when needed.
- Site config should include `profilesDir` and `storageState` path (storage-state flow) or `profilesDir` only (MCP flow).
- Profile JSON contains `username` and `passwordFile` (path to the secret file).

Pass-backed password file example (dev only; do not echo secrets):
  umask 077
  pass show dev/oidc/employees/alice | head -n1 > /home/clevere/playwright-auth/secrets/alice.txt
  /home/clevere/playwright-auth/scripts/run-auth.sh -c msa -u alice
  shred -u /home/clevere/playwright-auth/secrets/alice.txt

Run with short site name and explicit username:
  /home/clevere/playwright-auth/scripts/run-auth.sh -c msa -u alice

Resolution rules:
- If `-c` is not a path and has no extension, it resolves to `sites/<name>.json`.
- `-u <user>` selects `<profilesDir>/<user>.json` and sets `AUTH_USERNAME` for setup.
- The tool writes the authenticated `storageState` defined in the site config.

#### MCP Login Flow (fast-playwright-mcp)
Use the MCP-based login flow to generate a persistent browser profile without installing local Playwright:

Run the MCP login helper:
  /home/clevere/playwright-auth/scripts/run-auth-mcp.sh -c msa -u alice

This will:
- start a fast-playwright-mcp instance
- drive the login via MCP calls
- write the session profile under:
  `/home/clevere/playwright-auth/.auth/mcp/<site>/<user>`

Reuse that session for protected testing:
  npx -y @tontoko/fast-playwright-mcp@latest --user-data-dir /home/clevere/playwright-auth/.auth/mcp/msa/alice

### Dev-Only Credential Entry Exception
Password entry is permitted only when all conditions are true:
- The user explicitly confirms the target is a development/test server (e.g., hostname `ip-10-1-1-185`).
- The fast-playwright-mcp server is configured to avoid echoing actions/arguments.
- Tracing/recording is disabled (no traces, videos, or screenshots during login).
- Credentials are entered only via browser automation (not pasted into chat/task packets).
- Credentials are not stored after login (no storageState export; close context after use if possible).

Never:
- paste passwords into chat or task packets
- use password entry outside the dev-only exception
- use password entry if the tool path echoes executed actions or arguments

## Deprovisioning Procedure (Stop/Release)
Stop a browser (keep lease) when you intend to reuse it soon:
  pw-mcp-lease stop "$PORT"
  Update registry status to "stopped"

Release a browser (recommended when done):
  pw-mcp-lease release "$PORT"
  Update registry status to "released"

At session end, release all running instances found in registry.

## Failure Handling
If start fails:
- Try the next port: release the lease (if any) and allocate again.
- Inspect logs:
  - $XDG_RUNTIME_DIR/pw-mcp-lease/logs/mcp-<port>.log (or /tmp equivalent)
Common causes:
- npx cold start (slow) → retry
- Playwright browser dependencies missing → install system deps
- port already in use → allocator should skip; investigate conflicting process

## Deliverables (for any browser automation subtask)
- A short, deterministic summary of:
  - browser id(s) used (b1/b2)
  - URLs visited
  - assertions performed
  - artifacts produced (screenshots, traces) and where stored
- No secrets in output

## Prohibited Behaviors
- Starting MCP servers preemptively “just in case”
- Reusing a browser profile for different identities unintentionally
- Leaving leases active after task completion
- Using password entry outside the dev-only exception or through echoed channels
