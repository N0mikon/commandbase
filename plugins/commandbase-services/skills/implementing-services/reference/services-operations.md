# Services Operations

Detailed guide for service implementation operations in `/implementing-services`.

## Config File Operations

### Editing Compose Files

**Reading current state:**
```
Read("path/to/docker-compose.yml")
```

**Surgical edits** (modifying existing services):
```
Edit(
  file_path="path/to/docker-compose.yml",
  old_string="existing content",
  new_string="modified content"
)
```

**Creating new compose files:**
```
Write(
  file_path="services/new-service/docker-compose.yml",
  content="<complete compose file content>"
)
```

**Compose file conventions:**
- Preserve existing indentation (usually 2 spaces)
- Keep existing comments
- Add new services at the end of the services block
- Use the same style as existing services in the repo

**YAML validation checklist:**
- Consistent indentation (2 spaces, no tabs)
- Proper quoting for strings with special characters
- Lists use `- ` prefix with consistent spacing
- Environment variables properly formatted
- Port mappings in quotes if using host:container format

### Creating .env.example Files

**Template structure:**
```
# [Service Name] Configuration
# Copy this file to .env and fill in the actual values
# DO NOT commit the .env file to git

# =============================================================================
# Required Variables
# =============================================================================

# Database password for [service]
SERVICE_DB_PASSWORD=CHANGE_ME

# Secret key for session encryption
SERVICE_SECRET_KEY=CHANGE_ME

# =============================================================================
# Optional Variables (defaults shown)
# =============================================================================

# Log level (debug, info, warn, error)
SERVICE_LOG_LEVEL=info

# External URL for this service
SERVICE_URL=https://service.example.com
```

**Rules:**
- NEVER include real secret values
- Use `CHANGE_ME` for secrets that must be set
- Use sensible defaults for non-secret variables
- Group by required vs optional
- Comment every variable explaining its purpose
- Include header noting to copy to .env

### Updating Proxy Configs

**Traefik labels (in compose):**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.service.rule=Host(`service.domain.com`)"
  - "traefik.http.routers.service.tls.certresolver=letsencrypt"
  - "traefik.http.services.service.loadbalancer.server.port=8080"
```

**Traefik file provider:**
```yaml
# traefik/dynamic/service.yml
http:
  routers:
    service:
      rule: "Host(`service.domain.com`)"
      service: service
      tls:
        certResolver: letsencrypt
  services:
    service:
      loadBalancer:
        servers:
          - url: "http://service:8080"
```

**Nginx server block:**
```nginx
server {
    listen 443 ssl;
    server_name service.domain.com;

    location / {
        proxy_pass http://service:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Follow existing patterns** — check which proxy the repo uses and match its style.

### Creating Config Files

**Process:**
1. Read the plan for file path and content requirements
2. Check if parent directory exists (create with Bash `mkdir -p` if needed)
3. Write the config file using Write tool
4. Verify the file was created

**Common config patterns:**
- TOML for application configs
- YAML for Docker and orchestration
- INI for legacy applications
- JSON for API-oriented services

## Command Generation

### Deployment Commands

Generate commands following this pattern:

```bash
# Step 1: Pull latest images
docker compose -f path/to/docker-compose.yml pull [service-name]

# Step 2: Create .env from template (USER MUST DO THIS)
# cp path/to/.env.example path/to/.env
# Then edit .env to fill in real values

# Step 3: Start the service
docker compose -f path/to/docker-compose.yml up -d [service-name]

# Step 4: Verify
docker compose -f path/to/docker-compose.yml ps [service-name]
docker logs --tail 50 [service-name]
```

**Command conventions:**
- Always include `-f` flag when compose file is not in current directory
- Specify service name to avoid affecting other services
- Include verification commands after deployment
- Comment each step with what it does
- Note when user must take manual action (filling in .env)

### Rollback Commands

Every phase must include rollback:

```bash
# Option 1: Stop and remove the new service
docker compose -f path/to/docker-compose.yml stop [service-name]
docker compose -f path/to/docker-compose.yml rm -f [service-name]

# Option 2: Restore previous config and redeploy
git checkout HEAD~1 -- path/to/docker-compose.yml
docker compose -f path/to/docker-compose.yml up -d

# Option 3: Full rollback (if multiple files changed)
git stash  # or git checkout to previous state
docker compose -f path/to/docker-compose.yml down
docker compose -f path/to/docker-compose.yml up -d
```

### Verification Commands

Read-only commands safe for same-machine auto-execution:

```bash
# Check service status
docker compose -f path/to/docker-compose.yml ps [service-name]

# Check logs for errors
docker logs --tail 50 [service-name]

# Check network connectivity
docker network ls
docker network inspect [network-name]

# Check resource usage
docker stats --no-stream [service-name]

# Check port binding
docker port [service-name]
```

## Operation Patterns by Compose Layout

### Single Compose File

```bash
# All commands from repo root
docker compose pull [service]
docker compose up -d [service]
docker compose ps [service]
```

### Per-Service Directories

```bash
# Commands from service directory or with -f flag
docker compose -f services/app/docker-compose.yml pull
docker compose -f services/app/docker-compose.yml up -d
docker compose -f services/app/docker-compose.yml ps
```

### Grouped Compose Files

```bash
# Commands with specific compose file
docker compose -f compose.media.yml pull [service]
docker compose -f compose.media.yml up -d [service]
docker compose -f compose.media.yml ps [service]
```

### Multiple Compose Files (shared networks)

```bash
# Bring up shared resources first
docker compose -f shared/networks.yml up -d

# Then bring up the service
docker compose -f services/app/docker-compose.yml up -d
```

## Secrets Safety Checklist

Before completing any phase, verify:
- [ ] No .env file contents were read
- [ ] .env.example uses placeholder values only
- [ ] Generated commands don't echo or print secrets
- [ ] No secret values appear in compose file labels or environment
- [ ] User is instructed to create .env from .env.example manually
