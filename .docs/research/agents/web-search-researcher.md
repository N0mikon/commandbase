# Research: web-researcher Agent

## Overview

The `web-researcher` agent (`~/.claude/agents/web-researcher.md`) researches information from the web when you need modern, up-to-date information that may not be in training data.

**When to Use**: For API docs, best practices, library usage, and technical solutions that require current information.

## Capabilities

- Web search with WebSearch tool
- Fetch web pages with WebFetch tool
- Read files with Read tool
- Search code with Grep tool
- Find files with Glob tool
- List directories with LS tool

**Tools Available**: WebSearch, WebFetch, Read, Grep, Glob, LS

## Invocation Pattern

Called from skills via Task tool:
```
subagent_type: "web-researcher"
prompt: "Research [topic] - focus on [specific aspect]"
```

## Use Cases

1. **API Documentation**: Find current API docs
2. **Best Practices**: Research current recommendations
3. **Library Usage**: Find how to use specific libraries
4. **Technical Solutions**: Research solutions to problems

## Output Format

```markdown
## Research: [Topic]

### Summary
[High-level findings]

### Key Findings
1. [Finding 1] - Source: [link]
2. [Finding 2] - Source: [link]

### Recommendations
Based on research:
- [Recommendation 1]
- [Recommendation 2]

### Sources
- [Title 1](url)
- [Title 2](url)
```

## Integration Points

- Supports `/planning-code` for technology research
- Helps `/starting-projects` with best practices
- Assists `/researching-code` for external context

## File Reference

- Agent: `~/.claude/agents/web-researcher.md`
