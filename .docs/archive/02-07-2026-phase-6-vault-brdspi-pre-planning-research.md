---
date: 2026-02-07
status: complete
topic: "Phase 6 Vault BRDSPI Pre-Planning Research"
tags: [research, vault, brdspi, phase-6, obsidian, mcp]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Updated after 25 commits - bumped git_commit, corrected references path to archive location"
references:
  - .docs/archive/02-07-2026-future-skills-implementation-roadmap.md
archived: 2026-02-09
archive_reason: "Phase 6 fully implemented in commit 31aa0ef. All 7 vault BRDSPI skills deployed to plugins/commandbase-vault/skills/. Research served its purpose — decisions resolved, recommendations adopted. Implementation plan (.docs/plans/02-07-2026-phase-6-vault-brdspi-implementation.md) also marked complete."
---

# Phase 6 Vault BRDSPI Pre-Planning Research

**Date**: 2026-02-07
**Branch**: master

## Research Question
What patterns, tools, and architecture decisions are needed to implement 7 Vault BRDSPI skills (Phase 6 of the future skills roadmap)?

## Summary
Phase 6 requires building 7 skills that apply the proven Code-domain BRDSPI pattern to Obsidian vault management: `/starting-vault`, `/researching-vault`, `/designing-vault`, `/structuring-vault`, `/planning-vault`, `/implementing-vault`, and `/importing-vault`. Research confirms: (1) All 4 existing Code BRDSPI skills share a rigid 11-section structure that vault skills must replicate exactly. (2) `/brainstorming-vault` already exists as the entry point with 5 vault domains. (3) Obsidian MCP servers are mature with 47+ community implementations, all built on Obsidian Local REST API. (4) No CLI-based broken wikilink checker exists — vault linting must use Obsidian plugins or custom scripting. (5) The `.docs/` to Obsidian conversion for `/importing-vault` is straightforward since YAML frontmatter and markdown tables are natively compatible.

## Detailed Findings

### 1. Proven BRDSPI Skill Architecture (Code Domain)

All 4 Code BRDSPI skills (`/designing-code`, `/structuring-code`, `/starting-refactors`, `/planning-code`) share an identical 11-section structure:

1. **Frontmatter** — `name` (kebab-case) + `description` (4-part: use case, capability, sub-capabilities, activation phrases)
2. **Title** — `# Skill Name Title Case`
3. **Purpose Statement** — Single sentence
4. **Iron Law Enforcement** — "Violating the letter of these rules is violating the spirit of these rules."
5. **The Iron Law** — Primary constraint in code block + 4 "No exceptions" bullets
6. **The Gate Function** — 6-7 numbered steps with "Skipping steps = [consequence]"
7. **Initial Response** — Conditional branching (upstream artifacts present / missing / no params)
8. **Process Steps** — Numbered steps with agent spawning and artifact creation
9. **Important Guidelines** — 5-item numbered list
10. **Red Flags - STOP and Verify** — Bullet list of failure modes
11. **Rationalization Prevention** — Table (Excuse | Reality) + **The Bottom Line**

**File structure per skill:**
```
skill-name/
├── SKILL.md
├── reference/
│   └── domain-specific.md
└── templates/
    └── output-template.md
```

**Agent patterns:**
- Research agents: `code-locator`, `code-analyzer`, `code-librarian` spawned in parallel
- Writing agent: `docs-writer` with doc_type, topic, tags, template reference
- Model: Only `/designing-code` uses opus; others use default
- All require "Wait for ALL agents to complete" before synthesis

**Artifact chain:**
- `.docs/brainstorm/` → `/designing-code` reads
- `.docs/design/` → `/structuring-code` reads
- `.docs/structure/` → `/planning-code` reads (Structured mode)
- `.docs/plans/` → `/implementing-plans` reads

### 2. Existing Vault Entry Point (`/brainstorming-vault`)

Already deployed at `~/.claude/skills/brainstorming-vault/`. Covers 5 vault domains:

| Domain | What It Settles |
|--------|----------------|
| **Structure** | Folder hierarchy, flat vs nested, MOC strategy, daily notes |
| **Linking** | Wikilinks vs markdown, link density, hub-and-spoke vs organic |
| **Templates** | Templater vs core, note types, frontmatter strategy |
| **Organization** | PARA vs Zettelkasten vs hybrid, tag taxonomy, naming |
| **Plugins** | Minimal vs maximal, Dataview usage, automation level |

**Output:** `.docs/brainstorm/{topic-name}.md` with Decisions, Claude's Discretion, Deferred Ideas sections.

**Downstream references:** Already mentions `/starting-vault` and vault BRDSPI chain in completion summary (with "when available" caveat).

**Key insight:** Brainstorming captures vault *philosophy* (Zettelkasten vs PARA, wikilinks vs markdown links). Design/Structure phases translate philosophy into concrete implementation.

### 3. `/starting-projects` Pattern (Template for `/starting-vault`)

