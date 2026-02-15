# Connection Strategies

Techniques for discovering relationships between vault notes. Use these strategies in order of reliability — start with strongest signals, fall back to weaker ones.

## Search Strategy: MCP-Preferred, Grep Fallback

**Primary path (MCP available):**
Use MCP semantic search tools for content-aware matching. These understand meaning, not just keywords.

**Fallback path (filesystem only):**
Use Grep-based keyword and tag matching. Less accurate for semantic similarity but works without MCP.

All strategies below document both paths where applicable.

## Strategy 1: Shared Tags

**Strength:** High — tags are explicit categorization signals.

**Procedure:**
1. Extract tags from the source note (frontmatter + inline)
2. Search vault for other notes with matching tags:
   - MCP: semantic search for tag values
   - Grep: `Grep("tags:.*target-tag", path=vault_path, glob="*.md")` for frontmatter tags
   - Grep: `Grep("#target-tag", path=vault_path, glob="*.md")` for inline tags
3. Rank matches by number of shared tags
4. Exclude notes already linked from the source

**Best for:** Finding topically related notes.

## Strategy 2: Keyword Overlap

**Strength:** Medium — keywords in titles and headings indicate related topics.

**Procedure:**
1. Extract significant keywords from the source note (title, H1, H2 headings)
2. Strip common words (the, a, an, is, are, etc.)
3. Search vault for each keyword:
   - MCP: semantic search with keyword as query
   - Grep: `Grep("keyword", path=vault_path, glob="*.md")` for each keyword
4. Score notes by keyword hit count
5. Filter to notes with 2+ keyword matches for higher confidence

**Best for:** Finding notes about similar topics that may use different tags.

## Strategy 3: Frontmatter Field Matching

**Strength:** Medium-high — structured metadata provides reliable signals.

**Procedure:**
1. Read the source note's frontmatter
2. Identify matchable fields: `type`, `project`, `category`, `related`, `source`
3. Search for notes with matching field values:
   - Grep: `Grep("project: target-project", path=vault_path, glob="*.md")`
4. Group matches by field type

**Best for:** Finding notes in the same project, category, or from the same source.

## Strategy 4: Temporal Proximity

**Strength:** Low-medium — notes created around the same time may be related.

**Procedure:**
1. Get the source note's creation date (from `created` frontmatter or file metadata)
2. Find notes created within a narrow window (same day, same week)
3. Present as potential connections with low confidence

**Best for:** Contextual connections — "what else was I working on when I wrote this?"

## Strategy 5: Heading Similarity

**Strength:** Medium — similar headings suggest similar structure/topic.

**Procedure:**
1. Extract all headings from the source note
2. For each heading, search for similar headings in other notes:
   - Grep: `Grep("^#{1,3}.*keyword", path=vault_path, glob="*.md")`
3. Notes with multiple heading overlaps are strong candidates

**Best for:** Finding notes with parallel structure (e.g., all meeting notes, all project plans).

## Strategy 6: Backlink Analysis

**Strength:** High — notes that link to the same targets are likely related.

**Procedure:**
1. Extract all wikilinks from the source note
2. For each linked target, find other notes that also link to it:
   - Grep: `Grep("\\[\\[target-name", path=vault_path, glob="*.md")`
3. Notes that share 2+ link targets with the source are strong candidates
4. The more shared targets, the stronger the connection

**Best for:** Finding notes in the same knowledge neighborhood.

## Scoring and Ranking

When combining strategies, use weighted scoring:

| Strategy | Weight | Rationale |
|----------|--------|-----------|
| Shared tags | 3 | Explicit categorization |
| Backlink overlap | 3 | Strong structural signal |
| Frontmatter match | 2 | Structured metadata |
| Keyword overlap | 2 | Topic similarity |
| Heading similarity | 1 | Structural similarity |
| Temporal proximity | 1 | Weak contextual signal |

**Threshold for suggestion:** Score >= 3 for confident suggestions.

## Orphan Rescue Strategies

For notes with zero incoming links:

1. **Tag-based rescue**: Find notes with matching tags → suggest adding a wikilink
2. **Folder siblings**: Other notes in the same folder → suggest cross-linking
3. **MOC addition**: Find the most relevant MOC → suggest adding the orphan
4. **Title-based search**: Search for the orphan's title keywords in other notes → found mentions without links should become wikilinks

## MOC Maintenance Strategies

For keeping Maps of Content current:

1. **Gap detection**: Compare MOC's linked notes vs all notes with matching tags → find unlinked matches
2. **Stale link check**: Verify all wikilinks in the MOC still resolve
3. **New note integration**: For recently created notes, find matching MOCs → suggest additions
4. **Section organization**: If MOC has sections, suggest where new notes fit based on tags/content

## Duplicate Detection Strategies

For finding notes that may be duplicates:

1. **Title similarity**: Normalize note names (lowercase, strip punctuation) → group identical names
2. **Content overlap**: Compare first 200 words of notes with similar titles → high overlap = likely duplicate
3. **Same-day creation**: Notes with similar titles created on the same day → likely duplicates from different capture sessions
4. **Merge suggestions**: When duplicates found, suggest which note to keep and what to merge from the other
