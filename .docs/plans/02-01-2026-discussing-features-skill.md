---
git_commit: 2d50723
last_updated: 2026-02-05
last_updated_by: docs-updater
last_updated_note: "Updated git_commit to current HEAD - no content changes needed, plan remains completed"
topic: "/discussing-features Skill Implementation"
tags: [plan, skill, discussing-features, pre-planning, context-engineering]
status: complete
research: .docs/research/02-01-2026-get-shit-done-skill-comparison.md
references:
  - newskills/discussing-features/SKILL.md
  - newskills/discussing-features/reference/question-domains.md
  - newskills/discussing-features/templates/context-template.md
---

# /discussing-features Skill Implementation Plan

## Overview

Create a new `/discussing-features` skill that captures user implementation preferences **before** research and planning. This skill fills the gap identified in the GSD comparison: we currently jump straight to research without understanding HOW the user wants features to work. The output constrains downstream research scope and planning decisions.

## Current State Analysis

### What Exists Now

| Skill | Purpose | Gap |
|-------|---------|-----|
| `/starting-projects` | **WHAT** are we building (one-time) | Project setup, not per-feature |
| `/researching-codebases` | **WHAT EXISTS** in the codebase | No user preference input |
| `/planning-codebases` | **HOW TO IMPLEMENT** | Asks questions AFTER research |

### Key Discoveries:

- `/planning-codebases` proceeds directly from user input to research (`SKILL.md:78-83`)
- No `.docs/context/` directory convention exists yet
- GSD's `discuss-phase` uses domain detection to generate relevant questions (`discuss-phase.md:56-64`)
- GSD outputs to `.planning/phases/XX-name/` - we'll adapt to `.docs/context/{feature-name}.md`
- Workflow skill template at `creating-skills/templates/workflow-skill-template.md` provides structure
- 4-question rhythm pattern from GSD prevents both endless questioning and premature closure

### Integration Points

1. **Output Location**: `.docs/context/{feature-name}.md`
2. **Downstream Consumer 1**: `/researching-codebases` - focuses research based on preferences
3. **Downstream Consumer 2**: `/planning-codebases` - honors decisions, doesn't revisit them
4. **Upstream Trigger**: After `/starting-projects` for new projects, standalone for existing codebases

## Desired End State

A `/discussing-features` skill that:

1. Detects feature domain (visual/API/CLI/documentation/organization)
2. Generates 3-4 domain-specific discussion topics
3. Uses 4-question rhythm with check-ins for depth control
4. Outputs structured context document to `.docs/context/{feature-name}.md`
5. Captures deferred ideas without acting on them
6. Provides clear handoff to `/planning-codebases` or `/researching-codebases`

**Verification**: Run `/discussing-features` on a sample feature, verify output structure matches template, verify downstream skills can read and honor the context.

## What We're NOT Doing

- Modifying `/planning-codebases` (separate enhancement task)
- Modifying `/researching-codebases` (separate enhancement task)
- Adding model profile selection
- Adding wave-based execution
- Creating `/debugging` skill (separate task)
- Creating `/quick-implementing` skill (separate task)

## Implementation Approach

Create the skill using our established directory-based structure with progressive disclosure. The skill follows the workflow pattern with domain detection, adaptive questioning, and structured output.

---

## Phase 1: Core Skill Structure

### Overview
Create the SKILL.md file with frontmatter, iron law, gate function, and main workflow.

### Changes Required:

#### 1. Create Skill Directory
**File**: `newskills/discussing-features/`
**Changes**: Create directory structure

#### 2. Create SKILL.md
**File**: `newskills/discussing-features/SKILL.md`
**Changes**: Main skill definition

```markdown
---
name: discussing-features
description: "Use this skill when capturing user intent before planning a feature. This includes discussing layout preferences, API design choices, UX decisions, error handling behavior, and content organization. Activate when the user says 'let's discuss this feature', 'how should this work', 'design decisions for', or before invoking /planning-codebases on a new feature."
---

# Feature Discussion

You are capturing implementation decisions from the user through adaptive questioning BEFORE research and planning. This skill produces a context document that constrains downstream research scope and planning decisions.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
CAPTURE HOW PREFERENCES BEFORE RESEARCH
```

