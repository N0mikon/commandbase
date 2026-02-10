---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Archived - all recommendations implemented. Global CLAUDE.md exists, skills updated with scope detection, guidelines updated with hierarchy awareness."
topic: "Global CLAUDE.md Architecture Research"
tags: [research, claude-md, security, configuration, hierarchy]
status: archived
archived: 2026-02-09
archive_reason: "All 3 recommendations fully implemented: (1) ~/.claude/CLAUDE.md created with proposed structure, (2) starting-projects guidelines updated with hierarchy awareness, (3) updating-claude-md skill has scope detection. Code references use obsolete newskills/ paths (now plugins/). Superseded by archived handoff and plan docs."
references:
  - plugins/commandbase-core/skills/updating-claude-md/SKILL.md
  - plugins/commandbase-core/skills/starting-projects/reference/claude-md-guidelines.md
  - plugins/commandbase-git-workflow/skills/committing-changes/SKILL.md
  - plugins/commandbase-git-workflow/skills/reviewing-security/SKILL.md
---

# Research: Global CLAUDE.md Architecture

**Date**: 02-01-2026
**Topic**: Global vs Project CLAUDE.md separation and security gatekeeper patterns
**Status**: Complete (all recommendations implemented)

## Research Question

How should we structure a global `~/.claude/CLAUDE.md` and what adjustments should we make to project CLAUDE.md guidelines to implement the memory hierarchy and security gatekeeper patterns?

## Key Findings

### 1. Current State

**No global CLAUDE.md exists** at `~/.claude/CLAUDE.md`.

**Current project guidelines** (`newskills/starting-projects/reference/claude-md-guidelines.md:1-61`):
- 5 core principles: Less is more, Universally applicable, Progressive disclosure, No code style rules, WHAT/WHY/HOW
- Under 60 lines ideal, never exceed 300
- No security content currently specified

**Current skills have security but in isolated silos:**
- `/committing-changes` has NEVER commit .env rules (SKILL.md:23, 36, 209, 234)
- `/reviewing-security` has secret detection patterns (SKILL.md:94-112)
- But these are skill-level, not global behavioral guardrails

### 2. Memory Hierarchy (User Input)

| Level | Location | Purpose |
|-------|----------|---------|
| Enterprise | `/etc/claude-code/CLAUDE.md` | Org-wide policies |
| Global User | `~/.claude/CLAUDE.md` | Standards for ALL projects |
| Project | `./CLAUDE.md` | Team-shared project instructions |
| Project Local | `./CLAUDE.local.md` | Personal project overrides |

**Key insight**: Global CLAUDE.md applies to EVERY project. Project CLAUDE.md adds project-specific context.

### 3. What Belongs Where

#### Global (`~/.claude/CLAUDE.md`)

Content that applies to ALL your projects:

| Category | Example Content |
|----------|-----------------|
| **Identity** | GitHub username, Docker Hub user |
| **Security NEVER rules** | Never commit .env, never expose secrets |
| **Account defaults** | SSH vs HTTPS preference |
| **Cross-project behaviors** | Pattern learning triggers |
| **Personal standards** | Commit message style, PR format |

#### Project (`./CLAUDE.md`)

Content specific to THIS project:

| Category | Example Content |
|----------|-----------------|
| **Project identity** | What it is, why it exists |
| **Directory structure** | Key folders for this codebase |
| **Commands** | Build/test/run for this stack |
| **Verification** | Pre-commit check for this project |
| **Context pointers** | .docs/ files for this project |

### 4. Security Gatekeeper Pattern

From user input and committing-changes skill analysis:

**Defense in Depth Layers:**

| Layer | What | How |
|-------|------|-----|
| 1 | Behavioral rules | Global CLAUDE.md "NEVER" rules |
| 2 | Skill enforcement | `/reviewing-security`, `/committing-changes` |
| 3 | Access control | Deny list in settings.json |
| 4 | Git safety | .gitignore |

**Why Global Gatekeeper Matters:**
- Claude reads `.env` files automatically (security risk)
- Global CLAUDE.md creates behavioral guardrails
- Even if Claude has access, it won't output secrets
- Applies to every project without per-project setup

### 5. Existing Enforcement Patterns in Skills

From codebase analysis (`newskills/committing-changes/SKILL.md`, `newskills/reviewing-security/SKILL.md`):

**Iron Law Pattern:**
```markdown
## The Iron Law

```
[ALL CAPS ABSOLUTE RULE]
```

[Why this rule exists]

**No exceptions:**
- [Violation 1]
- [Violation 2]
```

**NEVER Rules Pattern:**
```markdown
- **NEVER** commit sensitive files (.env, credentials, keys)
- **NEVER** use `git add -A` or `git add .`
- **ALWAYS** run `/reviewing-security` before public commits
```

