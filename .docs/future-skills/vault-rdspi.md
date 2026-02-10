---
git_commit: 8e92bba
last_updated: 2026-02-09
last_updated_by: docs-updater
last_updated_note: "Added frontmatter; corrected skill locations from newskills/ to plugins/commandbase-vault/; updated old verb-noun naming examples to verb-domain; fixed archived plan reference"
references:
  - plugins/commandbase-vault/skills/starting-vault/SKILL.md
  - plugins/commandbase-vault/skills/researching-vault/SKILL.md
  - plugins/commandbase-vault/skills/designing-vault/SKILL.md
  - plugins/commandbase-vault/skills/structuring-vault/SKILL.md
  - plugins/commandbase-vault/skills/planning-vault/SKILL.md
  - plugins/commandbase-vault/skills/implementing-vault/SKILL.md
  - plugins/commandbase-vault/skills/importing-vault/SKILL.md
  - plugins/commandbase-vault/skills/brainstorming-vault/SKILL.md
---

# Obsidian Vault RDSPI Workflow

> **Status: IMPLEMENTED** -- Deployed in Phase 6 (2026-02-08). All 8 vault BRDSPI skills (including `/brainstorming-vault`) live at `plugins/commandbase-vault/skills/`: `/starting-vault`, `/researching-vault`, `/designing-vault`, `/structuring-vault`, `/planning-vault`, `/implementing-vault`, `/importing-vault`, `/brainstorming-vault`. Naming evolved from `verb-noun` (`/vault-research`) to `verb-domain` (`/researching-vault`) to match the code domain convention. See `.docs/archive/02-07-2026-phase-6-vault-brdspi-implementation.md` for full details.

## Problem

Knowledge management in Obsidian vaults has the same needs as code — understanding what exists, designing improvements, planning changes, and executing them — with none of the tooling. Reorganizing a vault, building a new topic area, or connecting scattered notes is done ad-hoc.

## Concept

Full RDSPI for vault operations, with `/brainstorming-vault` as the pre-step:

```
/brainstorming-vault         <- "should I reorganize by project or by topic?"
  R  /researching-vault      <- explore structure, tags, orphans, link graphs, conventions
  D  /designing-vault        <- MOC strategy, tagging taxonomy, template designs
  S  /structuring-vault      <- folder layout, naming conventions, which notes move where
  P  /planning-vault         <- ordered tasks with success criteria
  I  /implementing-vault     <- create/move notes, update links, apply frontmatter
```

## Vault-Specific Considerations

- **Link integrity after moves** — parse `[[wikilinks]]` and `[markdown](links)` to update references
- **Plugin awareness** — Dataview queries, Templater syntax, canvas files
- **Frontmatter schemas** vary per user — research phase must map existing conventions
- Obsidian's file-based structure maps naturally to Claude Code's file tools

## Research-to-Vault Bridge (`/importing-vault`)

Code research skills (`/researching-web`, `/researching-code`, `/researching-frameworks`, `/researching-repo`) produce `.docs/research/` artifacts in a flat markdown format designed for Claude Code consumption. These are useful during development but they're throwaway — they live in a project's `.docs/` and don't feed into long-term knowledge.

The `/importing-vault` skill converts research artifacts into Obsidian-native notes:

- **Frontmatter translation** — `.docs/` frontmatter → vault's frontmatter schema (dates, tags, status, source fields)
- **Wikilinks** — convert markdown links to `[[wikilinks]]` where targets exist in the vault, keep external URLs as-is
- **Tags** — convert topic metadata to `#tags` matching vault taxonomy
- **Callouts** — surface key findings, conflicts, and open questions as Obsidian callout blocks (`> [!warning]`, `> [!info]`)
- **Dataview fields** — add inline fields if the vault uses Dataview for queries
- **Placement** — file into the right vault folder based on topic, link to relevant MOCs

### How It Fits RDSPI

Two integration points:

1. **Standalone use** — after any `/researching-*` run, invoke `/importing-vault` to capture findings in the vault before they're forgotten. Research doesn't have to be part of a vault RDSPI cycle to be worth keeping.

2. **Vault RDSPI research phase** — `/researching-vault` can pull from existing `.docs/research/` artifacts as input, converting and incorporating them rather than starting from scratch. If you already researched a topic for code, don't research it again for the vault.

```
/researching-web "auth patterns"     <- produces .docs/research/ artifact
/importing-vault                     <- converts to Obsidian note in vault
```

or within vault RDSPI:

```
  R  /researching-vault              <- finds existing .docs/research/ artifacts, imports + extends
```

### Open Questions for importing-vault

- Should it import a single file or batch-import all `.docs/research/` artifacts?
- How to handle vault taxonomy discovery — does it read existing tags/folders first or ask?
- Should it also handle `.docs/plans/` and `.docs/handoffs/`, not just research?
- Does the user review the converted note before it lands in the vault, or is it automatic?

## Markdown Linting for Vault Output

All vault skills produce or modify markdown files. A linter (skill or script) could validate output before it lands in the vault:

- **Broken wikilinks** — `[[targets]]` that don't resolve to existing notes
- **Frontmatter validation** — required fields present, dates formatted correctly, tags exist in taxonomy
- **Heading structure** — consistent hierarchy, no skipped levels
- **Obsidian compatibility** — no syntax that renders in standard markdown but breaks in Obsidian (or vice versa)
- **Dataview field consistency** — inline fields match expected types and naming conventions
- **Orphan detection** — new notes that aren't linked from anywhere

Could be a standalone `/vault-lint` skill, a validation step baked into `/implementing-vault`, or a hook that runs after any vault skill writes files. Lightest option: a script that `/implementing-vault` calls as a post-step.

## Open Questions (All Resolved)

- ~~How to locate the vault? Env var, config in CLAUDE.md, or ask on first use?~~ **Resolved: `/starting-vault` sets up CLAUDE.md with vault path configuration during setup flow**
- ~~Could a single `/vault` skill with subcommands work better than separate skills per phase?~~ **Resolved: separate skills per phase (matches code domain pattern, proven BRDSPI architecture)**
- ~~How heavy does Design need to be for vaults vs code? Vault "architecture" is simpler~~ **Resolved: `/designing-vault` uses opus model (like `/designing-code`), adapted for vault-specific decisions (MOC strategy, tagging taxonomy, template designs)**
- ~~Should vault skills be aware of community plugins (Dataview, Templater) and their syntax?~~ **Resolved: plugin awareness built into skills, especially `/researching-vault` and `/implementing-vault`**
- ~~Vault linting — standalone skill, built into `/implementing-vault`, or post-write hook?~~ **Resolved: built into `/implementing-vault` as MCP-based validation (verify link targets exist via read operations)**
