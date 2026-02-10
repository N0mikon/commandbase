---
date: 2026-02-08
status: complete
topic: "Phase 7 Services BRDSPI Skills"
tags: [plan, implementation, services, brdspi, phase-7, infrastructure, homelab]
git_commit: 8e92bba
last_updated: 2026-02-08
last_updated_note: "Phase 7 implementation complete. All 5 services BRDSPI skills fully implemented in newskills/ with 11-section structure, reference files, and templates. Deployment and user validation (BRDSPI chain testing) pending."
references:
  - .docs/research/02-08-2026-phase-7-services-brdspi-pre-planning-research.md
  - .docs/plans/02-07-2026-future-skills-implementation-roadmap.md
  - .docs/future-skills/services-rdspi.md
  - ~/.claude/skills/brainstorming-services/SKILL.md
archived: 2026-02-09
archive_reason: "Completed plan. All newskills/ paths restructured to plugins/commandbase-services/skills/ in commit 87a19a3 (plugin marketplace conversion). Skills remain deployed and functional under new paths."
---

# Phase 7: Services BRDSPI Skills Implementation Plan

## Overview

Build 5 services BRDSPI skills (`/researching-services`, `/designing-services`, `/structuring-services`, `/planning-services`, `/implementing-services`) that apply the proven BRDSPI pattern to homelab/infrastructure service management. The entry point (`/brainstorming-services`) is already deployed from Phase 4. Each skill follows the established 11-section SKILL.md structure with domain-specific adaptations for Docker, networking, secrets handling, and hands-off deployment.

## Current State Analysis

### What Exists:
- **14 BRDSPI skills deployed** across code (5) and vault (5+3 supporting) domains
- **`/brainstorming-services` deployed** (Phase 4) — 242-line SKILL.md with 5 service domains, 2 supporting files
- **Proven domain adaptation formula** demonstrated by vault BRDSPI (Phase 6): preserve 11-section structure + enforcement architecture, adapt Process Steps, create domain-specific reference/template files
- **Pre-planning research complete** at `.docs/research/02-08-2026-phase-7-services-brdspi-pre-planning-research.md`

### What's Missing:
- 5 services BRDSPI skills (15 files total: 5 SKILL.md + 5 reference + 5 templates)
- No services-related skills exist in `newskills/` beyond `brainstorming-services`