**Rationalization Prevention Pattern:**
```markdown
| Excuse | Reality |
|--------|---------|
| ".env is in .gitignore" | Check anyway. Gitignore can have holes. |
| "It's just this once" | One wrong commit can leak secrets. Never. |
```

### 6. Gap Analysis

**Current gaps in our system:**

| Gap | Impact | Solution |
|-----|--------|----------|
| No global CLAUDE.md | Security rules must be repeated in every skill | Create `~/.claude/CLAUDE.md` with global rules |
| Project guidelines don't reference global | No separation of concerns | Update guidelines to explain hierarchy |
| Skills can't inherit from global | Redundant rule definitions | Skills reference global rules, don't duplicate |
| No scaffolding rules for new projects | Each project starts blank | Add scaffolding section to global |

### 7. Proposed Changes

#### A. Create `~/.claude/CLAUDE.md` (NEW)

Proposed structure:

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

When creating ANY new project:

### Required Files
- `.gitignore` - Must include: .env, node_modules/, dist/
- `CLAUDE.md` - Project overview (see /starting-projects)
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

#### B. Update Project CLAUDE.md Guidelines

Changes to `starting-projects/reference/claude-md-guidelines.md`:

**Add section: Hierarchy Awareness**
```markdown
## Hierarchy Awareness

Project CLAUDE.md inherits from global (`~/.claude/CLAUDE.md`).

**Don't duplicate in project:**
- Security NEVER rules (defined globally)
- Git safety rules (defined globally)
- Personal identity/accounts (defined globally)

**Do include in project:**
- Project-specific identity and purpose
- This project's directory structure
- This project's commands
- This project's verification steps
- Pointers to this project's .docs/
```

**Update "What NOT to Include":**
```markdown
## What NOT to Include

- Code style rules (use linters)
- Detailed API documentation
- Database schema details
- Every possible command
- Technology tutorials
- **Security NEVER rules** (defined in global CLAUDE.md)
- **Personal identity** (defined in global CLAUDE.md)
```

#### C. Update `updating-claude-md` Skill

Add global vs project awareness:

**New section in SKILL.md:**
```markdown
## Scope Detection

When invoked, detect if updating global or project CLAUDE.md:

**Global** (`~/.claude/CLAUDE.md`):
- Contains: Identity, NEVER rules, Scaffolding, Cross-project behaviors
- Different validation: Focus on universality across ALL projects
- Red flag: Adding project-specific content to global

**Project** (`./CLAUDE.md`):
- Contains: Project identity, Structure, Commands, Verification
- Different validation: Focus on THIS project's needs
- Red flag: Duplicating global rules in project file
```

### 8. Dotfiles Sync Pattern

For multi-machine consistency (from user input):

```bash
# Using GNU Stow
cd ~/dotfiles
mkdir -p claude/.claude
cp ~/.claude/CLAUDE.md claude/.claude/
stow claude  # Symlinks ~/.claude to dotfiles/claude/.claude
```

Benefits:
- Version control on settings
- Consistent configuration everywhere
- Easy recovery if something breaks

### 9. Team Workflow Pattern

"Mistakes become documentation" (from user input, citing Anthropic's approach):

```
Claude makes mistake → You fix it → Add rule to CLAUDE.md → Never happens again
```

For global: Personal mistakes across projects
For project: Team mistakes in this codebase

## Recommendations

### Immediate Actions

1. **Create `~/.claude/CLAUDE.md`** with:
   - Identity section (GitHub username)
   - Security NEVER rules (from committing-changes skill)
   - New project scaffolding requirements
   - Pattern learning automatic behavior

2. **Update `starting-projects` guidelines** to:
   - Explain the hierarchy
   - Remove advice to add security rules (they're global)
   - Focus project CLAUDE.md on project-specific content

3. **Update `updating-claude-md` skill** to:
   - Detect global vs project scope
   - Apply different validation rules per scope
   - Warn when adding project content to global (or vice versa)

### Future Considerations

- Create `/updating-global-claude` skill specifically for global file
- Add dotfiles sync guidance to starting-projects
- Consider enterprise-level CLAUDE.md support

## References

- `C:/code/commandbase/newskills/starting-projects/reference/claude-md-guidelines.md:1-61` - Current project guidelines
- `C:/code/commandbase/newskills/committing-changes/SKILL.md:23,36,209,234` - Security NEVER rules
- `C:/code/commandbase/newskills/reviewing-security/SKILL.md:94-112` - Secret detection patterns
- `C:/code/commandbase/newskills/updating-claude-md/SKILL.md:1-252` - Update skill (no global awareness)
- User input - Memory hierarchy documentation and scaffolding patterns
