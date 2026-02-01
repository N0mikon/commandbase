# Project Setup Plan Template

Use this template when creating `.docs/plans/project-setup.md` for a new project.

## Template

```markdown
---
git_commit: [current HEAD commit hash, or "initial" if new repo]
last_updated: [YYYY-MM-DD]
last_updated_by: [user name]
topic: "Project Setup"
tags: [plan, setup, project-initialization]
status: draft
references: []
---

# [Project Name] - Project Setup Plan

**Generated**: [Date]
**Project Type**: [Type from discovery]
**Tech Stack**: [Primary technologies]

## Project Overview

[2-3 sentence description from discovery]

## Success Criteria

- [ ] Project structure created
- [ ] Dependencies installed and working
- [ ] Dev server runs successfully
- [ ] Tests pass
- [ ] Linting/formatting configured
- [ ] CLAUDE.md in place

## Phase 1: Environment Setup

### Tasks
- [ ] Initialize project with [package manager]
- [ ] Install core dependencies
- [ ] Configure [linter/formatter]
- [ ] Set up testing framework

### Verification
```bash
[command to verify setup works]
```

## Phase 2: Project Structure

### Directory Layout
```
[Recommended structure from research]
```

### Tasks
- [ ] Create directory structure
- [ ] Set up entry point
- [ ] Configure build process

## Phase 3: Core Configuration

### Configuration Files to Create
- [ ] [List specific config files]

### Tasks
- [ ] [Specific configuration tasks]

## Phase 4: Initial Features (if applicable)

### MVP Goals
- [MVP goals from discovery]

### Features to Implement
1. [Feature from discovery]
2. [Feature from discovery]
3. [Feature from discovery]

## Development Commands

```bash
# Install dependencies
[command]

# Run development server
[command]

# Run tests
[command]

# Build for production
[command]

# Lint/format code
[command]
```

## Notes

[Any special considerations, constraints, or decisions from discovery]
```
