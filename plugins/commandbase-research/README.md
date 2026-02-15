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
| context7-researcher | Fetches framework/library docs via Context7 MCP, returns concise summaries — keeps large responses out of caller's context |
| web-researcher | Searches the web and fetches page content for current, sourced information |

## Installation

```shell
/plugin install commandbase-research
```
