---
date: 2026-02-07
status: complete
topic: "Phase 6 Vault BRDSPI Implementation"
tags: [plan, vault, brdspi, phase-6, obsidian, skills]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Bumped git_commit to HEAD and updated references to current locations (archive for docs, plugins for skills). No content changes needed -- plan is complete and archived."
archived: 2026-02-09
archive_reason: "Completed plan with all 7 vault BRDSPI skills deployed. newskills/ paths no longer exist after plugin marketplace restructure (commit 87a19a3). Skills now live under plugins/commandbase-vault/skills/."
references:
  - .docs/archive/02-07-2026-phase-6-vault-brdspi-pre-planning-research.md
  - .docs/archive/02-07-2026-future-skills-implementation-roadmap.md
  - plugins/commandbase-vault/skills/brainstorming-vault/SKILL.md
  - plugins/commandbase-vault/skills/designing-vault/SKILL.md
  - plugins/commandbase-vault/skills/implementing-vault/SKILL.md
  - plugins/commandbase-vault/skills/importing-vault/SKILL.md
  - plugins/commandbase-vault/skills/planning-vault/SKILL.md
  - plugins/commandbase-vault/skills/researching-vault/SKILL.md
  - plugins/commandbase-vault/skills/starting-vault/SKILL.md
  - plugins/commandbase-vault/skills/structuring-vault/SKILL.md
---

# Phase 6: Vault BRDSPI Implementation Plan

## Overview

Implement 7 vault-domain BRDSPI skills that mirror the proven code-domain BRDSPI chain, adapted for Obsidian vault management. Each skill follows the exact 11-section BRDSPI structure (frontmatter, title, purpose, iron law enforcement, iron law, gate function, initial response, process steps, important guidelines, red flags, rationalization prevention). Skills use the best tool for each job — MCP tools for vault search/metadata operations, file-system tools for direct note creation/editing. MCP server choice is deferred to `/starting-vault`'s setup flow.

**Upstream dependency:** Phase 2 (BRDSPI Core) — COMPLETE. All 4 code BRDSPI skills deployed.
**Entry point:** `/brainstorming-vault` — already deployed (Phase 4).

## Current State Analysis

**What exists:**
- `/brainstorming-vault` deployed at `~/.claude/skills/brainstorming-vault/` — captures vault philosophy (structure, linking, templates, organization, plugins domains). Produces `.docs/brainstorm/` artifacts.
- 4 code-domain BRDSPI skills deployed (`/designing-code`, `/structuring-code`, `/planning-code`, `/starting-refactors`) — serve as structural templates.
- `/starting-projects` deployed — serves as the template for `/starting-vault`.
- `/researching-code` deployed — serves as the template for `/researching-vault`.
- Pre-planning research complete at `.docs/research/02-07-2026-phase-6-vault-brdspi-pre-planning-research.md`.
- 47+ Obsidian MCP servers available. Top candidates: cyanheads (comprehensive, 8 tools), iansinnott (Claude Code-specific).

**What's missing:**
- All 7 vault BRDSPI skills (`/starting-vault`, `/researching-vault`, `/designing-vault`, `/structuring-vault`, `/planning-vault`, `/implementing-vault`, `/importing-vault`).
- No MCP server configured for vault operations.
- No vault-specific reference docs or templates.

### Key Discoveries:
- All Code BRDSPI skills share an identical 11-section structure — vault skills MUST replicate this exactly (research finding §1)
- `/brainstorming-vault` already outputs to `.docs/brainstorm/` with vault philosophy decisions — design/structure phases read this (research finding §2)
- Vault skills cannot use `code-locator`/`code-analyzer`/`code-librarian` agents — they must use MCP tools directly or spawn `general-purpose` agents with MCP access (research finding, Architecture Notes §Vault Skill Agent Strategy)
- CLI tools don't validate wikilinks — vault linting must use MCP read operations to verify link targets (research finding §5)
- `.docs/` artifacts transfer to Obsidian with minimal conversion — YAML frontmatter, markdown tables, code fences, checkboxes all work natively (research finding §7)
- Obsidian does NOT support nested YAML in frontmatter natively (research finding §6)
- Reuse existing `.docs/design/` and `.docs/structure/` directories with vault-specific tags — no new artifact directories needed (research finding, Architecture Notes §Artifact Directory Mapping)

