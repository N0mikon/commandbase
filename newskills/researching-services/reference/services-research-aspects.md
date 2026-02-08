# Services Research Aspects

Guide to infrastructure research dimensions and tool usage for `/researching-services`.

## Research Dimensions

### 1. Service Inventory

**What to investigate:** Running services, container images, versions, restart policies.

**File-system tool commands:**
- `Glob("**/docker-compose*.yml", path=repo_path)` — find all compose files
- `Glob("**/compose*.yml", path=repo_path)` — find v2-style compose files
- `Grep("image:", path=repo_path, glob="*.yml")` — extract image references
- `Read` each compose file to map service definitions

**Live-state commands (optional, user-executed or same-machine):**
- `docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"`
- `docker compose ls` — list all compose projects

**Output format:** Table of service name, image, version, restart policy, compose file location.

### 2. Port Mapping

**What to investigate:** Host:container port bindings, exposed ports, potential conflicts.

**File-system tool commands:**
- `Grep("ports:", path=repo_path, glob="*.yml", -A=5)` — find port mappings with context
- `Grep("expose:", path=repo_path, glob="*.yml", -A=3)` — find internal-only exposed ports

**Live-state commands (optional):**
- `docker ps --format "{{.Names}}\t{{.Ports}}"` — actual port bindings

**Output format:** Table of service, host port, container port, protocol, compose file. Flag any host port used by multiple services.

### 3. Network Topology

**What to investigate:** Docker networks, which services share networks, inter-service connectivity.

**File-system tool commands:**
- `Grep("networks:", path=repo_path, glob="*.yml", -A=10)` — find network definitions and service attachments
- Look for top-level `networks:` blocks (network definitions) vs service-level `networks:` (attachments)

**Live-state commands (optional):**
- `docker network ls`
- `docker network inspect <network>` — see connected containers

**Output format:** Network map showing which services are on which networks, with connectivity implications.

### 4. Volume Mapping

**What to investigate:** Bind mounts, named volumes, data persistence locations.

**File-system tool commands:**
- `Grep("volumes:", path=repo_path, glob="*.yml", -A=10)` — find volume definitions
- Look for top-level `volumes:` blocks (named volumes) vs service-level `volumes:` (mount points)
- Identify bind mount paths (host:container format)

**Live-state commands (optional):**
- `docker volume ls`
- `docker volume inspect <volume>` — see mount points

**Output format:** Table of service, volume type (bind/named), host path, container path, read-only flag.

### 5. Environment Config

**What to investigate:** .env file locations, variable names, configuration patterns.

**File-system tool commands:**
- `Glob("**/.env.example", path=repo_path)` — find .env templates
- `Glob("**/.env.sample", path=repo_path)` — find .env samples
- `Glob("**/.env", path=repo_path)` — find .env file LOCATIONS only (NEVER read contents)
- `Grep("env_file:", path=repo_path, glob="*.yml")` — find env_file references in compose
- `Grep("environment:", path=repo_path, glob="*.yml", -A=10)` — find inline environment variables (names only)
- Read .env.example files to document variable names and descriptions

**CRITICAL: NEVER read .env file contents. Only read .env.example or .env.sample files.**

**Output format:** Table of service, .env file location, variable names (from .env.example), whether .env exists.

### 6. Reverse Proxy Routes

**What to investigate:** Domain mappings, path routing, SSL certificates, middleware.

**File-system tool commands:**
- `Grep("traefik", path=repo_path, glob="*.yml", -i=true)` — find Traefik labels
- `Grep("Host\\(", path=repo_path, glob="*.yml")` — find Traefik Host rules
- `Glob("**/traefik/**", path=repo_path)` — find Traefik config directory
- `Glob("**/nginx/**", path=repo_path)` — find Nginx config directory
- `Glob("**/Caddyfile", path=repo_path)` — find Caddy configs
- `Grep("server_name", path=repo_path, glob="*.conf")` — find Nginx server blocks
- `Grep("certresolver", path=repo_path, glob="*.yml", -i=true)` — find SSL config

**Output format:** Table of domain/path, target service, SSL status, middleware chain.

### 7. Dependencies

**What to investigate:** Service startup order, health checks, shared databases.

**File-system tool commands:**
- `Grep("depends_on:", path=repo_path, glob="*.yml", -A=5)` — find dependency declarations
- `Grep("healthcheck:", path=repo_path, glob="*.yml", -A=8)` — find health check definitions
- `Grep("condition:", path=repo_path, glob="*.yml")` — find startup conditions

**Output format:** Dependency graph showing startup order, health check status per service, shared database connections.

### 8. Backup Coverage

**What to investigate:** Backup tool configuration, scope, schedule, destinations.

**File-system tool commands:**
- `Glob("**/backup*", path=repo_path)` — find backup-related files
- `Glob("**/*borg*", path=repo_path)` — find Borg backup configs
- `Glob("**/*restic*", path=repo_path)` — find Restic backup configs
- `Grep("cron", path=repo_path)` — find scheduled tasks
- `Grep("backup", path=repo_path, -i=true)` — find backup references

**Output format:** Table of what's backed up, tool, schedule, destination, retention policy.

### 9. Resource Usage

**What to investigate:** CPU/memory limits, reservations, actual usage.

**File-system tool commands:**
- `Grep("mem_limit\\|cpus\\|memory\\|cpu_shares", path=repo_path, glob="*.yml")` — find resource constraints
- `Grep("deploy:", path=repo_path, glob="*.yml", -A=10)` — find deploy resource limits

**Live-state commands (optional):**
- `docker stats --no-stream` — current resource usage

**Output format:** Table of service, memory limit, CPU limit, actual usage (if available).

### 10. Gaps & Risks

**What to investigate:** Missing configurations, potential issues, security concerns.

**Source:** Cross-referencing findings from dimensions 1-9.

**Common gaps to check:**
- Services without health checks
- Volumes not covered by backup configs
- Ports exposed on 0.0.0.0 without reverse proxy protection
- Services without restart policies
- Missing .env.example for services using .env
- Services on the default bridge network (not isolated)
- No resource limits defined

**Output format:** Prioritized list of gaps with severity (critical/warning/info) and affected services.

## Parallel vs Sequential Exploration

**Use parallel exploration** (spawn agents) when:
- Infrastructure has 5+ services
- Multiple compose files in different directories
- Complex proxy configuration

**Use sequential exploration** when:
- Small infrastructure (1-3 services)
- Single compose file
- User asked about one specific aspect

## Example Query → Dimensions Map

| Research Question | Primary Dimensions | Secondary Dimensions |
|------------------|-------------------|---------------------|
| "What services are running?" | Service Inventory | Port Mapping, Dependencies |
| "Map the network topology" | Network Topology | Port Mapping, Reverse Proxy |
| "What's backed up?" | Backup Coverage | Volume Mapping, Gaps & Risks |
| "Full infrastructure audit" | All 10 dimensions | — |
| "Is anything exposed?" | Reverse Proxy, Port Mapping | Network Topology, Gaps & Risks |
| "Show me the data layout" | Volume Mapping | Backup Coverage, Environment Config |
