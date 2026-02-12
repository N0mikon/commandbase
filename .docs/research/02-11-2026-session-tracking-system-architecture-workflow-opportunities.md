---
date: 2026-02-11
status: active
topic: "Session Tracking System - Architecture, Workflow, and Refactor Direction"
tags: [research, session, hooks, skills, architecture, workflow, refactor]
git_commit: caab3d0
references:
  - plugins/commandbase-session/skills/starting-session/SKILL.md
  - plugins/commandbase-session/skills/resuming-session/SKILL.md
  - plugins/commandbase-session/skills/ending-session/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
  - plugins/commandbase-session/scripts/session_utils.py
  - plugins/commandbase-session/scripts/detect-session.py
  - plugins/commandbase-session/scripts/track-errors.py
  - plugins/commandbase-session/scripts/harvest-errors.py
  - plugins/commandbase-session/scripts/trigger-learning.py
  - plugins/commandbase-session/hooks/hooks.json
  - plugins/commandbase-core/skills/bookmarking-code/SKILL.md
  - plugins/commandbase-code/skills/implementing-plans/SKILL.md
  - plugins/commandbase-code/skills/starting-refactors/SKILL.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - .docs/research/02-11-2026-old-handing-over-skill-pre-v2.md
  - .docs/research/02-11-2026-old-taking-over-skill-pre-v2.md
---

# Session Tracking System - Architecture, Workflow, and Refactor Direction

**Date**: 2026-02-11
**Branch**: refactor/session-finetuning

## Research Question
Comprehensive analysis of the session tracking system from multiple angles: architecture, data model, lifecycle, hook integration, cross-skill dependencies, and refactor direction based on discussion with the user.

## Summary
The commandbase session system manages isolated development sessions using git bare-repo + worktrees. It comprises 4 skills, 4 hooks, 1 utility module, and integrates with 4 external skills. Analysis revealed a core architectural problem: **three distinct concepts (worktree, session, handoff) were conflated in v2**, creating confusion and friction. The refactor direction separates these into independent layers: worktrees for git isolation, sessions for conversation tracking, and handoffs for knowledge transfer.

## The Core Problem: Concept Conflation

In v2, three distinct concepts were merged into a single lifecycle:

| Concept | What it is | Old world (pre-v2) | v2 world (current) |
|---|---|---|---|
| **Worktree** | Git isolation (branch + directory) | Didn't exist | Baked into `/starting-session` |
| **Session** | Claude conversation tracking (UUIDs, errors, learnings) | `_current` + handoff mentions | Baked into `/starting-session` |
| **Handoff** | Knowledge transfer document | `/handing-over` (standalone) | Absorbed into `/ending-session` Mode B |
| **Takeover** | Context absorption | `/taking-over` (standalone) | Absorbed into `/resuming-session` Mode B |

### What went wrong
- v2 forced everything through the session lifecycle: you can't hand off without ending, you can't take over without resuming
- `/resuming-session` Mode B/C picker mixes worktree state with handoff documents in a confusing way
- Handing off to yourself between conversations on the same worktree feels wrong through `/ending-session`
- Taking over a handoff from a different project doesn't fit `/resuming-session`
- One worktree can have **multiple sessions** over its lifetime, but v2 treats them as 1:1

### The old skills were clean
The pre-v2 `/handing-over` and `/taking-over` skills (deleted in commit `92113aa`, preserved in `.docs/research/02-11-2026-old-handing-over-skill-pre-v2.md` and `02-11-2026-old-taking-over-skill-pre-v2.md`) were standalone knowledge transfer tools. They had optional session awareness (checked `_current`, included session errors/checkpoints if present) but worked fine without sessions.

## Refactor Direction: Separate the Three Layers

### New conceptual model

```
Worktree (long-lived git isolation)
  └─ Session A (tracking unit: UUIDs, errors, learnings)
      ├─ Conversation 1 (UUID-1)
      ├─ Conversation 2 (UUID-2, after /clear or restart)
      └─ /handing-over → handoff doc (stamps session ID + UUIDs)
  └─ Session B (new tracking unit, same worktree)
      ├─ /taking-over → absorbs handoff from Session A (captures new UUID)
      ├─ Conversation 3 (UUID-3)
      └─ ...
```

### New skill breakdown

