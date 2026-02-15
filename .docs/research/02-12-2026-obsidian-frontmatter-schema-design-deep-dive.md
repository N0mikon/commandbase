---
date: 2026-02-12
status: complete
topic: "Obsidian Frontmatter Schema Design - Deep Dive"
tags: [research, obsidian, frontmatter, yaml, properties, dataview, schema-design, ai-workflows]
git_commit: 9c4c7f4
---

# Obsidian Frontmatter Schema Design — Deep Dive

## Research Question
What are the best practices for designing frontmatter schemas in Obsidian vaults, optimized for AI/Claude integration, Dataview/Bases queries, and long-term scalability?

## Summary
Frontmatter schema design in Obsidian operates under hard constraints from the Properties system (no nested YAML, global type registry, 6 property types) and soft constraints from the query ecosystem (Dataview's 8 types vs Bases' frontmatter-only requirement). The community consensus favors flat schemas with short descriptive field names, list-type defaults for multi-value fields, and a mandatory `type` property for note classification. For AI-native vaults, the most effective approach combines a well-documented CLAUDE.md schema definition, consistent kebab-case or snake_case naming, Templater-driven auto-population, and the Linter plugin for enforcement. Obsidian Bases is replacing Dataview as the primary query engine, which means frontmatter-only metadata (no inline fields) is the future-proof path.

## Detailed Findings

### 1. Obsidian Properties System — Hard Constraints

The Properties system (introduced v1.4, August 2023) defines the technical boundaries for all frontmatter design.

**Six supported property types:**
- **Text**: Default type, single string values
- **List**: Multiple text items (tags, aliases, cssclasses use this)
- **Number**: Integers and decimals only — no "list of numbers" type exists
- **Checkbox**: Boolean true/false
- **Date**: ISO 8601 format (YYYY-MM-DD), generates date picker
- **Date & Time**: Same as Date plus time component (12-hour display)

**Critical constraints:**
- **No nested YAML objects**: Nested structures display as "unknown" type with no editing UI. The Properties editor converts nested YAML to unreadable JSON strings like `book: {"started": "2023-09-01", "format": "Digital"}`. The feature request for nested support has 277+ upvotes with no official response.
- **Global type registry**: Once a property name is assigned a type in any file, ALL properties with that name across the entire vault must use the same type. Changing types doesn't auto-migrate existing values.
- **Automatic reformatting**: Properties UI strips YAML comments and reformats structure. Template comments are destroyed on insertion. This is by design for plugin compatibility and "unlikely to change."
- **No empty lines before frontmatter**: As of v1.4.10, empty lines before the opening `---` break parsing.
- **No multi-word tags**: `tag: master note` splits into two tags. Use underscores: `master_note`.
- **Wikilinks must be quoted**: `key: "[[Link]]"` — unquoted wikilinks break YAML parsing.
- **Links don't auto-update**: Renaming a referenced note does NOT update wikilinks in frontmatter.

**Deprecated forms (breaking as of v1.9):**
- `tag` → `tags` (must be list)
- `alias` → `aliases` (must be list)
- `cssclass` → `cssclasses` (must be list)
- Migration tool: Format Converter core plugin (added in v1.9.3)

