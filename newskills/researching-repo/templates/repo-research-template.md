# Repository Research Template

Use this template when writing repository analysis findings to `.docs/research/`. Frontmatter is handled by the `docs-writer` agent — provide the body sections below as the `content` field.

## File Naming

**Format:** `MM-DD-YYYY-<repo-name>-repository-analysis.md`

- MM-DD-YYYY is today's date
- repo-name is the repository name in kebab-case

**Examples:**
- `02-07-2026-claude-code-repository-analysis.md`
- `02-07-2026-express-repository-analysis.md`
- `02-07-2026-next-js-repository-analysis.md`

## Body Sections Template

```markdown
# [Repository Name] Repository Analysis

**Date**: [Current date]
**Branch**: [Branch analyzed, typically main/master]
**Source**: [Git URL]

## Research Question

[What the user wanted to learn about this repository]

## Summary

[2-4 sentences describing what this repo is, what it does, and the key architectural takeaway]

## Repository Overview

- **Purpose**: [What the project does]
- **Language(s)**: [Primary and secondary languages]
- **Framework(s)**: [Key frameworks/libraries]
- **License**: [License type if detected]

## Repository Structure

```
[Annotated directory tree showing key directories and their purposes]
```

## Key Components

### [Component/Module 1]
- **Location**: [directory path]
- **Purpose**: [What it does]
- **Key files**: [Important files within]

### [Component/Module 2]
- **Location**: [directory path]
- **Purpose**: [What it does]
- **Key files**: [Important files within]

## Architecture Patterns

[Design patterns, conventions, and architectural decisions observed]
- [Pattern 1]: [Description with file references]
- [Pattern 2]: [Description with file references]

## Build & Development

- **Build system**: [How the project is built]
- **Test framework**: [How tests are run]
- **Dev workflow**: [How to develop locally]

## CLAUDE.md / AGENTS.md Summary

[If present: context-aware summary. If absent: "Not found in this repository."]

## Patterns Worth Adopting

[Optional section — include only if user requested pattern analysis]
- [Pattern]: [What it is, where it's used, why it's worth adopting]

## Open Questions

[Areas that need further investigation or weren't fully covered]
```

## Section Guidelines

### Summary
- 2-4 sentences answering "what is this and why should I care?"
- Include the repository URL for reference
- Mention the primary language and purpose
- State the key architectural takeaway

### Repository Overview
- Quick-reference metadata block
- Detect language from file extensions and config files (package.json, Cargo.toml, pyproject.toml, go.mod)
- Detect framework from dependencies and project structure
- License from LICENSE file if present

### Repository Structure
- Annotated directory tree from `git ls-tree` output
- Annotate key directories only — don't list every file
- Focus on top-level directories and their purposes
- Use indentation to show hierarchy

### Key Components
- One subsection per major module or component
- Include file paths from the clone directory
- Describe purpose and key files within each component
- Focus on the most important 3-5 components

### Architecture Patterns
- Document what you observe, don't evaluate or critique
- Include file references for each pattern identified
- Cover: module organization, dependency patterns, error handling approach, configuration strategy

### Build & Development
- Extract from README, Makefile, package.json scripts, CI configs
- Include specific commands when found (e.g., `npm run build`, `cargo test`)
- Note any prerequisites or setup steps

### CLAUDE.md / AGENTS.md Summary
- Context-aware interpretation (skills repo vs app repo — see `../reference/analysis-strategies.md`)
- If skills repo: describe the skill development workflow documented
- If app repo: describe the development instructions provided for Claude Code
- If absent: state "Not found in this repository."

### Patterns Worth Adopting
- Only include when user explicitly asked for pattern analysis
- List concrete, actionable patterns with file references
- Each pattern should be something that could be applied to another project
- Do not include this section if the user didn't request it

### Open Questions
- Areas that weren't fully covered during analysis
- Questions that emerged during research
- Suggestions for follow-up investigation or scoped deep-dives