`/starting-projects` follows a 5-phase process that `/starting-vault` should mirror:

| starting-projects Phase | starting-vault Equivalent |
|------------------------|--------------------------|
| Phase 1: Discovery Questions | Vault path, existing notes, use case |
| Phase 2: Research Best Practices | Obsidian MCP setup, API key config |
| Phase 3: Create Development Plan | `.docs/plans/vault-setup.md` |
| Phase 4: Create CLAUDE.md | Vault-specific CLAUDE.md with MCP pointers |
| Phase 5: Wrap Up | Present MCP test commands, workflow chain |

**CLAUDE.md constraints from `/starting-projects`:**
- Under 60 lines ideal, never exceed 300
- Progressive disclosure — point to docs, don't inline
- No duplication of global rules
- Include vault path, MCP connection commands, verification steps

**Key difference:** `/starting-projects` delegates to `/researching-frameworks` for tech research. `/starting-vault` won't need this — vault setup is more procedural (MCP config, API key, vault path).

### 4. Obsidian MCP Server Landscape

**47+ community MCP servers** exist for Obsidian. All bridge to the **Obsidian Local REST API plugin**.

**Top implementations:**

| Server | Focus | Tools |
|--------|-------|-------|
| cyanheads/obsidian-mcp-server | Comprehensive | 8 tools (read, write, search, metadata, tags) |
| MarkusPfundstein/mcp-obsidian | Task-oriented | 7 tools + patch content |
| iansinnott/obsidian-claude-code-mcp | Claude Code specific | Optimized for CC workflow |
| aaronsb/obsidian-mcp-plugin | High-performance | Semantic operations |

**API key management:**
- Single key per vault from Obsidian Local REST API plugin settings
- Environment variables: `OBSIDIAN_API_KEY`, `OBSIDIAN_BASE_URL` (default `http://127.0.0.1:27124`)
- No folder-level permissions — access is binary (valid key = full vault)
- No multi-vault key management — each vault needs its own REST API instance

**Available operations:**
- Read/write notes (append, prepend, overwrite modes)
- Global search (text/regex with pagination)
- Find/replace within notes
- Directory listing with filtering
- Frontmatter management (atomic YAML key operations)
- Tag management (add, remove, list)
- Delete notes

**Decision needed for `/starting-vault`:** Which MCP server to recommend/configure. `cyanheads/obsidian-mcp-server` is most comprehensive. `iansinnott/obsidian-claude-code-mcp` is purpose-built for Claude Code.

### 5. Vault Linting Tools

**CLI linters (general markdown):**
- `markdownlint-cli2` (v0.47.0) — CommonMark/GFM validation, `--fix` auto-repair
- `remark-lint` — 70+ plugins, frontmatter schema validation via `remark-lint-frontmatter-schema`

**Critical gap: No CLI tool validates wikilinks.** Wikilinks (`[[note]]`) are non-standard markdown. CLI linters flag them as invalid syntax.

**Obsidian-specific linting:**
- **Obsidian Linter Plugin** — In-app only, rules for YAML/headings/footnotes/spacing
- **Broken Links Plugin** — Identifies links to non-existent files/headings/blocks
- **Find Orphaned Files Plugin** — Finds unlinked notes

**Decision for `/implementing-vault`:**
- Broken wikilink checking requires Obsidian plugins or custom scripting
- Frontmatter schema validation possible via `remark-lint-frontmatter-schema`
- General markdown linting via `markdownlint-cli2` (but must disable wikilink warnings)
- **Recommendation:** Vault linting as a validation step in `/implementing-vault`, not a standalone hook. Use MCP read operations to verify link targets exist rather than CLI tools.

### 6. Obsidian Vault Best Practices (Current)

**Folder structure consensus:**
- Obsidian CEO (Steph Ango) advocates minimal/no folders — use links, tags, search
- Community favors PARA method (Projects/Areas/Resources/Archives) for structured users
- Hybrid: Minimal top-level folders (`attachments/`, `templates/`, `daily/`) with tags for everything else
- Anti-pattern: Deep nesting (3+ levels)

**MOC strategies:**
- Maps of Content as index notes linking to topic collections
- Can be automated with Dataview queries (dynamic MOCs)
- Link maps together, embed maps in other notes
- Infinitely flexible — notes can appear in multiple maps

**Tag taxonomy:**
- Property tags (frontmatter) for classification
- Inline tags for contextual use
- Hierarchical tags (`#status/draft`, `#type/moc`) for structured taxonomy
- Flat tags for simplicity

**Frontmatter:**
- No official schema standard
- Built-in types: Text, List, Number, Checkbox, Date
- Obsidian does NOT support nested YAML natively
- Properties view plugin manages vault-wide properties

### 7. `.docs/` to Obsidian Conversion Analysis (for `/importing-vault`)

