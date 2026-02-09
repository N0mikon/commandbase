---
name: designing-code
description: "Use this skill when making architectural decisions for a feature or system. This includes choosing API shapes, selecting patterns, resolving trade-offs, defining component boundaries, deciding error handling strategies, and making state management choices. Activate when the user says 'design this', 'architecture decisions', 'how should this be structured', or after completing research with /researching-code."
---

# Designing Code

You are making architectural decisions for a feature or system by analyzing research artifacts, asking the user informed technical questions, and producing a design document with decisions and rationale.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO DESIGN WITHOUT RESEARCH ARTIFACTS FIRST
```

Design decisions must be grounded in codebase research. If no research artifacts exist, redirect to `/researching-code` first.

**No exceptions:**
- Don't design from assumptions - read research artifacts
- Don't skip research for "obvious" architectures - obvious to you is not obvious to the user
- Don't make decisions without presenting options when multiple valid approaches exist
- Don't include implementation details in the design doc - that's for Structure and Plan

## The Gate Function

```
BEFORE writing any design document:

1. READ: Find and read research artifacts (.docs/research/) relevant to this task
2. ANALYZE: Identify design decisions that need to be made
3. QUESTION: Ask technical choice questions inline as they arise (AskUserQuestion)
4. DESIGN: Spawn opus-model agents to reason through architecture
5. WRITE: Create .docs/design/ document via docs-writer
6. PRESENT: Summary to user with decision list and link to design doc

Skipping steps = designing blind
```

## Initial Response

When this skill is invoked:

### If research artifacts are provided or referenced:
- Read ALL relevant research artifacts FULLY
- Also check `.docs/brainstorm/` for direction and preferences from `/brainstorming-code`
- Proceed to Step 2

### If no research artifacts exist:
```
No research artifacts found for this topic.

Design decisions must be grounded in research. Please run one of:
- /researching-code — to analyze codebase patterns and architecture
- /researching-web — to research community best practices
- /researching-frameworks — to get framework-specific documentation

Then re-run /designing-code with the research output.
```

### If no parameters provided:
```
I'll help you make architectural decisions for your feature or system.

Please provide:
1. A research artifact (.docs/research/) or topic to design for
2. Any specific constraints or preferences

I'll analyze the research, identify design decisions, and work with you to make informed choices.
```

## Process Steps

### Step 1: Locate and Read Research Artifacts

- Check for research files mentioned by user or recently created in `.docs/research/`
- **Staleness auto-update**: For each research or brainstorm artifact found, check its freshness before reading:
  ```bash
  f="<artifact-path>"
  commit=$(head -10 "$f" | grep "^git_commit:" | awk '{print $2}')
  if [ -n "$commit" ] && [ "$commit" != "n/a" ]; then
    git rev-parse "$commit" >/dev/null 2>&1 && \
    behind=$(git rev-list "$commit"..HEAD --count 2>/dev/null)
    [ -n "$behind" ] && [ "$behind" -gt 3 ] && echo "$behind"
  fi
  ```
  - If >3 commits behind: spawn docs-updater agent to refresh it before reading
  - If docs-updater archives it: skip this artifact and note it was obsolete
  - If current or no git_commit: proceed normally
- Read ALL relevant research artifacts FULLY — no limit/offset, no skimming
- Also check `.docs/brainstorm/` for brainstorming artifacts — apply the same staleness check, then read Direction, Decisions, and Claude's Discretion sections to inform design decisions
  - If brainstorm artifact exists: respect directional preferences as constraints (e.g., "REST not GraphQL"), note Claude's Discretion areas where design has freedom
  - If no brainstorm artifact: proceed normally (brainstorming is optional in BRDSPI)
- If no research artifacts exist, STOP and redirect to research first
- Note key findings, constraints, and options discovered during research

### Step 2: Identify Design Decisions

Analyze research findings to determine what architectural decisions are needed. Categorize by design domain (see `./reference/design-domains.md`):

- **API Design** — endpoints, function signatures, data contracts, versioning
- **Pattern Selection** — architectural patterns, data flow, state management
- **Error Strategy** — failure modes, recovery approaches, user-facing errors
- **Component Boundaries** — modules, interfaces, dependency direction
- **Data & State** — storage, caching, data flow, synchronization

Present decision topics to user for confirmation:
```
Based on the research, I've identified these design decisions:

1. [Domain]: [Decision topic]
2. [Domain]: [Decision topic]
3. [Domain]: [Decision topic]

Are these the right areas to focus on? Any to add or skip?
```

### Step 3: Design with Inline Questioning

For each design domain that needs decisions:

1. Spawn an opus-model Task agent to analyze the options based on research findings
2. When a decision point requires user input, use AskUserQuestion with concrete options
   - Options must be specific: "REST", "GraphQL", "tRPC" — NOT "Option A", "Option B"
   - Always include a "You decide" option for areas the user wants to delegate
   - See `./reference/design-domains.md` for example questions per domain
3. Capture rationale alongside each decision — WHY this approach, not just WHAT
4. When the user selects "You decide", document your reasoning as "Claude's Discretion"

### Step 4: Write Design Document

After all decisions are made:

1. Compile decisions with rationale into a design document
2. Spawn a `docs-writer` agent via the Task tool:

   ```
   Task prompt:
     doc_type: "design"
     topic: "<feature/system name>"
     tags: [<relevant component tags>]
     references: [<research artifacts used, key files affected>]
     content: |
       <compiled design document using ./templates/design-document-template.md>
   ```

3. The design doc must contain:
   - Decisions with rationale for each domain
   - Alternatives considered and why rejected
   - Claude's Discretion section for delegated decisions
   - Constraints discovered during research
   - NO implementation details — no code, no file paths, no line numbers

### Step 5: Present and Suggest Next Step

```
DESIGN COMPLETE
===============

Design document: .docs/design/MM-DD-YYYY-<topic>.md

Key decisions:
- [Decision 1]: [choice] — [one-line rationale]
- [Decision 2]: [choice] — [one-line rationale]
- [Decision 3]: [choice] — [one-line rationale]

Next: /structuring-code to map file placement and module organization
Or: /planning-code if structure is straightforward
```

## Important Guidelines

1. **Design captures WHY, not HOW** — decisions and rationale, no implementation details
2. **Research first, always** — every design decision references research findings
3. **Concrete options** — "JWT" not "Option A", "PostgreSQL" not "Database option 1"
4. **User decides, with context** — present trade-offs, let user choose
5. **Rationale is mandatory** — even for "obvious" choices, document why

## Red Flags - STOP and Redirect

If you notice any of these, pause:

- Designing without reading research artifacts first
- Including implementation details (code, specific line changes) in the design doc
- Making decisions without asking user when multiple valid approaches exist
- Skipping inline questions to "move faster"
- Writing a design doc without spawning the docs-writer agent
- Proposing architecture without understanding existing codebase patterns

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The research already decided this" | Research reveals options. Design chooses between them with user. |
| "This is obvious, no question needed" | Obvious to you ≠ obvious to user. Ask. |
| "I'll include implementation hints to help planning" | Design doc is decisions only. Structure and Plan handle the rest. |
| "User said 'you decide' for everything" | Document what you decided and why. Rationale is mandatory. |
| "No research exists but I know the answer" | Redirect to research. Design without evidence is guessing. |

## The Bottom Line

**Design captures WHY this approach, not HOW to build it.**

Decisions with rationale. No implementation details. Concrete options. User chooses.

This is non-negotiable. Every design. Every time.
