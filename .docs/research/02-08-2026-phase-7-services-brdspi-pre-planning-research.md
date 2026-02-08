---
date: 2026-02-08
status: complete
topic: "Phase 7 Services BRDSPI Pre-Planning Research"
tags: [research, services, brdspi, phase-7, infrastructure, homelab]
git_commit: 31aa0ef
implementation_status: "All 5 skills deployed and operational (31aa0ef)"
last_updated: 2026-02-08
last_updated_note: "Phase 7 implementation complete - all open questions resolved and built into deployed skills"
references:
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/plans/02-08-2026-phase-7-services-brdspi-skills.md
  - .docs/future-skills/services-rdspi.md
  - ~/.claude/skills/brainstorming-services/SKILL.md
  - ~/.claude/skills/researching-services/SKILL.md
  - ~/.claude/skills/designing-services/SKILL.md
  - ~/.claude/skills/structuring-services/SKILL.md
  - ~/.claude/skills/planning-services/SKILL.md
  - ~/.claude/skills/implementing-services/SKILL.md
  - ~/.claude/skills/researching-vault/SKILL.md
  - ~/.claude/skills/designing-vault/SKILL.md
  - ~/.claude/skills/structuring-vault/SKILL.md
  - ~/.claude/skills/planning-vault/SKILL.md
  - ~/.claude/skills/implementing-vault/SKILL.md
  - ~/.claude/skills/designing-code/SKILL.md
  - ~/.claude/skills/implementing-plans/SKILL.md
---

# Phase 7 Services BRDSPI Pre-Planning Research

**Date**: 2026-02-08
**Branch**: master
**Status**: Complete and Implemented (All 5 skills deployed to ~/.claude/skills/ as of 31aa0ef)

## Research Question
What patterns, structures, and domain-specific adaptations are needed to build 5 Services BRDSPI skills (/researching-services, /designing-services, /structuring-services, /planning-services, /implementing-services) based on proven code and vault BRDSPI patterns?

## Summary
Phase 7 is the final phase of the future-skills roadmap. It applies the BRDSPI pattern (proven across code and vault domains) to homelab/infrastructure service management. The entry point (/brainstorming-services) is already deployed. Five skills need to be built, following the established 11-section SKILL.md structure with domain-specific adaptations for Docker, networking, secrets, and hands-off deployment. The vault BRDSPI implementation (Phase 6) is the closest precedent, demonstrating how to adapt the code patterns to a new domain.

## Detailed Findings

### 1. Proven BRDSPI Skill Structure (Universal Across Domains)

Every BRDSPI skill follows an 11-section structure (~190-264 lines per skill):

| Section | Purpose | Avg Lines |
|---------|---------|-----------|
| Frontmatter | name + description | 4 |
| Title + Mission | One-sentence role | 4 |
| The Iron Law | Non-negotiable principle in code block | 15 |
| The Gate Function | Numbered verification checklist (6-7 steps) | 18 |
| Initial Response | Conditional: params → proceed, no params → prompt | 18 |
| Process Steps | Domain-specific workflow (H3 per step) | 99-158 |
| Important Guidelines | 4-5 numbered principles | 12 |
| Red Flags | 5-7 anti-pattern bullets | 14 |
| Rationalization Prevention | Excuse vs Reality table (5-7 rows) | 12 |
| The Bottom Line | Imperative summary + "non-negotiable" closing | 6 |
| Output Format | Summary template shown to user | 20 |

**Enforcement architecture** (consistent in all 14 existing BRDSPI skills): Iron Law → Gate Function → Red Flags → Rationalization Prevention → Bottom Line. This pattern accounts for ~35 lines per skill (~18% of total).

### 2. Artifact Chain Pattern

Each BRDSPI phase reads upstream artifacts and writes downstream:

```
/brainstorming-services  → .docs/brainstorm/{topic}.md     [ALREADY DEPLOYED]
/researching-services    → .docs/research/MM-DD-YYYY-*.md
/designing-services      → .docs/design/MM-DD-YYYY-*.md
/structuring-services    → .docs/structure/MM-DD-YYYY-*.md
/planning-services       → .docs/plans/MM-DD-YYYY-*.md
/implementing-services   → updates plan checkboxes + generates commands
```

**Consumption rules (from vault/code precedent):**
- Research: no upstream required (entry point after brainstorm)
- Design: REQUIRES research artifacts (fails without them), READS brainstorm (if exists)
- Structure: PREFERS design doc, can work standalone for simple changes
- Planning: PREFERS structural map, falls back to design, can work standalone
- Implementation: REQUIRES plan file

**All artifacts created via docs-writer agent** with consistent Task prompt:
```
doc_type: "research|design|structure|plan"
topic: "<service/infrastructure topic>"
tags: [services, <specific tags>]
references: [<key files>]
content: |
  <compiled body using ./templates/<domain>-<type>-template.md>
```

### 3. Existing Entry Point: /brainstorming-services

Already deployed (Phase 4). 3 files, 242-line SKILL.md.

**Covers 5 service domains:**
1. Stack Selection — reverse proxy, auth, container management, updates
2. Compose Architecture — file organization, network topology, config management, volumes
3. Networking — external access, DNS, internal comms, remote access
4. Backup Strategy — tool, scope, destination, schedule
5. Dependencies & Ordering — startup order, health checks, failure behavior, shared resources

**Output:** `.docs/brainstorm/{topic}.md` with Direction, Decisions, Decision Dependencies, Claude's Discretion, Deferred Ideas, Suggested Next Steps sections.

**Key for Phase 7:** The brainstorm artifact's Decision Dependencies section tells downstream skills which choices constrain which. The Claude's Discretion section marks areas with flexibility.

### 4. Domain-Specific Adaptations Needed for Services

Based on how vault adapted code patterns, services needs these domain-specific sections:

#### 4a. Hands-Off Deployment (Critical)
The roadmap states: "Edit configs, generate deploy commands (user executes, never auto-run)."

**Implementation pattern (unique to services):**
- `/implementing-services` generates commands but NEVER executes them
- Present commands in fenced code blocks for user to copy/run
- Include rollback commands alongside deploy commands
- Post-deploy verification suggestions (not auto-executed): connectivity checks, log review, backup registration

**Vault equivalent:** Vault skills use MCP tools or file-system tools to directly modify notes. Services CANNOT directly deploy — this is the key domain difference.

**Suggested Iron Law for /implementing-services:**
```
NO COMMAND EXECUTION — GENERATE, NEVER RUN
```

#### 4b. Secrets Handling
The roadmap states: "Reference .env files without reading/committing."

**Pattern needed across all 5 skills:**
- Research: note which services use .env files, document variable NAMES not VALUES
- Design: specify which secrets are needed without including actual values
- Structure: define .env.example templates with placeholder values
- Plan: include "create .env from .env.example" as manual user step
- Implement: reference .env paths, never read .env contents, never include in generated commands

**Red Flag for all services skills:**
- "Reading .env file contents"
- "Including secret values in output"
- "Generating commands that echo/print secrets"

#### 4c. Homelab Plan Repo Configuration
The roadmap specifies: "CLAUDE.md pointer (homelab_repo_path)"

**Open question from concept doc:** "How to reference the homelab plan repo?"
**Roadmap resolution:** CLAUDE.md pointer. Services skills read `homelab_repo_path` from project CLAUDE.md.

