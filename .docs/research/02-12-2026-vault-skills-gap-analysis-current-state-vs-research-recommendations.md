---
date: 2026-02-12
status: complete
topic: "Vault Skills Gap Analysis: Current State vs Research Recommendations"
tags: [research, vault-skills, gap-analysis, commandbase-vault, obsidian]
git_commit: 9c4c7f4
references:
  - plugins/commandbase-vault/skills/brainstorming-vault/SKILL.md
  - plugins/commandbase-vault/skills/starting-vault/SKILL.md
  - plugins/commandbase-vault/skills/researching-vault/SKILL.md
  - plugins/commandbase-vault/skills/designing-vault/SKILL.md
  - plugins/commandbase-vault/skills/structuring-vault/SKILL.md
  - plugins/commandbase-vault/skills/planning-vault/SKILL.md
  - plugins/commandbase-vault/skills/implementing-vault/SKILL.md
  - plugins/commandbase-vault/skills/importing-vault/SKILL.md
  - .docs/research/02-12-2026-obsidian-vault-management-with-claude-summary.md
  - .docs/research/02-12-2026-kepano-obsidian-skills-repo-analysis.md
  - .docs/research/02-12-2026-axton-obsidian-visual-skills-repository-analysis.md
---

# Vault Skills Gap Analysis: Current State vs Research Recommendations

**Date**: 2026-02-12
**Branch**: refactor/vault-skill-refinement

## Research Question
What opportunities exist for additional skills, revisions, or replacements in commandbase-vault, based on research into Obsidian vault management best practices and community patterns?

## Summary

The current 8 vault skills form a strong **BRDSPI workflow** (Brainstorm → Research → Design → Structure → Plan → Implement) plus setup and import. They excel at vault initialization and reorganization — the "set up once, reorganize sometimes" use case.

The biggest gap is **daily operations** — the things you do WITH a vault once it's set up. Community repos (ZanderRuss: 29 commands, ballred PKM Kit, ashish141199: 9 commands) all center on daily note workflows, content capture, connection discovery, and ongoing maintenance. Our current skills have zero coverage here.

Secondary gaps include standalone vault health/linting (currently embedded in implementing-vault only) and broader content ingestion beyond .docs/ artifacts.

## Current Skill Inventory

| # | Skill | Purpose | Category |
|---|-------|---------|----------|
| 1 | brainstorming-vault | Explore vault philosophy before building | Planning |
| 2 | starting-vault | Initialize vault + MCP connectivity | Setup |
| 3 | researching-vault | Analyze vault structure and conventions | Planning |
| 4 | designing-vault | Make organizational decisions | Planning |
| 5 | structuring-vault | Map folder layout and note placement | Planning |
| 6 | planning-vault | Create phased implementation plans | Planning |
| 7 | implementing-vault | Execute plans with linting verification | Execution |
| 8 | importing-vault | Convert .docs/ artifacts to vault notes | Conversion |

**Distribution problem:** 5 planning, 1 setup, 1 execution, 1 conversion, 0 daily operations, 0 maintenance.

## Gap Analysis

### Gap 1: Daily/Periodic Operations (HIGH PRIORITY)

**What's missing:** No skills for the workflows users perform daily, weekly, or monthly with their vault.

**Community evidence:**
- ballred PKM Kit: `/daily`, `/weekly` commands with 4 agents (note-organizer, weekly-reviewer, goal-aligner, inbox-processor)
- ZanderRuss: `/daily-review`, `/weekly-synthesis`, `/inbox-processor`, `/thinking-partner`
- ashish141199: `/day` (interactive daily journaling with smart linking), `/log` (quick logging)
- ArtemXTech: `/review`, `/tasknotes`
- Claudesidian: `/daily-review`, `/weekly-synthesis`

**Potential new skills:**
- **`reviewing-vault`** — Daily/weekly/monthly review workflows. Scan recent notes, identify patterns, surface connections, generate review summaries. Supports temporal rollup (daily → weekly → monthly).
- **`capturing-vault`** — Quick note creation from various sources (web clips, voice transcripts, fleeting thoughts, meeting notes). Routes content to appropriate folder based on vault conventions. Lighter weight than importing-vault (which handles .docs/ conversion with full frontmatter translation).

