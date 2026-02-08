---
status: archived
archived: 2026-02-07
archive_reason: "Concept fully implemented as /naming-session skill. The skill is deployed at ~/.claude/skills/naming-session/ with source at newskills/naming-session/SKILL.md. All open questions resolved during Phase 1 Foundations implementation (commits ae98216, 3d737ac)."
references:
  - newskills/naming-session/SKILL.md
---

# Session Naming (`/naming-session`)

## Problem

Sessions accumulate without clear identity. When resuming work or reviewing history, there's no easy way to find "that session where I debugged the hook issue" vs "the one where I scaffolded the new project."

## Concept

A skill invoked at the start of a session that:

- Asks the user what they plan to work on (or infers from context)
- Assigns a short, descriptive name to the session (e.g., "hook-enforcement-debug", "skill-audit-v2")
- Writes the name and purpose to a lightweight session log (`.docs/sessions/` or similar)
- Could be referenced by `/handing-over` to auto-title handoff documents

## Why It Matters

- Makes handoff documents easier to find later
- Gives sessions a human-readable identity beyond timestamps
- Pairs naturally with `/taking-over` — pick up by name, not by date
- Could feed into a session history index over time

## Connection to RDSPI

Critical for phase-by-phase work. Each phase gets its own named session:

```
/naming-session "mvp-phase-1-auth"
  R -> D -> S -> P -> I
/handing-over              <- handoff carries the session name
...next session...
/naming-session "mvp-phase-2-core-crud"
/taking-over               <- finds previous handover by name
```

## Open Questions

- Where to store session metadata? `.docs/sessions/` directory vs a single index file?
- Should it auto-suggest a name based on the first few messages, or always ask?
- Integration with `/handing-over` — should handoff filenames include the session name?