**What transfers directly (no conversion):**
- YAML frontmatter (Obsidian reads natively)
- Markdown tables
- Code fences
- Checkbox syntax (`- [x]` / `- [ ]`)
- File naming convention (dates work well)

**What needs conversion:**

| Current Format | Obsidian Format | Priority |
|---------------|-----------------|----------|
| `.docs/path/to/file.md` | `[[file-name]]` (wikilinks) | High |
| File:line citations | Keep as-is (no native support) | Low |
| `references:` paths | Wikilinks in frontmatter or Related Notes section | Medium |
| Markdown headers for warnings | `> [!warning]` callouts | Medium |
| Global config refs (`~/.claude/`) | MOC note mapping | Medium |
| Subdirectory organization | Preserve as vault folders | High |

**Recommended conversion strategy:**
1. Map `.docs/` subdirectories to vault folders (Research/, Plans/, Handoffs/)
2. Convert cross-references to wikilinks
3. Add "## Related Notes" section with wikilinks for backlink discovery
4. Optionally convert key sections to Obsidian callouts
5. Create MOC notes for navigation

**Scope decision needed:** Import only `.docs/research/` initially, or also plans/handoffs/learnings?

### 8. Canvas File Format (for future consideration)

JSON Canvas (v1.0) is an open specification:
- Node types: text, file, link, group
- Edges connect nodes with optional labels and directional arrows
- Programmatic generation possible — could create visual MOCs or architecture diagrams
- **Not needed for Phase 6 MVP** but useful for future vault visualization features

## Architecture Notes

### Skill Build Order (recommended)

Based on dependency analysis and the Code BRDSPI precedent:

1. **`/starting-vault`** — Parallel to `/starting-projects`. Sets up vault context, MCP config, CLAUDE.md.
2. **`/researching-vault`** — Explore existing vault structure, tags, orphans, link graphs. Uses MCP read operations.
3. **`/designing-vault`** — MOC strategy, tagging taxonomy, template designs. Should use opus model (like `/designing-code`).
4. **`/structuring-vault`** — Folder layout, naming conventions, note placement rules.
5. **`/planning-vault`** — Ordered tasks with success criteria for vault implementation.
6. **`/implementing-vault`** — Create/move notes, update links, apply frontmatter. Includes vault linting validation.
7. **`/importing-vault`** — Bridge from `.docs/` to Obsidian format. Can be built last since it's a converter.

### Key Design Decisions for Planning

| Decision | Options | Recommendation |
|----------|---------|---------------|
| MCP server choice | cyanheads, iansinnott, MarkusPfundstein | Research during `/starting-vault` implementation |
| Vault linting approach | CLI tool, Obsidian plugin, MCP-based validation | MCP-based (verify via read operations) |
| Link format default | Wikilinks, markdown links | Wikilinks (Obsidian-native) |
| `/designing-vault` model | Default, opus | Opus (matches `/designing-code` precedent) |
| `/importing-vault` scope | Research only, all .docs/ | Start with research, expand |
| Agent types for vault research | code-locator/analyzer/librarian | New vault-specific or reuse existing |
| Broken link detection | Obsidian plugin, custom MCP queries | MCP queries (list + verify targets) |

### Artifact Directory Mapping

New `.docs/` directories needed:
- `.docs/vault-design/` (from `/designing-vault`) — or reuse `.docs/design/` with vault tags?
- `.docs/vault-structure/` (from `/structuring-vault`) — or reuse `.docs/structure/`?

**Decision:** Reuse existing `.docs/design/` and `.docs/structure/` directories with vault-specific tags (consistent with code domain). The `doc_type` and `tags` fields distinguish vault from code artifacts.

### Vault Skill Agent Strategy

**Research agents for vault skills:**
Vault skills can't use `code-locator` / `code-analyzer` / `code-librarian` since they analyze code, not vault structure. Options:
- Use MCP tools directly in skill process (read vault contents via MCP)
- Spawn generic `Explore` or `general-purpose` agents with MCP access
- Create vault-specific reference docs that guide manual exploration

**Recommendation:** Vault skills that interact with vault content should use MCP tools directly within their process steps (not spawn code-analysis agents). Skills that analyze vault structure (`/researching-vault`) can spawn `general-purpose` agents that use MCP tools.

## Open Questions

1. **Which MCP server should `/starting-vault` configure?** Need to test top candidates (cyanheads vs iansinnott) for Claude Code compatibility
2. **Should vault skills use a shared MCP connection config?** Or should each skill independently read vault config from CLAUDE.md?
3. **What's the minimum Obsidian plugin set required?** Local REST API is mandatory. Templater? Dataview? Linter?
4. **How should `/implementing-vault` handle note moves?** Parse all `[[wikilinks]]` and update references, or rely on Obsidian's auto-update?
5. **Should `/importing-vault` create MOC notes automatically?** Or just convert individual docs?
6. **Does the user have a target vault already?** This affects whether `/starting-vault` creates a new vault or configures access to an existing one
