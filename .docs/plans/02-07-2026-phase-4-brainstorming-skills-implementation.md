---
date: 2026-02-07
status: draft
topic: "Phase 4 Brainstorming Skills Implementation"
tags: [plan, implementation, brainstorming, phase-4, brdspi, discussing-features, retirement]
git_commit: 0713c81
references:
  - ".docs/research/02-07-2026-phase-4-brainstorming-skills-pre-planning-research.md"
  - ".docs/plans/02-07-2026-future-skills-implementation-roadmap.md"
  - "~/.claude/skills/discussing-features/SKILL.md"
  - "~/.claude/skills/designing-code/SKILL.md"
  - "~/.claude/agents/docs-writer.md"
---

# Phase 4: Brainstorming Skills + `/discussing-features` Retirement — Implementation Plan

## Overview

Build three domain-specific brainstorming skills (`/brainstorming-code`, `/brainstorming-vault`, `/brainstorming-services`) that replace the generic `/discussing-features` skill. Extend the `docs-writer` agent with a `brainstorm` doc_type, update `/designing-code` to consume brainstorm artifacts instead of context artifacts, and archive `/discussing-features` after absorption is confirmed.

This is Phase 4 of the future skills implementation roadmap (roadmap:292-337). It depends on Phase 2 (BRDSPI Core) which is complete.

## Current State Analysis

### What Exists:
- `/discussing-features` — 188-line skill with domain detection (5 types: visual/api/cli/content/organization), 4-question rhythm, topic selection, scope guardrail, and `.docs/context/` output with XML tags (discussing-features/SKILL.md:1-188)
- Supporting files: `reference/question-domains.md` (151 lines), `templates/context-template.md` (93 lines)
- `docs-writer` agent supports 8 doc_types (docs-writer.md:32), maps to `.docs/` subdirectories (docs-writer.md:63-72)
- `/designing-code` reads `.docs/research/` (mandatory) and `.docs/context/` (optional) at lines 47 and 79
- Source of truth copy at `newskills/discussing-features/` in commandbase repo

### What's Missing:
- No brainstorming skills exist (verified: `newskills/brainstorming*` is empty)
- No `brainstorm` doc_type in `docs-writer`
- No `.docs/brainstorm/` directory
- `/designing-code` has no awareness of `.docs/brainstorm/`

### Key Discoveries:
- `/discussing-features` domain detection uses action verbs (SEE/CALL/RUN/READ/ORGANIZE) to classify features — this pattern only applies to `/brainstorming-code`, not vault or services (discussing-features/SKILL.md:62-79)
- The 4-question rhythm, topic selection with `multiSelect: true`, and scope guardrail are universal patterns shared across all three brainstorming skills (discussing-features/SKILL.md:83-123)
- Only `/designing-code` references `.docs/context/` (designing-code/SKILL.md:47,79). No other skill consumes it. Clean replacement target.
- `/starting-projects` and `/starting-refactors` consume no upstream artifacts — they use interactive discovery (starting-projects/SKILL.md:42-48, starting-refactors/SKILL.md:46-58)
- `docs-writer` doc_type additions follow a 3-line pattern: enum list, count, mapping row (docs-writer.md:32,44,63-72)
- Skill template requires 11 sections, target 200-300 lines SKILL.md, reference files with intention-revealing names (creating-skills/SKILL.md:106-108)

## Desired End State

After this plan is complete:
1. Three brainstorming skills deployed to `~/.claude/skills/` and tracked in `newskills/`
2. Each skill is purpose-built for its domain with tailored Iron Law, Gate Function, domain logic, question banks, and output sections
3. `docs-writer` supports `brainstorm` doc_type → `.docs/brainstorm/` directory
4. `/designing-code` reads `.docs/brainstorm/` (optional) instead of `.docs/context/`
5. `/discussing-features` removed from deployed skills, archived in `newskills/discussing-features/` with a note
6. Brainstorm artifacts are programmatically consumed by `/designing-code` in the BRDSPI chain

