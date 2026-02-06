---
git_commit: 6227f53
last_updated: 2026-02-06
last_updated_by: planning-code
topic: "Add allowed-tools to reviewing-security"
tags: [plan, implementation, skills, allowed-tools, security]
status: draft
references:
  - newskills/reviewing-security/SKILL.md
  - .docs/references/framework-docs-snapshot.md
  - .docs/plans/02-06-2026-framework-feature-adoption.md
---

# Phase 5: Add `allowed-tools` to `reviewing-security`

## Overview

Restrict `reviewing-security` to only the tools it needs, preventing accidental writes during security review. This is the one skill where the tool restriction is a clean fit — no Write, Edit, or Task needed.

## Current State Analysis

### `reviewing-security/SKILL.md` Frontmatter

```yaml
---
name: reviewing-security
description: "Use this skill when reviewing code for security vulnerabilities before committing to public repositories..."
---
```

No `allowed-tools` field currently. The skill has unrestricted tool access.

### Tools Actually Used by the Skill

From reading the skill body:
- `Read` — reads staged files for review
- `Grep` — searches for secret patterns
- `Glob` — finds files matching patterns
- `Bash` — runs `git diff --cached`, `npm audit`, `pip-audit`, `govulncheck`
- `AskUserQuestion` — asks for scope/confirmation when needed

**Tools NOT needed:**
- `Write` — skill produces no files
- `Edit` — skill doesn't modify code
- `Task` — skill doesn't spawn sub-agents

### Why Only This Skill

Research skills (`researching-code`, `researching-web`) were considered but rejected:
- They need Write for `.docs/` output (or Task for docs-writer delegation in Phase 3)
- The restriction would be leaky — body instructions are the real guardrail
- Only `reviewing-security` has a clean tool boundary (100% read-only + Bash for audit commands)

## Desired End State

`reviewing-security` restricted to exactly the tools it uses:

```yaml
---
name: reviewing-security
description: "Use this skill when..."
allowed-tools: [Read, Grep, Glob, LS, Bash, AskUserQuestion]
---
```

## What We're NOT Doing

- Not adding `allowed-tools` to research skills (leaky restriction)
- Not adding `allowed-tools` to any other skills
- Not changing skill body content — frontmatter-only edit

## Implementation Approach

Single frontmatter edit. No body changes.

## Changes Required

### 1. `reviewing-security/SKILL.md`

Add `allowed-tools` to frontmatter:

```yaml
---
name: reviewing-security
description: "Use this skill when reviewing code for security vulnerabilities before committing to public repositories. This includes scanning for hardcoded secrets and API keys, checking for SQL injection and XSS vulnerabilities, validating input sanitization, detecting OWASP Top 10 issues, and reviewing authentication/authorization logic. Trigger phrases: '/review-security', 'security review', 'check for secrets', 'is this safe to commit publicly'."
allowed-tools: [Read, Grep, Glob, LS, Bash, AskUserQuestion]
---
```

### 2. Deploy

```bash
cp newskills/reviewing-security/SKILL.md ~/.claude/skills/reviewing-security/SKILL.md
```

## Pre-Implementation Research

### `/researching-web`: Verify `allowed-tools` Syntax

- Search: "Claude Code SKILL.md allowed-tools syntax 2026"
- Search: "Claude Code skill allowed-tools array format"
- Verify: Is the syntax `allowed-tools: [Read, Grep]` (YAML array) or `allowed-tools: Read, Grep` (comma-separated string)?
- Verify: Is `AskUserQuestion` a valid tool name for `allowed-tools`?
- Verify: Does `allowed-tools` interact with `LS` tool? (LS is used implicitly by some tools)
- Verify: Any known issues with `allowed-tools` blocking Bash subcommands?

### `/researching-code`: Verify Tool Usage

- Re-read `reviewing-security/SKILL.md` to confirm no hidden Write/Edit/Task usage
- Verify the skill doesn't need Task tool for any sub-agent delegation

## Success Criteria

- [ ] `reviewing-security/SKILL.md` has valid `allowed-tools` frontmatter
- [ ] `/reviewing-security` can still run: `git diff`, `npm audit`, `pip-audit`, `govulncheck`
- [ ] `/reviewing-security` can still use: Read, Grep, Glob, LS
- [ ] `/reviewing-security` cannot use: Write, Edit, Task
- [ ] Test: invoke `/reviewing-security` on a repo — full review completes without tool errors
- [ ] Deployed to `~/.claude/skills/reviewing-security/SKILL.md`

## Dependencies

- **Blocked by:** Nothing (independent of all other phases)
- **Blocks:** Nothing
