---
date: 2026-02-08
status: complete
topic: "cross-referencing-research-skill-analysis"
tags: [research, skills, cross-referencing, synthesis, meta-analysis]
git_commit: 7f0eb8e
references:
  - plugins/commandbase-code/skills/researching-code/SKILL.md
  - plugins/commandbase-research/skills/researching-web/SKILL.md
  - plugins/commandbase-research/skills/researching-frameworks/SKILL.md
  - plugins/commandbase-research/skills/researching-repo/SKILL.md
  - plugins/commandbase-vault/skills/researching-vault/SKILL.md
  - plugins/commandbase-services/skills/researching-services/SKILL.md
  - plugins/commandbase-core/agents/docs-locator.md
  - plugins/commandbase-core/agents/docs-analyzer.md
  - plugins/commandbase-core/agents/docs-writer.md
  - plugins/commandbase-core/agents/docs-updater.md
  - plugins/commandbase-research/agents/web-researcher.md
---

# Cross-Referencing Research Skill Analysis

**Date**: 2026-02-08
**Branch**: master

## Research Question
How do existing research skills work, and what would a new skill that cross-references and draws conclusions from multiple research files need to look like?

## Summary
The commandbase system has 6 research skills across 4 plugins, each producing standalone `.docs/research/MM-DD-YYYY-description.md` files. All follow the Iron Law (no synthesis without parallel research) and mandatory file output. However, no existing skill reads ACROSS previously-written research files to find patterns, contradictions, or emergent insights. The gap is clear: individual research creates files, but nothing connects them after the fact.

## Detailed Findings

### Existing Research Skills Inventory

| Skill | Plugin | Domain | Sources | Output |
|-------|--------|--------|---------|--------|
| `/researching-code` | commandbase-code | Codebase | code-locator, code-analyzer, code-librarian, docs-locator, docs-analyzer | `.docs/research/` |
| `/researching-web` | commandbase-research | Web | 2-4 web-researcher agents | `.docs/research/` |
| `/researching-frameworks` | commandbase-research | Frameworks | Context7 MCP + web-researcher | `.docs/references/` (3 files) |
| `/researching-repo` | commandbase-research | External repos | code-locator, code-analyzer (on clone) | `.docs/research/` |
| `/researching-vault` | commandbase-vault | Obsidian vaults | MCP tools or file-system tools | `.docs/research/` |
| `/researching-services` | commandbase-services | Docker/homelab | file-system tools + optional Docker CLI | `.docs/research/` |

### Universal Patterns Across All Research Skills

1. **The Iron Law**: NO SYNTHESIS WITHOUT PARALLEL RESEARCH FIRST — enforced in all 6 skills
2. **Mandatory File Output**: Every research invocation produces a `.docs/research/` or `.docs/references/` file via docs-writer agent
3. **Gate Function**: 6-9 step pre-flight checklist enforcing SPAWN → WAIT → VERIFY → WRITE → PRESENT
4. **Evidence Requirements**: Every claim needs specific references (file:line for code, URLs for web, note paths for vault)
5. **Minimum 2 Agents**: All skills spawn at least 2 parallel research agents
6. **Rationalization Prevention**: Two-column Excuse|Reality tables prevent shortcuts
7. **Red Flags**: Lists of warning signs that trigger STOP-and-verify behavior

### Existing Cross-Referencing Capabilities

Cross-referencing exists but is INTRA-session only — within a single research invocation:

- **`/researching-web`**: Cross-references multiple web sources for conflicts, ranks by authority tier
- **`/researching-frameworks`**: Cross-references Context7 docs against web findings, builds compatibility matrices
- **`/researching-services`**: Cross-references repo compose files against live Docker state
- **`/researching-code`**: Connects findings across components via multiple agent types

**No existing skill performs INTER-file cross-referencing** — reading multiple previously-written `.docs/research/` files and finding patterns between them.

### Supporting Agent Capabilities

| Agent | Can Read Multiple Docs? | Can Compare? | Can Write? |
|-------|------------------------|--------------|------------|
| `docs-locator` | Yes (finds by topic) | No (discovery only) | No |
| `docs-analyzer` | Yes (reads fully) | Partial (staleness, validity) | No |
| `docs-updater` | Yes (checks references) | Partial (current vs stale) | Yes (updates/archives) |
| `docs-writer` | No (creates only) | No | Yes (new files) |
| `web-researcher` | No (web only) | Yes (source conflicts) | No |

**Key insight**: `docs-analyzer` is the closest to what's needed — it extracts decisions, constraints, learnings, and file references from individual documents. But it operates on ONE document at a time and returns structured insights. It doesn't compare findings across documents.

### The Gap: What's Missing

1. **No multi-document synthesis**: Individual research files are created but never systematically cross-referenced
2. **No pattern detection across files**: Similar findings in different research documents aren't connected
3. **No contradiction detection**: Conflicting conclusions across research files go unnoticed
4. **No temporal analysis**: How findings evolve over time (same topic researched weeks apart) isn't tracked
5. **No tag-based clustering**: Documents share tags but nothing groups related documents by shared tags
6. **No citation graph**: Research files don't reference each other, creating isolated knowledge islands