### Verification:
- Invoke `/brainstorming-code` on a test feature → produces `.docs/brainstorm/` artifact with code-specific direction and preferences
- Invoke `/brainstorming-vault` → produces vault-specific brainstorm artifact
- Invoke `/brainstorming-services` → produces services-specific brainstorm artifact
- Invoke `/designing-code` after brainstorming → reads and incorporates `.docs/brainstorm/` artifact
- `/discussing-features` no longer appears in skill list

## What We're NOT Doing

- **Not building Vault BRDSPI** (Phase 6) or Services BRDSPI (Phase 7) — vault and services brainstorming skills work standalone
- **Not adding codebase research agents to brainstorming** — brainstorming is purely exploratory/conversational; codebase investigation stays in `/researching-code`
- **Not migrating existing `.docs/context/` files** — they're historical artifacts, left in place
- **Not modifying `/starting-projects` or `/starting-refactors`** — they use interactive discovery, brainstorming flows into them via user context
- **Not creating a shared template library** — each skill gets its own self-contained template copy

## Implementation Approach

Build infrastructure first (docs-writer extension), then skills in order of complexity (code absorbs the most from discussing-features, vault and services are greenfield), then update the downstream consumer (/designing-code), and finally retire the replaced skill after all absorption is verified.

Each brainstorming skill is purpose-built for its domain:
- `/brainstorming-code` inherits domain detection (5 action-verb types) and adds codebase-focused direction questions
- `/brainstorming-vault` has entirely different domains (structure, linking, templates, organization, plugins) — no action-verb detection needed
- `/brainstorming-services` has infrastructure domains (stack, compose, networking, backup, dependencies) with interdependent decisions

All three share the structural skeleton (11-section template, 4-question rhythm, scope guardrail) but differ in Iron Law emphasis, Gate Function checks, domain logic, question content, and suggested next steps.

---

## Phase 1: Infrastructure — `docs-writer` Extension

### Overview
Add `brainstorm` as the 9th doc_type to the `docs-writer` agent. This is a prerequisite for all three brainstorming skills since they delegate artifact creation to `docs-writer`.

### Changes Required:

#### 1. `docs-writer` Agent
**File**: `~/.claude/agents/docs-writer.md`
**Changes**: 3-line modification following the Phase 2 pattern

Line 32 — Add `brainstorm` to enum:
```
| `doc_type` | Yes | One of: `research`, `plan`, `handoff`, `reference`, `debug`, `design`, `structure`, `refactor`, `brainstorm` |
```

Line 44 — Update count:
```
- `doc_type` must be one of the 9 valid types
```

After line 72 — Add mapping row:
```
| `brainstorm` | `.docs/brainstorm/` | `draft` |
```

#### 2. Repo Copy
**File**: `newagents/docs-writer.md`
**Changes**: Same 3-line modification, synced from deployed version

### Success Criteria:
- [x] `docs-writer.md` lists 9 valid doc_types including `brainstorm`
- [x] Mapping table has `brainstorm` → `.docs/brainstorm/` → `draft` row
- [x] Repo copy at `newagents/docs-writer.md` matches deployed version

---

## Phase 2: `/brainstorming-code` — Codebase Feature Exploration

### Overview
The most complex skill — absorbs `/discussing-features`' domain detection system, 4-question rhythm, topic selection, and scope guardrail. Adds codebase-focused direction questions. Produces `.docs/brainstorm/` artifacts consumed by `/designing-code`.

### What It Absorbs from `/discussing-features`:
- **Domain detection** (discussing-features/SKILL.md:62-79): 5 types via action verbs (SEE→visual, CALL→api, RUN→cli, READ→content, ORGANIZE→organization)
- **4-question rhythm** (discussing-features/SKILL.md:96-111): Announce topic → 4 AskUserQuestion calls with concrete options → "More or move on?"
- **Topic selection** (discussing-features/SKILL.md:83-93): 3-4 domain-specific topics via `multiSelect: true`, no "skip all" option
- **Scope guardrail** (discussing-features/SKILL.md:113-123): Defer out-of-scope ideas, redirect to current topic, track for artifact
- **Quality checklist** (discussing-features/templates/context-template.md:85-92): 5-item validation before finalizing