Discussion comes BEFORE research because user preferences constrain what gets researched. No point researching card layouts if the user already said they want a table view.

**No exceptions:**
- Don't assume user wants "standard" implementation
- Don't skip discussion for "simple" features (simple features have UX decisions)
- Don't let technical constraints override user preferences before capturing them
- Don't re-ask questions that discussion context already answered

## The Gate Function

```
BEFORE generating questions:

1. IDENTIFY: What is the feature being discussed?
2. DETECT: What domain does this feature belong to?
3. GENERATE: Create domain-specific discussion topics
4. CONFIRM: User selects which topics to discuss
5. ONLY THEN: Begin 4-question rhythm per topic

Skipping domain detection = generic questions = wasted discussion
```

## Initial Response

When invoked, determine the feature and domain:

1. If feature name provided as argument, use it
2. If no argument, ask: "What feature would you like to discuss?"
3. Analyze the feature to detect domain type
4. Present discussion topics for selection

```
Feature: [Name from input]
Domain: [Detected domain type]
Topics I'd like to discuss:

☐ [Topic 1] — [What this covers]
☐ [Topic 2] — [What this covers]
☐ [Topic 3] — [What this covers]
☐ [Topic 4] — [What this covers]

Which topics should we cover? (Select all that apply)
```

## Domain Detection

See `reference/question-domains.md` for domain-specific question templates.

**Domain Types:**

| If users will... | Domain | Example Topics |
|------------------|--------|----------------|
| SEE it | visual | Layout, density, interactions, empty states |
| CALL it | api | Response format, errors, versioning, auth |
| RUN it | cli | Flags, output format, progress, error handling |
| READ it | content | Structure, tone, depth, navigation |
| ORGANIZE with it | system | Criteria, grouping, naming, exceptions |

**Detection Process:**
1. Analyze feature description for action verbs
2. Identify primary user interaction mode
3. If mixed: identify DOMINANT mode, secondary informs sub-questions

## Process

### Step 1: Topic Selection

Present 3-4 domain-specific topics using AskUserQuestion with multiSelect: true.

**Critical**: NO "skip all" option. User invoked this command to discuss - give them concrete topics.

**Topic Generation Guidelines:**
- Topics must be specific to THIS feature, not generic
- Each topic should represent a real decision point
- Include mini-description of what each topic covers

### Step 2: Deep Discussion

For each selected topic, use the 4-question rhythm:

1. Announce: "Let's talk about [Topic]"
2. Ask 4 questions using AskUserQuestion
   - 2-3 concrete options per question (not abstract)
   - Include "You decide" option when reasonable
   - "Other" is added automatically by the tool
3. After 4 questions, check: "More questions about [topic], or move on?"
   - If "More" → ask 4 more, check again
   - If "Move on" → proceed to next topic

**Question Design:**
- Options are concrete: "Cards" not "Option A"
- Each answer can inform the next question
- If user picks "Other", capture input, reflect back, confirm understanding

### Step 3: Scope Guardrail

If user mentions something outside the feature scope:

```
"[Mentioned capability] sounds like it belongs in a separate feature.
I'll note it as a deferred idea so it's not lost.

Back to [current topic]: [return to current question]"
```

Track deferred ideas for inclusion in context document.

### Step 4: Context Document Creation

After all topics discussed:

1. Confirm: "Ready to create the context document?"
2. Create `.docs/context/` directory if needed
3. Write context document using `templates/context-template.md`
4. Present summary and next steps

## Output Format

```
DISCUSSION COMPLETE
===================

Context captured at: .docs/context/{feature-name}.md

Decisions made:
- [Key decision 1]
- [Key decision 2]
- [Key decision 3]

Deferred ideas: [count or "None"]

Next steps:
- Run /planning-codebases to create implementation plan
- Or /researching-codebases if you need to understand existing patterns first
```

## Error Recovery

