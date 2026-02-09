---
date: 2026-02-08
status: complete
topic: "session-skills-current-state"
tags: [research, session-skills, naming-session, resuming-sessions, handing-over, taking-over, learning-from-sessions, bookmarking-code, hooks, infrastructure]
git_commit: 7f0eb8e
references:
  - plugins/commandbase-session/skills/naming-session/SKILL.md
  - plugins/commandbase-session/skills/resuming-sessions/SKILL.md
  - plugins/commandbase-session/skills/handing-over/SKILL.md
  - plugins/commandbase-session/skills/taking-over/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-session/scripts/track-errors.py
  - plugins/commandbase-session/scripts/harvest-errors.py
  - plugins/commandbase-session/scripts/trigger-learning.py
---

# Session Skills: Current State Analysis

**Date**: 2026-02-08
**Branch**: master

## Research Question
How do the current session skills work together, what is their architecture, and what are their interaction patterns?

## Summary
The session system consists of 6 skills, 3 hooks, and 3 Python scripts organized across 2 plugins (commandbase-session and commandbase-core). The system provides session naming, error tracking, checkpoint management, handover/takeover workflows, session resumption, and learning extraction. All components coordinate through a shared file-based state layer at `.claude/sessions/`.

## Architecture Overview

### Plugin Distribution

| Plugin | Components | Role |
|--------|-----------|------|
| commandbase-session | 5 skills, 3 hooks, 3 scripts | Session lifecycle management |
| commandbase-core | 1 skill (bookmarking-code) | Checkpoint creation/verification |

### Skill Inventory

| Skill | Plugin | Trigger Phrases | Purpose |
|-------|--------|----------------|---------|
| `/naming-session` | commandbase-session | `name session`, session name arguments | Creates session identity, folder structure, and pointer files |
| `/resuming-sessions` | commandbase-session | `resume session`, `restore session` | Reconstructs session context from state files after restart |
| `/handing-over` | commandbase-session | `/handover`, `end session` | Creates handoff document with session context for another session |
| `/taking-over` | commandbase-session | `/takeover`, `continue from handover` | Resumes work from a handoff document with state verification |
| `/learning-from-sessions` | commandbase-session | `/learn`, `what did we learn` | Extracts reusable knowledge from session errors/discoveries |
| `/bookmarking-code` | commandbase-core | `/checkpoint create`, `save a checkpoint` | Creates/verifies named git state snapshots |

### Hook Inventory

| Hook | Event | Script | Purpose |
|------|-------|--------|---------|
| track-errors | PostToolUseFailure | `track-errors.py` | Real-time error logging (subagent context only) |
| harvest-errors | Stop | `harvest-errors.py` | End-of-session transcript parsing for all errors |
| trigger-learning | PreCompact | `trigger-learning.py` | Nudges user to run `/learning-from-sessions` when errors exist |

## Shared State Layer

All session-aware components coordinate through files in `.claude/sessions/`:

### File Inventory

| File | Format | Written By | Read By |
|------|--------|-----------|---------|
| `_current` | Plain text (session name, no newline) | `/naming-session` | All skills, all hooks |
| `session-map.json` | JSON `{session_id: {name, created}}` | `/naming-session` | `/resuming-sessions`, all hooks |
| `{name}/meta.json` | JSON `{sessionId, name, created, gitBranch, summary}` | `/naming-session` | `/resuming-sessions`, `/handing-over` |
| `{name}/checkpoints.log` | Pipe-delimited `YYYY-MM-DD-HH:MM \| name \| sha` | `/bookmarking-code` | `/resuming-sessions`, `/handing-over`, `/bookmarking-code verify` |
| `{name}/errors.log` | JSONL `{timestamp, session_id, tool, input, error, source}` | `track-errors.py`, `harvest-errors.py` | `/resuming-sessions`, `/handing-over`, `/learning-from-sessions`, `trigger-learning.py` |

### Session Resolution Pattern

All 3 hooks and most skills share the same session discovery logic:

1. **Primary**: Read `session-map.json`, look up session_id key → get session name
2. **Fallback**: Read `_current` file → get session name directly
3. **No session**: Return empty/skip session-specific behavior

This dual-path approach exists for concurrent terminal safety (session-map.json uses atomic writes) with backward compatibility (_current as simple fallback).

### External State: Claude's sessions-index.json

