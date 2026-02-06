---
git_commit: c03615e
last_updated: 2026-02-06
last_updated_by: N0mikon
topic: "Framework Research Skill Design"
tags: [research, skill-design, context7, mcp, project-scaffolding]
status: complete
references:
  - newskills/starting-projects/SKILL.md
  - newskills/researching-web/SKILL.md
---

# Framework Research Skill: Automatic Docs Gathering for New Projects

**Research Date**: 2026-02-06
**Research Angles**: Context7 MCP capabilities, AI-assisted scaffolding patterns, MCP documentation ecosystem, docs system integration

## Problem Statement

When starting a new project, AI assistants generate code based on stale training data. Frameworks iterate quickly (Next.js, React, Vue, Astro), and patterns from even 6 months ago may be deprecated. The current `/starting-projects` skill spawns generic web-researcher agents, but doesn't leverage specialized documentation tools like Context7 MCP or the broader MCP documentation ecosystem.

**The question**: What would a skill look like that automatically pulls down current, authoritative framework documentation before any code is written or recommended?

## Key Findings

### 1. Context7 MCP: The Core Documentation Engine

Context7 (by Upstash) is an open-source MCP server that fetches up-to-date, version-specific documentation and injects it into the LLM context window.

**How it works:**
1. Detects library/framework mentioned in prompt
2. Pulls latest documentation from official sources
3. Filters by topic using a proprietary ranking algorithm
4. Injects relevant docs directly into model context

**Two tools provided:**
- `resolve-library-id` - Converts library names to Context7 IDs (e.g., "next.js" -> `/vercel/next.js`)
- `get-library-docs` (aka `query-docs`) - Retrieves version-specific documentation

**Coverage:** 33,000+ libraries across JS/TS, Python, Go, Rust, Ruby, Java. Strongest for fast-moving frameworks: Next.js, React, Vue, Astro, Svelte, Tailwind, Prisma, Supabase.

**Setup for Claude Code:**
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

**Limitations:**
- Rate limiting without API key (free key available at context7.com/dashboard)
- Windows timeout issues (may need `cmd /c` wrapper)
- Community-contributed docs can't be guaranteed for accuracy
- Backend/parsing is proprietary; only MCP server is open source

**Sources:**
- https://github.com/upstash/context7
- https://context7.com/docs/overview
- https://context7.com/docs/clients/claude-code
- https://upstash.com/blog/context7-mcp

### 2. Beyond Context7: The MCP Documentation Ecosystem

Several other MCP servers provide documentation access:

| Server | Scope | Key Feature |
|--------|-------|-------------|
| **Grounded Docs MCP** (arabold) | Any library, local files, PDFs | Private/local operation, no proprietary APIs |
| **Library Docs MCP** (vikramdse) | Langchain, Llama-Index, MCP, OpenAI | Real-time fetching via Serper API |
| **mcp-package-docs** (sammcj) | Go, Python, npm, Rust | Multi-ecosystem package docs |
| **Fetch MCP** (Anthropic official) | Any URL | Converts HTML to markdown |
| **Brave Search MCP** | Web search | Privacy-focused, broad coverage |
| **AWS Documentation MCP** | AWS services | 65+ servers for AWS ecosystem |

**Key insight:** No single MCP server covers everything. The skill should leverage Context7 for framework docs + web search for broader patterns/best practices + Brave/Fetch for specific URLs.

**Sources:**
- https://github.com/arabold/docs-mcp-server
- https://github.com/sammcj/mcp-package-docs
- https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
- https://awslabs.github.io/mcp/

### 3. The llms.txt Standard

A new standard (`/llms.txt`) provides LLM-optimized documentation summaries at well-known URLs. Adopted by Anthropic, Vercel, Hugging Face, and others. Context7 leverages this standard.

**Relevance to skill:** When researching a framework, check if `<domain>/llms.txt` exists as a high-quality, pre-processed documentation source.

**Sources:**
- https://llmstxt.org/
- https://www.mintlify.com/blog/simplifying-docs-with-llms-txt

### 4. What a Skill Should Pull Down

Based on the research, here's what developers need when starting a project:

