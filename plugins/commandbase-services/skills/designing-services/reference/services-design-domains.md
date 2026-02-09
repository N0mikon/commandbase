# Services Design Domains

Categories of infrastructure architecture decisions for `/designing-services`.

## Design Domains

### 1. Stack Topology

**When this applies:** Adding or removing services, grouping related services, deciding service boundaries.

**Decision areas:**
- Service grouping (media stack, monitoring stack, productivity stack)
- Shared vs dedicated databases (one PostgreSQL vs per-service)
- Service redundancy and failover
- Container vs host-native for specific services

**Example AskUserQuestion options:**
```
question: "How should database services be organized?"
options:
  - label: "Shared PostgreSQL"
    description: "Single PostgreSQL instance with per-service databases. Simpler backup, one upgrade path."
  - label: "Per-service databases"
    description: "Each service gets its own DB container. Full isolation, independent upgrades."
  - label: "You decide"
    description: "I'll choose based on the research findings and document my reasoning."
```

**Anti-patterns (belongs in Structure/Implementation, NOT Design):**
- Specific Docker image names or tags
- Compose file organization (that's Structure)
- Database schema or configuration details

### 2. Networking Strategy

**When this applies:** Deciding how services communicate, how external access works, network isolation.

**Decision areas:**
- Network isolation model (flat vs segmented)
- Reverse proxy strategy (Traefik labels, Nginx file-based, Caddy)
- DNS approach (public DNS, split-horizon, local only)
- Remote access method (VPN, tunnel, direct)
- Internal service discovery (Docker DNS, static IPs)

**Example AskUserQuestion options:**
```
question: "How should networks be segmented?"
options:
  - label: "Segmented by function"
    description: "Separate networks for frontend, backend, databases. Services only see what they need."
  - label: "Segmented by stack"
    description: "Each service group gets its own network. Media stack isolated from monitoring stack."
  - label: "Flat network"
    description: "All services on one network. Simplest setup, all services can reach each other."
  - label: "You decide"
    description: "I'll choose based on the research findings and document my reasoning."
```

**Anti-patterns (belongs in Structure/Implementation, NOT Design):**
- Specific subnet ranges or CIDR blocks
- Traefik label syntax or Nginx config blocks
- DNS record values or zone file entries

### 3. Auth Approach

**When this applies:** Deciding authentication and authorization for services.

**Decision areas:**
- SSO vs per-service authentication
- Auth middleware (Authelia, Authentik, Cloudflare Access)
- Which services need auth, which are public
- API key management approach

**Example AskUserQuestion options:**
```
question: "How should service authentication work?"
options:
  - label: "SSO with Authelia"
    description: "Centralized auth via Authelia forward-auth. Single login for all services."
  - label: "Per-service auth"
    description: "Each service handles its own auth. No shared auth layer."
  - label: "Cloudflare Access"
    description: "Auth at the edge via Cloudflare Zero Trust. No self-hosted auth needed."
  - label: "You decide"
    description: "I'll choose based on the research findings and document my reasoning."
```

**Anti-patterns (belongs in Structure/Implementation, NOT Design):**
- Auth middleware configuration syntax
- Specific OAuth client IDs or redirect URIs
- LDAP schema or user group definitions

### 4. Data Management

**When this applies:** Deciding volume strategy, backup policy, data retention.

**Decision areas:**
- Volume type preference (bind mounts vs named volumes)
- Backup tool and strategy (Borg, restic, rsync)
- Backup scope (volumes only, full container state, configs + data)
- Retention policy (daily/weekly/monthly, how long)
- Backup destination (local, remote, cloud)

**Example AskUserQuestion options:**
```
question: "What backup strategy should be used?"
options:
  - label: "Borg with local + remote"
    description: "Borg for deduplication. Backup to local disk + remote server. Strong retention."
  - label: "Restic to cloud"
    description: "Restic with S3-compatible backend. Cloud-native, encrypted at rest."
  - label: "Rsync to NAS"
    description: "Simple rsync to local NAS. No deduplication but easy to understand."
  - label: "You decide"
    description: "I'll choose based on the research findings and document my reasoning."
```

**Anti-patterns (belongs in Structure/Implementation, NOT Design):**
- Specific backup scripts or cron schedules
- Volume mount paths or permission settings
- Retention policy exact numbers (that's Planning)

### 5. Update Strategy

**When this applies:** Deciding how services are updated, tested, and rolled back.

**Decision areas:**
- Image version pinning (exact SHA, semver, latest)
- Update testing approach (staging, canary, direct)
- Rollback mechanism (git revert, previous image tag, snapshots)
- Automated vs manual updates (Watchtower, Renovate, manual)

**Example AskUserQuestion options:**
```
question: "How should container images be versioned?"
options:
  - label: "Pin exact versions"
    description: "Pin to specific version tags (e.g., postgres:16.2). Maximum reproducibility."
  - label: "Pin major version"
    description: "Pin to major version (e.g., postgres:16). Get patches automatically."
  - label: "Automated with Renovate"
    description: "Use Renovate to create PRs for version bumps. Review before applying."
  - label: "You decide"
    description: "I'll choose based on the research findings and document my reasoning."
```

**Anti-patterns (belongs in Structure/Implementation, NOT Design):**
- Specific image tags or SHA digests
- Watchtower configuration details
- Renovate config file contents

### 6. Monitoring

**When this applies:** Only when user has or wants monitoring tools. Not required for all designs.

**Decision areas:**
- Health check approach (Docker health checks, external probes)
- Monitoring stack (Uptime Kuma, Prometheus+Grafana, Netdata)
- Alert channels (email, Slack, Discord, Gotify)
- What to monitor (uptime, resource usage, logs, backups)

**Example AskUserQuestion options:**
```
question: "What monitoring approach should be used?"
options:
  - label: "Uptime Kuma"
    description: "Simple uptime monitoring with status page. Low overhead, easy setup."
  - label: "Prometheus + Grafana"
    description: "Full metrics pipeline. Powerful dashboards, flexible alerting. More complex."
  - label: "Docker health checks only"
    description: "Built-in Docker health checks with restart policies. No separate monitoring stack."
  - label: "You decide"
    description: "I'll choose based on the research findings and document my reasoning."
```

**Anti-patterns (belongs in Structure/Implementation, NOT Design):**
- Prometheus scrape configs or Grafana dashboard JSON
- Alert rule definitions
- Health check command syntax

## Domain Selection

Not all 6 domains apply to every design. Select based on research findings:

| Scenario | Domains Likely Needed |
|----------|----------------------|
| Adding a single service | Stack Topology, Networking |
| New homelab from scratch | All 6 domains |
| Reorganizing existing stack | Stack Topology, Networking, Data Management |
| Setting up backups | Data Management |
| Securing access | Auth Approach, Networking |
| Monitoring setup | Monitoring, Networking |

## Decision Quality Checklist

For each decision, verify:
- [ ] Based on research findings (not assumptions)
- [ ] Concrete options presented (not "Option A/B")
- [ ] User made the choice (or explicitly delegated via "You decide")
- [ ] Rationale documented (why this choice)
- [ ] Alternatives noted (why NOT the others)
- [ ] No implementation details leaked into design
- [ ] Secrets described by requirement, not by value
