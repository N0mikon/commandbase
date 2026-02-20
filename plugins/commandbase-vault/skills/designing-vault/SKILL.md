---
name: designing-vault
description: "Use this skill when making organizational decisions for an Obsidian vault. This includes designing MOC strategy, defining tagging taxonomy, choosing template patterns, setting frontmatter schema, and deciding linking conventions. Activate when the user says 'design vault', 'vault architecture', 'MOC strategy', 'tag taxonomy', or after completing research with /researching-vault."
---

# Designing Vault

You are making organizational decisions for an Obsidian vault by analyzing research artifacts and brainstorm preferences, asking the user informed questions, and producing a design document with decisions and rationale.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO DESIGN WITHOUT RESEARCH ARTIFACTS FIRST
```

Design decisions must be grounded in vault research. If no research artifacts exist, redirect to `/researching-vault` first.

**No exceptions:**
- Don't design from assumptions - read research artifacts
- Don't skip research for "obvious" organization - obvious to you is not obvious to the user
- Don't make decisions without presenting options when multiple valid approaches exist
- Don't include implementation details in the design doc - that's for Structure and Plan

## The Gate Function

```
BEFORE writing any design document:

1. READ: Find and read research artifacts (.docs/research/) relevant to this vault
2. ANALYZE: Identify vault design decisions that need to be made
3. QUESTION: Ask organizational choice questions inline as they arise (AskUserQuestion)
4. DESIGN: Spawn opus-model agents to reason through vault architecture
5. WRITE: Create .docs/design/ document via docs-writer
6. PRESENT: Summary to user with decision list and link to design doc

Skipping steps = designing blind
```

## Initial Response

When this skill is invoked:

### If research artifacts are provided or referenced:
- Read ALL relevant research artifacts FULLY
- Also check `.docs/brainstorm/` for direction and preferences from `/brainstorming-vault`
- Proceed to Step 2

### If no research artifacts exist:
```
No vault research artifacts found for this topic.

Design decisions must be grounded in research. Please run:
- /researching-vault — to analyze vault structure, tags, links, and conventions

Then re-run /designing-vault with the research output.
```

### If no parameters provided:
```
I'll help you make organizational decisions for your Obsidian vault.

Please provide:
1. A research artifact (.docs/research/) or vault topic to design for
2. Any specific constraints or preferences

I'll analyze the research, identify design decisions, and work with you to make informed choices.
```

## Process Steps

### Step 1: Locate and Read Research Artifacts

- Check for research files mentioned by user or recently created in `.docs/research/` with vault tags
- Read ALL relevant research artifacts FULLY — no limit/offset, no skimming
- Also check `.docs/brainstorm/` for brainstorming artifacts — read Direction, Decisions, and Claude's Discretion sections to inform design decisions
  - If brainstorm artifact exists: respect directional preferences as constraints (e.g., "Zettelkasten not PARA"), note Claude's Discretion areas where design has freedom
  - If no brainstorm artifact: proceed normally (brainstorming is optional in BRDSPI)
- If no research artifacts exist, STOP and redirect to research first
- Note key findings, constraints, and options discovered during research

### Step 2: Identify Design Decisions

Analyze research findings to determine what organizational decisions are needed. Categorize by vault design domain (see `./reference/vault-design-domains.md`):

- **Frontmatter Schema** — property names, types, required fields per note type
- **MOC Strategy** — hub-and-spoke, topic clusters, dynamic Dataview MOCs
- **Orphan Prevention** — linking conventions, MOC coverage requirements
- **Folder Boundaries** — what goes where, nesting depth, separation of concerns
- **Tag Taxonomy** — hierarchical vs flat, property tags vs inline, naming conventions
- **Template Design** — note types, Templater vs core templates, frontmatter defaults

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
   - Options must be specific: "Hub-and-spoke MOCs", "Flat topic tags" — NOT "Option A", "Option B"
   - Always include a "You decide" option for areas the user wants to delegate
   - See `./reference/vault-design-domains.md` for example questions per domain
3. Capture rationale alongside each decision — WHY this approach, not just WHAT
4. When the user selects "You decide", document your reasoning as "Claude's Discretion"

### Step 4: Write Design Document

After all decisions are made:

1. Compile decisions with rationale into a design document
2. Spawn a `docs-writer` agent via the Task tool:

   ```
   Task prompt:
     doc_type: "design"
     topic: "<vault name/purpose>"
     tags: [vault, <relevant aspect tags>]
     references: [<research artifacts used, key vault paths>]
     content: |
       <compiled design document using ./templates/vault-design-template.md>
   ```

3. The design doc must contain:
   - Decisions with rationale for each domain
   - Alternatives considered and why rejected
   - Claude's Discretion section for delegated decisions
   - Constraints discovered during research
   - NO implementation details — no note paths, no folder creation commands, no template syntax

### Step 5: Present and Suggest Next Step

```
DESIGN COMPLETE
===============

Design document: .docs/design/MM-DD-YYYY-<topic>.md

Key decisions:
- [Decision 1]: [choice] — [one-line rationale]
- [Decision 2]: [choice] — [one-line rationale]
- [Decision 3]: [choice] — [one-line rationale]

Next: /structuring-vault to map folder layout and note placement
Or: /planning-vault if structure is straightforward
```

## Important Guidelines

1. **Design captures WHY, not HOW** — decisions and rationale, no implementation details
2. **Research first, always** — every design decision references research findings
3. **Concrete options** — "Hub-and-spoke MOCs" not "Option A", "Hierarchical tags" not "Strategy 1"
4. **User decides, with context** — present trade-offs, let user choose
5. **Rationale is mandatory** — even for "obvious" choices, document why

## Self-Improvement

Before finishing, review this skill execution:

- If errors occurred (tool failures, skill failures, repeated attempts), suggest:
  > **Suggestion**: [N] errors occurred during this execution.
  > Consider running `/extracting-patterns` to capture learnings.
  >
  > Errors: [brief summary of error types]
- Only suggest when errors are meaningful — use judgment about significance.
- Do not auto-run. Suggest only.

## Red Flags - STOP and Redirect

If you notice any of these, pause:

- Designing without reading research artifacts first
- Including implementation details (note templates, folder creation commands) in the design doc
- Making decisions without asking user when multiple valid approaches exist
- Skipping inline questions to "move faster"
- Writing a design doc without spawning the docs-writer agent
- Proposing organization without understanding existing vault patterns

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The research already decided this" | Research reveals options. Design chooses between them with user. |
| "This is obvious, no question needed" | Obvious to you ≠ obvious to user. Ask. |
| "I'll include template syntax to help planning" | Design doc is decisions only. Structure and Plan handle the rest. |
| "User said 'you decide' for everything" | Document what you decided and why. Rationale is mandatory. |
| "No research exists but I know Obsidian well" | Redirect to research. Design without evidence is guessing. |

## The Bottom Line

**Design captures WHY this organization, not HOW to build it.**

Decisions with rationale. No implementation details. Concrete options. User chooses.

This is non-negotiable. Every design. Every time.
