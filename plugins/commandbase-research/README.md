# commandbase-research

Web and framework research with sourced documentation output. Requires commandbase-core for docs agents.

## Dependencies

- commandbase-core (docs agents)

## Skills

| Skill | Description |
|-------|-------------|
| /analyzing-research | Cross-reference multiple research documents to find patterns, contradictions, or emergent insights |
| /researching-frameworks | Research framework docs and library APIs before building — fetches current docs, gathers patterns |
| /researching-repo | Analyze external git repos for structure, patterns, conventions, and CLAUDE.md files |
| /researching-web | Research topics on the web for up-to-date information beyond training data |

## Agents

| Agent | Description |
|-------|-------------|
| web-researcher | Searches the web and fetches page content for current, sourced information |

> **Note:** Context7 MCP research uses `general-purpose` built-in agents (not a custom plugin agent) because plugin subagents cannot inherit MCP server connections. See `/researching-frameworks` SKILL.md for details.

## Installation

```shell
/plugin install commandbase-research
```
