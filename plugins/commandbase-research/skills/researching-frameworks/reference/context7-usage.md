# Context7 MCP Usage

How to detect, use, and fall back from Context7 MCP in this skill.

## Detection

Before any Context7 query, check availability:

```
Use ToolSearch with query: "resolve-library-id"
```

**If found:** Context7 is available. Proceed with Context7 as primary source.
**If not found:** Context7 is not configured. Fall back to web-only research.

Do NOT assume Context7 is available. Do NOT skip detection.

## Available Tools

Context7 provides two tools:

### resolve-library-id

Converts a library name to a Context7-compatible identifier.

**Input:** A general library name (e.g., "next.js", "react", "tailwind css")
**Output:** A Context7 library ID (e.g., `/vercel/next.js`, `/facebook/react`)

**Usage notes:**
- Always resolve the ID first - don't guess the ID format
- The resolver handles fuzzy matching ("nextjs", "next.js", "Next.js" all work)
- If resolution fails, the library may not be in Context7's index - fall back to web search

### get-library-docs (also called query-docs)

Fetches version-specific documentation for a resolved library.

**Parameters:**
- `context7CompatibleLibraryID` (required) — the resolved library ID
- `topic` (optional) — focus documentation on a specific area (e.g., "routing", "hooks")
- `tokens` (optional) — controls response size. **Default: 10,000 tokens.** Values below the server's `DEFAULT_MINIMUM_TOKENS` floor are automatically raised. **Always set this explicitly** to avoid bloated responses.

**Output:** Relevant documentation snippets with source attribution

**Usage notes:**
- Use focused topic queries, not broad requests
- Each query should target a specific aspect of the library
- **Always pass `tokens` explicitly** — omitting it returns the 10,000-token default, which fills context fast

## Query Patterns

### Good queries (focused, specific):

For a primary framework (Tier 1):
1. "project setup and initial configuration"
2. "key API patterns, hooks, and conventions"
3. "breaking changes and migration from previous version"
4. "recommended project structure and file organization"
5. "routing configuration and patterns"

For a supporting library (Tier 2):
1. "setup and configuration with [primary framework]"
2. "key API usage patterns"

For version-specific research:
1. "what changed in version [X] from version [Y]"
2. "new features in the latest release"

### Bad queries (too broad, token-wasteful):

- "tell me everything about Next.js" - too broad, wastes context
- "documentation" - no topic focus
- "all APIs" - will return too much irrelevant content

## Token Management

Context7 defaults to **10,000 tokens per response** if you don't set the `tokens` parameter. A single uncontrolled query can consume ~14k tokens in the main context window. Two strategies prevent this:

### Strategy 1: Set `tokens` explicitly on every call

| Tier | Queries per dep | `tokens` value | Rationale |
|------|----------------|----------------|-----------|
| Tier 1 | Up to 3 | 10000 | Primary framework, needs depth |
| Tier 2 | Up to 2 | 5000 | Supporting library, focused queries |
| Tier 3 | 1 | 5000 | Setup integration only |

Example call:
```
get-library-docs(
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "app router setup and configuration",
  tokens: 5000
)
```

**Note:** The server enforces a minimum floor (default 10,000). If you request 5,000, the server may return up to 10,000 anyway. This is a server-side setting — if the user has configured `DEFAULT_MINIMUM_TOKENS` lower, smaller values will work.

### Strategy 2: Delegate to context7-researcher agent (preferred for multi-dep research)

Use the `context7-researcher` agent to absorb large MCP responses. The agent resolves library IDs, fetches docs with explicit token limits, and returns only concise summaries (max 500 words). The raw MCP output stays in the agent's context, not yours.

```
Task prompt (subagent_type: "commandbase-research:context7-researcher"):
  "Research [framework]: [specific topic]. Depth: full/focused/minimal."
```

Spawn multiple agents in parallel for independent libraries:
```
Agent 1: "Research next.js: app router setup and configuration. Depth: full."
Agent 2: "Research react: server components patterns and conventions. Depth: full."
Agent 3: "Research tailwind css: v4 configuration and migration. Depth: focused."
```

**When to use each strategy:**
- **Single dependency, quick lookup:** Strategy 1 (direct call, set tokens)
- **Multi-dependency stack (3+ deps):** Strategy 2 (context7-researcher agents protect main context)
- **Called by /starting-projects:** Always Strategy 2 (research is a long pipeline, context preservation is critical)
- **Context7 unavailable:** Skip both, use `web-researcher` agents as fallback

### Token budget for a typical stack

With Strategy 2, the main context sees only distilled summaries (~500 words each):
- 3 Tier 1 deps × 500 words = ~1,500 words returned to main context
- 3 Tier 2 deps × 300 words = ~900 words returned to main context
- Total main context impact: ~2,400 words (~3,200 tokens) vs ~84,000 tokens unmanaged

## Fallback: Web-Only Research

When Context7 is unavailable, use these alternatives:

1. **Web search agents** for current documentation:
   - "[framework] official documentation [version]"
   - "[framework] getting started guide [year]"
   - "[framework] breaking changes [version]"

2. **WebFetch** for specific documentation URLs:
   - Check `https://[framework-domain]/llms.txt` for LLM-optimized docs
   - Fetch official getting-started pages directly
   - Fetch changelog/release notes pages

3. **Package registry queries** via web search:
   - npm: "site:npmjs.com [package name]" for latest version info
   - PyPI: "site:pypi.org [package name]" for Python packages

## Known Issues

### Rate Limiting
Context7 may rate-limit without an API key. If you get rate limited:
- Switch to web-only for remaining queries
- Note in output that some docs came from web search instead of Context7
- Suggest the user get a free API key from context7.com/dashboard

### Windows Compatibility
On Windows/MINGW, Context7 may experience timeouts. The standard `npx` invocation usually works with Claude Code's MCP system, but if issues arise, the `cmd /c` wrapper may be needed:
```bash
claude mcp add context7 -- cmd /c npx -y @upstash/context7-mcp@latest
```

### Library Not Found
If `resolve-library-id` returns no results:
- The library may not be indexed in Context7
- Fall back to web search for that specific library
- Note in output: "Documentation for [library] fetched via web search (not in Context7 index)"