## Desired End State

After this plan is complete:
1. All 7 vault BRDSPI skills deployed to `~/.claude/skills/` and tracked in `newskills/`
2. Full BRDSPI chain works: `/brainstorming-vault` → `/starting-vault` → `/researching-vault` → `/designing-vault` → `/structuring-vault` → `/planning-vault` → `/implementing-vault`
3. `/importing-vault` can convert `.docs/research/` artifacts to Obsidian-native notes
4. Each skill follows the exact 11-section structure with vault-appropriate iron laws and gate functions
5. Each skill has `reference/` and `templates/` subdirectories with domain-specific content
6. `/starting-vault` configures MCP connection and creates vault-aware CLAUDE.md
7. Skills use MCP tools for search/metadata and file-system tools for direct editing as appropriate

**Verification:** Each phase has specific success criteria. Final verification: invoke the complete chain on a real vault operation.

## What We're NOT Doing

- Not building vault-specific agents (e.g., `vault-analyzer`) — vault skills use MCP tools directly or `general-purpose` agents
- Not creating a `/vault-lint` standalone skill — linting is a validation step within `/implementing-vault`
- Not implementing Canvas file generation — deferred to future work
- Not building multi-vault management — each vault is configured independently
- Not creating Dataview query generation — skills can reference Dataview syntax but don't generate custom queries
- Not modifying existing code-domain BRDSPI skills
- Not deciding which MCP server to use in this plan — `/starting-vault` handles MCP discovery

## Implementation Approach

Build skills sequentially in BRDSPI chain order. Each skill:
1. Mirror its code-domain counterpart's 11-section structure
2. Replace code-specific concepts with vault equivalents (agents → MCP tools, files → notes, modules → folders/MOCs)
3. Create vault-specific `reference/` and `templates/` subdirectories
4. Deploy to `~/.claude/skills/` AND track in `newskills/`
5. Validate by checking the skill description appears in Claude Code's skill list

**Structural template mapping:**

| Vault Skill | Code Template | Key Adaptation |
|------------|---------------|----------------|
| `/starting-vault` | `/starting-projects` | MCP setup instead of framework research. Vault path + API key instead of tech stack. |
| `/researching-vault` | `/researching-code` | MCP read/search instead of code-locator/analyzer agents. Vault structure instead of codebase patterns. |
| `/designing-vault` | `/designing-code` | MOC strategy, tag taxonomy, template design instead of API shape, pattern selection. Uses opus model. |
| `/structuring-vault` | `/structuring-code` | Folder layout, note placement instead of file placement, module boundaries. |
| `/planning-vault` | `/planning-code` | Vault tasks instead of code tasks. MCP verification instead of test commands. |
| `/implementing-vault` | `/implementing-plans` (adapted) | MCP write operations, wikilink management, frontmatter application. Includes vault linting. |
| `/importing-vault` | No direct template | New pattern: `.docs/` → Obsidian conversion with wikilinks, callouts, tags. |

---

## Phase 1: `/starting-vault` Skill