### What It Adds Beyond `/discussing-features`:
- **Direction choices**: Higher-level architectural questions ("REST or GraphQL?", "monolith or microservices?", "event-driven or polling?")
- **Explicit next-step guidance**: Suggests `/starting-projects` or `/starting-refactors` as next step based on greenfield vs brownfield
- **Structured artifact for downstream consumption**: `.docs/brainstorm/` format readable by `/designing-code`

### Changes Required:

#### 1. SKILL.md (~200-220 lines)
**File**: `newskills/brainstorming-code/SKILL.md`
**Creates**: New file

Frontmatter:
```yaml
---
name: brainstorming-code
description: "Use this skill when exploring direction and preferences for a code feature before research or planning. This includes discussing layout vs API vs CLI interaction modes, settling high-level architecture direction ('REST or GraphQL?'), capturing user preferences for downstream design phases, and replacing /discussing-features for code-domain brainstorming."
---
```

Key sections tailored for code domain:
- **Iron Law**: `CAPTURE DIRECTION BEFORE RESEARCH` — brainstorming settles "what direction?" not "how to implement?"
- **Gate Function**: (1) Read feature description, (2) Detect domain via action verbs, (3) Select domain-specific topics, (4) Confirm brainstorm scope, (5) ONLY THEN begin questioning
- **Domain Detection**: Inherited 5-type system — analyze feature for action verbs (SEE/CALL/RUN/READ/ORGANIZE), identify primary interaction mode, handle mixed domains
- **Process**: Topic selection (multiSelect) → 4-question rhythm per topic → scope guardrail → artifact creation via docs-writer
- **Output**: `.docs/brainstorm/` artifact via `docs-writer` with `doc_type: "brainstorm"`
- **Next Steps**: Suggests `/starting-projects` (greenfield) or `/starting-refactors` (brownfield) → then RDSPI chain

#### 2. Question Domains Reference (~160-180 lines)
**File**: `newskills/brainstorming-code/reference/question-domains.md`
**Creates**: New file, adapted from `discussing-features/reference/question-domains.md`

Adapts the 5 domain definitions from `/discussing-features` (151 lines) and expands with:
- **Code-specific direction questions** per domain: architecture direction, pattern choices, integration approaches
- **Visual domain additions**: "Dashboard or detail view?", "Realtime updates or refresh?"
- **API domain additions**: "REST or GraphQL?", "Sync or async?", "Webhook or polling?"
- **CLI domain additions**: "Interactive or scripted?", "Single command or subcommands?"
- **Content domain additions**: "Static or dynamic?", "Markdown or rich text?"
- **Organization domain additions**: "Flat or hierarchical?", "Tags or categories?"
- **Mixed domain handling**: Same dominant/secondary pattern
- **Anti-patterns updated**: DON'T ask research-level questions (existing patterns, library choices) — those belong in `/researching-code`. DON'T ask design-level questions (specific API shapes, error handling strategies) — those belong in `/designing-code`. DO ask direction questions (which paradigm, which interaction mode, which organizational approach).

#### 3. Brainstorm Output Template (~60-70 lines)
**File**: `newskills/brainstorming-code/templates/brainstorm-template.md`
**Creates**: New file

```markdown
# Brainstorm Output Template

## File Naming
- Location: `.docs/brainstorm/`
- Format: `{topic-name}.md` (lowercase, hyphens)
- Examples: `user-auth-feature.md`, `export-api.md`, `backup-cli.md`

## Template

---
topic: "[Brainstorm Topic]"
domain: code
sub_domain: [visual|api|cli|content|organization]
date: [YYYY-MM-DD]
status: draft
---

# [Topic] — Brainstorm

## Direction
[High-level direction settled during brainstorming — 2-3 sentences summarizing the overall approach chosen]

## Decisions
### [Topic 1 Name]
- **Choice**: [Specific preference or direction chosen]
- **Rationale**: [Why this direction, in user's words]

### [Topic 2 Name]
- **Choice**: [Specific preference or direction chosen]
- **Rationale**: [Why this direction]

[Continue for each discussed topic]

### Claude's Discretion
[Areas where user said "you decide" — listed so /designing-code knows where it has freedom]
[Or: "User provided specific preferences for all topics."]

## Deferred Ideas
- [Idea that came up but belongs in a separate feature]
[Or: "None."]

## Suggested Next Steps
[Based on greenfield vs brownfield detection:]
- Greenfield: "Consider `/starting-projects` to initialize the workspace, then `/researching-code` → `/designing-code` → `/structuring-code` → `/planning-code` → `/implementing-plans`"
- Brownfield: "Consider `/starting-refactors` to scope the change, then `/researching-code` → `/designing-code` → `/structuring-code` → `/planning-code` → `/implementing-plans`"

## Quality Checklist
- [ ] Each discussed topic has at least one concrete direction choice
- [ ] Decisions are directional, not implementation-specific (no code, no file paths)
- [ ] Scope matches original feature description
- [ ] Deferred ideas captured or explicitly noted as none
- [ ] Sub-domain correctly identified
- [ ] Next steps suggest appropriate initializer skill
```

