# Vault Research Aspects

Guide to vault research dimensions and tool usage for each.

## Research Dimensions

### Folder Structure
**What to investigate:** Directory hierarchy, nesting depth, folder purposes, empty folders.

**MCP tools:**
- List vault root to get top-level structure
- List each directory recursively for full tree

**File-system tools:**
- `Glob("**/*.md", path=vault_path)` to find all markdown files
- `Glob("**/", path=vault_path)` to find all directories

**Output format:** Folder tree with note counts per directory.

---

### Tag Usage
**What to investigate:** Tag taxonomy, frequency, hierarchical vs flat, property vs inline tags.

**MCP tools:**
- MCP tag listing tool for vault-wide tag inventory
- MCP search for specific tag usage contexts

**File-system tools:**
- `Grep("tags:", path=vault_path, glob="*.md")` for frontmatter tags
- `Grep("#[a-zA-Z]", path=vault_path, glob="*.md")` for inline tags
- `Grep("tags:.*\\[", path=vault_path, glob="*.md")` for YAML list tags

**Output format:** Tag taxonomy tree with usage counts and example notes.

---

### Link Patterns
**What to investigate:** Wikilink density, backlink usage, hub notes (high link count), link direction patterns.

**MCP tools:**
- MCP search for `[[` patterns
- MCP read specific notes to count links

**File-system tools:**
- `Grep("\\[\\[", path=vault_path, glob="*.md", output_mode="count")` for link density per file
- `Grep("\\[\\[specific-note\\]\\]", path=vault_path)` for backlink discovery

**Output format:** Link density statistics, hub notes identified, link direction patterns.

---

### Frontmatter Conventions
**What to investigate:** Property names, types, required vs optional fields, consistency across note types.

**MCP tools:**
- MCP read sample notes from each folder for frontmatter inspection

**File-system tools:**
- `Grep("^---", path=vault_path, glob="*.md")` to find files with frontmatter
- `Grep("^[a-z_]+:", path=vault_path, glob="*.md")` to discover property names
- Read specific notes to inspect full frontmatter blocks

**Output format:** Frontmatter schema per note type, with required/optional/frequency analysis.

---

### MOC Patterns
**What to investigate:** Maps of Content structure, coverage, linking direction (MOC→notes or notes→MOC), dynamic vs static MOCs.

**MCP tools:**
- MCP search for "MOC" or "Map of Content" or "Index" in note titles/content

**File-system tools:**
- `Glob("**/MOC*.md", path=vault_path)` or `Glob("**/*Index*.md", path=vault_path)`
- `Grep("MOC|Map of Content|Index", path=vault_path, glob="*.md")`
- Read identified MOCs to analyze link structure

**Output format:** MOC inventory, coverage analysis, linking patterns.

---

### Orphan Notes
**What to investigate:** Notes with no incoming links, disconnected clusters, notes not reachable from any MOC.

**MCP tools:**
- MCP search to find all note names, then search for `[[name]]` references

**File-system tools:**
- `Glob("**/*.md", path=vault_path)` to list all notes
- For each note: `Grep("\\[\\[note-name\\]\\]", path=vault_path)` to check for incoming links

**Output format:** Orphan note list with creation dates and folder locations.

---

### Plugins
**What to investigate:** Installed plugins, plugin configuration, plugin-generated content.

**File-system tools:**
- `Glob(".obsidian/plugins/*/manifest.json", path=vault_path)` to list installed plugins
- Read manifest.json for each to get plugin names and versions

**Output format:** Plugin inventory with names, versions, and brief descriptions.

## Parallel vs Sequential Exploration

**Explore in parallel** when:
- Researching independent aspects (tags AND folder structure)
- Each exploration can work independently
- Maximizing coverage quickly

**Explore sequentially** when:
- Later exploration needs earlier results (find MOCs, then analyze their link structure)
- Following a chain of connections
- Drilling deeper based on initial findings

## Example Queries and Approaches

| User Query | Primary Dimensions | Approach |
|-----------|-------------------|----------|
| "What's in my vault?" | Folder structure, note count, tag overview | Parallel: folder tree + tag inventory + note count |
| "How are notes connected?" | Link patterns, MOC patterns, orphans | Sequential: find hubs → trace connections → find orphans |
| "Document conventions" | Frontmatter, tags, naming, structure | Parallel: all dimensions, compile into conventions doc |
| "Find orphan notes" | Orphan detection | Sequential: list all → check incoming links → report |
