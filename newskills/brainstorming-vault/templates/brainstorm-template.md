# Brainstorm Output Template (Vault)

Use this template when creating vault brainstorm artifacts via `docs-writer` with `doc_type: "brainstorm"`.

## File Naming

- **Location**: `.docs/brainstorm/`
- **Format**: `{topic-name}.md` (lowercase, hyphens) — handled by docs-writer
- **Examples**: `personal-knowledge-vault.md`, `research-notes-vault.md`, `project-docs-vault.md`

## Template

```markdown
# [Vault Purpose] — Brainstorm

## Direction

[High-level vault philosophy settled during brainstorming — 2-3 sentences summarizing the organizational approach, linking philosophy, and overall vault vision]

## Decisions

### [Topic 1 Name]
- **Choice**: [Specific philosophy or direction chosen]
- **Rationale**: [Why this direction, in user's words]

### [Topic 2 Name]
- **Choice**: [Specific philosophy or direction chosen]
- **Rationale**: [Why this direction]

[Continue for each discussed topic]

### Claude's Discretion
[Areas where user said "you decide" — listed so downstream phases know where there is flexibility]
[Or: "User provided specific preferences for all topics."]

## Deferred Ideas
- [Idea that came up but belongs in a separate brainstorm or implementation task]
[Or: "None."]

## Suggested Next Steps
- When Vault BRDSPI is available: `/starting-vault` to initialize workspace, then research → design → structure → plan → implement
- For now: Use these decisions to guide vault setup manually. Reference this brainstorm when making vault structure decisions.
```

## Frontmatter

Handled by `docs-writer`. Provide these fields in the Task prompt:

```yaml
doc_type: "brainstorm"
topic: "<vault purpose/name>"
tags: [vault]
```

## Quality Checklist

Before finalizing the brainstorm artifact:
- [ ] Each discussed topic has at least one concrete philosophy choice
- [ ] Decisions are philosophical, not configuration-specific (no plugin settings, no YAML syntax)
- [ ] Scope matches original vault purpose
- [ ] Deferred ideas captured or explicitly noted as none
- [ ] Direction section summarizes overall vault philosophy in 2-3 sentences
- [ ] Next steps acknowledge Vault BRDSPI availability status
- [ ] Claude's Discretion section lists delegated areas or notes full user specification
