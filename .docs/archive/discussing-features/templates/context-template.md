# Context Document Template

Use this template when writing context documents to `.docs/context/{feature-name}.md`.

## File Naming

- **Location**: `.docs/context/`
- **Format**: `{feature-name}.md` (lowercase, hyphens)
- **Examples**: `user-profile-page.md`, `export-api.md`, `backup-cli.md`

## Template

```markdown
---
feature: "[Feature Name]"
domain: [visual|api|cli|content|organization]
gathered: [YYYY-MM-DD]
status: ready-for-planning
---

# [Feature Name] - Implementation Context

<domain>
## Feature Scope

[One paragraph describing what this feature delivers - the scope anchor]
</domain>

<decisions>
## Implementation Decisions

### [Topic 1 that was discussed]
- [Specific decision made]
- [Another decision if applicable]

### [Topic 2 that was discussed]
- [Specific decision made]

### Claude's Discretion
[Areas where user explicitly said "you decide"]
[If none: "User provided specific preferences for all discussed topics."]
</decisions>

<specifics>
## Specific Requests

[User references, examples, "I want it like X" moments]
[If none: "No specific references provided - open to standard approaches that fit the decisions above."]
</specifics>

<deferred>
## Deferred Ideas

[Ideas mentioned that belong to other features or future scope]
[If none: "None - discussion stayed within feature scope."]
</deferred>

---
*Context gathered: [YYYY-MM-DD]*
*Next: /planning-code or /researching-code*
```

## Template Usage Notes

### XML Tags Purpose

The XML tags (`<domain>`, `<decisions>`, `<specifics>`, `<deferred>`) enable downstream skills to parse specific sections:

- `/researching-code` reads `<decisions>` to focus research scope
- `/planning-code` reads `<decisions>` to honor user choices
- Both read `<deferred>` to know what's out of scope

### Decisions Section

- **One heading per discussed topic** - categories emerge from discussion
- **Concrete, not vague** - "Card-based layout with 3 columns" not "Modern feel"
- **Claude's Discretion subsection** - Explicitly notes where user delegated

### Deferred Ideas

- Capture ideas that came up but belong elsewhere
- Don't lose them, don't act on them
- Helps user track future features

### Quality Checklist

Before finalizing context document:
- [ ] Decisions are specific enough for downstream agents to act without re-asking
- [ ] Each discussed topic has at least one concrete decision
- [ ] Scope section matches original feature description
- [ ] Deferred ideas are captured (or explicitly noted as none)
- [ ] No technical/architecture decisions (those belong in planning)