### Overview
Create the vault initialization skill, parallel to `/starting-projects`. Guides users through vault setup: discovering vault path, configuring MCP connection, creating vault-aware CLAUDE.md with vault path and MCP connection info.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/starting-vault/SKILL.md`
**Template**: `/starting-projects` (adapted for vault domain)

**Frontmatter:**
```yaml
name: starting-vault
description: "Use this skill when initializing a new Obsidian vault for Claude Code management or configuring Claude Code to work with an existing vault. This includes discovering vault path, configuring MCP server connection, setting up API key, creating vault-aware CLAUDE.md, and testing MCP connectivity. Activate when the user says 'start a vault', 'set up vault', 'configure obsidian', 'connect to vault', or before running vault BRDSPI."
```

**Iron Law:** `NO VAULT SETUP WITHOUT TESTING CONNECTIVITY FIRST`

**Gate Function (5 steps):**
1. DISCOVER: Vault path, existing or new, MCP server preference
2. CONFIGURE: MCP server setup (API key, base URL, server choice)
3. TEST: Verify MCP connectivity (list vault root, read a note)
4. CREATE: Vault-aware CLAUDE.md with vault path, MCP config, verification commands
5. PRESENT: Summary with workflow chain and next steps

**Process (5 phases matching /starting-projects):**
- Phase 1: Vault Discovery — AskUserQuestion for vault path, existing/new, use case
- Phase 2: MCP Configuration — Guide Obsidian Local REST API plugin install, API key setup, MCP server selection and configuration
- Phase 3: Connectivity Test — Use MCP tools to list vault root, verify read/write capability
- Phase 4: Create CLAUDE.md — Vault path, MCP connection details, verification commands, vault conventions
- Phase 5: Wrap Up — Present workflow chain (`/brainstorming-vault` → full BRDSPI)

**Key differences from /starting-projects:**
- No `/researching-frameworks` delegation — vault setup is procedural, not research-heavy
- MCP connectivity testing is mandatory (equivalent to "project builds" verification)
- CLAUDE.md includes vault-specific sections: vault path, MCP config, plugin requirements

#### 2. Reference Files
**File**: `newskills/starting-vault/reference/mcp-setup-guide.md`
- Obsidian Local REST API plugin installation steps
- API key generation
- MCP server options (cyanheads, iansinnott, others) with trade-offs
- Environment variable configuration (OBSIDIAN_API_KEY, OBSIDIAN_BASE_URL)
- Troubleshooting common connection issues

**File**: `newskills/starting-vault/reference/claude-md-guidelines.md`
- Vault-specific CLAUDE.md sections (vault path, MCP connection, conventions)
- Under 60 lines guidance (consistent with /starting-projects)
- Example vault CLAUDE.md

#### 3. Template Files
**File**: `newskills/starting-vault/templates/vault-claude-md-template.md`
- Template for vault-aware CLAUDE.md generation

### Deployment:
```bash
cp -r newskills/starting-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows 11-section BRDSPI structure
- [x] AskUserQuestion used for vault path and MCP server selection
- [x] MCP connectivity test included as mandatory step
- [x] Vault-aware CLAUDE.md template created
- [x] Skill description appears in Claude Code skill list
- [x] `/brainstorming-vault` completion message updated to reference `/starting-vault` (remove "when available" caveat)

---

## Phase 2: `/researching-vault` Skill