### Success Criteria:
- [x] `newskills/brainstorming-code/` contains SKILL.md, reference/question-domains.md, templates/brainstorm-template.md
- [x] SKILL.md follows 11-section template, 200-300 line target (218 lines)
- [x] Domain detection covers all 5 types (visual/api/cli/content/organization) with action-verb triggers
- [x] 4-question rhythm, topic selection, and scope guardrail patterns present
- [x] Anti-patterns clearly separate brainstorming from research and design boundaries
- [x] Deploy to `~/.claude/skills/brainstorming-code/` and invoke on a test feature
- [ ] Produces valid `.docs/brainstorm/` artifact with correct frontmatter and sections

---

## Phase 3: `/brainstorming-vault` — Knowledge Management Exploration

### Overview
Vault-specific brainstorming for Obsidian knowledge management decisions. Completely different domain knowledge from code — no action-verb domain detection. Standalone-capable even before Vault BRDSPI (Phase 6) exists.

### Domain-Specific Design:
- **Iron Law**: `CAPTURE VAULT PHILOSOPHY BEFORE BUILDING` — settle organizational philosophy (Zettelkasten vs PARA vs hybrid) before creating any structure
- **Gate Function**: (1) Read vault goal/topic description, (2) Identify which vault domains apply (structure, linking, templates, organization, plugins), (3) Select topics, (4) ONLY THEN begin questioning
- **No action-verb detection**: Vault brainstorming always covers the same 5 vault domains — the question is which ones are relevant, not which type the feature is
- **Vault domains** (fundamentally different from code domains):
  - **Structure**: Folder hierarchy, flat vs nested, MOCs vs indexes, daily notes placement
  - **Linking**: Wikilinks vs markdown links, backlink strategy, link density, hub-and-spoke vs web
  - **Templates**: Templater vs core templates, note types, metadata/frontmatter strategy
  - **Organization**: PARA, Zettelkasten, hybrid, tag taxonomy, naming conventions
  - **Plugins**: Dataview queries, community plugins, minimal vs maximal plugin strategy

### Changes Required:

#### 1. SKILL.md (~180-200 lines)
**File**: `newskills/brainstorming-vault/SKILL.md`
**Creates**: New file

Frontmatter:
```yaml
---
name: brainstorming-vault
description: "Use this skill when exploring direction and preferences for an Obsidian vault before building structure. This includes discussing folder hierarchy vs flat tags, MOC strategies, linking philosophies (Zettelkasten vs PARA vs hybrid), template approaches, and plugin decisions for knowledge management."
---
```

Tailored sections:
- Process uses vault-specific topic selection (structure/linking/templates/organization/plugins) instead of action-verb domain detection
- Questions probe knowledge management philosophy, not code architecture
- Next steps detect whether Vault BRDSPI chain exists: if yes → suggest `/starting-vault`; if no → suggest manual vault work with brainstorm artifact as guide

#### 2. Vault Question Domains Reference (~100-120 lines)
**File**: `newskills/brainstorming-vault/reference/vault-question-domains.md`
**Creates**: New file

