---
date: 2026-02-12
status: complete
topic: "Vault Skills Expansion: 5 New Skills + 3 Existing Skill Revisions"
tags: [plan, implementation, vault-skills, commandbase-vault, obsidian, creating-skills]
git_commit: 9c4c7f4
references:
  - plugins/commandbase-vault/skills/implementing-vault/SKILL.md
  - plugins/commandbase-vault/skills/importing-vault/SKILL.md
  - plugins/commandbase-vault/skills/starting-vault/SKILL.md
  - plugins/commandbase-vault/.claude-plugin/plugin.json
  - plugins/commandbase-vault/README.md
  - plugins/commandbase-meta/skills/creating-skills/SKILL.md
  - .docs/research/02-12-2026-vault-skills-gap-analysis-current-state-vs-research-recommendations.md
---

# Vault Skills Expansion: 5 New Skills + 3 Existing Skill Revisions

## Overview

Expand commandbase-vault from 8 to 13 skills based on the gap analysis at `.docs/research/02-12-2026-vault-skills-gap-analysis-current-state-vs-research-recommendations.md`. Create 5 new skills for daily operations and maintenance, revise 3 existing skills, and update the plugin manifest and README.

All skill creation and editing uses `/creating-skills` (Mode 1: Create, Mode 2: Edit). One invocation per phase.

## Resolved Design Decisions

These were debated and settled before planning:

| Decision | Resolution |
|----------|-----------|
| Review cadences | Single reviewing-vault skill with daily/weekly/monthly modes |
| Semantic search | MCP-preferred, Grep-based keyword matching fallback |
| Lint output | Direct output by default, ask user if they want saved to .docs/ |
| Plugin split | Single commandbase-vault plugin (13 skills), README organized into Construction/Operations sections |
| kepano dependency | No external dependency. Bake relevant OFM format knowledge into our own reference files |
| obsidian-cli | Skip. Keep filesystem + MCP dual-path only |
| Starting-vault MCP | Make MCP optional (filesystem-first), add multi-vault awareness |

## What We're NOT Doing

- No new agents (only skills)
- No plugin split (staying as single commandbase-vault)
- No obsidian-cli integration
- No kepano plugin dependency — we bake format knowledge ourselves
- No changes to brainstorming-vault, researching-vault, designing-vault, structuring-vault, or planning-vault
- No changes to commandbase-core or other plugins

## Phase 1: Create linting-vault (standalone vault health checks)

**Why first:** Other new skills (maintaining-vault) and the implementing-vault revision depend on linting-vault existing.

**Invoke:** `/creating-skills` Mode 1 (Create New Skill)

**Skill specification:**
- **Name:** `linting-vault`
- **Template:** Workflow (multi-mode: targeted lint vs full vault lint)
- **Freedom tier:** Low (error-prone validation, exact procedures matter)
- **Description formula:** "Use this skill when checking vault health, validating note quality, or running vault-wide linting checks. This includes detecting broken wikilinks, validating frontmatter against schema, finding orphaned notes with no incoming links, checking heading structure, identifying empty files, and generating actionable health reports. Activate when the user says 'lint vault', 'check vault health', 'find broken links', 'validate frontmatter', or 'run vault checks'."

**Content sources:**
- Seed from `plugins/commandbase-vault/skills/implementing-vault/reference/vault-linting.md` (4 check types: broken wikilinks, frontmatter validation, orphan detection, heading structure)
- Expand with: empty file detection, duplicate note detection, tag consistency checks
- Research: quality control deep dive (4 validation layers), Obsidian Linter plugin patterns, ZanderRuss 3-layer quality control

**Modes:**
- Mode A: Targeted lint (specific notes/folders, after operations)
- Mode B: Full vault lint (comprehensive health report)

