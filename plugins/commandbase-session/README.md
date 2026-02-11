# commandbase-session

Session continuity with git branching — start, end, and resume sessions as isolated worktrees. It's got error tracking and learning extraction built in. Requires commandbase-core for docs agents.

## Dependencies

- commandbase-core (docs agents)

## Skills

| Skill | Description |
|-------|-------------|
| /ending-session | End a work session — squash merge to main, remove worktree, optionally create handoff docs |
| /learning-from-sessions | Extract reusable knowledge from work sessions and capture to .docs/learnings/ |
| /resuming-session | Resume a previous session after restarting Claude Code or picking up from a handover |
| /starting-session | Start a new work session with an isolated git branch and worktree |

## Hooks

| Event | Description |
|-------|-------------|
| SessionStart | Detects and resumes active sessions automatically on Claude Code startup |
| PostToolUseFailure | Tracks errors during a session for later analysis |
| Stop | Harvests accumulated errors at session end |
| PreCompact | Triggers learning extraction before context compaction |

## Installation

```shell
/plugin install commandbase-session
```
