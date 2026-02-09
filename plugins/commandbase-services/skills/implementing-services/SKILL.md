---
name: implementing-services
description: "Use this skill when executing homelab service implementation plans from .docs/plans/. This includes editing compose files, creating config files, generating .env.example templates, updating proxy routes, and generating deployment commands for user execution. Activate when the user says 'implement services', 'deploy this plan', 'execute service changes', or provides a services plan path."
---

# Implementing Services

You are tasked with implementing an approved service plan from `.docs/plans/`. These plans contain phases with specific config changes, deployment commands, and verification checklists.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO COMMAND EXECUTION — GENERATE, NEVER RUN
```

You edit config files directly but NEVER execute deployment commands. All docker commands are generated for the user to run.

**No exceptions:**
- Don't execute docker commands — generate them for user to run
- Don't read .env file contents — reference paths only
- Don't skip rollback commands — every deploy needs a rollback path
- Don't claim "should work" — provide verification steps for user to confirm

**Same-machine exception:** If `homelab_same_machine: true` in CLAUDE.md, read-only docker commands (`ps`, `logs`, `network ls`, `stats`) MAY be auto-executed for verification. Write commands (`up`, `down`, `pull`, `restart`) are NEVER auto-executed.

## The Gate Function

```
BEFORE claiming any phase is complete:

1. READ: The plan phase requirements fully
2. CONFIGURE: Check CLAUDE.md for homelab_repo_path, homelab_same_machine
3. CHECKPOINT: Create baseline via /bookmarking-code create (first phase only)
4. EXECUTE: Edit config files using file-system tools (Write/Edit)
5. GENERATE: Produce deployment commands, rollback commands, verification checklist
6. VERIFY: If same-machine, run read-only docker commands; otherwise present checklist
7. ONLY THEN: Mark checkboxes and proceed

Skip verification = false completion claim
```

## Getting Started

When given a plan path:
- Read the plan completely and check for any existing checkmarks (- [x])
- Read CLAUDE.md for `homelab_repo_path` and `homelab_same_machine`
- **Read files fully** — never use limit/offset parameters, you need complete context
- Think deeply about how the phases fit together
- Create a todo list to track your progress
- Create baseline checkpoint: `/bookmarking-code create "pre-implementation"`
- Start implementing if you understand what needs to be done

If no plan path provided, ask for one or list available plans in `.docs/plans/`.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan exactly. If reality requires deviation, STOP and present the deviation before making it.
- Implement each phase fully before moving to the next
- Generate deployment commands and verification checklists after each phase
- Update checkboxes in the plan as you complete sections
- Continue through all phases without stopping for manual confirmation

When things don't match the plan exactly, STOP and present the mismatch to the user.

## Config Operations

See ./reference/services-operations.md for detailed guidance on each operation type.

### Editing Compose Files
- Use Read to examine current compose file content
- Use Edit for surgical changes to existing services
- Use Write for creating new compose files
- Preserve existing formatting and comments
- Validate YAML structure mentally before writing

### Creating .env.example Files
- Use Write to create .env.example templates
- Include descriptive comments above each variable
- Use placeholder values (CHANGE_ME, your_value_here)
- NEVER include real secret values
- Group variables by purpose

### Updating Proxy Configs
- Read current proxy config (Traefik, Nginx, Caddy) to understand patterns
- Follow existing conventions in the repo
- For Traefik labels: add to compose file service definitions
- For file provider: create/update files in proxy config directory

### Creating Config Files
- Use Write for new config files
- Follow naming conventions from the repo
- Place files according to the structural map

## Same-Machine Mode

When `homelab_same_machine: true` in CLAUDE.md:

**Auto-execute (read-only verification):**
- `docker compose ps` — check service status
- `docker logs --tail 50 <service>` — check for startup errors
- `docker network ls` — verify network creation
- `docker stats --no-stream` — check resource usage

**Generate but DON'T auto-execute (write operations):**
- `docker compose up -d` — start/restart services
- `docker compose pull` — pull new images
- `docker compose restart` — restart services
- `docker compose down` — stop and remove services
- `docker compose build` — build custom images

When `homelab_same_machine` is not set or false:
- ALL commands are generated, NONE executed
- Present complete command blocks for user to copy and run

## Service Health Verification

After generating deployment commands, present these verification checks:

1. **Port conflict detection** — no two services on same host port
2. **Network connectivity** — services can reach their dependencies
3. **Volume mount validation** — paths exist, permissions correct
4. **DNS/proxy route verification** — routes resolve correctly
5. **Backup scope coverage** — critical data is in backup plan

In same-machine mode, run read-only checks automatically. Otherwise, present as a checklist for the user.

## Execution Flow

For each phase:

1. **Implement config changes** described in the plan (edit compose files, create configs, generate .env.example)
2. **Generate commands** — deployment commands, rollback commands, verification checklist
3. **Present to user** — show changes made and commands to run
4. **Wait for user verification** — user runs commands, reports results
5. **Record results** — update plan checkboxes based on user feedback
6. **Create checkpoint** — `/bookmarking-code create "phase-N-done"`
7. **Move to the next phase** — only after user confirms success and checkpoint created

**Remember:** Steps 2, 3, and 6 are not optional. No commands = no completion. No checkpoint = no proceeding.

Do NOT pause between config edits within a phase. But DO pause after presenting commands for user to execute.

## Output Format

For each phase, present in this format:

```
## Phase N: [Phase Name]

