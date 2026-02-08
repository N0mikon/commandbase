# Services Research Workflow

Detailed process for researching homelab infrastructure before writing service plans.

## Step 1: Context Gathering & Initial Analysis

### Read All Mentioned Files

When invoked with arguments or context:
1. Read ALL files mentioned by the user immediately and FULLY — no limit/offset
2. Read upstream BRDSPI artifacts if they exist:
   - `.docs/research/` with services tags — infrastructure research findings
   - `.docs/design/` with services tags — architecture decisions
   - `.docs/structure/` with services tags — structural map
   - `.docs/brainstorm/` with services tags — direction and preferences
3. Note key constraints, decisions, and affected services

### Explore the Repo

Before presenting understanding, gather context from the actual repo:

**File-system exploration commands:**
- `Glob("**/docker-compose*.yml", path=repo_path)` — find all compose files
- `Glob("**/compose*.yml", path=repo_path)` — find v2-style compose files
- `Glob("**/.env.example", path=repo_path)` — find .env templates
- `Grep("image:", path=repo_path, glob="*.yml")` — find service images
- `Grep("ports:", path=repo_path, glob="*.yml")` — find port mappings
- `Grep("depends_on:", path=repo_path, glob="*.yml")` — find dependencies
- `Grep("healthcheck:", path=repo_path, glob="*.yml")` — find health checks
- `Grep("networks:", path=repo_path, glob="*.yml")` — find network definitions

**Read affected files:**
- Read compose files that will be modified
- Read config files that will change
- Read .env.example files for variable names (NEVER read .env files)

### Present Understanding

After exploration, present what you found:
```
Here's my understanding of the infrastructure based on repo exploration:

Current state:
- [N] services across [N] compose file(s)
- Key services affected: [list]
- Current topology: [brief description]

Files I'll need to reference:
- [file 1] — [what it contains]
- [file 2] — [what it contains]

Questions exploration couldn't answer:
1. [Question 1]
2. [Question 2]
```

Ask ONLY questions that tool exploration couldn't answer. Don't ask about things you can discover from the repo.

## Step 2: Deep Research & Discovery

### When Corrections Come In

If the user corrects a misunderstanding:
1. Explore further to verify the correction
2. Read additional files as needed
3. Update your understanding

### Complex Infrastructure

For complex changes affecting many services:
1. Spawn `general-purpose` agents to explore different areas in parallel
2. One agent per concern area (networking, volumes, proxy, etc.)
3. Wait for ALL agents to complete
4. Compile findings before proceeding

### Verification Before Planning

Before writing the plan, verify you have:
- [ ] Read all compose files that will be modified
- [ ] Identified all services affected by the change
- [ ] Mapped dependencies between affected services
- [ ] Found all config files that need updating
- [ ] Documented port allocations to avoid conflicts
- [ ] Identified volume mounts that will change
- [ ] Checked for .env.example templates
- [ ] Verified network topology for affected services

## Exploration Best Practices

### Use the Right Tool

| Need | Tool | Example |
|------|------|---------|
| Find compose files | Glob | `Glob("**/docker-compose*.yml")` |
| Search for service name | Grep | `Grep("service_name", glob="*.yml")` |
| Read specific file | Read | `Read("services/app/docker-compose.yml")` |
| Explore directory | Bash ls | `ls services/` |
| Find port usage | Grep | `Grep("8080", glob="*.yml")` |

### Verify, Don't Assume

- **Don't assume** service names — find them in compose files
- **Don't assume** port numbers — check compose port mappings
- **Don't assume** network names — read network definitions
- **Don't assume** volume paths — check compose volume mounts
- **Don't assume** .env variables — read .env.example files

### Secrets Safety

- NEVER read `.env` file contents
- Only read `.env.example` or `.env.sample` files
- Reference .env files by path only
- Plan phases should include "create .env from .env.example" as a user step
