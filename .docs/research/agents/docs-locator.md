---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated agent path from ~/.claude/agents/ to plugin structure, fixed stale /taking-over reference, aligned output format with actual agent"
references:
  - plugins/commandbase-core/agents/docs-locator.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/researching-code/SKILL.md
---

# Research: docs-locator Agent

## Overview

The `docs-locator` agent (`plugins/commandbase-core/agents/docs-locator.md`) finds relevant documents across the `.docs/` directory (plans, research, handoffs). It's the discovery tool for documentation. Part of the `commandbase-core` plugin, which must be installed first since other plugins depend on its agents.

**When to Use**: When you need to discover what documentation exists about a topic before creating new docs or when looking for historical context.

## Capabilities

- Search content with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: Grep, Glob, LS
**Model**: sonnet

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "docs-locator"
prompt: "Find documents related to [topic] in .docs/"
```

## Use Cases

1. **Doc Discovery**: Find what documentation already exists
2. **History Search**: Locate historical context
3. **Duplication Prevention**: Check before creating new docs
4. **Reference Finding**: Find related research or plans

## Output Format

Returns list of relevant documents grouped by type:
```markdown
## Documents about [Topic]

### Implementation Plans
- `.docs/plans/01-27-2026-feature.md` - [Brief description]

### Research Documents
- `.docs/research/01-27-2026-patterns.md` - [Brief description]

### Handoffs
- `.docs/handoffs/01-27-2026-session.md` - [Brief description]

### Archived
- `.docs/archive/01-27-2026-old-approach.md` - [Brief description]

### Frontmatter Summary (if available)
| Document | git_commit | last_updated | status |
|----------|------------|--------------|--------|
| plans/01-27-2026-feature.md | abc1234 | 01-27-2026 | complete |

Total: X relevant documents found
```

## Integration Points

- Used by `/planning-code` to find existing research before writing plans
- Used by `/researching-code` to avoid duplicating existing research
- Referenced in `plugins/commandbase-code/skills/researching-code/reference/research-agents.md` as a documentation agent

## File Reference

- Agent: `plugins/commandbase-core/agents/docs-locator.md`
- Plugin manifest: `plugins/commandbase-core/.claude-plugin/plugin.json`
