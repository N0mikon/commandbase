# Brainstorm Output Template

Use this template when creating brainstorm artifacts via `docs-writer` with `doc_type: "brainstorm"`.

## File Naming

- **Location**: `.docs/brainstorm/`
- **Format**: `{topic-name}.md` (lowercase, hyphens) — handled by docs-writer
- **Examples**: `user-auth-feature.md`, `export-api.md`, `backup-cli.md`

## Template

```markdown
# [Topic] — Brainstorm

## Direction

[High-level direction settled during brainstorming — 2-3 sentences summarizing the overall approach chosen and primary interaction mode]

## Decisions

### [Topic 1 Name]
- **Choice**: [Specific direction chosen]
- **Rationale**: [Why this direction, in user's words]

### [Topic 2 Name]
- **Choice**: [Specific direction chosen]
- **Rationale**: [Why this direction]

[Continue for each discussed topic]

### Claude's Discretion
[Areas where user said "you decide" — listed so /designing-code knows where it has freedom to make architectural choices]
[Or: "User provided specific preferences for all topics."]

## Deferred Ideas
- [Idea that came up but belongs in a separate feature]
[Or: "None."]

## Suggested Next Steps
[Based on greenfield vs brownfield detection:]
- Greenfield: "Consider `/starting-projects` to initialize the workspace, then `/researching-code` → `/designing-code` → `/structuring-code` → `/planning-code` → `/implementing-plans`"
- Brownfield: "Consider `/starting-refactors` to scope the change, then `/researching-code` → `/designing-code` → `/structuring-code` → `/planning-code` → `/implementing-plans`"
```

## Frontmatter

Handled by `docs-writer`. Provide these fields in the Task prompt:

```yaml
doc_type: "brainstorm"
topic: "<feature name>"
tags: [<detected sub-domain>, code]
```

The `docs-writer` agent generates the standard frontmatter:
- `date`, `status` (draft), `git_commit`, `tags`, `topic`

## Quality Checklist

Before finalizing the brainstorm artifact:
- [ ] Each discussed topic has at least one concrete direction choice
- [ ] Decisions are directional, not implementation-specific (no code, no file paths, no library names)
- [ ] Scope matches original feature description
- [ ] Deferred ideas captured or explicitly noted as none
- [ ] Direction section summarizes overall approach in 2-3 sentences
- [ ] Next steps suggest appropriate initializer skill (starting-projects vs starting-refactors)
- [ ] Claude's Discretion section lists delegated areas or notes full user specification

## What This Template Does NOT Include

- XML tags (brainstorm artifacts are consumed via section headers, not XML parsing)
- Implementation details (no code, no file paths, no line numbers)
- Research findings (those go in `.docs/research/`)
- Architectural decisions (those go in `.docs/design/`)
