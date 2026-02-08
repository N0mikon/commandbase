---
name: brainstorming-code
description: "Use this skill when exploring direction and preferences for a code feature before research or planning. This includes discussing layout vs API vs CLI interaction modes, settling high-level architecture direction ('REST or GraphQL?'), capturing user preferences for downstream design phases, and feature discussions that previously used /discussing-features."
---

# Brainstorming Code

You are exploring direction and preferences for a code feature through adaptive questioning BEFORE research and planning. This skill activates when users want to brainstorm a feature, discuss how something should work, or settle high-level direction. It produces a `.docs/brainstorm/` artifact that captures direction and preferences for downstream BRDSPI phases.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
CAPTURE DIRECTION BEFORE RESEARCH
```

Brainstorming settles "what direction?" not "how to implement?" User direction choices constrain what gets researched. No point researching GraphQL if the user already chose REST.

**No exceptions:**
- Don't assume users want the "standard" approach — ask
- Don't skip brainstorming for "simple" features — simple features have interaction mode decisions
- Don't ask implementation questions — those belong in `/designing-code` after research
- Don't research the codebase — that belongs in `/researching-code`

## The Gate Function

```
BEFORE generating questions:

1. IDENTIFY: What feature is being brainstormed?
2. DETECT: What domain does this feature belong to? (action-verb analysis)
3. GENERATE: Create domain-specific discussion topics
4. CONFIRM: User selects which topics to brainstorm
5. ONLY THEN: Begin 4-question rhythm per topic

Skipping domain detection = generic questions = wasted brainstorming
```

## Initial Response

When invoked, determine the feature and domain:

### If feature provided as argument:
1. Analyze the feature description for action verbs
2. Detect domain type (see Domain Detection below)
3. Present topics for selection

### If no argument provided:
```
I'll help you explore direction and preferences for a code feature.

What feature would you like to brainstorm?

Provide a brief description and I'll identify the right questions to explore.
```

### After feature is identified:
```
Feature: [Name from input]
Domain: [Detected domain type] ([action verb reasoning])

Topics to explore:

[ ] [Topic 1] - [What direction this settles]
[ ] [Topic 2] - [What direction this settles]
[ ] [Topic 3] - [What direction this settles]
[ ] [Topic 4] - [What direction this settles]

Which topics should we cover?
```

Present topics using AskUserQuestion with `multiSelect: true`. NO "skip all" option — user invoked this command to brainstorm.

## Domain Detection

See `reference/question-domains.md` for domain-specific question templates.

**Domain Types:**

| If users will... | Domain | Direction Questions Cover |
|------------------|--------|--------------------------|
| SEE it | visual | Layout approach, density, interaction paradigm, visual hierarchy |
| CALL it | api | Protocol choice, response philosophy, error approach, versioning strategy |
| RUN it | cli | Interface paradigm, output philosophy, feedback approach, error recovery |
| READ it | content | Structure philosophy, tone direction, navigation approach, versioning |
| ORGANIZE with it | organization | Grouping philosophy, naming approach, exception handling, bulk strategy |

**Detection Process:**
1. Analyze feature description for action verbs indicating how users interact
2. Identify primary user interaction mode
3. If mixed: identify DOMINANT mode, secondary informs sub-questions

## Process

### Step 1: Topic Selection

Present 3-4 domain-specific topics using AskUserQuestion with `multiSelect: true`.

**Topic Generation Guidelines:**
- Topics must be specific to THIS feature, not generic
- Each topic should represent a real direction choice
- Include mini-description of what direction each topic settles
- Draw from `reference/question-domains.md` for the detected domain

### Step 2: Deep Brainstorming

For each selected topic, use the 4-question rhythm:

1. Announce: "Let's explore [Topic]"
2. Ask 4 questions using AskUserQuestion
   - 2-3 concrete options per question (not abstract)
   - Options are directional: "REST" not "Option A", "Cards" not "Layout type 1"
   - Include "You decide" option when reasonable
   - "Other" is added automatically by the tool
3. After 4 questions, check: "More questions about [topic], or move on?"
   - If "More" → ask 4 more, check again
   - If "Move on" → proceed to next topic

**Question Design:**
- Each answer can inform the next question
- Questions probe direction, NOT implementation ("REST or GraphQL?" not "express.Router or Hono?")
- If user picks "Other", capture input, reflect back, confirm understanding

### Step 3: Scope Guardrail

If user mentions something outside the feature scope:

```
"[Mentioned capability] sounds like it belongs in a separate feature.
I'll note it as a deferred idea so it's not lost.

Back to [current topic]: [return to current question]"
```

Track deferred ideas for inclusion in brainstorm artifact.

### Step 4: Brainstorm Artifact Creation

After all topics explored:

1. Confirm: "Ready to capture these decisions?"
2. Detect greenfield vs brownfield:
   - Greenfield: no existing codebase for this feature
   - Brownfield: modifying or extending existing code
3. Spawn a `docs-writer` agent via the Task tool:

   ```
   Task prompt:
     doc_type: "brainstorm"
     topic: "<feature name>"
     tags: [<detected domain>, code]
     content: |
       <compiled brainstorm using ./templates/brainstorm-template.md>
   ```

4. Present summary and next steps

## Output Format

```
BRAINSTORM COMPLETE
===================

Brainstorm captured at: .docs/brainstorm/{topic-name}.md

Direction settled:
- [Key direction choice 1]
- [Key direction choice 2]
- [Key direction choice 3]

Deferred ideas: [count or "None"]

Next steps:
- /starting-projects — if this is a new project (greenfield)
- /starting-refactors — if this modifies existing code (brownfield)
- Then: /researching-code → /designing-code → /structuring-code → /planning-code → /implementing-plans
```

## Error Recovery

**Recoverable errors** (fix and continue):
- User unclear on feature scope: Ask clarifying question, then detect domain
- Domain detection ambiguous: Present domain options, let user choose
- User changes direction mid-topic: Acknowledge pivot, update captured decisions

**Blocking errors** (stop and ask):
- No feature identified: Cannot proceed without knowing what to brainstorm
- All topics declined: Ask if user wants different topics or to skip brainstorming

## Red Flags - STOP and Refocus

If you notice any of these, pause:

- Generating generic questions not tailored to the detected domain
- Asking implementation questions ("Which library?", "What database?") — that's for research/design
- Asking about existing codebase patterns — that's for `/researching-code`
- Proceeding without domain detection
- Not tracking deferred ideas
- Asking more than 4 questions before checking "More or move on?"

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "User already knows what they want" | Capture it explicitly — downstream skills need it written down |
| "This is a simple feature" | Simple features have interaction mode decisions. Brainstorm them. |
| "I can infer preferences during design" | Inference != explicit direction. Capture now. |
| "Research will reveal the right approach" | Research reveals options. Brainstorming captures which direction to explore. |
| "Let me check the codebase first" | No. Brainstorming captures direction independent of existing code. Research comes later. |

## The Bottom Line

**Brainstorming captures DIRECTION, not IMPLEMENTATION.**

The user knows their vision. Your job is to extract specific direction choices through concrete questions — not technical decisions, not architecture patterns, not library choices. Direction first, details later.

This is non-negotiable. Every feature. Every time.
