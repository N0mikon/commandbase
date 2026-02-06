---
name: researching-web
description: "Use this skill when researching topics on the web to find up-to-date information. This includes finding API documentation, comparing libraries or frameworks, researching best practices, troubleshooting errors with web sources, answering 'what is the current best way to do X', and gathering external context that goes beyond the codebase. Activate when the user says 'research this online', 'search the web for', 'find best practices', 'what do the docs say about', or needs information beyond training data."
---

# Researching Web

You are tasked with conducting comprehensive web research by spawning parallel web-researcher agents and synthesizing their findings into a documented, sourced answer.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Find, verify, and synthesize information from web sources:
- Search from multiple angles to ensure comprehensive coverage
- Cross-reference findings between sources
- Evaluate source quality, recency, and authority
- Present findings with full attribution
- Persist results so they survive beyond this conversation

## The Iron Law

```
NO SYNTHESIS WITHOUT PARALLEL WEB RESEARCH FIRST
```

If you haven't spawned web-researcher agents and waited for their results, you cannot synthesize findings.

**No exceptions:**
- Don't answer from training data - spawn agents to get current information
- Don't skip agents for "simple" questions - simple questions deserve verified answers
- Don't synthesize partial results - wait for ALL agents to complete
- Don't use a single search angle - decompose into multiple perspectives

## The Gate Function

```
BEFORE completing research:

1. IDENTIFY: What angles of the question need investigation?
2. DECOMPOSE: Break into 2-4 distinct search angles
3. SPAWN: Create parallel web-researcher agents (minimum 2)
4. WAIT: All agents must complete before proceeding
5. VERIFY: Did agents return sourced findings with URLs?
   - If NO: Spawn follow-up agents with refined queries
   - If YES: Proceed to synthesis
6. CROSS-REFERENCE: Compare findings across agents, flag conflicts
7. WRITE: Create .docs/research/MM-DD-YYYY-description.md (MANDATORY)
8. PRESENT: Summary to user with link to research file

Skipping steps = incomplete research
Research without a file = research that will be lost
```

## Initial Response

When this skill is invoked:

1. **If a specific question or topic was provided**, begin research immediately
2. **If no parameters provided**, respond with:
```
I'm ready to research the web. Please provide your question or topic, and I'll investigate it thoroughly using multiple search angles and verified sources.

Examples:
- "What are the best auth libraries for Next.js 15?"
- "How does Stripe handle webhook signature verification?"
- "Compare Bun vs Deno for production use in 2026"
- "Current best practices for React Server Components"
```

Then wait for the user's query.

## Research Process

### Step 1: Decompose the Research Question

Break the query into distinct search angles that cover different facets:

- **Official sources**: Documentation, specs, changelogs
- **Community consensus**: Stack Overflow, GitHub discussions, forums
- **Expert analysis**: Technical blogs, conference talks, comparison articles
- **Practical examples**: Tutorials, real-world implementations, case studies

Not every question needs all four. Choose 2-4 angles that fit the question.

### Step 2: Spawn Parallel web-researcher Agents

Create multiple Task agents with `subagent_type: "web-researcher"` to research different angles concurrently.

See ./reference/search-strategies.md for domain-specific search approaches and query crafting guidance.

**Each agent prompt should:**
- Specify the search angle clearly
- Include relevant search terms and operators
- Request source URLs and publication dates
- Ask for direct quotes from authoritative sources

**Example decomposition:**
```
Question: "What are the best auth libraries for Next.js 15?"

Agent 1: "Search for Next.js 15 official authentication documentation
          and recommended auth patterns. Focus on official Next.js docs
          and Vercel blog posts. Include version-specific details."

Agent 2: "Search for 'NextAuth vs Clerk vs Auth0 vs Lucia' comparisons
          published in 2025-2026. Find benchmark data, migration guides,
          and developer experience comparisons."

Agent 3: "Search for Next.js 15 authentication security best practices
          and common vulnerabilities. Look for OWASP guidance specific
          to React/Next.js server components and server actions."
```

### Step 3: Synthesize Findings

After ALL agents complete:
- Compile results from all agents
- Cross-reference findings: do sources agree or conflict?
- Evaluate source quality using the authority tiers in ./reference/evidence-requirements.md
- Note the recency of each source
- Identify gaps where information is missing or uncertain

### Step 4: Write Research Document

Write findings to `.docs/research/MM-DD-YYYY-description.md`
- Create `.docs/research/` directory if it doesn't exist

See ./templates/web-research-document-template.md for the full template and section guidelines.

### Step 5: Present Findings

- Present a concise summary to the user
- Include key source URLs for verification
- Note any conflicts or gaps in the findings
- Ask if they want deeper research on any aspect

## Important Guidelines

1. **Source Everything**
   - Every claim needs a URL
   - Include publication dates when available
   - Note when sources are older than 6 months
   - Distinguish official docs from community content

2. **Be Thorough**
   - Use parallel agents to cover multiple angles
   - Cross-reference findings between agents
   - Don't stop at the first answer found

3. **Be Honest About Uncertainty**
   - Flag when sources conflict
   - Note when information may be outdated
   - Distinguish consensus from minority opinions
   - Say "no authoritative source found" when that's the case

4. **Stay Focused**
   - Answer the specific question asked
   - Don't pad with tangentially related information
   - Depth over breadth on the actual question

## Evidence Requirements

See ./reference/evidence-requirements.md for:
- Source authority tiers
- What counts as valid web evidence
- Red flags that indicate insufficient research
- Verification checklist

## Example Interaction

```
User: /researching-web What are the best testing frameworks for Bun in 2026?
Assistant: I'll research testing frameworks for Bun...

[Decomposes into search angles]
[Spawns 3 web-researcher agents in parallel]
  - Agent 1: Bun official docs on built-in test runner
  - Agent 2: "Bun testing framework comparison 2026" community articles
  - Agent 3: Bun + Jest/Vitest compatibility and migration guides

[All agents return]

Based on my research, here's what I found:

**Summary:**
Bun ships with a built-in test runner (`bun test`) that covers most use cases...

**Key findings:**
- Built-in runner documented at bun.sh/docs/cli/test (Agent 1)
- Community consensus favors built-in for unit tests (Agent 2)
- Vitest compatibility layer available for migration (Agent 3)

**Conflicts:**
- Some 2025 articles recommend Vitest, but Bun 1.2+ made built-in runner competitive

I've documented the full details in `.docs/research/02-05-2026-bun-testing-frameworks.md`

Would you like me to dig deeper into any specific framework?
```

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting findings without creating a research file first
- Saying "I'll document this later" or "if you want I can save this"
- Completing research without a `.docs/research/` file path in your response
- Skipping the research file because "it was a simple question"
- Synthesizing without spawning parallel agents first
- Answering from training data without spawning any agents
- Using only one search angle when the question has multiple facets

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I already know this from training data" | Training data is stale. Spawn agents. Get current info. |
| "It was a quick answer, no file needed" | Every research produces a file. No exceptions. |
| "I'll create the file if they ask" | Create it first. They shouldn't have to ask. |
| "One agent was enough" | One angle isn't research. Decompose and parallelize. |
| "I already presented the findings" | File comes BEFORE presentation, not after. |
| "There wasn't much to document" | Short findings = short file. Still required. |
| "The user just wants a quick answer" | Quick answers without sources are unreliable. Research properly. |

## The Bottom Line

**No shortcuts for web research.**

Decompose the question. Spawn parallel agents. Wait for all results. Cross-reference sources. Write the research file. THEN present findings.

This is non-negotiable. Every question. Every time.