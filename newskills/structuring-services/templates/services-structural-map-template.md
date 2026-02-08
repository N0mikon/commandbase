# Services Structural Map Template

Template for structural map documents written to `.docs/structure/`.

## File Naming

Format: `MM-DD-YYYY-description.md` in `.docs/structure/`

Examples:
- `02-08-2026-homelab-file-layout.md`
- `02-08-2026-media-stack-reorganization.md`
- `02-08-2026-per-service-directory-migration.md`

## Frontmatter

Handled by docs-writer agent. Provide these fields:
```yaml
doc_type: "structure"
topic: "<infrastructure structure topic>"
tags: [services, <relevant aspect tags>]
references: [<design doc, key repo paths>]
```

## Body Sections

```markdown
# <Structure Topic>

**Date**: YYYY-MM-DD
**Design Reference**: <link to design doc or "lightweight mode — no design doc">

## Current Structure

Relevant file tree of the existing repo:
```
homelab/
├── docker-compose.yml          # [N] services defined
├── .env                        # exists (not read)
├── .env.example                # [N] variables documented
├── traefik/
│   ├── traefik.yml
│   └── dynamic/
│       └── ...
└── ...
```

Notes on current conventions:
- [Convention 1]
- [Convention 2]

## Proposed Structure

Target state with markers:
```
homelab/
├── services/                    # [NEW]
│   ├── traefik/                 # [REORGANIZED from root]
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   └── config/
│   ├── postgres/                # [NEW]
│   │   ├── docker-compose.yml
│   │   ├── .env.example
│   │   └── data/               # volume mount target
│   └── ...
├── shared/                      # [NEW]
│   ├── networks.yml             # shared network definitions
│   └── .env.example             # shared variables
└── ...
```

Markers: [NEW] = created, [REORGANIZED] = moved/renamed, [UNCHANGED] = no changes, [REMOVED] = deleted

## Changes Required

File-by-file changes:

| Action | File/Directory | Details |
|--------|---------------|---------|
| Create | `services/traefik/` | New directory for Traefik service |
| Move | `docker-compose.yml` → `services/traefik/docker-compose.yml` | Extract Traefik service |
| Create | `services/traefik/.env.example` | Template with placeholder values |
| ... | ... | ... |

## .env.example Templates

Placeholder-value templates for each service:

### [Service Name]
```
# [Service Name] Configuration
# Copy to .env and fill in real values

# Database
SERVICE_DB_PASSWORD=CHANGE_ME
SERVICE_DB_NAME=service_db

# Application
SERVICE_SECRET_KEY=CHANGE_ME
SERVICE_DOMAIN=service.example.com
```

**All values are placeholders. Never include real secrets.**

## Network Map

| Network | Purpose | Services | Defined In |
|---------|---------|----------|-----------|
| proxy | Reverse proxy access | traefik, app1, app2 | shared/networks.yml |
| internal | Backend communication | app1, postgres | services/app1/docker-compose.yml |

## Migration Sequence

Ordered steps for reorganization (each leaves services reachable):

### Step 1: [Description]
**Changes**: [What files/configs change]
**Services affected**: [Which services]
**Verification**: [How to confirm services still work]
**Rollback**: [How to undo if needed]

### Step 2: [Description]
...

[Number each step. Each step must leave all services reachable.]

## Conventions

| Convention | Pattern | Example |
|-----------|---------|---------|
| Compose file naming | `docker-compose.yml` per service dir | `services/app/docker-compose.yml` |
| .env template naming | `.env.example` per service dir | `services/app/.env.example` |
| Volume base path | `/opt/docker/<service>/` | `/opt/docker/postgres/data/` |
| Network naming | Lowercase, descriptive | `proxy`, `internal`, `monitoring` |

## Next Steps

- /planning-services — to break this into phased implementation tasks
```

## What Does NOT Belong in Structural Maps

- Compose YAML syntax or service definitions
- Actual config file contents (only file locations and purposes)
- Design rationale (that's in the design doc)
- Task breakdown or phase planning (that's for /planning-services)
- Secret values or real .env contents
- Docker commands or deployment procedures

## Section Guidelines

- **Current Structure**: Show actual file tree from repo exploration. Include note counts/service counts
- **Proposed Structure**: Use [NEW], [REORGANIZED], [UNCHANGED], [REMOVED] markers
- **Changes Required**: One row per file operation. Be specific about source and destination
- **.env.example Templates**: Placeholder values only. Group by service. Include comments explaining each variable
- **Migration Sequence**: Only for reorganizations. Each step must state what changes AND how to verify services still work
- **Conventions**: Document patterns for future reference. These become the repo's style guide