### Gap 2: Connection Discovery & Graph Maintenance (HIGH PRIORITY)

**What's missing:** No skills for discovering relationships between notes, maintaining MOCs, or analyzing vault graph health.

**Community evidence:**
- ZanderRuss: `/smart-link`, `/graph-analysis`, 6 specialized agents (moc-agent, connection-agent, tag-agent)
- Corti CI/CD pattern: `/connect-notes` (reviews notes modified in last 7 days, suggests wikilinks), `/update-indexes` (refreshes MOCs), `/suggest-merges` (finds duplicates)
- Research deep dive: semantic embeddings, NetworkX analysis, hub identification, gap detection, non-obvious relationship discovery

**Potential new skill:**
- **`connecting-vault`** — Discover relationships between notes, suggest wikilinks, identify orphans needing links, maintain/update MOCs, detect duplicates. Could use MCP semantic search when available or Grep-based keyword matching as fallback.

### Gap 3: Standalone Vault Health & Linting (MEDIUM PRIORITY)

**What's missing:** Vault linting currently exists ONLY inside implementing-vault (reference: `./reference/vault-linting.md`). Cannot run health checks independently.

**Community evidence:**
- Quality control deep dive identifies 4 validation layers: broken links, frontmatter schema, orphan detection, heading structure
- Find Orphaned Files plugin: orphans, broken links, empty files
- Obsidian Linter plugin: YAML validation, heading hierarchy, spacing
- Quality gate checklist pattern: pre-operation checkpoint → post-operation review → verification
- ZanderRuss: vault-optimizer agent, 3-layer quality control (Prevention → Detection → Validation)

**Potential new skill:**
- **`linting-vault`** — Standalone vault health checks. Broken wikilinks, orphaned notes, frontmatter validation against schema, empty files, heading structure. Can run independently of any plan or implementation. Outputs actionable report. This extracts and expands the linting logic already in implementing-vault's reference files.

### Gap 4: Vault Maintenance at Scale (MEDIUM PRIORITY)

**What's missing:** No skills for batch operations on existing vault content (metadata normalization, tag cleanup, link rot detection).

**Community evidence:**
- Creative workflows deep dive: batch metadata normalization, tag cleanup/reorganization, link rot prevention, Dataview-to-Properties migration
- Obsidian Frontmatter Tool: batch validation with dry-run mode
- Tag Wrangler: batch rename/merge tags
- wayback-archiver pattern: find URLs → check snapshots → archive → output mapping

**Potential new skill:**
- **`maintaining-vault`** — Batch maintenance operations. Tag normalization, frontmatter bulk updates, link rot detection, duplicate detection, stale note identification. Always dry-run first, git checkpoint before execution. This fills the gap between "implementing a reorganization plan" and "keeping a healthy vault over time."

### Gap 5: Content Transformation (LOW PRIORITY)

**What's missing:** importing-vault only handles .docs/ → vault conversion. No skills for web clips, voice transcripts, PDFs, meeting notes, or other external content.

**Community evidence:**
- ZanderRuss: `/web-clip`, `/voice-process`, `/flashcards`, `/note-to-blog`
- ashish141199: `/resource` (capture articles/videos as linked notes)
- Content pipeline patterns: voice → structured notes, web → knowledge, RSS → summaries, Kindle highlights → connected knowledge

**Assessment:** Lower priority because many of these require external tools (Whisper, browser extensions, RSS readers) that are outside commandbase's scope. The `capturing-vault` skill from Gap 1 could handle the simpler cases. Complex pipelines may be better served by n8n workflows or external scripts.

**New finding:** kepano's defuddle skill provides CLI-based web content extraction (`defuddle parse <url> --md`) that could serve as the web clip ingestion path for capturing-vault, reducing dependence on external browser extensions. defuddle outputs clean markdown from web pages — a simpler alternative to WebFetch for vault-bound content capture.

## Revision Opportunities for Existing Skills

### implementing-vault — Extract linting + format knowledge dependency
Currently bundles vault linting as an internal reference. If `linting-vault` is created as a standalone skill, implementing-vault should delegate to it rather than duplicate the logic. implementing-vault's `./reference/vault-linting.md` becomes the seed for the new skill.

