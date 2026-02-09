---
name: researching-frameworks
description: "Use this skill when researching framework documentation and library APIs before building a new project or adding a major dependency. This includes fetching current docs via Context7 MCP, gathering version-specific patterns and breaking changes, building dependency compatibility matrices, recording architecture decisions as ADRs, and producing .docs/references/ artifacts for offline use. Activate when the user says 'research this framework', 'get current docs for', 'what are the latest patterns for', or before scaffolding a new project with /starting-projects."
---

# Researching Frameworks

You are tasked with gathering current, authoritative framework and library documentation before any code is written. This skill combines Context7 MCP (live framework docs) with web research (ecosystem patterns, gotchas) to produce structured reference artifacts in `.docs/references/`.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Solve the stale training data problem. Frameworks iterate fast - patterns from 6 months ago may be deprecated. Your job is to fetch what's current, verify it, and persist it so this project has a reliable documentation baseline.

## The Iron Law

```
NO RECOMMENDATION WITHOUT CURRENT DOCUMENTATION
```

Don't suggest patterns, configurations, or dependency versions based on training data alone. Fetch current docs first.

**No exceptions:**
- Don't skip Context7 because "I already know this framework well"
- Don't recommend a version without checking the latest release
- Don't describe an API without verifying it exists in the current version
- Don't produce reference docs without source URLs

## The Gate Function

```
BEFORE producing any framework reference artifacts:

1. IDENTIFY: What frameworks/libraries need research?
2. DETECT: Is Context7 MCP available? (ToolSearch for "resolve-library-id")
3. TIER: Classify each dependency by research tier (see ./reference/research-tiers.md)
4. FETCH: Query Context7 for Tier 1 dependencies, web search for patterns
5. VERIFY: Cross-reference Context7 docs against web findings
6. PERSIST: Write .docs/references/ artifacts
7. ONLY THEN: Present findings and recommendations

Skip detection = wasted queries on unavailable tools
Skip tiering = researching everything at equal depth (token waste)
Skip persistence = research that dies with the session
```

## Initial Response

When this skill is invoked, determine the situation:

1. **If called with a specific framework/stack**: Begin research immediately
2. **If called by `/starting-projects`**: Receive the tech stack from discovery, begin research
3. **If no parameters**: Ask what frameworks to research

```
I'll research current documentation for your tech stack. First, let me check what documentation tools are available.
```

Then immediately check for Context7 MCP availability.

## Modes

### Mode A: Standalone Research

Use when the user directly invokes this skill with a framework or tech stack.

**Steps:**
1. Parse the requested frameworks/libraries from user input
2. Detect Context7 availability
3. Classify dependencies by tier
4. Execute research (see Process below)
5. Write `.docs/references/` artifacts
6. Present findings with recommendations

### Mode B: Called by /starting-projects

Use when `/starting-projects` delegates Phase 2 research to this skill.

**Steps:**
1. Receive tech stack from discovery phase (framework, language, key dependencies)
2. Detect Context7 availability
3. Classify all discovered dependencies by tier
4. Execute research (see Process below)
5. Write `.docs/references/` artifacts
6. Return findings to `/starting-projects` for plan creation

### Mode C: Adding a Dependency

Use when researching a single new framework/library to add to an existing project.

**Steps:**
1. Identify the new dependency and the existing stack
2. Detect Context7 availability
3. Research the new dependency at Tier 1 depth
4. Check compatibility with existing dependencies
5. Update `.docs/references/` with new dependency info
6. Present integration guidance

## Process

### Step 1: Detect Context7

Use ToolSearch to check for Context7 MCP availability.

See ./reference/context7-usage.md for detection logic, tool usage patterns, and fallback behavior.

**Decision point:**
- If Context7 available: Use it as primary source, web search as supplement
- If Context7 unavailable: Use web search as primary, WebFetch for official docs URLs

### Step 2: Classify Dependencies

Assign each framework/library a research tier. See ./reference/research-tiers.md for the full tier definitions.

**Quick reference:**
- **Tier 1** (always): Primary framework, language runtime - full depth research
- **Tier 2** (major deps): Testing, build tools, CSS framework - focused research
- **Tier 3** (on request): Database, auth, deployment - research if user specifies
- **Tier 4** (AI-specific): MCP servers, AI SDKs, automation tools - research if applicable

Present the classification to the user:
```
Here's my research plan:

Tier 1 (full depth): Next.js 15, React 19
Tier 2 (focused): Vitest, Tailwind CSS 4
Tier 3 (if needed): Prisma, NextAuth
Tier 4 (AI tooling): Vercel AI SDK

Proceed with this plan?
```

### Step 3: Fetch Documentation

For each dependency, starting with Tier 1:

