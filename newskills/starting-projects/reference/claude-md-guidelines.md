# CLAUDE.md Guidelines

Based on "Writing a good CLAUDE.md" by Kyle (HumanLayer).

## Core Principles

1. **Less is more** - Under 60 lines ideal, never exceed 300
2. **Universally applicable** - Only info relevant to EVERY session
3. **Progressive disclosure** - Point to docs, don't inline everything
4. **No code style rules** - Let linters handle formatting
5. **WHAT, WHY, HOW** - Cover project identity, purpose, and commands

## Structure Template

```markdown
# [Project Name]

[One sentence: what and why]

## Project Structure
[Brief directory layout - key directories only]

## Development

### Quick Start
[Single command to get started]

### Key Commands
[4-6 most important commands]

### Verification
[Single command to verify before committing]

## Additional Context
[Pointers to detailed docs via progressive disclosure]
```

## What NOT to Include

- Code style rules (use linters)
- Detailed API documentation
- Database schema details
- Every possible command
- Technology tutorials

## Progressive Disclosure Pattern

Instead of:
```markdown
## Database Schema
[50 lines of schema details]
```

Do:
```markdown
## Additional Context
- `.docs/database-schema.md` - Schema documentation
```

Claude reads the file only when working on database tasks.
