# Architecture Decision Template

Use this template when writing `.docs/references/architecture-decisions.md`. Each technology choice gets one ADR entry. Present draft ADRs to the user for confirmation before persisting.

## File Template

```markdown
---
date_created: YYYY-MM-DD
status: current
---

# Architecture Decisions

Technology choices for this project, recorded with rationale so future sessions don't re-debate settled decisions.

## ADR-001: [Decision Title]

**Status:** Accepted
**Date:** YYYY-MM-DD
**Context:** [1-2 sentences describing the situation that required a decision]

**Decision:** [What was chosen]

**Alternatives Considered:**
- [Alternative A]: [Why it wasn't chosen - 1 sentence]
- [Alternative B]: [Why it wasn't chosen - 1 sentence]

**Consequences:**
- [Positive consequence]
- [Trade-off or limitation accepted]

**Sources:** [URL that informed this decision]

---

## ADR-002: [Next Decision]
...
```

## Writing Guidelines

### What Makes a Good ADR

**Context:** Describe the problem or need, not the solution. "We need server-side rendering with good SEO" not "We decided to use Next.js."

**Decision:** State the choice clearly. "Use Next.js 15 with App Router" not "We went with Next.js."

**Alternatives:** List 1-3 real alternatives that were considered. Don't list options that were never seriously considered.

**Consequences:** Include at least one positive and one trade-off. Honest trade-offs prevent future "why didn't we use X?" questions.

### When to Create an ADR

Create one for each of these decisions:
- Primary framework choice
- Language/runtime choice (if not obvious from framework)
- Database or ORM selection
- Authentication approach
- Deployment target
- Any decision where the user chose between 2+ viable options

### When NOT to Create an ADR

Skip ADRs for:
- Obvious tooling (linter, formatter - these follow from the framework)
- Version choices within a single library (use compatibility matrix instead)
- Standard conventions that come with the framework

### Numbering

Use sequential numbering: ADR-001, ADR-002, etc. If a decision is superseded later, add a new ADR and mark the old one as "Superseded by ADR-XXX" rather than editing the original.

### User Confirmation

Always present draft ADRs before writing them:

```
Here are the architecture decisions I've drafted based on our research:

ADR-001: Use Next.js 15 with App Router for the primary framework
  - Over: Remix, SvelteKit, Nuxt
  - Because: [reason from research]

ADR-002: Use Tailwind CSS 4 for styling
  - Over: CSS Modules, styled-components
  - Because: [reason from research]

Want me to adjust any of these before recording them?
```

Wait for user confirmation. They may want to change rationale, add alternatives, or skip certain ADRs.