**With Context7:**
1. Use `resolve-library-id` to get the Context7 ID
2. Use `get-library-docs` with focused topic queries:
   - "project setup and configuration"
   - "key API patterns and conventions"
   - "breaking changes from previous version"
   - "recommended project structure"
3. Capture results with source attribution

**With web search (supplement or fallback):**
1. Spawn parallel web-researcher agents for:
   - Official documentation and migration guides
   - Version compatibility and known issues
   - Community best practices and gotchas
2. Check for `llms.txt` at the framework's documentation domain

**Token management:** Query specific topics, not entire library docs. Each Context7 query should target a focused aspect. See ./reference/context7-usage.md for query patterns.

### Step 4: Build Compatibility Matrix

Cross-reference version requirements across all researched dependencies:
- Which versions of each library are compatible with each other?
- Are there known conflicts between any dependencies?
- What are the minimum version requirements?

### Step 5: Draft Architecture Decisions

For each significant technology choice, draft a lightweight ADR:
- What was chosen and why
- What alternatives were considered
- What trade-offs were accepted

See ./templates/architecture-decision-template.md for the ADR format.

Present draft ADRs to the user for confirmation before persisting.

### Step 6: Persist to .docs/references/

Spawn a `docs-writer` agent via the Task tool for each output file:

**1. Framework Docs Snapshot:**
```
Task prompt:
  doc_type: "reference"
  topic: "<primary framework> Documentation Snapshot"
  tags: [<framework names>]
  references: [<source URLs>]
  content: |
    <compiled framework docs using body sections from ./templates/framework-research-template.md>
```

**2. Dependency Compatibility:**
```
Task prompt:
  doc_type: "reference"
  topic: "<primary framework> Dependency Compatibility"
  tags: [<framework names>, compatibility]
  content: |
    <compiled compatibility matrix using body sections from ./templates/framework-research-template.md>
```

**3. Architecture Decisions** (written directly, not via docs-writer — ADRs use a different format):
- Write `architecture-decisions.md` to `.docs/references/` using the ADR template at ./templates/architecture-decision-template.md

The `docs-writer` agent handles frontmatter, file naming, and directory creation for files 1 and 2. See ./templates/framework-research-template.md for the body section templates.

### Step 7: Suggest Project MCP Configuration (Optional)

If the researched stack would benefit from specific MCP servers, suggest a `.mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

Only suggest MCP servers that are directly relevant to the chosen stack. Don't suggest every possible server.

## Output Format

When complete, present:

```
FRAMEWORK RESEARCH COMPLETE
============================

Researched: [list of frameworks/libraries]
Sources: Context7 MCP + [N] web sources
Date: [YYYY-MM-DD]

Key Findings:
- [Most important finding per Tier 1 dependency]
- [Version compatibility summary]
- [Notable gotchas or breaking changes]

Files created:
- .docs/references/framework-docs-snapshot.md
- .docs/references/dependency-compatibility.md
- .docs/references/architecture-decisions.md

Suggested MCP config: [yes/no - .mcp.json]

Next steps:
- Review architecture decisions and confirm choices
- Run `/starting-projects` to create the project plan (if not already in progress)
- Or run `/planning-code` to plan implementation with these references
```

## Error Recovery

**Recoverable errors (fix and continue):**
- Context7 rate limited: Switch to web-only research for remaining queries
- Context7 library not found: Use web search for that specific library
- Web search returns stale results: Note staleness in output, flag for user review

**Blocking errors (stop and ask):**
- No research sources available (no Context7, no web search): Cannot proceed - ask user to configure at least one
- Framework doesn't exist or name is ambiguous: Ask user to clarify

**Prevention:**
- Always check Context7 availability before querying
- Use focused queries to stay within rate limits
- Note the date on all persisted documentation

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Recommending patterns without having fetched current docs
- Persisting documentation without source URLs
- Skipping the compatibility matrix for multi-dependency stacks
- Writing ADRs without presenting them for user confirmation
- Dumping entire library docs instead of focused topic queries
- Proceeding without checking Context7 availability first
- Making changes beyond the research scope (writing code, modifying configs)

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know Next.js 15 well from training" | Training data has a cutoff. Fetch current docs. |
| "Context7 is slow, I'll skip it" | Stale patterns are slower to debug. Wait for the query. |
| "One web search is enough" | One angle isn't research. Cross-reference sources. |
| "The user just wants to start coding" | Starting with wrong patterns wastes more time. Research first. |
| "I'll write the docs later" | Docs written later are docs forgotten. Persist now. |
| "This stack is too simple to need ADRs" | Simple decisions still benefit from recorded rationale. |
| "I don't need the compatibility matrix" | Version conflicts are the #1 cause of setup failures. Check compatibility. |

## The Bottom Line

**No code without current documentation.**

Detect tools. Tier your research. Fetch current docs. Cross-reference. Persist everything. Every framework. Every project. Every time.
