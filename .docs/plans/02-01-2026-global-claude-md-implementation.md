---
git_commit: fe26d61
last_updated: 2026-02-01
completed_date: 2026-02-01
topic: Global CLAUDE.md Architecture Implementation
tags: [claude-md, security, configuration, hierarchy]
status: completed
references:
  - .docs/research/02-01-2026-global-claude-md-architecture.md
---

# Global CLAUDE.md Architecture Implementation

## Overview

Implement the global CLAUDE.md architecture to separate universal security rules from project-specific content. This creates a memory hierarchy where global rules (identity, security NEVER rules, scaffolding) apply to all projects automatically, while project CLAUDE.md files focus on project-specific content.

## Success Criteria

- [x] `~/.claude/CLAUDE.md` exists with identity, security rules, and scaffolding
- [x] `starting-projects` guidelines explain hierarchy and what NOT to duplicate
- [x] `updating-claude-md` skill detects global vs project scope
- [x] Global file stays under 60 lines (46 lines)
- [x] No duplication of security rules between global and project files

## What We're NOT Doing

- Not creating a separate `/updating-global-claude` skill (use existing skill with scope detection)
- Not implementing enterprise-level `/etc/claude-code/CLAUDE.md` support
- Not adding dotfiles sync automation (manual documentation only)
- Not modifying `/committing-changes` or `/reviewing-security` (they keep their enforcement)

---

## Phase 1: Create Global CLAUDE.md

**Goal:** Create `~/.claude/CLAUDE.md` with universal rules that apply to all projects.

### Tasks

1. **Create the global file** at `~/.claude/CLAUDE.md`

2. **Content sections:**
   - Identity (GitHub username, SSH preference)
   - Security NEVER rules (consolidated from committing-changes skill)
   - Git safety rules
   - New project scaffolding requirements
   - Automatic behaviors (pattern learning)

### Implementation Details

**File:** `~/.claude/CLAUDE.md`

```markdown
# Global Claude Configuration

Personal standards that apply to ALL projects.

## Identity

GitHub: N0mikon
SSH preferred: `git@github.com:N0mikon/<repo>.git`

## NEVER Rules

These are ABSOLUTE across all projects:

### Secrets & Credentials
- **NEVER** output API keys, tokens, or passwords in responses
- **NEVER** commit `.env` files to git
- **NEVER** include credentials in code suggestions
- Before ANY commit: verify no secrets included

### Git Safety
- **NEVER** use `git add -A` or `git add .`
- **NEVER** force push without explicit request
- **ALWAYS** stage specific files by name

## New Project Scaffolding

When creating ANY new project, ensure:

### Required Files
- `.gitignore` - Must include: .env, node_modules/, dist/
- `CLAUDE.md` - Project overview (use /starting-projects)
- `.env.example` - Template with placeholders (if env vars needed)

### Standard Structure
```
project/
├── src/           # Source code
├── tests/         # Test files
├── .docs/         # Plans, research, handoffs
└── scripts/       # Build/deploy scripts
```

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"),
offer to save the solution as a learned pattern.
```

### Success Criteria

- [x] File exists at `~/.claude/CLAUDE.md`
- [x] Contains Identity section with GitHub username
- [x] Contains NEVER rules for secrets and git safety
- [x] Contains scaffolding requirements
- [x] Contains automatic behaviors section
- [x] Under 60 lines total (46 lines)

---

## Phase 2: Update Project Guidelines

**Goal:** Modify starting-projects guidelines to explain hierarchy and remove global content.

### Tasks

1. **Update `claude-md-guidelines.md`** to add Hierarchy Awareness section
2. **Update "What NOT to Include"** to mention global rules
3. **Update `claude-md-template.md`** to remove automatic behaviors (now global)

### Implementation Details

**File:** `newskills/starting-projects/reference/claude-md-guidelines.md`

**Add after line 44 (after "What NOT to Include" list):**

```markdown

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
```

