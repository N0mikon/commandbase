# Services Plan Template

Template for service implementation plans written to `.docs/plans/`.

## File Naming

Format: `MM-DD-YYYY-description.md` in `.docs/plans/`

Examples:
- `02-08-2026-media-stack-deployment.md`
- `02-08-2026-traefik-migration.md`
- `02-08-2026-backup-system-setup.md`

## Frontmatter

Handled by docs-writer agent. Provide these fields:
```yaml
doc_type: "plan"
topic: "<infrastructure task name>"
tags: [services, implementation, <relevant aspect tags>]
references: [<key repo files this plan will modify>]
```

## Body Sections

```markdown
# <Plan Title>

## Overview

<What changes and why, in 2-3 sentences>

## Current State Analysis

### What Exists:
- **Services**: [list of relevant services with compose file locations]
- **Networking**: [current network topology]
- **Storage**: [current volume layout]
- **Proxy**: [current reverse proxy setup]

### What's Missing:
- [Gap 1]
- [Gap 2]

### Key Discoveries:
- [Discovery from repo exploration with file reference]

## Desired End State

<What the infrastructure should look like after implementation>

## What We're NOT Doing

- NOT [out-of-scope item 1]
- NOT [out-of-scope item 2]

## Implementation Approach

<High-level strategy for the changes. Reference design/structure docs if applicable.>

---

## Phase N: [Phase Name]

### Overview
<What this phase accomplishes, in 1-2 sentences>

### Config Changes
Files to create, modify, or move:
- Create `path/to/new-file.yml` — [purpose]
- Modify `path/to/existing.yml` — [what changes]
- Create `path/to/.env.example` — [template with placeholder values]

### Commands to Execute
**User runs these commands** (Claude generates, never executes):
```bash
# Step 1: [Description]
docker compose -f path/to/docker-compose.yml pull service-name

# Step 2: [Description]
docker compose -f path/to/docker-compose.yml up -d service-name

# Step 3: Verify
docker compose -f path/to/docker-compose.yml ps service-name
docker logs --tail 50 service-name
```

### Rollback Commands
**If something goes wrong**, run these to restore previous state:
```bash
# Stop the new service
docker compose -f path/to/docker-compose.yml stop service-name

# Restore previous config from git
git checkout HEAD~1 -- path/to/docker-compose.yml

# Restart with previous config
docker compose -f path/to/docker-compose.yml up -d
```

### Verification Checklist
- [ ] Service is running (`docker compose ps` shows "Up")
- [ ] Service responds on expected port
- [ ] Reverse proxy route works (if applicable)
- [ ] Health check passes (if configured)
- [ ] Other dependent services still work
- [ ] Backup job registered (if applicable)

### Success Criteria:
- [ ] [Specific, verifiable criterion with file reference]
- [ ] [Specific, verifiable criterion]
- [ ] All services reachable after this phase

---

[Repeat Phase structure for each phase]

---

## Verification Strategy

### Per-Phase Verification:
- Config file exists and is syntactically valid
- Service starts without errors
- Port binding is correct (no conflicts)
- Network connectivity to dependencies works
- Reverse proxy route resolves (if applicable)

### Final Verification:
- All services running and healthy
- No port conflicts across entire stack
- Backup coverage includes new services (if applicable)
- Rollback procedures documented for each phase

## Migration Notes

<Notes about:
- Service downtime expectations
- Data migration requirements
- Order-dependent operations
- Secrets that user needs to create>

## References

- [Link to research doc]
- [Link to design doc]
- [Link to structural map]
- [Key compose files affected]
```

## What Does NOT Belong in Plans

- Actual secret values (reference .env.example templates instead)
- .env file contents (only reference paths and variable names)
- Decisions that should be in design docs (why this architecture)
- Structural decisions that should be in structural maps (where files go)

## Section Guidelines

- **Config Changes**: Be specific about file paths. Include purpose for each change
- **Commands to Execute**: Always in fenced bash blocks. Include comments. Mark as "User runs these"
- **Rollback Commands**: Every phase MUST have rollback commands. No exceptions
- **Verification Checklist**: Actionable items the user can check. Include specific commands
- **Success Criteria**: Checkboxes that /implementing-services will mark during execution
- **Migration Notes**: Anything the user needs to know about timing, downtime, or preparation
