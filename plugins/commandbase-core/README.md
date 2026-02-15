# commandbase-core

Shared documentation agents and standalone utility skills. Install this first — other commandbase plugins won't work without its agents (docs-writer, docs-updater, docs-locator, docs-analyzer).

## Dependencies

None. This is the base plugin.

## Skills

| Skill | Description |
|-------|-------------|
| /bookmarking-code | Save dev checkpoints, compare against previous states, detect regressions between phases |
| /debating-options | Research multiple options in parallel with synthesized recommendations |
| /starting-projects | Initialize new greenfield projects from scratch with guided discovery |
| /updating-claude-md | Update an existing CLAUDE.md file with new sections or project configuration |
| /validating-code | Verify implementation against a plan and check success criteria |

## Agents

| Agent | Description |
|-------|-------------|
| docs-analyzer | Extracts high-value insights from .docs/ documents without reading every file yourself |
| docs-locator | Finds relevant documents across the .docs/ directory (plans, research, handoffs) |
| docs-updater | Checks if a document is stale and updates it or archives it if no longer relevant |
| docs-writer | Creates and formats .docs/ output files with consistent frontmatter and structure |

## Shared References

| Reference | Description |
|-----------|-------------|
| reference/batch-safety-protocol.md | Reusable three-layer safety pattern (dry-run → checkpoint → chunked processing) for any skill that modifies >10 files |

These are design-time references — skills in other plugins can adapt these patterns into their own domain-specific reference files.

## Installation

```shell
/plugin install commandbase-core
```
