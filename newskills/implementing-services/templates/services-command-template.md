# Services Command Template

Per-phase output format for `/implementing-services`.

## Phase Output Structure

For each plan phase, present output in this format:

```markdown
## Phase N: [Phase Name]

### Changes Made (to repo files)

Files created or modified during this phase:
- Modified `path/to/docker-compose.yml` — added [service] service definition
- Created `path/to/.env.example` — template with [N] variables (placeholders only)
- Created `path/to/config/app.conf` — [service] configuration file
- Updated `traefik/dynamic/routes.yml` — added route for [service].domain.com

### Commands to Execute

**User runs these commands** — Claude generates, never executes:

```bash
# Step 1: Create .env from template
cp path/to/.env.example path/to/.env
# IMPORTANT: Edit .env and fill in real values before proceeding

# Step 2: Pull images
docker compose -f path/to/docker-compose.yml pull [service]

# Step 3: Deploy
docker compose -f path/to/docker-compose.yml up -d [service]

# Step 4: Verify deployment
docker compose -f path/to/docker-compose.yml ps [service]
docker logs --tail 50 [service]
```

### Rollback Commands (if needed)

**If something goes wrong**, run these to restore previous state:

```bash
# Stop the problematic service
docker compose -f path/to/docker-compose.yml stop [service]
docker compose -f path/to/docker-compose.yml rm -f [service]

# Restore previous config files
git checkout HEAD~1 -- path/to/docker-compose.yml
git checkout HEAD~1 -- traefik/dynamic/routes.yml

# If needed, restart with previous config
docker compose -f path/to/docker-compose.yml up -d
```

### Verification Checklist

- [ ] Service is running (`docker compose ps` shows "Up" or "running")
- [ ] Service responds on expected port (`curl -s http://localhost:PORT`)
- [ ] Reverse proxy route works (`curl -s https://service.domain.com`)
- [ ] Health check passes (`docker inspect --format='{{.State.Health.Status}}' service`)
- [ ] No port conflicts with other services
- [ ] Dependent services still working
- [ ] Backup job registered (if applicable)
```

## Formatting Rules

### Changes Made
- One bullet per file operation
- Include the action (Created, Modified, Updated, Moved, Deleted)
- Include the file path in backticks
- Include a brief description of what changed

### Commands to Execute
- Always in fenced bash code blocks
- Comment every step with what it does
- Include the `.env` creation step when .env.example was generated
- Include verification commands after deployment
- Use `-f` flag for non-default compose file locations
- Specify service name to avoid affecting other services

### Rollback Commands
- Always in fenced bash code blocks
- Include steps to stop the new service
- Include steps to restore previous config from git
- Include steps to redeploy with previous config
- Order: stop → restore → redeploy

### Verification Checklist
- Actionable checkbox items
- Include specific commands in parentheses
- Cover: running status, port response, proxy route, health check
- Include service-specific checks as needed
- Add backup registration check if the service has critical data

## Same-Machine Mode Adaptations

When `homelab_same_machine: true`, the output format changes slightly:

```markdown
### Verification Results (auto-checked)

Read-only verification commands were executed automatically:

```
$ docker compose ps [service]
NAME        STATUS    PORTS
service     Up 30s    0.0.0.0:8080->8080/tcp

$ docker logs --tail 10 [service]
[timestamp] Server started on port 8080
[timestamp] Connected to database
```

Remaining manual checks:
- [ ] Reverse proxy route works (https://service.domain.com)
- [ ] External connectivity verified
```

## Multi-Phase Summary

After all phases are complete, present a summary:

```markdown
## Implementation Summary

### All Phases Complete

| Phase | Status | Services Affected |
|-------|--------|-------------------|
| Phase 1: [name] | Verified | [services] |
| Phase 2: [name] | Verified | [services] |
| Phase 3: [name] | Verified | [services] |

### Files Changed
- [N] compose files modified
- [N] config files created
- [N] .env.example templates generated
- [N] proxy routes added/updated

### Commands Executed by User
All deployment commands were generated and executed by the user.
Rollback commands are documented in each phase above.

### Verification
All verification checklists confirmed by user.
```
