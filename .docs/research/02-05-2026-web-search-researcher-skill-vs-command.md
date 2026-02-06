# Should web-researcher Become a Skill or Get a Slash Command?

```yaml
git_commit: 46b48db
last_updated: 02-05-2026
topic: Architecture decision for web-researcher - keep as agent, convert to skill, or hybrid
tags: [agents, skills, architecture, web-search, decision]
status: complete
references:
  - ~/.claude/agents/web-researcher.md
  - ~/.claude/skills/creating-skills/SKILL.md
  - ~/.claude/skills/creating-skills/reference/converting-subagents.md
  - ~/.claude/skills/researching-code/SKILL.md
  - ~/.claude/skills/starting-projects/SKILL.md
  - .docs/research/02-05-2026-web-researcher-vs-researching-code.md
```

## Research Question

Should the web-researcher agent be converted into a skill, have a slash command wrapper added, or take a hybrid approach? What are the pros/cons of each?

## Summary

There are three viable options, but the hybrid approach (Option C) is the strongest fit. It mirrors the proven `/researching-code` architecture — an orchestrator skill that spawns worker agents — while preserving web-researcher's role as a reusable worker. A critical discovery: **slash commands have been merged into skills** as of Claude Code 2.1.3, so "add a slash command" and "create a skill" are now the same thing.

## Key Discovery: Slash Commands = Skills Now

As of Claude Code 2.1.3, slash commands have been consolidated into the skills system. Both use `/` prefix invocation, both can auto-trigger from descriptions, and both follow the SKILL.md format. This means **the question reduces to: convert the agent to a skill, or create a new orchestrator skill alongside the agent.**

Source: Multiple 2026 community articles confirm this merge.

## The Three Options

### Option A: Convert web-researcher Agent → Skill

Replace the agent file entirely with a skill directory.

**What changes:**
- `~/.claude/agents/web-researcher.md` → `~/.claude/skills/researching-web/SKILL.md`
- Name transforms: `web-researcher` → `researching-web` (gerund form per convention)
- Description transforms from WHAT to WHEN
- Gains progressive disclosure, reference files, templates, enforcement patterns

**Pros:**
- Auto-invocation: triggers when user asks "research X online", "find best practices for Y"
- Progressive disclosure: search strategies move to `reference/search-strategies.md`, output template to `templates/`
- Can add enforcement patterns (Iron Law, rationalization prevention)
- Can mandate persistent artifacts (`.docs/research/` files)
- Single component to maintain

**Cons:**
- **Breaks the worker pattern**: `/starting-projects` currently spawns `web-researcher` as a worker agent via Task tool. Skills run in main context — they can't be spawned as subagents the same way.
- **Context cost**: Skills load metadata into every conversation (~100 tokens). As an agent, it costs nothing until spawned.
- **Overweight for worker tasks**: When another skill just needs "go search for X", a full skill with enforcement gates is overkill.
- **Loses model routing**: Agent specifies `model: sonnet` for cost efficiency. Skills run in main context on whatever model is active.

**Verdict:** Breaks the composability that makes agents valuable as workers.

### Option B: Create a Thin Skill Wrapper (Skill Calls Agent)

Create a minimal skill that just spawns the existing agent with better prompting.

**What it looks like:**
```
~/.claude/skills/researching-web/SKILL.md  (thin wrapper, spawns agent)
~/.claude/agents/web-researcher.md  (unchanged worker)
```

**Pros:**
- Gets `/researching-web` invocation
- Agent stays available as a worker for other skills
- Minimal maintenance overhead
- Auto-triggers on web research requests

**Cons:**
- Skill is just a pass-through — doesn't add much value over the agent alone
- No enforcement patterns (the skill just delegates immediately)
- No multi-agent orchestration (spawns one agent, waits, returns)
- Doesn't solve the methodology gap identified in earlier research
- "Thin wrapper" skills feel like unnecessary indirection

**Verdict:** Works but doesn't leverage what makes skills powerful.

### Option C: Create an Orchestrator Skill (Parallel to /researching-code)

Create `/researching-web` as a full orchestrator skill that decomposes web research questions and spawns multiple web-researcher agents in parallel — exactly mirroring how `/researching-code` orchestrates codebase-* agents.