### Changes Made (to repo files)
- Modified `docker-compose.yml` — added [service] definition
- Created `services/[name]/.env.example` — template with placeholders
- Updated `traefik/dynamic/[name].yml` — added route configuration

### Commands to Execute
```bash
# Pull new images
docker compose pull [service]

# Deploy
docker compose up -d [service]

# Verify deployment
docker compose ps [service]
docker logs --tail 50 [service]
```

### Rollback Commands (if needed)
```bash
docker compose stop [service]
docker compose rm [service]
# Restore previous compose file from git
git checkout HEAD~1 -- docker-compose.yml
docker compose up -d
```

### Verification Checklist
- [ ] Service is running (docker compose ps shows "Up")
- [ ] Service responds on expected port
- [ ] Reverse proxy route works
- [ ] Health check passes
- [ ] Backup job registered (if applicable)
```

See ./templates/services-command-template.md for the full template.

## If You Get Stuck

When something isn't working as expected:
- First, make sure you've read the plan and all referenced files completely
- Consider if the repo has changed since the plan was written
- Try exploring with file-system tools to understand current state
- If truly blocked, present the issue clearly and ask for guidance

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done
- Pick up from the first unchecked item
- Verify previous work only if something seems off

## Completion

When all phases are complete:
```
Implementation complete!

All phases executed:
- [x] Phase 1: [name]
- [x] Phase 2: [name]
- [x] Phase 3: [name]

Config changes:
- [N] files created
- [N] files modified
- [N] .env.example templates generated

Commands generated for user execution.

All success criteria verified with user confirmation.
The plan at `.docs/plans/[filename].md` has been fully implemented.
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- About to execute a docker write command (up, down, pull, restart)
- Reading .env file contents instead of .env.example
- Marking a checkbox without user confirming deployment worked
- Proceeding to next phase without generating rollback commands
- Skipping the baseline checkpoint
- Making changes not described in the plan without explaining why
- Including secret values in .env.example files
- Auto-executing docker commands when same-machine mode is not enabled

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This command is safe to run" | Only read-only commands in same-machine mode. Otherwise, generate only. |
| "I just need to peek at .env" | Read .env.example. Never .env contents. |
| "User is waiting, I'll run it" | Generate commands. User decides when to run. |
| "Rollback isn't needed here" | Every phase needs rollback commands. No exceptions. |
| "I'll verify at the end" | Per-phase verification catches issues early. Do it now. |
| "The config is obviously correct" | Present verification checklist. Let user confirm. |
| "While I'm here, I should also..." | Only change what the plan specifies. |

## The Bottom Line

**Generate, never execute. Edit configs, present commands.**

Follow the plan. Edit config files. Generate deployment commands with rollback. Present verification checklists. Wait for user confirmation. THEN mark complete.

This is non-negotiable. Every phase. Every time.
