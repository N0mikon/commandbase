---
name: updating-claude-md
description: "Use this skill when updating an existing CLAUDE.md file, adding new sections to project instructions, or modifying project configuration for Claude. This includes adding commands, updating directory structures, adding context pointers to new documentation, recording learned patterns as automatic behaviors, and restructuring files that have grown too large. Trigger phrases: 'update CLAUDE.md', 'add to CLAUDE.md', 'modify project instructions', 'change the project config'."
---

# Updating CLAUDE.md

You are updating an existing CLAUDE.md file while enforcing the same guidelines used by `/starting-projects`. Every change must pass validation against the 5 core principles before being applied.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO CHANGE WITHOUT READING THE CURRENT FILE FIRST
```

CLAUDE.md is the foundation of every Claude session in a project. Blind edits corrupt project context. Read, understand, then propose.

**No exceptions:**
- Don't propose changes based on user description alone
- Don't assume the current structure
- Don't skip line counting
- Don't make changes without explicit approval

## The Gate Function

```
BEFORE proposing any edit:

1. READ: Load the current CLAUDE.md completely
2. PARSE: Identify sections, count lines, note structure
3. CLASSIFY: What type of update is this?
4. VALIDATE: Will the change violate any guideline?
5. ONLY THEN: Propose the specific change

Skip any step = risk corrupting project configuration
```

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

## The 5 Principles

Every change must respect these guidelines from `/starting-projects`:

| # | Principle | Rule |
|---|-----------|------|
| 1 | **Less is more** | Under 60 lines ideal, never exceed 300 |
| 2 | **Universally applicable** | Only info relevant to EVERY session |
| 3 | **Progressive disclosure** | Point to docs, don't inline everything |
| 4 | **No code style rules** | Let linters handle formatting |
| 5 | **WHAT, WHY, HOW** | Cover identity, purpose, and commands |

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

## Update Types

### Type 1: Add Section

Adding a new `##` section (e.g., Deployment, Testing).

**Validation:**
- Is this universally applicable? (Not session-specific?)
- Will adding it exceed 60 lines? If so, suggest progressive disclosure.
- Does it fit the WHAT/WHY/HOW framework?

**Process:**
1. Identify where the section belongs in the structure
2. Draft minimal content (2-5 lines max for most sections)
3. Present proposal with line impact
4. Apply after approval

### Type 2: Update Commands

Modifying commands in `### Key Commands` or similar sections.

**Validation:**
- Is the command universally needed? (Not a one-off?)
- Keep to 4-6 commands total in Key Commands

**Process:**
1. Show current command section
2. Show proposed change (add/modify/remove)
3. Apply after approval

### Type 3: Add Context Pointer

Adding a reference to `.docs/` or other documentation.

**Validation:**
- Does the referenced file exist? (Create if not)
- Is this the right section? (Usually `## Additional Context`)

**Process:**
1. Check if `## Additional Context` section exists
2. Add pointer in format: `- [path] - [brief description]`
3. Optionally create the referenced file

### Type 4: Add Automatic Behavior

Recording a learned pattern for future sessions.

**Validation:**
- Is this a repeatable pattern? (Not a one-time fix?)
- Does `## Automatic Behaviors` section exist?

**Process:**
1. Locate or create `## Automatic Behaviors` section
2. Add the new behavior trigger and response
3. Keep format consistent with existing behaviors

**Standard format:**
```markdown
When I mention [trigger phrase pattern], [expected Claude response].
```

### Type 5: Restructure

File has grown too large and needs reorganization.

**Validation:**
- Is file over 60 lines? (Threshold for restructure consideration)
- What content can move to `.docs/`?

**Process:**
1. Identify content that isn't universally applicable
2. Propose moving detailed content to `.docs/[topic].md`
3. Replace with brief pointer
4. Show before/after line counts

### Type 6: Remove Outdated

Deleting content that's no longer relevant.

**Validation:**
- Confirm the content is truly obsolete
- Won't removing it break session context?

**Process:**
1. Show what will be removed
2. Explain why it's outdated
3. Apply after approval

## Proposal Format

Present every change like this:

```
PROPOSED CHANGE
===============

Type: [Update Type]
Section: [## Section Name]
Impact: [current lines] → [new lines] ([+/-] change)

Current:
```
[exact current content if modifying]
```

Proposed:
```
[exact new content]
```

Principles check:
- [✓/✗] Less is more: [assessment]
- [✓/✗] Universally applicable: [assessment]
- [✓/✗] Progressive disclosure: [assessment]
- [✓/✗] No code style rules: [assessment]
- [✓/✗] WHAT, WHY, HOW: [assessment]

Apply this change?
```

## Progressive Disclosure Enforcement

When an addition would exceed the ideal line count:

```
This change would bring CLAUDE.md to [N] lines (over the 60-line ideal).

Options:
1. Create .docs/[topic].md with full details, add brief pointer here
2. Condense to essential information only ([estimated] lines)
3. Add as-is (acceptable if under 300 max)

Which approach?
```

Always recommend option 1 for content over 10 lines.

## Completion Format

After applying changes:

```
CLAUDE.MD UPDATED
=================

Change applied: [brief description]
Lines: [before] → [after]
Section: [## Section Name]

The file now has [N] lines ([status relative to 60-line ideal]).
```

## Red Flags - STOP and Verify

Pause if you notice:

- Adding content without reading the current file first
- Proposing changes that exceed 300 lines total
- Adding code style rules (should be in linter config)
- Including detailed documentation inline (use progressive disclosure)
- Making changes without showing the proposal
- Skipping the principles check
- Adding project-specific content to global file (commands, structure)
- Duplicating global rules in project file (security, identity)
- Not detecting scope before proposing changes

## Error Recovery

**Recoverable:**
- No CLAUDE.md exists → Suggest `/starting-projects` instead
- Section doesn't exist → Offer to create it

**Blocking:**
- File would exceed 300 lines → Must restructure first
- Change violates core principle → Cannot proceed as proposed

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Just a small addition" | Small additions compound. Check line count. |
| "Users need this detail" | If it's detailed, use progressive disclosure. |
| "This is important context" | Important for every session, or just some? |
| "I'll clean it up later" | Later never comes. Enforce now. |

## The Bottom Line

**No change without validation against the 5 principles.**

Read first. Propose with line counts. Get approval. Every update. Every time.
