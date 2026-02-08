# Services Structure Aspects

Guide to structural dimensions and decisions for `/structuring-services`.

## Structural Elements

### 1. Compose File Organization

**What to decide:** How compose files are arranged in the repo.

**Common patterns:**

| Pattern | Description | Best For |
|---------|-------------|----------|
| Single file | One `docker-compose.yml` with all services | Small stacks (< 10 services) |
| Grouped by function | `compose.media.yml`, `compose.monitoring.yml` | Medium stacks with clear groupings |
| Per-service directories | `services/traefik/docker-compose.yml` | Large stacks, independent service management |
| Override files | Base + `docker-compose.override.yml` | Dev/prod differences on same stack |

**Current vs proposed comparison format:**
```
Current: Single docker-compose.yml (15 services)
Proposed: Per-service directories under services/
Rationale: Independent restarts, clearer ownership
```

**Migration considerations:**
- Moving from single to per-service requires extracting shared networks to a separate file or using `docker compose -f` with multiple files
- Shared volumes and networks need explicit external declarations
- Service names must remain consistent to preserve inter-service references

### 2. .env Template Layout

**What to decide:** How environment variable templates are organized.

**Common patterns:**

| Pattern | Description | Best For |
|---------|-------------|----------|
| Single .env.example | One file at repo root | Small stacks, shared variables |
| Per-service .env.example | `services/app/.env.example` | Per-service directories |
| Shared + per-service | Root `.env.example` for shared, per-service for specific | Hybrid setups |

**Naming conventions:**
- `.env.example` — most common, understood by developers
- `.env.sample` — alternative naming
- `.env.template` — less common but explicit
- `env.example` (no dot) — visible in file managers

**Variable naming patterns:**
- `SERVICE_VARIABLE` — prefixed by service name (e.g., `POSTGRES_PASSWORD`)
- `CATEGORY_VARIABLE` — prefixed by category (e.g., `DB_PASSWORD`)
- Uppercase with underscores is the universal convention

**Placeholder format:**
- `CHANGE_ME` — clear call to action
- `your_value_here` — descriptive placeholder
- `<description>` — angle bracket placeholder
- Comments above each variable explaining purpose

**CRITICAL: .env.example files use placeholder values only. NEVER include real secrets.**

### 3. Proxy Route Organization

**What to decide:** How reverse proxy routes are configured and organized.

**Traefik patterns:**

| Pattern | Description | Best For |
|---------|-------------|----------|
| Labels in compose | Traefik labels on each service | Tight coupling, single compose file |
| File provider | `traefik/dynamic/*.yml` files | Decoupled, per-service config files |
| Mixed | Labels for simple routes, file provider for complex | Gradual migration |

**Nginx patterns:**

| Pattern | Description | Best For |
|---------|-------------|----------|
| Single config | One `nginx.conf` with all server blocks | Simple setups |
| Per-service includes | `conf.d/service.conf` per service | Modular management |
| Template-based | `templates/*.conf.template` with envsubst | Dynamic configuration |

**Migration considerations:**
- Switching from labels to file provider requires updating compose files AND creating config files
- Route changes should be atomic — don't leave a service unreachable between steps

### 4. Volume Directory Layout

**What to decide:** Where persistent data lives on the host.

**Common base paths:**

| Path | Convention | Notes |
|------|-----------|-------|
| `/opt/docker/` | Server convention | Standard for managed services |
| `/srv/` | FHS standard | "Data for services provided by this system" |
| `~/docker/` | User home | Easy permissions, no sudo needed |
| `/data/` | Simple custom | Clear purpose, separate partition |

**Subdirectory structure:**
```
/opt/docker/
├── service-name/
│   ├── config/    # Configuration files
│   ├── data/      # Persistent data
│   └── logs/      # Log files (if not using Docker logging)
```

**Migration considerations:**
- Moving volumes requires stopping services, copying data, updating compose mounts, restarting
- Permissions must be preserved (uid:gid mapping)
- Symlinks can ease transitions but add complexity

### 5. Backup Configuration

**What to decide:** Where backup scripts and configs live.

**Common patterns:**

| Component | Location Options |
|-----------|-----------------|
| Backup scripts | `scripts/backup/`, `backup/`, alongside compose files |
| Schedule config | `crontab`, `systemd/timers/`, compose-based scheduling |
| Exclusion lists | `backup/.excludes`, alongside backup script |
| Restore scripts | Next to backup scripts |

**Migration considerations:**
- Backup scripts reference volume paths — update when volumes move
- Schedule configs may reference script paths — update when scripts move
- Test restore procedures after any backup config relocation

### 6. Network Definitions

**What to decide:** How Docker networks are defined and where.

**Common patterns:**

| Pattern | Description | Best For |
|---------|-------------|-------|
| In compose file | Networks defined in each compose file | Single compose setups |
| Shared network file | Separate compose file for shared networks | Per-service directory setups |
| Pre-created external | Networks created outside compose | Multi-compose coordination |

**Naming conventions:**
- `proxy` or `web` — for reverse proxy network
- `internal` or `backend` — for backend services
- `<stack>_default` — Docker Compose auto-generated
- Descriptive: `monitoring`, `database`, `media`

**Migration considerations:**
- Renaming networks requires recreating containers
- External networks must exist before compose up
- Services on different compose files need external network declarations

## Convention Deference Principle

When working with an established repo:

1. **Identify existing patterns** — how are files currently organized?
2. **Follow existing patterns** where they don't conflict with design decisions
3. **Only deviate** when the design explicitly requires a different approach
4. **Document deviations** — explain why the new pattern was chosen over the existing one
5. **Minimize disruption** — propose the smallest change that achieves the design goals

When working with a new repo:

1. **Propose conventions** based on the design decisions
2. **Present options** via AskUserQuestion for subjective choices
3. **Document chosen conventions** for future reference

## Migration Sequencing Rules

For infrastructure reorganizations:

1. **Service reachability is paramount** — every intermediate state must have all services reachable
2. **Config changes before restart** — modify all configs, then restart affected services
3. **Network changes are dangerous** — plan these carefully, may require brief coordinated restart
4. **Volume moves require downtime** — stop service, move data, update config, restart
5. **Proxy changes should be atomic** — update route and restart proxy in one step
6. **Test after each step** — verify affected services respond correctly
