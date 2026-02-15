# commandbase-vault

Vault BRDSPI workflow plus daily operations for Obsidian vault management — brainstorm, research, design, structure, plan, implement chain, plus reviewing, capturing, connecting, linting, and maintaining. Requires commandbase-core for docs agents.

## Dependencies

- commandbase-core (docs agents)

## Skills (13)

### Construction (BRDSPI)

Setup and reorganization workflow — run these in sequence when building or restructuring a vault.

| Skill | Description |
|-------|-------------|
| /brainstorming-vault | Explore direction and preferences for an Obsidian vault before building structure |
| /starting-vault | Initialize a vault or configure Claude Code access (filesystem or MCP) — revised with multi-vault support |
| /researching-vault | Research vault structure, conventions, link graphs, and content patterns |
| /designing-vault | Make organizational decisions: MOC strategy, tagging taxonomy, template patterns |
| /structuring-vault | Map folder layout, naming conventions, and note placement rules |
| /planning-vault | Create or iterate on vault implementation plans with thorough vault research |
| /implementing-vault | Execute vault implementation plans — revised to delegate linting to /linting-vault |
| /importing-vault | Convert .docs/ artifacts into vault notes — revised with scope boundary vs /capturing-vault |

### Operations (Daily Use)

Daily operations and maintenance — run these independently as needed.

| Skill | Description |
|-------|-------------|
| /reviewing-vault | Daily, weekly, or monthly vault reviews to surface patterns and track progress |
| /capturing-vault | Quick note creation from various sources — fleeting notes, web clips, meeting notes, inbox processing |
| /connecting-vault | Discover relationships between notes, maintain MOCs, find orphans, detect duplicates |
| /linting-vault | Vault health checks — broken links, frontmatter validation, orphans, heading structure |
| /maintaining-vault | Batch maintenance — tag normalization, frontmatter bulk updates, link rot, stale notes, cleanup |

### Companion Skills

OFM format knowledge (wikilink syntax, callout types, frontmatter constraints) is baked into our reference files rather than depending on external plugins. See `reference/ofm-validation-rules.md` in linting-vault and `reference/ofm-note-formats.md` in capturing-vault.

## Installation

```shell
/plugin install commandbase-vault
```
