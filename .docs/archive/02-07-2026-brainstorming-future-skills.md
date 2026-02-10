---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
archived: 2026-02-09
archive_reason: "Fully implemented in Phase 4 (2026-02-07). Skills deployed as plugins at plugins/commandbase-code/skills/brainstorming-code/, plugins/commandbase-vault/skills/brainstorming-vault/, plugins/commandbase-services/skills/brainstorming-services/. Original newskills/ path no longer exists. Implementation plan also archived."
references:
  - plugins/commandbase-code/skills/brainstorming-code/
  - plugins/commandbase-vault/skills/brainstorming-vault/
  - plugins/commandbase-services/skills/brainstorming-services/
---

# Domain-Specific Brainstorming Skills

> **Status: IMPLEMENTED** -- Deployed in Phase 4 (2026-02-07). All 3 brainstorming skills live at `newskills/` and `~/.claude/skills/`: `/brainstorming-code`, `/brainstorming-vault`, `/brainstorming-services`. `/discussing-features` retired (absorbed into brainstorming + `/designing-code`). See `.docs/plans/02-07-2026-phase-4-brainstorming-skills-implementation.md` for full details.

## Problem

`/discussing-features` is generic. Brainstorming a vault reorganization is fundamentally different from brainstorming an API endpoint — a generic skill can't ask the right questions or go deep enough in any domain.

## Concept

Replace `/discussing-features` with domain-specific brainstorming skills that serve as the **pre-RDSPI entry point** — exploring ideas before committing to a direction.

| Skill | Domain knowledge |
|---|---|
| `/brainstorming-code` | Patterns, APIs, data models, existing codebase conventions |
| `/brainstorming-vault` | Obsidian structure, MOCs, tags, linking strategies |
| `/brainstorming-services` | Docker, networking, reverse proxy, backup, dependencies |

## Why Domain-Specific

- `/brainstorming-code` asks "REST or GraphQL?" and "event-driven or polling?"
- `/brainstorming-vault` asks "flat tags or nested folders?" and "one MOC or topic hubs?"
- `/brainstorming-services` asks "Authelia or Cloudflare tunnels?" and "single compose or per-service?"
- A generic skill can only ask "what do you want to build?" — it doesn't know the decision space

## Where It Fits

Brainstorming is always the first step, before any initializer or RDSPI phase:

```
/brainstorming-*   <- explore ideas, settle on direction
/starting-*        <- set up workspace
  R -> D -> S -> P -> I
```

## Open Questions (All Resolved)

- ~~Does `/discussing-features` survive as a cross-domain brainstorming fallback, or is it fully replaced?~~ **Resolved: fully replaced and retired. Domain detection absorbed into `/brainstorming-code`, technical choices into `/designing-code`.**
- ~~Should brainstorming skills produce an artifact (`.docs/` file) or just be conversational?~~ **Resolved: yes, all produce `.docs/brainstorm/` artifacts via docs-writer agent. Artifacts are programmatically consumed by `/designing-code` (not human-mediated).**
- ~~How much should brainstorming skills know about the current codebase/vault/infra state vs being purely exploratory?~~ **Resolved: each skill has domain-specific awareness. Code reads codebase conventions, vault reads vault structure, services reads compose/infrastructure state.**
