# Design Document Template

Template for `.docs/design/` documents produced by `/designing-code`. The docs-writer agent handles frontmatter — this template defines body sections.

---

## Body Sections

```markdown
# [Feature/System] Design Document

## Design Context

**Research artifacts referenced:**
- [Link to .docs/research/ file(s) that informed this design]

**Feature context:** [Link to .docs/context/ file if one exists]

**Scope:** [One sentence describing what this design covers]

## Decisions

### [Decision Domain 1: e.g., API Design]

**Decision:** [What was decided — concrete, specific]

**Rationale:** [Why this approach was chosen over alternatives]

**Alternatives considered:**
- [Alternative A] — rejected because [reason]
- [Alternative B] — rejected because [reason]

### [Decision Domain 2: e.g., Error Strategy]

**Decision:** [What was decided]

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

[Design decisions explicitly deferred to later phases or not relevant to this feature]

- [Deferred topic — why deferred]

## Next Steps

- Run `/structuring-code` to map file placement and module organization based on these decisions
- Or run `/planning-code` directly if structure is straightforward
```

## Section Guidelines

- **Design Context**: Always link to research artifacts. Design without research context is untraceable.
- **Decisions**: One subsection per design domain. Include rationale and alternatives for every decision.
- **Claude's Discretion**: Required if any "You decide" responses were given. Omit only if user made every choice.
- **Constraints Discovered**: Technical limitations found during research that narrowed options.
- **Out of Scope**: Prevents scope creep by explicitly listing what was NOT designed.
- **Next Steps**: Always point to the next BRDSPI phase.

## What Does NOT Belong

- Code snippets or pseudocode
- File paths or line numbers
- Implementation details or task breakdowns
- Performance benchmarks or optimization plans
- Test strategies

These belong in Structure (file paths), Plan (tasks), or Implementation (code).
