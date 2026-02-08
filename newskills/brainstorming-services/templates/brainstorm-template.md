# Brainstorm Output Template (Services)

Use this template when creating services brainstorm artifacts via `docs-writer` with `doc_type: "brainstorm"`.

## File Naming

- **Location**: `.docs/brainstorm/`
- **Format**: `{topic-name}.md` (lowercase, hyphens) — handled by docs-writer
- **Examples**: `homelab-media-stack.md`, `monitoring-infrastructure.md`, `backup-strategy.md`

## Template

```markdown
# [Infrastructure Goal] — Brainstorm

## Direction

[High-level infrastructure direction settled during brainstorming — 2-3 sentences summarizing the stack philosophy, key service choices, and deployment approach]

## Decisions

### [Topic 1 Name]
- **Choice**: [Specific stack or direction chosen]
- **Rationale**: [Why this direction, in user's words]

### [Topic 2 Name]
- **Choice**: [Specific stack or direction chosen]
- **Rationale**: [Why this direction]

[Continue for each discussed topic]

### Decision Dependencies
[Which choices constrain which — e.g., "Traefik chosen → labels-based routing → compose files need labels sections"]
[Or: "No significant interdependencies between decisions."]

### Claude's Discretion
[Areas where user said "you decide" — listed so downstream phases know where there is flexibility]
[Or: "User provided specific preferences for all topics."]

## Deferred Ideas
- [Idea that came up but belongs in a separate brainstorm or implementation task]
[Or: "None."]

## Suggested Next Steps
- When Services BRDSPI is available: `/researching-services` to investigate implementation details
- For now: Use these decisions to guide infrastructure setup manually. Reference this brainstorm when writing compose files and configs.
```

## Frontmatter

Handled by `docs-writer`. Provide these fields in the Task prompt:

```yaml
doc_type: "brainstorm"
topic: "<infrastructure goal>"
tags: [services]
```

## Quality Checklist

Before finalizing the brainstorm artifact:
- [ ] Each discussed topic has at least one concrete stack/direction choice
- [ ] Decisions are directional, not configuration-specific (no Docker tags, no YAML syntax)
- [ ] Decision dependencies are documented (which choices constrain which)
- [ ] Scope matches original infrastructure goal
- [ ] Deferred ideas captured or explicitly noted as none
- [ ] Direction section summarizes overall stack philosophy in 2-3 sentences
- [ ] Next steps acknowledge Services BRDSPI availability status
- [ ] Claude's Discretion section lists delegated areas or notes full user specification
