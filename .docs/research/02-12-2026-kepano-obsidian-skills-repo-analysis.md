---
date: 2026-02-12
status: final
topic: "kepano/obsidian-skills Repository Analysis"
tags: [research, repo-analysis, obsidian, claude-skills, markdown, canvas, bases]
git_commit: 9c4c7f4
references:
  - skills/obsidian-markdown/SKILL.md
  - skills/obsidian-bases/SKILL.md
  - skills/json-canvas/SKILL.md
  - skills/obsidian-cli/SKILL.md
  - skills/defuddle/SKILL.md
---

# kepano/obsidian-skills Repository Analysis

## Repository Overview

- **Source**: https://github.com/kepano/obsidian-skills
- **Author**: Steph Ango (Obsidian CEO, stephango.com)
- **License**: MIT
- **Plugin Name**: `obsidian` (version 1.0.0)
- **Description**: "Create and edit Obsidian vault files including Markdown, Bases, and Canvas"
- **Architecture**: Claude Code plugin with marketplace manifest
- **Total Lines**: 2,071 across 5 skills
- **Commit History**: ~20 commits, community contributions accepted (PRs merged from multiple authors)
- **Agent Skills Spec**: Aligned with agentskills.io specification for cross-agent compatibility (Claude Code + Codex CLI)

## Directory Structure

```
obsidian-skills/
├── .claude-plugin/
│   ├── marketplace.json    # Single-plugin marketplace
│   └── plugin.json         # Plugin manifest (name: "obsidian")
├── LICENSE                 # MIT
├── README.md              # Installation + skill table
└── skills/
    ├── defuddle/SKILL.md       (41 lines)
    ├── json-canvas/SKILL.md    (656 lines)
    ├── obsidian-bases/SKILL.md (651 lines)
    ├── obsidian-cli/SKILL.md   (103 lines)
    └── obsidian-markdown/SKILL.md (620 lines)
```

## Skill-by-Skill Analysis

### 1. obsidian-markdown (620 lines) — Format Reference

**Purpose**: Comprehensive Obsidian Flavored Markdown syntax reference for Claude to create/edit .md files.

**Coverage**:
- Basic formatting (paragraphs, headings, bold/italic/highlight/strikethrough)
- Internal links (wikilinks): `[[Note]]`, `[[Note#Heading]]`, `[[Note#^block-id]]`, search links `[[##heading]]`
- Markdown-style links with URL encoding
- Embeds: notes, images (with dimensions), audio, PDFs (with page targeting), lists, search results via query blocks
- Callouts: all 13 built-in types with aliases, foldable (+/-), nested, custom CSS
- Lists: unordered, ordered, task lists with nesting
- Code: inline, blocks with language, nesting with extra backticks
- Tables: basic, alignment, pipe escaping in wikilinks
- Math: inline/block LaTeX
- Mermaid diagrams: flowcharts, sequence diagrams
- Footnotes: numbered, named, inline
- Comments: `%%hidden%%`
- Properties/frontmatter: full YAML spec with property types (text, number, checkbox, date, datetime, list, links)
- Tags: syntax rules, nesting with `/`, in-body and frontmatter forms
- HTML support
- Complete example note tying everything together
- Reference links to official Obsidian docs

**Pattern**: Pure reference documentation. No workflow guidance, no "when to use what." Designed as a lookup table for an AI to produce valid OFM syntax.

**Strengths**: Thorough coverage of ALL OFM extensions. Excellent callout type table. Good embed variants. The complete example at the end is well-designed.

**Gaps**: No guidance on linking conventions (when to wikilink vs markdown link), no template patterns, no MOC/index patterns, no discussion of aliases or YAML edge cases.

### 2. obsidian-bases (651 lines) — Format Reference

**Purpose**: Complete .base file format specification for Obsidian Bases (database views of notes).