```
/starting-worktree    — git isolation (branch + directory), run from main
    ↓
/starting-session     — establish session ID + summary for tracking, run from worktree
                        captures current conversation UUID into claudeSessionIds
    ↓
[work happens, hooks track via session ID]
    ↓
/handing-over         — standalone handoff doc, reads session ID for context
                        stamps current UUID(s) into handoff for traceability
/taking-over          — standalone handoff absorption, reads session ID for context
                        ensures new conversation UUID is associated with session
    ↓
/ending-session       — closes session tracking unit (NOT the worktree)
/ending-worktree      — merge/cleanup of worktree (git plumbing only)
```

### Key separations
- **Worktree** is git plumbing — you can have one without tracking
- **Session** is the tracking layer — UUID collection, error tracking, learning capture
- **Handoff** is knowledge transfer — works with or without sessions, looks at session ID when available
- **Ending** is split: session end (close tracking) vs worktree end (merge + cleanup)

### One worktree, many sessions
- `.claude/sessions/` in a worktree accumulates multiple session directories over time
- `session-map.json` maps session IDs to worktrees (many-to-one)
- Only one session active per worktree at a time
- `/starting-session` checks no other session is active in the worktree

## Current Component Inventory

### Skills (plugins/commandbase-session/skills/)
- `/starting-session` — Creates branches, worktrees, AND state files (conflated). Handles first-time migration (Mode A) and normal creation (Mode B). Iron law: no session without user confirmation of name and branch type.
- `/resuming-session` — Read-only context restoration from worktree state OR handoff documents (conflated). Three modes: worktree resume (A), handoff resume (B), session picker (C). Includes staleness detection for related .docs/ files.
- `/ending-session` — Terminates sessions via merge (squash to main), handoff (keep branch, write handoff doc), OR discard (conflated). Handles worktree removal, branch cleanup, and session-map status updates.
- `/learning-from-sessions` — Extracts reusable knowledge to .docs/learnings/. Standard mode reads errors.log + conversation context. Post-session mode reads transcripts via claudeSessionIds array.

### Hooks (plugins/commandbase-session/hooks/hooks.json)
- `SessionStart` → detect-session.py — Matches worktree to session-map entry, appends Claude UUID to meta.json, injects session context into conversation via stdout.
- `PostToolUseFailure` → track-errors.py — Real-time error logging (subagent only). Appends to errors.log as JSONL.
- `Stop` → harvest-errors.py — End-of-session transcript parsing. Backfills errors.log with main-conversation errors missed by real-time tracking. Deduplicates by (tool, input) key.
- `PreCompact` → trigger-learning.py — Nudges /learning-from-sessions via stderr (exit 2) when errors.log has entries.

### Utilities (plugins/commandbase-session/scripts/)
- `session_utils.py` — Stdlib-only shared functions: path normalization, repo layout detection, session-map CRUD, meta.json updates, session resolution, atomic JSON writes, log utilities.

## Current Data Model

### Container-level: session-map.json
```json
{
  "<session-name>": {
    "name": "<session-name>",
    "branch": "<type>/<session-name>",
    "worktree": "/absolute/path",
    "created": "<ISO 8601>",
    "status": "active" | "handed-off" | "ended"
  }
}
```
Written by: /starting-session, /ending-session
Read by: SessionStart hook, /resuming-session, /ending-session, /learning-from-sessions, /bookmarking-code, resolve_session()

### Per-session: meta.json
```json
{
  "sessionId": "<session-name>",
  "claudeSessionIds": ["<uuid>", ...],
  "name": "<session-name>",
  "branch": "<type>/<session-name>",
  "worktree": "/absolute/path",
  "created": "<ISO 8601>",
  "gitBranch": "<type>/<session-name>",
  "summary": "optional — NEVER WRITTEN (dead field, needs fix)"
}
```
Written by: /starting-session (initial), SessionStart hook (appends UUIDs)
Read by: /resuming-session, /learning-from-sessions

**Note on `summary`**: The field exists in the schema and `/resuming-session` reads and displays it (`Summary: {summary}`, `Continue working on: {summary}`), but NO skill or hook ever writes it. It was intended as a one-line session purpose (e.g., "implement auth MVP"). Should be written during `/starting-session` (user provides purpose) and optionally updated during `/handing-over`.

