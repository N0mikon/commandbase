---
name: connecting-vault
description: "Use this skill when discovering relationships between vault notes, maintaining Maps of Content, or improving vault connectivity. This includes suggesting wikilinks between related notes, identifying orphaned notes needing connections, updating or generating MOCs, detecting duplicate or near-duplicate notes, and analyzing link graph density. Activate when the user says 'connect notes', 'find related notes', 'update MOC', 'find orphans', 'link suggestions', or 'vault graph analysis'."
---

# Connecting Vault

You are discovering and strengthening relationships between notes in an Obsidian vault. This skill finds connections that aren't yet explicit — related notes that should be linked, orphans that need rescue, MOCs that need updating, and duplicates that should be merged.

**Violating the letter of these rules is violating the spirit of these rules.**

## The Iron Law

```
NO CONNECTION SUGGESTIONS WITHOUT VERIFYING TARGET NOTES EXIST
```

Every wikilink suggestion must point to a real, existing note. Suggesting links to non-existent notes creates broken links instead of connections.

**No exceptions:**
- Don't suggest `[[Note]]` without Glob-verifying `Note.md` exists
- Don't assume MOCs are current — read them before suggesting additions
- Don't suggest merges without reading both candidate notes
- Don't modify notes without user approval — suggest, don't act

## The Gate Function

```
BEFORE suggesting any connections:

1. READ: Vault CLAUDE.md for conventions, MOC strategy, tag taxonomy
2. SCOPE: Determine mode (link suggestions/orphan rescue/MOC maintenance/duplicate detection)
3. SEARCH: Use MCP semantic search (preferred) or Grep keyword matching (fallback)
4. VERIFY: Confirm all suggested targets exist in the vault
5. PRESENT: Show suggestions with evidence (why these notes are related)
6. ONLY THEN: Apply changes if user approves

Skip target verification = broken link suggestions = worse than no suggestions
```

## Search Strategy

**MCP-preferred path:** When MCP tools are available, use semantic search for content-aware matching. This finds conceptual relationships that keyword matching misses.

**Grep fallback path:** When MCP is not available, use Grep-based strategies from ./reference/connection-strategies.md — shared tags, keyword overlap, backlink analysis, frontmatter matching.

Both paths are documented in the reference. Always try MCP first, fall back to Grep if MCP is unavailable or returns no results.

## Modes

### Mode A: Link Suggestions

Use this mode to find connections for specific notes (recent or user-specified).

**Steps:**
1. Read vault CLAUDE.md for conventions
2. Identify target notes (from argument, or recently created/modified notes)
3. For each target note:
   - Extract tags, keywords, headings, existing links
   - Run connection strategies from ./reference/connection-strategies.md
   - Score and rank candidates
4. Present suggestions with evidence:
   ```
   [[Source Note]] might connect to:
   - [[Candidate 1]] — 3 shared tags, 2 keyword matches (score: 11)
   - [[Candidate 2]] — shared backlinks to [[Common Target]] (score: 6)
   ```
5. If user approves, add wikilinks to the source note

### Mode B: Orphan Rescue

Use this mode to find notes with zero incoming links and suggest connections.

**Steps:**
1. Read vault CLAUDE.md for MOC strategy
2. Find orphan notes (notes with no incoming `[[wikilinks]]` from other notes)
3. For each orphan:
   - Run rescue strategies: tag-based, folder siblings, MOC addition, title search
   - Find the best connection point
4. Present rescue suggestions:
   ```
   Orphan: [[Unlinked Note]]
   Rescue options:
   - Add to [[Topic MOC]] (matching tags: #topic)
   - Link from [[Related Note]] (keyword overlap: "api", "endpoints")
   ```
5. If user approves, add the wikilinks

### Mode C: MOC Maintenance

Use this mode to refresh existing MOCs or generate new ones for topic clusters.

**Steps:**
1. Read vault CLAUDE.md for MOC conventions
2. If maintaining existing MOC:
   - Read the MOC, extract all current links
   - Find notes matching the MOC's topic that aren't yet linked
   - Check for stale links (targets that no longer exist)
   - Present additions and removals
3. If generating new MOC:
   - Identify the topic cluster (from argument or tag-based grouping)
   - Find all notes belonging to the cluster
   - Organize into logical sections
   - Present draft MOC for user review
4. Apply changes after user approval

### Mode D: Duplicate Detection

Use this mode to find notes that may be duplicates or near-duplicates.

**Steps:**
1. Collect note names in scope (full vault or specified folder)
2. Run duplicate strategies from ./reference/connection-strategies.md:
   - Title similarity (normalized name comparison)
   - Same-day creation with similar titles
   - Content overlap for candidate pairs
3. Present findings:
   ```
   Potential duplicates:
   - "API Guide" (resources/) and "api-guide" (notes/) — same normalized name
     Recommendation: merge into single note at [location]
   ```
4. If user approves merge, consolidate content and update references

## Important Guidelines

1. **Suggest, don't act**: Present connection suggestions for user approval before making changes
2. **Show evidence**: Every suggestion must include WHY the connection was suggested
3. **Verify existence**: Every `[[wikilink]]` suggestion must point to a verified existing note
4. **Respect vault structure**: Follow the vault's MOC strategy and linking conventions
5. **Batch size**: For large vaults, process in manageable batches (20-30 notes per pass)

## Red Flags - STOP and Verify

If you notice any of these, pause:

- Suggesting wikilinks to notes you haven't verified exist
- Modifying MOCs without reading them first
- Running duplicate detection without content comparison (title alone is insufficient)
- Adding connections without user approval
- Ignoring the vault's MOC strategy when suggesting where to add links

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "This note probably exists" | Verify with Glob. Probably isn't evidence. |
| "All orphans need connections" | Some notes are intentionally standalone. Suggest, don't force. |
| "MOC is too long to read" | Read it. You need to know what's already linked. |
| "These are obviously duplicates" | Read both notes. Similar titles don't guarantee duplicate content. |
| "I'll verify links after adding them" | Verify before. Broken links are worse than no links. |

## The Bottom Line

**Search with evidence. Verify targets. Suggest with reasons. Let the user decide.**

Connections are the vault's neural pathways — they turn isolated notes into a knowledge network. This is non-negotiable. Every suggestion. Every time.
