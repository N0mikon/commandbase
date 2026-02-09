# Framework Research Template

Use this template when writing `.docs/references/framework-docs-snapshot.md` and `.docs/references/dependency-compatibility.md`.

## Framework Docs Snapshot Template

Frontmatter is handled by the `docs-writer` agent. Provide these body sections as the `content` field:

```markdown
# Framework Documentation Snapshot

Research date: [YYYY-MM-DD]
Sources: Context7 MCP, web search
Shelf life: Review after [30/60/90] days (based on framework release cadence)

## [Primary Framework] (Tier 1)

### Version
- Current stable: [version]
- Researched version: [version]
- Previous major: [version] (for migration reference)

### Project Structure
```
[Recommended directory layout from official docs]
```

### Key API Patterns
[Core APIs, hooks, components with brief usage notes]
- [Pattern 1]: [Brief description and when to use]
- [Pattern 2]: [Brief description and when to use]

### Configuration
[Essential config files and their purpose]
- [config file]: [What it configures]

### Breaking Changes from Previous Version
[List of breaking changes relevant to project setup]
- [Change 1]: [What changed and how to handle it]
- [Change 2]: [What changed and how to handle it]

### Gotchas
[Non-obvious issues discovered during research]
- [Gotcha 1]: [Description and workaround]

### Sources
- [URL 1] (official docs)
- [URL 2] (migration guide)

---

## [Tier 2 Dependency] (Tier 2)

### Version
- Current stable: [version]
- Compatible with [primary framework] [version range]

### Setup with [Primary Framework]
[How to configure this dependency for the chosen primary framework]

### Key Patterns
[Most important APIs/patterns for this project]

### Sources
- [URL]

---

## [Tier 3 Dependency] (Tier 3)

### Version
- Current stable: [version]

### Integration Notes
[How to integrate with the primary framework]

### Sources
- [URL]
```

## Dependency Compatibility Template

Frontmatter is handled by the `docs-writer` agent. Provide these body sections as the `content` field:

```markdown
# Dependency Compatibility Matrix

## Version Matrix

| Dependency | Version | Compatible With | Notes |
|-----------|---------|-----------------|-------|
| [Framework] | [version] | - | Primary framework |
| [Library A] | [version] | [Framework] [range] | [Any notes] |
| [Library B] | [version] | [Framework] [range], [Library A] [range] | [Any notes] |

## Known Conflicts

[List any known version conflicts or incompatibilities]

- **[Conflict]**: [Library A] [version] is incompatible with [Library B] [version] because [reason]. Resolution: [use version X instead].

If no conflicts: "No known conflicts between these dependency versions."

## Minimum Requirements

- Node.js: [version]+ (or Python [version]+, etc.)
- Package manager: [npm/yarn/pnpm/bun] [version]+
- OS: [any restrictions]

## Setup Verification Commands

Run these after initial setup to verify the stack works:

```bash
# Install dependencies
[install command]

# Verify framework runs
[dev server command]

# Verify tests run
[test command]

# Verify build succeeds
[build command]

# Verify linting passes
[lint command]
```

## Sources

- [URL 1] - [What it verified]
- [URL 2] - [What it verified]
```

## Guidelines

### What to Include
- Version numbers - always specific, never "latest"
- Source URLs - every claim needs a source
- Dates - when was this researched?
- Shelf life - how quickly does this go stale?

### What to Exclude
- Full API documentation (link to it instead)
- Tutorial content (just reference patterns)
- Opinions without sources
- Anything not verified against current docs

### Keeping It Current
Add a "shelf life" note at the top. Fast-moving frameworks (Next.js, React) should be re-researched every 30-60 days. Stable frameworks (Express, Django) can go 90+ days.