### Overview
Create the vault research skill, parallel to `/researching-code`. Explores existing vault structure, tags, orphan notes, link graphs, and conventions using MCP tools and file-system access. Produces `.docs/research/` artifact.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/researching-vault/SKILL.md`
**Template**: `/researching-code` (adapted for vault domain)

**Frontmatter:**
```yaml
name: researching-vault
description: "Use this skill when researching an Obsidian vault to understand its structure, conventions, and content patterns. This includes mapping folder structure, analyzing tag usage, finding orphan notes, tracing link graphs, documenting frontmatter conventions, and identifying MOC patterns. Activate when the user says 'research vault', 'analyze vault structure', 'what's in my vault', 'map vault conventions', or before designing vault changes."
```

**Iron Law:** `NO SYNTHESIS WITHOUT VAULT EXPLORATION FIRST`

**Gate Function (7 steps):**
1. IDENTIFY: What aspects of the vault need investigation?
2. EXPLORE: Use MCP search/list tools to map vault structure
3. ANALYZE: Examine tag usage, frontmatter patterns, link density
4. DETECT: Find orphan notes, broken links, empty folders
5. VERIFY: Are findings backed by specific note references?
6. WRITE: Create `.docs/research/MM-DD-YYYY-description.md` via docs-writer (MANDATORY)
7. PRESENT: Summary to user with link to research file

**Process Steps:**
- Step 1: Read vault CLAUDE.md for vault path and MCP config
- Step 2: Decompose the research question into vault aspects (structure, tags, links, frontmatter, orphans, MOCs)
- Step 3: Vault exploration — use MCP tools to list directories, search content, read sample notes. Can also spawn `general-purpose` agents with instructions to use MCP tools for parallel exploration.
- Step 4: Synthesize findings — folder tree, tag taxonomy, frontmatter schema, link patterns, orphan list
- Step 5: Write research document via docs-writer
- Step 6: Present findings with note references

**Key differences from /researching-code:**
- Uses MCP tools (list, search, read) instead of code-locator/analyzer/librarian agents
- Can also use file-system Read/Glob/Grep tools directly on vault path for operations like finding all files with specific frontmatter
- Research aspects are vault-specific: folders, tags, links, frontmatter schemas, MOCs, orphans
- "file:line references" become "note references" (note path + section)
- Also checks for existing `.docs/research/` artifacts about the vault topic (avoid re-researching)

#### 2. Reference Files
**File**: `newskills/researching-vault/reference/vault-research-aspects.md`
- Vault research dimensions: structure, tags, links, frontmatter, orphans, MOCs, plugins
- MCP tool usage for each dimension
- File-system tool usage for batch operations (Glob for file patterns, Grep for frontmatter fields)
- Example queries and expected output formats

**File**: `newskills/researching-vault/reference/evidence-requirements.md`
- What counts as valid vault evidence (note paths, tag counts, link counts)
- How to cite vault findings

#### 3. Template Files
**File**: `newskills/researching-vault/templates/vault-research-template.md`
- Research document template with vault-specific sections (folder tree, tag taxonomy, frontmatter schema, link graph summary, orphan list)

### Deployment:
```bash
cp -r newskills/researching-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows 11-section BRDSPI structure
- [x] Uses MCP tools and/or file-system tools appropriately based on operation type
- [x] Produces `.docs/research/` artifact via docs-writer
- [x] Covers all vault research dimensions (structure, tags, links, frontmatter, orphans, MOCs)
- [x] Skill description appears in Claude Code skill list

---

## Phase 3: `/designing-vault` Skill

### Overview
Create the vault design skill, parallel to `/designing-code`. Makes architectural decisions for vault organization: MOC strategy, tagging taxonomy, template designs, frontmatter schema. Uses opus model for deeper reasoning. Produces `.docs/design/` artifact.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/designing-vault/SKILL.md`
**Template**: `/designing-code` (adapted for vault domain)

**Frontmatter:**
```yaml
name: designing-vault
description: "Use this skill when making organizational decisions for an Obsidian vault. This includes designing MOC strategy, defining tagging taxonomy, choosing template patterns, setting frontmatter schema, and deciding linking conventions. Activate when the user says 'design vault', 'vault architecture', 'MOC strategy', 'tag taxonomy', or after completing research with /researching-vault."
```

**Iron Law:** `NO DESIGN WITHOUT RESEARCH ARTIFACTS FIRST`

**Gate Function (6 steps):**
1. READ: Find and read vault research artifacts (`.docs/research/`)
2. ANALYZE: Identify vault design decisions needed (MOCs, tags, templates, frontmatter, linking)
3. QUESTION: Ask vault organizational questions inline (AskUserQuestion)
4. DESIGN: Spawn opus-model agents to reason through vault architecture
5. WRITE: Create `.docs/design/` document via docs-writer
6. PRESENT: Summary with decision list and link to design doc

**Vault Design Domains (replacing code design domains):**

| Code Domain | Vault Equivalent |
|------------|-----------------|
| API Design | Frontmatter Schema — property names, types, required fields |
| Pattern Selection | MOC Strategy — hub-and-spoke, topic clusters, dynamic Dataview MOCs |
| Error Strategy | Orphan Prevention — linking conventions, MOC coverage requirements |
| Component Boundaries | Folder Boundaries — what goes where, nesting depth, separation of concerns |
| Data & State | Tag Taxonomy — hierarchical vs flat, property tags vs inline, naming conventions |

Additional vault-specific domain:
- **Template Design** — note types, Templater vs core templates, frontmatter defaults per type

**Key differences from /designing-code:**
- Uses opus model (same as `/designing-code`)
- Reads vault research artifacts AND `.docs/brainstorm/` from `/brainstorming-vault`
- Design domains are vault-specific (MOCs, tags, templates, frontmatter, folders)
- No implementation details — design says WHAT organization, not HOW to reorganize

#### 2. Reference Files
**File**: `newskills/designing-vault/reference/vault-design-domains.md`
- Vault design domain descriptions and example questions
- MOC strategy options with trade-offs
- Tag taxonomy patterns
- Frontmatter schema design considerations
- Template design patterns

#### 3. Template Files
**File**: `newskills/designing-vault/templates/vault-design-template.md`
- Design document template with vault-specific sections

### Deployment:
```bash
cp -r newskills/designing-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows 11-section BRDSPI structure
- [x] Uses opus model for design reasoning (matches `/designing-code` precedent)
- [x] Reads both research artifacts and brainstorm artifacts
- [x] Vault design domains are appropriate (MOCs, tags, templates, frontmatter, folders)
- [x] Produces `.docs/design/` artifact with vault-specific tags via docs-writer
- [x] Skill description appears in Claude Code skill list

