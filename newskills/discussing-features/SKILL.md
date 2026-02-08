<!-- ARCHIVED: Phase 4 (2026-02-07). Absorbed by /brainstorming-code (domain detection,
preferences) and /designing-code (technical choices). Kept as reference. -->
---
name: discussing-features
description: "Use this skill when capturing user intent before planning a feature. This includes discussing layout preferences, API design choices, UX decisions, error handling behavior, and content organization. Activate when the user says 'let's discuss this feature', 'how should this work', 'design decisions for', or before invoking /planning-code on a new feature."
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

[ ] [Topic 1] - [What this covers]
[ ] [Topic 2] - [What this covers]
[ ] [Topic 3] - [What this covers]
[ ] [Topic 4] - [What this covers]

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
   - If "More" -> ask 4 more, check again
   - If "Move on" -> proceed to next topic

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
- Run /planning-code to create implementation plan
- Or /researching-code if you need to understand existing patterns first
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
| "I can infer preferences during planning" | Inference != explicit decision. Capture now. |
| "Research will reveal the right approach" | Research reveals options. User chooses approach. |

## The Bottom Line

**Discussion captures HOW, not WHAT.**

The user knows their vision. Your job is to extract specific decisions through concrete questions, not abstract preferences. Every feature. Every time.
