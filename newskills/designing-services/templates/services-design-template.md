# Services Design Template

Template for infrastructure design documents written to `.docs/design/`.

## File Naming

Format: `MM-DD-YYYY-description.md` in `.docs/design/`

Examples:
- `02-08-2026-media-stack-architecture.md`
- `02-08-2026-homelab-networking-redesign.md`
- `02-08-2026-backup-strategy-design.md`

## Frontmatter

Handled by docs-writer agent. Provide these fields:
```yaml
doc_type: "design"
topic: "<infrastructure design topic>"
tags: [services, <relevant aspect tags>]
references: [<research artifacts used, key config files>]
```

## Body Sections

```markdown
# <Design Topic>

**Date**: YYYY-MM-DD
**Research Base**: <link to research artifact(s)>

## Design Context

Research artifacts reviewed:
- .docs/research/MM-DD-YYYY-description.md — [key findings summary]
- .docs/brainstorm/topic.md — [directional preferences, if exists]

Key constraints from research:
- [Constraint 1]
- [Constraint 2]

## Decisions

### [Domain 1]: [Decision Topic]

**Decision**: [What was chosen]

**Rationale**: [Why this approach — reference research findings]

**Alternatives considered**:
- [Alternative 1] — rejected because [reason]
- [Alternative 2] — rejected because [reason]

### [Domain 2]: [Decision Topic]

**Decision**: [What was chosen]

**Rationale**: [Why this approach]

**Alternatives considered**:
- [Alternative 1] — rejected because [reason]

[... repeat for each domain ...]

## Claude's Discretion

Decisions delegated by user via "You decide":

### [Delegated Decision Topic]

**Decision**: [What Claude chose]

**Reasoning**: [Why this choice makes sense given research findings and other decisions]

## Secrets Requirements

Services that need secrets configured:
- [Service 1]: [secret type needed, e.g., "database password", "API key"]
- [Service 2]: [secret type needed]

**Note**: These describe WHAT secrets are needed, not their values. Actual secret values are managed in .env files during implementation.

## Constraints Discovered

Technical or operational constraints that shaped design decisions:
- [Constraint 1]: [how it affected decisions]
- [Constraint 2]: [how it affected decisions]

## Out of Scope

Decisions explicitly deferred:
- [Deferred item 1] — [why deferred]
- [Deferred item 2] — [why deferred]

## Next Steps

- /structuring-services — to map compose file layout and config placement
- /planning-services — if structure is straightforward
```

## What Does NOT Belong in Design

- Compose YAML syntax or service definitions
- Docker image names or version tags
- Middleware configuration (Traefik labels, Nginx blocks)
- Volume mount paths or directory structures
- Backup scripts or cron schedules
- DNS record values or zone file entries
- Secret values or .env file contents
- Specific port numbers (use "web port" not "8080")

## Section Guidelines

- **Design Context**: Always link to research artifacts that informed decisions
- **Decisions**: One subsection per domain. Include rationale and alternatives for every decision
- **Claude's Discretion**: Only present if user delegated decisions. Document reasoning thoroughly
- **Secrets Requirements**: Describe what's needed by type, never include values
- **Constraints**: Technical limitations that narrowed the decision space
- **Out of Scope**: Items that were considered but explicitly deferred