**Recoverable errors** (fix and continue):
- User unclear on feature scope: Ask clarifying question, then detect domain
- Domain detection ambiguous: Present options, let user choose

**Blocking errors** (stop and ask):
- No feature identified: Cannot proceed without knowing what to discuss
- All topics declined: Ask if user wants different topics or to skip discussion

## Red Flags - STOP and Refocus

If you notice any of these, pause:

- Generating generic questions (not domain-specific)
- Asking technical/architecture questions (that's for planning)
- Asking about codebase patterns (that's for research)
- Proceeding without domain detection
- Not tracking deferred ideas

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User already knows what they want" | Capture it explicitly - downstream agents need it written |
| "This is a simple feature" | Simple features have UX decisions. Discuss them. |
| "I can infer preferences during planning" | Inference ≠ explicit decision. Capture now. |
| "Research will reveal the right approach" | Research reveals options. User chooses approach. |

## The Bottom Line

**Discussion captures HOW, not WHAT.**

The user knows their vision. Your job is to extract specific decisions through concrete questions, not abstract preferences. Every feature. Every time.
```

### Success Criteria:
- [x] SKILL.md follows workflow template structure
- [x] Frontmatter description triggers on correct phrases
- [x] Iron Law and Gate Function enforce discuss-before-research
- [x] Domain detection covered with examples
- [x] 4-question rhythm documented
- [x] Scope guardrail pattern included
- [x] Output location specified as `.docs/context/{feature-name}.md`

---

## Phase 2: Question Domains Reference

### Overview
Create reference file with domain-specific question templates.

### Changes Required:

#### 1. Create Reference Directory and File
**File**: `newskills/discussing-features/reference/question-domains.md`
**Changes**: Domain-specific question templates

```markdown
# Question Domains Reference

This reference provides domain-specific question templates. Use these as starting points - adapt questions to the specific feature being discussed.

## Visual Domain (Users SEE)

**Trigger:** UI components, dashboards, displays, views, pages, screens

**Default Topics:**
1. **Layout & Density** — How information is arranged and spaced
2. **Interaction Patterns** — How users navigate and manipulate
3. **Visual States** — Loading, empty, error, success appearances
4. **Information Hierarchy** — What's prominent vs. secondary

**Example Questions:**

Layout:
- "Cards, list, or table view?" → [Cards] [List] [Table] [You decide]
- "Dense with more info, or spacious with less?" → [Dense] [Spacious] [You decide]
- "Single column or multi-column?" → [Single] [Multi] [Responsive] [You decide]

Interaction:
- "Click to expand, or navigate to detail page?" → [Expand in place] [New page] [Modal] [You decide]
- "Infinite scroll or pagination?" → [Infinite scroll] [Pagination] [Load more button] [You decide]

States:
- "Empty state: helpful message or call-to-action?" → [Message only] [CTA to create] [You decide]
- "Loading: skeleton, spinner, or progressive?" → [Skeleton] [Spinner] [Progressive] [You decide]

---

## API Domain (Users CALL)

**Trigger:** Endpoints, APIs, services, integrations, webhooks

**Default Topics:**
1. **Response Format** — Structure and content of responses
2. **Error Handling** — How failures are communicated
3. **Authentication & Authorization** — Access control patterns
4. **Versioning & Compatibility** — How changes are managed

**Example Questions:**

Response:
- "Return minimal data or include related resources?" → [Minimal] [Include related] [Configurable via params] [You decide]
- "Envelope wrapper or direct response?" → [Envelope {data, meta}] [Direct] [You decide]
- "Pagination style?" → [Offset/limit] [Cursor-based] [Page numbers] [You decide]

Errors:
- "Error detail level?" → [Code only] [Code + message] [Code + message + suggestions] [You decide]
- "Validation errors: first only or all?" → [First error] [All errors] [You decide]

---

## CLI Domain (Users RUN)

**Trigger:** Commands, scripts, tools, utilities, automation

**Default Topics:**
1. **Output Format** — How results are displayed
2. **Flag Design** — Command-line interface patterns
3. **Progress & Feedback** — How status is communicated
4. **Error Recovery** — How failures are handled

**Example Questions:**

Output:
- "Default output: human-readable or machine-parseable?" → [Human (pretty)] [Machine (JSON)] [Auto-detect TTY] [You decide]
- "Verbosity levels?" → [Quiet/normal only] [Quiet/normal/verbose] [Multiple -v flags] [You decide]

Flags:
- "Short flags, long flags, or both?" → [Long only] [Both] [You decide]
- "Positional args or named flags?" → [Positional] [Named] [Mix] [You decide]

Progress:
- "Long operations: silent, spinner, or progress bar?" → [Silent] [Spinner] [Progress bar] [You decide]

---

## Content Domain (Users READ)

**Trigger:** Documentation, help text, guides, notifications, messages

**Default Topics:**
1. **Structure & Depth** — How content is organized
2. **Tone & Voice** — Communication style
3. **Navigation & Discovery** — How users find content
4. **Versioning** — How content changes are managed

**Example Questions:**

Structure:
- "Quick reference or comprehensive guide?" → [Quick reference] [Comprehensive] [Both with toggle] [You decide]
- "Inline examples or separate examples section?" → [Inline] [Separate] [Both] [You decide]

Tone:
- "Formal or conversational?" → [Formal] [Conversational] [You decide]
- "Technical precision or accessibility first?" → [Technical] [Accessible] [Layered (simple → advanced)] [You decide]

---

## Organization Domain (Users ORGANIZE)

**Trigger:** Sorting, filtering, categorizing, managing, structuring data

**Default Topics:**
1. **Grouping Criteria** — How items are categorized
2. **Naming & Labels** — How things are identified
3. **Exception Handling** — What happens with edge cases
4. **Bulk Operations** — How multiple items are handled

**Example Questions:**

Grouping:
- "Primary grouping method?" → [By date] [By type] [By status] [User-defined] [You decide]
- "Allow multiple categories per item?" → [Single category] [Multiple tags] [You decide]

Exceptions:
- "Items that don't fit categories?" → [Uncategorized bucket] [Force categorization] [Special 'Other'] [You decide]
- "Duplicate detection?" → [Automatic merge] [Flag for review] [Allow duplicates] [You decide]

---

## Mixed Domain Handling

When a feature spans multiple domains:

1. **Identify dominant domain** - What's the PRIMARY user interaction?
2. **Use dominant domain topics** - Start with those questions
3. **Pull 1-2 topics from secondary domain** - Add relevant sub-questions

Example: "User settings page" = Visual (dominant) + API (data persistence)
- Lead with visual questions (layout, states)
- Add API question: "Settings save immediately or require explicit save?"

---

## Anti-Patterns

**DON'T ask:**
- Technical architecture questions (defer to /planning-codebases)
- Performance optimization questions (defer to planning)
- "Should we use library X?" (defer to research)
- Generic questions not specific to this feature

**DO ask:**
- User-observable behavior questions
- Visual and interaction preferences
- Error presentation (not error handling implementation)
- Output format preferences
```

### Success Criteria:
- [x] All 5 domains have topic templates
- [x] Example questions provided for each domain
- [x] Mixed domain handling explained
- [x] Anti-patterns documented
- [x] Questions are concrete, not abstract

---

## Phase 3: Context Output Template

### Overview
Create template for the context document output.

### Changes Required:

#### 1. Create Templates Directory and File
**File**: `newskills/discussing-features/templates/context-template.md`
**Changes**: Output template with XML tags for machine parsing

```markdown
# Context Document Template

Use this template when writing context documents to `.docs/context/{feature-name}.md`.

## File Naming

- **Location**: `.docs/context/`
- **Format**: `{feature-name}.md` (lowercase, hyphens)
- **Examples**: `user-profile-page.md`, `export-api.md`, `backup-cli.md`

## Template

```markdown
---
feature: "[Feature Name]"
domain: [visual|api|cli|content|organization]
gathered: [YYYY-MM-DD]
status: ready-for-planning
---

# [Feature Name] - Implementation Context

<domain>
## Feature Scope

[One paragraph describing what this feature delivers - the scope anchor]
</domain>

<decisions>
## Implementation Decisions

### [Topic 1 that was discussed]
- [Specific decision made]
- [Another decision if applicable]

### [Topic 2 that was discussed]
- [Specific decision made]

### Claude's Discretion
[Areas where user explicitly said "you decide"]
[If none: "User provided specific preferences for all discussed topics."]
</decisions>

<specifics>
## Specific Requests

[User references, examples, "I want it like X" moments]
[If none: "No specific references provided — open to standard approaches that fit the decisions above."]
</specifics>

<deferred>
## Deferred Ideas

[Ideas mentioned that belong to other features or future scope]
[If none: "None — discussion stayed within feature scope."]
</deferred>

---
*Context gathered: [YYYY-MM-DD]*
*Next: /planning-codebases or /researching-codebases*
```

## Template Usage Notes

### XML Tags Purpose

The XML tags (`<domain>`, `<decisions>`, `<specifics>`, `<deferred>`) enable downstream skills to parse specific sections:

- `/researching-codebases` reads `<decisions>` to focus research scope
- `/planning-codebases` reads `<decisions>` to honor user choices
- Both read `<deferred>` to know what's out of scope

### Decisions Section

- **One heading per discussed topic** - categories emerge from discussion
- **Concrete, not vague** - "Card-based layout with 3 columns" not "Modern feel"
- **Claude's Discretion subsection** - Explicitly notes where user delegated

### Deferred Ideas

- Capture ideas that came up but belong elsewhere
- Don't lose them, don't act on them
- Helps user track future features

### Quality Checklist

Before finalizing context document:
- [ ] Decisions are specific enough for downstream agents to act without re-asking
- [ ] Each discussed topic has at least one concrete decision
- [ ] Scope section matches original feature description
- [ ] Deferred ideas are captured (or explicitly noted as none)
- [ ] No technical/architecture decisions (those belong in planning)
```

### Success Criteria:
- [x] Template has YAML frontmatter
- [x] XML tags included for machine parsing
- [x] All sections documented with examples
- [x] Claude's Discretion section included
- [x] Deferred Ideas section included
- [x] Quality checklist provided

---

## Phase 4: Deploy and Test

### Overview
Deploy skill to global config and verify it works.

### Changes Required:

#### 1. Deploy to Global Config
**Command**: `cp -r newskills/discussing-features ~/.claude/skills/`

#### 2. Test with Sample Feature
**Test scenarios**:
- Visual feature: "user profile page"
- API feature: "export endpoint"
- CLI feature: "backup command"

### Success Criteria:
- [x] Skill appears in Claude Code skill list
- [x] Skill deployed to ~/.claude/skills/discussing-features/
- [ ] Invocation with "let's discuss this feature" triggers skill (requires interactive test)
- [ ] Domain detection works for visual/API/CLI features (requires interactive test)
- [ ] 4-question rhythm functions correctly (requires interactive test)
- [ ] Context document created at `.docs/context/{feature-name}.md` (requires interactive test)
- [ ] Output matches template structure (requires interactive test)
- [ ] Deferred ideas captured when mentioned (requires interactive test)

---

## Testing Strategy

### Unit Tests (Manual):
- Verify domain detection for each type (visual, API, CLI, content, organization)
- Verify 4-question rhythm check-in appears
- Verify scope guardrail triggers on out-of-scope mentions
- Verify "Other" option handling

### Integration Tests:
- Run `/discussing-features user-dashboard`
- Verify output at `.docs/context/user-dashboard.md`
- Run `/planning-codebases` and verify it reads the context file
- Verify research scope is constrained by decisions

## References

- Research: `.docs/research/02-01-2026-get-shit-done-skill-comparison.md`
- GSD discuss-phase: `C:/code/repo-library/get-shit-done/commands/gsd/discuss-phase.md`
- Workflow template: `newskills/creating-skills/templates/workflow-skill-template.md`
- Planning skill: `newskills/planning-codebases/SKILL.md`