**Tier 1 - Critical (always fetch):**
- Current API documentation for chosen framework (Context7)
- Project structure conventions (Context7 + web search)
- Breaking changes / migration guides from recent versions (web search)
- Official starter templates and recommended patterns (Context7)

**Tier 2 - Important (fetch for major dependencies):**
- Testing framework setup for the stack (Context7 for each dep)
- Build tool / bundler configuration (Vite, webpack, etc.)
- TypeScript/type system configuration patterns
- CSS framework integration (Tailwind, etc.)

**Tier 3 - Optional (fetch on request or for complex projects):**
- Database/ORM setup patterns (Prisma, Drizzle, etc.)
- Auth library integration (NextAuth, Clerk, etc.)
- Deployment patterns for target platform (Vercel, AWS, Docker)
- CI/CD configuration for chosen providers

**Tier 4 - AI-Specific Tooling:**
- MCP server documentation for tools the project will use
- n8n/automation workflow patterns if applicable
- AI SDK integration patterns (Vercel AI SDK, LangChain, etc.)

### 5. Docs System Integration

Research artifacts should persist in the `.docs/` directory:

**Proposed output structure:**
```
.docs/
├── research/
│   └── MM-DD-YYYY-framework-research.md    # Full research document
├── plans/
│   └── project-setup.md                     # Enhanced with research refs
└── references/
    ├── framework-docs-snapshot.md           # Key API patterns captured
    ├── dependency-compatibility.md          # Version compatibility matrix
    └── architecture-decisions.md            # ADR-style decisions made
```

**Key pattern from research:** ADRs (Architecture Decision Records) should capture *why* a technology was chosen, not just what was chosen. This prevents future sessions from re-debating settled decisions.

**Sources:**
- https://github.com/joelparkerhenderson/architecture-decision-record
- https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html

### 6. Existing Patterns to Build On

**VS Code #new + Context7:** VS Code 1.103+ uses Context7 for project scaffolding via `#new`. Makes multiple Context7 calls, ensures accurate dependency versions and framework standards.

**RPI Workflow:** The Research -> Plan -> Implement pattern (used by our own skills) naturally fits. Phase 1 becomes "research with Context7 + web", Phase 2 becomes "plan with researched docs", Phase 3 becomes "implement with verified patterns."

**Addy Osmani's spec.md pattern:** Research -> spec.md -> plan -> implement. The skill could generate a `spec.md`-like artifact that captures all research findings.

**Sources:**
- https://github.com/microsoft/vscode/issues/258369
- https://addyosmani.com/blog/ai-coding-workflow/
- https://github.com/brilliantconsultingdev/claude-research-plan-implement

### 7. Context Window Considerations

**Critical constraint:** Don't enable all MCPs at once. Context window can shrink from 200K to 70K with too many tools. Keep under 10 MCPs with under 80 tools active.

**Claude Code's tool search:** Auto-enabled when MCP tool descriptions consume >10% of context. Tools are deferred and loaded on demand.

**Implication for skill:** The skill should use `resolve-library-id` + `get-library-docs` with focused queries rather than dumping all docs into context. Pull specific topics, not entire library docs.

**Sources:**
- https://scottspence.com/posts/configuring-mcp-tools-in-claude-code
- https://code.claude.com/docs/en/mcp

## Skill Design Considerations

### Option A: Enhance `/starting-projects`

Add a Context7 research phase between discovery and web research:
- After discovering tech stack, use Context7 to pull framework docs
- Supplement with web search for patterns not covered
- Output enhanced `.docs/references/` directory

**Pros:** Single entry point, natural flow
**Cons:** Makes an already complex skill more complex; Context7 research is useful beyond project initialization

### Option B: New standalone skill (`/researching-frameworks`)

Dedicated skill focused purely on framework documentation gathering:
- Input: List of frameworks/libraries + project context
- Process: Context7 queries + web research + synthesis
- Output: `.docs/references/` with framework snapshots, compatibility matrix, ADRs
- Called by `/starting-projects` or independently

**Pros:** Composable, reusable, focused responsibility
**Cons:** Another skill to maintain; needs coordination with `/starting-projects`

