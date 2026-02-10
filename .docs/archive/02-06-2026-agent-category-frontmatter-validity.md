---
date: 2026-02-06
status: archived
archived: 2026-02-09
archive_reason: "Research complete and consumed — finding that category is not valid agent frontmatter was applied (Phase 6 skipped). No code references remain."
topic: "Claude Code Agent category Frontmatter Field Validity"
tags: [research, agents, frontmatter, category, framework-adoption]
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Verified after 30 commits — finding still accurate, no agents use category field, git_commit bumped to HEAD"
---

# Claude Code Agent `category` Frontmatter Field Validity

## Research Question
Is `category` a valid/supported frontmatter field for Claude Code agents (subagents)? Does it have any runtime effect?

## Summary
`category` is **NOT** a supported Claude Code agent frontmatter field. It was never part of the official specification. The field originated from community collections (davepoon/claude-code-subagents-collection) and was incorrectly recorded in our framework-docs-snapshot.md as official. Unknown frontmatter fields are silently ignored — no errors, but no runtime benefit either.

## Detailed Findings

### Official Agent Frontmatter Fields
**Source:** [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)

The official specification lists these fields:
- `name` (required) - Unique identifier
- `description` (required) - When to delegate
- `tools` - Available tools
- `disallowedTools` - Denied tools
- `model` - Model selection (sonnet, opus, haiku, inherit)
- `permissionMode` - Permission handling
- `maxTurns` - Turn limit
- `skills` - Preloaded skills
- `mcpServers` - MCP server access
- `hooks` - Lifecycle hooks
- `memory` - Persistent memory scope

No `category`, `color`, or `tags` fields are listed.

### Source of Confusion
Our `framework-docs-snapshot.md` (line 128) lists `category` and `color` as optional agent frontmatter. This came from Context7 MCP querying the `/davepoon/claude-code-subagents-collection` community library (Tier 3), not the official Claude Code docs. The community collection organizes agents by category directories and some examples include `category` in frontmatter, but Claude Code does not process it.

### Runtime Behavior
- `category` has zero runtime effect
- Not used for agent discovery, `/agents` listing, or delegation
- Unknown fields are silently ignored (no errors)
- The `/agents` command groups by scope (built-in, user, project, plugin), not by category

### Alternative Organization Approaches
1. **Directory structure** - VoltAgent uses numbered category dirs (01-core-development/)
2. **Naming prefixes** - e.g., code-*, docs-*, web-* (already used in commandbase)
3. **Description keywords** - Claude uses descriptions for delegation decisions
4. **Plugin bundling** - Group agents into themed plugins

## Source Conflicts
- **framework-docs-snapshot.md** (Context7/community source): Lists `category` as optional
- **Official Claude Code docs** (code.claude.com): Does NOT list `category`
- Resolution: The community source was incorrectly treated as authoritative. The official docs are definitive.

## Currency Assessment
- Most recent source: February 2026 (official docs)
- Topic velocity: Fast-moving (Claude Code updates frequently)
- Confidence in currency: High — multiple independent searches confirm the same field list

## Decision Options
| Option | Description | Trade-off |
|--------|-------------|-----------|
| A | Add category anyway as self-documentation | Zero risk, zero benefit, adds noise |
| B | Skip Phase 6 entirely | Cleanest; naming convention already categorizes |
| C | Use description keywords instead | Already in place |

## Open Questions
- Should framework-docs-snapshot.md be corrected to remove `category` and `color` from the agent frontmatter section?
- Could a future Claude Code version add organizational metadata? (No evidence of this being planned)