**Coverage**:
- File format: YAML in .base files
- Complete schema: filters, formulas, properties, summaries, views
- Filter syntax: single filters, AND/OR/NOT, nested filters, operators
- Three property types: note properties (frontmatter), file properties, formula properties
- File properties reference: 12 properties (name, path, folder, ext, size, ctime, mtime, tags, links, backlinks, embeds, properties)
- `this` keyword semantics (base file vs embedded context vs sidebar)
- Formula syntax with examples (arithmetic, conditional, string formatting, date formatting, duration calculations)
- **Comprehensive function reference** (50+ functions organized by type):
  - Global: date(), duration(), now(), today(), if(), min(), max(), number(), link(), list(), file(), image(), icon(), html(), escapeHTML()
  - Any type: isTruthy(), isType(), toString()
  - Date: fields (year/month/day/hour/minute/second/millisecond), format(), time(), relative(), isEmpty()
  - Duration type: days/hours/minutes/seconds/milliseconds fields (with explicit warning about .round() not working on Duration directly)
  - Date arithmetic: duration units, add/subtract, date subtraction returning Duration
  - String: 15 functions (contains, startsWith, endsWith, lower, title, trim, replace, repeat, reverse, slice, split, etc.)
  - Number: abs, ceil, floor, round, toFixed, isEmpty
  - List: 16 functions (contains, filter, map, reduce, flat, join, reverse, slice, sort, unique, isEmpty, etc.)
  - File: asLink, hasLink, hasTag, hasProperty, inFolder
  - Link: asFile, linksTo
  - Object: isEmpty, keys, values
  - Regex: matches
- View types: table, cards, list, map (with note that map requires community plugin)
- Default summary formulas: 15 built-in (Average, Min, Max, Sum, Range, Median, Stddev, Earliest, Latest, Checked, Unchecked, Empty, Filled, Unique)
- 4 complete examples: Task Tracker, Reading List, Project Notes, Daily Notes Index
- Embedding syntax
- YAML quoting rules

**Pattern**: Exhaustive format specification. This is the kind of document you'd write to teach an AI a new file format from scratch. Very well organized.

**Strengths**: The function reference is remarkably thorough. The Duration type documentation (contributed via PR) fixes a common pitfall. The 4 complete examples cover diverse use cases. YAML quoting rules section prevents common errors.

**Gaps**: No discussion of performance with large vaults, no mention of Bases limitations, no guidance on when to use Bases vs Dataview.

### 3. json-canvas (656 lines) — Format Reference

**Purpose**: Complete JSON Canvas 1.0 specification for .canvas file creation/editing.

**Coverage**:
- File structure: nodes[] + edges[]
- Z-index ordering semantics
- Generic node attributes (id, type, x, y, width, height, color)
- 4 node types with full attribute tables:
  - Text: Markdown content, newline escaping pitfall documented
  - File: vault file references with subpath (heading/block targeting)
  - Link: external URLs
  - Group: labels, background images, background styles (cover/ratio/repeat)
- Edges: full attribute table (fromNode, toNode, fromSide, toSide, fromEnd, toEnd, color, label)
- Side values (top/right/bottom/left)
- End shapes (none/arrow)
- Colors: hex and preset (1-6 mapping to Red/Orange/Yellow/Green/Cyan/Purple)
- 4 complete examples: Simple text + connections, Project board with groups, Research canvas with files + links, Flowchart
- ID generation: 16-char hex format
- Layout guidelines: positioning, recommended sizes, spacing
- 8 validation rules

**Pattern**: Spec-faithful reference. Follows the JSON Canvas 1.0 spec closely. The examples are excellent for showing spatial layout conventions.

**Strengths**: The newline escaping pitfall note (contributed via PR) is a valuable addition. Layout guidelines with recommended pixel sizes is very practical. Validation rules give Claude guardrails.

**Gaps**: No discussion of canvas-to-note linking patterns, no mention of canvas plugins/extensions.

### 4. obsidian-cli (103 lines) — Tool Reference

**Purpose**: Quick reference for the `obsidian` CLI command for vault interaction and plugin development.