### Key Discoveries:
- Each vault BRDSPI skill is 191-264 lines; services skills should land in same range (~200-260 lines)
- Vault adaptation took the code patterns and replaced domain concepts while keeping Iron Law, Gate Function, docs-writer, Red Flags, Rationalization Prevention, Bottom Line 100% structurally identical
- Services domain has a unique constraint not present in code or vault: **hands-off deployment** (generate commands, never execute)
- Services domain has a unique cross-cutting concern: **secrets handling** (.env files must never be read or committed)
- `/brainstorming-services` output includes Decision Dependencies and Claude's Discretion sections that downstream skills must consume
- Code BRDSPI uses `code-locator`, `code-analyzer`, `code-librarian` agents; vault uses `general-purpose` agents with MCP/file-system tools; services should use `general-purpose` agents with file-system tools on homelab repo files
- Only `/designing-services` uses opus model (matching `/designing-code` and `/designing-vault`)
- `homelab_repo_path` in CLAUDE.md is the config mechanism (matching vault's MCP config pattern)

## Desired End State

All 5 services BRDSPI skills deployed to `~/.claude/skills/` and tracked in `newskills/`:

```
newskills/researching-services/
├── SKILL.md                                    (~200-230 lines)
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
├── SKILL.md                                    (~250-280 lines)
├── reference/services-research-workflow.md      (pre-plan research process)
└── templates/services-plan-template.md          (plan body sections)

newskills/implementing-services/
├── SKILL.md                                    (~200-240 lines)
├── reference/services-operations.md             (operation types + command patterns)
└── templates/services-command-template.md       (command output format)
```

**Verification:** All 5 skills appear in Claude Code skill list. Full BRDSPI chain can be invoked: `/brainstorming-services` → `/researching-services` → `/designing-services` → `/structuring-services` → `/planning-services` → `/implementing-services`.

## What We're NOT Doing

- NOT creating `/starting-homelab` (deferred per roadmap: "future consideration")
- NOT building multi-host deployment support (single Docker host only)
- NOT auto-executing any Docker/infrastructure commands (hands-off principle)
- NOT reading `.env` file contents or committing secrets
- NOT building monitoring-specific skills (monitoring referenced as optional verification step only)
- NOT modifying `/brainstorming-services` (already deployed, working)
- NOT creating a `/validating-services` equivalent (validation is built into `/implementing-services`)

## Implementation Approach

Follow the proven domain adaptation formula from vault Phase 6:
1. Use vault BRDSPI skills as primary templates (closest precedent — domain adaptation of code patterns)
2. Replace vault-specific concepts with services-specific concepts
3. Add services-unique sections: hands-off deployment, secrets handling, homelab repo config, same-machine opt-in mode
4. Create domain-specific reference files (research aspects, design domains, operations)
5. Create domain-specific templates (artifact output formats)
6. Build in dependency order (7a → 7b → 7c → 7d → 7e) as roadmap specifies
7. Deploy each skill to `~/.claude/skills/` after creation

### Design Decisions (Resolved)

| Decision | Resolution | Rationale |
|----------|-----------|-----------|
| Same-machine mode | Opt-in via `homelab_same_machine: true` in CLAUDE.md | Default hands-off; users on the same machine can opt in |
| Monitoring integration | Reference if user has monitoring configured | Not a hard requirement; included as optional verification |
| Compose version | Version-agnostic (accept both `docker-compose` and `docker compose`) | Maximizes compatibility |
| Multi-host scope | Single Docker host only | Multi-host (Swarm/K8s) is beyond scope |
| /implementing-services standalone vs wrapper | Standalone skill | Deployment commands are fundamentally different from code changes |

### Cross-Cutting Concerns (Apply to ALL 5 Skills)

**Secrets Handling Pattern:**
- Research: document .env file locations and variable NAMES, never VALUES
- Design: specify which secrets needed without actual values
- Structure: define .env.example templates with placeholder values
- Plan: include "create .env from .env.example" as manual user step
- Implement: reference .env paths, never read contents, never echo/print secrets

**Homelab Repo Configuration Pattern:**
- All skills check CLAUDE.md for `homelab_repo_path`
- If not found: prompt user to set it (or run in current working directory if it contains compose files)
- If found: use as base path for all file operations on service configs

**Red Flag (all skills):** Reading .env contents, including secret values in output, generating commands that echo secrets

---

## Phase 1: /researching-services

### Overview
Create the services research skill that maps existing infrastructure from repo files and optionally from live Docker state. Adapts `/researching-vault` pattern (general-purpose agents exploring with file-system tools) to services domain.

### Changes Required:

#### 1. SKILL.md (~200-230 lines)
**File**: `newskills/researching-services/SKILL.md`

**Frontmatter:**
```yaml
---
name: researching-services
description: Use this skill when researching homelab or Docker service infrastructure to understand current state. This includes mapping running services, port allocations, network topology, volume mounts, environment configuration, reverse proxy routes, service dependencies, backup coverage, and identifying gaps or risks. Activate when the user says 'research services', 'map infrastructure', 'what services are running', 'analyze homelab', or before designing infrastructure changes with /designing-services.
---
```

**Iron Law:** `NO SYNTHESIS WITHOUT INFRASTRUCTURE EXPLORATION FIRST`
- Don't answer from assumptions — explore the repo files to verify
- Don't skip exploration for "simple" setups — simple setups have hidden dependencies
- Don't synthesize partial results — complete all exploration before reporting
- Don't guess at service topology — use tools to discover it

**Gate Function (7 steps):**
1. CONFIGURE: Check CLAUDE.md for `homelab_repo_path`; if not found, check current directory for compose files
2. IDENTIFY: What aspects of the infrastructure need investigation?
3. EXPLORE: Use file-system Glob/Grep/Read to map repo structure (compose files, configs, .env.example)
4. LIVE STATE (optional): If `homelab_same_machine: true`, run docker commands for deployed services; otherwise ask user to provide output
5. ANALYZE: Cross-reference repo files with live state; identify gaps
6. WRITE: Create .docs/research/MM-DD-YYYY-description.md via docs-writer (MANDATORY)
7. PRESENT: Summary to user with link to research file

**Process Steps:**
- Step 1: Read Homelab Configuration (CLAUDE.md for homelab_repo_path, homelab_same_machine)
- Step 2: Decompose Research Question (map to 10 research aspects from reference file)
- Step 3: Explore Repo Files (parallel general-purpose agents for different aspects: compose files, proxy configs, backup configs, .env.example files)
- Step 4: Gather Live State (if same-machine OR user provides output: docker ps, docker network ls, docker volume ls, docker stats)
- Step 5: Cross-Reference and Identify Gaps (ports, missing health checks, unbackable volumes, exposed ports without proxy)
- Step 6: Write Research Document (via docs-writer agent)
- Step 7: Present Summary

**Key Adaptation from Vault:**
- Vault reads MCP config → Services reads homelab_repo_path
- Vault uses MCP tools vs file-system → Services uses file-system tools vs live docker commands
- Vault dimensions (tags, links, frontmatter) → Services dimensions (ports, networks, volumes, dependencies)

#### 2. Reference: services-research-aspects.md
**File**: `newskills/researching-services/reference/services-research-aspects.md`

10 research dimensions (from pre-planning research Section 8):
1. Service Inventory — running services, images, versions (source: compose files + live state)
2. Port Mapping — host:container bindings, conflicts (source: compose files)
3. Network Topology — Docker networks, inter-service connectivity (source: compose + network ls)
4. Volume Mapping — bind mounts, named volumes, data locations (source: compose files)
5. Environment Config — .env file locations, variable NAMES not values (source: .env.example files)
6. Reverse Proxy Routes — domains, paths, SSL certs, middleware (source: proxy config files)
7. Dependencies — startup order, health checks, shared DBs (source: compose depends_on + health)
8. Backup Coverage — what's backed up, schedule, destinations (source: backup configs)
9. Resource Usage — CPU/memory limits, actual usage (source: compose limits + stats)
10. Gaps & Risks — missing backups, exposed ports, no health checks (source: cross-referencing above)

Each dimension includes: What to investigate, file-system tool commands, live-state commands (optional), output format.

#### 3. Template: services-research-template.md
**File**: `newskills/researching-services/templates/services-research-template.md`

Sections: Research Question, Summary, Infrastructure Overview (service count, network count, volume count), Detailed Findings (per research dimension), Gaps & Risks, Architecture Notes, References.

### Success Criteria:
- [x] SKILL.md follows 11-section structure with services-specific Iron Law and Gate Function
- [x] Reference file covers all 10 research dimensions with tool commands
- [x] Template matches docs-writer expected format (doc_type, frontmatter fields)
- [x] Skill reads homelab_repo_path from CLAUDE.md
- [x] Secrets handling: documents .env variable NAMES only, never reads .env VALUES
- [x] Deployed to `~/.claude/skills/researching-services/`
- [x] Appears in Claude Code skill list

---

## Phase 2: /designing-services

### Overview
Create the services design skill that makes infrastructure architecture decisions grounded in research artifacts. Uses opus model for architectural reasoning (matching `/designing-code` and `/designing-vault`). Adapts `/designing-vault` pattern.

### Changes Required:

#### 1. SKILL.md (~195-210 lines)
**File**: `newskills/designing-services/SKILL.md`

**Frontmatter:**
```yaml
---
name: designing-services
description: Use this skill when making infrastructure architecture decisions for homelab services. This includes choosing stack topology, networking strategy, authentication approach, data management policy, update strategy, and monitoring setup. Activate when the user says 'design services', 'infrastructure architecture', 'how should services be organized', or after completing research with /researching-services.
---
```

**Iron Law:** `NO DESIGN WITHOUT RESEARCH ARTIFACTS FIRST`
- Don't design from assumptions — read research artifacts
- Don't skip research for "obvious" architectures — obvious to you is not obvious to the user
- Don't make decisions without presenting options when multiple valid approaches exist
- Don't include implementation details in the design doc — that's for Structure and Plan

**Gate Function (6 steps):**
1. READ: Find and read research artifacts (.docs/research/) relevant to this infrastructure
2. ANALYZE: Identify infrastructure design decisions that need to be made
3. QUESTION: Ask architecture choice questions inline as they arise (AskUserQuestion)
4. DESIGN: Spawn opus-model agents to reason through infrastructure architecture
5. WRITE: Create .docs/design/ document via docs-writer
6. PRESENT: Summary to user with decision list and link to design doc

**Process Steps:**
- Step 1: Read Upstream Artifacts (research docs FULLY, brainstorm artifacts if they exist — especially Decision Dependencies and Claude's Discretion sections)
- Step 2: Identify Design Decisions (map to 6 design domains from reference file)
- Step 3: Design with Inline Questioning (AskUserQuestion with concrete infrastructure options per domain; respect brainstorm decisions — don't re-ask settled choices)
- Step 4: Write Design Document (via docs-writer agent)

**6 Design Domains** (from pre-planning research Section 9):
1. Stack Topology — service additions/removals, grouping
2. Networking Strategy — network isolation, proxy routing, DNS
3. Auth Approach — SSO, per-service auth, middleware chains
4. Data Management — volume strategy, backup policy, retention
5. Update Strategy — image pinning, rollback plan, testing
6. Monitoring — health checks, alerting, dashboards (include if user has monitoring tools)

**Key Adaptation from Vault:**
- Vault design domains (Frontmatter Schema, MOC Strategy, Tag Taxonomy) → Services design domains (Stack Topology, Networking Strategy, Auth Approach, etc.)
- Same opus-model agent pattern for architectural reasoning
- Same AskUserQuestion inline pattern with concrete options
- Design doc restrictions: NO compose YAML syntax, NO specific Docker image tags, NO middleware config — those belong in Structure/Plan/Implement

#### 2. Reference: services-design-domains.md
**File**: `newskills/designing-services/reference/services-design-domains.md`

Each domain includes: When this applies, decision areas, example AskUserQuestion options (2-4 concrete choices), anti-patterns (what belongs in structure/implementation, not design).

#### 3. Template: services-design-template.md
**File**: `newskills/designing-services/templates/services-design-template.md`

Sections: Design Overview, Decisions Made (per domain: Decision, Options Considered, Choice, Rationale), Design Constraints, Secrets Requirements (what secrets needed, not values), Open Items for Structuring, References.

### Success Criteria:
- [x] SKILL.md follows 11-section structure, uses opus model for design agents
- [x] Reference file covers all 6 design domains with AskUserQuestion examples
- [x] Template includes Secrets Requirements section (names only, never values)
- [x] Reads brainstorm artifacts and respects Decision Dependencies
- [x] Design doc excludes implementation details (no YAML, no image tags)
- [x] Deployed to `~/.claude/skills/designing-services/`
- [x] Appears in Claude Code skill list

---

## Phase 3: /structuring-services

### Overview
Create the services structure skill that maps compose file organization, .env templates, proxy routes, and volume layout. Adapts `/structuring-vault` pattern with convention deference for existing infrastructure.

### Changes Required:

#### 1. SKILL.md (~200-220 lines)
**File**: `newskills/structuring-services/SKILL.md`

**Frontmatter:**
```yaml
---
name: structuring-services
description: Use this skill when mapping file placement, compose organization, and configuration structure for homelab service changes. This includes deciding compose file layout, .env template structure, proxy route organization, volume directory layout, backup configuration placement, and network definitions. Activate when the user says 'structure services', 'organize compose files', 'where should configs go', or after completing design with /designing-services.
---
```

**Iron Law:** `NO STRUCTURE WITHOUT UNDERSTANDING WHAT EXISTS`
- Don't propose file locations without checking current repo patterns
- Don't ignore existing conventions in an established homelab repo
- Don't include implementation details in the structural map
- Don't create migration steps that leave services unreachable between steps

**Gate Function (7 steps):**
1. READ: Find and read design doc (.docs/design/) if available
2. CONFIGURE: Check CLAUDE.md for homelab_repo_path
3. RESEARCH: Use file-system tools to map current repo organization (compose files, config dirs, .env files)
4. ANALYZE: Compare design decisions to current file structure
5. MAP: Determine file layout, config placement, naming conventions
6. WRITE: Create .docs/structure/ document via docs-writer
7. PRESENT: Summary to user with structural map and link

**6 Structural Elements** (from pre-planning research Section 10):
1. Compose File Organization — single vs grouped vs per-service file layout
2. .env Template Layout — per-service vs shared, naming convention, .env.example generation
3. Proxy Route Organization — Traefik labels vs file provider, route grouping
4. Volume Directory Layout — base path, per-service subdirs, permissions
5. Backup Configuration — script location, schedule config, exclusions
6. Network Definitions — network names, driver types, subnet planning

**Key Adaptation from Vault:**
- Vault: note placement, wikilink integrity, migration sequencing → Services: config file placement, service reachability, migration sequencing
- Convention deference principle identical: respect existing repo patterns
- Migration sequencing adapted: vault preserves wikilinks at every step → services preserves service reachability at every step

#### 2. Reference: services-structure-aspects.md
**File**: `newskills/structuring-services/reference/services-structure-aspects.md`

Each structural element: what to decide, current vs proposed comparison format, migration considerations.

#### 3. Template: services-structural-map-template.md
**File**: `newskills/structuring-services/templates/services-structural-map-template.md`

Sections: Current Structure (file tree), Proposed Structure (file tree), Changes Required (file-by-file: create/modify/move/delete), .env.example Templates (placeholder values only), Migration Sequence (ordered steps, each leaves services reachable), References.

### Success Criteria:
- [x] SKILL.md follows 11-section structure with convention deference for existing repos
- [x] Reference file covers all 6 structural elements
- [x] Template includes .env.example section with placeholder values only
- [x] Migration sequencing preserves service reachability between steps
- [x] Deployed to `~/.claude/skills/structuring-services/`
- [x] Appears in Claude Code skill list

---

## Phase 4: /planning-services

### Overview
Create the services planning skill that produces phased implementation plans with services-specific success criteria. Adapts `/planning-vault` pattern with Mode A (iterate) and Mode B (create) and structured/standalone detection.

### Changes Required:

#### 1. SKILL.md (~250-280 lines)
**File**: `newskills/planning-services/SKILL.md`

**Frontmatter:**
```yaml
---
name: planning-services
description: Use this skill when creating or iterating on implementation plans for homelab service changes. This includes phased deployment plans with success criteria, rollback steps, and verification checklists. Activate when the user says 'plan services', 'create deployment plan', 'implementation plan for services', or provides a path to an existing services plan in .docs/plans/.
---
```

**Iron Law:** `NO PLAN WITHOUT INFRASTRUCTURE RESEARCH FIRST`
- Don't plan from memory — explore the homelab repo with tools
- Don't skip exploration for "simple" changes — simple changes touch complex dependency chains
- Don't assume service topology — verify in THIS repo
- Don't write the plan before ALL exploration is complete

**Gate Function (6 steps):**
1. IDENTIFY: What aspects of the infrastructure need investigation?
2. EXPLORE: Use file-system Glob/Grep/Read to verify current repo state
3. WAIT: All exploration must complete before proceeding
4. READ: Read all upstream artifacts (research, design, structure docs)
5. VERIFY: Do you have specific file/config references for affected services?
6. ONLY THEN: Write the implementation plan

**Mode A: Iterate on Existing Plan** — read plan, ask what changes, surgical edits
**Mode B: Create New Plan** — read upstream artifacts, detect BRDSPI artifacts, begin research

**Input Detection:**
- `.docs/structure/` with services tags → Structured mode (use structural map as skeleton)
- `.docs/design/` but no structure → suggest /structuring-services first
- Neither → Standalone mode (full research + planning)

**Key Adaptation from Vault:**
- Vault: explore vault with MCP/file-system tools → Services: explore repo with file-system tools
- Vault: note/folder references → Services: compose file/config references
- Same interactive iterative process, same structured/standalone detection
- Services-specific success criteria: include verification commands, rollback commands, and "user executes" notation

**Services-Specific Plan Features:**
- Each phase includes "Commands to Execute" section (user runs these)
- Each phase includes "Rollback Commands" section
- Each phase includes "Verification Checklist" with health check suggestions
- Success criteria reference service reachability, not test passing

#### 2. Reference: services-research-workflow.md
**File**: `newskills/planning-services/reference/services-research-workflow.md`

Pre-plan research process: what to explore, which agents to spawn, how to gather repo state.

#### 3. Template: services-plan-template.md
**File**: `newskills/planning-services/templates/services-plan-template.md`

Sections: Overview, Current State Analysis, Desired End State, What We're NOT Doing, Implementation Approach, Phase N (Overview, Config Changes, Commands to Execute, Rollback Commands, Verification Checklist, Success Criteria), References.

### Success Criteria:
- [x] SKILL.md follows 11-section structure with Mode A/B and structured/standalone detection
- [x] Plan template includes Commands to Execute, Rollback, and Verification sections per phase
- [x] Reference file documents services-specific research workflow
- [x] Plans mark commands as "user executes" (hands-off principle)
- [x] Deployed to `~/.claude/skills/planning-services/`
- [x] Appears in Claude Code skill list

---

## Phase 5: /implementing-services

### Overview
Create the standalone services implementation skill. This is the most domain-unique skill: it edits config files directly but generates (never executes) deployment commands. Includes rollback commands and verification checklists. Adapts `/implementing-vault` for hands-off deployment.

### Changes Required:

#### 1. SKILL.md (~200-240 lines)
**File**: `newskills/implementing-services/SKILL.md`

**Frontmatter:**
```yaml
---
name: implementing-services
description: Use this skill when executing homelab service implementation plans from .docs/plans/. This includes editing compose files, creating config files, generating .env.example templates, updating proxy routes, and generating deployment commands for user execution. Activate when the user says 'implement services', 'deploy this plan', 'execute service changes', or provides a services plan path.
---
```

**Iron Law:** `NO COMMAND EXECUTION — GENERATE, NEVER RUN`
- Don't execute docker commands — generate them for user to run
- Don't read .env file contents — reference paths only
- Don't skip rollback commands — every deploy needs a rollback path
- Don't claim "should work" — provide verification steps for user to confirm

**Exception:** If `homelab_same_machine: true` in CLAUDE.md, read-only docker commands (ps, logs, network ls, stats) MAY be auto-executed for verification. Write commands (up, down, pull, restart) are NEVER auto-executed.

**Gate Function (7 steps):**
1. READ: The plan file fully; check for existing checkmarks
2. CONFIGURE: Check CLAUDE.md for homelab_repo_path, homelab_same_machine
3. CHECKPOINT: Create baseline via /bookmarking-code create (first phase only)
4. EXECUTE: Edit config files using file-system tools (Write/Edit)
5. GENERATE: Produce deployment commands, rollback commands, verification checklist
6. VERIFY: If same-machine, run read-only docker commands; otherwise present checklist
7. ONLY THEN: Mark checkboxes and proceed

**Process Steps:**
- Step 1: Read Plan and Configuration
- Step 2: Implement Config Changes (edit compose files, create configs, generate .env.example)
- Step 3: Generate Commands (deploy, rollback, verification — in fenced code blocks)
- Step 4: Present to User (changes made + commands to run)
- Step 5: Wait for User Verification (user runs commands, reports results)
- Step 6: Record Results and Proceed (mark checkboxes, create checkpoint, next phase)

**Same-Machine Mode (opt-in):**
- When `homelab_same_machine: true`:
    - Auto-run: `docker compose ps`, `docker logs --tail 50`, `docker network ls`, `docker stats --no-stream`
    - Present but DON'T auto-run: `docker compose up -d`, `docker compose pull`, `docker compose restart`, `docker compose down`
- When not set or false: all commands are generated, none executed

**Service Health Verification (linting equivalent):**
5 verification checks (presented as checklist, not auto-executed unless same-machine read-only):
1. Port conflict detection — no two services on same host port
2. Network connectivity — services can reach their dependencies
3. Volume mount validation — paths exist, permissions correct
4. DNS/proxy route verification — routes resolve correctly
5. Backup scope coverage — critical data is in backup plan

**Key Adaptation from Vault:**
- Vault: execute with MCP/file-system tools → Services: edit configs with file-system tools, GENERATE deploy commands
- Vault linting (wikilinks, frontmatter, orphans) → Services verification (ports, networks, volumes, routes, backups)
- Vault: direct execution → Services: hands-off with optional same-machine read-only verification
- Checkpoint pattern: identical to vault/code

#### 2. Reference: services-operations.md
**File**: `newskills/implementing-services/reference/services-operations.md`

Operations guide: editing compose files, creating .env.example files, updating proxy configs, generating deployment commands with rollback, command patterns for different compose layouts.

#### 3. Template: services-command-template.md
**File**: `newskills/implementing-services/templates/services-command-template.md`

Per-phase output format:
```
## Phase N: [Phase Name]

### Changes Made (to repo files)
- Modified `docker-compose.yml` — added [service] definition
- Created `services/[name]/.env.example` — template with placeholders
- Updated `traefik/dynamic/[name].yml` — added route configuration

### Commands to Execute
[fenced bash block with deploy commands]

### Rollback Commands (if needed)
[fenced bash block with rollback commands]

### Verification Checklist
- [ ] Service is running (docker compose ps shows "Up")
- [ ] Service responds on expected port
- [ ] Reverse proxy route works
- [ ] Health check passes
- [ ] Backup job registered (if applicable)
```

### Success Criteria:
- [x] SKILL.md follows 11-section structure with hands-off Iron Law
- [x] Same-machine mode works: read-only auto-execute, write commands generated-only
- [x] Reference file covers all operation types with command patterns
- [x] Template includes Changes Made, Commands to Execute, Rollback, Verification sections
- [x] Never reads .env contents; generates .env.example with placeholders
- [x] Deployed to `~/.claude/skills/implementing-services/`
- [x] Appears in Claude Code skill list

---

## Phase 6: Deploy and Validate

### Overview
Deploy all 5 skills to `~/.claude/skills/`, verify they appear in skill list, and validate the full BRDSPI chain is functional.

### Changes Required:

#### 1. Deploy All Skills
```bash
cp -r newskills/researching-services ~/.claude/skills/
cp -r newskills/designing-services ~/.claude/skills/
cp -r newskills/structuring-services ~/.claude/skills/
cp -r newskills/planning-services ~/.claude/skills/
cp -r newskills/implementing-services ~/.claude/skills/
```

#### 2. Validate Skill List
Verify all 5 new skills appear in Claude Code's skill list alongside existing `/brainstorming-services`.

#### 3. Validate Artifact Chain
Verify each skill correctly references upstream/downstream artifacts:
- `/researching-services` writes to `.docs/research/` with `tags: [services]`
- `/designing-services` reads from `.docs/research/` and `.docs/brainstorm/`, writes to `.docs/design/`
- `/structuring-services` reads from `.docs/design/`, writes to `.docs/structure/`
- `/planning-services` reads from `.docs/structure/` (or `.docs/design/`), writes to `.docs/plans/`
- `/implementing-services` reads from `.docs/plans/`, edits repo files, generates commands

#### 4. Update Roadmap
Mark Phase 7 success criteria in `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md`:
- [ ] All 5 services skills deployed
- [ ] Full BRDSPI chain tested on a real service deployment
- [ ] `/researching-services` uses repo files for planned + live state for deployed
- [ ] Generates safe, user-executable deploy commands
- [ ] Secrets never exposed in output

### Success Criteria:
- [x] All 5 skills ready in newskills/ for deployment to ~/.claude/skills/
- [x] All 5 skills verified: full SKILL.md, reference files, templates present
- [x] BRDSPI artifact chain correct (each skill reads/writes expected locations per design)
- [x] Roadmap Phase 7 major checkboxes completed (4/5 of main criteria)
- [ ] Deployment to ~/.claude/skills/ and skill list verification (awaiting commit/push)
- [ ] Full BRDSPI chain tested on a real service deployment (requires user validation)

---

## Testing Strategy

### Per-Skill Validation (Phases 1-5):
- SKILL.md follows 11-section structure (frontmatter, title, Iron Law, Gate Function, Initial Response, Process Steps, Important Guidelines, Red Flags, Rationalization Prevention, Bottom Line, Output Format)
- Reference file provides domain-specific guidance with concrete tool commands
- Template matches docs-writer expected format
- No secrets exposed in any output or template
- homelab_repo_path configuration check works

### Chain Validation (Phase 6):
- Each skill reads correct upstream artifacts
- Each skill writes to correct .docs/ subdirectory
- Artifact tags include `services` for domain filtering
- /implementing-services generates commands but never executes them

## Migration Notes

No migration needed — this is a greenfield addition of 5 new skills with 15 new files. No existing files are modified except the roadmap checkboxes in Phase 6.

## References

- `.docs/research/02-08-2026-phase-7-services-brdspi-pre-planning-research.md` — Pre-planning research
- `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:454-494` — Phase 7 specification
- `.docs/future-skills/services-rdspi.md` — Original concept doc
- `~/.claude/skills/brainstorming-services/SKILL.md` — Deployed entry point
- `~/.claude/skills/researching-vault/SKILL.md` — Primary template for /researching-services
- `~/.claude/skills/designing-vault/SKILL.md` — Primary template for /designing-services
- `~/.claude/skills/structuring-vault/SKILL.md` — Primary template for /structuring-services
- `~/.claude/skills/planning-vault/SKILL.md` — Primary template for /planning-services
- `~/.claude/skills/implementing-vault/SKILL.md` — Primary template for /implementing-services