Format correctness: implementing-vault produces markdown files, frontmatter, and potentially canvas/bases files. kepano's obsidian-markdown skill (620 lines of OFM syntax) and obsidian-bases skill (651 lines with 50+ formula functions) provide the format knowledge that ensures generated files are valid. Recommend documenting kepano's obsidian plugin as a companion install for full format coverage rather than duplicating format specs in our skills.

### importing-vault — Clarify scope boundary + format awareness
If `capturing-vault` is created for lightweight note creation, importing-vault's scope should be explicitly narrowed to ".docs/ artifact conversion with full frontmatter translation and MOC integration." The two skills serve different use cases: capturing is quick and lightweight, importing is thorough and convention-aware.

importing-vault would benefit from kepano's obsidian-markdown format knowledge when generating vault notes — particularly for callout syntax (13 built-in types), embed variants, and property/frontmatter type correctness. Currently importing-vault must encode this knowledge itself; with kepano's skill installed, it can rely on the format reference for valid OFM output.

### starting-vault — MCP-optional path and multi-vault awareness
Research recommends direct filesystem as primary, MCP as supplemental. Currently starting-vault treats MCP setup as a core phase. Could offer a streamlined path that skips MCP entirely for users who only want filesystem access, with MCP as an optional enhancement step.

Additionally, kepano's obsidian-cli skill documents a `obsidian` CLI for direct vault interaction (read, create, append, search, daily notes, properties, tasks, tags, backlinks). This could offer a third interaction path alongside filesystem and MCP — particularly useful since it uses wikilink-style file targeting (`file=<name>`) that aligns with Obsidian's native addressing. Worth evaluating whether obsidian-cli replaces or supplements MCP for specific operations.

Additionally, starting-vault should support multi-vault configurations: detect single vs multi-vault setups, configure unique MCP ports per vault (Local REST API plugin requires unique ports to avoid auth errors), and recommend shared convention patterns (symlinks for CLAUDE.md, `.claude/rules/` for shared + vault-specific rules, or `claude-sync` npm package). The generated CLAUDE.md should document vault boundaries explicitly.

## Replacement Assessment

**No skills should be replaced.** All 8 current skills serve distinct purposes in the BRDSPI workflow chain. The workflow is well-structured with clear handoff points between skills. The gap is not in what exists but in what's missing.

## Proposed Skill Roster (Current + New)

| # | Skill | Status | Category |
|---|-------|--------|----------|
| 1 | brainstorming-vault | Existing | Planning |
| 2 | starting-vault | Existing (minor revision) | Setup |
| 3 | researching-vault | Existing | Planning |
| 4 | designing-vault | Existing | Planning |
| 5 | structuring-vault | Existing | Planning |
| 6 | planning-vault | Existing | Planning |
| 7 | implementing-vault | Existing (extract linting) | Execution |
| 8 | importing-vault | Existing (clarify scope) | Conversion |
| 9 | **reviewing-vault** | **NEW** | Daily Operations |
| 10 | **capturing-vault** | **NEW** | Daily Operations |
| 11 | **connecting-vault** | **NEW** | Daily Operations |
| 12 | **linting-vault** | **NEW** | Maintenance |
| 13 | **maintaining-vault** | **NEW** | Maintenance |

This brings the plugin from 8 to 13 skills, adding coverage for daily operations (3 skills) and maintenance (2 skills).

## Architecture Notes

### Two Usage Modes
The expanded skill set serves two distinct modes:
1. **Setup/Reorganization Mode** (existing BRDSPI chain): brainstorming → starting → researching → designing → structuring → planning → implementing → importing
2. **Daily Operations Mode** (new): reviewing, capturing, connecting, linting, maintaining — used independently, not in a fixed sequence

### Design Constraints
- **Desktop-only**: commandbase-vault skills are desktop-only by architecture. Mobile Obsidian sandboxes prevent CLI execution, and MCP doesn't work on Claude Mobile. Mobile serves as a capture-and-sync endpoint only.
- **Vault boundaries**: Skills must respect vault boundaries. No cross-vault operations without explicit user intent. Multi-vault setups require separate MCP instances per vault.
- **Filesystem-accessible formats**: All skills should prefer filesystem-accessible data formats (markdown, JSON sidecar) over database storage (SQLite), ensuring Claude Code's Read/Write/Edit tools can operate on the data directly.