---

## Phase 4: `/structuring-vault` Skill

### Overview
Create the vault structure skill, parallel to `/structuring-code`. Maps folder layout, naming conventions, and note placement rules based on design decisions. Produces `.docs/structure/` artifact.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/structuring-vault/SKILL.md`
**Template**: `/structuring-code` (adapted for vault domain)

**Frontmatter:**
```yaml
name: structuring-vault
description: "Use this skill when mapping folder layout, naming conventions, and note placement rules for an Obsidian vault. This includes deciding folder hierarchy, note file naming, MOC placement, template locations, attachment organization, and migration order for vault reorganizations. Activate when the user says 'structure vault', 'organize vault folders', 'where should notes go', or after /designing-vault."
```

**Iron Law:** `NO STRUCTURE WITHOUT UNDERSTANDING WHAT EXISTS`

**Gate Function (7 steps):**
1. READ: Find and read vault design doc (`.docs/design/`) if available
2. RESEARCH: Use MCP tools and/or file-system tools to map current vault folder organization
3. ANALYZE: Compare design decisions to current vault structure
4. MAP: Determine folder layout, note placement, naming conventions
5. SEQUENCE: For reorganizations, determine migration order (each step leaves vault functional)
6. WRITE: Create `.docs/structure/` document via docs-writer
7. PRESENT: Summary with structural map and link

**Vault Structure Concerns (replacing code structure concerns):**

| Code Concern | Vault Equivalent |
|-------------|-----------------|
| File placement | Note placement — which folder each note type goes in |
| Module boundaries | Folder boundaries — top-level vs nested, MOC folder strategy |
| Dependency direction | Link direction — which notes link to which, backlink expectations |
| Test organization | Template organization — template location, naming, accessibility |
| Import patterns | Attachment handling — images, PDFs, embedded files organization |

**Key differences from /structuring-code:**
- Uses MCP list/search tools and/or file-system Glob/Grep instead of code-locator/analyzer/librarian agents
- Structure concerns are vault-specific (folders, MOC placement, attachment handling)
- Migration steps must preserve wikilinks (critical vault integrity concern)
- "Every step deployable" becomes "every step leaves vault navigable"

#### 2. Reference Files
**File**: `newskills/structuring-vault/reference/vault-structure-patterns.md`
- Common vault structures (PARA, Zettelkasten, hybrid, minimal)
- Naming convention patterns
- Attachment organization strategies
- Migration sequencing for vault reorganization

#### 3. Template Files
**File**: `newskills/structuring-vault/templates/vault-structural-map-template.md`
- Structural map template with vault-specific sections (folder tree, note placement rules, MOC map, migration steps)

### Deployment:
```bash
cp -r newskills/structuring-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows 11-section BRDSPI structure
- [x] Uses MCP tools and/or file-system tools to map current vault structure
- [x] Vault structure concerns appropriate (folders, MOCs, attachments, naming)
- [x] Migration steps preserve wikilink integrity
- [x] Produces `.docs/structure/` artifact with vault-specific tags via docs-writer
- [x] Skill description appears in Claude Code skill list

---

## Phase 5: `/planning-vault` Skill

