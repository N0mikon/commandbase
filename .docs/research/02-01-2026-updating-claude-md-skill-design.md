# Research: Updating CLAUDE.md Skill Design

**Date**: 02-01-2026
**Topic**: Designing a skill to update existing CLAUDE.md files while following starting-projects guidelines
**Status**: Complete

## Research Question

How should we design an `updating-claude-md` skill that updates existing CLAUDE.md files while staying within the same guidelines used by `/starting-projects`?

## Key Findings

### 1. Starting-Projects CLAUDE.md Guidelines

From `~/.claude/skills/starting-projects/reference/claude-md-guidelines.md`:

**Core Principles**:
1. **Less is more** - Under 60 lines ideal, never exceed 300
2. **Universally applicable** - Only info relevant to EVERY session
3. **Progressive disclosure** - Point to docs, don't inline everything
4. **No code style rules** - Let linters handle formatting
5. **WHAT, WHY, HOW** - Cover project identity, purpose, and commands

**What NOT to Include**:
- Code style rules (use linters)
- Detailed API documentation
- Database schema details
- Every possible command
- Technology tutorials

### 2. Standard CLAUDE.md Structure

From `~/.claude/skills/starting-projects/templates/claude-md-template.md:15-53`:

```markdown
# [Project Name]
[One sentence: what this project is and its purpose]

## Project Structure
[Brief directory layout - only key directories]

## Development
### Quick Start
[Single command to get started]

### Key Commands
[4-6 most important commands]

### Verification
[Single verification command before committing]

## Architecture Notes (optional)
[2-3 sentences on key architectural decisions - only if non-obvious]

## Additional Context
[Pointers to detailed docs]

## Automatic Behaviors
[Pattern learning detection]
```

### 3. Discussing-Features Pattern for Gathering Intent

From `~/.claude/skills/discussing-features/SKILL.md`:

**Key Pattern**: Domain-based adaptive questioning
- Detect what TYPE of update is needed
- Generate relevant questions based on update type
- 4-question rhythm with check-ins
- Capture concrete decisions, not abstract preferences

**Gate Function**: Before any action, identify and confirm the update scope.

### 4. Update Types to Support

Based on how CLAUDE.md files evolve:

| Update Type | Trigger | Example Changes |
|-------------|---------|-----------------|
| **Add section** | New capability/workflow | Add "Deployment" section |
| **Update commands** | Commands changed | Update test command |
| **Add context pointer** | New docs created | Point to new `.docs/` file |
| **Add automatic behavior** | Pattern learned | Add new trigger phrase |
| **Restructure** | File grew too large | Split or reorganize |
| **Remove outdated** | Feature removed | Delete obsolete sections |

### 5. Quality Guardrails from Starting-Projects

From `~/.claude/skills/starting-projects/SKILL.md:126-140`:

**Red Flags - Stop and Reconsider**:
- Writing CLAUDE.md over 60 lines (ideal) or approaching 300 (max)
- Including code style rules
- Adding detailed documentation inline
- Not using progressive disclosure
- Making changes without user confirmation

## Proposed Skill Design

### Skill Name
`updating-claude-md`

### Activation Triggers
- "update CLAUDE.md"
- "add to CLAUDE.md"
- "update project instructions"
- "modify CLAUDE.md"

### Core Flow

```
1. READ current CLAUDE.md
   - Parse existing structure
   - Count lines
   - Identify sections

2. CLASSIFY the update type
   - What kind of change?
   - Which section affected?

3. VALIDATE against guidelines
   - Will this exceed line limits?
   - Should this use progressive disclosure instead?
   - Is this universally applicable?

4. PROPOSE the change
   - Show before/after diff concept
   - Explain which guideline principles apply
   - Ask for approval

5. APPLY with confirmation
   - Make the edit
   - Show final result
   - Verify line count
```

### Key Differentiators from Starting-Projects

| Aspect | Starting-Projects | Updating-CLAUDE.md |
|--------|-------------------|-------------------|
| Input state | No CLAUDE.md exists | CLAUDE.md exists |
| Discovery | Full project questionnaire | Focused on specific change |
| Research | Web search for best practices | None needed (guidelines known) |
| Output | New file | Edit to existing file |
| Scope | Entire project setup | Single update |

### Progressive Disclosure Enforcement

When update would make CLAUDE.md too long:

```
This addition would bring CLAUDE.md to 85 lines (over the 60-line ideal).

Options:
1. Add as brief pointer → Create detailed doc at .docs/[topic].md
2. Add condensed version → Reduce to essential info only
3. Add as-is → Accept longer file (still under 300 max)

Which approach?
```

### Automatic Behaviors Section Updates

Special handling for learned patterns:

```markdown
## Automatic Behaviors

When I mention a repeat problem ("this happened before", "same issue again"),
offer to save the solution as a learned pattern.

[NEW] When working with [topic], remember that [learned insight].
```

### Validation Checklist

Before applying any update:
- [ ] Change is universally applicable (not session-specific)
- [ ] No code style rules added
- [ ] Uses progressive disclosure where appropriate
- [ ] Final file stays under 60 lines (ideal) or 300 (max)
- [ ] Section structure matches template
- [ ] User confirmed the change

## Recommended Skill Structure

```
updating-claude-md/
├── SKILL.md                    # Main workflow
├── reference/
│   ├── update-types.md         # Classification of update types
│   └── validation-rules.md     # Guardrails and checks
└── templates/
    └── change-proposal.md      # How to present proposed changes
```

## Integration Points

### Upstream Skills
- `/learning-from-sessions` → May trigger updates for learned patterns
- `/starting-projects` → Creates initial CLAUDE.md this skill updates

### Downstream Impact
- All future Claude sessions read the updated CLAUDE.md

## Key Design Decisions for Skill Creation

1. **Read-first approach**: Always read and parse existing CLAUDE.md before proposing changes
2. **Guideline-aware**: Enforce the same 5 principles from starting-projects
3. **Progressive disclosure default**: When adding significant content, default to creating a `.docs/` file
4. **Diff-style proposals**: Show what will change before applying
5. **Line count awareness**: Track and warn about file size

## References

- `C:/code/commandbase/newskills/starting-projects/SKILL.md` - Main skill workflow
- `C:/code/commandbase/newskills/starting-projects/reference/claude-md-guidelines.md` - Core guidelines
- `C:/code/commandbase/newskills/starting-projects/templates/claude-md-template.md` - Template structure
- `C:/code/commandbase/newskills/discussing-features/SKILL.md` - Intent capture patterns
- `C:/code/commandbase/CLAUDE.md` - Live example (31 lines)