**Update lines 40-44 to add two items:**

```markdown
## What NOT to Include

- Code style rules (use linters)
- Detailed API documentation
- Database schema details
- Every possible command
- Technology tutorials
- Security NEVER rules (defined in ~/.claude/CLAUDE.md)
- Personal identity/accounts (defined in ~/.claude/CLAUDE.md)
```

**File:** `newskills/starting-projects/templates/claude-md-template.md`

**Remove or simplify lines 50-52** (Automatic Behaviors section) since it's now in global:

```markdown
## Automatic Behaviors

See ~/.claude/CLAUDE.md for global behaviors.
Project-specific behaviors can be added here if needed.
```

### Success Criteria

- [x] Guidelines include "Hierarchy Awareness" section
- [x] "What NOT to Include" mentions global rules
- [x] Template references global for automatic behaviors
- [x] No security rules duplicated in project template

---

## Phase 3: Update Skill for Scope Awareness

**Goal:** Add scope detection to `updating-claude-md` skill to apply different validation per scope.

### Tasks

1. **Add Scope Detection section** after The Gate Function (line 38)
2. **Update Initial Response** to report detected scope
3. **Add scope-specific red flags**

### Implementation Details

**File:** `newskills/updating-claude-md/SKILL.md`

**Insert after line 38 (after The Gate Function), before The 5 Principles:**

```markdown
## Scope Detection

Detect whether updating global or project CLAUDE.md based on file path:

**Global** (`~/.claude/CLAUDE.md` or `~/.claude/CLAUDE.local.md`):
- Contains: Identity, NEVER rules, Scaffolding, Cross-project behaviors
- Validation focus: Universality across ALL projects
- Red flag: Adding project-specific content (commands, structure)

**Project** (`./CLAUDE.md` or `./CLAUDE.local.md`):
- Contains: Project identity, Structure, Commands, Verification
- Validation focus: THIS project's needs
- Red flag: Duplicating global rules (security, identity)

### Detection Logic

```
IF path contains "~/.claude/" OR path contains home directory + "/.claude/"
  THEN scope = GLOBAL
ELSE
  scope = PROJECT
```

Report scope in initial response before proposing changes.
```

**Update Initial Response section (lines 52-63) to include scope:**

```markdown
## Initial Response

When invoked:

1. **Read CLAUDE.md** in the current project (or specified path)
2. **Detect scope** (global vs project based on path)
3. **Report current state**:
   ```
   Current CLAUDE.md: [line count] lines
   Scope: [GLOBAL | PROJECT]
   Sections: [list of ## headings]
   Status: [under ideal / approaching limit / over limit]
   ```
4. **Ask what change is needed** if not already specified
```

**Add to Red Flags section (after line 226):**

```markdown
- Adding project-specific content to global file (commands, structure)
- Duplicating global rules in project file (security, identity)
- Not detecting scope before proposing changes
```

### Success Criteria

- [x] Scope Detection section added after Gate Function
- [x] Initial Response reports detected scope
- [x] Red flags include scope-specific warnings
- [x] Skill distinguishes `~/.claude/CLAUDE.md` from `./CLAUDE.md`

---

## Verification Commands

After implementation, verify:

```bash
# Check global file exists and line count
wc -l ~/.claude/CLAUDE.md

# Check guidelines updated
grep -n "Hierarchy Awareness" newskills/starting-projects/reference/claude-md-guidelines.md

# Check template updated
grep -n "global behaviors" newskills/starting-projects/templates/claude-md-template.md

# Check skill updated
grep -n "Scope Detection" newskills/updating-claude-md/SKILL.md
```

## Notes

- The global CLAUDE.md creates a "behavioral gatekeeper" - even if Claude can read .env files, it won't output secrets
- Skills like `/committing-changes` still enforce rules at execution time; global rules are defense-in-depth
- The hierarchy is: Enterprise → Global → Project → Project Local (we're implementing Global + Project awareness)