### Overview
Create the vault planning skill, parallel to `/planning-code`. Breaks vault changes into phased, ordered tasks with success criteria. Accepts structural map from `/structuring-vault` when available. Produces `.docs/plans/` artifact.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/planning-vault/SKILL.md`
**Template**: `/planning-code` (adapted for vault domain)

**Frontmatter:**
```yaml
name: planning-vault
description: "Create or iterate on vault implementation plans with thorough vault research. Use when the user says 'plan vault changes', 'vault implementation plan', 'plan vault reorganization', or provides a path to an existing vault plan in .docs/plans/. Researches vault structure before planning, produces phased plans with success criteria."
```

**Iron Law:** `NO PLAN WITHOUT VAULT RESEARCH FIRST`

**Gate Function (6 steps):**
1. IDENTIFY: What aspects of the vault need investigation?
2. EXPLORE: Use MCP tools and/or file-system tools to verify current vault state
3. WAIT: All exploration must complete before proceeding
4. READ: Read all vault artifacts (research, design, structure docs)
5. VERIFY: Do you have specific note/folder references for affected areas?
6. ONLY THEN: Write the implementation plan

**Process (matching /planning-code):**
- Mode A: Iterate on existing vault plan (surgical edits)
- Mode B: Create new vault plan
- Input Detection: Check for upstream vault artifacts (`.docs/structure/` with vault tags → Structured mode)
- Step 1: Context gathering — read vault artifacts, explore vault via MCP/file-system tools
- Step 2: Deep research — verify vault state, discover edge cases
- Step 3: Plan structure development — present phases for approval
- Step 4: Detailed plan writing via docs-writer
- Step 5: Review and checkpoint suggestion

**Vault-specific verification commands (replacing code test commands):**
- "Verify note exists at path via MCP read or file-system Read"
- "Verify wikilinks resolve via MCP search or Grep"
- "Verify frontmatter contains expected properties"
- "Verify folder structure matches plan via MCP list or Glob"
- "Verify tag applied to expected notes"

**Key differences from /planning-code:**
- Uses MCP tools and/or file-system tools instead of code-locator/analyzer agents for vault exploration
- Success criteria reference vault verification (note existence, wikilink resolution, frontmatter properties) instead of test suites
- Plan phases may include "batch" operations (apply frontmatter to all notes in a folder)

#### 2. Reference Files
**File**: `newskills/planning-vault/reference/vault-verification-commands.md`
- How to verify vault changes (MCP and file-system approaches)
- Common success criteria patterns for vault operations

**File**: `newskills/planning-vault/reference/research-workflow.md`
- Vault research workflow (adapted from code research workflow)

#### 3. Template Files
**File**: `newskills/planning-vault/templates/vault-plan-template.md`
- Plan template with vault-specific sections and success criteria patterns

### Deployment:
```bash
cp -r newskills/planning-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows 11-section BRDSPI structure
- [x] Accepts vault structural map in Structured mode
- [x] Mode A (iterate) and Mode B (create new) both work
- [x] Vault verification commands are appropriate (MCP read/search, file-system Read/Glob/Grep)
- [x] Produces `.docs/plans/` artifact via docs-writer
- [x] Skill description appears in Claude Code skill list

---

## Phase 6: `/implementing-vault` Skill

