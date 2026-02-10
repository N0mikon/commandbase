---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Staleness review at 64 commits behind - corrected references after plugin restructure; newskills/ removed, skills migrated to plugins/, /handing-over skill retired"
topic: "Automatic Pattern Learning with /learn Skill"
tags: [plan, learn, patterns, CLAUDE.md, reference]
status: historical
archived: 2026-02-01
archive_reason: "Plan fully implemented - /learning-from-sessions skill operational with reference files, automatic behaviors in CLAUDE.md, all success criteria met"
references:
  - .docs/archive/01-28-2026-learn-command-pattern.md
  - C:/Users/Jason/.claude/reference/Writing a good CLAUDE.md
  - plugins/commandbase-core/skills/starting-projects/SKILL.md
  - plugins/commandbase-session/skills/learning-from-sessions/SKILL.md
---

# Automatic Pattern Learning Implementation Plan

> **Historical Note (2026-02-01, updated 2026-02-09)**:
> - The `newreference/` approach in this plan was superseded by skill-local `reference/` subdirectories
> - `/learn` is now implemented as `/learning-from-sessions` (in `plugins/commandbase-session/`)
> - `/new_project` is now `/starting-projects` (in `plugins/commandbase-core/`)
> - `/handover` / `/handing-over` was retired during the plugin restructure
> - The `newskills/` directory was removed; all skills now live under `plugins/<plugin>/skills/`

## Overview

Implement a two-part pattern learning system:
1. **Automatic detection** via CLAUDE.md instruction - notices when user mentions repeat problems
2. **Manual invocation** via `/learn` skill - explicit pattern extraction

Also establish a `reference/` folder pattern for progressive disclosure in CLAUDE.md files.

## Desired End State

1. When a user says "this happened before" or similar, Claude automatically offers to save the pattern
2. Users can explicitly run `/learn` to extract a pattern mid-session
3. Learned patterns save to `~/.claude/skills/learned/` and auto-load in future sessions
4. A reference folder pattern exists for CLAUDE.md progressive disclosure
5. `/new_project` generates CLAUDE.md files that include the pattern detection behavior

### Verification

- [ ] Say "I've hit this before" after solving a problem → Claude offers to save pattern
- [ ] Run `/learn` → Claude extracts and saves pattern with confirmation
- [ ] New session loads patterns from `~/.claude/skills/learned/`
- [ ] `/new_project` creates CLAUDE.md with pattern detection instruction

## What We're NOT Doing

- Hook-based observation (too heavy for this use case)
- Background analysis with Haiku (overkill)
- Instinct confidence scoring (complexity not justified)
- Automatic saving without user confirmation

## Implementation Approach

Use the article's principles:
- **Progressive disclosure**: Reference docs point to detailed files
- **Less is more**: CLAUDE.md instruction is one small section
- **Universal applicability**: Pattern detection applies to all sessions

---

## Phase 1: Create Reference Folder Structure

### Overview
Establish `newreference/` in commandbase for reference documents, deployable to `~/.claude/reference/`.

### Changes Required:

#### 1. Create reference directory
**Directory**: `newreference/`

Create these reference documents:

**File**: `newreference/pattern-learning.md`
```markdown
# Pattern Learning Guidelines

## What Makes a Good Learned Pattern

A pattern worth saving:
- Solves a problem that WILL recur
- Is not trivial (typos, simple syntax)
- Is not one-time (specific API outage)
- Transfers across projects or contexts

## Pattern Categories

| Category | Example |
|----------|---------|
| **Error Resolution** | bcrypt fails on Windows → use bcryptjs |
| **Debugging Technique** | Check X before Y when debugging Z |
| **Workaround** | Library X has bug, use Y instead |
| **Integration Pattern** | When connecting A to B, always do C first |

## Pattern File Format

Save to `~/.claude/skills/learned/[pattern-name].md`:

```markdown
# [Descriptive Pattern Name]

**Extracted:** [Date]
**Context:** [When this applies]

## Problem
[Specific problem this solves]

## Solution
[The technique/workaround/pattern]

## Example
[Code or steps if applicable]

## When to Use
[Trigger conditions - what signals this pattern applies]
```

## Triggers for Automatic Detection

Claude should offer to save a pattern when user says:
- "this happened before"
- "same issue again"
- "we already solved this"
- "I keep hitting this"
- "every time I..."
- "always have to..."

## Storage Location

Patterns save to `~/.claude/skills/learned/` which Claude Code auto-loads.
```

**File**: `newreference/claude-md-guidelines.md`
```markdown
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
```

### Success Criteria:
- [x] `newreference/` directory exists
- [x] `pattern-learning.md` created
- [x] `claude-md-guidelines.md` created

---

## Phase 2: Create /learn Skill

### Overview
Manual skill for explicit pattern extraction mid-session.

### Changes Required:

