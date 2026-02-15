---
date: 2026-02-12
status: active
topic: "Session Learnings: vault-skill-refinement"
tags: [learnings, vault-skill-refinement, obsidian, plugin-design, reference-files, safety-protocol, skill-architecture]
git_commit: 2394de1
references:
  - plugins/commandbase-vault/skills/linting-vault/SKILL.md
  - plugins/commandbase-vault/skills/capturing-vault/SKILL.md
  - plugins/commandbase-vault/skills/maintaining-vault/SKILL.md
  - plugins/commandbase-vault/skills/starting-vault/SKILL.md
  - plugins/commandbase-vault/skills/connecting-vault/SKILL.md
  - plugins/commandbase-vault/skills/reviewing-vault/SKILL.md
---

# Session Learnings: vault-skill-refinement

## Error Summary

From `.claude/sessions/vault-skill-refinement/errors.log` (79 entries):
- All errors were WebFetch/Brave search failures against paywalled Medium articles or missing GitHub pages — expected behavior during broad research sweeps, not actionable.
- No tool errors during implementation phases.

## Discoveries

### 1. Split shared format knowledge into use-case-specific reference files

**Problem:** Multiple vault skills need Obsidian Flavored Markdown (OFM) knowledge — linting needs validation rules, capturing needs creation templates. The initial instinct was a single monolithic OFM reference file.

**What was non-obvious:** A single reference file bloats every skill that includes it with irrelevant content. Linting doesn't need note creation templates; capturing doesn't need validation regex patterns. The split isn't by topic (OFM) but by use case (validate vs create).

**What would help next time:** When multiple skills share domain knowledge, split reference files by *how the knowledge is used*, not by *what the knowledge is about*:
- `ofm-validation-rules.md` (linting-vault) — regex patterns, structural rules, error detection
- `ofm-note-formats.md` (capturing-vault) — templates, frontmatter schemas, format examples

This pattern applies to any plugin where skills share overlapping domain knowledge.

**Trigger conditions:** Designing a new skill that needs reference material already partially covered by another skill's reference files.

### 2. Filesystem-first design over MCP for vault access

**Problem:** starting-vault initially assumed MCP (obsidian-mcp-tools via Local REST API plugin) was the primary access path. Research revealed multi-vault users hit a wall: Local REST API binds to one port per vault, requiring unique port configuration per vault.

**What was non-obvious:** MCP adds a layer of complexity with marginal benefit for most vault operations. Claude Code already has filesystem access — Read, Write, Edit, Glob, Grep all work directly on vault files. MCP's value is limited to Obsidian-specific operations (search_vault_smart, execute_template) that have no filesystem equivalent.

**What would help next time:** Default to filesystem-first for file operations. Only add MCP as an optional enhancement for operations that genuinely require Obsidian's runtime (smart search, template execution, showing files in the app). Test: "Can I do this with Read/Write/Glob?" — if yes, don't require MCP.

**Trigger conditions:** Designing any skill that integrates with a tool that has both an API/MCP and a filesystem representation.

### 3. Three-layer safety protocol for batch vault operations

**Problem:** maintaining-vault performs bulk operations (rename, reorganize, archive) that can damage hundreds of notes. A simple "are you sure?" confirmation is insufficient for operations affecting 50+ files.

**What was non-obvious:** The right safety model isn't binary (safe/unsafe) but graduated:
1. **Dry-run first** — show what would change without changing anything
2. **Git checkpoint** — create a commit before any modifications so rollback is one command
3. **Chunked processing** — process in 20-note batches with pause points between chunks

The 20-note chunk size emerged from balancing context window limits against meaningful progress per batch.

**What would help next time:** For any batch operation affecting >10 files, implement the three-layer protocol. The pattern is reusable beyond vault skills — any destructive batch operation (bulk refactoring, mass file moves, tag migrations) benefits from dry-run → checkpoint → chunked execution.

**Trigger conditions:** Any skill that modifies more than 10 files in a single invocation.

### 4. Bake domain knowledge into reference files rather than depending on external plugins

**Problem:** kepano's obsidian-skills plugin already had comprehensive OFM format knowledge. The question was whether to depend on it or duplicate the knowledge.

**What was non-obvious:** External plugin dependencies create adoption friction — users must install the dependency first, versions must stay compatible, and if the external plugin changes structure, downstream skills break. For domain knowledge (as opposed to runtime functionality), self-contained reference files are strictly better.

**What would help next time:** Decision framework:
- **Runtime dependency** (needs the plugin's tools/hooks at execution time) → acceptable dependency
- **Knowledge dependency** (needs the plugin's reference content at design time) → bake it in, cite the source

**Trigger conditions:** Designing a plugin that could reuse content from another plugin's reference files or documentation.

### 5. Check for daily-use gaps when designing a skill suite

**Problem:** The original 8 vault skills covered setup (starting-vault, scaffolding-vault), bulk operations (implementing-vault, importing-vault), and knowledge architecture (designing-vault, researching-vault, planning-vault, auditing-vault). Zero skills for what users do every day.

**What was non-obvious:** The skill suite was designed around the RPI workflow (research, plan, implement) which is episodic. Daily vault use is habitual — quick capture, review, connection-building, maintenance. Community repo analysis (ZanderRuss: 29 commands, ballred PKM Kit) revealed the blind spot: the most-used operations had no skill coverage.

**What would help next time:** After designing a skill suite, run a gap check: "What does a user do with this tool on a normal Tuesday?" If the answer doesn't map to any existing skill, there's a daily-use gap. The 5 new skills (capturing, reviewing, connecting, maintaining, linting) all fill daily/weekly operations.

**Trigger conditions:** Completing initial design of any skill plugin with 5+ skills. Run the Tuesday test before considering the suite complete.

## Deferred Actions

- [ ] Consider creating a plugin design guide skill: reference file architecture patterns (discovery 1), dependency decisions (discovery 4), daily-use gap testing (discovery 5)
- [x] Added filesystem-first architecture section to commandbase-vault README (discovery 2)
- [x] Updated creating-skills: added "reference file splitting by use case" pattern in Step 4 and "Tuesday test" in Step 1 (discovery 1, 5)
- [x] Created commandbase-core/reference/batch-safety-protocol.md with generalized three-layer pattern; updated maintaining-vault to reference it (discovery 3)
- [x] Added chunk size rationale and adjustment guidance to maintaining-vault batch-safety-protocol.md (discovery 3, 5)
