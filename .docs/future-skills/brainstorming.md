# Domain-Specific Brainstorming Skills

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

## Open Questions

- Does `/discussing-features` survive as a cross-domain brainstorming fallback, or is it fully replaced?
- Should brainstorming skills produce an artifact (`.docs/` file) or just be conversational?
- How much should brainstorming skills know about the current codebase/vault/infra state vs being purely exploratory?