#### 1. Create learn skill
**File**: `newskills/learn/SKILL.md`

```markdown
---
description: Extract and save a reusable pattern from the current session
---

# Learn Pattern

You are extracting a reusable pattern from something solved in this session. The goal is to capture knowledge that will prevent re-solving this problem in the future.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO PATTERN WITHOUT USER CONFIRMATION
```

Never save a pattern without explicit user approval. They must confirm:
1. The pattern is worth saving
2. The content is accurate
3. The trigger conditions are correct

## The Gate Function

```
BEFORE saving a pattern:

1. IDENTIFY: What problem was solved?
2. ASSESS: Is this worth saving?
   - Will it recur? (not one-time issue)
   - Is it non-trivial? (not typo/syntax)
   - Is it transferable? (applies beyond this exact situation)
3. DRAFT: Write the pattern in standard format
4. PRESENT: Show to user for review
5. CONFIRM: Get explicit approval
6. ONLY THEN: Save to ~/.claude/skills/learned/

Skip confirmation = violated trust
```

## Process

### Step 1: Identify the Pattern

Review the recent session for:
- Error resolutions (what broke, why, how it was fixed)
- Debugging techniques (non-obvious diagnostic steps)
- Workarounds (library quirks, API limitations)
- Integration patterns (how to connect X to Y)

### Step 2: Assess Worth

**Worth saving:**
- Problem will likely recur
- Solution wasn't obvious
- Applies to other projects/contexts
- Would save significant time if encountered again

**NOT worth saving:**
- Simple typos or syntax errors
- One-time issues (specific API outage)
- Project-specific configuration (use handover instead)
- Trivial fixes found immediately

If not worth saving:
```
I reviewed the session but didn't find a pattern worth extracting.

Patterns worth saving are:
- Non-trivial problems that will recur
- Solutions that weren't obvious
- Knowledge that transfers across projects

Would you like me to look for something specific?
```

### Step 3: Draft the Pattern

Use this format:

```markdown
# [Descriptive Pattern Name]

**Extracted:** [Today's date]
**Context:** [Brief description of when this applies]

## Problem
[What problem this solves - be specific about symptoms]

## Solution
[The technique/workaround/pattern - actionable steps]

## Example
[Code example if applicable, or step-by-step]

## When to Use
[Trigger conditions - what signals this pattern applies]
```

### Step 4: Present for Review

```
I've identified a pattern worth saving:

---
[Show the drafted pattern]
---

**Save to:** `~/.claude/skills/learned/[suggested-filename].md`

This will be auto-loaded in all future Claude Code sessions.

Does this look accurate? Any adjustments needed?
```

### Step 5: Save with Confirmation

After user approves:

1. Create `~/.claude/skills/learned/` directory if needed
2. Write the pattern file
3. Confirm:

```
Pattern saved to:
~/.claude/skills/learned/[filename].md

This will be automatically loaded in future sessions. You can:
- Edit it manually at any time
- Delete it if no longer needed
- View all patterns in ~/.claude/skills/learned/
```

## Naming Convention

Pattern filenames should be:
- Kebab-case
- Descriptive but concise
- Indicate the problem domain

Examples:
- `bcrypt-windows-node20-fix.md`
- `jwt-clock-skew-ci.md`
- `react-useeffect-cleanup-pattern.md`
- `git-rebase-conflict-resolution.md`

## Red Flags - STOP and Reconsider

If you notice any of these, pause:

- About to save without user confirmation
- Pattern is project-specific (should be in handover)
- Pattern is trivial (typo, obvious fix)
- Pattern description is vague or generic
- "When to Use" section is empty or unclear

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User will want this saved" | Ask. Never assume. |
| "It's obviously worth saving" | Assess against criteria first. |
| "I'll save now, they can delete later" | No. Confirm first. |
| "Similar to another pattern" | Each pattern must stand alone. |

## The Bottom Line

**User confirmation is mandatory.**

Identify the pattern. Assess its worth. Draft clearly. Get approval. Then save.

This is non-negotiable. Every pattern. Every time.
```

### Success Criteria:
- [x] `newskills/learn/SKILL.md` exists
- [x] Skill can be invoked with `/learn`
- [x] Pattern is drafted and shown to user before saving
- [x] Pattern saves to `~/.claude/skills/learned/`

---

## Phase 3: Add Pattern Detection to CLAUDE.md Template

### Overview
Add a small, universally-applicable instruction to detect repeat-problem signals.

### Changes Required:

#### 1. Create reference for CLAUDE.md behavior
**File**: `newreference/automatic-behaviors.md`

```markdown
# Automatic Claude Behaviors

Behaviors that should be included in every CLAUDE.md for consistent experience.

## Pattern Learning Detection

When the user indicates a repeat problem, offer to save the pattern:

