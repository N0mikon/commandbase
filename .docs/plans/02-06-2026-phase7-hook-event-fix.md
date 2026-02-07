---
git_commit: 6227f53
last_updated: 2026-02-06
last_updated_by: planning-code
topic: "Fix Framework Docs Snapshot Hook Event Count"
tags: [plan, implementation, hooks, documentation, framework-docs-snapshot]
status: implemented
references:
  - .docs/references/framework-docs-snapshot.md
  - newskills/creating-hooks/SKILL.md
  - .docs/plans/02-06-2026-framework-feature-adoption.md
---

# Phase 7: Fix Framework Docs Snapshot — Hook Event Discrepancy

## Overview

Update `framework-docs-snapshot.md` to document all 12 hook events instead of only 7. The current snapshot captured the 7 "core" events from the official docs at the time of research, but the `creating-hooks` skill documents 12 events total including 5 lifecycle/expanding events.

## Current State Analysis

### Current Hook Events Table (lines 52-61)

```markdown
### Hook Events (7 types)
| Event | When | Can Block? |
|-------|------|-----------|
| PreToolUse | Before tool execution | Yes (approve/block) |
| PostToolUse | After tool completes | Yes (block) |
| Notification | System notification | No |
| Stop | Main agent stopping | Yes (block) |
| SubagentStop | Subagent stopping | Yes (block) |
| UserPromptSubmit | User submits prompt | Yes (block) |
| PreCompact | Before context compaction | No |
```

### Missing Events (from `creating-hooks` skill)

| Event | When | Can Block? | Why Missing |
|-------|------|-----------|-------------|
| SessionStart | Session begins | No | Lifecycle event, not in core docs at time of research |
| SessionEnd | Session terminates | No | Lifecycle event |
| PostToolUseFailure | After tool fails | No | Lifecycle event |
| PermissionRequest | Permission dialog | Yes | Lifecycle event |
| SubagentStart | Subagent spawns | No | Lifecycle event |

### Verified from Web Research

The official docs now document additional events:
- `SubagentStart` with matcher support (matches agent type name)
- `SubagentStop` fires for all subagent completions
- Agent-scoped hooks (defined in agent frontmatter) — `Stop` converts to `SubagentStop` at runtime

## Desired End State

The hook events table in `framework-docs-snapshot.md` shows all 12 events, with a "Tier" column distinguishing core from lifecycle events.

### Updated Table

```markdown
### Hook Events (12 types)
| Event | When | Can Block? | Tier |
|-------|------|-----------|------|
| PreToolUse | Before tool execution | Yes (approve/block) | Core |
| PostToolUse | After tool completes | Yes (block) | Core |
| Notification | System notification | No | Core |
| Stop | Main agent stopping | Yes (block) | Core |
| SubagentStop | Subagent stopping | Yes (block) | Core |
| UserPromptSubmit | User submits prompt | Yes (block) | Core |
| PreCompact | Before context compaction | No | Core |
| SessionStart | Session begins | No | Lifecycle |
| SessionEnd | Session terminates | No | Lifecycle |
| PostToolUseFailure | After tool fails | No | Lifecycle |
| PermissionRequest | Permission dialog | Yes | Lifecycle |
| SubagentStart | Subagent spawns | No | Lifecycle |
```

## What We're NOT Doing

- Not updating the `creating-hooks` skill — it already documents all 12 events
- Not adding new hooks — this is a documentation fix only
- Not changing the rest of `framework-docs-snapshot.md`

## Implementation Approach

Single file edit: replace the hook events table in `framework-docs-snapshot.md`.

## Changes Required

### 1. Edit `.docs/references/framework-docs-snapshot.md`

**Lines to change:** 52-61

Replace:
```markdown
### Hook Events (7 types)
| Event | When | Can Block? |
|-------|------|-----------|
| PreToolUse | Before tool execution | Yes (approve/block) |
| PostToolUse | After tool completes | Yes (block) |
| Notification | System notification | No |
| Stop | Main agent stopping | Yes (block) |
| SubagentStop | Subagent stopping | Yes (block) |
| UserPromptSubmit | User submits prompt | Yes (block) |
| PreCompact | Before context compaction | No |
```

With:
```markdown
### Hook Events (12 types)
| Event | When | Can Block? | Tier |
|-------|------|-----------|------|
| PreToolUse | Before tool execution | Yes (approve/block) | Core |
| PostToolUse | After tool completes | Yes (block) | Core |
| Notification | System notification | No | Core |
| Stop | Main agent stopping | Yes (block) | Core |
| SubagentStop | Subagent stopping | Yes (block) | Core |
| UserPromptSubmit | User submits prompt | Yes (block) | Core |
| PreCompact | Before context compaction | No | Core |
| SessionStart | Session begins | No | Lifecycle |
| SessionEnd | Session terminates | No | Lifecycle |
| PostToolUseFailure | After tool fails | No | Lifecycle |
| PermissionRequest | Permission dialog | Yes | Lifecycle |
| SubagentStart | Subagent spawns | No | Lifecycle |
```

## Pre-Implementation Research

### `/researching-web`: Verify Complete Event List

- Search: "Claude Code hook events complete list 2026"
- Search: "Claude Code hooks SessionStart SessionEnd SubagentStart"
- Verify: Are all 12 events still current? Have any been added or removed?
- Verify: Are the "Can Block?" values correct for lifecycle events?
- Verify: Is `PermissionRequest` still listed as blocking?
- Verify: Any new hook events added since the audit (e.g., `PreCompact` was once missing)?

### `/researching-code`: Cross-Reference with Creating-Hooks Skill

- Read `creating-hooks/SKILL.md` to verify the 12-event list matches
- Read `creating-hooks/reference/` for any additional event details

## Success Criteria

- [x] Table shows all 14 events with Tier classification (updated from plan's 12 to 14 — TeammateIdle and TaskCompleted added in v2.1.33)
- [x] Header updated from "7 types" to "14 types"
- [x] All "Can Block?" values verified against current spec (PostToolUse corrected to "No")
- [x] `creating-hooks` skill and `framework-docs-snapshot.md` are consistent (both show 14 events)
- [x] `creating-hooks` skill deployed to `~/.claude/skills/creating-hooks/SKILL.md`

## Dependencies

- **Blocked by:** Nothing (independent of all other phases)
- **Blocks:** Nothing
