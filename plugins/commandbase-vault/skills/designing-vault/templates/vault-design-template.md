# Vault Design Document Template

Template for `.docs/design/` documents produced by `/designing-vault`. The docs-writer agent handles frontmatter — this template defines body sections.

---

## Body Sections

```markdown
# [Vault Name/Purpose] Design Document

## Design Context

**Research artifacts referenced:**
- [Link to .docs/research/ file(s) that informed this design]

**Brainstorm artifacts referenced:**
- [Link to .docs/brainstorm/ file(s) with vault philosophy decisions]

**Scope:** [One sentence describing what this design covers]

## Decisions

### Frontmatter Schema

**Decision:** [What schema approach was chosen — concrete, specific]

**Rationale:** [Why this approach was chosen over alternatives]

**Alternatives considered:**
- [Alternative A] — rejected because [reason]
- [Alternative B] — rejected because [reason]

### MOC Strategy

**Decision:** [What MOC approach was chosen]

**Rationale:** [Why]

**Alternatives considered:**
- [Alternative] — rejected because [reason]

### Tag Taxonomy

**Decision:** [What tagging approach was chosen]

**Rationale:** [Why]

**Alternatives considered:**
- [Alternative] — rejected because [reason]

### Folder Boundaries

**Decision:** [What folder organization was chosen]

**Rationale:** [Why]

**Alternatives considered:**
- [Alternative] — rejected because [reason]

### Template Design

**Decision:** [What template approach was chosen]

**Rationale:** [Why]

**Alternatives considered:**
- [Alternative] — rejected because [reason]

### [Additional domains as needed]

...

## Claude's Discretion

[For decisions the user delegated with "You decide" — document what was chosen and the reasoning. This section is mandatory if any decisions were delegated.]

- **[Topic]:** Chose [X] because [rationale]

## Constraints Discovered

[Technical constraints from research that shaped or limited design decisions]

- [Constraint 1 — how it affected decisions]
- [Constraint 2 — how it affected decisions]

## Out of Scope

[Design decisions explicitly deferred or not relevant]

- [Deferred topic — why deferred]

## Next Steps

- Run `/structuring-vault` to map folder layout and note placement based on these decisions
- Or run `/planning-vault` directly if structure is straightforward
```

## Section Guidelines

- **Design Context**: Always link to research and brainstorm artifacts. Design without context is untraceable.
- **Decisions**: One subsection per vault design domain. Include rationale and alternatives for every decision.
- **Claude's Discretion**: Required if any "You decide" responses were given. Omit only if user made every choice.
- **Constraints Discovered**: Technical limitations (e.g., Obsidian doesn't support nested YAML) that narrowed options.
- **Out of Scope**: Prevents scope creep by explicitly listing what was NOT designed.
- **Next Steps**: Always point to the next vault BRDSPI phase.

## What Does NOT Belong

- YAML syntax or template code
- Folder paths or note file names
- Implementation commands or scripts
- Plugin configuration details
- Specific Dataview query syntax

These belong in Structure (paths), Plan (tasks), or Implementation (execution).

## Frontmatter

Handled by `docs-writer`. Provide these fields in the Task prompt:

```yaml
doc_type: "design"
topic: "<vault name/purpose>"
tags: [vault, <relevant aspect tags>]
```