### Format Knowledge Dependencies
Our vault skills are **workflow procedures** — they guide Claude through multi-step vault management processes. kepano's obsidian-skills are **format references** — they teach Claude what valid Obsidian files look like. These are orthogonal concerns that work together:

| Dependency | Provider (kepano) | Consumers (commandbase-vault) |
|-----------|-------------------|------------------------------|
| OFM markdown syntax | obsidian-markdown | implementing-vault, importing-vault, capturing-vault |
| Bases/database views | obsidian-bases | reviewing-vault (review dashboards), connecting-vault (relationship views) |
| Canvas spec | json-canvas | (future visual vault mapping) |
| Vault CLI | obsidian-cli | starting-vault (alternative to MCP), all read operations |
| Web extraction | defuddle | capturing-vault (web clips) |

**Recommendation:** Document kepano's `obsidian` plugin as a recommended companion install in commandbase-vault's README/setup. Don't duplicate format specs — delegate format correctness to the format reference skills. This keeps our skills focused on workflow logic while benefiting from community-maintained format knowledge.

axton's obsidian-visual-skills (Excalidraw, Mermaid, Canvas diagram generation) are also complementary but more loosely coupled — they generate visual artifacts that can live in a vault but aren't part of vault management workflows. Recommend as optional install for users who want diagram capabilities.

### Shared Infrastructure
- All new skills should use the same MCP + filesystem dual-path approach (with obsidian-cli as potential third path)
- linting-vault's logic should be callable by implementing-vault (avoid duplication)
- All skills read vault CLAUDE.md for conventions before operating
- Git safety remains mandatory for any write operations
- Format validation can delegate to kepano's format reference skills when installed

### Community Skill Comparison
- ZanderRuss (29 commands + 16 agents): Most comprehensive, but includes academic research pipeline (11 commands) outside our scope
- ballred PKM Kit: Closest to our target — focused on daily workflows with 4 agents
- ashish141199 (9 commands): Entry-level, good inspiration for capturing-vault
- kepano (5 skills, 2,071 lines): **Complementary format references**, not competing workflow skills. Three format references (obsidian-markdown: 620 lines OFM syntax, obsidian-bases: 651 lines database views, json-canvas: 656 lines canvas spec) + two tool references (obsidian-cli: vault CLI commands, defuddle: web content extraction). Teaches Claude *what valid files look like*, not *how to manage a vault*. Key integration point: our workflow skills produce files whose format correctness benefits from kepano's format skills being installed alongside commandbase-vault. See "Format Knowledge Dependencies" below.
- axton (3 skills, single plugin): **Visual diagram generation** — Excalidraw (437 lines, 3 output modes), Mermaid (273 lines, 64 config combinations), Canvas (204 lines + 1,019 lines of references). Output-focused (generate visual files from text descriptions), not management-focused. Notable patterns: multi-mode skills triggered by keyword detection, template-driven output via example .canvas files, heavy use of `references/` subdirectories for specs. Out of scope for vault management but complementary — users wanting diagram capabilities should install axton's plugin separately.

## Open Questions
- Should reviewing-vault support configurable review cadences (daily/weekly/monthly) or should each cadence be a separate skill?
- How should connecting-vault handle semantic search — require MCP, or fall back to Grep-based keyword matching?
- Should linting-vault produce a .docs/ artifact or just output to the user?
- Is 13 skills too many for one plugin? Should daily operations become a separate commandbase-vault-daily plugin?
- Should commandbase-vault formally declare kepano's obsidian plugin as a recommended dependency, or keep format knowledge loosely coupled? (kepano's skills are MIT-licensed and actively maintained with community PRs)
- Should starting-vault offer obsidian-cli as a vault interaction path alongside/instead of MCP? The CLI provides wikilink-style file targeting and plugin dev tools that MCP doesn't cover.
- Could obsidian-bases enable a "vault dashboard" capability in reviewing-vault? Bases can create database views (task trackers, daily note indexes) that would enhance review workflows.
