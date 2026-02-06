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

**Input:** Library ID + topic query
**Output:** Relevant documentation snippets with source attribution

**Usage notes:**
- Use focused topic queries, not broad requests
- Each query should target a specific aspect of the library

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

Context7 defaults to ~5000 tokens per query response. To stay within budget:

- **Tier 1 dependencies:** Up to 4 queries each (setup, API, breaking changes, structure)
- **Tier 2 dependencies:** Up to 2 queries each (setup, key APIs)
- **Tier 3 dependencies:** 1 query each (setup with primary framework)

This keeps total Context7 token usage under ~40,000 tokens for a typical 5-8 dependency stack.

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
