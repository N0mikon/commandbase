# OFM Note Formats

Valid Obsidian Flavored Markdown patterns for creating captured notes. Use these to ensure captured content renders correctly in Obsidian.

## Frontmatter

### Valid Structure
```yaml
---
type: resource
created: 2026-02-12
tags: [topic/subtopic, status/inbox]
source: "https://example.com"
aliases: [alternate name]
---
```

### Property Type Constraints
Obsidian supports exactly 6 property types (global per property name):

| Type | Format | Example |
|------|--------|---------|
| Text | `key: value` | `title: My Note` |
| List | `key: [a, b]` | `tags: [project, active]` |
| Number | `key: 42` | `priority: 1` |
| Checkbox | `key: true` | `completed: false` |
| Date | `key: 2026-02-12` | `created: 2026-02-12` |
| Date & time | `key: 2026-02-12T14:30:00` | `meeting-time: 2026-02-12T14:30:00` |

### Rules
- No nested YAML objects (Obsidian renders them as unreadable JSON)
- `tags`, `aliases`, `cssclasses` must be plural form
- Wikilinks in frontmatter must be quoted: `related: "[[Other Note]]"`
- No empty lines before the opening `---`

## Wikilinks

### Basic Links
- `[[Note Name]]` — link to a note
- `[[Note Name|Display Text]]` — link with custom display text
- `[[Note Name#Heading]]` — link to a specific heading
- `[[Note Name#^block-id]]` — link to a specific block

### Rules for Captured Notes
- Only create wikilinks to notes you've verified exist in the vault
- If unsure whether a target exists, use plain text instead
- For web captures, use standard markdown links for external URLs: `[text](url)`
- Wikilinks are for internal vault connections only

## Embeds

- `![[Note Name]]` — embed full note content
- `![[image.png]]` — embed image
- `![[image.png|640]]` — embed image with width
- `![[Note Name#Heading]]` — embed specific section

Use embeds sparingly in captured notes. Prefer wikilinks for connections.

## Callouts

For structuring captured content (source attribution, warnings, key points):

```markdown
> [!info] Source
> Captured from [Title](url) on 2026-02-12

> [!tip] Key Takeaway
> The main insight from this content.

> [!warning] Needs Review
> This content hasn't been verified.

> [!quote] Notable Quote
> "Quoted text from the source."
```

### 13 Built-in Types
note, abstract (summary, tldr), info, todo, tip (hint, important), success (check, done), question (help, faq), warning (caution, attention), failure (fail, missing), danger (error), bug, example, quote (cite)

## Tags

### In Frontmatter (Preferred)
```yaml
tags: [topic/subtopic, status/inbox]
```

### Inline (For Block-Level Annotation)
```markdown
This paragraph is about #topic/specific-point
```

### Rules
- Lowercase only
- No spaces (use hyphens: `#my-tag`)
- Nested with forward slash: `#parent/child`
- Cannot start with a number
- Frontmatter tags describe the whole note
- Inline tags annotate specific blocks

## Block References

To make a block linkable from other notes:
```markdown
This is a notable paragraph. ^my-block-id
```

Referenced via `[[Note#^my-block-id]]`. Use sparingly — most captured notes don't need block references.

## Comments

```markdown
%%This text is hidden in reading view%%
```

Useful for capture metadata that shouldn't render:
```markdown
%%Captured by /capturing-vault on 2026-02-12%%
%%Original URL: https://example.com/article%%
```

## Highlights

```markdown
This is ==highlighted text== that stands out.
```

Use for key phrases in captured content.

## Note Templates by Capture Mode

### Fleeting Note
```markdown
---
type: fleeting
created: [date]
tags: []
status: inbox
---

# [Brief Title]

[Idea or thought captured quickly]

## Context
[What prompted this thought, if relevant]
```

### Web Capture
```markdown
---
type: resource
created: [date]
source: "[url]"
tags: []
status: inbox
---

# [Article Title]

> [!info] Source
> Captured from [Title](url) on [date]

## Summary
[Key points from the article]

## Notes
[Your annotations and connections]
```

### Meeting Note
```markdown
---
type: meeting
created: [date]
participants: []
tags: []
status: inbox
---

# [Meeting Name] — [date]

## Attendees
- [Person 1]
- [Person 2]

## Agenda
1. [Topic 1]
2. [Topic 2]

## Notes
[Discussion notes]

## Action Items
- [ ] [Action] — assigned to [person] — due [date]
```

### Log Entry
```markdown
---
type: log
created: [date]
tags: []
---

# [date] — [optional topic]

[Log content]
```
