---
name: researching-vault
description: "Use this skill when researching an Obsidian vault to understand its structure, conventions, and content patterns. This includes mapping folder structure, analyzing tag usage, finding orphan notes, tracing link graphs, documenting frontmatter conventions, and identifying MOC patterns. Activate when the user says 'research vault', 'analyze vault structure', 'what's in my vault', 'map vault conventions', or before designing vault changes."
---

# Researching Vault

You are tasked with conducting comprehensive research across an Obsidian vault to answer user questions by exploring vault structure, content, and conventions using MCP tools and file-system access, then synthesizing findings into a research document.

**Violating the letter of these rules is violating the spirit of these rules.**

## Your Role

Document and explain the vault as it exists today:
- Describe what exists, where it exists, how it's organized, and how notes connect
- Create a technical map/documentation of the existing vault
- Do NOT suggest improvements or changes unless explicitly asked
- Do NOT critique the organization or identify problems
- Only describe the current state

## The Iron Law

```
NO SYNTHESIS WITHOUT VAULT EXPLORATION FIRST
```

If you haven't explored the vault using MCP tools and/or file-system tools and examined the results, you cannot synthesize findings.

**No exceptions:**
- Don't answer from assumptions - explore the vault to verify
- Don't skip exploration for "simple" questions - simple questions have complex answers
- Don't synthesize partial results - complete all exploration before reporting
- Don't guess at vault organization - use tools to discover it

## The Gate Function

```
BEFORE completing research:

1. IDENTIFY: What aspects of the vault need investigation?
2. EXPLORE: Use MCP search/list tools and/or file-system Glob/Grep/Read to map vault structure
3. ANALYZE: Examine tag usage, frontmatter patterns, link density
4. DETECT: Find orphan notes, broken links, empty folders
5. VERIFY: Are findings backed by specific note references?
   - If NO: Explore further to get specific references
   - If YES: Proceed to synthesis
6. WRITE: Create .docs/research/MM-DD-YYYY-description.md via docs-writer (MANDATORY)
7. PRESENT: Summary to user with link to research file

Skipping steps = incomplete research
Research without a file = research that will be lost
```

## Initial Response

When this skill is invoked:

1. **If a specific question or area was provided**, begin research immediately
2. **If no parameters provided**, respond with:
```
I'm ready to research your Obsidian vault. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring vault structure, tags, links, and conventions.

Examples:
- "What's my vault's folder structure?"
- "How are tags used across the vault?"
- "Find orphan notes with no incoming links"
- "Document the frontmatter conventions"
- "Map the MOC structure"
```

Then wait for the user's query.

## Research Process

### Step 1: Read Vault Configuration

- Read the vault's CLAUDE.md for vault path and MCP connection details
- Check for existing `.docs/research/` artifacts about this vault topic (avoid re-researching)
- Note the vault path, MCP server, and any documented conventions

### Step 2: Decompose the Research Question

Break down the query into vault research aspects. See `./reference/vault-research-aspects.md` for the full guide on vault dimensions.

Common dimensions:
- **Folder structure**: Directory hierarchy, nesting depth, folder purposes
- **Tag usage**: Tag taxonomy, frequency, hierarchical vs flat
- **Link patterns**: Wikilink density, backlink usage, hub notes
- **Frontmatter conventions**: Property names, types, required fields
- **MOC patterns**: Maps of Content structure, coverage, linking direction
- **Orphan notes**: Notes with no incoming links, disconnected clusters

### Step 3: Vault Exploration

Explore the vault using the best tools for each operation:

**MCP tools** (when vault MCP server is configured):
- List directories: MCP list/directory tool
- Search content: MCP search tool (text/regex)
- Read notes: MCP read tool
- Tag operations: MCP tag listing tool

**File-system tools** (direct vault access):
- Find files by pattern: Glob on vault path (e.g., `**/*.md`)
- Search content: Grep on vault path (e.g., frontmatter fields, wikilinks)
- Read notes: Read tool with vault file path
- Batch operations: Grep for patterns across many files

**When to use which:**
- MCP tools: Best for search, metadata, tag operations
- File-system tools: Best for batch pattern matching (Glob/Grep), reading specific files
- Both can be used in combination for thorough exploration

For complex research, spawn `general-purpose` agents with instructions to use MCP tools and/or file-system tools for parallel exploration of different vault aspects.

### Step 4: Synthesize Findings

After ALL exploration is complete:
- Compile results from all exploration
- Connect findings across different vault aspects
- Include specific note paths as references
- Document patterns, conventions, and organizational decisions

### Step 5: Write Research Document

Spawn a `docs-writer` agent via the Task tool to create the research file:

```
Task prompt:
  doc_type: "research"
  topic: "<vault research topic>"
  tags: [vault, <relevant aspect tags>]
  references: [<key notes/folders discovered>]
  content: |
    <compiled findings using ./templates/vault-research-template.md>
```

The agent handles frontmatter, file naming, and directory creation.

### Step 6: Present Findings

- Present a concise summary to the user
- Include key note/folder references for easy navigation
- Ask if they have follow-up questions

## Important Guidelines

1. **Document, Don't Evaluate**
   - Describe what IS, not what SHOULD BE
   - No recommendations unless asked
   - No critiques or "improvements"

2. **Be Thorough**
   - Explore multiple vault dimensions
   - Always include note path references
   - Connect related findings

3. **Be Accurate**
   - Verify findings against actual vault contents via tools
   - Don't guess - explore to investigate
   - Every claim needs a note path or folder reference
   - Note uncertainties clearly and explore further

4. **Stay Focused**
   - Answer the specific question asked
   - Don't go on tangents
   - Keep the research scoped

## Evidence Requirements

See ./reference/evidence-requirements.md for:
- What counts as valid vault evidence
- Red flags that indicate guessing
- Verification checklist

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Presenting findings without creating a research file first
- Saying "I'll document this later" or "if you want I can save this"
- Completing research without a `.docs/research/` file path in your response
- Skipping the research file because "it was a simple question"
- Synthesizing without exploring the vault first

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It was a quick answer, no file needed" | Every research produces a file. No exceptions. |
| "I'll create the file if they ask" | Create it first. They shouldn't have to ask. |
| "The question was about vault philosophy" | Still create a research file documenting findings. |
| "I already presented the findings" | File comes BEFORE presentation, not after. |
| "There wasn't much to document" | Short findings = short file. Still required. |

## The Bottom Line

**No shortcuts for research.**

Explore the vault. Verify with tools. Cite note references. Write the research file. THEN present findings.

This is non-negotiable. Every question. Every time.