Only `/naming-session` reads Claude's native session index at `~/.claude/projects/{encoded-path}/sessions-index.json`. This is read-only — no skill writes to it. The encoded path format is: `C:\code\commandbase` → `C--code-commandbase`.

## Detailed Skill Flows

### 1. /naming-session — Session Creation

**Process (6 steps):**

1. **Discover**: Read `~/.claude/projects/{encoded-path}/sessions-index.json`, find most recent entry by `modified` timestamp, extract sessionId/summary/gitBranch
2. **Check existing**: Read `session-map.json` and `_current` for existing session. If found, warn user with replace/keep/cancel options
3. **Suggest name**: Auto-generate kebab-case name from session summary, truncate to 40 chars at word boundary
4. **Confirm**: Present suggestion, wait for user confirmation or custom name (Iron Law: no folder before confirmation)
5. **Validate**: Name must match `^[a-z0-9-]+$`, 3-40 chars, no leading/trailing/consecutive hyphens
6. **Create**: mkdir `.claude/sessions/{name}/`, write `meta.json`, write `_current`, update `session-map.json` (atomic write)

**Key constraint**: User MUST confirm the name before any folder creation. Auto-suggestions are never auto-accepted.

### 2. /bookmarking-code — Checkpoint Management

**Four operations:**

- **create "name"**: Check git status → warn if dirty → get SHA via `git rev-parse --short HEAD` → append `YYYY-MM-DD-HH:MM | name | sha` to checkpoints.log
- **verify "name"**: Find checkpoint in log → run `git diff --stat <sha>..HEAD` and `git log --oneline <sha>..HEAD` → report changes
- **list**: Read checkpoints.log → display table with Name/Timestamp/SHA/Status (commits behind HEAD)
- **clear**: Count entries → confirm if >5 → keep last 5 lines

**Session awareness**: If `_current` exists, uses `.claude/sessions/{name}/checkpoints.log`. Otherwise uses `.claude/checkpoints.log`. Display uses `{session}:{checkpoint}` prefix but storage uses folder isolation.

**Integration point**: `/implementing-plans` mandates `bookmarking-code create "phase-N-done"` after every verified phase. This is enforced, not optional.

### 3. /handing-over — Session Handoff Creation

**Process:**

1. **Analyze session**: Review conversation for tasks, accomplishments, learnings, files, state, next steps
2. **Session check**: If `_current` exists, prefix topic with `{session-name} -` and include Session Context section (checkpoints, error count, meta reference)
3. **Create document**: Spawn `docs-writer` agent with doc_type "handoff", compiled body with 10 sections
4. **Learning check**: If session has errors.log entries, remind user to run `/learning-from-sessions`

**Iron Law**: NO HANDOVER WITHOUT KEY LEARNINGS. The Key Learnings section is mandatory and must contain substantive insights with file:line references, not generic summaries.

**Output**: `.docs/handoffs/MM-DD-YYYY-description.md` with frontmatter (date, status, topic, tags, git_commit, references)

### 4. /taking-over — Handoff Consumption

**Process (6 steps):**

1. **Load**: Read handoff document fully. Run staleness check (>3 commits behind → spawn docs-updater to refresh)
2. **Read linked docs**: Read all referenced plans/research with same staleness check
3. **Absorb**: Internalize 5 key components (tasks, accomplishments, learnings, state, next steps). Pay special attention to Key Learnings
4. **Verify state**: Run `git status`, `git branch --show-current`, `git log -5`. Verify files exist, changes are present, no drift
5. **Present summary**: Show previous work, absorbed learnings, state verification result, recommended next steps. Ask for confirmation
6. **Begin work**: Create TodoWrite task list, start with first next step, apply learnings throughout

**Iron Law**: NO WORK WITHOUT STATE VERIFICATION. Never start before running git commands and confirming with user.

**Does NOT create a session**: This skill reads handoffs but doesn't interact with session files directly. Session context comes from the handoff body.

### 5. /resuming-sessions — Session State Reconstruction

**Process:**

1. **Discover sessions**: Read `session-map.json`, fall back to `_current`. If neither exists, offer `/naming-session` or `/taking-over`
2. **Select**: Single session auto-selected. Multiple sessions: present list, ask user
3. **Load state**: Read `meta.json` (required), `errors.log` (optional, count + 3 most recent), `checkpoints.log` (optional, list all)
4. **Scan related docs**: Check `.docs/handoffs/` and `.docs/learnings/` for session-related documents. Run staleness auto-update (>3 commits behind → spawn docs-updater)
5. **Verify git**: Compare current branch with `meta.json.gitBranch`, warn if mismatch
6. **Present**: Structured summary with name/ID/branch/created/summary, errors section, checkpoints section, related docs, suggested next steps