Purpose-built question bank for each vault domain:
- **Structure**: "Flat files with tags or nested folder hierarchy?", "One MOC to rule them all or topic-specific hubs?", "Daily notes in root or dated subfolder?"
- **Linking**: "Wikilinks or standard markdown links?", "Aggressive backlinks or curated connections?", "Hub-and-spoke or organic web?"
- **Templates**: "Templater plugin or core templates?", "Strict note types or freeform?", "Frontmatter on every note or only structured notes?"
- **Organization**: "PARA (Projects/Areas/Resources/Archive)?", "Zettelkasten (atomic, linked)?", "Hybrid approach?", "Tag taxonomy — flat or hierarchical?"
- **Plugins**: "Minimal (core only) or maximal (Dataview, Templater, etc.)?", "Community plugins or built-in features?", "Automation or manual workflow?"

#### 3. Brainstorm Output Template (~60-70 lines)
**File**: `newskills/brainstorming-vault/templates/brainstorm-template.md`
**Creates**: New file (same structure as code version, vault-specific frontmatter)

Key difference from code version: `domain: vault`, no `sub_domain` field (vault domains are presented as topics, not detected). Next steps section references Vault BRDSPI availability.

### Success Criteria:
- [x] `newskills/brainstorming-vault/` contains SKILL.md, reference/vault-question-domains.md, templates/brainstorm-template.md
- [x] SKILL.md follows 11-section template, 180-200 line target (221 lines)
- [x] Question domains cover all 5 vault areas (structure, linking, templates, organization, plugins)
- [x] No code-domain concepts leaked into vault skill (no action-verb detection, no API/CLI questions)
- [x] Standalone-capable: works without Vault BRDSPI, suggests manual workflow when downstream chain absent
- [x] Deploy to `~/.claude/skills/brainstorming-vault/` and invoke on a test vault topic
- [ ] Produces valid `.docs/brainstorm/` artifact with `domain: vault`

---

## Phase 4: `/brainstorming-services` — Infrastructure Architecture Exploration

### Overview
Infrastructure brainstorming for homelab/Docker service management. Domain knowledge is about service interdependencies, networking topology, and stack selection. Decisions are often interdependent (reverse proxy choice affects auth, which affects networking).

### Domain-Specific Design:
- **Iron Law**: `CAPTURE STACK DECISIONS BEFORE DEPLOYING` — settle on service stack and topology before writing any compose files
- **Gate Function**: (1) Read infrastructure goal/topic description, (2) Identify which service domains apply (stack, compose, networking, backup, dependencies), (3) Map decision interdependencies, (4) Order topics so dependent decisions come after their prerequisites, (5) ONLY THEN begin questioning
- **Decision interdependency**: Unique to services — choosing Traefik vs Nginx Proxy Manager affects how auth is configured, which affects networking. The gate function must identify and order these dependencies.
- **Service domains** (fundamentally different from code and vault):
  - **Stack Selection**: Which services to run — Authelia vs Cloudflare tunnels, Traefik vs Nginx Proxy Manager, Portainer vs CLI-only
  - **Compose Architecture**: Single compose or per-service compose files, shared networks or isolated, environment variable management
  - **Networking**: Reverse proxy routing, DNS strategy, internal vs external access, VPN/tunnel approach
  - **Backup Strategy**: Borg vs restic, local vs remote vs both, backup frequency, what to include/exclude
  - **Dependencies & Ordering**: Which services depend on which, startup order, health checks, failure cascading

### Changes Required:

#### 1. SKILL.md (~180-200 lines)
**File**: `newskills/brainstorming-services/SKILL.md`
**Creates**: New file

Frontmatter:
```yaml
---
name: brainstorming-services
description: "Use this skill when exploring direction and preferences for homelab or Docker service infrastructure before deployment. This includes discussing reverse proxy choices (Traefik vs Nginx), compose architecture (single vs per-service), backup strategies (Borg vs restic), networking topology, and service dependency ordering."
---
```

Tailored sections:
- Gate function includes dependency mapping step unique to services (e.g., must decide reverse proxy before auth approach)
- Process orders topics by dependency chain, not just user selection
- Questions probe infrastructure decisions with awareness of interdependencies
- Next steps detect whether Services BRDSPI chain exists: if yes → suggest research; if no → suggest manual infrastructure work with brainstorm artifact as guide

#### 2. Services Question Domains Reference (~100-120 lines)
**File**: `newskills/brainstorming-services/reference/services-question-domains.md`
**Creates**: New file

