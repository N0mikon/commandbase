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
- Security NEVER rules (defined in ~/.claude/CLAUDE.md)
- Personal identity/accounts (defined in ~/.claude/CLAUDE.md)

## Hierarchy Awareness

Project CLAUDE.md inherits from global (`~/.claude/CLAUDE.md`).

**Don't duplicate in project:**
- Security NEVER rules (defined globally)
- Git safety rules (defined globally)
- Personal identity/accounts (defined globally)
- Pattern learning behaviors (defined globally)

**Do include in project:**
- Project-specific identity and purpose
- This project's directory structure
- This project's commands
- This project's verification steps
- Pointers to this project's .docs/

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