**Key difference from /taking-over**: Reconstructs context from state files (meta.json, errors.log, checkpoints.log) rather than narrated handoff documents. Read-only — never modifies session files.

### 6. /learning-from-sessions — Knowledge Extraction

**Process (10-step gate function):**

1. **Session check**: Read `_current`, set title format (`Session Learnings: {name}` or `Session Learnings: {date}`)
2. **Detect**: Recognize extractable knowledge via signals (non-obvious debugging, misleading errors, workaround discovery, configuration insights, trial-and-error)
3. **Read errors**: If session active, read `errors.log` for error context
4. **Scan debug**: Check `.docs/debug/` for recent debug files
5. **Dedup**: Search `.docs/learnings/` and skill directories via ripgrep
6. **Analyze**: Run 4 identification questions + worth assessment (must pass 3 of 4 criteria: recurrence, non-triviality, transferability, time savings)
7. **Draft**: Structure via docs-writer with sections: Error Summary, Discoveries, Debug References, Deferred Actions
8. **Validate**: Run quality gates checklist (16 items)
9. **Confirm**: Present draft to user, wait for approval (Iron Law: never save without confirmation)
10. **Write**: docs-writer creates `.docs/learnings/MM-DD-YYYY-session-learnings.md`

**Deferred Actions routing**:
- Create skill → when reusable across projects, multi-step solution
- Add to CLAUDE.md → when project-specific preference/convention
- Update existing skill → when new edge case for known pattern
- Not worth capturing → simple typo, one-time issue, well-documented knowledge

**Error timing note**: Mid-session invocations only see real-time subagent errors (from track-errors hook). For complete error coverage, run at start of next session after harvest-errors has parsed the transcript.

## Hook System

### 1. track-errors.py (PostToolUseFailure)

**Trigger**: Every tool failure in subagent contexts
**Process**: Resolve session name → if no session, exit → build JSON entry (timestamp, session_id, tool, input[200 chars], error[500 chars]) → append to `errors.log`
**Limitation**: Only fires in subagent contexts (Claude Code limitation). Main conversation errors are missed until harvest runs.

### 2. harvest-errors.py (Stop)

**Trigger**: Session end
**Process**: Re-entry guard → resolve session → stream JSONL transcript line-by-line (constant memory) → index tool_use blocks → match tool_result blocks → detect errors (is_error flag OR non-zero Bash exit) → deduplicate against existing errors.log → backfill empty error fields → write new entries
**Skips**: "Sibling tool call errored", "user doesn't want to proceed", "progress" entries, "file-history-snapshot"
**Always exits 0**: Never triggers conversation restart

### 3. trigger-learning.py (PreCompact)

**Trigger**: Before conversation compaction
**Process**: Resolve session → if no session, exit → read errors.log → count entries → if >0, print reminder to stderr → exit 2 (sends message to Claude as feedback)
**Nudge message**: "SESSION LEARNING REMINDER: This session ({name}) has {count} error(s) logged..."

### Common Patterns Across Hooks

All 3 scripts share:
- **Session resolution**: session-map.json → _current → empty string
- **MINGW path normalization**: `/c/...` → `C:\...` via `cygpath -w` on win32
- **Fast exit on no session**: If no session name resolved, exit immediately (no tracking/nudging)

## Data Flow Diagram