Purpose-built question bank:
- **Stack**: "Authelia or Cloudflare tunnels for auth?", "Traefik or Nginx Proxy Manager?", "Portainer or Docker CLI only?", "Watchtower for auto-updates or manual?"
- **Compose**: "Single docker-compose.yml or per-service files?", "Shared Docker network or isolated per-service?", "`.env` files or Docker secrets?", "Version pinning strategy?"
- **Networking**: "Reverse proxy with SSL termination?", "Internal DNS or Docker DNS?", "Tailscale/WireGuard or Cloudflare tunnels for remote access?", "Exposed ports vs proxy-only?"
- **Backup**: "Borg or restic?", "Local NAS, remote cloud, or both?", "Daily, weekly, or continuous?", "Volumes only or full container state?"
- **Dependencies**: "Which services must start first?", "Health check requirements?", "What happens when a dependency fails — graceful degradation or hard stop?", "Shared databases or per-service?"
- **Interdependency map**: Document which decisions constrain which — e.g., "If Traefik → labels-based routing → affects compose structure"

#### 3. Brainstorm Output Template (~60-70 lines)
**File**: `newskills/brainstorming-services/templates/brainstorm-template.md`
**Creates**: New file (same structure, services-specific frontmatter)

Key difference: `domain: services`, no `sub_domain` field. Includes "Decision Dependencies" section showing which choices constrain downstream decisions. Next steps reference Services BRDSPI availability.

### Success Criteria:
- [x] `newskills/brainstorming-services/` contains SKILL.md, reference/services-question-domains.md, templates/brainstorm-template.md
- [x] SKILL.md follows 11-section template, 180-200 line target (241 lines — larger due to interdependency logic)
- [x] Question domains cover all 5 service areas (stack, compose, networking, backup, dependencies)
- [x] Decision interdependency ordering is built into the gate function and process
- [x] No code or vault concepts leaked into services skill
- [x] Standalone-capable: works without Services BRDSPI
- [x] Deploy to `~/.claude/skills/brainstorming-services/` and invoke on a test infrastructure topic
- [ ] Produces valid `.docs/brainstorm/` artifact with `domain: services`

---

## Phase 5: Update `/designing-code` — Consume Brainstorm Artifacts

### Overview
Update `/designing-code` to read `.docs/brainstorm/` artifacts (optional input) instead of `.docs/context/`. This connects the brainstorming phase to the design phase programmatically.

### Changes Required:

#### 1. Input Requirements Update
**File**: `~/.claude/skills/designing-code/SKILL.md`
**Changes**: Replace `.docs/context/` references with `.docs/brainstorm/`

At line 47 (Initial Response - Research Artifacts Provided):
- Remove: "Also checks `.docs/context/` for feature context from `/discussing-features`"
- Add: "Also checks `.docs/brainstorm/` for direction and preferences from `/brainstorming-code`"

At line 79 (Step 1: Locate and Read Research):
- Remove: "Also checks `.docs/context/` for feature context documents"
- Add: "Also checks `.docs/brainstorm/` for brainstorming artifacts — reads direction choices, user preferences, and Claude's Discretion sections to inform design decisions"

#### 2. Brainstorm Integration Logic
**File**: `~/.claude/skills/designing-code/SKILL.md`
**Changes**: Add guidance on how brainstorm artifacts inform design

In the research reading step, add after the brainstorm check:
- If brainstorm artifact exists: read it to understand user's directional preferences (e.g., "REST not GraphQL"), respect those constraints during design, note "Claude's Discretion" areas where the design phase has freedom
- If no brainstorm artifact: proceed normally (brainstorming is optional in BRDSPI)

#### 3. Repo Copy
**File**: `newskills/designing-code/SKILL.md` (if tracked in commandbase)
**Changes**: Sync from deployed version

