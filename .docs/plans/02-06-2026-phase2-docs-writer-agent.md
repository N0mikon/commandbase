---
git_commit: 6227f53
last_updated: 2026-02-06
last_updated_by: planning-code
topic: "Create docs-writer Agent"
tags: [plan, implementation, agent, docs-writer]
status: implemented
references:
  - newagents/docs-writer.md
  - .docs/plans/02-06-2026-phase1-docs-frontmatter-standard.md
  - .docs/plans/02-06-2026-framework-feature-adoption.md
---

# Phase 2: Create `docs-writer` Agent

## Overview

Create a new `docs-writer` agent that centralizes `.docs/` file creation, enforcing the frontmatter standard from Phase 1. Skills will delegate file creation to this agent instead of writing directly.

## Current State Analysis

- `docs-writer.md` does **not** exist yet (confirmed by research)
- 6 skills currently write `.docs/` files directly with inconsistent frontmatter
- Existing agents: 7 (code-locator, code-librarian, code-analyzer, docs-locator, docs-analyzer, docs-updater, web-researcher)

### Existing Pattern to Follow

The closest existing agent is `docs-updater`:
```yaml
# newagents/docs-updater.md
---
name: docs-updater
description: Checks if a document is stale and either updates it with current information or archives it if no longer relevant. Spawned by /committing-changes when docs are behind HEAD.
tools: Read, Grep, Glob, LS, Edit, Bash
model: opus
---
```

`docs-writer` complements `docs-updater`: writer creates, updater maintains.

## Desired End State

A working `docs-writer` agent at `newagents/docs-writer.md` that:
1. Accepts structured input (doc_type, topic, tags, content, optional references)
2. Generates standardized frontmatter per Phase 1 spec
3. Writes to the correct `.docs/` subdirectory
4. Returns the file path

## What We're NOT Doing

- Agent does NOT generate content — skills provide the body text
- Agent does NOT modify existing files — that's `docs-updater`'s job
- Agent does NOT make decisions about what to document — skills decide

## Implementation Approach

Create the agent file with frontmatter and system prompt following the Contract Format (role, process, deliverables).

## Changes Required

### 1. Create Agent File

**File:** `newagents/docs-writer.md`

**Frontmatter:**
```yaml
---
name: docs-writer
description: Creates and formats .docs/ output files with consistent frontmatter and structure. Use when a skill needs to persist research findings, plans, handoffs, or other documentation to the .docs/ directory.
tools: Write, Read, Bash, Glob
model: haiku
---
```

**Design decisions:**
- `Write` — creates the output file
- `Read` — reads existing files to check for duplicates or append
- `Bash` — runs `git rev-parse --short HEAD` for `git_commit` field
- `Glob` — checks `.docs/` subdirectory exists
- `model: haiku` — this is a formatting/writing task, not analysis

**System prompt responsibilities:**
1. Accept structured input: `doc_type`, `topic`, `tags`, `content` (markdown body), optional `references`
2. Generate standardized frontmatter per Phase 1 spec
3. Get `git_commit` via `git rev-parse --short HEAD`
4. Determine correct subdirectory from `doc_type`:
   - `research` -> `.docs/research/`
   - `plan` -> `.docs/plans/`
   - `handoff` -> `.docs/handoffs/`
   - `reference` -> `.docs/references/`
   - `debug` -> `.docs/debug/`
5. Generate filename: `MM-DD-YYYY-<topic-slug>.md`
6. Create subdirectory if it doesn't exist
7. Write the file
8. Return the file path

### 2. Deploy

```bash
cp newagents/docs-writer.md ~/.claude/agents/docs-writer.md
```

## Pre-Implementation Research

### `/researching-web`: Agent Best Practices

Before creating the agent, verify current patterns:

- Search: "Claude Code agent system prompt best practices 2026"
- Search: "Claude Code haiku model agent performance"
- Verify: Is `haiku` still appropriate for structured writing tasks, or has model performance changed?
- Verify: Any new agent frontmatter fields (like `memory`) that would benefit this agent?

### `/researching-code`: Existing Agent Patterns

- Read all 7 existing agent files to identify the system prompt pattern used
- Ensure `docs-writer` follows the same Contract Format (role, process, deliverables)

## Success Criteria

- [x] `newagents/docs-writer.md` exists with valid frontmatter and system prompt
- [x] Agent can be spawned via Task tool with `subagent_type: docs-writer`
- [x] Agent accepts `doc_type`, `topic`, `tags`, `content` input
- [x] Output files have correct frontmatter matching Phase 1 standard
- [x] Output files are written to correct `.docs/` subdirectory
- [x] Filename follows `MM-DD-YYYY-<topic-slug>.md` pattern
- [x] Deployed to `~/.claude/agents/docs-writer.md`

## Dependencies

- **Blocked by:** Phase 1 (frontmatter standard must be defined)
- **Blocks:** Phase 3 (skills need this agent to exist before delegating to it)