### Overview
Create the vault implementation skill. Executes vault plans by creating/moving notes, updating wikilinks, applying frontmatter, and managing folder structure. Includes vault linting validation (broken wikilinks, frontmatter completeness, orphan detection). Uses MCP tools for search/metadata and file-system tools for direct note editing.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/implementing-vault/SKILL.md`
**Template**: Hybrid of `/implementing-plans` structure + vault-specific operations

**Frontmatter:**
```yaml
name: implementing-vault
description: "Use this skill when executing vault implementation plans from .docs/plans/. This includes creating notes, moving notes, updating wikilinks after moves, applying frontmatter properties, managing folder structure, and running vault linting validation. Activate when the user says 'implement vault plan', 'execute vault changes', 'apply vault structure', or after completing planning with /planning-vault."
```

**Iron Law:** `NO IMPLEMENTATION WITHOUT A PLAN AND CHECKPOINT FIRST`

**Gate Function (6 steps):**
1. READ: Find and read the vault plan from `.docs/plans/`
2. CHECKPOINT: Create baseline via `/bookmarking-code create` (mandatory)
3. EXECUTE: Implement each phase using MCP write/move tools and/or file-system Write/Edit
4. LINT: Run vault linting after each phase (broken wikilinks, frontmatter, orphans)
5. VERIFY: Check success criteria for each phase
6. CHECKPOINT: Create post-phase checkpoint

**Vault Operations:**
- Create notes: MCP write or file-system Write tool
- Move notes: Update file location + scan for wikilinks referencing old path + update them
- Update frontmatter: MCP frontmatter tools or file-system Edit on YAML block
- Apply tags: MCP tag tools or Edit on frontmatter
- Create folders: File-system mkdir via Bash
- Manage wikilinks: Grep to find references, Edit to update paths

**Vault Linting (built into each phase, not standalone):**
- Broken wikilinks: For each `[[target]]`, verify target note exists via MCP search or Glob
- Frontmatter validation: Check required properties exist in modified notes
- Orphan detection: After moves, check if any notes lost all incoming links
- Heading structure: Verify no skipped heading levels in created/modified notes

**Key differences from /implementing-plans:**
- Operates on vault notes instead of code files
- Wikilink integrity management is critical — every note move must update references
- Linting is vault-specific (wikilinks, frontmatter, orphans) instead of code-specific (tests, types, lint)
- Checkpoint scope includes vault path files
- No test suite — verification via MCP read and file-system tool checks

#### 2. Reference Files
**File**: `newskills/implementing-vault/reference/vault-operations.md`
- MCP tool usage for vault operations (create, move, update, delete)
- File-system tool usage for direct note editing
- Wikilink update procedure after note moves
- Frontmatter modification patterns

**File**: `newskills/implementing-vault/reference/vault-linting.md`
- Linting checks and how to perform each
- Wikilink resolution verification
- Frontmatter validation rules
- Orphan detection approach

#### 3. Template Files
**File**: `newskills/implementing-vault/templates/vault-implementation-checklist.md`
- Per-phase checklist template for vault operations

### Deployment:
```bash
cp -r newskills/implementing-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows 11-section BRDSPI structure (adapted for implementation)
- [x] Mandatory checkpoint before implementation
- [x] Wikilink update procedure after note moves
- [x] Vault linting built into each phase (broken wikilinks, frontmatter, orphans)
- [x] Uses MCP and/or file-system tools appropriately based on operation
- [x] Skill description appears in Claude Code skill list

---

## Phase 7: `/importing-vault` Skill

### Overview
Create the vault import skill. Converts `.docs/` artifacts (research, plans, handoffs, learnings) into Obsidian-native notes with wikilinks, callouts, tags, and proper frontmatter. This is a bridge skill — not part of the standard BRDSPI chain but a companion that feeds project knowledge into the vault.

### Changes Required:

#### 1. Main Skill File
**File**: `newskills/importing-vault/SKILL.md`
**Template**: New pattern (no direct code-domain counterpart)

**Frontmatter:**
```yaml
name: importing-vault
description: "Use this skill when converting .docs/ artifacts into Obsidian vault notes. This includes transforming research documents, plans, handoffs, and learnings into vault-native format with wikilinks, callouts, tags, and frontmatter. Activate when the user says 'import to vault', 'convert docs to vault', 'move research to obsidian', or after completing a research/planning cycle."
```

**Iron Law:** `NO IMPORT WITHOUT UNDERSTANDING VAULT CONVENTIONS FIRST`

**Gate Function (6 steps):**
1. READ: Read vault CLAUDE.md for vault path, conventions, frontmatter schema
2. DISCOVER: Find `.docs/` artifacts to import (user-specified or discover available)
3. MAP: Determine conversion rules (frontmatter translation, tag mapping, wikilink targets)
4. CONVERT: Transform each artifact to vault-native format
5. VERIFY: Check converted notes for broken wikilinks, proper frontmatter, tag consistency
6. PRESENT: Summary of imported notes with vault locations