**Reference files needed:**
- `reference/lint-checks.md` — Detailed procedures for each check type (expanded from implementing-vault's vault-linting.md)
- `reference/ofm-validation-rules.md` — Obsidian Flavored Markdown validation rules (baked from kepano research: frontmatter constraints, wikilink syntax, callout types, heading rules)

**Output behavior:** Direct output by default. After presenting results, ask: "Would you like me to save this report to .docs/vault-health/?"

**Iron Law:** NO LINT REPORT WITHOUT READING VAULT CLAUDE.MD FIRST (frontmatter schema and conventions come from there)

**Success criteria:**
- [x] SKILL.md created at `plugins/commandbase-vault/skills/linting-vault/SKILL.md`
- [x] reference/lint-checks.md created with all check procedures
- [x] reference/ofm-validation-rules.md created with OFM format rules
- [x] Description passes 4C check and validation rules
- [x] SKILL.md under 500 lines (153 lines)
- [x] All checks from creating-skills validation-rules.md pass

## Phase 2: Edit implementing-vault (delegate linting to linting-vault)

**Invoke:** `/creating-skills` Mode 2 (Edit Existing Skill)

**Changes:**
1. Update the "Vault Linting" section (lines 98-106) to delegate to linting-vault:
   - Replace inline linting instructions with: "Run `/linting-vault` in targeted mode on notes affected by this phase. See linting-vault for the full check procedures."
   - Keep the Gate Function step 4 (LINT) but change it to reference linting-vault
2. Update the Execution Flow step 2 to say "Run `/linting-vault` targeted on affected notes"
3. Keep `reference/vault-linting.md` as-is for backward compatibility (it's the seed, not a duplicate — linting-vault expands on it)
4. Do NOT change the description — implementing-vault still mentions "running vault linting validation" which is accurate (it delegates, not removes)

**Success criteria:**
- [x] implementing-vault SKILL.md updated to delegate linting to linting-vault
- [x] reference/vault-linting.md preserved (not deleted)
- [x] No description change needed
- [x] SKILL.md still under 500 lines (185 lines)
- [x] Validation passes

## Phase 3: Create reviewing-vault (daily/weekly/monthly review workflows)

**Invoke:** `/creating-skills` Mode 1 (Create New Skill)

**Skill specification:**
- **Name:** `reviewing-vault`
- **Template:** Workflow (multi-mode: daily/weekly/monthly cadences)
- **Freedom tier:** Medium (review patterns vary, but cadence structure is fixed)
- **Description formula:** "Use this skill when performing periodic vault reviews to surface patterns, track progress, and maintain knowledge freshness. This includes daily note reviews scanning recent additions, weekly synthesis connecting themes across notes, monthly retrospectives identifying stale or orphaned content, and generating review summaries with actionable insights. Activate when the user says 'review vault', 'daily review', 'weekly synthesis', 'what changed this week', or 'vault retrospective'."

**Content sources:**
- Research: ballred PKM Kit (/daily, /weekly with 4 agents), ZanderRuss (/daily-review, /weekly-synthesis), ashish141199 (/day interactive journaling)
- Creative workflows deep dive: daily automation, task scanning, research digests

**Modes:**
- Mode A: Daily review (notes created/modified today, quick scan, surface connections)
- Mode B: Weekly synthesis (broader pattern detection, theme clustering, MOC updates needed)
- Mode C: Monthly retrospective (stale note identification, orphan detection, tag drift, progress against goals)

**Reference files needed:**
- `reference/review-cadence-guide.md` — What to check at each cadence level, temporal rollup patterns (daily → weekly → monthly)

**Iron Law:** NO REVIEW WITHOUT READING VAULT CLAUDE.MD FIRST (need conventions to evaluate health)

**Success criteria:**
- [x] SKILL.md created at `plugins/commandbase-vault/skills/reviewing-vault/SKILL.md`
- [x] reference/review-cadence-guide.md created
- [x] Three modes clearly defined (daily/weekly/monthly)
- [x] Description passes 4C check
- [x] SKILL.md under 500 lines (153 lines)
- [x] Validation passes

## Phase 4: Create capturing-vault (quick note creation from various sources)

**Invoke:** `/creating-skills` Mode 1 (Create New Skill)

**Skill specification:**
- **Name:** `capturing-vault`
- **Template:** Workflow (multi-mode: by source type)
- **Freedom tier:** Medium (routing conventions vary, but capture format is structured)
- **Description formula:** "Use this skill when quickly capturing content into the vault from various sources. This includes creating fleeting notes from ideas or thoughts, capturing web content as vault notes, logging meeting notes or voice transcript summaries, processing inbox items into proper vault notes, and routing captured content to appropriate folders based on vault conventions. Activate when the user says 'capture to vault', 'quick note', 'save this to vault', 'clip this', 'process inbox', or 'log to vault'."

**Content sources:**
- Research: ashish141199 (/day, /log, /resource), ballred (inbox-processor agent), ZanderRuss (/web-clip)
- Gap analysis: lighter weight than importing-vault (which handles .docs/ conversion with full frontmatter translation)
- kepano defuddle: web content extraction via WebFetch (no CLI dependency, use WebFetch tool instead)

**Modes:**
- Mode A: Fleeting note (quick idea capture, minimal frontmatter, inbox/triage folder)
- Mode B: Web capture (URL → clean markdown → vault note with source attribution)
- Mode C: Meeting/log capture (structured template with date, participants, action items)
- Mode D: Inbox processing (review triage/inbox folder, route notes to proper locations)

**Scope boundary with importing-vault:**
- capturing-vault: Quick, lightweight, single-note creation from external content
- importing-vault: Thorough .docs/ artifact conversion with full frontmatter translation and MOC integration

**Reference files needed:**
- `reference/capture-routing-rules.md` — How to determine where a captured note goes based on vault conventions
- `reference/ofm-note-formats.md` — Valid Obsidian note format patterns (frontmatter types, wikilink syntax, callout types) for captured content. Baked from kepano research.

**Iron Law:** NO CAPTURE WITHOUT READING VAULT CONVENTIONS FIRST (need folder structure and frontmatter schema to route correctly)

**Success criteria:**
- [x] SKILL.md created at `plugins/commandbase-vault/skills/capturing-vault/SKILL.md`
- [x] reference/capture-routing-rules.md created
- [x] reference/ofm-note-formats.md created
- [x] Four modes clearly defined
- [x] Scope boundary with importing-vault documented
- [x] Description passes 4C check
- [x] SKILL.md under 500 lines (146 lines)
- [x] Validation passes

## Phase 5: Create connecting-vault (relationship discovery and MOC maintenance)

**Invoke:** `/creating-skills` Mode 1 (Create New Skill)

**Skill specification:**
- **Name:** `connecting-vault`
- **Template:** Workflow (multi-mode: by connection task)
- **Freedom tier:** Medium (discovery is exploratory, but MOC updates are structured)
- **Description formula:** "Use this skill when discovering relationships between vault notes, maintaining Maps of Content, or improving vault connectivity. This includes suggesting wikilinks between related notes, identifying orphaned notes needing connections, updating or generating MOCs, detecting duplicate or near-duplicate notes, and analyzing link graph density. Activate when the user says 'connect notes', 'find related notes', 'update MOC', 'find orphans', 'link suggestions', or 'vault graph analysis'."

**Content sources:**
- Research: ZanderRuss (/smart-link, /graph-analysis, 6 agents), Corti CI/CD (/connect-notes, /update-indexes, /suggest-merges)
- Connection discovery deep dive: semantic embeddings, keyword matching, hub identification, gap detection

**Modes:**
- Mode A: Link suggestions (scan recent/specified notes, suggest wikilinks to existing notes)
- Mode B: Orphan rescue (find notes with 0 incoming links, suggest connections)
- Mode C: MOC maintenance (refresh existing MOCs with new notes, or generate MOC for a topic cluster)
- Mode D: Duplicate detection (find notes with similar titles/content, suggest merges)

**Search strategy:** MCP search first (semantic if available), Grep-based keyword/tag matching as fallback. Document the dual-path approach in the skill.

**Reference files needed:**
- `reference/connection-strategies.md` — Techniques for finding connections: keyword overlap, shared tags, temporal proximity, frontmatter field matching, heading similarity

**Iron Law:** NO CONNECTION SUGGESTIONS WITHOUT VERIFYING TARGET NOTES EXIST (don't suggest links to non-existent notes)

**Success criteria:**
- [x] SKILL.md created at `plugins/commandbase-vault/skills/connecting-vault/SKILL.md`
- [x] reference/connection-strategies.md created
- [x] Four modes clearly defined
- [x] MCP-preferred + Grep fallback documented
- [x] Description passes 4C check
- [x] SKILL.md under 500 lines (158 lines)
- [x] Validation passes

## Phase 6: Create maintaining-vault (batch maintenance operations)

**Invoke:** `/creating-skills` Mode 1 (Create New Skill)

**Skill specification:**
- **Name:** `maintaining-vault`
- **Template:** Workflow (multi-mode: by maintenance operation)
- **Freedom tier:** Low (batch operations are risky, exact procedures and safety gates matter)
- **Description formula:** "Use this skill when performing batch maintenance operations on vault content. This includes normalizing tags across notes, bulk-updating frontmatter properties, detecting and fixing link rot, identifying stale notes needing review, cleaning up empty or placeholder notes, and running batch metadata corrections. Activate when the user says 'maintain vault', 'normalize tags', 'bulk update frontmatter', 'find stale notes', 'clean up vault', or 'fix link rot'."

**Content sources:**
- Research: creative workflows deep dive (batch metadata normalization, tag cleanup), Obsidian Frontmatter Tool (dry-run mode), Tag Wrangler (batch rename/merge)
- Gap analysis: fills gap between "implementing a reorganization plan" and "keeping healthy vault over time"

**Modes:**
- Mode A: Tag normalization (rename, merge, or reorganize tags across notes)
- Mode B: Frontmatter bulk update (add/modify/remove properties across matching notes)
- Mode C: Link rot detection (find external URLs that are dead, suggest fixes)
- Mode D: Stale note identification (find notes not modified in N days, surface for review)
- Mode E: Cleanup (empty files, placeholder-only notes, duplicate content)

**Safety gates:**
- ALWAYS dry-run first (show what would change, don't change it)
- ALWAYS git checkpoint before execution (`/bookmarking-code create "pre-maintenance"`)
- Present changes for user approval before applying
- Batch size limits (process in chunks of 20 notes, verify between chunks)

**Reference files needed:**
- `reference/maintenance-operations.md` — Detailed procedures for each operation type, including Grep/Glob patterns for finding affected notes
- `reference/batch-safety-protocol.md` — Dry-run format, checkpoint requirements, chunk processing rules, rollback procedures

**Iron Law:** NO BATCH CHANGES WITHOUT DRY-RUN AND CHECKPOINT FIRST

**Success criteria:**
- [x] SKILL.md created at `plugins/commandbase-vault/skills/maintaining-vault/SKILL.md`
- [x] reference/maintenance-operations.md created
- [x] reference/batch-safety-protocol.md created
- [x] Five modes clearly defined with safety gates
- [x] Dry-run and checkpoint requirements are non-negotiable in the skill
- [x] Description passes 4C check
- [x] SKILL.md under 500 lines (175 lines)
- [x] Validation passes

## Phase 7: Edit importing-vault (clarify scope boundary)

**Invoke:** `/creating-skills` Mode 2 (Edit Existing Skill)

**Changes:**
1. Add a "Scope Boundary" section after the Iron Law that explicitly differentiates from capturing-vault:
   ```
   ## Scope Boundary

   This skill handles `.docs/` artifact conversion with full frontmatter translation and MOC integration.
   For quick note creation from external sources (web clips, fleeting thoughts, meeting notes),
   use `/capturing-vault` instead.

   | Aspect | /importing-vault (this skill) | /capturing-vault |
   |--------|-------------------------------|-----------------|
   | Source | .docs/ artifacts only | Any external content |
   | Depth | Full frontmatter translation, MOC integration | Minimal frontmatter, inbox routing |
   | Speed | Thorough, convention-aware | Quick, lightweight |
   | Review | User reviews before placement | Routes to inbox/triage folder |
   ```
2. Do NOT change the description — importing-vault's description is already correctly scoped to ".docs/ artifacts"
3. Do NOT change the workflow — only add the scope boundary clarification

**Success criteria:**
- [x] Scope boundary section added to importing-vault SKILL.md
- [x] No description change
- [x] No workflow change
- [x] Comparison table with capturing-vault included
- [x] SKILL.md still under 500 lines (197 lines)
- [x] Validation passes

## Phase 8: Edit starting-vault (MCP-optional path + multi-vault awareness)

**Invoke:** `/creating-skills` Mode 2 (Edit Existing Skill)

**Changes:**
1. **Update the Iron Law** from "NO VAULT SETUP WITHOUT TESTING CONNECTIVITY FIRST" to "NO VAULT SETUP WITHOUT VERIFYING ACCESS FIRST" — broader than just MCP connectivity
2. **Update the Gate Function** to support filesystem-only path:
   - Step 1: DISCOVER (unchanged)
   - Step 2: CHOOSE ACCESS PATH (new): filesystem-only or filesystem + MCP
   - Step 3: CONFIGURE (MCP setup if chosen, skip if filesystem-only)
   - Step 4: TEST (verify vault path exists for filesystem; test MCP connectivity if configured)
   - Step 5: CREATE CLAUDE.md (adapted to access path)
3. **Update Phase 1 Round 2** to ask about access path preference:
   - "Filesystem only (no plugins needed, works immediately)"
   - "Filesystem + MCP (adds search and metadata tools, requires Obsidian Local REST API plugin)"
4. **Add multi-vault awareness** to Phase 1 Round 1:
   - "Do you have multiple vaults? (Single vault, Multiple vaults)"
   - If multiple: ask about shared conventions, unique MCP ports per vault, vault boundary rules
5. **Update Phase 2** to be conditional on MCP being chosen
6. **Update Phase 3** to test appropriate path (filesystem: verify vault path exists via Glob; MCP: test connectivity)
7. **Update Phase 5 wrap-up** to show Operations skills alongside Construction BRDSPI:
   - Add: "Daily operations: /reviewing-vault, /capturing-vault, /connecting-vault"
   - Add: "Maintenance: /linting-vault, /maintaining-vault"
8. **Update description** to remove MCP-specific language. New description:
   "Use this skill when initializing a new Obsidian vault for Claude Code management or configuring Claude Code to work with an existing vault. This includes discovering vault path, choosing an access method (filesystem or MCP), configuring connectivity, supporting multi-vault setups, creating vault-aware CLAUDE.md, and verifying access. Activate when the user says 'start a vault', 'set up vault', 'configure obsidian', 'connect to vault', or before running vault workflows."
9. **Update reference/mcp-setup-guide.md** to note it only applies when MCP path is chosen

**Success criteria:**
- [x] Iron Law updated to broader "verifying access" language
- [x] Gate Function updated with access path choice
- [x] Filesystem-only path works without MCP setup
- [x] Multi-vault questions added to discovery phase
- [x] Phase 5 lists both Construction and Operations skills
- [x] Description updated to remove MCP-specific language
- [x] SKILL.md still under 500 lines (216 lines)
- [x] Validation passes

## Phase 9: Update plugin manifest + README

**No `/creating-skills` invocation** — this is plugin configuration, not skill authoring.

**Changes to `plugins/commandbase-vault/.claude-plugin/plugin.json`:**
- No structural changes needed — the plugin manifest is minimal (name, version, description)
- Update description to mention both construction and operations:
  "Vault BRDSPI workflow plus daily operations for Obsidian vault management — brainstorm, research, design, structure, plan, implement chain, plus reviewing, capturing, connecting, linting, and maintaining. Requires commandbase-core for docs agents."

**Changes to `plugins/commandbase-vault/README.md`:**
- Reorganize skills table into two sections: "Construction (BRDSPI)" and "Operations (Daily Use)"
- Add the 5 new skills to the Operations section
- Note the 3 revised skills in the Construction section
- Add a "Companion Skills" section noting kepano's format knowledge is baked into our reference files
- Update skill count from 8 to 13

**Changes to `.claude-plugin/marketplace.json` (root level):**
- Update commandbase-vault description to match plugin.json

**Changes to root `CLAUDE.md`:**
- Update `commandbase-vault` line in Directory Structure to show "8 skills" → "13 skills"

**Success criteria:**
- [x] plugin.json description updated
- [x] README reorganized with Construction/Operations sections
- [x] All 13 skills listed in README
- [x] marketplace.json description updated
- [x] Root CLAUDE.md skill count updated
- [x] No other plugins affected

## Execution Notes

### Invocation pattern
Each phase (except Phase 9) is executed as a separate `/creating-skills` invocation:
- Phases 1, 3, 4, 5, 6: Mode 1 (Create New Skill)
- Phases 2, 7, 8: Mode 2 (Edit Existing Skill)
- Phase 9: Direct file edits (no /creating-skills needed)

### Research inputs for /creating-skills
When invoking `/creating-skills`, pass these research files as context:
- `.docs/research/02-12-2026-vault-skills-gap-analysis-current-state-vs-research-recommendations.md`
- `.docs/research/02-12-2026-obsidian-vault-management-with-claude-summary.md` (for format knowledge, workflow patterns)
- Relevant deep dives for specific skills (e.g., quality control deep dive for linting-vault)

### OFM format knowledge to bake
The following format knowledge from kepano research should be baked into our reference files (not depend on external plugin):
- Wikilink syntax: `[[Note]]`, `[[Note|Alias]]`, `[[Note#Heading]]`, `[[Note#^block-id]]`
- Embed syntax: `![[Note]]`, `![[image.png|640x480]]`
- Callout types: 13 built-in (note, abstract, info, todo, tip, success, question, warning, failure, danger, bug, example, quote)
- Frontmatter constraints: no nested YAML, 6 supported types (text, list, number, checkbox, date, date+time), global type registry
- Block references: `^block-id` syntax
- Comments: `%%hidden%%`
- Highlight: `==text==`

### Shared reference file strategy
- linting-vault gets `reference/ofm-validation-rules.md` (validation-focused OFM rules)
- capturing-vault gets `reference/ofm-note-formats.md` (creation-focused OFM patterns)
- These are complementary views of the same format knowledge, tailored to each skill's use case
- implementing-vault keeps its existing `reference/vault-linting.md` as-is (backward compatible)

### Dependencies between phases
- Phase 2 (edit implementing-vault) depends on Phase 1 (linting-vault exists to delegate to)
- Phase 7 (edit importing-vault) depends on Phase 4 (capturing-vault exists for scope boundary reference)
- Phase 8 (edit starting-vault) depends on all new skills being created (Phase 5 wrap-up lists them)
- Phase 9 depends on all skill creation/editing being complete
- Phases 1, 3, 4, 5, 6 are independent of each other (but sequential ordering helps maintain context)