**Pattern (similar to vault's MCP config):**
- Check CLAUDE.md for `homelab_repo_path`
- If not found: prompt user to configure it
- If found: use as base path for all file operations on service configs

#### 4d. Dual Source: Repo Files vs Live State
The concept doc asks: "Should research pull live state (docker ps via SSH) or only analyze repo files?"
The roadmap answers: "Repo files for new/planned services, live docker state for already-deployed ones."

**Pattern for /researching-services:**
- Primary source: repo files (compose files, configs, documentation)
- Secondary source: live state commands (docker ps, docker network ls, etc.)
- User executes live-state commands and provides output (hands-off principle)
- OR: if running on the same machine, can run docker commands directly (configurable)

**Gate Function consideration:** Research should check which services are deployed vs planned-only.

#### 4e. Service Health Verification (Linting Equivalent)
Vault has wikilink integrity checks. Services need:

**Post-phase verification for /implementing-services:**
1. Port conflict detection (no two services on same port)
2. Network connectivity verification (services can reach their dependencies)
3. Volume mount validation (paths exist, permissions correct)
4. DNS/proxy route verification (routes resolve correctly)
5. Backup scope coverage (critical data is in backup plan)

**These are SUGGESTIONS, not auto-executed** (hands-off principle). Present as a verification checklist.

### 5. Naming Convention Analysis

The concept doc uses `/services-research`, `/services-design`, etc. The roadmap uses `/researching-services`, `/designing-services`, etc.

**The roadmap's naming is correct** — it follows the established `verb-domain` pattern:
- Code: `/researching-code`, `/designing-code`, `/structuring-code`, `/planning-code`
- Vault: `/researching-vault`, `/designing-vault`, `/structuring-vault`, `/planning-vault`, `/implementing-vault`
- Services: `/researching-services`, `/designing-services`, `/structuring-services`, `/planning-services`, `/implementing-services`

**Note:** `/implementing-plans` (code) is the generic implementation skill. Vault created `/implementing-vault` as a domain-specific version. Services should create `/implementing-services` as a separate domain-specific skill that generates (but doesn't execute) commands.

### 6. File Structure Per Skill (From Patterns)

Based on vault and code precedent, each services skill should have:

```
newskills/researching-services/
├── SKILL.md                                    (~200-250 lines)
├── reference/services-research-aspects.md       (research dimensions)
└── templates/services-research-template.md      (docs-writer output format)

newskills/designing-services/
├── SKILL.md                                    (~195-210 lines)
├── reference/services-design-domains.md         (decision domains + questions)
└── templates/services-design-template.md        (design doc format)

newskills/structuring-services/
├── SKILL.md                                    (~200-220 lines)
├── reference/services-structure-aspects.md      (structural dimensions)
└── templates/services-structural-map-template.md (structural map format)

newskills/planning-services/
├── SKILL.md                                    (~250-300 lines)
├── reference/services-research-workflow.md      (pre-plan research process)
└── templates/services-plan-template.md          (plan body sections)

newskills/implementing-services/
├── SKILL.md                                    (~200-230 lines)
├── reference/services-operations.md             (operation types + command patterns)
└── templates/services-command-template.md       (command output format)
```

**Total: 15 files (5 SKILL.md + 5 reference + 5 templates)**

### 7. Model Usage

Only `/designing-services` should use Opus model (matching `/designing-code` and `/designing-vault`). All other services skills use default Sonnet.

**Rationale:** Architecture decisions (stack topology, networking strategy, auth approach) require deeper reasoning. Research, structure, planning, and implementation are more procedural.

### 8. Domain-Specific Research Dimensions

`/researching-services` should investigate these aspects (parallel to vault research aspects):

| Aspect | What to Map | Source |
|--------|-------------|--------|
| Service Inventory | Running services, images, versions | Compose files + live state |
| Port Mapping | Host:container port bindings, conflicts | Compose files |
| Network Topology | Docker networks, inter-service connectivity | Compose files + network ls |
| Volume Mapping | Bind mounts, named volumes, data locations | Compose files |
| Environment Config | .env file locations, variable NAMES (not values) | .env.example files |
| Reverse Proxy Routes | Domains, paths, SSL certs, middleware | Proxy config files |
| Dependencies | Service startup order, health checks, shared DBs | Compose depends_on + health |
| Backup Coverage | What's backed up, schedule, destinations | Backup configs |
| Resource Usage | CPU/memory limits, actual usage | Compose limits + stats |
| Gaps & Risks | Missing backups, exposed ports, no health checks | Cross-referencing above |

### 9. Domain-Specific Design Domains

`/designing-services` should cover these decision areas:

| Domain | Decisions | Example Questions |
|--------|-----------|-------------------|
| Stack Topology | Service additions/removals, grouping | "Separate DB per app or shared PostgreSQL?" |
| Networking Strategy | Network isolation, proxy routing, DNS | "Internal DNS or Docker network aliases?" |
| Auth Approach | SSO, per-service auth, middleware chains | "Forward auth via Traefik or app-level auth?" |
| Data Management | Volume strategy, backup policy, retention | "Backup volumes only or full state snapshots?" |
| Update Strategy | Image pinning, rollback plan, testing | "Pin exact versions or use semver ranges?" |
| Monitoring | Health checks, alerting, dashboards | "Uptime Kuma or Prometheus+Grafana?" |

### 10. Domain-Specific Structural Decisions

`/structuring-services` should map:

| Element | What to Decide | Output |
|---------|---------------|--------|
| Compose File Organization | Single vs grouped vs per-service | File tree |
| .env Template Layout | Per-service vs shared, naming convention | .env.example templates |
| Proxy Route Organization | Traefik labels vs file provider, route grouping | Config file structure |
| Volume Directory Layout | Base path, per-service subdirs, permissions | Directory tree |
| Backup Configuration | Script location, schedule config, exclusions | Config file locations |
| Network Definitions | Network names, driver types, subnet planning | Network map |

### 11. Implementation Output Format (Unique to Services)

Unlike code/vault implementation which directly modifies files, `/implementing-services` should output:

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

# Deploy with zero-downtime (if applicable)
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
- [ ] Service is running (`docker compose ps` shows "Up")
- [ ] Service responds on expected port
- [ ] Reverse proxy route works (https://service.domain.com)
- [ ] Health check passes
- [ ] Backup job registered (if applicable)
```

### 12. Open Questions Resolved and Remaining

#### Resolved by Roadmap
| Question | Resolution |
|----------|-----------|
| How to reference homelab plan repo? | CLAUDE.md pointer (`homelab_repo_path`) |
| Repo files vs live state? | Both — repo for planned, live for deployed |
| Naming convention? | `verb-domain`: /researching-services, /designing-services, etc. |

#### Still Open
| Question | Options | Recommendation |
|----------|---------|----------------|
| Integration with monitoring for post-deploy verification? | Reference Uptime Kuma/Prometheus if configured, otherwise manual | Include as optional verification step, not required |
| Services equivalent of /starting-refactors? | Create /starting-services or reuse /starting-refactors | Defer — roadmap says "future consideration: /starting-homelab" |
| Should /implementing-services use /implementing-plans or be standalone? | Standalone (like /implementing-vault) vs wrapper around /implementing-plans | Standalone — deployment commands are fundamentally different from code changes |
| Can services skills run docker commands directly (same machine)? | Yes with user opt-in vs always hands-off | Default hands-off, with CLAUDE.md flag for same-machine execution |

### 13. Build Order

The roadmap specifies "build in order": 7a → 7b → 7c → 7d → 7e.

**Recommended session breakdown (2-3 sessions per roadmap):**

**Session 1:** /researching-services + /designing-services (R + D)
- These are the most complex, with domain-specific research dimensions and design domains
- /designing-services uses opus model, needs careful prompt engineering

**Session 2:** /structuring-services + /planning-services (S + P)
- These follow established patterns more closely
- /planning-services is typically the longest skill (~250-300 lines)

**Session 3:** /implementing-services (I)
- Most domain-unique skill (hands-off deployment)
- Needs careful command generation and rollback patterns
- Includes verification checklist format

### 14. Comparison: Services vs Vault Domain Adaptations

| Adaptation Area | Vault | Services |
|----------------|-------|----------|
| External tool integration | MCP tools (Local REST API) | Docker CLI commands |
| Tool execution model | Direct (MCP calls) | Hands-off (generate, don't run) |
| Data integrity concern | Wikilink integrity | Port conflicts, network connectivity |
| Verification method | MCP-based link verification | User-executed health checks |
| Config location | Vault CLAUDE.md (vault path, MCP config) | Project CLAUDE.md (homelab_repo_path) |
| Linting equivalent | Broken wikilinks, orphan notes, frontmatter | Port conflicts, missing health checks, backup gaps |
| Supporting skills | /starting-vault, /importing-vault | None in scope (future: /starting-homelab) |
| Secrets concern | N/A | .env files must never be read/committed |
| Convention deference | Existing vault patterns | Existing compose/networking patterns |

## Code References

- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:454-494` — Phase 7 specification
- `.docs/future-skills/services-rdspi.md:1-33` — Original concept with open questions
- `~/.claude/skills/brainstorming-services/SKILL.md:1-242` — Already deployed entry point
- `~/.claude/skills/brainstorming-services/reference/services-question-domains.md:1-196` — 5 service domains
- `~/.claude/skills/researching-vault/SKILL.md` — Vault research pattern (203 lines)
- `~/.claude/skills/designing-vault/SKILL.md` — Vault design pattern, opus usage (194 lines)
- `~/.claude/skills/structuring-vault/SKILL.md` — Convention deference + migration sequencing (212 lines)
- `~/.claude/skills/planning-vault/SKILL.md` — Mode detection (structured vs standalone) (264 lines)
- `~/.claude/skills/implementing-vault/SKILL.md` — Vault linting + checkpoint pattern (191 lines)
- `~/.claude/skills/designing-code/SKILL.md:34,110` — Opus model usage pattern
- `~/.claude/skills/implementing-plans/SKILL.md:17-24` — Verification workflow reference
- `~/.claude/skills/implementing-plans/reference/verification-workflow.md:7-19` — Strictest verification pattern

## Architecture Notes

### Pattern: Domain Adaptation Formula
Based on code → vault → services progression, the domain adaptation formula is:
1. Keep the 11-section structure unchanged
2. Keep the enforcement architecture unchanged (Iron Law → Gate → Red Flags → Rationalization → Bottom Line)
3. Keep the artifact chain pattern unchanged (.docs/ output via docs-writer)
4. Adapt the Process Steps section for domain-specific operations
5. Add domain-specific sections as needed (e.g., "Wikilink Integrity" for vault, "Hands-Off Deployment" for services)
6. Create domain-specific reference files (research aspects, design domains, operations)
7. Create domain-specific templates (artifact output formats)

### Pattern: Escalating Evidence Requirements
Evidence strictness increases through the BRDSPI chain:
- Research: file:line references
- Design: research artifact links + decision rationale
- Structure: current vs proposed comparison
- Plan: file references + verification commands
- Implementation: command output + exit codes (services: user-reported verification results)

### Key Decision: /implementing-services as Standalone
Unlike code (which uses generic /implementing-plans) and vault (which created /implementing-vault), services MUST have a standalone implementation skill because:
1. It generates commands instead of executing them
2. Verification depends on user-reported results
3. Rollback commands must accompany deploy commands
4. The workflow is fundamentally "generate → present → user runs → user reports → verify"

## Open Questions — ALL RESOLVED

These questions were answered during implementation (see `.docs/plans/02-08-2026-phase-7-services-brdspi-skills.md` lines 96-104). All resolutions have been built into the 5 deployed skills.

### Question 1: Same-Machine Mode
**Original**: Should /implementing-services include a "same-machine mode" where docker commands CAN be auto-executed (opt-in via CLAUDE.md flag)?

**Resolution**: YES — Implemented as `homelab_same_machine: true` in CLAUDE.md
- When enabled: read-only docker commands (`ps`, `logs`, `network ls`, `stats`) auto-execute for verification
- When disabled (default): all commands generated but never auto-executed
- Write commands (`up`, `down`, `pull`, `restart`) NEVER auto-execute in any mode
- See `~/.claude/skills/implementing-services/SKILL.md` lines 26, 34, 38, 48, 99-128, 238-244 for implementation

### Question 2: Monitoring Integration
**Original**: Should monitoring integration (Uptime Kuma, Prometheus) be a reference file or deferred to a future /monitoring-services skill?

**Resolution**: OPTIONAL VERIFICATION STEP — Not a hard requirement
- Services skills reference monitoring tools if user has them configured
- Included as optional checklist items in `/implementing-services` verification section
- Deferred in roadmap as "future consideration: /monitoring-services"
- See `.docs/plans/02-08-2026-phase-7-services-brdspi-skills.md` line 101

### Question 3: Compose Version Compatibility
**Original**: Should the services skills assume a specific compose file version or be version-agnostic?

**Resolution**: VERSION-AGNOSTIC — Accept both `docker-compose` and `docker compose`
- Skills written to work with either form of the docker compose command
- Maximizes compatibility across different development/homelab environments
- See `.docs/plans/02-08-2026-phase-7-services-brdspi-skills.md` line 102

### Question 4: Multi-Host Deployments
**Original**: How should multi-host deployments be handled (single Docker host vs Docker Swarm vs Kubernetes)?

**Resolution**: SINGLE DOCKER HOST ONLY — Multi-host out of scope
- Skills assume single-machine Docker installation
- Docker Swarm and Kubernetes support deferred to future phases/skills
- See `.docs/plans/02-08-2026-phase-7-services-brdspi-skills.md` line 103

---

## Phase 7 Implementation Summary

All findings from this research document were implemented as 5 complete BRDSPI skills (15 files: 5 SKILL.md + 5 reference + 5 templates) deployed to `~/.claude/skills/` and tracked in `newskills/`:

### Skills Deployed
| Skill | Location | Size | Status |
|-------|----------|------|--------|
| /researching-services | `~/.claude/skills/researching-services/` | 9.3 KB | Deployed |
| /designing-services | `~/.claude/skills/designing-services/` | 8.9 KB | Deployed |
| /structuring-services | `~/.claude/skills/structuring-services/` | (verified to exist) | Deployed |
| /planning-services | `~/.claude/skills/planning-services/` | (verified to exist) | Deployed |
| /implementing-services | `~/.claude/skills/implementing-services/` | 10.2 KB | Deployed |

### Key Implementations
- ✓ All 5 skills follow the 11-section SKILL.md structure proven by vault BRDSPI
- ✓ Hands-off deployment pattern: /implementing-services generates commands (never executes write commands)
- ✓ Secrets handling: all skills reference .env file NAMES, never read VALUES
- ✓ Same-machine mode: opt-in via `homelab_same_machine: true` in CLAUDE.md
- ✓ Artifact chain: .docs/ output via docs-writer agent with correct tags and references
- ✓ Domain-specific adaptations: research aspects, design domains, structural elements, operation types
- ✓ Verification checklists: health checks, port conflicts, network connectivity, backup coverage

### Full BRDSPI Chain Operational
The complete services domain BRDSPI workflow is now available:
```
/brainstorming-services  → .docs/brainstorm/{topic}.md
→ /researching-services    → .docs/research/MM-DD-YYYY-*.md
→ /designing-services      → .docs/design/MM-DD-YYYY-*.md
→ /structuring-services    → .docs/structure/MM-DD-YYYY-*.md
→ /planning-services       → .docs/plans/MM-DD-YYYY-*.md
→ /implementing-services   → edits repo files + generates commands
```

### This Document's Purpose
This research document captured the discovery and analysis process that led to Phase 7 implementation. It serves as a historical record of:
- How the domain-specific BRDSPI pattern was adapted from code → vault → services
- The enforcement architecture and 11-section structure used across all skills
- The artifact chain pattern and docs-writer integration
- The unique services domain constraints (hands-off deployment, secrets handling)
- Research dimensions, design domains, and structural decisions
- How each open question was resolved during implementation

Reference this document to understand the rationale behind the services BRDSPI design and implementation choices.
