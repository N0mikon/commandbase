# OFM Validation Rules

Obsidian Flavored Markdown validation rules for vault linting. Use these to verify notes conform to OFM format constraints.

## Frontmatter Constraints

### Structure
- Must start with `---` on the very first line of the file (no blank lines before it)
- Must end with `---` on its own line
- Content between delimiters must be valid YAML
- No empty lines allowed before the opening `---`
- YAML comments (`# comment`) will be stripped by Obsidian on save

### Property Types
Obsidian supports exactly 6 types. The type is set globally per property name (vault-wide type registry):

| Type | YAML Format | Notes |
|------|-------------|-------|
| Text | `key: value` | Single-line string |
| List | `key: [a, b]` or multiline `- a` | Array of strings |
| Number | `key: 42` | Integer or float |
| Checkbox | `key: true` or `key: false` | Boolean only |
| Date | `key: 2026-02-12` | ISO 8601 date |
| Date & time | `key: 2026-02-12T14:30:00` | ISO 8601 datetime |

### Property Rules
- **No nested YAML objects** — Obsidian renders them as unreadable JSON strings
- **Plural properties**: `tags`, `aliases`, `cssclasses` must use plural form
- **Wikilinks in frontmatter** must be quoted: `related: "[[Other Note]]"`
- **Links in frontmatter** do NOT auto-update on rename (unlike body links)
- Property names: lowercase, kebab-case or snake_case recommended
- One type per property name vault-wide — setting `status` as text in one note means it's text everywhere

## Wikilink Syntax

### Valid Forms
- `[[Note Name]]` — basic link
- `[[Note Name|Display Text]]` — aliased link
- `[[Note Name#Heading]]` — heading link
- `[[Note Name#^block-id]]` — block reference link
- `[[#Heading]]` — same-note heading link
- `[[#^block-id]]` — same-note block reference

### Embed Syntax
- `![[Note Name]]` — embed full note
- `![[image.png]]` — embed image
- `![[image.png|640x480]]` — embed image with dimensions
- `![[image.png|640]]` — embed image with width only
- `![[Note Name#Heading]]` — embed specific section

### Validation Checks
- Target note must exist in vault (check via Glob)
- Heading targets must exist in the target note
- Block IDs must exist in the target note (look for `^block-id` at end of a block)
- No spaces before `[[` in wikilink syntax (breaks rendering)
- No nested wikilinks: `[[a [[b]]]]` is invalid

## Callout Types

13 built-in callout types (case-insensitive):

| Type | Aliases |
|------|---------|
| note | — |
| abstract | summary, tldr |
| info | — |
| todo | — |
| tip | hint, important |
| success | check, done |
| question | help, faq |
| warning | caution, attention |
| failure | fail, missing |
| danger | error |
| bug | — |
| example | — |
| quote | cite |

### Callout Syntax
```markdown
> [!type] Optional title
> Content here

> [!type]+ Foldable (open by default)
> Content here

> [!type]- Foldable (collapsed by default)
> Content here
```

### Validation
- Type must be one of the 13 built-in types or a custom type
- No space between `[!` and the type name
- Title is optional; if omitted, the type name is displayed
- Foldable markers (`+`/`-`) must immediately follow the closing `]`

## Block References

- Format: `^block-id` at the end of any block (paragraph, list item, etc.)
- Block IDs: alphanumeric and hyphens only
- Referenced via `[[Note#^block-id]]` or `![[Note#^block-id]]`
- The `^block-id` is invisible in reading view

## Comments

- Syntax: `%%comment text%%`
- Hidden in reading view, visible in source/live preview
- Can span multiple lines: `%%\nmultiline\n%%`
- Cannot be nested

## Highlights

- Syntax: `==highlighted text==`
- No nesting
- Must open and close on the same line (no multi-line highlights)

## Heading Rules

- H1 (`#`) should appear at most once per note (typically the note title)
- Headings should not skip levels (H1 to H3 without H2 is invalid)
- Obsidian uses headings for outline and linking — skipped levels break navigation
- Heading text becomes the link target for `[[Note#Heading]]` links
- Duplicate headings within a note are allowed but create ambiguous link targets

## Tags

### Frontmatter Tags
```yaml
tags: [tag1, tag2, nested/tag]
```

### Inline Tags
- Format: `#tag-name` in note body
- Allowed characters: alphanumeric, hyphens, underscores, forward slashes (for nesting)
- Cannot start with a number
- Case-insensitive (`#Tag` and `#tag` are the same tag)
- Nested tags: `#parent/child/grandchild`

### Validation
- No spaces in tag names
- No special characters except `-`, `_`, `/`
- Frontmatter tags and inline tags merge into `file.tags`