**Coverage**:
- Command syntax: parameters (key=value) and flags (boolean)
- File targeting: `file=<name>` (wikilink-style) vs `path=<path>` (exact)
- Vault targeting: `vault=<name>`
- Common patterns: read, create, append, search, daily notes, properties, tasks, tags, backlinks
- Plugin development: plugin:reload, eval, dev:errors, dev:console, dev:screenshot, dev:dom, dev:css, dev:mobile
- Utility flags: --copy, silent, total

**Pattern**: Lean tool reference. Points to `obsidian help` as the canonical source. Just enough to get Claude oriented.

**Strengths**: Very concise. The plugin development section is unique — enables Claude to act as a plugin dev assistant. The file vs path targeting distinction is well explained.

**Gaps**: No exhaustive command list (defers to `obsidian help`). No examples of complex workflows. No error handling guidance.

### 5. defuddle (41 lines) — Tool Reference

**Purpose**: Quick reference for Defuddle CLI, a web content extraction tool.

**Coverage**:
- Installation: `npm install -g defuddle-cli`
- Usage: `defuddle parse <url> --md`
- Output formats: --md, --json, none (HTML), -p for specific metadata
- Save to file: -o flag
- Metadata extraction: title, description, domain

**Pattern**: Minimal tool stub. This is essentially a "use this instead of WebFetch" directive with the basic syntax.

**Strengths**: Smart skill description — "Use instead of WebFetch" gives Claude clear tool selection guidance.

**Gaps**: No error handling, no rate limiting guidance, no examples of chaining with other tools.

## Design Patterns Observed

### Skill Structure Pattern
All skills follow a consistent structure:
1. YAML frontmatter with `name` and `description` (Agent Skills spec)
2. H1 title
3. Brief overview/purpose
4. Reference documentation organized by feature
5. Complete examples section
6. References section with official doc links

### Two Skill Categories
1. **Format References** (obsidian-markdown, obsidian-bases, json-canvas): Exhaustive syntax documentation teaching Claude a file format. 600-660 lines each.
2. **Tool References** (obsidian-cli, defuddle): Concise CLI usage guides. 40-100 lines. Point to external help for completeness.

### Frontmatter Pattern
Minimal frontmatter — only `name` and `description`. No version, no author, no tags, no dependencies. The `description` field doubles as the skill's invocation trigger (tells Claude when to use it).

### No Workflow Logic
These skills contain zero workflow instructions. They don't tell Claude *when* to create a note or *how* to organize a vault. They are purely "here is the syntax/format" references. This is a deliberate design choice — format knowledge is separated from workflow knowledge.

### Community Contribution Pattern
Multiple community PRs merged:
- Duration type documentation fix
- JSON newline escaping pitfall
- Agent Skills spec alignment for Codex compatibility
- Claude Code skill discovery fix (standardizing skills/ layout)
- Maps community plugin clarification

## Relevance to commandbase-vault

### Complementary, Not Competing
- **kepano/obsidian-skills**: Teaches Claude *what valid Obsidian files look like* (format/syntax)
- **commandbase-vault**: Teaches Claude *how to manage a vault* (workflow/process)

These are orthogonal concerns. A vault management workflow needs format knowledge to produce valid output, but format knowledge alone doesn't produce good vault organization.

### Integration Opportunities
1. **obsidian-markdown** syntax knowledge could be embedded in or referenced by commandbase-vault's implementing-vault and importing-vault skills
2. **obsidian-bases** could enable a "create database views" capability in vault implementation
3. **obsidian-cli** could be used by commandbase-vault skills for vault interaction instead of the MCP server (direct CLI vs REST API)
4. **json-canvas** could enable visual vault mapping features
5. **defuddle** could improve the importing-vault skill's web content ingestion

### Key Takeaway
kepano's skills are **reference materials** that an AI consults while executing. commandbase-vault skills are **workflow procedures** that guide an AI through multi-step processes. The two plugin suites serve fundamentally different purposes and could work together.