**Sources:** [Properties - Obsidian Help](https://help.obsidian.md/properties), [Obsidian 1.4.5 Changelog](https://obsidian.md/changelog/2023-08-31-desktop-v1.4.5/), [Forum: Properties multi-level YAML (277 upvotes)](https://forum.obsidian.md/t/properties-bases-support-multi-level-yaml-mapping-of-mappings-nested-attributes/63826), [Forum: Reformatting complaint](https://forum.obsidian.md/t/make-new-properties-feature-not-re-format-frontmatter/66297), [Obsidian Rocks: Properties Introduction](https://obsidian.rocks/an-introduction-to-obsidian-properties/)

### 2. Dataview vs Bases — The Query Ecosystem Split

Schema design must account for both Dataview (current dominant) and Bases (official successor).

**Dataview (8 types, inline + frontmatter):**
- Text, Number, Boolean, Date, Duration, Link, List, Object
- Supports inline fields (`Key:: Value`) and YAML frontmatter equally — "no performance difference" between them
- Object type works via dot notation for nested YAML (e.g., `obj.key1`), but this conflicts with Properties UI
- Uses IndexedDB caching; scales to "hundreds of thousands of annotated notes without issue"
- `FROM` filters are faster than `WHERE` filters — schema design should enable folder-based queries
- Multi-value fields (lists) require `FLATTEN` before `GROUP BY`
- **No longer actively developed** — successor Datacore is in progress

**Obsidian Bases (frontmatter-only, GUI-driven):**
- Only queries Properties (YAML frontmatter) — inline fields are invisible
- "Results render nearly instantly, even in vaults with over 50,000 notes"
- Currently limited: table views only, no GROUP BY, no task aggregation
- Every note needs a `type` property as "primary identifier"
- List/Kanban views planned but not yet available

**Migration implications:**
- Inline fields (`Key:: Value`) must move to frontmatter for Bases compatibility
- Tools: QuickAdd macro, Dataview-to-Properties plugin, Templater scripts
- Nested YAML works for Dataview queries but breaks Properties UI and Bases queries

**Design recommendation:** Target frontmatter-only metadata with flat structure to ensure compatibility with both current Dataview and future Bases.

**Sources:** [Dataview Types Docs](https://blacksmithgu.github.io/obsidian-dataview/annotation/types-of-metadata/), [Dataview vs Datacore vs Bases](https://obsidian.rocks/dataview-vs-datacore-vs-obsidian-bases/), [The Architect's Guide to Obsidian Bases](https://chughkabir.com/guide-obsidian-bases/), [Bases Migration Guide](https://practicalpkm.com/moving-to-obsidian-bases-from-dataview/)

### 3. Schema Design Rules — Community Consensus

Synthesized from Steph Ango (Obsidian CEO), Eleanor Konik, Bryan Jenks, and vault template repositories.

**Core rules:**

1. **Mandatory `type` field**: Every note gets a type — `daily`, `weekly`, `person`, `project`, `moc`, `resource`, `meeting`, `book`, `article`. This is the primary classification axis and enables Bases queries.

2. **Flat structure only**: No nested objects. Use `series_name` and `series_num` instead of `series: {name: ..., num: ...}`. One user with 400+ book notes had to flatten their entire schema when nested YAML broke Properties.

3. **Default to list type**: If there's any chance a field will have multiple values, make it a list from the start. Changing a text field to a list field later requires manual migration of every note. Steph Ango: "Default to list type properties if there's any chance of multiple values."

4. **Short, descriptive names**: `author` not `book_author_name`. `due` not `due_date`. Efficiency matters for manual entry and AI parsing.

5. **Consistent casing**: Pick one and enforce it vault-wide. Options:
   - `snake_case`: `date_read`, `series_name` — Python-friendly, used by BBBBlog book schema
   - `kebab-case`: `last-contact`, `growth-edge` — CSS-friendly, used in some tag systems
   - `lowercase`: `author`, `status`, `rating` — simplest, used by Steph Ango
   - Avoid `camelCase` — not standard in the Obsidian community

6. **ISO dates always**: `YYYY-MM-DD` for dates, `YYYY-MM-DDTHH:mm` for datetimes. Non-ISO formats are treated as strings by both Dataview and Bases.

7. **Tags for themes, type field for classification**: A note belongs to one folder (physical) and has one type (frontmatter), but can have many tags. Use nested tag hierarchies: `#status/active`, `#topic/ai`, `#context/work`.

8. **Reserved property names**: `tags`, `aliases`, `cssclasses`, `title`, `description`, `created`, `updated`, `status`, `due`, `cover` all have special behavior in Obsidian. Use them intentionally.

**Sources:** [Steph Ango's Vault](https://stephango.com/vault), [BBBBlog: Nested YAML for Book Notes](https://bbbburns.com/blog/2025/07/nested-yaml-frontmatter-for-obsidian-book-notes/), [Bryan Jenks FAQ](https://github.com/BryanJenksCommunity/FAQ/discussions/189), [voidashi vault template](https://github.com/voidashi/obsidian-vault-template)

### 4. Real-World Schema Examples

**Universal base (all note types):**
```yaml
---
type: [note-type]
tags:
  - topic/domain
  - status/active
aliases: []
created: YYYY-MM-DD
---
```

**Daily note:**
```yaml
---
type: daily
tags:
  - periodic/daily
created: 2026-02-12
mood:
energy:
---
```

**Person/Contact:**
```yaml
---
type: person
tags:
  - people/coworker
aliases:
  - nickname
role:
org:
email:
last_contact: 2026-01-15
---
```

**Project:**
```yaml
---
type: project
tags:
  - status/active
  - area/work
status: active
due: 2026-03-15
area: "[[Area Name]]"
---
```

**Book/Resource:**
```yaml
---
type: book
tags:
  - media/book
author: []
status: reading
rating:
series_name:
series_num:
date_start:
date_end:
isbn:
---
```

**Meeting:**
```yaml
---
type: meeting
tags:
  - work/meeting
date: 2026-02-12
company:
attendees: []
summary: " "
---
```

**MOC (Map of Content):**
```yaml
---
type: moc
tags:
  - moc
  - topic/domain
---
```

**Sources:** [Steph Ango's Vault](https://stephango.com/vault), [Dann Berg Meeting Template](https://dannb.org/blog/2023/obsidian-meeting-note-template/), [Cassidy Williams Templater](https://cassidoo.co/post/obsidian-templater/), [BBBBlog Book Notes](https://bbbburns.com/blog/2025/07/nested-yaml-frontmatter-for-obsidian-book-notes/), [ThoughtAsylum Meeting Template](https://www.thoughtasylum.com/2023/02/26/my-obsidian-generic-meeting-template/)

### 5. AI-Native Schema Design

Frontmatter conventions specifically optimized for Claude/LLM interaction.

**CLAUDE.md as schema documentation:**
The single most important practice is documenting your entire frontmatter schema in CLAUDE.md. This gives Claude the vocabulary and rules for every note type. One user's CLAUDE.md grew from 3 lines to 370+ as they refined frontmatter conventions. Include:
- Complete list of property names, types, and allowed values
- Note type definitions with required vs optional fields
- Tag taxonomy rules (nesting, pluralization, max count)
- Forbidden patterns (no nested YAML, no inline Dataview fields)

**AI-friendly field naming:**
- Use descriptive names that Claude can understand without context: `author` not `au`, `last_contact` not `lc`
- Avoid reserved programming keywords that might confuse LLMs: `from`, `where`, `type` (though `type` is standard in Obsidian)
- Consistent casing helps Claude generate correct metadata without guessing

**Automated frontmatter generation plugins:**
- **Metadata Auto Classifier**: AI-powered tag and field suggestions based on note content. Uses GPT to understand context.
- **Auto Tag**: One-click AI tagging integrated into frontmatter. Creates tags if frontmatter doesn't exist.
- **Auto Front Matter**: Rule-based frontmatter generation with JSON/JS expressions on save.
- **Linter plugin**: 14 YAML rules for enforcement (dedup arrays, sort keys, format tags, auto-timestamps).

**MCP frontmatter tools:**
- `manage_frontmatter` (cyanheads/obsidian-mcp-server): Atomic get/set/delete on individual keys without rewriting entire files
- Batch operations via Frontmatter MCP: Update, add, remove, replace values across files matching glob patterns
- MegaMem plugin: Scans vault to infer frontmatter patterns and generates Pydantic schemas for AI consumption

**Schema evolution strategy:**
1. Test changes on a copy vault first
2. Use git version control before bulk migrations
3. Migrate gradually with QuickAdd macros or Templater scripts
4. Validate with Linter rules post-migration
5. Update CLAUDE.md schema documentation immediately after changes

**Sources:** [Teaching Claude Code My Obsidian Vault](https://mauriciogomes.com/teaching-claude-code-my-obsidian-vault), [AI-Native Vault Setup Guide](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide), [Metadata Auto Classifier](https://www.obsidianstats.com/plugins/metadata-auto-classifier), [cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server), [MegaMem Plugin](https://github.com/C-Bjorn/MegaMem)

### 6. Linter Plugin — Schema Enforcement

The Linter plugin provides 14 YAML-specific rules for maintaining schema consistency.

**Most relevant rules for schema enforcement:**
- **Insert YAML attributes**: Adds predefined fields to every note automatically
- **YAML Key Sort**: Enforces consistent property ordering (priority-based)
- **Format Tags in YAML**: Removes hashtags from frontmatter tags
- **Dedupe YAML Array Values**: Removes duplicate list entries
- **YAML Timestamp**: Auto-tracks `created` and `modified` dates
- **YAML Title**: Extracts title from heading or filename
- **Move Tags to YAML**: Consolidates inline body tags into frontmatter
- **Format YAML Array**: Enforces single-line or multi-line array format
- **Sort YAML Array Values**: Alphabetical ordering within arrays

**Limitation**: Rules use regex parsing, not a YAML library. Edge cases with complex values may misparsed.

**Sources:** [Linter YAML Rules](https://platers.github.io/obsidian-linter/settings/yaml-rules/), [GitHub - platers/obsidian-linter](https://github.com/platers/obsidian-linter)

### 7. Tag Taxonomy as Schema Extension

Tags function as a flexible metadata layer that complements frontmatter properties.

**Nested tag hierarchies (queryable with Dataview `#parent/*`):**
```
#type/daily, #type/meeting, #type/project, #type/moc
#status/active, #status/paused, #status/archived
#context/work, #context/personal, #context/academic
#topic/ai, #topic/programming, #topic/design
#people/team-a, #people/external
```

**Design rules:**
- Always pluralize tag categories
- Max 5 tags per note to avoid clutter
- Frontmatter tags (YAML) for AI compatibility — property-based tags are queryable
- Use `status/` prefix tags for workflow state rather than a separate `status` property (opinionated — some prefer both)

**Sources:** [AI-Native Vault Setup Guide](https://www.curiouslychase.com/posts/ai-native-obsidian-vault-setup-guide), [voidashi vault template](https://github.com/voidashi/obsidian-vault-template)

## Source Conflicts

**Nested YAML**: Dataview documentation says Objects are supported via dot notation in YAML frontmatter, but Obsidian Properties UI cannot display or edit them. Both statements are true — Dataview can query nested YAML that Properties can't render. For future-proofing with Bases, avoid nested YAML entirely.

**Field naming convention**: No community consensus on casing. Steph Ango uses plain lowercase (`author`, `rating`). BBBBlog uses snake_case (`date_start`, `series_name`). Some templates use kebab-case (`last-contact`). The safest choice is lowercase single-word fields where possible, snake_case for compound names.

**Tags vs properties for status tracking**: Some practitioners use `status` as a frontmatter property (text or list), others use `#status/active` tag hierarchy. The tag approach enables Dataview `#status/*` queries; the property approach works better with Bases filters. Using both is redundant but common during migration.

**Type field values**: No standardized vocabulary. Steph Ango uses `daily|weekly|person|project|moc|resource`. The Architect's Guide to Bases uses `Book|Movie|Show|Music|Recipe|Project`. Vault templates use different taxonomies. Pick a set that matches your vault's purpose and document it in CLAUDE.md.

**Inline fields future**: Dataview supports inline fields as a first-class feature, but Bases ignores them entirely. Datacore (Dataview successor) plans to make inline fields opt-in. The trend is strongly toward frontmatter-only metadata.

## Currency Assessment
- Most recent source: February 2026 (forum discussions, MCP servers)
- Topic velocity: Fast-moving — Obsidian Bases is actively changing the query landscape
- Confidence in currency: High for Properties constraints (stable since v1.4), medium for Bases (still in active development with missing features)

## Open Questions
- What are the exact property value length limits in Obsidian Properties?
- How does frontmatter field count affect Properties UI rendering performance on large vaults?
- Will Obsidian Bases ever support nested YAML, or is flat-only the permanent design direction?
- What is the recommended migration path from Dataview inline fields to Bases-compatible frontmatter at scale (10k+ notes)?
- How should CLAUDE.md schema definitions handle version changes when vault conventions evolve?
- What is the performance impact of Linter regex-based YAML parsing on vaults with complex frontmatter?
