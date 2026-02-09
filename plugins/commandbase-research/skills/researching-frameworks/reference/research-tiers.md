# Research Tiers

Not every dependency needs the same depth of research. Classify each dependency by tier to allocate research effort proportionally.

## Tier Definitions

### Tier 1 - Critical (Always Research)

**What:** The primary framework and language runtime. The foundation everything else builds on.

**Examples:** Next.js, React, Vue, SvelteKit, Django, FastAPI, Express, Rails, Go stdlib

**Research depth:** Full - 4 Context7 queries + web search
- Current API documentation and key patterns
- Project structure conventions and file organization
- Breaking changes from previous major version
- Official starter templates and recommended patterns
- Routing, middleware, and core configuration

**Why full depth:** Mistakes in the foundation cascade through the entire project. Getting the primary framework wrong wastes the most time.

### Tier 2 - Important (Research Major Dependencies)

**What:** Testing frameworks, build tools, CSS frameworks, type system configuration. Libraries you'll interact with daily.

**Examples:** Vitest, Jest, Playwright, Vite, webpack, Tailwind CSS, TypeScript config, ESLint

**Research depth:** Focused - 2 Context7 queries + targeted web search
- Setup and configuration with the primary framework (Tier 1)
- Key API usage patterns and conventions

**Why focused:** These are important but their configuration is largely determined by Tier 1 choices. Research how they integrate, not everything about them.

### Tier 3 - Optional (Research on Request)

**What:** Database/ORM, auth libraries, deployment targets, CI/CD. Libraries that may or may not be part of the initial setup.

**Examples:** Prisma, Drizzle, NextAuth, Clerk, Auth0, Docker config, GitHub Actions, Vercel deployment

**Research depth:** Light - 1 Context7 query + web search only if user specifies
- Setup instructions specific to the primary framework
- Version compatibility with Tier 1/2 dependencies

**Why light:** These are often added later and have good standalone documentation. Research integration points, not the full library.

### Tier 4 - AI-Specific Tooling (Research if Applicable)

**What:** MCP servers, AI SDKs, automation tools. Only relevant if the project involves AI features or AI-assisted workflows.

**Examples:** Vercel AI SDK, LangChain, OpenAI SDK, n8n integration, MCP server setup

**Research depth:** Targeted - web search focused on integration with chosen stack
- SDK setup with the primary framework
- Available MCP servers for project dependencies
- Integration patterns and configuration

**Why targeted:** AI tooling is niche and often not covered by Context7. Web search and official docs are the primary sources.

## Classification Rules

1. **One primary framework = Tier 1.** If the project uses Next.js, that's Tier 1. React (underlying) is also Tier 1 if the project uses React-specific patterns beyond what Next.js provides.

2. **Daily-use libraries = Tier 2.** If you'll import it in most files or run it on every save, it's Tier 2.

3. **Feature-specific libraries = Tier 3.** If it powers one feature or system (auth, database, email), it's Tier 3 unless the user specifically needs it researched.

4. **AI/automation = Tier 4.** Only applies if the project involves AI features. Skip entirely for non-AI projects.

5. **User can override.** If the user says "I need deep research on Prisma", promote it to Tier 1 depth regardless of default classification.

## Token Budget by Tier

| Tier | Context7 Queries | Web Search Agents | Approximate Tokens |
|------|-----------------|-------------------|-------------------|
| 1    | Up to 4 per dep | 1-2 per dep       | ~20,000 per dep   |
| 2    | Up to 2 per dep | 1 per dep          | ~10,000 per dep   |
| 3    | Up to 1 per dep | 0-1 per dep        | ~5,000 per dep    |
| 4    | 0 (web only)    | 1 per dep          | ~5,000 per dep    |

**Typical project budget:** A Next.js + React + Tailwind + Vitest + Prisma stack would use:
- Tier 1: Next.js (20K) + React (20K) = 40K tokens
- Tier 2: Tailwind (10K) + Vitest (10K) = 20K tokens
- Tier 3: Prisma (5K) = 5K tokens
- **Total: ~65K tokens** of research context

## Presenting the Plan

Before researching, present the tier classification to the user:

```
Research plan for your stack:

Tier 1 (full depth):
- Next.js 15 - primary framework
- React 19 - core UI library

Tier 2 (focused):
- Vitest - testing framework
- Tailwind CSS 4 - styling

Tier 3 (if needed):
- Prisma - database ORM

Shall I proceed? Want to promote/demote any dependencies?
```

Wait for confirmation before spending tokens on research.