### Per-session: errors.log (JSONL)
```json
{"timestamp": "...", "session_id": "...", "tool": "...", "input": "...", "error": "...", "source": "harvest|backfilled"}
```
Written by: track-errors.py (real-time), harvest-errors.py (batch)
Read by: /resuming-session, /ending-session, /learning-from-sessions, trigger-learning.py

### Per-session: checkpoints.log (pipe-delimited)
```
YYYY-MM-DD-HH:MM | checkpoint-name | git-sha
```
Written by: /bookmarking-code
Read by: /resuming-session, /bookmarking-code verify

## UUID Tracking Analysis

### Implementation: Correct
- `update_meta_json()` at `session_utils.py:149-164` handles dedup via `if claude_session_id not in ids:`
- Atomic writes via temp file + `os.replace()` prevent corruption
- Silent failure handling in `detect-session.py:66-67` prevents hook crashes
- After `/clear`, new UUID generated, SessionStart fires again, appends to array

### Gap: UUID not captured at session boundaries
The SessionStart hook captures UUIDs on conversation start, but skill-level transitions can miss UUID changes:

- **`/starting-session`** creates meta.json with empty `claudeSessionIds: []`. The conversation UUID that created the session isn't captured until the NEXT hook fire. Fix: `/starting-session` should capture the current conversation UUID into the array at creation time.
- **`/handing-over`** should stamp the current UUID(s) into the handoff doc for traceability (which conversation produced this handoff).
- **`/taking-over`** should ensure the new conversation's UUID is associated with the session being taken over (may be a new session in the same worktree).

### Activity timeline
No need for a separate activity log — the transcript files at `~/.claude/projects/{path-encoded}/{uuid}.jsonl` already contain everything. The `claudeSessionIds` array maps directly to those files. Search transcripts by UUID for full session history.

## Cross-Skill Integration Map

### Tight integration (session-aware behavior)
- `/bookmarking-code` — Detects sessions via session-map.json, stores checkpoints in session-scoped directory, prefixes names with session name for display.

### Loose integration (delegates to session-aware skills)
- `/starting-refactors` — Checks `_current` (STALE — needs update to v2 resolution), creates baseline checkpoint via /bookmarking-code.
- `/implementing-plans` — Checks `_current` (STALE — needs update to v2 resolution), creates phase checkpoints via /bookmarking-code.
- `/committing-changes` — Adapts for squash merge context when invoked by /ending-session (skips stale docs check, reads MERGE_MSG).

### No integration
- `/planning-code`, `/designing-code`, `/auditing-docs`, `/creating-prs`, `/debugging-code`, docs-updater agent, docs-locator agent.

## Known Issues to Fix

### 1. Legacy `_current` references (3 skills)
Three skills still reference the deprecated `.claude/sessions/_current` file:
- `plugins/commandbase-core/skills/bookmarking-code/SKILL.md` — session detection fallback
- `plugins/commandbase-code/skills/starting-refactors/SKILL.md:76` — session awareness check
- `plugins/commandbase-code/skills/implementing-plans/SKILL.md:171` — checkpoint session check

The v2 system eliminated `_current` in favor of worktree-based resolution via `session-map.json`. These skills need updating to use the same detection pattern as `/bookmarking-code`'s primary path (bare-worktree layout detection → session-map.json match).

The `_current` fallback in `resolve_session()` at `session_utils.py:191-212` can also be removed once all consumers are updated.

### 2. `summary` field is dead
The `summary` field in meta.json is read by `/resuming-session` but never written by any skill or hook. Needs to be written during `/starting-session` and optionally updated during `/handing-over`.

### 3. `/starting-session` doesn't capture initial UUID
Creates `claudeSessionIds: []` — the conversation UUID that created the session isn't recorded until the next SessionStart hook fire (next conversation). Fix: capture UUID at creation time.

## Key Architecture Patterns (Preserved)

**1. Worktree-based session isolation**
Each session gets its own filesystem directory via git worktrees. Session resolution uses worktree path matching instead of a singleton `_current` file, avoiding race conditions.

**2. Two-phase error tracking**
Real-time (PostToolUseFailure, subagent only) + batch harvest (Stop hook, parses transcript). The batch phase deduplicates and backfills, ensuring complete coverage despite the subagent-only limitation of PostToolUseFailure.

**3. Atomic file operations**
All JSON state files use temp file + os.replace() for crash safety. Session-map.json updates are read-modify-write with fsync.