```
/naming-session
    │
    ├─> Creates: _current, session-map.json, {name}/meta.json
    │
    ▼
Work Session
    │
    ├─> Tool Failure → PostToolUseFailure → track-errors.py → errors.log (subagent only)
    ├─> /bookmarking-code create → checkpoints.log (session-scoped when _current exists)
    │
    ▼
/handing-over
    │
    ├─> Reads: _current, checkpoints.log, errors.log
    ├─> Creates: .docs/handoffs/MM-DD-YYYY-description.md (via docs-writer agent)
    ├─> Reminds: run /learning-from-sessions if errors exist
    │
    ▼
Session End
    │
    ├─> Stop → harvest-errors.py → errors.log (full transcript parse, dedup + backfill)
    │
    ▼
[Claude Code restarts]
    │
    ├─> /resuming-sessions
    │       Reads: session-map.json/_current → meta.json → errors.log → checkpoints.log
    │       Scans: .docs/handoffs/, .docs/learnings/ (staleness auto-update)
    │       Verifies: git branch match
    │       Presents: session summary + next steps
    │
    └─> /taking-over .docs/handoffs/MM-DD-YYYY-description.md
            Reads: handoff document (staleness auto-update)
            Reads: linked plans/research (staleness auto-update)
            Verifies: git status, file existence, state drift
            Presents: takeover summary, waits for confirmation
            Begins: work with TodoWrite
    │
    ▼
Conversation grows large
    │
    ├─> PreCompact → trigger-learning.py → nudge if errors exist
    │
    ▼
/learning-from-sessions
    │
    ├─> Reads: _current, errors.log, .docs/debug/
    ├─> Dedup: .docs/learnings/, skill directories
    ├─> Creates: .docs/learnings/MM-DD-YYYY-session-learnings.md (via docs-writer agent)
    └─> Deferred Actions checklist for future implementation
```

## Interaction Patterns Between Skills

### Skill Pairs

| Producer | Consumer | Shared Artifact |
|----------|----------|----------------|
| `/naming-session` | All session-aware skills + hooks | `_current`, `session-map.json`, `meta.json` |
| `/bookmarking-code` | `/resuming-sessions`, `/handing-over` | `checkpoints.log` |
| `track-errors.py` + `harvest-errors.py` | `/resuming-sessions`, `/handing-over`, `/learning-from-sessions`, `trigger-learning.py` | `errors.log` |
| `/handing-over` | `/taking-over` | `.docs/handoffs/MM-DD-YYYY-*.md` |
| `/learning-from-sessions` | Future sessions (manual) | `.docs/learnings/MM-DD-YYYY-*.md` |

### Two Session Resume Paths

There are two distinct paths to resume a session, optimized for different scenarios:

| | /resuming-sessions | /taking-over |
|---|---|---|
| **Input source** | Session state files (meta.json, errors.log, checkpoints.log) | Handoff document (.docs/handoffs/) |
| **Best for** | Same person restarting Claude Code | Different person or different context picking up work |
| **Context type** | Reconstructed from structured data | Narrated by previous session (richer context) |
| **Creates session?** | No (reads existing session) | No (reads handoff, no session interaction) |
| **State verification** | Branch mismatch check only | Full git status/log verification + drift detection |

### Staleness Auto-Update Pattern

Three skills implement the same staleness check before reading documents:

- `/taking-over`: Checks handoff and linked docs
- `/resuming-sessions`: Checks related handoffs and learnings
- `/planning-code`, `/designing-code`: Check referenced plans/research (upstream skills, not session-specific)

Pattern: Read `git_commit` from frontmatter → count commits behind HEAD → if >3 → spawn `docs-updater` agent → re-read updated version (or note if archived)

## Shared Agent Dependencies

| Agent | Used By | Purpose |
|-------|---------|---------|
| `docs-writer` (commandbase-core) | `/handing-over`, `/learning-from-sessions` | Creates .docs/ files with standardized frontmatter |
| `docs-updater` (commandbase-core) | `/taking-over`, `/resuming-sessions` | Refreshes or archives stale .docs/ files |

## Iron Laws Summary

Each session skill enforces a non-negotiable rule:

| Skill | Iron Law |
|-------|----------|
| `/naming-session` | No session name without user confirmation |
| `/bookmarking-code` | No checkpoint without git state verification |
| `/handing-over` | No handover without Key Learnings section |
| `/taking-over` | No work without state verification |
| `/resuming-sessions` | No session resume without reading state files |
| `/learning-from-sessions` | No learnings document without verified discoveries and user approval |

## Open Questions

- The two resume paths (/resuming-sessions vs /taking-over) have overlapping use cases — when exactly should each be used?
- /taking-over doesn't create a session, so checkpoints and error tracking are inactive unless /naming-session is run separately
- The track-errors hook only fires in subagent contexts, meaning main conversation errors are invisible until session end when harvest-errors runs
- session-map.json uses inconsistent key types (some are UUIDs, some are plain names like "current" or "skill-audit")
- /resuming-sessions and /taking-over both implement staleness auto-update independently rather than sharing a common implementation