### Success Criteria:
- [x] `/designing-code` SKILL.md no longer references `.docs/context/` anywhere
- [x] `/designing-code` SKILL.md references `.docs/brainstorm/` as optional input
- [x] Brainstorm artifact reading logic specifies what sections to consume (Direction, Decisions, Claude's Discretion)
- [x] Design phase respects brainstorm direction choices as constraints
- [x] Repo copy synced if applicable

---

## Phase 6: Retire `/discussing-features`

### Overview
Archive `/discussing-features` after confirming all its functionality has been absorbed by `/brainstorming-code` and `/designing-code`. Remove from deployed skills, keep in repo as archive reference.

### Absorption Verification Checklist:
Before archiving, verify each capability has a new home:

| Capability | Absorbed By | Verified |
|-----------|------------|---------|
| Domain detection (5 types) | `/brainstorming-code` | [x] |
| 4-question rhythm | All 3 brainstorming skills | [x] |
| Topic selection (multiSelect) | All 3 brainstorming skills | [x] |
| Scope guardrail + deferred tracking | All 3 brainstorming skills | [x] |
| Research-informed technical choices | `/designing-code` (Phase 2) | [x] Already done |
| `.docs/context/` artifact creation | Replaced by `.docs/brainstorm/` | [x] |
| Quality checklist | Brainstorm templates | [x] |

### Changes Required:

#### 1. Remove Deployed Skill
**Action**: Delete `~/.claude/skills/discussing-features/` directory (SKILL.md, reference/, templates/)

#### 2. Archive in Repo
**File**: `newskills/discussing-features/SKILL.md`
**Changes**: Add archive notice at top of file:
```markdown
<!-- ARCHIVED: Phase 4 (2026-02-07). Absorbed by /brainstorming-code (domain detection,
preferences) and /designing-code (technical choices). Kept as reference. -->
```

#### 3. Update Cross-References
**Action**: Search all deployed skills for mentions of `/discussing-features` and update:
- Roadmap references — will be updated as part of roadmap maintenance
- No deployed skills currently invoke or depend on `/discussing-features` programmatically

### Success Criteria:
- [x] All rows in absorption verification checklist are checked
- [x] `~/.claude/skills/discussing-features/` directory no longer exists
- [x] `newskills/discussing-features/SKILL.md` has archive notice at top
- [x] No deployed skill references `/discussing-features` as a dependency or suggestion
- [x] `/brainstorming-code` description includes trigger phrases that catch habitual `/discussing-features` users (e.g., "for feature discussions")

---

## Testing Strategy

### Per-Skill Validation:
- Invoke each brainstorming skill with a representative topic
- Verify 4-question rhythm fires correctly with concrete options via AskUserQuestion
- Verify topic selection uses multiSelect
- Verify scope guardrail activates on out-of-scope input
- Verify artifact is created in `.docs/brainstorm/` with correct frontmatter

### Chain Integration:
- Run `/brainstorming-code` → `/designing-code` and verify design phase reads brainstorm artifact
- Confirm brainstorm direction choices appear as constraints in design output
- Confirm "Claude's Discretion" areas give design phase freedom

### Domain Isolation:
- Verify `/brainstorming-vault` asks no code-specific questions
- Verify `/brainstorming-services` asks no vault-specific questions
- Verify `/brainstorming-code` domain detection works for all 5 types

### Retirement Verification:
- After removing `/discussing-features`, verify no skill errors or broken references
- Verify `/brainstorming-code` catches users who type "discuss" or "discussing" in their intent

## Migration Notes

- Existing `.docs/context/` files are left in place as historical artifacts — no migration needed
- Users who habitually invoke `/discussing-features` will be caught by `/brainstorming-code`'s description which includes "for feature discussions" and "replaces /discussing-features"
- The brainstorming → design flow is optional — RDSPI chain still works without brainstorming (backward compatible)

## References

- Research document: `.docs/research/02-07-2026-phase-4-brainstorming-skills-pre-planning-research.md`
- Roadmap Phase 4 spec: `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md:292-337`
- Skill being retired: `~/.claude/skills/discussing-features/SKILL.md:1-188`
- Downstream consumer: `~/.claude/skills/designing-code/SKILL.md:47,79`
- Agent to extend: `~/.claude/agents/docs-writer.md:32,44,63-72`
- Skill creation rules: `~/.claude/skills/creating-skills/SKILL.md:28-48,106-108`
- Workflow template: `~/.claude/skills/creating-skills/templates/workflow-skill-template.md:1-177`
- Original concept: `.docs/future-skills/brainstorming.md:1-39`
