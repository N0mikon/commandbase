# commandbase-session

Worktree isolation, context handoff, and pattern extraction — three independent concerns with zero coupling. Requires commandbase-core for docs agents.

## Three Independent Concerns

```
Worktree Management (git plumbing)
  /starting-worktree  -- create isolated branch + directory, or migrate to bare-repo layout
  /ending-worktree    -- squash merge to main or discard

Context Handoff (knowledge transfer)
  /handing-over       -- create standalone handoff document with key learnings
  /taking-over        -- absorb handoff document and restore context

Pattern Extraction (learning)
  /extracting-patterns -- extract reusable knowledge from conversations
```

Each concern operates independently. Worktrees don't require handoffs. Handoffs don't require worktrees. Pattern extraction works in any context.

## Dependencies

- commandbase-core (docs agents)

## Skills

| Skill | Concern | Description |
|-------|---------|-------------|
| /starting-worktree | Worktree | Create isolated git branch + worktree, or migrate repo to bare-repo layout |
| /ending-worktree | Worktree | Squash merge to main or discard — git plumbing only |
| /handing-over | Handoff | Create standalone handoff document with key learnings and file references |
| /taking-over | Handoff | Absorb handoff document and restore context for new conversation |
| /extracting-patterns | Patterns | Extract reusable knowledge from conversations and capture to .docs/learnings/ |

## Migration from v3.x

If upgrading from v3.x (session tracking architecture), these files are now orphaned and safe to delete:

- `session-map.json` (container root) — no skill reads or writes it
- `.claude/sessions/*/meta.json` — no skill reads or writes it
- `.claude/sessions/*/errors.log` — no skill reads or writes it
- `.claude/sessions/*/checkpoints.log` — bookmarking-code now uses `.claude/checkpoints.log` (no session scoping)

## Installation

```shell
/plugin install commandbase-session
```