**4. Context injection via hook exit codes**
SessionStart uses exit 0 + stdout to inject session context. PreCompact uses exit 2 + stderr to send nudges. This is the only mechanism for hooks to communicate with the conversation.

**5. Deferred action pattern**
/learning-from-sessions captures knowledge to .docs/learnings/ with "Deferred Actions" checklists rather than immediately modifying skills or CLAUDE.md. This prevents mid-session disruption.

## Remaining Opportunities (Lower Priority)

These items surfaced during initial research but are lower priority than the core refactor:

**1. `/learning-from-sessions` should leverage UUID transcripts**
Should pull transcripts by UUID from the `claudeSessionIds` array for post-session learning. Also should be invokable mid-session to capture reasoning patterns (not just tool errors). The transcript parsing infrastructure exists in `harvest-errors.py` and can be reused.

**2. No session duration or time tracking**
Sessions have a `created` timestamp but no `ended` timestamp.

**3. checkpoints.log format inconsistency**
Only non-JSON state file. errors.log uses JSONL, meta.json and session-map.json use JSON, but checkpoints.log uses pipe-delimited text.

**4. No cross-session learning aggregation**
Each session's learnings are written to separate .docs/learnings/ files with no roll-up mechanism.

**5. No session-aware `/creating-prs`**
Could auto-populate PR descriptions from session context.

## Code References
- `plugins/commandbase-session/skills/starting-session/SKILL.md` — Session creation skill (to be split)
- `plugins/commandbase-session/skills/resuming-session/SKILL.md` — Session resumption skill (handoff mode to be extracted)
- `plugins/commandbase-session/skills/ending-session/SKILL.md` — Session termination skill (to be split)
- `plugins/commandbase-session/skills/learning-from-sessions/SKILL.md` — Learning extraction skill
- `plugins/commandbase-session/scripts/session_utils.py` — Shared utility functions
- `plugins/commandbase-session/scripts/detect-session.py` — SessionStart hook script
- `plugins/commandbase-session/scripts/track-errors.py` — PostToolUseFailure hook script
- `plugins/commandbase-session/scripts/harvest-errors.py` — Stop hook script
- `plugins/commandbase-session/scripts/trigger-learning.py` — PreCompact hook script
- `plugins/commandbase-session/hooks/hooks.json` — Hook configuration
- `plugins/commandbase-core/skills/bookmarking-code/SKILL.md` — Session-aware checkpointing (has stale `_current` ref)
- `plugins/commandbase-code/skills/implementing-plans/SKILL.md` — Phase checkpoints (has stale `_current` ref)
- `plugins/commandbase-code/skills/starting-refactors/SKILL.md` — Baseline checkpoints (has stale `_current` ref)
- `plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md` — Squash merge adaptation
- `.docs/research/02-11-2026-old-handing-over-skill-pre-v2.md` — Preserved old /handing-over skill
- `.docs/research/02-11-2026-old-taking-over-skill-pre-v2.md` — Preserved old /taking-over skill

## Architecture Notes
The system follows a hub-and-spoke pattern: session_utils.py is the shared hub, hooks are the automated spokes (fire on events), and skills are the user-initiated spokes. State flows downward from session-map.json (registry) to meta.json (identity) to errors.log/checkpoints.log (activity). The only upward flow is the SessionStart hook injecting context and the PreCompact hook nudging /learning-from-sessions. Cross-skill integration is minimal — only /bookmarking-code has tight session awareness; other skills delegate to it or operate independently.

## Open Questions (Resolved)
1. ~~Should the `summary` field in meta.json be actively maintained?~~ **YES** — write during /starting-session, optionally update during /handing-over.
2. ~~Is the legacy `_current` fallback still needed?~~ **NO** — remove from resolve_session() and update 3 consuming skills.
3. ~~Would a session activity log add value?~~ **NO** — search UUID transcripts directly instead.
4. ~~Should /creating-prs be session-aware?~~ **Lower priority** — defer to after core refactor.
5. ~~Could the PreCompact nudge be extended?~~ **Lower priority** — defer.

## Open Questions (New)
1. What should the exact session-map.json schema look like when sessions are many-to-one with worktrees?
2. Should `/ending-worktree` be a separate skill or a mode of `/ending-session`?
3. How does the SessionStart hook detect which session is active when multiple sessions exist in one worktree?
4. Should `/starting-session` auto-detect the current conversation UUID, or should it require the SessionStart hook to have fired first?
