---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter, updated file path from ~/.claude/agents/ to plugin location, corrected tools list, refreshed output format and integration points to match current agent definition"
references:
  - plugins/commandbase-research/agents/web-researcher.md
  - plugins/commandbase-research/skills/researching-web/SKILL.md
---

# Research: web-researcher Agent

## Overview

The `web-researcher` agent (`plugins/commandbase-research/agents/web-researcher.md`) searches the web and fetches page content to find current, sourced information. It is used when up-to-date information beyond training data is needed -- API docs, best practices, library comparisons, error solutions, or any question where recency matters.

**When to Use**: For API docs, best practices, library usage, technical solutions, comparisons, and any topic where current information is required.

## Capabilities

- Web search with WebSearch tool
- Fetch and analyze web page content with WebFetch tool

**Tools Available**: WebSearch, WebFetch

**Model**: sonnet

## Core Responsibilities

1. **Source Every Claim** -- Every finding must have a URL attribution
2. **Include Direct Quotes** -- Key findings backed by exact quotes from sources
3. **Assess Source Authority** -- Rank: official docs > recognized experts > community consensus > individual blogs
4. **Note Publication Dates** -- Flag time-sensitive information with dates
5. **Highlight Conflicts** -- When sources disagree, present both sides with attribution

## Invocation Pattern

Called from skills (primarily `/researching-web`) via Task tool:
```
subagent_type: "web-researcher"
prompt: "Research [topic] - focus on [specific aspect]. Include source URLs and publication dates."
```

The `/researching-web` skill decomposes questions into 2-4 search angles and spawns multiple `web-researcher` agents in parallel, each handling a different angle.

## Search Strategies

- **API/Library Documentation**: Official docs first, changelogs, code examples
- **Best Practices**: Recent articles, recognized experts, cross-referenced consensus, anti-patterns
- **Technical Solutions**: Specific error messages, Stack Overflow, GitHub issues
- **Comparisons**: "X vs Y" articles, benchmarks, migration guides, evaluation criteria

## Search Efficiency

- Start with 2-3 well-crafted searches before fetching content
- Fetch only the most promising 3-5 pages initially
- Use search operators: quotes for exact phrases, `-` for exclusions, `site:` for specific domains

## Output Format

```markdown
### Summary
[Brief overview of key findings]

### Detailed Findings

#### [Topic/Source 1]
**Source**: [Name](URL) (date, authority tier)
**Key Information**:
- Direct quote or finding
- Additional relevant details

#### [Topic/Source 2]
[Continue pattern...]

### Gaps
[Information that couldn't be found or needs further investigation]
```

## Integration Points

- Primary caller: `/researching-web` (spawns parallel web-researcher agents)
- Also used by: `/researching-frameworks` for framework evaluation
- Indirectly supports `/planning-code`, `/starting-projects`, and `/researching-code` when those skills need external context

## File Reference

- Agent: `plugins/commandbase-research/agents/web-researcher.md`
- Primary skill: `plugins/commandbase-research/skills/researching-web/SKILL.md`
- Search strategies reference: `plugins/commandbase-research/skills/researching-web/reference/search-strategies.md`
- Evidence requirements: `plugins/commandbase-research/skills/researching-web/reference/evidence-requirements.md`