### Option C: Enhance `/researching-web` with Context7 awareness

Add Context7 as a first-class research source alongside web search:
- When topic involves a known library/framework, auto-query Context7
- Fall back to web search for broader topics
- Same `.docs/research/` output pattern

**Pros:** Minimal new surface area, leverages existing skill
**Cons:** Conflates two different research modes; `/researching-web` is already well-scoped

### Recommendation: Option B with `/starting-projects` integration

A new `/researching-frameworks` skill that:
1. Is callable standalone or by `/starting-projects`
2. Uses Context7 MCP as primary source for framework-specific docs
3. Uses web search for ecosystem patterns, best practices, gotchas
4. Outputs structured `.docs/references/` artifacts
5. Produces a dependency compatibility matrix
6. Records technology decisions as lightweight ADRs

`/starting-projects` would call it during Phase 2 instead of spawning raw web-researcher agents.

## What the Skill Would Produce

### For each major dependency:
1. **Current API patterns** - Key APIs, hooks, components from Context7
2. **Version-specific gotchas** - Breaking changes, deprecations from web search
3. **Integration patterns** - How it works with other chosen dependencies
4. **Recommended configuration** - tsconfig, vite.config, etc. from official docs

### For the project overall:
1. **Dependency compatibility matrix** - Version ranges that work together
2. **Architecture decisions** - ADR-format records of technology choices
3. **Framework documentation snapshot** - Key patterns captured for offline reference
4. **Setup verification commands** - Commands to validate the setup works

## MCP Prerequisites

The skill would need these MCP servers available:

**Required:**
- Context7 MCP (`@upstash/context7-mcp`) - Framework documentation

**Strongly recommended:**
- Brave Search MCP or web search capability - Broader research

**Optional enhancements:**
- Fetch MCP (Anthropic) - For fetching specific URLs/llms.txt files
- Package docs MCP (sammcj) - For multi-language package docs

## Open Questions

1. **Should the skill check for Context7 availability** and fall back to web-only if not configured?
2. **How much documentation to persist** vs. re-fetching each session?
3. **Should ADRs be auto-generated** or presented as suggestions for user to confirm?
4. **Token budget per framework** - How many tokens of docs to pull per dependency?
5. **Should it produce a `.mcp.json`** for the new project suggesting MCP servers for the chosen stack?

## Sources

### Context7 & Documentation Tools
- https://github.com/upstash/context7
- https://context7.com/docs/overview
- https://context7.com/docs/clients/claude-code
- https://upstash.com/blog/context7-mcp
- https://www.trevorlasn.com/blog/context7-mcp
- https://apidog.com/blog/context7-mcp-server/
- https://claudelog.com/claude-code-mcps/context7-mcp/

### MCP Ecosystem
- https://github.com/arabold/docs-mcp-server
- https://github.com/sammcj/mcp-package-docs
- https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
- https://awslabs.github.io/mcp/
- https://code.claude.com/docs/en/mcp
- https://mcpservers.org/
- https://mcp-awesome.com/

### llms.txt Standard
- https://llmstxt.org/
- https://www.mintlify.com/blog/simplifying-docs-with-llms-txt

### Project Scaffolding & Workflows
- https://github.com/microsoft/vscode/issues/258369
- https://addyosmani.com/blog/ai-coding-workflow/
- https://github.com/brilliantconsultingdev/claude-research-plan-implement
- https://github.com/tony/claude-code-riper-5
- https://github.com/hmohamed01/Claude-Code-Scaffolding-Skill

### Documentation Patterns
- https://github.com/joelparkerhenderson/architecture-decision-record
- https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
- https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design
- https://www.builder.io/blog/claude-md-guide
- https://www.humanlayer.dev/blog/writing-a-good-claude-md

### AI Coding Best Practices
- https://code.claude.com/docs/en/best-practices
- https://thomaslandgraf.substack.com/p/context-engineering-for-claude-code
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://scottspence.com/posts/configuring-mcp-tools-in-claude-code
- https://www.deployhq.com/blog/context7-guide-stop-ai-hallucinations-with-live-docs
