---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter; corrected agent path from ~/.claude/agents/ to plugins/commandbase-core/agents/; updated invocation pattern to Task tool spawn; corrected /committing-changes step reference; added /auditing-docs and 4 upstream-reading skills as invokers; added model, key constraints, and archive/update decision criteria"
references:
  - plugins/commandbase-core/agents/docs-updater.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - plugins/commandbase-git-workflow/skills/auditing-docs/SKILL.md
  - plugins/commandbase-git-workflow/skills/auditing-docs/reference/staleness-detection.md
  - plugins/commandbase-code/skills/planning-code/SKILL.md
  - plugins/commandbase-code/skills/designing-code/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
---

# Research: docs-updater Agent

## Overview

The `docs-updater` agent (`plugins/commandbase-core/agents/docs-updater.md`) checks if a document is stale and either updates it with current information or archives it if no longer relevant. It is the single agent responsible for keeping `.docs/` content honest -- updating what is stale, archiving what is obsolete, and always verifying against actual code before changing anything.

**When to Use**: When documents need to be updated after code changes, when checking documentation freshness, or when a skill detects that an upstream document is behind HEAD.

**Model**: opus

## Capabilities

- Read files with Read tool
- Search content with Grep tool
- Find files with Glob tool
- List directories with LS tool
- Edit files with Edit tool
- Run commands with Bash tool

**Tools Available**: Read, Grep, Glob, LS, Edit, Bash

## Invocation Pattern

Spawned via the Task tool by skills that detect stale documents:

```
Task tool call:
  prompt: "Check if this document is stale and either update it with current information or archive it if no longer relevant:\n\nFile: <path>\nWorking directory: <cwd>\n\nThis document has [description of staleness, e.g., 'git_commit X commits behind HEAD']."
```

The agent receives the document path and staleness context, then independently reads the document, checks referenced files, and decides whether to update or archive.

## Process

1. **Read and Analyze**: Load the document fully, extract frontmatter metadata (`git_commit`, `last_updated`, `references`)
2. **Check Staleness**: Use `git rev-list <git_commit>..HEAD --count` to measure how far behind, and `git diff --name-only` to see what changed
3. **Check References**: Verify each file in the `references` list still exists
4. **Decide Action**:
   - **Archive** if: all referenced files deleted, feature/topic removed, superseded by newer doc, or handoff for completed/abandoned work older than 30 days
   - **Update** if: referenced files still exist but changed, topic still relevant, document contains valuable context worth preserving
5. **Execute**: Edit the document content and update frontmatter (if updating), or add archive frontmatter and move to `.docs/archive/` (if archiving)
6. **Report**: Structured output showing what was assessed, decided, and done

## Output Format

```markdown
## Document Assessment: [path]

### Staleness
- **git_commit**: abc1234 (15 commits behind)
- **Last Updated**: 2026-01-15
- **Referenced Files**:
  - src/api/auth.ts - EXISTS (modified in 3 commits)
  - src/middleware/session.ts - EXISTS (unchanged)

### Decision: [UPDATE / ARCHIVE]

### Reason
[Why this decision was made]

### Action Taken
[What was done - moved to archive OR what was updated]

### Result
[Final state - new location if archived, or confirmation of update]
```

## Integration Points

The docs-updater agent is invoked by multiple skills through two distinct patterns:

**Interactive (user-prompted):**
- `/committing-changes` Step 2 -- scans all `.docs/` for files >5 commits behind HEAD, prompts the user, then spawns docs-updater for selected documents
- `/auditing-docs` update mode -- presents a staleness dashboard, then spawns docs-updater one-by-one with user confirmation between each

**Automatic (silent refresh):**
- `/planning-code` -- auto-refreshes stale upstream `.docs/structure/` or `.docs/design/` artifacts (>3 commits behind) before using them as plan input
- `/designing-code` -- auto-refreshes stale research/brainstorm artifacts (>3 commits behind) before reading
- `/resuming-session` -- auto-refreshes stale handoff and learning documents (>3 commits behind) before presenting session context

All skills use the staleness detection scripts from `plugins/commandbase-git-workflow/skills/auditing-docs/reference/staleness-detection.md`.

## Key Constraints

The agent is explicitly conservative:
- Be conservative with archives -- only archive if truly obsolete; when in doubt, update instead
- Be thorough with updates -- do not make superficial updates (frontmatter only); research actual current state before updating
- Preserve history -- add notes about what changed, keep archive organized, document why things were archived
- One document at a time -- focus on the single document given, do it well rather than rushing
- Never delete documents -- always archive instead

## File Reference

- Agent: `plugins/commandbase-core/agents/docs-updater.md`
- Plugin: `commandbase-core`