### Trigger Phrases
- "this happened before"
- "same issue again"
- "we already solved this"
- "I keep hitting this"
- "every time I..."
- "always have to..."
- "not again"
- "this keeps happening"

### Response

When triggered, after solving the problem:

```
I notice this seems like a recurring issue. Would you like me to save this as a learned pattern?

If yes, I'll extract it to `~/.claude/skills/learned/` so it's automatically available in future sessions.
```

If user agrees, follow the /learn skill process.

### Why This Matters

- Users often re-solve the same problems across sessions
- LLMs are stateless - they don't remember previous solutions
- Learned patterns auto-load, providing persistent knowledge
- Saves time and frustration on repeat issues
```

#### 2. Update /new_project CLAUDE.md template

In `newskills/new_project/SKILL.md`, update the CLAUDE.md template section (around line 247-281) to include pattern detection.

**Current template ends with:**
```markdown
## Additional Context

For detailed documentation, see:
- `[path/to/doc]` - [brief description]
```

**Add after "Additional Context":**
```markdown
## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again", etc.), offer to save the solution as a learned pattern to `~/.claude/skills/learned/`.
```

### Success Criteria:
- [x] `newreference/automatic-behaviors.md` created
- [x] `/new_project` CLAUDE.md template includes pattern detection instruction

---

## Phase 4: Update Commandbase CLAUDE.md

### Overview
Update the project's own CLAUDE.md to demonstrate the pattern and reference the new structure.

### Changes Required:

#### 1. Update CLAUDE.md
**File**: `CLAUDE.md`

Add reference folder to directory structure and add automatic behaviors section:

```markdown
# commandbase

Personal Claude Code workflow tools - skills, agents, and hooks for the RPI workflow (research, plan, implement, validate).

## Directory Structure

```
commandbase/
├── newskills/       # Skills in development (→ ~/.claude/skills/)
├── newagents/       # Agents in development (→ ~/.claude/agents/)
├── newhooks/        # Hooks in development (→ ~/.claude/hooks/)
├── newreference/    # Reference docs (→ ~/.claude/reference/)
└── .docs/           # Research, plans, and handoff documents
```

## Development

### Deploy to Global Config
```bash
cp -r newskills/skillname ~/.claude/skills/
cp newagents/agent.md ~/.claude/agents/
cp newreference/doc.md ~/.claude/reference/
```

## Additional Context

- `.docs/handoffs/` - Latest session context
- `.docs/research/` - Pattern analysis from other repos
- `~/.claude/reference/` - Guidelines for CLAUDE.md and patterns

## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"), offer to save the solution as a learned pattern.
```

### Success Criteria:
- [x] CLAUDE.md updated with new directory structure
- [x] Automatic behaviors section added
- [x] References to newreference/ included

---

## Phase 5: Deploy and Test

### Overview
Deploy the new components and verify the system works.

### Tasks:

1. **Create directories**
```bash
mkdir -p ~/.claude/skills/learned
mkdir -p newreference
```

2. **Deploy reference docs**
```bash
cp newreference/*.md ~/.claude/reference/
```

3. **Deploy learn skill**
```bash
cp -r newskills/learn ~/.claude/skills/
```

4. **Test automatic detection**
- Start new session
- Solve a problem
- Say "I've hit this before"
- Verify Claude offers to save pattern

5. **Test manual /learn**
- Solve a non-trivial problem
- Run `/learn`
- Verify pattern is drafted and confirmation requested
- Approve and verify file is saved

6. **Test pattern loading**
- Start new session
- Verify learned pattern is available

### Success Criteria:
- [x] `~/.claude/skills/learned/` directory exists
- [x] Reference docs deployed to `~/.claude/reference/`
- [x] `/learn` skill functional
- [x] Automatic detection triggers on repeat-problem phrases
- [x] Saved patterns load in new sessions

---

## Testing Strategy

### Manual Tests:
1. **Automatic detection**: Solve problem, say "this keeps happening", verify offer
2. **Manual learn**: Run `/learn`, verify draft shown, approve, verify saved
3. **Pattern loading**: New session, verify pattern content accessible
4. **Filtering**: Try to save trivial fix, verify Claude declines

### Integration Tests:
1. **With /handover**: Ensure patterns and handovers serve different purposes
2. **With /new_project**: Verify generated CLAUDE.md includes automatic behaviors
3. **Cross-session**: Pattern saved in session A is available in session B

---

## Migration Notes

No migration needed - this is additive:
- New skill (`/learn`)
- New reference docs
- New CLAUDE.md section
- New directory (`~/.claude/skills/learned/`)

Existing workflows unaffected.

---

## References

- Research: `.docs/research/01-28-2026-learn-command-pattern.md`
- Article: `~/.claude/reference/Writing a good CLAUDE.md`
- everything-claude-code: `/c/code/everything-claude-code/commands/learn.md`
