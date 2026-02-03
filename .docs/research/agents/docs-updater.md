# Research: docs-updater Agent

## Overview

The `docs-updater` agent (`~/.claude/agents/docs-updater.md`) checks if a document is stale and either updates it with current information or archives it if no longer relevant. Spawned by `/commit` when docs are behind HEAD.

**When to Use**: When documents need to be updated after code changes or when checking documentation freshness.

## Capabilities

- Read files with Read tool
- Search content with Grep tool
- Find files with Glob tool
- List directories with LS tool
- Edit files with Edit tool
- Run commands with Bash tool

**Tools Available**: Read, Grep, Glob, LS, Edit, Bash

## Invocation Pattern

Called from `/committing-changes` when stale docs detected:
```
subagent_type: "docs-updater"
prompt: "Update [document path] - currently [N] commits behind HEAD"
```

## Process

1. **Read Current Document**: Load the stale document
2. **Analyze Staleness**: Determine what's outdated
3. **Check Code State**: Read current implementation
4. **Decide Action**:
   - Update: Modify document to reflect current state
   - Archive: Move to archive if no longer relevant
5. **Make Changes**: Edit or move the document
6. **Update Frontmatter**: Set new git_commit reference

## Output Format

```markdown
## Document Update: [Path]

### Status
[Updated/Archived/No changes needed]

### Changes Made
- [Change 1]
- [Change 2]

### New git_commit
[current HEAD hash]
```

## Integration Points

- Spawned by `/committing-changes` Step 8
- Works with documents that have `git_commit` frontmatter
- Maintains document freshness across the codebase

## File Reference

- Agent: `~/.claude/agents/docs-updater.md`