### Existing Infrastructure That Would Support Cross-Referencing

1. **Frontmatter metadata**: Every `.docs/` file has `date`, `status`, `topic`, `tags`, `git_commit`, `references` — this is queryable structure
2. **`docs-locator` agent**: Already finds documents by topic across all `.docs/` subdirectories — could be the discovery layer
3. **`docs-analyzer` agent**: Already extracts key decisions, constraints, learnings — could be the extraction layer
4. **`docs-writer` agent**: Already creates standardized output files — could write the synthesis document
5. **Tag system**: Documents already have tags in frontmatter — enables clustering by shared tags
6. **Standardized sections**: All research docs have Summary, Detailed Findings, Code References, Open Questions — enables structured comparison

### Design Considerations for a Cross-Referencing Skill

#### Input Modes
- **Tag-based**: "Cross-reference all research tagged with `skills`" — uses `docs-locator` to find by tag
- **Topic-based**: "Cross-reference research about authentication" — uses `docs-locator` to find by topic/content
- **Explicit list**: "Cross-reference these 3 files: ..." — user provides paths
- **Temporal**: "Cross-reference all research from the last week" — uses `date` frontmatter
- **All**: "Cross-reference everything in `.docs/research/`" — full sweep

#### Process Architecture
1. **Discovery phase**: Use `docs-locator` to find relevant documents
2. **Extraction phase**: Spawn parallel `docs-analyzer` agents (one per document or batch)
3. **Comparison phase**: Main context synthesizes extracted insights, looking for:
   - Shared conclusions across documents
   - Contradictions or conflicts
   - Evolution of understanding over time
   - Gaps (questions raised in one doc, answered in another)
   - Emergent patterns not visible in any single document
4. **Output phase**: Use `docs-writer` to create synthesis document

#### Output Format
A new document type or subtype:
- Location: `.docs/research/MM-DD-YYYY-cross-reference-<topic>.md`
- Sections: Source Documents, Shared Findings, Contradictions, Evolution, Emergent Patterns, Gaps Filled, Remaining Questions
- Each finding attributed to specific source documents

#### Key Design Decisions
- **Agent model**: `docs-analyzer` runs on sonnet — adequate for extraction. Main synthesis runs in skill context (opus). This is the right split.
- **Scalability**: With many research files, batch documents into groups of 3-5 per `docs-analyzer` agent to avoid context overflow
- **Freshness**: Should stale documents be included? Decision: yes, but flag staleness in output and note how many commits behind
- **Plugin placement**: Fits in `commandbase-research` alongside `/researching-web` and `/researching-frameworks`, or in `commandbase-core` since it reads `.docs/` artifacts created by all domain skills
- **Naming**: Following gerund convention: `analyzing-research`, `cross-referencing-research`, `synthesizing-research`, or `connecting-research`

## Architecture Notes

### Plugin Placement Analysis

**Option A: `commandbase-research`**
- Pro: Groups with other research skills
- Pro: Research is the primary input domain
- Con: It reads ALL `.docs/` artifacts, not just research — plans, handoffs, learnings too

**Option B: `commandbase-core`**
- Pro: Core dependency — available to all other plugins
- Pro: Reads `.docs/` artifacts from all domains
- Con: Core is already the largest plugin (5 skills + 4 agents)
- Con: It's more of a meta-analysis tool than a core workflow tool

**Option C: `commandbase-meta`**
- Pro: Meta-analysis of existing artifacts is definitionally "meta"
- Pro: Meta plugin already has auditing skills that scan across artifacts
- Con: Meta is for skill/agent tooling, not research synthesis

**Recommendation**: `commandbase-research` — the skill's primary input and output are research documents, even if it can read other `.docs/` types. Cross-domain reading doesn't change the skill's identity.

### Relationship to Existing Skills

The new skill would be DOWNSTREAM of all research skills:
```
/researching-code ──────┐
/researching-web ───────┤
/researching-frameworks ─┼──► [new skill] ──► .docs/research/cross-reference-*.md
/researching-repo ──────┤
/researching-vault ─────┤
/researching-services ──┘
```

It consumes what they produce. It does NOT replace any existing skill — it adds a synthesis layer on top.

### Precedent: `/auditing-docs` Pattern

The `/auditing-docs` skill already sweeps across `.docs/` directories, checks staleness, and spawns `docs-updater` per document. The cross-referencing skill would follow a similar sweep-and-analyze pattern but with synthesis instead of update.

## Open Questions

1. **Scope**: Should the skill only read `.docs/research/` files, or also `.docs/plans/`, `.docs/learnings/`, `.docs/handoffs/`?
2. **Interactivity**: Should it present intermediate findings and ask the user which threads to pull, or run fully autonomously?
3. **Citation format**: How should cross-reference documents cite their source documents? Relative paths? Wikilinks?
4. **Incremental mode**: Should it support "add this new research to the existing cross-reference" or always create fresh?
5. **Minimum documents**: What's the minimum number of source documents for cross-referencing to be valuable? (Likely 3+)
