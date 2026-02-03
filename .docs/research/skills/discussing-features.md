# Research: discussing-features Skill

## Overview

The `discussing-features` skill (`~/.claude/skills/discussing-features/SKILL.md`) captures user implementation preferences through structured questioning BEFORE research or planning begins. It produces context documents in `.docs/context/{feature-name}.md` that constrain downstream research scope and planning decisions.

**Trigger phrases**: `let's discuss this feature`, `how should this work`, `design decisions for`, or before invoking `/planning-codebases` on a new feature

## The Iron Law (SKILL.md:12-24)

```
CAPTURE HOW PREFERENCES BEFORE RESEARCH
```

Discussion comes BEFORE research because user preferences constrain what gets researched. No point researching card layouts if the user already said they want a table view.

**No exceptions:**
- Don't assume user wants "standard" implementation
- Don't skip discussion for "simple" features
- Don't let technical constraints override user preferences before capturing them
- Don't re-ask questions that discussion context already answered

## The Gate Function (SKILL.md:26-38)

5-step process before generating questions:

1. **IDENTIFY**: What is the feature being discussed?
2. **DETECT**: What domain does this feature belong to?
3. **GENERATE**: Create domain-specific discussion topics
4. **CONFIRM**: User selects which topics to discuss
5. **ONLY THEN**: Begin 4-question rhythm per topic

## Domain Detection (SKILL.md:62-80)

| User Action | Domain | Example Topics |
|-------------|--------|----------------|
| SEE it | visual | Layout, density, interactions, empty states |
| CALL it | api | Response format, errors, versioning, auth |
| RUN it | cli | Flags, output format, progress, error handling |
| READ it | content | Structure, tone, depth, navigation |
| ORGANIZE with it | system | Criteria, grouping, naming, exceptions |

## Discussion Categories

### Visual Domain
**Trigger**: UI components, dashboards, displays, views, pages, screens

**Topics**:
1. Layout & Density - How information is arranged and spaced
2. Interaction Patterns - How users navigate and manipulate
3. Visual States - Loading, empty, error, success appearances
4. Information Hierarchy - What's prominent vs. secondary

**Example Questions**:
- "Cards, list, or table view?" → [Cards] [List] [Table] [You decide]
- "Click to expand, or navigate to detail page?" → [Expand in place] [New page] [Modal]

### API Domain
**Trigger**: Endpoints, APIs, services, integrations, webhooks

**Topics**:
1. Response Format - Structure and content of responses
2. Error Handling - How failures are communicated
3. Authentication & Authorization - Access control patterns
4. Versioning & Compatibility - How changes are managed

### CLI Domain
**Trigger**: Commands, scripts, tools, utilities, automation

**Topics**:
1. Output Format - How results are displayed
2. Flag Design - Command-line interface patterns
3. Progress & Feedback - How status is communicated
4. Error Recovery - How failures are handled

### Content Domain
**Trigger**: Documentation, help text, guides, notifications, messages

**Topics**:
1. Structure & Depth - How content is organized
2. Tone & Voice - Communication style
3. Navigation & Discovery - How users find content

### Organization Domain
**Trigger**: Sorting, filtering, categorizing, managing, structuring data

**Topics**:
1. Grouping Criteria - How items are categorized
2. Naming & Labels - How things are identified
3. Exception Handling - What happens with edge cases
4. Bulk Operations - How multiple items are handled

## Process: 4-Question Rhythm

For each selected topic:
1. Announce: "Let's talk about [Topic]"
2. Ask 4 questions using AskUserQuestion (2-3 concrete options per question)
3. After 4 questions, check: "More questions about [topic], or move on?"

## Decision Capture Format

### Output Structure
```
DISCUSSION COMPLETE
===================

Context captured at: .docs/context/{feature-name}.md

Decisions made:
- [Key decision 1]
- [Key decision 2]

Deferred ideas: [count or "None"]

Next steps:
- Run /planning-codebases to create implementation plan
- Or /researching-codebases if you need to understand existing patterns first
```

### Context Document Template
Written to `.docs/context/{feature-name}.md` with XML-tagged sections:
- `<domain>` - Feature scope
- `<decisions>` - Implementation decisions by topic
- `<specifics>` - User references and examples
- `<deferred>` - Ideas for other features

Downstream skills parse these sections:
- `/researching-codebases` reads `<decisions>` to focus research scope
- `/planning-codebases` reads `<decisions>` to honor user choices

## Anti-Patterns

**DON'T ask:**
- Technical architecture questions (defer to `/planning-codebases`)
- Performance optimization questions
- "Should we use library X?" (defer to research)

**DO ask:**
- User-observable behavior questions
- Visual and interaction preferences
- Error presentation preferences
- Output format preferences

## File References

- Main: `~/.claude/skills/discussing-features/SKILL.md`
- Domain templates: `~/.claude/skills/discussing-features/reference/question-domains.md`
- Context template: `~/.claude/skills/discussing-features/templates/context-template.md`