**Conversion Rules:**
- YAML frontmatter → translate to vault's property schema (rename fields, add vault-specific properties)
- `.docs/path/to/file.md` references → `[[file-name]]` wikilinks (if target exists in vault)
- `file.ext:line` code citations → keep as-is (no native vault equivalent)
- `references:` paths → wikilinks in a "Related Notes" section
- Warning/info headers → `> [!warning]` / `> [!info]` Obsidian callouts
- Tags from frontmatter → map to vault tag taxonomy
- Subdirectory organization → vault folder placement based on doc_type

**Import Scope Options (presented via AskUserQuestion):**
- Single file import (user provides path)
- Batch import by type (all research, all plans, etc.)
- Full `.docs/` import

**Key design decisions:**
- User reviews converted note before vault placement (not automatic)
- Frontmatter translation rules discovered from vault conventions (not hardcoded)
- MOC integration: offer to add imported note to relevant MOC
- Duplicate detection: check if vault already has a note with similar title/content

#### 2. Reference Files
**File**: `newskills/importing-vault/reference/conversion-rules.md`
- Detailed conversion rules for each `.docs/` element type
- Frontmatter field mapping examples
- Callout syntax reference
- Wikilink generation rules

**File**: `newskills/importing-vault/reference/docs-types.md`
- `.docs/` artifact types (research, plan, design, structure, handoff, learning, brainstorm, refactor)
- Expected frontmatter fields per type
- Suggested vault folder placement per type

#### 3. Template Files
**File**: `newskills/importing-vault/templates/imported-note-template.md`
- Template for converted vault notes with standard sections (Source Info, Content, Related Notes)

### Deployment:
```bash
cp -r newskills/importing-vault ~/.claude/skills/
```

### Success Criteria:
- [x] Skill follows adapted BRDSPI structure (11 sections)
- [x] Reads vault conventions before converting
- [x] Converts frontmatter, references, callouts, tags correctly
- [x] User reviews converted note before vault placement
- [x] Single file and batch import modes work
- [x] Wikilinks generated only for notes that exist in vault
- [x] Skill description appears in Claude Code skill list

---

## Testing Strategy

### Per-Phase Validation:
- Each phase: verify skill follows 11-section structure (frontmatter, title, purpose, enforcement, iron law, gate function, initial response, process steps, guidelines, red flags, rationalization prevention)
- Each phase: verify skill description appears in Claude Code skill list after deployment
- Each phase: verify reference/ and templates/ subdirectories exist with content
- Each phase: verify skill is tracked in both `newskills/` and `~/.claude/skills/`

### Chain Validation (after all 7 phases):
- Invoke `/brainstorming-vault` → verify `.docs/brainstorm/` artifact created
- Invoke `/starting-vault` → verify CLAUDE.md with vault config created
- Invoke `/researching-vault` → verify `.docs/research/` artifact with vault findings
- Invoke `/designing-vault` → verify `.docs/design/` artifact with vault decisions
- Invoke `/structuring-vault` → verify `.docs/structure/` artifact with vault layout
- Invoke `/planning-vault` → verify `.docs/plans/` artifact with vault tasks
- Invoke `/implementing-vault` → verify vault notes created/moved per plan
- Invoke `/importing-vault` → verify `.docs/` artifact converted to vault note

## Performance Considerations

- MCP operations may be slow for large vaults — batch operations should have progress indicators
- Wikilink scanning (Grep for `[[target]]` patterns) can be expensive — limit to affected files, not full vault
- Vault linting after each implementation phase adds overhead but catches issues early

## Migration Notes

- `/brainstorming-vault` already deployed — update its completion message to remove "when available" caveat for `/starting-vault`
- Future skills roadmap needs updating after each phase completes (update Phase 6 section)
- No existing vault skills to migrate from — all 7 are new

## References

- Pre-planning research: `.docs/research/02-07-2026-phase-6-vault-brdspi-pre-planning-research.md`
- Master roadmap: `.docs/plans/02-07-2026-future-skills-implementation-roadmap.md`
- Code BRDSPI templates: `newskills/designing-code/`, `newskills/structuring-code/`, `newskills/planning-code/`, `newskills/starting-projects/`, `newskills/researching-code/`
- Existing vault entry point: `newskills/brainstorming-vault/`