**What it looks like:**
```
~/.claude/skills/researching-web/
├── SKILL.md                              # Orchestrator with Iron Law, Gate Function
├── reference/
│   ├── search-strategies.md              # Domain-specific search approaches
│   └── evidence-requirements.md          # Web source quality standards
└── templates/
    └── web-research-document-template.md # Output format for .docs/research/

~/.claude/agents/web-researcher.md  # Unchanged worker agent
```

**Pros:**
- **Mirrors proven architecture**: Same pattern as `/researching-code` → codebase-* agents
- **Multi-angle research**: Decomposes "how should I implement auth?" into parallel searches (official docs, community patterns, security best practices, comparison articles)
- **Preserves worker role**: Agent stays available for `/starting-projects` and any future skill that needs web search
- **Enforcement patterns**: Iron Law ("NO SYNTHESIS WITHOUT PARALLEL WEB RESEARCH"), mandatory `.docs/research/` artifacts
- **Evidence standards**: Web-specific quality rules (source recency, authority, cross-referencing)
- **Progressive disclosure**: Search strategies and templates load only when needed
- **Composable with /researching-code**: Could eventually have `/researching-code` spawn `/researching-web` agents when questions need both local and external context

**Cons:**
- More files to maintain (skill + agent)
- Heavier process for simple "just Google this" requests
- Need to define when orchestration adds value vs. when a single agent search suffices

**Verdict:** Best fit. Leverages everything we've learned about skill architecture.

## Architecture Comparison

| Dimension | Option A (Convert) | Option B (Thin Wrapper) | Option C (Orchestrator) |
|-----------|-------------------|------------------------|------------------------|
| Invocation | `/researching-web` | `/researching-web` | `/researching-web` |
| Worker reuse | Broken | Preserved | Preserved |
| Enforcement | Full | None | Full |
| Parallel research | No (single skill) | No (single agent) | Yes (multiple agents) |
| Artifacts | Yes | No | Yes |
| Context cost | Higher (main context) | Low | Medium (orchestrator in main, workers in subagent) |
| Mirrors existing patterns | No | Partially | Yes (mirrors /researching-code) |
| Maintenance | 1 component | 2 components | 2 components |

## How Option C Would Work

### The Pattern

```
User: /researching-web "What are the best auth libraries for Next.js 15?"

Skill activates → Decomposes into search angles:
  1. Spawn web-researcher: "Next.js 15 official authentication documentation"
  2. Spawn web-researcher: "NextAuth vs Clerk vs Auth0 comparison 2026"
  3. Spawn web-researcher: "Next.js 15 auth security best practices"

All agents return → Skill synthesizes:
  - Cross-references findings
  - Flags conflicts between sources
  - Evaluates source quality/recency
  - Writes .docs/research/02-05-2026-nextjs-auth-libraries.md
  - Presents summary with sources
```

### The Iron Law (for the skill)

```
NO SYNTHESIS WITHOUT PARALLEL WEB RESEARCH FIRST
```
- Minimum 2 web-researcher agents per question
- Don't answer from memory — spawn agents to verify
- Don't skip parallel angles for "simple" questions
- Don't synthesize partial results — wait for ALL agents

### What reference/search-strategies.md Would Contain

- Domain-specific search patterns (API docs, best practices, troubleshooting, comparisons)
- Search operator guidance (site:, quotes, date filtering)
- Source authority tiers (official docs > recognized experts > community > blog posts)
- When to use broad vs. targeted searches

### What the template would add

- Web-specific frontmatter (sources list, date_searched, query_decomposition)
- Source quality assessment section
- Conflict resolution section (when sources disagree)
- Currency assessment (how recent are the findings?)

## Open Questions

1. **Naming**: `researching-web` follows the gerund convention, but should it be `web-researching` or `researching-online`?
2. **Scope overlap**: When should `/researching-code` delegate to `/researching-web` vs. user invoking directly?
3. **Simple queries**: Should the skill have a "fast path" that skips full orchestration for single-angle questions?
4. **Integration**: Should `/researching-code` gain an option to also spawn web-researcher agents for mixed queries?

## Recommendation

**Go with Option C: Orchestrator Skill + Unchanged Agent.**

This is the natural evolution that:
- Applies the lessons from `/researching-code` to web research
- Preserves the agent as a composable worker
- Adds the enforcement patterns that the earlier comparison identified as missing
- Creates a symmetric architecture: `/researching-code` for internal, `/researching-web` for external
