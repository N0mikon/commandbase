# commandbase-session

Session continuity with three-layer architecture: worktree isolation, session tracking, and standalone handoff. Includes error tracking and learning extraction. Requires commandbase-core for docs agents.

## Three-Layer Architecture

```
Worktree Layer (git plumbing)
  /starting-worktree  -- create isolated branch + directory
  /ending-worktree    -- merge to main or discard

Session Layer (tracking)
  /starting-session   -- discovery + state setup (purpose, UUID, meta.json)
  /ending-session     -- close-out + summary.json (no merge, no worktree ops)
  /resuming-session   -- restore context from session state files
  /learning-from-sessions -- extract reusable knowledge from errors

Handoff Layer (knowledge transfer)
  /handing-over       -- create standalone handoff document
  /taking-over        -- absorb handoff document
```

One worktree can have multiple sessions (many-to-one). Only one session active per worktree at a time. Handoffs are independent of both layers.

## Dependencies

- commandbase-core (docs agents)

## Skills

| Skill | Layer | Description |
|-------|-------|-------------|
| /starting-worktree | Worktree | Create isolated git branch + worktree, or migrate repo to bare-repo layout |
| /ending-worktree | Worktree | Squash merge to main or discard -- git plumbing only |
| /starting-session | Session | Discovery-driven session setup -- captures purpose, writes meta.json, registers in session-map |
| /ending-session | Session | Close-out session tracking -- produces .docs/sessions/{name}/summary.json |
| /resuming-session | Session | Restore session context from worktree state files |
| /learning-from-sessions | Session | Extract reusable knowledge from session errors and capture to .docs/learnings/ |
| /handing-over | Handoff | Create standalone handoff document with key learnings and file references |
| /taking-over | Handoff | Absorb handoff document and restore context for new conversation |

## Hooks

| Event | Description |
|-------|-------------|
| SessionStart | Detects active session for current worktree, injects context including purpose |
| PostToolUseFailure | Tracks errors during a session for later analysis |
| Stop | Harvests accumulated errors at session end |
| PreCompact | Triggers learning extraction before context compaction |

## State Files

| File | Location | Committed? | Contents |
|------|----------|------------|----------|
| session-map.json | Container root | No (gitignored) | Registry of all sessions (name, branch, worktree, status, summary) |
| meta.json | `.claude/sessions/{name}/` | No (gitignored) | Session metadata + Claude conversation UUIDs |
| errors.log | `.claude/sessions/{name}/` | No (gitignored) | JSONL error tracking from hooks |
| checkpoints.log | `.claude/sessions/{name}/` | No (gitignored) | Checkpoint history from /bookmarking-code |
| summary.json | `.docs/sessions/{name}/` | Yes (committed) | Session close-out summary with full lifecycle data |

## Installation

```shell
/plugin install commandbase-session
```
