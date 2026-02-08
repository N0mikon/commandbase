# Services Question Domains Reference

This reference provides infrastructure-specific direction question templates. Use these as starting points — adapt questions to the specific infrastructure goal being brainstormed. Questions should probe DIRECTION, not configuration details.

## Stack Selection Domain

**What it settles:** Which core services and tools to run — the foundation everything else builds on.

**Constrains:** Compose Architecture, Networking

**Default Topics:**
1. **Reverse Proxy** - Which traffic routing tool to use
2. **Authentication** - How access is controlled
3. **Container Management** - How containers are monitored and managed
4. **Update Strategy** - How services stay current

**Direction Questions:**

Reverse Proxy:
- "Traefik or Nginx Proxy Manager?" → [Traefik (config-as-code)] [Nginx Proxy Manager (GUI)] [Caddy (simple)] [You decide]
- "SSL certificate management?" → [Let's Encrypt automatic] [Cloudflare origin certs] [Self-signed for internal] [You decide]

Authentication:
- "Authelia or Cloudflare tunnels for auth?" → [Authelia (self-hosted SSO)] [Cloudflare Access] [Basic auth per-service] [You decide]
- "Single sign-on or per-service credentials?" → [SSO (one login)] [Per-service] [You decide]

Management:
- "Portainer or Docker CLI only?" → [Portainer (GUI)] [CLI only] [Dockge (lightweight)] [You decide]
- "Watchtower for auto-updates or manual?" → [Watchtower (automatic)] [Manual updates] [Scheduled maintenance window] [You decide]

**Interdependency notes:**
- If Traefik → labels-based routing → affects compose file structure
- If Cloudflare tunnels → no port forwarding needed → simplifies networking
- If Authelia → needs Redis/database → adds to dependency chain

---

## Compose Architecture Domain

**What it settles:** How Docker services are organized, grouped, and configured.

**Constrains:** Dependencies & Ordering

**Default Topics:**
1. **File Organization** - Single compose or per-service files
2. **Network Topology** - Shared networks or isolated per-service
3. **Configuration Management** - How secrets and environment variables are handled
4. **Volume Strategy** - Where data lives and how it's mounted

**Direction Questions:**

Organization:
- "Single docker-compose.yml or per-service files?" → [Single monolith] [Per-service files] [Grouped by function] [You decide]
- "Version pinning strategy?" → [Exact versions (nginx:1.25.3)] [Minor versions (nginx:1.25)] [Latest tag] [You decide]

Networking:
- "Shared Docker network or isolated per-service?" → [Shared network] [Isolated + explicit connections] [You decide]
- "Custom bridge networks or default?" → [Custom named networks] [Default bridge] [You decide]

Configuration:
- "`.env` files or Docker secrets?" → [.env files] [Docker secrets] [Mix (secrets for sensitive)] [You decide]
- "One global .env or per-service .env?" → [Global] [Per-service] [You decide]

Volumes:
- "Named volumes or bind mounts?" → [Named volumes] [Bind mounts] [Mix] [You decide]
- "Data directory location?" → [/opt/docker/] [~/docker/] [Custom path] [You decide]

---

## Networking Domain

**What it settles:** How services communicate with each other and how they're accessed externally.

**Default Topics:**
1. **External Access** - How services are reached from outside the network
2. **DNS Strategy** - How services are addressed
3. **Internal Communication** - How services talk to each other
4. **Remote Access** - How you connect when away from home

**Direction Questions:**

External Access:
- "Reverse proxy with SSL termination?" → [Yes, all traffic through proxy] [Direct port exposure for some] [You decide]
- "Exposed ports vs proxy-only?" → [All through proxy] [Some direct ports] [You decide]

DNS:
- "Public DNS pointing to your IP or split DNS?" → [Public DNS] [Split DNS (internal/external)] [Local only] [You decide]
- "Wildcard subdomain or per-service subdomains?" → [Wildcard (*.home.example.com)] [Per-service] [You decide]

Remote Access:
- "Tailscale/WireGuard or Cloudflare tunnels for remote access?" → [Tailscale (mesh VPN)] [WireGuard (traditional VPN)] [Cloudflare tunnels] [You decide]
- "Full network access or per-service tunnels?" → [Full network VPN] [Per-service exposure] [You decide]

---

## Backup Strategy Domain

**What it settles:** What's protected, how often, and where backups go.

**Default Topics:**
1. **Backup Tool** - Which backup solution to use
2. **Backup Scope** - What gets backed up
3. **Backup Destination** - Where backups are stored
4. **Backup Schedule** - How often and when

**Direction Questions:**

Tool:
- "Borg or restic?" → [Borg (mature, SSH)] [Restic (modern, multi-backend)] [Both for different data] [You decide]
- "Backup orchestrator?" → [Manual scripts] [Borgmatic] [Autorestic] [You decide]

Scope:
- "Volumes only or full container state?" → [Volumes only] [Volumes + configs] [Full state (images too)] [You decide]
- "Database dumps or volume snapshots?" → [Database dumps (consistent)] [Volume snapshots (fast)] [Both] [You decide]

Destination:
- "Local NAS, remote cloud, or both?" → [Local NAS only] [Remote cloud only] [Both (3-2-1)] [You decide]
- "Which remote target?" → [Backblaze B2] [S3/MinIO] [Another machine via SSH] [You decide]

Schedule:
- "Daily, weekly, or continuous?" → [Daily] [Weekly] [Continuous (on change)] [You decide]
- "Retention policy?" → [Keep 7 daily, 4 weekly, 12 monthly] [Keep everything] [Custom] [You decide]

---

## Dependencies & Ordering Domain

**What it settles:** How services relate to each other at startup, runtime, and failure.

**Default Topics:**
1. **Startup Ordering** - Which services must start first
2. **Health Checks** - How readiness is verified
3. **Failure Behavior** - What happens when a service goes down
4. **Shared Resources** - Databases and caches that multiple services use

**Direction Questions:**

Startup:
- "Which services must start first?" → [Database → App → Proxy] [All parallel] [Explicit depends_on chain] [You decide]
- "Wait for healthy or just started?" → [Wait for healthy (health checks)] [Just wait for started] [You decide]

Health:
- "Health check requirements?" → [HTTP checks on every service] [Only critical services] [None (trust Docker)] [You decide]
- "Restart policy?" → [Always restart] [Restart on failure only] [No auto-restart] [You decide]

Failure:
- "What happens when a dependency fails?" → [Dependent services stop] [Graceful degradation] [Manual intervention] [You decide]
- "Alerting on failure?" → [Email/webhook alerts] [Dashboard only] [Logs only] [You decide]

Shared Resources:
- "Shared databases or per-service?" → [Shared (PostgreSQL/MariaDB)] [Per-service (SQLite)] [Mix] [You decide]
- "Shared Redis or per-service caching?" → [Shared Redis] [Per-service] [No caching layer] [You decide]

---

## Interdependency Map

When brainstorming multiple domains, decisions in one domain constrain options in others:

```
Stack Selection
  ├── Reverse proxy choice → affects Compose (labels vs config files)
  ├── Auth choice → affects Dependencies (Authelia needs Redis)
  └── Tunnel choice → affects Networking (no port forwarding needed)

Compose Architecture
  ├── File organization → affects Dependencies (single vs multi-file deps)
  └── Network topology → affects how services discover each other

Networking
  └── Remote access method → affects Backup (which destinations are reachable)
```

**Always brainstorm Stack Selection before Compose and Networking.** Dependencies & Ordering should come last since it depends on all other decisions.

---

## Anti-Patterns

**DON'T ask (belongs in implementation):**
- Specific Docker image tags or versions
- Compose YAML syntax or structure
- Traefik middleware configuration
- Exact backup cron schedules

**DON'T ask (belongs in code or vault brainstorming):**
- Application code architecture
- Vault organization philosophy
- UI/UX design decisions

**DO ask (direction questions):**
- Which service for each role? (Traefik vs Nginx, Borg vs restic)
- Which organizational philosophy? (monolith compose vs per-service)
- Which access pattern? (VPN vs tunnel, shared vs isolated)
- Which backup philosophy? (3-2-1, local only, continuous vs scheduled)
