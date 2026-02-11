# Vault Workflow

commandbase-vault provides the BRDSPI chain for Obsidian vault management — 8 skills with two extras for vault initialization and `.docs/` importing. It depends on commandbase-core for documentation agents.

## Skill chain

```mermaid
flowchart LR
    sv["/starting-vault"] -.->|"init"| bv["/brainstorming-vault"]
    bv -->|".docs/brainstorm/"| rv["/researching-vault"]
    rv -->|".docs/research/"| dv["/designing-vault"]
    dv -->|".docs/design/"| stv["/structuring-vault"]
    stv -->|".docs/structure/"| pv["/planning-vault"]
    pv -->|".docs/plans/"| iv["/implementing-vault"]
    iv -.->|"updates plan checkboxes"| pv
```

## Skills

| Skill | Phase | What it does |
|-------|-------|-------------|
| /starting-vault | Init | Initialize a new Obsidian vault or configure Claude Code to work with an existing one (MCP server, API key) |
| /brainstorming-vault | Brainstorm | Explore direction — folder hierarchy vs flat tags, MOC strategies, linking philosophies, plugin decisions |
| /researching-vault | Research | Research vault structure, conventions, link graphs, frontmatter patterns, orphan notes |
| /designing-vault | Design | Make organizational decisions — MOC strategy, tagging taxonomy, template patterns, frontmatter schema |
| /structuring-vault | Structure | Map folder layout, naming conventions, note placement rules, template locations, attachment organization |
| /planning-vault | Plan | Create phased implementation plans for vault changes with verification checklists |
| /implementing-vault | Implement | Execute plans — create notes, move notes, update wikilinks, apply frontmatter, run vault linting |
| /importing-vault | — | Convert `.docs/` artifacts into Obsidian vault notes with wikilinks, callouts, tags, and frontmatter |

## Extra skills

Two skills sit outside the main BRDSPI chain:

- **/starting-vault** runs before the chain begins. It discovers the vault path, configures the MCP server connection, sets up the API key, creates a vault-aware CLAUDE.md, and tests connectivity. You only need it once per vault.
- **/importing-vault** can run anytime. It takes research docs, plans, handoffs, or learnings from `.docs/` and converts them into vault-native format — adding wikilinks, callouts, and proper frontmatter.

## No staleness detection

Unlike the code domain, vault skills don't currently auto-check upstream artifacts for staleness. If you've made significant changes between phases, run `/auditing-docs` manually to refresh stale documents.
