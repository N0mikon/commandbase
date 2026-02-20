---
name: designing-services
description: "Use this skill when making infrastructure architecture decisions for homelab services. This includes choosing stack topology, networking strategy, authentication approach, data management policy, update strategy, and monitoring setup. Activate when the user says 'design services', 'infrastructure architecture', 'how should services be organized', or after completing research with /researching-services."
---

# Designing Services

You are making infrastructure architecture decisions for homelab services by analyzing research artifacts and brainstorm preferences, asking the user informed questions, and producing a design document with decisions and rationale.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO DESIGN WITHOUT RESEARCH ARTIFACTS FIRST
```

Design decisions must be grounded in infrastructure research. If no research artifacts exist, redirect to `/researching-services` first.

**No exceptions:**
- Don't design from assumptions - read research artifacts
- Don't skip research for "obvious" architectures - obvious to you is not obvious to the user
- Don't make decisions without presenting options when multiple valid approaches exist
- Don't include implementation details in the design doc - that's for Structure and Plan

## The Gate Function

```
BEFORE writing any design document:

1. READ: Find and read research artifacts (.docs/research/) relevant to this infrastructure
2. ANALYZE: Identify infrastructure design decisions that need to be made
3. QUESTION: Ask architecture choice questions inline as they arise (AskUserQuestion)
4. DESIGN: Spawn opus-model agents to reason through infrastructure architecture
5. WRITE: Create .docs/design/ document via docs-writer
6. PRESENT: Summary to user with decision list and link to design doc

Skipping steps = designing blind
```

## Initial Response

When this skill is invoked:

### If research artifacts are provided or referenced:
- Read ALL relevant research artifacts FULLY
- Also check `.docs/brainstorm/` for direction and preferences from `/brainstorming-services`
- Proceed to Step 2

### If no research artifacts exist:
```
No infrastructure research artifacts found for this topic.

Design decisions must be grounded in research. Please run:
- /researching-services — to analyze infrastructure state, services, networking, and configs

Then re-run /designing-services with the research output.
```

### If no parameters provided:
```
I'll help you make infrastructure architecture decisions for your homelab services.

Please provide:
1. A research artifact (.docs/research/) or infrastructure topic to design for
2. Any specific constraints or preferences

I'll analyze the research, identify design decisions, and work with you to make informed choices.
```

## Process Steps

### Step 1: Locate and Read Research Artifacts

- Check for research files mentioned by user or recently created in `.docs/research/` with services tags
- Read ALL relevant research artifacts FULLY — no limit/offset, no skimming
- Also check `.docs/brainstorm/` for brainstorming artifacts — read Direction, Decisions, and Claude's Discretion sections to inform design decisions
  - If brainstorm artifact exists: respect directional preferences as constraints (e.g., "Traefik not Nginx"), note Claude's Discretion areas where design has freedom
  - If no brainstorm artifact: proceed normally (brainstorming is optional in BRDSPI)
- If no research artifacts exist, STOP and redirect to research first
- Note key findings, constraints, and options discovered during research

### Step 2: Identify Design Decisions

Analyze research findings to determine what infrastructure decisions are needed. Categorize by services design domain (see `./reference/services-design-domains.md`):

- **Stack Topology** — service additions/removals, grouping, shared vs isolated
- **Networking Strategy** — network isolation, proxy routing, DNS, remote access
- **Auth Approach** — SSO, per-service auth, middleware chains
- **Data Management** — volume strategy, backup policy, retention
- **Update Strategy** — image pinning, rollback plan, testing
- **Monitoring** — health checks, alerting, dashboards (if user has monitoring tools)

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
   - Options must be specific: "Traefik with labels", "Nginx Proxy Manager" — NOT "Option A", "Option B"
   - Always include a "You decide" option for areas the user wants to delegate
   - See `./reference/services-design-domains.md` for example questions per domain
3. Capture rationale alongside each decision — WHY this approach, not just WHAT
4. When the user selects "You decide", document your reasoning as "Claude's Discretion"

**Secrets handling:** When designing, specify which secrets are NEEDED (e.g., "database password", "API key for service X") without including actual values. Design docs describe secret requirements, not secret contents.

### Step 4: Write Design Document

After all decisions are made:

1. Compile decisions with rationale into a design document
2. Spawn a `docs-writer` agent via the Task tool:

   ```
   Task prompt:
     doc_type: "design"
     topic: "<infrastructure purpose>"
     tags: [services, <relevant aspect tags>]
     references: [<research artifacts used, key config files>]
     content: |
       <compiled design document using ./templates/services-design-template.md>
   ```

3. The design doc must contain:
   - Decisions with rationale for each domain
   - Alternatives considered and why rejected
   - Claude's Discretion section for delegated decisions
   - Secrets requirements (what secrets are needed, not values)
   - Constraints discovered during research
   - NO implementation details — no compose YAML, no Docker image tags, no middleware config syntax

### Step 5: Present and Suggest Next Step

```
DESIGN COMPLETE
===============

Design document: .docs/design/MM-DD-YYYY-<topic>.md

Key decisions:
- [Decision 1]: [choice] — [one-line rationale]
- [Decision 2]: [choice] — [one-line rationale]
- [Decision 3]: [choice] — [one-line rationale]

Next: /structuring-services to map compose file layout and config placement
Or: /planning-services if structure is straightforward
```

## Important Guidelines

1. **Design captures WHY, not HOW** — decisions and rationale, no implementation details
2. **Research first, always** — every design decision references research findings
3. **Concrete options** — "Traefik with labels" not "Option A", "Shared PostgreSQL" not "Strategy 1"
4. **User decides, with context** — present trade-offs, let user choose
5. **Rationale is mandatory** — even for "obvious" choices, document why
6. **No compose YAML in design** — no image tags, no labels syntax, no middleware config

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
- Including implementation details (compose YAML, Docker image tags, config syntax) in the design doc
- Making decisions without asking user when multiple valid approaches exist
- Skipping inline questions to "move faster"
- Writing a design doc without spawning the docs-writer agent
- Proposing architecture without understanding existing infrastructure patterns
- Including secret values in the design document

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "The research already decided this" | Research reveals options. Design chooses between them with user. |
| "This is obvious, no question needed" | Obvious to you ≠ obvious to user. Ask. |
| "I'll include compose syntax to help planning" | Design doc is decisions only. Structure and Plan handle the rest. |
| "User said 'you decide' for everything" | Document what you decided and why. Rationale is mandatory. |
| "No research exists but I know Docker well" | Redirect to research. Design without evidence is guessing. |

## The Bottom Line

**Design captures WHY this architecture, not HOW to build it.**

Decisions with rationale. No implementation details. Concrete options. User chooses. Secrets described by name, never by value.

This is non-negotiable. Every design. Every time.
