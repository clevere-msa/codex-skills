# MCP Failure Diagnostics (Codex Skill)

## Symptom → Cause Mapping

### "initialize response closed"
- Server exited early
- stdout contamination
- missing env
- Docker env not passed

### timeout after X seconds
- npx install delay
- slow network
- increase startup_timeout_sec

### MCP notification: Internal Server Error
- Server runtime exception
- Inspect STDERR logs
- Validate external system connectivity

## Debug Protocol
1. Run server manually
2. Capture stdout vs stderr separately
3. Fix runtime error before retrying Codex
4. Never guess; always reproduce

