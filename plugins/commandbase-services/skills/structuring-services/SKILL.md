---
name: structuring-services
description: "Use this skill when mapping file placement, compose organization, and configuration structure for homelab service changes. This includes deciding compose file layout, .env template structure, proxy route organization, volume directory layout, backup configuration placement, and network definitions. Activate when the user says 'structure services', 'organize compose files', 'where should configs go', or after completing design with /designing-services."
---

# Structuring Services

You are mapping file placement, compose organization, and configuration structure for homelab services by analyzing design decisions and current repo organization, then producing a structural map document.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO STRUCTURE WITHOUT UNDERSTANDING WHAT EXISTS
```

Structure decisions must be grounded in the actual repo. Use file-system tools to verify current repo organization before proposing changes.

**No exceptions:**
- Don't propose file locations without checking current repo patterns
- Don't ignore existing conventions in an established homelab repo
- Don't include implementation details in the structural map
- Don't create migration steps that leave services unreachable between steps

## The Gate Function

```
BEFORE writing any structural map:

1. READ: Find and read design doc (.docs/design/) if available
2. CONFIGURE: Check CLAUDE.md for homelab_repo_path
3. RESEARCH: Use file-system tools to map current repo organization (compose files, config dirs, .env files)
4. ANALYZE: Compare design decisions to current file structure
5. MAP: Determine file layout, config placement, naming conventions
6. WRITE: Create .docs/structure/ document via docs-writer
7. PRESENT: Summary to user with structural map and link

Skipping steps = structuring blind
```

## Initial Response

When this skill is invoked:

### If a design doc is provided or referenced:
- Read the design doc FULLY
- Proceed to Step 2

### If no design doc but user provides requirements directly:
- Proceed in lightweight mode (skip design doc lookup)
- Note: structural maps without design docs are valid for simple infrastructure

### If no parameters provided:
```
I'll help you map file layout and config organization for your services.

Please provide:
1. A design document (.docs/design/) or infrastructure description
2. The target repo (homelab_repo_path from CLAUDE.md or current directory)

I'll analyze current structure and create a map showing where everything goes.
```

## Process Steps

### Step 1: Gather Context

- Check for design doc in `.docs/design/` with services tags — read FULLY if exists
- Check for brainstorm doc in `.docs/brainstorm/` — note infrastructure philosophy preferences
- Read CLAUDE.md for `homelab_repo_path`
- If user provides a target area directly, note it for exploration scoping

### Step 2: Analyze Current Structure

Use file-system tools to understand what exists in the repo:

- `Glob("**/docker-compose*.yml", path=repo_path)` — find all compose files
- `Glob("**/compose*.yml", path=repo_path)` — find v2-style compose files
- `Glob("**/.env*", path=repo_path)` — find all .env files (locations only)
- `Glob("**/traefik/**", path=repo_path)` — find proxy configs
- `Glob("**/nginx/**", path=repo_path)` — find nginx configs
- `Glob("**/backup*", path=repo_path)` — find backup configs
- Read sample compose files to understand conventions in use

For complex repos, spawn `general-purpose` agents to explore different areas in parallel.

Wait for ALL exploration to complete before proceeding.

Compile findings:
- Current file organization pattern (single compose vs per-service dirs)
- Naming conventions in use
- Config file locations
- .env file patterns
- Volume mount base paths
- Network definitions

### Step 3: Create Structural Map

For each organizational decision from the design doc (or user requirements):

**Compose file organization:**
- Single file vs grouped by function vs per-service directories
- Where each service definition lives
- How override files are used (docker-compose.override.yml)

**.env template layout:**
- Per-service vs shared .env.example files
- Naming convention (.env.example, .env.sample, env.template)
- Variable naming patterns (SERVICE_VAR vs generic)
- Placeholder value format (CHANGE_ME, your_value_here)

**Proxy route organization:**
- Traefik labels in compose vs file provider configs
- Route grouping (per-service files, single dynamic config)
- SSL certificate configuration location

**Volume directory layout:**
- Base path for persistent data (/opt/docker, /srv, ~/docker)
- Per-service subdirectories
- Permission requirements
- Separation of config vs data vs logs

**Backup configuration:**
- Backup script location
- Schedule config location (cron, systemd timers)
- Exclusion list placement
- Backup destination configuration

**Network definitions:**
- Network names and their purposes
- Which compose file defines shared networks
- Driver types (bridge, overlay)

**Convention deference:**
- For established repos: follow existing patterns where they don't conflict with design
- For new repos: propose conventions and confirm with user via AskUserQuestion

### Step 4: Sequence Migrations (Reorganizations Only)

For infrastructure reorganizations, determine migration order:
- Each step must leave all services reachable (no downtime between steps)
- Each step must preserve service connectivity — when moving configs, update all references
- Prefer changes that don't require service restarts first
- Number each step with a description of what changes and what still works after

**Critical services concern:** Every config file move or rename must account for service references. Identify which services reference the moved file and plan updates.

### Step 5: Write Structural Map

Spawn a `docs-writer` agent via the Task tool:

```
Task prompt:
  doc_type: "structure"
  topic: "<infrastructure purpose>"
  tags: [services, <relevant aspect tags>]
  references: [<design doc, key repo paths>]
  content: |
    <compiled structural map using ./templates/services-structural-map-template.md>
```

The structural map must contain:
- File tree visualization (current and proposed)
- Config placement rules per service type
- .env.example templates with placeholder values only
- Naming conventions
- Migration steps (reorganizations only)
- NO implementation details — no compose YAML syntax, no actual config content

### Step 6: Present and Suggest Next Step

```
STRUCTURE COMPLETE
==================

Structural map: .docs/structure/MM-DD-YYYY-<topic>.md

Compose files: [count and organization pattern]
Config directories: [count of service config dirs]
Migration steps: [count, if reorganization]

Next: /planning-services to break this into phased implementation tasks
```

## Important Guidelines

1. **Structure captures WHERE, not WHAT** — file layout and config placement, no implementation details
2. **Research current patterns** — explore with tools before proposing anything
3. **Defer to conventions** — in established repos, follow what exists where possible
4. **Every migration step must preserve reachability** — no service downtime in intermediate states
5. **.env.example only** — structural maps include .env templates with placeholder values, never real secrets

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Research

If you notice any of these, pause:

- Proposing file structure without exploring current repo patterns
- Ignoring existing conventions in an established repo
- Including implementation details (compose YAML, config syntax) in the structural map
- Creating migration steps that leave services unreachable between steps
- Assuming repo structure without using tools to verify
- Proposing new conventions in an established repo without acknowledging existing ones
- Including actual secret values in .env.example templates

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know the standard Docker layout" | THIS repo has its own patterns. Research them. |
| "The design doc already specifies structure" | Design says WHAT architecture. Structure says WHERE files go. Different concerns. |
| "Migration order doesn't matter" | Every step must preserve service reachability. Order is the hard problem. |
| "This is too simple for a structural map" | Simple structures still need documenting for the planning phase. |
| "I can see the directory layout" | Explore with tools. Directory layout alone doesn't reveal service dependencies. |

## The Bottom Line

**Structure captures WHERE everything goes, not WHAT it does.**

File layout, config placement, naming conventions. Defer to existing patterns in established repos. Preserve service reachability in every migration step. .env templates use placeholders only.

This is non-negotiable. Every structure. Every time.
